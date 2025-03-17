import os
import json
from pathlib import Path
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

config_path = resource_path('config/config.json')

with open(config_path, "r") as file:
    CONFIG = json.load(file)

def network_drive_available() -> bool:
    return os.path.exists(CONFIG["network_drive"])

def resolve_local_profiles_dir() -> str:
    return os.path.expandvars(CONFIG["local_profiles_dir"])

def get_shared_profiles_dir() -> str:
    return CONFIG["shared_profiles_dir"]

def get_user_shared_profiles(username: str) -> str:
    return os.path.join(CONFIG["shared_profiles_dir"], username)