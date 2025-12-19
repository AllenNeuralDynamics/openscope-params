# openscope-params

Central home for OpenScope/SLAP2 parameter JSON files (“param packs”) and the JSON Schemas they validate against.

Principles
----------
- Param files may optionally pin:
  - `launcher_version`: a PEP 440 specifier set (e.g. `>=0.2,<0.3`) to prevent incompatible launcher use.
  - `$schema`: a URL (or local path) to the schema the file was authored against.
- Schema URLs should be immutable (tag/commit), not a floating branch.
- Schemas are permissive by default: unknown keys are allowed to support heterogeneous modules.

Repo layout
-----------
- `schemas/launcher/`: base launcher schemas (per schema version).
- `packs/`: curated parameter files organized by rig/project.
- `tooling/`: validation tools.

Validate all packs
------------------
```powershell
python .\tooling\validate.py
```

Validate one pack file
```powershell
python .\tooling\validate.py --param .\packs\slap2\session_sync_master.json
```

Notes
-----
- This repo intentionally does **not** maintain a “known-good compatibility matrix”. Each param file pins the schema
  and launcher expectations.
- The launcher may optionally cache remote schema files for validation; rigs can prefetch schemas during provisioning.
