# Gitty Up 🚀  
### Keep your repos fresh. Keep your flow.

Never start work with stale code again. Gitty Up automatically discovers and updates all Git repositories in your project tree - in seconds, not minutes.

---

## Why Gitty Up?

**The Problem You Face:**  
You're juggling 5, 10, maybe 20 different projects. Client work, side projects, open source contributions. You switch between them constantly. And every time you start work, there's that nagging question: *"Did I pull the latest changes?"* 

Half the time you forget. Then boom - merge conflicts that could have been avoided. Or worse, you spend 30 minutes manually `cd`-ing into each project directory running `git pull` one by one.

**The Gitty Up Solution:**  
One command. All repositories. Always synchronized.

```bash
gittyup ~/projects
```

That's it. Start your workday with this one command, and every repository in your tree is fresh and ready to go. Parallel processing means updating 50 repos takes the same time as updating 5.

---

## What Makes It Special

🚀 **Blazing Fast** - Updates multiple repos in parallel (default: 4 concurrent workers)  
🛡️ **Totally Safe** - Never touches repositories with uncommitted changes  
🧠 **Zero Config** - Works perfectly out of the box with smart defaults  
⚡ **Automation Ready** - JSON output for scripts and CI/CD pipelines  
🎯 **Smart Discovery** - Finds repos automatically, skips junk directories like `node_modules` and `venv`  
🎨 **Beautiful Output** - Color-coded status updates that are easy to scan  
🔧 **Flexible** - Multiple strategies (pull, fetch, rebase), stash support, configurable everything

---

## Perfect For

- **Multi-project developers** managing client work, side projects, or microservices
- **Open source maintainers** tracking dozens of repositories
- **DevOps engineers** maintaining infrastructure repos at scale
- **Development teams** staying synchronized before daily standup
- **Consultants** switching between client codebases constantly

---

## Install & Run in 30 Seconds

```bash
# Install (when published to PyPI)
pip install gittyup

# Or install from source
git clone <repo-url>
cd gittyup
pip install -e .

# Run it
gittyup ~/projects
```

Done. That's the whole getting started guide.

---

## Quick Examples

```bash
# Update all repos in your projects folder
gittyup ~/projects

# Preview what would happen (dry run)
gittyup --dry-run

# Use 8 workers for even faster parallel updates
gittyup --workers 8

# Stash uncommitted changes, pull, then restore
gittyup --stash

# Output JSON for automation/scripting
gittyup --format json > results.json

# Limit how deep to search
gittyup --max-depth 2

# Exclude specific directories
gittyup --exclude "archived-*" --exclude "temp"
```

---

## See It In Action

```
🚀 Gitty Up - Scanning /Users/dev/projects...
   Found 15 git repositories

Updating repositories...
✓ project-alpha (main) - Already up to date
✓ project-beta (develop) - Fast-forward: 3 files changed
⚠ project-gamma (feature/new) - Uncommitted changes detected
✓ project-delta (main) - Already up to date
✓ project-epsilon (main) - Fast-forward: 12 files changed

Summary:
  📊 Repositories found: 15
  ✓ Successfully updated: 13
  ⚠ Skipped: 2
  ✗ Failed: 0
  ⏱ Duration: 8.3s
```

Clean, clear, and you know exactly what happened with each repository.

---

## How Gitty Up Compares

| Feature | Manual git pull | IDE "Update All" | Shell Script | **Gitty Up** |
|---------|----------------|------------------|--------------|--------------|
| **Auto-discovery** | ❌ Manual cd | ✅ If projects open | ❌ Hard-coded paths | ✅ Automatic |
| **Parallel updates** | ❌ Sequential | ⚠️ Sometimes | ⚠️ If you code it | ✅ Yes (4-8x faster) |
| **Safety checks** | ❌ Manual | ✅ Usually | ⚠️ If you code it | ✅ Automatic |
| **Works across IDEs** | ✅ Yes | ❌ IDE-specific | ✅ Yes | ✅ Yes |
| **Automation friendly** | ⚠️ Scripts needed | ❌ No | ✅ Yes | ✅ JSON output |
| **Zero configuration** | ✅ Yes | ❌ Setup needed | ❌ Write script | ✅ Yes |

**Why Gitty Up wins:** Combines the best of everything - automatic like an IDE, fast like async scripts, flexible like manual control, and safe by default.

---

## Complete Feature List

