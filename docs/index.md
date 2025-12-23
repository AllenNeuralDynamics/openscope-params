# OpenScope Params

This repository contains:

- **Parameter packs** under `packs/` (example launcher configuration JSON files)
	- `packs/shared/` for reusable, cross-project params
	- `packs/projects/` for project-specific params
- **JSON Schemas** under `tooling/*.schema.json` used to validate those parameter files
- **Tooling** under `tooling/` (e.g. validation and documentation generation)

## Relationship to `openscope-experimental-launcher`

- `openscope-params` is the canonical home for validated parameter files and schemas.
- `openscope-experimental-launcher` consumes parameter files and executes pre/post acquisition pipelines.

## Reference docs

- Packs reference: see **Packs → Reference (generated)**.
- Schemas reference: see **Schemas → Reference (generated)**.
