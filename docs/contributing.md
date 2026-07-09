# Contributing

## Source of truth

The JSON Schemas in `schema/` are generated from the dcide-app component validators. Those
validators are the source of truth for the data model. Do not hand edit a schema to change
the model; changes flow from the validators into `schema/` and `examples/`, and this site
regenerates from there.

## What is hand written and what is generated

- Hand written: the narrative guides (`docs/common.md` and one page per component type), this
  page, and the standards page. Edit these directly.
- Generated: the schema reference pages under `docs/reference/`. Do not edit them by hand.
  They are produced by `scripts/gen_schema_docs.py` from the schemas and are overwritten on
  every run.

## Regenerating the reference

From the repository root:

```
pip install -r requirements.txt
python scripts/gen_schema_docs.py
```

This reads every `schema/*.json`, walks the fields, and writes one Markdown page per
component plus the reference index, so the reference can never drift from the schemas.

## Previewing the site locally

```
pip install -r requirements.txt
python scripts/gen_schema_docs.py
mkdocs serve
```

Then open the local URL that `mkdocs serve` prints. Use `mkdocs build --strict` to catch
broken links and nav problems the way the deploy workflow does.

## Style

- No em dashes or en dashes.
- One item per line in bullet lists.
- Keep prose direct.
