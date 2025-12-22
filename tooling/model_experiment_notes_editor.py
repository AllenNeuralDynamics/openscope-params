from __future__ import annotations

"""Pydantic model for module `experiment_notes_editor` parameters."""

from typing import Union

from pydantic import BaseModel, ConfigDict, Field


class Parameters(BaseModel):
    model_config = ConfigDict(extra="allow")

    experiment_notes_filename: str | None = Field(
        default=None,
        description="Relative path (inside the session folder) for the notes file.",
        examples=["notes/experiment_notes.txt"],
    )
    experiment_notes_encoding: str = Field(
        default="utf-8",
        description="Text encoding used when reading/writing the notes file.",
    )
    experiment_notes_launch_editor: bool = Field(
        default=True,
        description="If true, launches an editor command to open the notes file.",
    )
    experiment_notes_editor_command: Union[str, list[str], None] = Field(
        default=None,
        description="Editor command (string) or argv list.",
    )
    experiment_notes_editor_args: Union[str, list[str], None] = Field(
        default=None,
        description="Additional args (string) or argv list.",
    )