### Core Features
- ✅ **Automatic Discovery** - Recursively scans directories to find all Git repositories
- ✅ **Batch Updates** - Pulls updates from all discovered repositories in one command
- ✅ **Parallel Processing** - Updates multiple repositories concurrently for speed (configurable workers)
- ✅ **Smart Exclusions** - Automatically skips `node_modules`, `venv`, build directories, etc.
- ✅ **Safety First** - Skips repositories with uncommitted changes to prevent conflicts
- ✅ **Beautiful Output** - Color-coded terminal output that's easy to scan
- ✅ **Branch Awareness** - Shows current branch and update status for each repository

### Advanced Features
- ✅ **Multiple Strategies** - Choose between pull, fetch, or rebase
- ✅ **Stash Support** - Optionally stash uncommitted changes before pulling and restore after
- ✅ **JSON Output** - Machine-readable output format for automation and CI/CD
- ✅ **Configuration Files** - Support for `.gittyup.yaml` project-specific settings
- ✅ **Dry Run Mode** - Preview what would happen without making changes
- ✅ **Depth Control** - Limit how deep to traverse directory trees
- ✅ **Custom Exclusions** - Add your own directory patterns to skip
- ✅ **Flexible Workers** - Configure concurrency from 1 to N workers

---

## Usage Reference

```
gittyup [OPTIONS] [PATH]

Arguments:
  PATH                  Root directory to scan (default: current directory)

Options:
  -n, --dry-run        Show what would be done without making changes
  --max-depth DEPTH    Maximum directory depth to traverse
  --exclude PATTERN    Exclude directories matching pattern (can be repeated)
  --strategy {pull,fetch,rebase}
                       Update strategy (default: pull)
  --stash              Stash changes before pulling, pop after
  --workers N          Number of concurrent workers (default: 4)
  --sequential         Disable parallel processing (equivalent to --workers 1)
  --no-config          Ignore configuration files
  -w, --wordy          Increase output verbosity
  -q, --quiet          Minimize output (errors only)
  --no-color           Disable colored output
  --format {text,json} Output format (default: text)
  --version            Show version information
  -h, --help           Show this help message
```

---

## Configuration Files

Gitty Up works great with zero configuration, but power users can customize behavior with config files.

### Configuration Precedence

1. **Command-line arguments** (highest priority)
2. **Local config**: `.gittyup.yaml` in current directory
3. **User config**: `~/.config/gittyup/config.yaml`
4. **Built-in defaults** (lowest priority)

### Example Configuration

Create a `.gittyup.yaml` file in your project root:

```yaml
# Directory scanning
max_depth: 3
exclude:
  - node_modules
  - venv
  - .venv
  - build
  - dist

# Git operations
strategy: pull
pull_all_branches: true

# Performance
max_workers: 8

# Output
verbose: false
no_color: false
```

**Available Options:**
- `max_depth` - Maximum directory depth to traverse (integer or null)
- `exclude` - List of directory names to exclude
- `strategy` - Update strategy: `pull`, `fetch`, or `rebase`
- `max_workers` - Number of concurrent workers (default: 4)
- `verbose` - Enable verbose output (boolean)
- `no_color` - Disable colored output (boolean)

**Ignore config files:** Use `--no-config` flag

---

## Advanced: Stash Support

When you have repositories with uncommitted changes, Gitty Up normally skips them to protect your work. But sometimes you want to update everything anyway.

```bash
gittyup --stash
```

This automatically:
1. Stashes uncommitted changes in affected repos
2. Pulls the latest changes
3. Restores your changes by popping the stash

**Use this when:** You have work-in-progress across multiple repos and want to sync with your team before continuing.

---

## Advanced: JSON Output for Automation

Integrate Gitty Up into your automation workflows with JSON output:

```bash
gittyup --format json > results.json
```

Example output:
```json
{
  "summary": {
    "repos_found": 5,
    "repos_updated": 3,
    "repos_skipped": 1,
    "repos_failed": 1,
    "duration_seconds": 8.32
  },
  "repositories": [
    {
      "path": "/path/to/repo1",
      "state": "success",
      "branch": "main",
      "message": "Already up to date",
      "error": null,
      "has_uncommitted_changes": false,
      "commits_pulled": 0
    }
  ]
}
```

**Use cases:**
- CI/CD pipeline checks
- Monitoring dashboards
- Scheduled reports
- Custom automation scripts

---

## Smart Defaults

