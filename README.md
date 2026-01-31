# CSV Parser Modes

A versatile command-line CSV file reader and parser built with Python. This application provides an intuitive interface for managing, displaying, and analyzing CSV files with support for multiple operational modes.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Current Features](#current-features)
- [Project Architecture](#project-architecture)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
  - [Commands](#commands)
  - [Examples](#examples)
- [Project Structure](#project-structure)
- [SQL Mode & Clean Mode Implementation](#sql-mode--clean-mode-implementation)
- [Future Roadmap](#future-roadmap)
- [Contributing](#contributing)

---

## Project Overview

**CSV Parser Modes** is a CLI-based application designed to simplify CSV file management and data exploration. 
The project is built with extensibility in mind, featuring a modular architecture that supports multiple operational modes 
(currently Default Mode, with SQL Mode and Clean Mode in development).

### Key Design Philosophy

- **Mode-based Architecture**: Different operational modes for different use cases
- **User-Friendly CLI**: Interactive command-line interface with command history support
- **Extensible Design**: Easy to add new modes and commands
- **File Management**: Register and manage multiple CSV files with custom display names

---

## Current Features

### ✅ Default Mode (Currently Implemented)

The application starts in **Default Mode**, which provides:

1. **File Management**
   - Insert individual CSV files with optional custom display names
   - Load all CSV files from a directory (with recursive option)
   - Rename file display names
   - View all registered files

2. **Data Display**
   - Display CSV file contents in a formatted table
   - Preview files with configurable row limits
   - View all loaded files or specific files by name
   - Color-coded output for better readability

3. **Navigation & History**
   - Command history with arrow key support (up/down navigation)
   - Support for keyboard navigation (left/right arrows, home/end keys)
   - Command completion history tracking
   - Exit and shutdown commands

4. **User Interface**
   - Color-coded terminal output (success, error, warning messages)
   - Help menu with command documentation
   - Formatted table display for CSV data
   - Column width auto-calculation for readable output

---

## How It Works

### Application Flow

```
┌─────────────────┐
│   main.py       │
│   (Entry Point) │
└────────┬────────┘
         │
         v
┌──────────────────────┐
│  DefaultMode()       │
│  - Initialize        │
│  - Load file handler │
│  - Start CLI loop    │
└────────┬─────────────┘
         │
         v
   ┌─────────────┐
   │ Main Loop   │ ◄──── Command History Support
   └─────┬───────┘
         │
    ┌────┴────────────────────┬─────────────────────┐
    │                         │                     │
    v                         v                     v
┌────────────┐          ┌──────────────┐      ┌──────────────┐
│File Mgmt   │          │Data Display  │      │Navigation    │
│- insert    │          │- display-data│      │- help        │
│- load      │          │- filenames   │      │- exit        │
│- rename    │          │              │      │- --shutdown  │
└────────────┘          └──────────────┘      └──────────────┘
```

### Key Components

#### 1. **DefaultMode** (`modes/defaultmode.py`)
- Central handler for all user commands in default mode
- Manages file interactions through File_Handler
- Parses user input and delegates to appropriate handlers
- Provides formatted output and error handling

#### 2. **File_Handler** (`utility/file_handler.py`)
- Maintains in-memory list of file registrations
- Maps file paths to display names
- Provides duplicate name detection
- Generates unique names for conflicting duplicates

#### 3. **CommandHistory** (`commands/history.py`)
- Tracks previously executed commands (max 100 by default)
- Supports navigation through history (up/down arrows)
- Prevents duplicate consecutive commands from being stored

#### 4. **Utility Classes** (`utility/`)
- **Colors**: Terminal color codes for styled output
- **Prompts**: Customizable CLI prompts
- **Utility**: Input handling with arrow key support
- **Text_Handler**: Text formatting utilities

---

## Installation

### Prerequisites
- Python 3.8 or higher
- Windows OS (uses `msvcrt` for input handling)

### Setup

```bash
# Clone the repository
git clone https://github.com/Sphesihlebjamile/csv_parser_modes.git
cd csv_parser_modes

# Run the application
python main.py
```

---

## Usage Guide

### Commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| `insert` | `<file_path> [display_name]` | Add a new CSV file with optional custom display name |
| `load` | `<directory_path> [*]` | Load all CSV files from directory; use `*` for recursive |
| `filenames` | — | Show list of all registered files |
| `display-data` | `[filename1 filename2 ...]` | Display file contents (all files if none specified) |
| `rename` | `<current_name> <new_name>` | Rename a file's display name |
| `help` | — | Show this help message |
| `exit` | — | Exit the application or return to DefaultMode if not already there |
| `--shutdown` | — | Force shutdown the application |

### Examples

#### Insert a single CSV file
```
--csv-reader$ insert C:\data\sales.csv
Inserted your new file name as 'sales'.
```

#### Insert with custom display name
```
--csv-reader$ insert C:\data\sales.csv Q1_Sales
Inserted your new file name as 'Q1_Sales'.
```

#### Load all CSV files from a directory
```
--csv-reader$ load C:\data
Loaded CSV files from 'C:\data':

Root directory:
- sales
- products
- customers
```

#### Load recursively from subdirectories
```
--csv-reader$ load C:\data *
Loaded CSV files recursively from 'C:\data':

Root directory:
- sales
- products

Directory 'reports':
- quarterly_report
- annual_report
```

#### Display specific files
```
--csv-reader$ display-data sales
File: sales
──────────────────────────────────
ID | Product | Quantity | Price
──────────────────────────────────
1  | Widget  | 100      | $9.99
2  | Gadget  | 50       | $19.99
──────────────────────────────────
```

#### Rename a file
```
--csv-reader$ rename sales Q1_Sales
Filename has been renamed from 'sales' to 'Q1_Sales'.
```

---

## Project Structure

```
csv_parser_modes/
├── main.py                           # Entry point
├── README.md                         # Documentation
├── commands/
│   ├── commands.py                   # Command constants and definitions
│   └── history.py                    # Command history management
├── modes/
│   └── defaultmode.py                # Default mode implementation
└── utility/
    ├── colors.py                     # Terminal color codes
    ├── file_handler.py               # File registration management
    ├── prompts.py                    # CLI prompt definitions
    ├── text_handler.py               # Text formatting utilities
    └── utility.py                    # General utilities (input handling)
```

---

## SQL Mode & Clean Mode Implementation

The project is transitioning from **DefaultMode** (file management) to include **SQL Mode** and **Clean Mode**, 
following a **hybrid architecture** with DuckDB and temporary file management.

### 🗺️ Implementation Roadmap

The implementation is broken down into **6 phases** for incremental development:

| Phase | Focus | Status |
|-------|-------|--------|
| 0 | Foundation Setup | ⏳ Planned |
| 1 | SQL Mode (Core) | ⏳ Planned |
| 2 | SQL Mode Enhancement | ⏳ Planned |
| 3 | Clean Mode | ⏳ Planned |
| 4 | Mode Integration | ⏳ Planned |
| 5 | Cross-Mode Features | ⏳ Planned |
| 6 | Polish & Optimization | ⏳ Planned |

### 🚀 MVP Target
Complete **Phases 0-4** to achieve a working MVP with both SQL Mode and Clean Mode.

**Estimated Time to MVP:** 11-15 hours

**Full Feature Set:** Add Phases 5-6 (additional 12-17 hours)

---

## SQL Mode & Clean Mode Implementation

### Hybrid Architecture Overview

This project will implement a **hybrid approach** combining:
1. **DuckDB** - For fast, direct CSV querying without copying
2. **Temp File Management** - For optional data modification workflows

```
-----------------------------------------------------------
|                  DefaultMode                            |
|  (File registration, display, management)               |
-----------------------------------------------------------
                     │
         ┌───────────┴───────────┐
         │                       │
         v                       v
    ┌─────────┐            ┌──────────┐
    │SQLMode  │            │CleanMode │
    │(DuckDB) │            │(Temp Dir)│
    └─────────┘            └──────────┘
```

---

## Contributing

Contributions are welcome! To contribute:

1. Create a feature branch from `develop`
2. Make your changes following the existing code style
3. Test thoroughly
4. Submit a pull request with a clear description

---

## License

This project is open source. Check the repository for license details.

---

## Support & Feedback

For issues, suggestions, or feedback:
- Open an issue on GitHub
- Contact the development team
- Check existing documentation and FAQs

---

**Happy CSV parsing! 📊**

