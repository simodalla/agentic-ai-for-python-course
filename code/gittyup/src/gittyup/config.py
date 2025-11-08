"""
Configuration management for Gitty Up.

Handles loading and merging configuration from multiple sources:
1. Command-line arguments (highest priority)
2. Local config file (.gittyup.yaml in current directory)
3. User config file (~/.config/gittyup/config.yaml)
4. System defaults (lowest priority)
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional
import yaml
from .exceptions import GittyUpError


class ConfigError(GittyUpError):
    """Raised when there's an error with configuration."""

    pass


class Config:
    """Configuration manager for Gitty Up."""

    # Default configuration values
    DEFAULTS: Dict[str, Any] = {
        "max_depth": 10,
        "exclude_patterns": [
            "node_modules",
            "venv",
            ".venv",
            "__pycache__",
            ".tox",
            "build",
            "dist",
        ],
        "skip_dirty": True,
        "timeout_seconds": 30,
        "verbose": False,
        "quiet": False,
        "show_uptodate": True,
        "parallel_operations": False,
    }

    def __init__(self) -> None:
        """Initialize configuration with defaults."""
        self.config: Dict[str, Any] = self.DEFAULTS.copy()

    def load_from_file(self, config_path: Path) -> None:
        """
        Load configuration from a YAML file.

        Args:
            config_path: Path to the YAML configuration file

        Raises:
            ConfigError: If the file cannot be loaded or is invalid
        """
        if not config_path.exists():
            return

        try:
            with open(config_path, "r") as f:
                file_config = yaml.safe_load(f)

            if file_config is None:
                return

            if not isinstance(file_config, dict):
                raise ConfigError(
                    f"Invalid configuration file: {config_path}. Must be a YAML dictionary."
                )

            # Merge file config into current config
            self._merge_config(file_config)

        except yaml.YAMLError as e:
            raise ConfigError(f"Error parsing YAML file {config_path}: {e}")
        except IOError as e:
            raise ConfigError(f"Error reading configuration file {config_path}: {e}")

    def load_all_configs(self, working_dir: Optional[Path] = None) -> None:
        """
        Load configuration from all sources in priority order.

        Priority (highest to lowest):
        1. Local config file (.gittyup.yaml in working directory)
        2. User config file (~/.config/gittyup/config.yaml)
        3. Defaults (already loaded)

        Args:
            working_dir: Working directory to search for local config.
                        If None, uses current directory.
        """
        # Load user config first (lower priority)
        user_config_path = self._get_user_config_path()
        if user_config_path.exists():
            self.load_from_file(user_config_path)

        # Load local config second (higher priority, will override user config)
        if working_dir is None:
            working_dir = Path.cwd()
        local_config_path = working_dir / ".gittyup.yaml"
        if local_config_path.exists():
            self.load_from_file(local_config_path)

    def merge_cli_args(self, **kwargs: Any) -> None:
        """
        Merge command-line arguments into configuration.

        CLI arguments have the highest priority and will override
        any values from config files.

        Args:
            **kwargs: Command-line arguments to merge
        """
        # Remove None values (arguments that weren't specified)
        cli_config = {k: v for k, v in kwargs.items() if v is not None}
        self._merge_config(cli_config)

    def _merge_config(self, new_config: Dict[str, Any]) -> None:
        """
        Merge new configuration values into existing configuration.

        Special handling for lists (like exclude_patterns): extends rather than replaces.

        Args:
            new_config: Dictionary of new configuration values
        """
        for key, value in new_config.items():
            if key in self.config:
                # Special handling for exclude_patterns: extend the list
                if key == "exclude_patterns" and isinstance(value, list):
                    if isinstance(self.config[key], list):
                        # Extend existing list with new patterns (avoid duplicates)
                        existing = set(self.config[key])
                        new_patterns = [p for p in value if p not in existing]
                        self.config[key].extend(new_patterns)
                    else:
                        self.config[key] = value
                else:
                    # For other keys, replace the value
                    self.config[key] = value
            else:
                # New key, just add it
                self.config[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.

        Args:
            key: Configuration key
            default: Default value if key doesn't exist

        Returns:
            Configuration value or default
        """
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.

        Args:
            key: Configuration key
            value: Value to set
        """
        self.config[key] = value

    def _get_user_config_path(self) -> Path:
        """
        Get the path to the user configuration file.

        Returns:
            Path to user config file (~/.config/gittyup/config.yaml)
        """
        # Check for XDG_CONFIG_HOME first (Linux standard)
        config_home = os.environ.get("XDG_CONFIG_HOME")
        if config_home:
            config_dir = Path(config_home) / "gittyup"
        else:
            # Fall back to ~/.config
            home = Path.home()
            config_dir = home / ".config" / "gittyup"

        return config_dir / "config.yaml"

    def to_dict(self) -> Dict[str, Any]:
        """
        Get all configuration as a dictionary.

        Returns:
            Dictionary of all configuration values
        """
        return self.config.copy()

    def validate(self) -> None:
        """
        Validate configuration values.

        Raises:
            ConfigError: If any configuration value is invalid
        """
        # Validate max_depth
        if not isinstance(self.config["max_depth"], int) or self.config["max_depth"] < 1:
            raise ConfigError("max_depth must be a positive integer")

        # Validate exclude_patterns
        if not isinstance(self.config["exclude_patterns"], list):
            raise ConfigError("exclude_patterns must be a list")

        # Validate timeout_seconds
        if (
            not isinstance(self.config["timeout_seconds"], int)
            or self.config["timeout_seconds"] < 1
        ):
            raise ConfigError("timeout_seconds must be a positive integer")

        # Validate boolean flags
        for key in ["skip_dirty", "verbose", "quiet", "show_uptodate", "parallel_operations"]:
            if key in self.config and not isinstance(self.config[key], bool):
                raise ConfigError(f"{key} must be a boolean")

        # Validate that verbose and quiet are not both True
        if self.config.get("verbose") and self.config.get("quiet"):
            raise ConfigError("Cannot use both verbose and quiet modes simultaneously")
