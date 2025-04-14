import sys
from typing import List, Tuple
from pathlib import Path, WindowsPath

from commands.commands import Commands
from commands.history import CommandHistory
from utility.colors import Colors
from utility.utility import Utility
from utility.file_handler import File_Handler

class DefaultMode:
    def __init__(self):
        self.history = CommandHistory()
        self.file_handler = File_Handler() # Create a file handler instance

    @staticmethod
    def parse_input(input_str: str) -> List[Tuple[str, str]]:
        """
        Parse the input string to extract file path and optional display name.
    
        Args:
            input_str (str): Input string from user
    
        Returns:
            tuple: (file_path, display_name)
        """
        parts = input_str.strip().split()
        if not parts:
            return (None, None)

        file_path = parts[0]
        display_name = parts[1] if len(parts) > 1 else None
        return (file_path, display_name)

    def handle_insert(self, args) -> None:
        """
        Handle the insert command.
    
        Args:
            args (list): Command arguments
            file_entries (list): List of file entries
    
        Returns:
            bool: True if command was successful
        """
        if not args:
            print(f"{Colors.FAIL}Error: insert command requires a file path or directory.{Colors.ENDC}")
            return False

        data = " ".join(args)
        file_path, display_name = self.parse_input(data)

        if not file_path:
            print(f"{Colors.FAIL}Error: Please enter a valid file path.{Colors.ENDC}")
            return False

        if Path(file_path).exists() == False or Path(file_path).is_file() == False:
            print(f'{Colors.FAIL}Error: Please enter a valid file path.{Colors.ENDC}')
            return False

        # If no display name provided, use the file name or generate a random one
        if not display_name:
            base_name = Path(file_path).stem
            is_duplicated = self.file_handler.does_filename_exist(base_name)
            if is_duplicated:
                display_name = self.file_handler.generate_filename(base_name)
            else:
                display_name = base_name
        else:
            is_duplicated = self.file_handler.does_filename_exist(display_name)
            if is_duplicated:
                print(f"{Colors.FAIL}Error: Display name already exists. Please choose a different name.{Colors.ENDC}")
                return False

        self.file_handler.insert(file_path, display_name)
        print(f"{Colors.GREEN}Inserted your new file name as '{display_name}'.{Colors.ENDC}")
        return True

    def handle_load(self, args) -> bool:
        """
        Handle the load command to load all CSV files from a directory.
    
        Args:
            args (list): Command arguments (directory_path [depth_level|*])
            file_entries (list): List of file entries
    
        Returns:
            bool: True if command was successful
        """
        if not args:
            print(f"{Colors.FAIL}Error: load command requires a directory path{Colors.ENDC}")
            return False

        directory_path = args[0]
        recursive = len(args) > 1 and args[1] == '*'

        # Check if directory exists
        dir_path = Path(directory_path)
        if not dir_path.is_dir():
            print(f"{Colors.FAIL}Error: Directory '{directory_path}' does not exist{Colors.ENDC}")
            return False

        # Find all CSV files in the directory (recursively if '*' is specified)
        if recursive:
            csv_files = list(dir_path.rglob('*.csv'))
        else:
            csv_files = list(dir_path.glob('*.csv'))

        if not csv_files:
            search_msg = "recursively in all subdirectories" if recursive else "in directory"
            print(f"{Colors.WARNING}No CSV files found {search_msg} '{directory_path}'{Colors.ENDC}")
            return False

        # Add each CSV file to the file handler and track loaded files with their paths
        for file_path in csv_files:
            display_name = Path(file_path).stem
            is_duplicated = self.file_handler.does_filename_exist(display_name)
            if is_duplicated:
                display_name = self.file_handler.generate_filename(display_name)
            self.file_handler.insert(file_path, display_name)

        # Display the loaded files grouped by directory
        search_msg = "recursively from" if recursive else "from"
        print(f"\n{Colors.HEADER}Loaded CSV files {search_msg} '{directory_path}':{Colors.ENDC}")

        # Group files by their parent directory
        by_directory = {}
        for file_path, display_name in self.file_handler.get_files():
            parent = file_path.parent
            if parent not in by_directory:
                by_directory[parent] = []
            by_directory[parent].append(display_name)

        # Print files grouped by directory
        for directory, files in sorted(by_directory.items()):
            relative_path = directory.relative_to(dir_path)
            if str(relative_path) == ".":
                print(f"\n{Colors.CYAN}Root directory:{Colors.ENDC}")
            else:
                print(f"\n{Colors.CYAN}Directory '{relative_path}':{Colors.ENDC}")
            for display_name in sorted(files):
                print(f"{Colors.GREEN}- {display_name}{Colors.ENDC}")
        print()
        return True

    def run(self):
        print(f"{Colors.HEADER}Welcome to CSV Reader{Colors.ENDC}")
        print(f"{Colors.CYAN}{'-' * 50}{Colors.ENDC}")

        while True:
            try:
                prompt = f'{Colors.BOLD}--csv-reader${Colors.ENDC}'
                command = Utility.get_user_input(prompt, self.history)

                if not command:
                    continue

                # Split command into parts
                parts = command.split()
                cmd = parts[0]
                args = parts[1:]

                if cmd == Commands.INSERT:
                    self.handle_insert(args)
                if cmd == Commands.LOAD:
                    self.handle_load(args)
                elif cmd == Commands.EXIT:
                    print(f'\n{Colors.GREEN}Thank you for using CSV Reader!{Colors.ENDC}')
                    break
                elif cmd == Commands.SHUTDOWN:
                    print(f'\n{Colors.GREEN}Thank you for using CSV Reader!{Colors.ENDC}')
                    sys.exit(0)
                else:
                    print(f"\n{Colors.FAIL}Error: Unknown command '{cmd}'. Type 'help' to see a list of available commands.{Colors.ENDC}\n")

            except KeyboardInterrupt:
                print(f'\n\n{Colors.GREEN}Thank you for using CSV Reader!{Colors.ENDC}')
                break
            except Exception as e:
                print(f'{Colors.FAIL}Error: {str(e)}{Colors.ENDC}')