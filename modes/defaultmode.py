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

                continue

            except KeyboardInterrupt:
                print(f'\n\n{Colors.GREEN}Thank you for using CSV Reader!{Colors.ENDC}')
                break
            except Exception as e:
                print(f'{Colors.FAIL}Error: {str(e)}{Colors.ENDC}')