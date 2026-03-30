from __future__ import annotations

"""Pydantic model for module `disk_space_check` parameters."""

from pydantic import BaseModel, ConfigDict, Field


MODULE_DESCRIPTION = "Check that the session volume has enough free space before starting acquisition."


class Parameters(BaseModel):
    model_config = ConfigDict(extra="allow")

    required_free_gb: float = Field(
        gt=0,
        description="Minimum required free space (GiB).",
        examples=[250],
    )

    disk_space_check_path: str | None = Field(
        default=None,
        description=(
            "Path to check. If omitted, the launcher uses output_session_folder."
        ),
        examples=["{output_session_folder}"],
    )

    allow_override: bool = Field(
        default=False,
        description="If true, allow operator prompt to continue even if below threshold.",
    )
