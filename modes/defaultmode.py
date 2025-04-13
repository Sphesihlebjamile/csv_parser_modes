from commands.commands import Commands
from utility.colors import Colors

class DefaultMode:
    def __init__(self):
        print("Initiating default mode")

    def run(self):
        print(f"{Colors.HEADER}Welcome to CSV Reader{Colors.ENDC}")
        print(f"{Colors.CYAN}{'-' * 50}{Colors.ENDC}")