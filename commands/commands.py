class Commands:
    INSERT = "insert"
    LOAD = "load"
    FILENAMES = "filenames"
    DISPLAY_DATA = "display-data"
    RENAME = "rename"
    HELP = "help"
    EXIT = "exit"
    SHUTDOWN = "--shutdown"
    SQL_MODE = "-sql"
    CLEAN = "-clean"
    ALL_COMMANDS = [
            ("insert", "<file_path> [display_name]", "Add a new CSV file with optional custom display name"),
            ("load", "<directory_path>", "Load all CSV files from the specified directory"),
            ("filenames", "", "Show list of registered files"),
            ("display-data", "[filename1 filename2 ...]", "Display file contents. If no filenames provided, displays all files"),
            ("rename", "<current_name> <new_name>", "Rename a file's display name"),
            ("-sql", "<filename1> [filename2 ...]", "Enter SQL mode with specified files (1-10 files required)"),
            ("help", "", "Show this help message"),
            ("exit", "", "Exit the application"),
            ("--shutdown", "", "Force shutdown the application (works in both modes)"),
            ("-clean", "<filename1> [filename2 ...]", "Enter Clean mode with specified files (1-10 files required)")
        ]