import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse


def _is_url(value: str) -> bool:
    try:
        u = urlparse(value)
    except Exception:
        return False
    return u.scheme in {"http", "https"}


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _resolve_schema(param_path: Path, schema_ref: str) -> dict:
    # Local relative path (common for repo-contained validation)
    if not _is_url(schema_ref) and not schema_ref.startswith("file://"):
        schema_path = (param_path.parent / schema_ref).resolve()
        if not schema_path.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_path}")
        return _load_json(schema_path)

    # URL/file refs: keep simple for now. You can extend this to download/cache.
    raise RuntimeError(
        f"Remote schema refs are not supported by this validator yet: {schema_ref!r}. "
        "Use a relative path within the repo for CI validation."
    )


def validate_param(param_path: Path) -> int:
    payload = _load_json(param_path)
    schema_ref = payload.get("$schema")
    if not schema_ref:
        raise RuntimeError(f"Missing $schema in {param_path}")
    schema = _resolve_schema(param_path, str(schema_ref))

    # Minimal, dependency-free validation: ensure required keys exist and basic types match.
    # This is intentionally lightweight so it runs on rigs without extra packages.
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
        default=str(Path(__file__).resolve().parents[1] / "packs"),
        help="Root directory containing packs (default: ./packs)",
    )
    args = parser.parse_args(argv)

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
            validate_param(path)
            print(f"OK  {path}")
        except Exception as exc:
            failures += 1
            print(f"FAIL {path}: {exc}")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
