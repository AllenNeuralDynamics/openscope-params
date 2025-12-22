from __future__ import annotations

"""Pydantic model for module `session_enhancer_slap2` parameters."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Parameters(BaseModel):
    model_config = ConfigDict(extra="allow")

    session_type: Literal["Parent", "Branch"] | None = Field(
        default=None,
        description="Whether this session is a parent (primary) or a branch (child/follow-up) session.",
    )
    targeted_structure: str | None = Field(
        default=None,
        description="Brain structure targeted by the experiment (free-text).",
    )
    fov_coordinate_ml: float | None = Field(default=None, description="Field-of-view mediolateral coordinate.")
    fov_coordinate_ap: float | None = Field(default=None, description="Field-of-view anteroposterior coordinate.")
    fov_coordinate_unit: str | None = Field(
        default=None,
        description="Units for FOV coordinates (e.g. 'mm' or 'um').",
        examples=["mm"],
    )
    fov_reference: str | None = Field(
        default=None,
        description="Reference origin used for coordinates (free-text).",
        examples=["bregma"],
    )
    magnification: str | None = Field(
        default=None,
        description="Objective or system magnification descriptor.",
        examples=["16x"],
    )
    fov_scale_factor: float | None = Field(
        default=None,
        description="Scale factor applied to convert coordinates/pixels to physical units (module-specific).",
    )
