import string
from pathlib import Path
from typing import List, Tuple

class File_Handler:
    def __init__(self):
        self.files: List[Tuple[str, str]] = []

    def insert(self, file_path: str, file_name: str) -> None:
        self.files.append((file_path, file_name))
