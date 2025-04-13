import string
from pathlib import Path
from typing import List, Tuple

class File_Handler:
    def __init__(self):
        self.files: List[Tuple[str, str]] = []

    def get_files(self) -> List[Tuple[str, str]]:
        return self.files

    def does_filename_exist(self, file_name: str) -> bool:
        res = [tup for tup in self.files if file_name in tup]
        return bool(res)

    def update_filename(self, original_filename: str, new_filename: str) -> bool:
        res = [tup for tup in self.files if original_filename in tup]
        if not res or len(res) != 1:
            return False
        tup_index = self.files.index(res[0])
        self.files[tup_index] = (self.files[tup_index][0], new_filename)
        return True

    def insert(self, file_path: str, file_name: str) -> None:
        self.files.append((file_path, file_name))