from pathlib import Path

import toml


THIS_DIRECTORY_PATH = Path(__file__).parent
TOML_PATH = Path.joinpath(THIS_DIRECTORY_PATH, "..", "pyproject.toml")


def _get_project_meta() -> dict:
    """ Read Poetry meta information from the local pyproject.toml """
    with TOML_PATH.open() as pyproject_file:
        full_toml = toml.load(pyproject_file)

    return full_toml["tool"]["poetry"]


_meta = _get_project_meta()

description = _meta["description"]
author = _meta["authors"][0]
