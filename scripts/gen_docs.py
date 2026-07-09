#!/usr/bin/env python3
"""Build the Fumadocs content tree for the IDM documentation site.

This script owns website/content/docs entirely. On each run it:

- imports the hand written prose from docs/*.md (common base + one page per
  component type) as MDX guides, rewriting their links,
- generates one schema reference page per component from schema/*.json plus a
  reference index, walking the JSON Schema so the reference cannot drift,
- writes the authored overview, standards and contributing pages,
- writes the meta.json files that drive the sidebar nav.

It is deterministic and safe to re-run. Run from the repo root:

    python scripts/gen_docs.py
"""

import json
import glob
import os
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_DIR = os.path.join(ROOT, "schema")
EXAMPLE_DIR = os.path.join(ROOT, "examples")
SRC_DOCS = os.path.join(ROOT, "docs")
CONTENT = os.path.join(ROOT, "content", "docs")
GH_BLOB = ("https://github.com/Direct-Energy-Partners/interoperability-data-model"
           "/blob/main")

# type key -> (title, indicator), in the display order used across the site.
COMPONENTS = [
    ("battery", "Battery", "BAT"),
    ("cable", "Cable", "WIRE"),
    ("capacitor", "Capacitor", "C"),
    ("breaker", "Circuit Breaker", "Q"),
    ("combinerBox", "Combiner Box", "A"),
    ("contactor", "Contactor", "K"),
    ("converter", "Converter", "U"),
    ("currentTransducer", "Current Transducer", "CT"),
    ("diode", "Diode", "D"),
    ("disconnect", "Disconnect", "Q"),
    ("charger", "EV Charger", "CHG"),
    ("fuelCell", "Fuel Cell", "FC"),
    ("fuse", "Fuse", "F"),
    ("generator", "Generator", "G"),
    ("grounding", "Grounding", "GND"),
    ("hvac", "HVAC", "HVAC"),
    ("hydro", "Hydro", "HYDRO"),
    ("light", "Light", "LIGHT"),
    ("load", "Load", "LOAD"),
    ("meter", "Meter", "P"),
    ("motor", "Motor", "M"),
    ("panel", "Panel Switchboard", "A"),
    ("powerDistributionUnit", "Power Distribution Unit", "PDU"),
    ("precharge", "Precharge", "PRE"),
    ("rapidShutdownDevice", "Rapid Shutdown Device", "RSD"),
    ("solar", "Solar Panel", "PV"),
    ("transferSwitch", "Transfer Switch", "Q"),
    ("transformer", "Transformer", "T"),
    ("utility", "Utility", "GRID"),
    ("voltageTransducer", "Voltage Transducer", "PT"),
    ("wind", "Wind", "WIND"),
]
TITLES = {k: t for k, t, _ in COMPONENTS}

MEASUREMENT_KEYS = {"value", "min", "nom", "max", "unit"}
MAX_DEPTH = 8
MAX_ENUM = 8


# --------------------------------------------------------------------------- #
# JSON Schema walking (reference generation)
# --------------------------------------------------------------------------- #

