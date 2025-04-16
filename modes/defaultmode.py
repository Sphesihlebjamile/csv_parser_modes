import sys
import csv
from typing import List, Tuple
from pathlib import Path

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

    def handle_display_filenames(self) -> bool:
        """
        Handle the display-filenames command.
        """
        files = self.file_handler.get_files()
        if not files:
            print(f"{Colors.WARNING}No files have been added yet.{Colors.ENDC}")
            return False

        print(f"\n{Colors.HEADER}Registered files:{Colors.ENDC}")
        for _, display_name in files:
            print(f"{Colors.GREEN}- {display_name}{Colors.ENDC}")
        print()
        return True

    def read_csv_file(self, file_path, display_name, max_data = 10) -> None:
        """
        Read and display the contents of a CSV file.
    
        Args:
            file_path (str): Path to the CSV file
            display_name (str): Custom name to display for the file
        """
        try:
            # Check if file exists
            if not Path(file_path).exists():
                print(f"{Colors.FAIL}Error: File '{file_path}' does not exist.{Colors.ENDC}")
                return

            # Open and read the csv file
            with open(file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                rows = list(csv_reader)

                if not rows:
                    print(f"{Colors.FAIL}Error: CSV file '{file_path}' is empty.{Colors.ENDC}")
                    return

                # Calculate column widths
                widths = Utility.get_column_widths(rows, max_rows = max_data)

                # Print file name and table
                print(f"\n{Colors.HEADER}File: {display_name or file_path}{Colors.ENDC}")
                separator = "-" * (sum(widths) + (len(widths) * 3) - 1)
                print(f"{Colors.CYAN}{separator}{Colors.ENDC}")
                # Print header row in orange and bold
                print(f"{Colors.ORANGE}{Colors.BOLD}{Utility.format_row(rows[0], widths)}{Colors.ENDC}")
                print(f"{Colors.CYAN}{separator}{Colors.ENDC}")

                # Print data rows in white
                for count, row in enumerate(rows[1:]):
                    if count == max_data:
                        break
                    print(f"{Colors.WHITE}{Utility.format_row(row, widths)}{Colors.ENDC}")
                print(f"{Colors.CYAN}{separator}{Colors.ENDC}")
                print("\n" + "="*80 + "\n")  # Separator between files

        except Exception as e:
            print(f"{Colors.FAIL}Error reading the CSV file '{file_path}' {str(e)}{Colors.ENDC}")

    def handle_displa_data(self, args) -> bool | None:
        """
        Handle the display-data command.
    
        Args:
            args (list): Command arguments
            file_entries (list): List of file entries
        """
        file_entries = self.file_handler.get_files()
        if not file_entries:
            print(f"{Colors.WARNING}No files have been added yet.{Colors.ENDC}")
            return False

        # Display all files
        if not args:
            for file_path, display_name in file_entries:
                self.read_csv_file(file_path, display_name, max_data = 10)
            return True

        # Display specific files
        for filename in args:
            found = False
            for file_path, display_name in file_entries:
                if display_name == filename:
                    self.read_csv_file(file_path, display_name, max_data = 100)
                    found = True
            if not found:
                print(f"{Colors.FAIL}Error: File '{filename}' not found{Colors.ENDC}")
    
    @staticmethod
    def handle_display_help():
        """
        Display help information in a tabular format.
        """
        # Caulcilate column widths
        cmd_width = max(len(cmd[0]) for cmd in Commands.ALL_COMMANDS) + 2
        args_width = max(len(cmd[1]) for cmd in Commands.ALL_COMMANDS) + 2
        desc_width = max(len(cmd[2]) for cmd in Commands.ALL_COMMANDS) + 2

        # Print header
        print(f"\n{Colors.HEADER}Available Commands:{Colors.ENDC}")
        separator = "-" * (cmd_width + args_width + desc_width + 6) # 6 for separators
        print(f"{Colors.CYAN}{separator}{Colors.ENDC}")
        print(f"{Colors.ORANGE}{Colors.BOLD}{'Command'.ljust(cmd_width)} | {'Arguments'.ljust(args_width)} | {'Description'.ljust(desc_width)}{Colors.ENDC}")
        print(f"{Colors.CYAN}{separator}{Colors.ENDC}")

        # Print commands
        for cmd, args, desc in Commands.ALL_COMMANDS:
            print(f"{Colors.WHITE}{cmd.ljust(cmd_width)} | {args.ljust(args_width)} | {desc.ljust(desc_width)}{Colors.ENDC}")
        print(f"{Colors.CYAN}{separator}{Colors.ENDC}\n")

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
                elif cmd == Commands.LOAD:
                    self.handle_load(args)
                elif cmd == Commands.FILENAMES:
                    self.handle_display_filenames()
                elif cmd == Commands.DISPLAY_DATA:
                    self.handle_displa_data(args)
                elif cmd == Commands.HELP:
                    self.handle_display_help()
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