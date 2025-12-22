from __future__ import annotations

from typing import Annotated, Literal, Union

from pydantic import BaseModel, ConfigDict, Field


class ScriptModuleParameters(BaseModel):
    model_config = ConfigDict(extra="allow")

    function: str | None = Field(default=None, description="Function name to invoke from the script module.")
    function_args: dict | None = Field(default=None, description="Arguments passed to the script function.")


class PipelineEntryObject(BaseModel):
    model_config = ConfigDict(extra="allow")

    module_type: Literal["launcher_module", "script_module"] | None = Field(
        default=None,
        description="How to execute this pipeline entry.",
    )
    module_path: str = Field(
        ..., description="Identifier for module to run (launcher_module name or script path)."
    )
    module_parameters: dict | ScriptModuleParameters | None = Field(
        default=None,
        description="Arguments passed to the module.",
    )


class LegacyRepoModuleEntry(BaseModel):
    model_config = ConfigDict(extra="allow")

    type: Literal["repo_module"] = Field(default="repo_module", description="Legacy pipeline entry type.")
    repo_relative_path: str = Field(..., description="Repo-relative path containing the callable.")
    function: str | None = Field(default=None, description="Function name to invoke.")
    kwargs: dict | None = Field(default=None, description="Keyword arguments passed to the function.")


# We intentionally keep PipelineEntry permissive to avoid introducing a second hierarchy
# of module-entry models here; module schemas are exported from per-module files.
PipelineEntry = Union[str, PipelineEntryObject, LegacyRepoModuleEntry]


class LauncherParams(BaseModel):
    model_config = ConfigDict(extra="allow")

    schema_: Annotated[
        str | None,
        Field(default=None, alias="$schema", description="JSON Schema identifier (relative path within repo)."),
    ]

    launcher_version: str | None = Field(default=None)
    launcher: Literal["base", "bonsai", "python", "matlab"] | None = Field(default=None)

    subject_id: str | int = Field(..., description="Subject identifier used for naming and metadata lookup.")
    user_id: str = Field(..., description="Operator/user identifier recorded alongside the session.")

    # Optional richer identifiers. Kept as plain objects to avoid extra dependencies.
    operator: dict | None = Field(default=None, description="Optional operator identifier object.")
    experiment_code: dict | None = Field(default=None, description="Optional experiment code identifier object.")

    output_root_folder: str | None = None
    output_session_folder: str | None = None
    session_uuid: str | None = None

    rig_id: str | None = None
    rig_config_path: str | None = None

    repository_url: str | None = None
    repository_commit_hash: str | None = None
    local_repository_path: str | None = None

    script_path: str | None = None
    script_parameters: dict | None = None

    pre_acquisition_pipeline: list[PipelineEntry] | None = None
    post_acquisition_pipeline: list[PipelineEntry] | None = None

    # Common metadata + notes + archiving keys are left as permissive extras here;
    # module-specific parameter typing lives in per-module Pydantic files.