def resolve_pointer(root, ref):
    node = root
    for part in ref[2:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        if part == "":
            continue
        node = node[int(part)] if isinstance(node, list) else node[part]
    return node


def deref(root, s):
    guard = 0
    while isinstance(s, dict) and "$ref" in s:
        target = resolve_pointer(root, s["$ref"])
        merged = dict(target)
        for k, v in s.items():
            if k != "$ref":
                merged[k] = v
        s = merged
        guard += 1
        if guard > 40:
            break
    return s


def unwrap(root, s):
    s = deref(root, s)
    if not isinstance(s, dict):
        return {}, False
    nullable = False
    t = s.get("type")
    if isinstance(t, list):
        if "null" in t:
            nullable = True
        non_null = [x for x in t if x != "null"]
        s = dict(s)
        s["type"] = non_null[0] if len(non_null) == 1 else (non_null or None)
    key = "anyOf" if "anyOf" in s else ("oneOf" if "oneOf" in s else None)
    if key:
        real = []
        for member in s[key]:
            m = deref(root, member)
            if not isinstance(m, dict):
                continue
            if m.get("type") == "null":
                nullable = True
                continue
            if "not" in m and m.get("not") == {}:
                continue
            mm, mnull = unwrap(root, m)
            if mnull:
                nullable = True
            if mm.get("type") == "null" or not mm:
                continue
            real.append(mm)
        outer_default = s.get("default")
        if len(real) == 1:
            s = dict(real[0])
            if outer_default is not None and "default" not in s:
                s["default"] = outer_default
        elif len(real) > 1:
            s = {"_union": real, "default": outer_default}
    return s, nullable


def is_measurement(root, s):
    props = s.get("properties")
    if not isinstance(props, dict):
        return False
    keys = set(props.keys())
    return "unit" in keys and keys.issubset(MEASUREMENT_KEYS)


def unit_of(root, s):
    unit = deref(root, s.get("properties", {}).get("unit", {}))
    if "const" in unit:
        return unit["const"]
    if "default" in unit:
        return unit["default"]
    if "enum" in unit and unit["enum"]:
        return unit["enum"][0]
    return "?"


def fmt_default(val):
    if val == {}:
        return "`{}`"
    if val == []:
        return "`[]`"
    if val is None:
        return "`null`"
    if isinstance(val, bool):
        return "`true`" if val else "`false`"
    if val == "":
        return '`""`'
    if isinstance(val, (int, float, str)):
        return "`%s`" % val
    if isinstance(val, list) and len(json.dumps(val)) > 48:
        return "`[%d items]`" % len(val)
    if isinstance(val, dict) and len(json.dumps(val)) > 48:
        return "`{%d keys}`" % len(val)
    return "`%s`" % json.dumps(val)


def fmt_enum(values):
    shown = values[:MAX_ENUM]
    parts = ", ".join("`%s`" % v for v in shown)
    if len(values) > MAX_ENUM:
        parts += ", ... (%d total)" % len(values)
    return parts


def type_and_notes(root, s):
    if "_union" in s:
        labels = []
        for m in s["_union"]:
            lbl, _ = type_and_notes(root, m)
            labels.append(lbl)
        return " or ".join(dict.fromkeys(labels)), ""
    if is_measurement(root, s):
        fields = [k for k in ("value", "min", "nom", "max") if k in s["properties"]]
        return "measurement", "fields: %s; unit `%s`" % (", ".join(fields), unit_of(root, s))
    if "const" in s:
        return "const", "= `%s`" % s["const"]
    if "enum" in s:
        base = s.get("type")
        label = base if isinstance(base, str) else "enum"
        return label, "one of " + fmt_enum(s["enum"])
    t = s.get("type")
    if t == "array":
        items = s.get("items")
        if isinstance(items, list):
            items = items[0] if items else {}
        item_s, _ = unwrap(root, items or {})
        if item_s.get("type") == "object" or "properties" in item_s:
            return "array of objects", ""
        if "enum" in item_s:
            return "array", "items: one of " + fmt_enum(item_s["enum"])
        it_label, _ = type_and_notes(root, item_s)
        return "array of %s" % it_label, ""
    if t == "object" or "properties" in s:
        return "object", ""
    if isinstance(t, str):
        return t, ("format `%s`" % s["format"]) if "format" in s else ""
    if isinstance(t, list):
        return " or ".join(t), ""
    return "any", ""


def child_object(root, s):
    if "_union" in s or is_measurement(root, s):
        return None, ""
    if "properties" in s and isinstance(s["properties"], dict):
        return s, ""
    if s.get("type") == "array":
        items = s.get("items")
        if isinstance(items, list):
            items = items[0] if items else {}
        item_s, _ = unwrap(root, items or {})
        if "properties" in item_s:
            return item_s, "[]"
    return None, ""


def emit_object(root, schema, path, lines, sections, depth):
    props = schema.get("properties", {})
    required = set(schema.get("required", []))
    lines.append("| Field | Type | Required | Default | Allowed / notes |")
    lines.append("| --- | --- | --- | --- | --- |")
    queue = []
    for name in props.keys():
        s, nullable = unwrap(root, props[name])
        label, notes = type_and_notes(root, s)
        if nullable and "nullable" not in notes:
            notes = (notes + "; " if notes else "") + "nullable"
        req = "yes" if name in required else ""
        default = fmt_default(s["default"]) if "default" in s else ""
        lines.append("| `%s` | %s | %s | %s | %s |" % (name, label, req, default, notes))
        child, suffix = child_object(root, s)
        if child is not None and depth < MAX_DEPTH:
            queue.append((name + suffix, child))
    lines.append("")
    for child_name, child_schema in queue:
        child_path = path + "." + child_name if path else child_name
        sections.append((child_path, child_schema, depth + 1))


def render_reference(root, ctype):
    schema = deref(root, root)
    title = TITLES.get(ctype, ctype)
    indicator = next((i for k, _, i in COMPONENTS if k == ctype), "")
    required = ", ".join("`%s`" % r for r in schema.get("required", [])) or "none"
    example_name = "test%s.json" % (ctype[0].upper() + ctype[1:])

    lines = []
    lines.append("---")
    lines.append("title: %s" % title)
    lines.append("description: Field level schema reference for the %s component type." % title)
    lines.append("---")
    lines.append("")
    lines.append("Generated from `schema/%s.json` by `scripts/gen_docs.py`. The schemas are "
                 "the source of truth (dcide-app validators). Do not edit this page by hand." % ctype)
    lines.append("")
    lines.append("- Type key: `%s`" % ctype)
    if indicator:
        lines.append("- Indicator: `%s`" % indicator)
    lines.append("- Required top level fields: %s" % required)
    lines.append("- Narrative guide: [%s](../data-model/%s)" % (title, ctype))
    if os.path.exists(os.path.join(EXAMPLE_DIR, example_name)):
        lines.append("- Example instance: [`examples/%s`](%s/examples/%s)"
                     % (example_name, GH_BLOB, example_name))
    lines.append("")
    lines.append("## Top level attributes")
    lines.append("")

    sections = []
    emit_object(root, schema, "", lines, sections, 0)
    i = 0
    while i < len(sections):
        path, sub, depth = sections[i]
        i += 1
        heading = "#" * min(2 + depth, 6)
        lines.append("%s `%s`" % (heading, path))
        lines.append("")
        emit_object(root, sub, path, lines, sections, depth)
    return "\n".join(lines).rstrip() + "\n"


# --------------------------------------------------------------------------- #
# Prose import (guides)
# --------------------------------------------------------------------------- #

def import_guide(md_path):
    """Turn a hand written docs/*.md page into an MDX guide body + title."""
    with open(md_path) as fh:
        text = fh.read()

    title = None
    body_lines = []
    for line in text.splitlines():
        if title is None and line.startswith("# "):
            title = line[2:].strip()
            continue
        body_lines.append(line)
    if title is None:
        title = os.path.splitext(os.path.basename(md_path))[0]
    body = "\n".join(body_lines).strip()

    # Rewrite intra-guide links: ./common.md -> ./common, ./battery.md -> ./battery
    body = re.sub(r"\]\(\./([A-Za-z0-9_]+)\.md\)", r"](./\1)", body)
    # Rewrite example links to the GitHub source.
    body = re.sub(r"\]\(\.\./examples/([A-Za-z0-9_]+\.json)\)",
                  r"](%s/examples/\1)" % GH_BLOB, body)

    desc = title
    front = "---\ntitle: %s\ndescription: %s\n---\n\n" % (title, desc)
    return front + body + "\n"


# --------------------------------------------------------------------------- #
# Authored pages
# --------------------------------------------------------------------------- #

INDEX_PAGE = """---
title: Interoperability Data Model
description: A common, machine readable model for microgrid electrical components.
---

The Interoperability Data Model (IDM) describes electrical components in a common, machine
readable form so tools across the DC ecosystem can exchange product data. The model is
expressed as JSON Schema (draft-07), one file per component type, and is generated from the
dcide-app component validators, which are the source of truth.

## Where to go

- Data model: the shared common base and one narrative guide per component type. Start with
  [Common attributes](/docs/data-model/common).
- Schema reference: an auto generated, field level reference for every component type. See
  the [reference overview](/docs/reference).
- Standards and alignment: what the model actually references. See
  [Standards](/docs/standards).
- Contributing: how the schemas are generated and how to work on the docs. See
  [Contributing](/docs/contributing).

## How to read a component page

Each guide opens with a short description and a summary block (type key, indicator, port
configuration), then documents the ports and the component specific electrical attributes.
Anything not listed comes from the common base shared by all types. The matching schema
reference page lists every field exhaustively.
"""

STANDARDS_PAGE = """---
title: Standards and alignment
description: The standards and ratings the IDM actually references today.
---

This page documents the standards and ratings the Interoperability Data Model (IDM) actually
references today. It is scoped to what exists in the schemas. It does not claim a formal
standard the model does not implement.

## What the model aligns to

The IDM schemas are generated from the dcide-app component validators, which are the source
of truth. The model is an open effort championed through the Emerge Alliance
(https://www.emergealliance.org/). It is a harmonized data format for microgrid equipment,
not a certification standard in its own right.

## Compliance flags

Every component carries a `compliance` object with boolean flags for the certifications and
alliances a product meets: `CE`, `UL`, `currentOS` (Current/OS), `emergeAlliance` (Emerge
Alliance), `ODCA` and `other` (with free text `otherInput`). All default to `false`. These
are self declared flags, not evidence of certification.

## Free form standards lists

Components carry a top level `standards` string array, and several component types also carry
a type specific `standards` array inside their `electrical` section (for example battery,
breaker and fuse). These are free text lists and the model does not constrain their values.

## IEC and UL short circuit ratings

The only place the model names specific standards bodies is in the short circuit ratings on
protective devices. Circuit breakers (`breaker`) and fuses (`fuse`) both carry parallel IEC
and UL fields so a product can be described under either regime:

- `instantaneousShortCircuitCurrentUL` (value, unit `A`): the UL instantaneous short circuit
  current.
- `serviceShortCircuitBreakingCapacityIEC` (value, unit `A`): the IEC service short circuit
  breaking capacity, Ics.
- `ultimateShortCircuitBreakingCapacityIEC` (value, unit `A`): the IEC ultimate short circuit
  breaking capacity, Icu.

See the [Circuit Breaker](/docs/data-model/breaker) and [Fuse](/docs/data-model/fuse) guides
and their [breaker](/docs/reference/breaker) and [fuse](/docs/reference/fuse) schema
references for the full field lists.

## On IEC 62683

The model does not currently contain an IEC 62683 mapping or crosswalk. The IEC references in
the model are limited to the short circuit breaking capacity fields described above. If a
formal IEC 62683 (or eCl@ss, or other standard) alignment is wanted, it needs source material
and a deliberate mapping. This page will be extended once that material exists. Nothing here
is invented to fill that gap.
"""

CONTRIBUTING_PAGE = """---
title: Contributing
description: How the schemas, the reference pages and the docs site are built.
---

## Source of truth

The JSON Schemas in `schema/` are generated from the dcide-app component validators. Those
validators are the source of truth for the data model. Changes flow from the validators into
`schema/` and `examples/`, and this site regenerates from there.

## What is hand written and what is generated

The Fumadocs Next.js app lives at the repository root (package.json, next.config.mjs, src/,
content/). The data model source (schema/, examples/, docs/) sits alongside it.

- Hand written: the narrative guides (`docs/common.md` and one page per component type), and
  the authored overview, standards and contributing pages inside `scripts/gen_docs.py`.
- Generated: everything under `content/docs/` is produced by `scripts/gen_docs.py` from the
  hand written prose and the schemas. Do not edit files under `content/docs/` by hand; they
  are overwritten on every run.

## Building the site

From the repository root:

```
python scripts/gen_docs.py       # build the Fumadocs content tree
npm ci                            # install pinned dependencies
npm run build                     # build (static export under out/ when PAGES_DEPLOY=true)
```

`npm run dev` runs a local preview. The generator regenerates the whole `content/docs` tree
so the reference can never drift from the schemas.

## Deploying

The site supports two deploy targets from the same code. `next.config.mjs` gates the GitHub
Pages specifics behind the `PAGES_DEPLOY` env var.

Vercel (native Next.js):

- The app is at the repository root, so Vercel detects Next.js automatically. Import the
  repository in Vercel and deploy. No Root Directory change is needed.
- Vercel builds without `PAGES_DEPLOY`, so there is no base path and the app serves at the
  domain root and runs natively. Each branch and pull request gets a preview deployment.

GitHub Pages (static export):

- Handled by `.github/workflows/docs.yml`, which sets `PAGES_DEPLOY=true` so the build emits a
  static export under `out/` with the `/interoperability-data-model` base path.
- One time setup by a repo admin: Settings > Pages > Build and deployment > Source =
  GitHub Actions.

## Style

- No em dashes or en dashes.
- One item per line in bullet lists.
- Keep prose direct.
"""


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        fh.write(text)


def main():
    # This script owns content/docs: clear and rebuild it.
    if os.path.isdir(CONTENT):
        shutil.rmtree(CONTENT)
    os.makedirs(CONTENT)

    # Root pages.
    write(os.path.join(CONTENT, "index.mdx"), INDEX_PAGE)
    write(os.path.join(CONTENT, "standards.mdx"), STANDARDS_PAGE)
    write(os.path.join(CONTENT, "contributing.mdx"), CONTRIBUTING_PAGE)
    write(os.path.join(CONTENT, "meta.json"), json.dumps({
        "pages": ["index", "data-model", "reference", "standards", "contributing"],
    }, indent=2) + "\n")

    # Data model guides (imported prose).
    dm = os.path.join(CONTENT, "data-model")
    write(os.path.join(dm, "common.mdx"), import_guide(os.path.join(SRC_DOCS, "common.md")))
    for ctype, _, _ in COMPONENTS:
        src = os.path.join(SRC_DOCS, "%s.md" % ctype)
        write(os.path.join(dm, "%s.mdx" % ctype), import_guide(src))
    write(os.path.join(dm, "meta.json"), json.dumps({
        "title": "Data model",
        "pages": ["common"] + [c[0] for c in COMPONENTS],
    }, indent=2) + "\n")

    # Schema reference (generated).
    ref = os.path.join(CONTENT, "reference")
    rows = []
    for ctype, title, indicator in COMPONENTS:
        root = json.load(open(os.path.join(SCHEMA_DIR, "%s.json" % ctype)))
        write(os.path.join(ref, "%s.mdx" % ctype), render_reference(root, ctype))
        rows.append((title, ctype, indicator))

    idx = ["---", "title: Schema reference",
           "description: Auto generated field level reference for every component type.",
           "---", "",
           "One auto generated page per component type, produced from the JSON Schemas in "
           "`schema/` by `scripts/gen_docs.py`. Each page lists every field with its type, "
           "whether it is required, its default and its allowed values or unit.", "",
           "| Component | Type key | Indicator | Reference |",
           "| --- | --- | --- | --- |"]
    for title, ctype, indicator in sorted(rows):
        idx.append("| %s | `%s` | `%s` | [%s](./%s) |"
                   % (title, ctype, indicator, title, ctype))
    idx.append("")
    write(os.path.join(ref, "index.mdx"), "\n".join(idx) + "\n")
    write(os.path.join(ref, "meta.json"), json.dumps({
        "title": "Schema reference",
        "pages": ["index"] + [c[0] for c in COMPONENTS],
    }, indent=2) + "\n")

    print("Wrote overview, standards, contributing, %d guides and %d reference pages."
          % (len(COMPONENTS) + 1, len(COMPONENTS)))


if __name__ == "__main__":
    main()
