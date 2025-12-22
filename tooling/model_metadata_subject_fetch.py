from __future__ import annotations

"""Pydantic model for module `metadata_subject_fetch` parameters."""

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
