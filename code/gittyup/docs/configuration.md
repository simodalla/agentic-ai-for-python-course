# Gitty Up - Configuration Guide

This guide explains how to configure Gitty Up using YAML configuration files.

---

## Table of Contents

- [Overview](#overview)
- [Configuration Hierarchy](#configuration-hierarchy)
- [Configuration File Locations](#configuration-file-locations)
- [Configuration Options](#configuration-options)
- [Examples](#examples)
- [Command-Line Options](#command-line-options)

---

## Overview

Gitty Up can be configured using YAML files at multiple levels, allowing you to set global defaults and override them per-project or via command-line arguments.

---

## Configuration Hierarchy

Configuration is loaded and merged in the following priority order (highest to lowest):

1. **Command-line arguments** (highest priority)
2. **Local config file** (`.gittyup.yaml` in current/scanned directory)
3. **User config file** (`~/.config/gittyup/config.yaml`)
4. **System defaults** (lowest priority)

This means CLI arguments will always override file settings, and local settings override global settings.

---

## Configuration File Locations

### Local Configuration
**Path**: `.gittyup.yaml` in your project directory

Use this for project-specific settings. This file should be added to your project's `.gitignore` if the settings are personal, or committed if they're shared with the team.

**Example**:
```yaml
# .gittyup.yaml in ~/projects/my-project/
max_depth: 3
exclude_patterns:
  - old-branches
  - archive
```

### User/Global Configuration
**Path**: `~/.config/gittyup/config.yaml`

Use this for your personal default settings across all projects.

**Example**:
```yaml
# ~/.config/gittyup/config.yaml
verbose: true
skip_dirty: true
timeout_seconds: 60
```

### Specifying a Custom Config File
You can specify a custom configuration file using the `--config` option:
```bash
gittyup --config ~/my-custom-config.yaml ~/projects
```

---

## Configuration Options

### Scanning Behavior

#### `max_depth`
- **Type**: Integer
- **Default**: `10`
- **Description**: Maximum directory depth to traverse when scanning for repositories

```yaml
max_depth: 15
```

#### `exclude_patterns`
- **Type**: List of strings
- **Default**: `["node_modules", "venv", ".venv", "__pycache__", ".tox", "build", "dist"]`
- **Description**: Directory names to exclude from scanning. Your custom patterns are **added** to the defaults (not replaced)

```yaml
exclude_patterns:
  - temp
  - archive
  - old-*      # Pattern matching supported
```

**Note**: The default exclusions are always applied. Your patterns extend the list.

---

### Git Operations

#### `skip_dirty`
- **Type**: Boolean
- **Default**: `true`
- **Description**: Whether to skip repositories with uncommitted changes

```yaml
skip_dirty: true  # Skip repos with uncommitted changes (safe)
# or
skip_dirty: false  # Update even with uncommitted changes (use with caution!)
```

#### `timeout_seconds`
- **Type**: Integer
- **Default**: `30`
- **Description**: Timeout in seconds for git pull operations

```yaml
timeout_seconds: 60  # For slow networks
```

#### `parallel_operations`
- **Type**: Boolean
- **Default**: `false`
- **Description**: Whether to update repositories in parallel (experimental, Phase 3 feature)

```yaml
parallel_operations: false
```

---

### Output Options

#### `verbose`
- **Type**: Boolean
- **Default**: `false`
- **Description**: Show detailed output including debug information

```yaml
verbose: true
```

#### `quiet`
- **Type**: Boolean
- **Default**: `false`
- **Description**: Minimal output (only errors and summary)

```yaml
quiet: false
```

**Note**: `verbose` and `quiet` cannot both be `true`.

#### `show_uptodate`
- **Type**: Boolean
- **Default**: `true`
- **Description**: Whether to show repositories that are already up-to-date

```yaml
show_uptodate: true
```

---

## Examples

### Example 1: Minimal Configuration
Just the essentials for a specific project:

```yaml
# .gittyup.yaml
exclude_patterns:
  - temp
  - old-branches
skip_dirty: true
```

### Example 2: Developer-Friendly Defaults
Good defaults for most developers:

```yaml
# ~/.config/gittyup/config.yaml
max_depth: 10
skip_dirty: true
timeout_seconds: 45
verbose: false
show_uptodate: true

exclude_patterns:
  - node_modules
  - __pycache__
  - .mypy_cache
  - htmlcov
  - temp
```

### Example 3: Aggressive Update Mode
For when you want to pull everything (use with caution):

```yaml
# special-config.yaml
skip_dirty: false      # Update even with uncommitted changes
timeout_seconds: 120   # Long timeout
verbose: true          # See everything
max_depth: 20          # Deep scanning
```

Use with:
```bash
gittyup --config special-config.yaml ~/projects
```

### Example 4: Monorepo Configuration
For large monorepos with many nested projects:

```yaml
# .gittyup.yaml in monorepo root
max_depth: 5           # Don't scan too deep
skip_dirty: true
show_uptodate: false   # Only show repos that actually updated

exclude_patterns:
  - node_modules
  - target            # Rust/Java builds
  - build
  - dist
  - .venv
  - __pycache__
  - vendor            # Go dependencies
```

---

## Command-Line Options

All configuration options can be overridden via command-line arguments:

```bash
# Override max depth
gittyup --max-depth 5 ~/projects

# Add exclusions
gittyup --exclude temp --exclude archive ~/projects

# Force update (ignore dirty repos)
gittyup --no-skip-dirty ~/projects

# Verbose output
gittyup -v ~/projects

# Quiet mode
gittyup -q ~/projects

# Dry run (see what would happen)
gittyup --dry-run ~/projects

# Disable colors
gittyup --no-color ~/projects

# Disable logging
gittyup --no-log ~/projects
```

---

## Validation

Gitty Up validates your configuration and will report errors if:

- `max_depth` is not a positive integer
- `exclude_patterns` is not a list
- `timeout_seconds` is not a positive integer
- Boolean flags are not boolean values
- Both `verbose` and `quiet` are set to `true`

**Example Error**:
```
Configuration error: max_depth must be a positive integer
```

---

## Tips & Best Practices

### 1. Start Simple
Begin with a minimal configuration and add options as needed:
```yaml
# Start with just this
skip_dirty: true
```

### 2. Use Local Configs for Team Settings
Commit `.gittyup.yaml` to your repository if the settings should be shared:
```yaml
# Team-wide settings for this project
max_depth: 3
exclude_patterns:
  - archived-branches
```

### 3. Use Global Config for Personal Preferences
Keep your personal preferences in `~/.config/gittyup/config.yaml`:
```yaml
# My personal defaults
verbose: true
timeout_seconds: 60
```

### 4. Test with Dry Run
Always test new configurations with `--dry-run` first:
```bash
gittyup --dry-run ~/projects
```

### 5. Check Your Configuration
Use verbose mode to see what configuration is being used:
```bash
gittyup -v ~/projects
```

This will show which config file was loaded.

---

## Troubleshooting

### Configuration Not Loading
1. Check file location: `~/.config/gittyup/config.yaml`
2. Check YAML syntax (no tabs, proper indentation)
3. Run with `-v` to see if config file is detected

### Exclusions Not Working
- Remember: your exclusions are **added** to defaults
- Check spelling and case sensitivity
- Try `--dry-run` to see what's being scanned

### "Cannot use both verbose and quiet" Error
- Don't set both `verbose: true` and `quiet: true`
- Choose one or neither

---

## Example Configuration File

Here's a complete example with all options:

```yaml
# ~/.config/gittyup/config.yaml
# Complete configuration example

# Scanning behavior
max_depth: 10                    # Maximum directory depth
exclude_patterns:                # Additional patterns to exclude
  - node_modules                 # JavaScript
  - venv                         # Python virtual envs
  - .venv
  - __pycache__                  # Python cache
  - target                       # Rust builds
  - build                        # Build directories
  - dist
  - vendor                       # Go/PHP dependencies
  - temp                         # Temporary files
  - archive                      # Old stuff
  - "old-*"                      # Pattern: anything starting with "old-"

# Git operations
skip_dirty: true                 # Skip repos with uncommitted changes
timeout_seconds: 30              # Timeout for git operations

# Output options
verbose: false                   # Show detailed output
quiet: false                     # Minimal output
show_uptodate: true              # Show repos that are up-to-date

# Advanced options (experimental)
parallel_operations: false       # Not yet implemented in Phase 2
```

---

## Getting Help

- Run `gittyup --help` for CLI options
- Check the main README for general usage
- See the example files in the repository:
  - `.gittyup.yaml.example`
  - `docs/config-minimal.yaml`
  - `docs/config-advanced.yaml`

---

**Version**: 0.2.0 (Phase 2)  
**Last Updated**: November 1, 2025

