import string
import random
from pathlib import WindowsPath
from typing import List, Tuple

class File_Handler:
    """
    Manages file access and updates
    """
    def __init__(self):
        self.files: List[Tuple[str, str]] = [] # List of files

    def get_files(self) -> List[Tuple[WindowsPath, str]]:
        """
        Get's all the files that are stored in the application

        Returns:
            List[Tuple[WindowsPath, str]]: A list of files stored in the application
        """
        return self.files

    def does_filename_exist(self, file_name: str) -> bool:
        """
        Checks if the current name is assigned to any file-path

        Args:
            file_name (str): The name of the file to check

        Returns:
            bool: Represents whether or not a file with the provided file_name exists
        """
        res = [tup for tup in self.files if file_name in tup]
        return bool(res)

    def update_filename(self, original_filename: str, new_filename: str) -> bool:
        """
        Updates the name of the file in the list

        Args:
            original_filename (str): The name of the file as it's currently stored
            new_filename (str): The new name to be given to the file

        Returns:
            bool: represents whether or not the file 'name' update was successful
        """
        result = [tup for tup in self.files if original_filename in tup]
        if not result or len(result) != 1:
            return False
        tup_index = self.files.index(result[0])
        self.files[tup_index] = (self.files[tup_index][0], new_filename)
        return True

    def insert(self, file_path: str, file_name: str) -> None:
        """
        Inserts the provided file-path and file-name into the stored list of files

        Args:
            file_path: (str): The path to the file you want to insert
            file_name: (str): The name of the file you want to insert

        Returns:
            None
        """
        self.files.append((file_path, file_name))

    @staticmethod
    def generate_filename(base_name: str) -> str:
        """
        Generate a random name based on the original filename.
    
        Args:
            base_name (str): The originale name of the file
    
        Returns:
            str: Random name based on the original filename
        """
        # Generate a random suffix of 4 characters
        random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k = 4))
        return f"{base_name}_{random_suffix}"