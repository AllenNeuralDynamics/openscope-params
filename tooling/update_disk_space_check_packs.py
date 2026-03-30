"""Bulk-update disk_space_check requirements across parameter packs.

Policy:
- Any pack under a folder named `imaging` gets required_free_gb = 1000.
- Any pack under a folder named `behavior` or `behavior-videos`/`behavior_videos` gets required_free_gb = 10.

Behavior:
- Ensures a `disk_space_check` launcher_module exists in `pre_acquisition_pipeline`.
- If `wait_for_user_input` is present, inserts `disk_space_check` immediately before it.
- If `disk_space_check` exists, updates its parameters.
- Removes legacy/unsupported `required_free_bytes` if present.

Run from repo root:
    python ./tooling/update_disk_space_check_packs.py

"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKS_ROOT = REPO_ROOT / "packs"

BEHAVIOR_GB = 10
IMAGING_GB = 1000

BEHAVIOR_FOLDER_NAMES = {
    "behavior",
    "behavior-videos",
    "behavior_videos",
    "behaviorvideos",
    "behavior-video",
    "behavior_video",
}


def _classify_required_gb(path: Path) -> int | None:
    parts = [p.lower() for p in path.parts]

    if "imaging" in parts:
        return IMAGING_GB

    if any(p in BEHAVIOR_FOLDER_NAMES for p in parts):
        return BEHAVIOR_GB

    return None


def _is_disk_space_check_entry(entry: Any) -> bool:
    return (
        isinstance(entry, dict)
        and entry.get("module_type", "launcher_module") == "launcher_module"
        and entry.get("module_path") == "disk_space_check"
    )


def _is_wait_for_user_input_entry(entry: Any) -> bool:
    return (
        isinstance(entry, dict)
        and entry.get("module_type", "launcher_module") == "launcher_module"
        and entry.get("module_path") == "wait_for_user_input"
    )


def _ensure_disk_space_check(pipeline: list[Any], required_free_gb: int) -> None:
    # Update existing entries first.
    for entry in pipeline:
        if _is_disk_space_check_entry(entry):
            params = entry.get("module_parameters")
            if not isinstance(params, dict):
                params = {}
            params.pop("required_free_bytes", None)
            params["required_free_gb"] = required_free_gb
            entry["module_parameters"] = params
            return

    # Otherwise insert a new one (before wait_for_user_input if present).
    new_entry = {
        "module_type": "launcher_module",
        "module_path": "disk_space_check",
        "module_parameters": {"required_free_gb": required_free_gb},
    }

    for idx, entry in enumerate(pipeline):
        if _is_wait_for_user_input_entry(entry):
            pipeline.insert(idx, new_entry)
            return

    pipeline.append(new_entry)


def _load_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    path.write_text(text, encoding="utf-8")


def main() -> int:
    if not PACKS_ROOT.exists():
        raise SystemExit(f"packs root not found: {PACKS_ROOT}")

    updated = 0
    scanned = 0
    skipped = 0

    for json_path in sorted(PACKS_ROOT.rglob("*.json")):
        required_gb = _classify_required_gb(json_path)
        if required_gb is None:
            continue

        scanned += 1
        payload = _load_json(json_path)
        if payload is None or not isinstance(payload, dict):
            skipped += 1
            continue

        pipeline = payload.get("pre_acquisition_pipeline")
        if pipeline is None:
            pipeline = []
            payload["pre_acquisition_pipeline"] = pipeline

        if not isinstance(pipeline, list):
            skipped += 1
            continue

        before = json.dumps(payload, sort_keys=False)
        _ensure_disk_space_check(pipeline, required_free_gb=required_gb)
        after = json.dumps(payload, sort_keys=False)

        if before != after:
            _write_json(json_path, payload)
            updated += 1

    print(f"Scanned {scanned} pack(s); updated {updated}; skipped {skipped}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
