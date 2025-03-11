import hashlib
import shutil
import os
from typing import List

def calculate_checksum(file_path: str) -> str:
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

def copy_file(src: str, dst: str):
    shutil.copy(src, dst)

def list_xml_files(directory: str) -> List[str]:
    return [f for f in os.listdir(directory) if f.lower().endswith(".xml")]