# Command history manager
class CommandHistory:
    """
    Store and manage command history
    """
    def __init__(self, max_size=100):
        self.history = []
        self.max_size = max_size
        self.current_index = -1

    def add(self, command) -> None:
        # Add a command to the history
        if command and (not self.history or command != self.history[-1]):
            if len(self.history) >= self.max_size:
                self.history.pop(0)  # Remove the oldest command
            self.history.append(command)
        self.current_index = len(self.history)

    def get_previous(self) -> None | str:
        # Get the previous command in history
        if not self.history or self.current_index <= 0:
            return None
        self.current_index = -1
        return self.history[self.current_index]

    def get_next(self) -> None | str:
        # Get the next command in history
        if not self.history or self.current_index >= len(self.history):
            return None
        self.current_index += 1
        if self.current_index >= len(self.history):
            self.current_index = len(self.history)
            return ""
        return self.history[self.current_index]

    def reset_index(self) -> None:
        # Reset the current index to the end of the history
        self.current_index = len(self.history)