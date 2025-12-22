from __future__ import annotations

"""Pydantic model for module `session_enhancer_bonsai` parameters."""

from pydantic import BaseModel, ConfigDict


class Parameters(BaseModel):
    model_config = ConfigDict(extra="allow")

    pass
