import os
import json
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

config_path = resource_path('config/config.json')

with open(config_path, "r", encoding="utf-8") as file:
    CONFIG = json.load(file)

def get_config():
    return CONFIG