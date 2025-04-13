import sys

from commands.commands import Commands
from commands.history import CommandHistory
from utility.colors import Colors
from utility.utility import Utility

class DefaultMode:
    def __init__(self):
        self.history = CommandHistory()

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

                if cmd == Commands.EXIT:
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