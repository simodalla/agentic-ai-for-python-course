# 🚀 Gitty Up - Quick Start Guide

Get up and running with Gitty Up in 2 minutes!

---

## Installation

```bash
# 1. Navigate to the gittyup directory
cd /path/to/gittyup

# 2. Install the package
pip install -e .

# 3. Verify installation
python3 -m gittyup --version
```

---

## First Run

```bash
# See what would happen (dry run)
python3 -m gittyup --dry-run ~/projects

# Actually update repositories
python3 -m gittyup ~/projects
```

---

## Common Usage

```bash
# Update current directory
python3 -m gittyup

# Update specific directory
python3 -m gittyup ~/workspace

# Exclude directories
python3 -m gittyup --exclude node_modules --exclude temp ~/projects

# Limit search depth
python3 -m gittyup --max-depth 3 ~/projects

# Force update (even with uncommitted changes) - USE WITH CAUTION!
python3 -m gittyup --no-skip-dirty ~/projects
```

---

## Example Output

```
╔═══════════════════════════════════════╗
║           🚀 Gitty Up 🚀             ║
║   Keeping Your Repos Up to Date      ║
╚═══════════════════════════════════════╝

🔍 Scanning for repositories in: /Users/you/projects
✓ Found 5 repositories

📥 Updating repositories...

✓ project-1                    Successfully updated
✓ project-2                    Already up to date
⚠ project-3                    Skipped: Uncommitted changes
✓ project-4                    Successfully updated
○ project-5                    Skipped: No upstream configured

============================================================
Summary:
  Total repositories: 5
  ✓ Updated: 3
  ○ Skipped: 2
  ⏱️  Time elapsed: 4.23s
============================================================
```

---

## Tips

### 🛡️ Safety Features
- By default, repos with uncommitted changes are **skipped**
- Repos without upstream branches are **skipped**
- Use `--dry-run` to preview before making changes

### ⚡ Performance
- Automatically excludes common directories (node_modules, venv, etc.)
- Use `--max-depth` for faster scanning of deep directory trees

### 🎨 Output
- Green ✓ = Success
- Yellow ⚠ = Warning/Skipped
- Red ✗ = Error

---

## Troubleshooting

### "Git not found"
```bash
# Install Git first
# macOS: brew install git
# Linux: sudo apt install git
# Windows: Download from git-scm.com
```

### No repositories found
```bash
# Make sure you're in the right directory
# Check that your projects have .git directories
ls -la ~/projects/*/.git
```

### Permission denied
```bash
# Fix permissions
chmod -R u+r ~/projects
```

---

## Get Help

```bash
# Show all options
python3 -m gittyup --help

# Read full documentation
cat readme.md
```

---

## Next Steps

1. **Try it out** on your projects directory
2. **Read the full README** for advanced features
3. **Report issues** if you find any bugs
4. **Star the repo** if you find it useful!

---

**Happy coding! 🚀**

