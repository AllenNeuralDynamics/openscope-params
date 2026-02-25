from __future__ import annotations

"""Pydantic model for module `instrument_json_fetch` parameters."""

from pydantic import BaseModel, ConfigDict, Field


class Parameters(BaseModel):
    model_config = ConfigDict(extra="allow")

    instrument_json_source_root: str = Field(
        default="C:/Users/ScanImage/Documents/GitHub/slap2_processing",
        description="Directory to search for instrument.json (the most recently modified match is selected).",
    )
    instrument_json_source_path: str | None = Field(
        default=None,
        description="Optional explicit path to an instrument.json file (skips auto-search).",
    )
    instrument_json_filename: str = Field(
        default="instrument.json",
        description="Filename to search for under instrument_json_source_root.",
    )
    instrument_json_recursive: bool = Field(
        default=True,
        description="If true, search instrument_json_source_root recursively.",
    )
    instrument_json_destination_name: str = Field(
        default="instrument.json",
        description="Destination filename to write into the session root.",
    )
    instrument_json_required: bool = Field(
        default=True,
        description="If true, fail pre-acquisition when an instrument.json cannot be selected/copied.",
    )
