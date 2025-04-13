import sys
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