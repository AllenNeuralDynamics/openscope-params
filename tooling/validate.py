import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen


REPO_ROOT = Path(__file__).resolve().parents[1]


def _is_url(value: str) -> bool:
    try:
        u = urlparse(value)
    except Exception:
        return False
    return u.scheme in {"http", "https"}


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_module_schemas(tooling_dir: Path) -> dict[str, dict]:
    schemas: dict[str, dict] = {}
    for path in sorted(tooling_dir.glob("model_*.schema.json")):
        if path.name == "model_launcher.schema.json":
            continue
        data = _load_json(path)
        name = path.stem.removeprefix("model_")
        schemas[name] = data
    return schemas


def _resolve_schema(param_path: Path, schema_ref: str) -> dict:
    # Local relative path (common for repo-contained validation)
    if not _is_url(schema_ref) and not schema_ref.startswith("file://"):
        ref = schema_ref.strip()
        if ref.startswith("./"):
            ref = ref[2:]

        # Prefer repo-root-relative resolution for tooling schemas.
        candidates: list[Path] = []
        if ref.startswith("tooling/"):
            candidates.append((REPO_ROOT / ref).resolve())
        else:
            candidates.append((param_path.parent / ref).resolve())
            # Fallback: sometimes params are moved deeper but $schema was authored
            # as a repo-root-relative path (without the tooling/ prefix).
            candidates.append((REPO_ROOT / ref).resolve())

        for schema_path in candidates:
            if schema_path.exists():
                return _load_json(schema_path)

        raise FileNotFoundError(f"Schema file not found: {candidates[0]}")

    # Remote HTTP(S) URL
    if _is_url(schema_ref):
        parsed = urlparse(schema_ref)
        if parsed.netloc == "raw.githubusercontent.com" and parsed.path.endswith("/tooling/model_launcher.schema.json"):
            local = REPO_ROOT / "tooling" / "model_launcher.schema.json"
            if local.exists():
                return _load_json(local)
        with urlopen(schema_ref) as resp:
            if resp.status != 200:
                raise RuntimeError(f"Unable to fetch schema URL {schema_ref!r}: HTTP {resp.status}")
            data = resp.read().decode("utf-8")
            return json.loads(data)

    # file:// refs not yet supported
    raise RuntimeError(
        f"Schema refs of this form are not supported yet: {schema_ref!r}. "
        "Use a local path or HTTP(S) URL."
    )


def _validate_object_against_schema(payload: dict, schema: dict) -> None:
    required = schema.get("required", [])
    for key in required:
        if key not in payload or payload.get(key) is None:
            raise RuntimeError(f"Missing required key {key!r}")

    properties = schema.get("properties", {})
    for key, rules in properties.items():
        if key not in payload:
            continue
        expected = rules.get("type")
        if not expected:
            continue

        value = payload.get(key)
        if value is None:
            continue

        expected_types = expected if isinstance(expected, list) else [expected]
        type_ok = False
        for t in expected_types:
            if t == "string" and isinstance(value, str):
                type_ok = True
            elif t == "integer" and isinstance(value, int) and not isinstance(value, bool):
                type_ok = True
            elif t == "number" and isinstance(value, (int, float)) and not isinstance(value, bool):
                type_ok = True
            elif t == "object" and isinstance(value, dict):
                type_ok = True
            elif t == "array" and isinstance(value, list):
                type_ok = True
            elif t == "boolean" and isinstance(value, bool):
                type_ok = True
            elif t == "null" and value is None:
                type_ok = True
        if not type_ok:
            raise RuntimeError(f"Key {key!r} expected type {expected!r}, got {type(value).__name__}")


def validate_param(param_path: Path, module_schemas: dict[str, dict]) -> int:
    payload = _load_json(param_path)
    schema_ref = payload.get("$schema")
    if not schema_ref:
        raise RuntimeError(f"Missing $schema in {param_path}")
    schema = _resolve_schema(param_path, str(schema_ref))

    # Minimal, dependency-free validation: ensure required keys exist and basic types match.
    # This is intentionally lightweight so it runs on rigs without extra packages.
    _validate_object_against_schema(payload, schema)

    # Validate pipeline module entries against their module schemas when possible.
    def _validate_pipeline(pipeline):
        if not isinstance(pipeline, list):
            return
        for entry in pipeline:
            if not isinstance(entry, dict):
                continue
            module_path = entry.get("module_path")
            module_type = entry.get("module_type")
            if module_type and module_type != "launcher_module":
                continue
            params = entry.get("module_parameters")
            if not isinstance(params, dict):
                continue

            # Optional override per entry
            schema_ref = entry.get("module_schema")
            if schema_ref:
                module_schema = _resolve_schema(param_path, str(schema_ref))
            else:
                if not module_path:
                    continue
                module_schema = module_schemas.get(module_path)
                if not module_schema:
                    continue

            _validate_object_against_schema(params, module_schema)

    _validate_pipeline(payload.get("pre_acquisition_pipeline"))
    _validate_pipeline(payload.get("post_acquisition_pipeline"))
    return 0


def iter_json_files(root: Path):
    for path in root.rglob("*.json"):
        # Skip schema files themselves when validating packs
        if "schemas" in path.parts:
            continue
        yield path


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Validate OpenScope param packs against their $schema")
    parser.add_argument("--param", type=str, default=None, help="Validate a single param file")
    parser.add_argument(
        "--root",
        type=str,
        default=str(REPO_ROOT / "packs"),
        help="Root directory containing packs (default: ./packs)",
    )
    args = parser.parse_args(argv)

    tooling_dir = REPO_ROOT / "tooling"
    module_schemas = _load_module_schemas(tooling_dir)

    if args.param:
        paths = [Path(args.param).resolve()]
    else:
        paths = list(iter_json_files(Path(args.root).resolve()))
        if not paths:
            print(f"No JSON pack files found under: {args.root}")
            return 0

    failures = 0
    for path in paths:
        try:
            validate_param(path, module_schemas)
            print(f"OK  {path}")
        except Exception as exc:
            failures += 1
            print(f"FAIL {path}: {exc}")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
