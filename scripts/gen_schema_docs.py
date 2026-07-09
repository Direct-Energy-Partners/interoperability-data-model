#!/usr/bin/env python3
"""Generate MkDocs reference pages from the IDM JSON Schemas.

The schemas in schema/ are the source of truth (generated from the dcide-app
validators). This script walks each schema and emits a Markdown reference page
per component type under docs/reference/, plus an index/matrix page. It is
deterministic and safe to re-run. Do not hand edit the generated files.

Usage: python scripts/gen_schema_docs.py
"""

import json
import glob
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_DIR = os.path.join(ROOT, "schema")
EXAMPLE_DIR = os.path.join(ROOT, "examples")
OUT_DIR = os.path.join(ROOT, "docs", "reference")

# Human readable titles and indicators, mirrored from docs/README.md.
META = {
    "battery": ("Battery", "BAT"),
    "breaker": ("Circuit Breaker", "Q"),
    "cable": ("Cable", "WIRE"),
    "capacitor": ("Capacitor", "C"),
    "charger": ("EV Charger", "CHG"),
    "combinerBox": ("Combiner Box", "A"),
    "contactor": ("Contactor", "K"),
    "converter": ("Converter", "U"),
    "currentTransducer": ("Current Transducer", "CT"),
    "diode": ("Diode", "D"),
    "disconnect": ("Disconnect", "Q"),
    "fuelCell": ("Fuel Cell", "FC"),
    "fuse": ("Fuse", "F"),
    "generator": ("Generator", "G"),
    "grounding": ("Grounding", "GND"),
    "hvac": ("HVAC", "HVAC"),
    "hydro": ("Hydro", "HYDRO"),
    "light": ("Light", "LIGHT"),
    "load": ("Load", "LOAD"),
    "meter": ("Meter", "P"),
    "motor": ("Motor", "M"),
    "panel": ("Panel Switchboard", "A"),
    "powerDistributionUnit": ("Power Distribution Unit", "PDU"),
    "precharge": ("Precharge", "PRE"),
    "rapidShutdownDevice": ("Rapid Shutdown Device", "RSD"),
    "solar": ("Solar Panel", "PV"),
    "transferSwitch": ("Transfer Switch", "Q"),
    "transformer": ("Transformer", "T"),
    "utility": ("Utility", "GRID"),
    "voltageTransducer": ("Voltage Transducer", "PT"),
    "wind": ("Wind", "WIND"),
}

MEASUREMENT_KEYS = {"value", "min", "nom", "max", "unit"}
MAX_DEPTH = 8
MAX_ENUM = 8


