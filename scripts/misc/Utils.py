import pathlib
from datetime import datetime
import json
import sys
from os import makedirs

def _get_proj_folder():
    if getattr(sys, "frozen", False):
        return pathlib.Path(sys.executable).parent
    
    return pathlib.Path(pathlib.Path(__file__).resolve().parent.parent.parent)

ROOT = _get_proj_folder()

def merge_dict_lists(dict_1, dict_2):
    for key in dict_2:
        assert key in dict_1
        # merge without duplicates
        for val in dict_2[key]:
            if val not in dict_1[key]:
                dict_1[key].append(val)

def create_folder(folder_dir):
    makedirs(folder_dir, exist_ok=True)

def create_file(dir: pathlib.Path | str, name: str | None = None):
    dir = pathlib.Path(dir)
    full_path = dir if name is None else dir / name
    full_path.touch()

