from __future__ import annotations

"""Pydantic model for module `metadata_procedures_fetch` parameters."""

from pydantic import BaseModel, ConfigDict, Field


class Parameters(BaseModel):
    model_config = ConfigDict(extra="allow")

    metadata_subject_id: str | int | None = Field(
        default=None,
        description="Subject identifier to query (defaults to top-level subject_id if omitted).",
    )
    metadata_mouse_id: str | int | None = Field(
        default=None,
        description="Optional mouse identifier if distinct from subject_id.",
    )
    metadata_procedures_timeout: float = Field(
        default=60,
        ge=0,
        description="Timeout in seconds for procedures fetch calls.",
    )
