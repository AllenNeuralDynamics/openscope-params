from __future__ import annotations

"""Pydantic model for module `slap2_meta_annotator` parameters."""

from pydantic import BaseModel, ConfigDict, Field


class Parameters(BaseModel):
    model_config = ConfigDict(extra="allow")

    source_dir: str | None = Field(
        default=None,
        description="Session folder to scan and annotate (defaults to output_session_folder).",
    )
    assume_yes: bool = Field(
        default=False,
        description="If true, skip interactive confirmations and use defaults.",
    )
    default_brain_area: str = Field(
        default="VISp",
        description="Default brain area suggested to operator per meta file.",
    )
    default_depth: str = Field(
        default="unknown",
        description="Default depth suggested to operator per meta file.",
    )
    dynamic_dir: str = Field(
        default="slap2/dynamic_data",
        description="Relative destination for dynamic acquisition files.",
    )
    structure_dir: str = Field(
        default="slap2/structure_stack",
        description="Relative destination for structure stack files.",
    )
    ref_stack_dir: str = Field(
        default="slap2/dynamic_data/reference_stack",
        description="Relative destination for reference stack files.",
    )
    manifest_name: str = Field(
        default="routing_manifest.json",
        description="Filename for the routing/annotation manifest (written under launcher_metadata).",
    )
