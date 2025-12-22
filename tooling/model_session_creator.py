from __future__ import annotations

"""Pydantic model for module `session_creator` parameters."""

from pydantic import BaseModel, ConfigDict, Field


class Parameters(BaseModel):
    model_config = ConfigDict(extra="allow")

    force: bool = Field(
        default=False,
        description="If true, overwrite/recreate an existing session folder if present.",
    )
