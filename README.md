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
- `tooling/*.schema.json`: generated JSON Schemas (colocated with the Pydantic models).
- `packs/`: curated parameter files.
  - `packs/shared/<group>/`: reusable params shared across multiple projects.
  - `packs/projects/<project>/<context>/`: project-specific params.
- `tooling/`: validation tools.

Validate all packs
------------------
```powershell
python .\tooling\validate.py
```

Validate one pack file
```powershell
python .\tooling\validate.py --param .\packs\shared\core\session_sync_master.json
```
