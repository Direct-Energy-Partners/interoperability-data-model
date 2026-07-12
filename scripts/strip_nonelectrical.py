#!/usr/bin/env python3
"""Strip non-electrical attributes from the IDM schemas and examples.

The IDM should standardize the ELECTRICAL specifications of DC power system
components. The schemas were synced from the dcide-app zod validators, which
also carry commercial, catalog and app-internal fields. Those do not belong in
the IDM (they stay in the dcide-app validators). This script removes them from
schema/*.json and examples/*.json.

Classification and rationale are in REMOVED_FIELDS.md. Ambiguous fields (could
be spec relevant) are KEPT and flagged there, not deleted.

Run from the repo root:  python scripts/strip_nonelectrical.py
"""

import json
import glob
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_DIR = os.path.join(ROOT, "schema")
EXAMPLE_DIR = os.path.join(ROOT, "examples")

# Shared base fields present in all 31 schemas that are NOT electrical specs.
REMOVE_BASE = [
    # Distributor / pricing / availability (commercial)
    "distributors",
    "distributorsDetails",
    "msrp",
    "leadTime",
    "regionAvailability",
    # Catalog / marketing
    "questions",
    "images",
    # dcide-app internal: team scoping, per-field UI annotations, derived
    # compatibility helpers, system / lifecycle-management / analytics fields
    "teamManufacturer",
    "metadata",
    "compatibleWithCrossReference",
    "compatibleWithPlaceholders",
    "id",
    "visibility",
    "reviewed",
    "publishedBy",
    "publishedAt",
    "archivedAt",
    "deletedAt",
    "completeness",
    "viewedCount",
    # Previously flagged as ambiguous, removed at operator request: product
    # lifecycle dates, datasheet/manual file references, declared compatibility.
    "lifecycle",
    "files",
    "compatibleWith",
]

# Component-specific non-electrical fields (only on some schemas). Both are
# dcide-app modeling helpers and reference removed fields.
REMOVE_COMPONENT = [
    "canServeAs",          # breaker, rapidShutdownDevice (refs compatibleWithPlaceholders)
    "compatibleProducts",  # combinerBox, powerDistributionUnit (refs id)
]

REMOVE = set(REMOVE_BASE) | set(REMOVE_COMPONENT)


def strip_schema(path):
    ctype = os.path.splitext(os.path.basename(path))[0]
    doc = json.load(open(path))
    props = doc["definitions"][ctype]["properties"]
    removed = [k for k in list(props.keys()) if k in REMOVE]
    for k in removed:
        del props[k]
    req = doc["definitions"][ctype].get("required")
    if isinstance(req, list):
        doc["definitions"][ctype]["required"] = [r for r in req if r not in REMOVE]
    with open(path, "w") as fh:
        json.dump(doc, fh, indent=2)
        fh.write("\n")
    return ctype, removed


def strip_example(path):
    inst = json.load(open(path))
    removed = [k for k in list(inst.keys()) if k in REMOVE]
    for k in removed:
        del inst[k]
    with open(path, "w") as fh:
        json.dump(inst, fh, indent=2)
        fh.write("\n")
    return removed


def collect_refs(node, out):
    if isinstance(node, dict):
        if "$ref" in node and isinstance(node["$ref"], str):
            out.append(node["$ref"])
        for v in node.values():
            collect_refs(v, out)
    elif isinstance(node, list):
        for v in node:
            collect_refs(v, out)


def resolve(doc, ref):
    node = doc
    for part in ref[2:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        if part == "":
            continue
        try:
            node = node[int(part)] if isinstance(node, list) else node[part]
        except (KeyError, IndexError, ValueError):
            return False
    return True


def main():
    print("=== Removed per schema ===")
    dangling = 0
    for path in sorted(glob.glob(os.path.join(SCHEMA_DIR, "*.json"))):
        ctype, removed = strip_schema(path)
        # Dangling ref check: every $ref must still resolve.
        doc = json.load(open(path))
        refs = []
        collect_refs(doc, refs)
        bad = [r for r in refs if not (r.startswith("#/") and resolve(doc, r))]
        flag = "" if not bad else "  !! DANGLING: %s" % bad
        if bad:
            dangling += len(bad)
        print("%-22s -%d: %s%s" % (ctype, len(removed), ", ".join(removed), flag))

    print("\n=== Removed per example ===")
    for path in sorted(glob.glob(os.path.join(EXAMPLE_DIR, "*.json"))):
        removed = strip_example(path)
        print("%-26s -%d" % (os.path.basename(path), len(removed)))

    print("\nDangling refs after strip:", dangling)


if __name__ == "__main__":
    main()
