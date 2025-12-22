from __future__ import annotations

"""Pydantic model for module `metadata_protocol_validator` parameters."""

from typing import Union

from pydantic import BaseModel, ConfigDict, Field


class Parameters(BaseModel):
    model_config = ConfigDict(extra="allow")

    metadata_protocol_name: str | None = Field(default=None, description="Expected protocol name.")
    metadata_protocol_prompt: str | None = Field(
        default=None,
        description="Prompt shown if protocol validation needs operator confirmation.",
    )
    protocol_name: str | None = Field(default=None, description="Observed protocol name (advanced/legacy).")
    protocol_id: Union[str, int, list[Union[str, int]], None] = Field(
        default=None,
        description="Expected protocol identifier(s) (string/int or list).",
    )
