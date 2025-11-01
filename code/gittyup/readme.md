# 🚀 Gitty Up

**Automatically update all Git repositories in a directory tree**

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Gitty Up is a CLI tool for developers who work across multiple projects and machines. Never deal with merge conflicts from forgotten `git pull` commands again!

---

## 📋 Table of Contents

- [The Problem](#-the-problem)
- [The Solution](#-the-solution)
- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Examples](#-examples)
- [Configuration](#-configuration)
- [Development](#-development)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🔴 The Problem

When working on multiple computers or with many team members, and across many projects, it's easy to start working on an existing one and forget to do a `git pull`. Then when it's time to commit the changes, you realize you have merge conflicts and more. This is not fun.

## ✅ The Solution

Gitty Up runs in a folder at the root of your source code. It traverses the current directory and all subdirectories. Whenever it discovers a Git repository, it runs `git pull --all` to ensure that every project in this directory tree is up to date and ready to roll.

---

## ✨ Features

- 🔍 **Automatic Discovery**: Finds all Git repositories in a directory tree
- 🎨 **Beautiful Output**: Color-coded status messages with progress indicators
- 🛡️ **Safety First**: Skips repositories with uncommitted changes by default
- ⚙️ **Configurable**: Customize exclusion patterns and behavior
- 🚀 **Fast**: Efficiently scans even large directory structures
- 🔒 **Smart Detection**: Checks for upstream branches and repository status
- 🎯 **Dry Run Mode**: Preview what will happen before making changes
- 📊 **Summary Reports**: Clear statistics after operations complete

---

## 📦 Installation

### Prerequisites

- **Python 3.9 or higher**
- **Git 2.20 or higher**

### Install from Source

1. Clone this repository:
```bash
git clone https://github.com/yourusername/gittyup.git
cd gittyup
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install the package in development mode:
```bash
pip install -e .
```

### Verify Installation

```bash
gittyup --version
```

---

## 🚀 Quick Start

**Update all repositories in the current directory:**
```bash
gittyup
```

**Update all repositories in a specific directory:**
```bash
gittyup ~/projects
```

**See what would happen without making changes:**
```bash
gittyup --dry-run
```

---

## 📖 Usage

```bash
gittyup [OPTIONS] [PATH]
```

### Arguments

- `PATH`: Directory to scan (default: current directory)

### Options

| Option | Description |
|--------|-------------|
| `--max-depth N` | Maximum directory depth to traverse (default: 10) |
| `--exclude PATTERN` | Directory patterns to exclude (can be used multiple times) |
| `--skip-dirty` | Skip repositories with uncommitted changes (default) |
| `--no-skip-dirty` | Update even if there are uncommitted changes |
| `--dry-run` | Show what would happen without making changes |
| `--version` | Show version information |
| `--help` | Show help message |

---

## 💡 Examples

### Basic Usage

```bash
# Update all repos in current directory
gittyup

# Update all repos in ~/projects
gittyup ~/projects

# Update with verbose output
gittyup --verbose
```

### With Options

```bash
# Exclude specific directories
gittyup --exclude temp --exclude archive

# Limit search depth
gittyup --max-depth 5

# Preview changes without executing
gittyup --dry-run

# Force update even with uncommitted changes (use with caution!)
gittyup --no-skip-dirty
```

### Real-World Examples

```bash
# Update all work projects
gittyup ~/workspace/projects

# Update personal projects excluding old archives
gittyup ~/personal --exclude "old-*" --exclude archive

# Check what needs updating without actually updating
gittyup ~/all-repos --dry-run
```

---

## ⚙️ Configuration

### Default Excluded Directories

The following directories are automatically excluded:
- `node_modules`
- `venv`, `.venv`
- `__pycache__`
- `.tox`
- `build`, `dist`

### Repository Status

Gitty Up checks each repository before updating:
- ✅ **Clean repositories**: Updated automatically
- ⚠️ **Uncommitted changes**: Skipped by default (use `--no-skip-dirty` to override)
- ℹ️ **No upstream**: Skipped with informational message
- ❌ **Errors**: Reported with clear error messages

---

## 🔧 Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/gittyup.git
cd gittyup

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install package in editable mode
pip install -e .
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=gittyup --cov-report=html

# Run specific test file
pytest tests/test_scanner.py -v
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type checking
mypy src/
```

### Project Structure

```
gittyup/
├── src/gittyup/         # Source code
│   ├── __init__.py      # Package initialization
│   ├── __main__.py      # Entry point for python -m gittyup
│   ├── cli.py           # CLI interface
│   ├── scanner.py       # Directory scanning
│   ├── git_operations.py # Git commands
│   ├── output.py        # Formatted output
│   └── exceptions.py    # Custom exceptions
├── tests/               # Test suite
├── docs/                # Documentation
├── plans/               # Project planning
├── pyproject.toml       # Package configuration
├── requirements.txt     # Runtime dependencies
└── requirements-dev.txt # Development dependencies
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

Please ensure:
- All tests pass
- Code is formatted with `black`
- Type hints are included
- Documentation is updated

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [Click](https://click.palletsprojects.com/) for CLI
- Colored output by [Colorama](https://github.com/tartley/colorama)
- Beautiful formatting with [Rich](https://rich.readthedocs.io/)
- Git operations via [GitPython](https://gitpython.readthedocs.io/)

---

## 📬 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/gittyup/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/gittyup/discussions)

---

**Made with ❤️ by developers, for developers**