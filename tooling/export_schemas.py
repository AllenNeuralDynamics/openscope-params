"""Export JSON Schema files from Pydantic models.

Run from repo root:
    python ./tooling/export_schemas.py

This writes `tooling/*.schema.json` files next to the Pydantic models and is intended for development/CI.
"""

from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import Any, Type


REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_module(py_path: Path):
    spec = spec_from_file_location(py_path.stem, py_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to import {py_path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _iter_module_model_files(*, tooling_dir: Path) -> list[Path]:
    """Discover module model files.

    Convention:
    - Launcher model: tooling/model_launcher.py
    - Module models: tooling/model_*.py defining a `Parameters` Pydantic model
    """

    paths = sorted(tooling_dir.glob("model_*.py"))
    return [p for p in paths if p.name != "model_launcher.py" and p.is_file()]


def _infer_module_name(py_path: Path) -> str:
    stem = py_path.stem
    if stem.startswith("model_"):
        return stem[len("model_") :]
    return stem


def _module_description(module: Any, fallback: str) -> str:
    # Optional per-module constant
    desc = getattr(module, "MODULE_DESCRIPTION", None)
    if isinstance(desc, str) and desc.strip():
        return desc.strip()

    # Else, module docstring (first paragraph)
    doc = getattr(module, "__doc__", None)
    if isinstance(doc, str):
        doc = doc.strip()
        if doc:
            first_para = doc.split("\n\n", 1)[0].replace("\n", " ").strip()
            if first_para:
                return first_para

    return fallback


def _write_schema_json(*, path: Path, schema: dict[str, Any], schema_id: str, title: str, description: str) -> None:
    import json

    # Write Pydantic-generated schema first, then override top-level metadata.
    # This keeps our repo-level $id/title/description stable.
    out = {
        **schema,
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": schema_id,
        "title": title,
        "description": description,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    # Launcher schema (Pydantic)
    launcher_py = REPO_ROOT / "tooling" / "model_launcher.py"
    launcher_module = _load_module(launcher_py)
    launcher_model: Type[Any] = getattr(launcher_module, "LauncherParams")
    if hasattr(launcher_model, "model_rebuild"):
        launcher_model.model_rebuild(force=True, _types_namespace=launcher_module.__dict__)

    # Modules (auto-discovered)
    tooling_dir = REPO_ROOT / "tooling"
    module_model_files = _iter_module_model_files(tooling_dir=tooling_dir)

    for py_path in module_model_files:
        module = _load_module(py_path)
        model = getattr(module, "Parameters", None)
        if model is None:
            # Not a module-parameters model file; ignore.
            continue

        module_name = _infer_module_name(py_path)
        module_desc = _module_description(
            module,
            fallback="Module parameters schema generated from Pydantic.",
        )

        if hasattr(model, "model_rebuild"):
            model.model_rebuild(force=True, _types_namespace=module.__dict__)
        _write_schema_json(
            path=py_path.with_suffix(".schema.json"),
            schema=model.model_json_schema(),
            schema_id=f"https://example.invalid/openscope-params/tooling/{py_path.stem}.schema.json",
            title=f"Module Parameters: {module_name} (Pydantic)",
            description=f"Generated from Pydantic model {py_path.name}:Parameters. {module_desc}",
        )

    _write_schema_json(
        path=launcher_py.with_suffix(".schema.json"),
        schema=launcher_model.model_json_schema(),
        schema_id="https://example.invalid/openscope-params/tooling/model_launcher.schema.json",
        title="OpenScope Experimental Launcher Params (Pydantic)",
        description=(
            "Top-level schema for OpenScope launcher parameter files, generated from Pydantic. "
            "This schema is intentionally permissive (additionalProperties=true) while providing structured validation "
            "and documentation for common keys and pipeline entry formats."
        ),
    )

    print("Export complete.")


if __name__ == "__main__":
    main()