Gitty Up automatically skips these directories (you'll never wait for it to scan `node_modules`):

- `node_modules`
- `venv`, `.venv`, `env`, `.env`
- `.tox`
- `__pycache__`, `.pytest_cache`, `.mypy_cache`, `.ruff_cache`
- `dist`, `build`, `.eggs`
- `target` (Rust/Java)
- `vendor` (Go/PHP)

Add your own with `--exclude PATTERN` or in config files.

---

## How It Works

Gitty Up follows a simple, safe process:

1. **Load Config** - Loads configuration from files (if present) and merges with CLI arguments
2. **Scan** - Recursively traverses the specified directory tree
3. **Discover** - Identifies Git repositories by looking for `.git` directories
4. **Filter** - Applies exclusion patterns to skip unwanted directories
5. **Check** - Examines each repository for uncommitted changes
6. **Update** - Executes `git pull` (or chosen strategy) on clean repositories concurrently
7. **Report** - Displays results with colored output and summary statistics

**Safety guarantees:**
- ✅ Never modifies uncommitted changes (unless you use `--stash`)
- ✅ Automatically skips repositories with uncommitted changes
- ✅ Continues processing even if individual repositories fail
- ✅ Shows exactly what's happening with each repository

---

## Common Use Cases

### Morning Routine
```bash
# Add to your shell profile (.zshrc, .bashrc)
alias sync-all='gittyup ~/projects && echo "☕ All repos synced! Ready to code."'

# Run every morning
sync-all
```

### Pre-Standup Sync
```bash
# Quick sync before your daily standup
gittyup ~/work --workers 8
```

### Scheduled Background Updates
```bash
# Add to crontab - run every morning at 8:30 AM
30 8 * * 1-5 /usr/local/bin/gittyup ~/projects --quiet
```

### CI/CD Integration
```bash
# Check if repos are up to date in CI pipeline
gittyup --format json | jq '.summary.repos_failed' | grep -q '^0$' || exit 1
```

### Consultant Workflow
```bash
# Before starting work on any client
gittyup ~/clients/acme ~/clients/widgets ~/clients/gizmos
```

---

## Troubleshooting

### Git not found
**Problem:** `git: command not found`  
**Solution:** Ensure Git is installed and available in your PATH.

### Permission errors
**Problem:** Can't access certain directories  
**Solution:** This is normal. Gitty Up will skip them and continue. Use `--verbose` to see which directories are skipped.

### Authentication failures
**Problem:** Some repositories fail with authentication errors  
**Solution:** Ensure your Git credentials are configured (SSH keys or credential helper). Gitty Up uses your existing Git configuration.

### Repositories are skipped
**Problem:** Repos with uncommitted changes are skipped  
**Solution:** This is intentional for safety. Options:
- Commit or stash changes manually
- Use `gittyup --stash` to automatically stash and restore
- Use `--dry-run` to preview what will be skipped

### Slow performance
**Problem:** Taking a long time to update repos  
**Solution:** 
- Increase workers: `gittyup --workers 8`
- Limit depth: `gittyup --max-depth 3`
- Exclude large directories: `gittyup --exclude "archived-*"`

---

## Development

Want to contribute? Great! Here's how to get started.

### Setup Development Environment

```bash
# Clone the repository
git clone <repo-url>
cd gittyup

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-development.piptools
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific test file
pytest tests/test_scanner.py
```

**Current test coverage:** 59% overall, 70%+ for core modules

### Linting and Formatting

```bash
# Format code
ruff format .

# Check and fix linting issues
ruff check --fix .
```

### Project Structure

```
gittyup/
├── gittyup/              # Main package
│   ├── cli.py           # CLI interface
│   ├── scanner.py       # Repository discovery
│   ├── git_operations.py # Git command execution
│   ├── reporter.py      # Output formatting
│   ├── config.py        # Configuration management
│   ├── models.py        # Data structures
│   └── constants.py     # Constants and defaults
└── tests/               # Test suite
```

---

## Contributing

Contributions are welcome! Here's how you can help:

- 🐛 **Report bugs** - Open an issue with steps to reproduce
- 💡 **Suggest features** - Share your ideas for improvements
- 📖 **Improve docs** - Help make documentation clearer
- 🔧 **Submit PRs** - Fix bugs or add features

Please ensure:
- Tests pass (`pytest`)
- Code is formatted (`ruff format .`)
- Linting passes (`ruff check .`)

---

## Philosophy

Gitty Up exists because developers shouldn't waste mental energy on repository housekeeping. Your time is valuable. Your focus is precious. 

We believe:
- **Automation should be invisible** - Works perfectly without configuration
- **Speed respects your time** - Parallel processing by default
- **Safety enables confidence** - Never lose uncommitted work
- **Clarity reduces anxiety** - Always know what's happening

One command. All repositories. Fresh and ready. That's Gitty Up.

---

## License

MIT License - See LICENSE file for details

---

## Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/gittyup/issues)
- **Questions:** Open a GitHub Discussion
- **Security:** Email security concerns privately

---

**Made with ❤️ for developers who manage too many repositories**

*Star on GitHub if Gitty Up saves you time!* ⭐
