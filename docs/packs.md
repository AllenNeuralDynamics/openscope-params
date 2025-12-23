# Packs

A **pack** is a curated set of parameter files under a directory within `packs/`.

Layout:

- `packs/shared/<group>/`: reusable params shared across multiple projects.
- `packs/projects/<project>/<context>/`: project-specific params.

Conventions:

- Each pack contains one or more `.json` parameter files.
- Parameter files should declare the launcher schema via `$schema`.
- Use the `description` field in a params file to help generate nicer docs.

See **Packs → Reference (generated)** for the current list.
