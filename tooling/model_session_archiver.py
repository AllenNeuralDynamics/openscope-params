from __future__ import annotations

"""Pydantic model for module `session_archiver` parameters."""

from typing import Union

from pydantic import BaseModel, ConfigDict, Field


class Parameters(BaseModel):
    model_config = ConfigDict(extra="allow")

    session_dir: str | None = Field(
        default=None,
        description="Source session directory to archive (defaults to launcher session folder if omitted).",
    )
    network_dir: str | None = Field(default=None, description="Destination directory on a network share.")
    backup_dir: str | None = Field(
        default=None,
        description="Optional local backup directory used as an intermediate or fallback.",
    )
    manifest_path: str | None = Field(
        default=None,
        description="Optional path to a manifest file describing what was archived.",
    )
    include_patterns: Union[str, list[str], None] = Field(
        default=None,
        description="Glob(s) of files to include (string or list).",
    )
    exclude_patterns: Union[str, list[str], None] = Field(
        default=None,
        description="Glob(s) of files to exclude (string or list).",
    )
    checksum_algo: str | None = Field(
        default=None,
        description="Checksum algorithm for verification (e.g. 'md5', 'sha256').",
    )
    dry_run: bool = Field(default=False, description="If true, do not write/copy; only log intended operations.")
    skip_completed: bool = Field(default=True, description="If true, skip items that appear already archived.")
    max_retries: int = Field(default=3, ge=0, description="Maximum retries for transient failures (copy/verify).")
    remove_empty_dirs: bool = Field(
        default=False,
        description="If true, remove empty source directories after archiving.",
    )
