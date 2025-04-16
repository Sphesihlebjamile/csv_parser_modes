import msvcrt
from commands.history import CommandHistory
from utility.text_handler import Text_Handler
from typing import List

class Utility:
    # Utility class to handle user input and other utility functions
    @staticmethod
    def get_user_input(prompt: str, history: CommandHistory) -> str:
        """
        Get input text from the user with arrow key and command history support
        """
        print(prompt, end = ' ', flush=True)
        input_text = ""
        cursor_pos = 0

        while True:
            char = msvcrt.getch()

            # Handle special keys
            if char == b'\xe0': # Arrow key prefix
                key = msvcrt.getch()

                if key == b'K':  # Left arrow
                    if cursor_pos > 0:
                        cursor_pos -= 1
                        msvcrt.putch(b'\b')
                elif key == b'M':  # Right arrow
                    if cursor_pos < len(input_text):
                        cursor_pos += 1
                        msvcrt.putch(input_text[cursor_pos-1].encode('utf-8'))
                elif key == b'H':  # Up arrow
                    if history:
                        prev_cmd = history.get_previous()
                        if prev_cmd is not None:
                            # Clear current line
                            while cursor_pos > 0:
                                msvcrt.putch(b'\b')
                                msvcrt.putch(b' ')
                                msvcrt.putch(b'\b')
                                cursor_pos -= 1
                            # Clear any remaining characters
                            for _ in range(len(input_text) - cursor_pos):
                                msvcrt.putch(b' ')
                            for _ in range(len(input_text) - cursor_pos):
                                msvcrt.putch(b'\b')
                            # Print previous command
                            input_text = prev_cmd
                            cursor_pos = len(input_text)
                            print(input_text, end='', flush=True)
                elif key == b'P':  # Down arrow
                    if history:
                        next_cmd = history.get_next()
                        if next_cmd is not None:
                            # Clear current line
                            while cursor_pos > 0:
                                msvcrt.putch(b'\b')
                                msvcrt.putch(b' ')
                                msvcrt.putch(b'\b')
                                cursor_pos -= 1
                            # Clear any remaining characters
                            for _ in range(len(input_text) - cursor_pos):
                                msvcrt.putch(b' ')
                            for _ in range(len(input_text) - cursor_pos):
                                msvcrt.putch(b'\b')
                            # Print next command
                            input_text = next_cmd
                            cursor_pos = len(input_text)
                            print(input_text, end='', flush=True)
                elif key == b'G':  # Home
                    while cursor_pos > 0:
                        cursor_pos -= 1
                        msvcrt.putch(b'\b')
                elif key == b'O':  # End
                    while cursor_pos < len(input_text):
                        msvcrt.putch(input_text[cursor_pos].encode('utf-8'))
                        cursor_pos += 1
                continue

            # Handle regular input
            if char == b'\r': # Enter key
                print()  # New line
                if history:
                    history.add(input_text)
                    history.reset_index()
                break
            elif  char == b'\x08': # Backspace key
                if cursor_pos > 0:
                    # Move cursor back
                    msvcrt.putch(b'\b')
                    # Clear the current character
                    msvcrt.putch(b' ')
                    # Move cursor back again
                    msvcrt.putch(b'\b')
                
                    # Update text and cursor
                    input_text = input_text[:cursor_pos-1] + input_text[cursor_pos:]
                    cursor_pos -= 1
                
                    # Reprint the rest of the text
                    for c in input_text[cursor_pos:]:
                        msvcrt.putch(c.encode('utf-8'))
                    # Add a space to clear the last character
                    msvcrt.putch(b' ')
                    # Move cursor back to position
                    for _ in range(len(input_text) - cursor_pos + 1):
                        msvcrt.putch(b'\b')
            elif char == b'\x7f': # Control Backspace combination key
                # Clear the entire line
                while cursor_pos > 0:
                    if input_text[cursor_pos-1] == ' ':
                        break
                    msvcrt.putch(b'\b')
                    msvcrt.putch(b' ')
                    msvcrt.putch(b'\b')
                    cursor_pos -= 1
                    input_text = input_text[:cursor_pos] + input_text[cursor_pos+1:]
                # input_text = ""
            else:
                try:
                    char = char.decode('utf-8')
                    # Insert character at cursor position
                    input_text = input_text[:cursor_pos] + char + input_text[cursor_pos:]
                    cursor_pos += 1
                    # Print the character
                    msvcrt.putch(char.encode('utf-8'))
                    # Reprint the rest of the text
                    for c in input_text[cursor_pos:]:
                        msvcrt.putch(c.encode('utf-8'))
                    # Move cursor back to position
                    for _ in range(len(input_text) - cursor_pos):
                        msvcrt.putch(b'\b')
                except UnicodeDecodeError:
                    continue

        return input_text

    @staticmethod
    def get_column_widths(rows: List[str], max_rows: int = 10) -> List[int]:
        """
        Calculate the maximum width needed for each column.
    
        Args:
            rows (list): List of rows from the CSV file
    
        Returns:
            list: List of maximum widths for each column
        """
        widths = []
        for count, row in enumerate(rows):
            if count == max_rows:
                break
            for i, cell in enumerate(row):
                # Truncate the cell content before calculating width
                truncated_cell = Text_Handler.truncate_text(cell)
                if i >= len(widths):
                    widths.append(len(truncated_cell))
                else:
                    widths[i] = max(widths[i], len(truncated_cell))
        return widths

    @staticmethod
    def format_row(row, widths):
        """
        Format a row with fixed column widths.
    
        Args:
            row (list): Row data
            widths (list): Column widths
    
        Returns:
            str: Formatted row string
        """
        formatted_cells = []
        for cell, width in zip(row, widths):
            # Truncate and pad the cell content
            truncated_cell = Text_Handler.truncate_text(cell)
            fromatted_cell = truncated_cell.ljust(width)
            formatted_cells.append(fromatted_cell)
        return ' | '.join(formatted_cells)