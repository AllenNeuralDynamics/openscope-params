from __future__ import annotations

"""Pydantic model for module `wait_for_user_input` parameters."""

from pydantic import BaseModel, ConfigDict, Field


MODULE_DESCRIPTION = "Pause until an operator confirms readiness (press Enter)."


class Parameters(BaseModel):
    model_config = ConfigDict(extra="allow")

    prompt: str | None = Field(
        default=None,
        description="Prompt shown to the operator. If omitted, the launcher uses a built-in default.",
        examples=["Rig ready? Press Enter to start Bonsai"],
    )

    fail_if_no_input: bool = Field(
        default=False,
        description="If true, treat missing stdin (non-interactive) as an error.",
    )