def resolve_pointer(root, ref):
    """Resolve a local JSON pointer like '#/definitions/battery/...'."""
    node = root
    for part in ref[2:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        if part == "":
            continue
        node = node[int(part)] if isinstance(node, list) else node[part]
    return node


def deref(root, s):
    """Follow $ref chains, preserving local overrides such as default."""
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
    """Collapse nullable / anyOf wrappers. Returns (schema, nullable)."""
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
                # {"not": {}} is an "absent" marker used by the validators.
                continue
            mm, mnull = unwrap(root, m)
            if mnull:
                nullable = True
            if mm.get("type") == "null" or not mm:
                nullable = nullable or (mm.get("type") == "null")
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
    # Collapse large defaults so they do not blow out the table.
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
    """Return (type_label, notes) for a leaf-ish schema."""
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
        notes = ""
        if "format" in s:
            notes = "format `%s`" % s["format"]
        return t, notes
    if isinstance(t, list):
        return " or ".join(t), ""
    return "any", ""


def child_object(root, s):
    """If schema is an object with props or array of such, return the object
    schema to recurse into and a path suffix, else None."""
    if "_union" in s:
        return None, ""
    if is_measurement(root, s):
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
    """Emit a table for schema's direct properties; queue nested objects."""
    props = schema.get("properties", {})
    required = set(schema.get("required", []))
    order = list(props.keys())

    lines.append("| Field | Type | Required | Default | Allowed / notes |")
    lines.append("| --- | --- | --- | --- | --- |")
    queue = []
    for name in order:
        raw = props[name]
        s, nullable = unwrap(root, raw)
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


def render_component(root, ctype):
    schema = deref(root, root)  # root has $ref to definitions/<ctype>
    title, indicator = META.get(ctype, (ctype, ""))
    required = ", ".join("`%s`" % r for r in schema.get("required", [])) or "none"

    lines = []
    lines.append("# %s schema reference" % title)
    lines.append("")
    lines.append("Generated from `schema/%s.json` by `scripts/gen_schema_docs.py`. "
                 "The schemas are the source of truth (dcide-app validators). Do not "
                 "edit this page by hand." % ctype)
    lines.append("")
    lines.append("- Type key: `%s`" % ctype)
    if indicator:
        lines.append("- Indicator: `%s`" % indicator)
    lines.append("- Required top level fields: %s" % required)
    example_name = "test%s.json" % (ctype[0].upper() + ctype[1:])
    if os.path.exists(os.path.join(EXAMPLE_DIR, example_name)):
        # Links to the copy bundled into the site under docs/examples/.
        lines.append("- Example instance: [`examples/%s`](../examples/%s)" % (example_name, example_name))
    lines.append("- Narrative guide: [%s](../%s.md)" % (title, ctype))
    lines.append("")
    lines.append("## Top level attributes")
    lines.append("")

    sections = []
    emit_object(root, schema, "", lines, sections, 0)

    # Breadth first through nested object sections, keeping stable order.
    i = 0
    while i < len(sections):
        path, sub, depth = sections[i]
        i += 1
        heading = "#" * min(2 + depth, 6)
        lines.append("%s `%s`" % (heading, path))
        lines.append("")
        emit_object(root, sub, path, lines, sections, depth)

    return "\n".join(lines).rstrip() + "\n"


def copy_examples():
    """Bundle the example instances into the site so pages can link to them."""
    import shutil
    dest = os.path.join(ROOT, "docs", "examples")
    os.makedirs(dest, exist_ok=True)
    count = 0
    for path in sorted(glob.glob(os.path.join(EXAMPLE_DIR, "*.json"))):
        shutil.copy2(path, os.path.join(dest, os.path.basename(path)))
        count += 1
    return count


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    n_examples = copy_examples()
    schema_files = sorted(glob.glob(os.path.join(SCHEMA_DIR, "*.json")))
    rows = []
    for path in schema_files:
        ctype = os.path.splitext(os.path.basename(path))[0]
        root = json.load(open(path))
        out = render_component(root, ctype)
        with open(os.path.join(OUT_DIR, "%s.md" % ctype), "w") as fh:
            fh.write(out)
        title, indicator = META.get(ctype, (ctype, ""))
        rows.append((title, ctype, indicator))

    # Index / matrix page.
    idx = []
    idx.append("# Schema reference")
    idx.append("")
    idx.append("One auto generated page per component type, produced from the JSON "
               "Schemas in `schema/` by `scripts/gen_schema_docs.py`. Each page lists "
               "every field with its type, whether it is required, its default and its "
               "allowed values or unit. The prose guides under Data model add the "
               "context; these pages are the exhaustive field reference.")
    idx.append("")
    idx.append("| Component | Type key | Indicator | Reference |")
    idx.append("| --- | --- | --- | --- |")
    for title, ctype, indicator in sorted(rows):
        idx.append("| %s | `%s` | `%s` | [%s](%s.md) |" % (title, ctype, indicator, title, ctype))
    idx.append("")
    with open(os.path.join(OUT_DIR, "index.md"), "w") as fh:
        fh.write("\n".join(idx) + "\n")

    print("Generated %d reference pages + index in %s" % (len(rows), OUT_DIR))
    print("Bundled %d example instances into docs/examples/" % n_examples)


if __name__ == "__main__":
    main()
