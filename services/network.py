import os
import json
from pathlib import Path

with open("config/config.json", "r") as file:
    CONFIG = json.load(file)

def network_drive_available() -> bool:
    return os.path.exists(CONFIG["network_drive"])

def resolve_local_profiles_dir() -> str:
    return os.path.expandvars(CONFIG["local_profiles_dir"])

def get_shared_profiles_dir() -> str:
    return CONFIG["shared_profiles_dir"]

def get_user_shared_profiles(username: str) -> str:
    return os.path.join(CONFIG["shared_profiles_dir"], username)