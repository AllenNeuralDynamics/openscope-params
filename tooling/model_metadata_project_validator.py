from __future__ import annotations

"""Pydantic model for module `metadata_project_validator` parameters."""

from pydantic import BaseModel, ConfigDict, Field


class Parameters(BaseModel):
    model_config = ConfigDict(extra="allow")

    metadata_project_name: str | None = Field(default=None, description="Expected project name.")
    metadata_project_prompt: str | None = Field(
        default=None,
        description="Prompt shown if project validation needs operator confirmation.",
    )
    project_name: str | None = Field(default=None, description="Observed project name (advanced/legacy).")
    projects: list[str] | None = Field(
        default=None,
        description="List of observed/allowed projects (advanced/legacy).",
    )
