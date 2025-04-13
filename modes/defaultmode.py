import sys
from typing import List, Tuple

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
                    pass
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