from __future__ import annotations

"""Pydantic model for module `experiment_notes_finalize` parameters."""

from pydantic import BaseModel, ConfigDict, Field


class Parameters(BaseModel):
    model_config = ConfigDict(extra="allow")

    experiment_notes_filename: str | None = Field(
        default=None,
        description="Path to the notes file (absolute or placeholder-expanded).",
        examples=["{session_folder}/notes/experiment_notes.txt"],
    )
    experiment_notes_encoding: str = Field(
        default="utf-8",
        description="Text encoding used when reading the notes file.",
    )
    experiment_notes_preview: bool = Field(
        default=True,
        description="If true, print a preview of notes content to the console.",
    )
    experiment_notes_preview_limit: int = Field(
        default=2000,
        ge=0,
        description="Limit for preview output (module-specific).",
    )
    experiment_notes_confirm_prompt: str | None = Field(
        default=None,
        description="Prompt shown to the operator to confirm notes are complete.",
        examples=["Confirm experiment notes are saved; type 'yes' to finish."],
    )
    experiment_notes_autoclose_editor: bool = Field(
        default=True,
        description="If true, attempts to close the launched editor using the PID stored in the notes header.",
    )
