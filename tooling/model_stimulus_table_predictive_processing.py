from __future__ import annotations

"""Pydantic model for module `stimulus_table_predictive_processing` parameters."""

from pydantic import BaseModel, ConfigDict


class Parameters(BaseModel):
    model_config = ConfigDict(extra="allow")

    pass
