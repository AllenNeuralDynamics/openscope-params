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

    default_green_channel_target: str | None = Field(
        default=None,
        description="Default Intended Green Channel Target (asked once per experiment if not provided).",
    )
    default_red_channel_target: str | None = Field(
        default=None,
        description="Default Intended Red Channel Target (asked once per experiment if not provided).",
    )
    default_slap2_mode: str | None = Field(
        default=None,
        description="Default SLAP2 mode (asked once per acquisition / meta pair if not provided).",
    )
    default_dmd1_depth: str = Field(
        default="",
        description="Depth (microns from surface) for DMD1 acquisitions; used for all DMD1 files.",
    )
    default_dmd2_depth: str = Field(
        default="",
        description="Depth (microns from surface) for DMD2 acquisitions; used for all DMD2 files.",
    )
    dynamic_dir: str = Field(
        default="dynamic_data",
        description="Relative destination for dynamic acquisition files (under session folder).",
    )
    structure_dir: str = Field(
        default="structure_stack",
        description="Relative destination for structure stack files (under session folder).",
    )
    ref_stack_dir: str = Field(
        default="dynamic_data/reference_stack",
        description="Relative destination for reference stack files (under session folder).",
    )
    manifest_name: str = Field(
        default="routing_manifest.json",
        description="Filename for the routing/annotation manifest (written under launcher_metadata).",
    )
    manifest_path: str | None = Field(
        default=None,
        description="Optional manifest path (absolute or relative to session folder) to override the default under launcher_metadata.",
    )
