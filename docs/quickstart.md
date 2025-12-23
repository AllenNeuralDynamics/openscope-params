# Quickstart

## Validate a params file

From the repo root:

```powershell
python .\tooling\validate.py --param .\packs\shared\core\session_sync_master.json
```

## Validate all packs

```powershell
python .\tooling\validate.py
```

## Build docs locally

```powershell
python -m pip install -r .\requirements-docs.txt
python .\tooling\build_docs.py
mkdocs serve
```
