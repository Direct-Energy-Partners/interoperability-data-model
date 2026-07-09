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

## Deploying to GitHub Pages

The site is built and deployed by GitHub Actions using the official Pages-from-Actions flow.
See `.github/workflows/docs.yml`. On every push to the `idm-docs-website` branch the workflow
installs the pinned dependencies, runs `scripts/gen_schema_docs.py`, builds with
`mkdocs build --strict`, and deploys the `site/` artifact.

One time repository setup, which only a repository admin can do:

- Go to Settings > Pages > Build and deployment.
- Set Source to "GitHub Actions".

Nothing else needs toggling. The workflow already requests the `pages: write` and
`id-token: write` permissions it needs. The published URL is
`https://direct-energy-partners.github.io/interoperability-data-model/`.

After this branch merges, change the trigger branch in `.github/workflows/docs.yml` from
`idm-docs-website` to `main` so the live site tracks `main`.

## Style

- No em dashes or en dashes.
- One item per line in bullet lists.
- Keep prose direct.
