"""
Tests for the configuration module.
"""

import pytest
import tempfile
from pathlib import Path
import yaml
from gittyup.config import Config, ConfigError


class TestConfig:
    """Test suite for Config class."""

    def test_init_defaults(self):
        """Test that configuration initializes with default values."""
        config = Config()
        assert config.get("max_depth") == 10
        assert config.get("skip_dirty") is True
        assert config.get("timeout_seconds") == 30
        assert config.get("verbose") is False
        assert config.get("quiet") is False
        assert "node_modules" in config.get("exclude_patterns")
        assert "venv" in config.get("exclude_patterns")

    def test_get_existing_key(self):
        """Test getting an existing configuration key."""
        config = Config()
        assert config.get("max_depth") == 10

    def test_get_nonexistent_key(self):
        """Test getting a non-existent key returns None."""
        config = Config()
        assert config.get("nonexistent") is None

    def test_get_with_default(self):
        """Test getting a non-existent key with a default value."""
        config = Config()
        assert config.get("nonexistent", "default") == "default"

    def test_set_value(self):
        """Test setting a configuration value."""
        config = Config()
        config.set("custom_key", "custom_value")
        assert config.get("custom_key") == "custom_value"

    def test_load_from_nonexistent_file(self):
        """Test loading from a non-existent file does nothing."""
        config = Config()
        config.load_from_file(Path("/nonexistent/config.yaml"))
        # Should not raise an error, just skip

    def test_load_from_valid_yaml_file(self, tmp_path):
        """Test loading configuration from a valid YAML file."""
        config_file = tmp_path / "config.yaml"
        config_data = {
            "max_depth": 5,
            "verbose": True,
            "exclude_patterns": ["custom1", "custom2"],
        }
        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        config = Config()
        config.load_from_file(config_file)

        assert config.get("max_depth") == 5
        assert config.get("verbose") is True
        # Should have merged with defaults
        assert "custom1" in config.get("exclude_patterns")
        assert "node_modules" in config.get("exclude_patterns")

    def test_load_from_invalid_yaml_file(self, tmp_path):
        """Test loading from an invalid YAML file raises ConfigError."""
        config_file = tmp_path / "invalid.yaml"
        with open(config_file, "w") as f:
            f.write("{ invalid yaml content [")

        config = Config()
        with pytest.raises(ConfigError, match="Error parsing YAML"):
            config.load_from_file(config_file)

    def test_load_from_non_dict_yaml(self, tmp_path):
        """Test loading from a YAML file that's not a dictionary."""
        config_file = tmp_path / "list.yaml"
        with open(config_file, "w") as f:
            yaml.dump([1, 2, 3], f)

        config = Config()
        with pytest.raises(ConfigError, match="Must be a YAML dictionary"):
            config.load_from_file(config_file)

    def test_load_from_empty_yaml(self, tmp_path):
        """Test loading from an empty YAML file."""
        config_file = tmp_path / "empty.yaml"
        config_file.touch()

        config = Config()
        config.load_from_file(config_file)
        # Should still have defaults
        assert config.get("max_depth") == 10

    def test_merge_cli_args(self):
        """Test merging CLI arguments into configuration."""
        config = Config()
        config.merge_cli_args(max_depth=15, verbose=True, custom="value")

        assert config.get("max_depth") == 15
        assert config.get("verbose") is True
        assert config.get("custom") == "value"

    def test_merge_cli_args_excludes_none(self):
        """Test that None values from CLI args are excluded."""
        config = Config()
        original_depth = config.get("max_depth")
        config.merge_cli_args(max_depth=None, verbose=True)

        assert config.get("max_depth") == original_depth  # Unchanged
        assert config.get("verbose") is True

    def test_merge_exclude_patterns(self):
        """Test that exclude patterns are extended, not replaced."""
        config = Config()
        original_patterns = config.get("exclude_patterns").copy()

        config.merge_cli_args(exclude_patterns=["custom1", "custom2"])

        # Should contain both original and new patterns
        patterns = config.get("exclude_patterns")
        for pattern in original_patterns:
            assert pattern in patterns
        assert "custom1" in patterns
        assert "custom2" in patterns

    def test_merge_exclude_patterns_no_duplicates(self):
        """Test that merging exclude patterns doesn't create duplicates."""
        config = Config()
        config.merge_cli_args(exclude_patterns=["node_modules", "custom"])

        patterns = config.get("exclude_patterns")
        assert patterns.count("node_modules") == 1
        assert "custom" in patterns

    def test_to_dict(self):
        """Test converting configuration to dictionary."""
        config = Config()
        config.set("custom", "value")
        config_dict = config.to_dict()

        assert isinstance(config_dict, dict)
        assert config_dict["max_depth"] == 10
        assert config_dict["custom"] == "value"

    def test_to_dict_returns_copy(self):
        """Test that to_dict returns a copy, not a reference."""
        config = Config()
        config_dict = config.to_dict()
        config_dict["max_depth"] = 999

        # Original should be unchanged
        assert config.get("max_depth") == 10

    def test_validate_valid_config(self):
        """Test validation passes for valid configuration."""
        config = Config()
        # Should not raise an exception
        config.validate()

    def test_validate_invalid_max_depth(self):
        """Test validation fails for invalid max_depth."""
        config = Config()
        config.set("max_depth", -1)
        with pytest.raises(ConfigError, match="max_depth must be a positive integer"):
            config.validate()

        config.set("max_depth", "not a number")
        with pytest.raises(ConfigError, match="max_depth must be a positive integer"):
            config.validate()

    def test_validate_invalid_exclude_patterns(self):
        """Test validation fails for invalid exclude_patterns."""
        config = Config()
        config.set("exclude_patterns", "not a list")
        with pytest.raises(ConfigError, match="exclude_patterns must be a list"):
            config.validate()

    def test_validate_invalid_timeout(self):
        """Test validation fails for invalid timeout_seconds."""
        config = Config()
        config.set("timeout_seconds", -5)
        with pytest.raises(ConfigError, match="timeout_seconds must be a positive integer"):
            config.validate()

    def test_validate_invalid_boolean_flag(self):
        """Test validation fails for invalid boolean flags."""
        config = Config()
        config.set("verbose", "not a boolean")
        with pytest.raises(ConfigError, match="verbose must be a boolean"):
            config.validate()

    def test_validate_verbose_and_quiet_conflict(self):
        """Test validation fails when both verbose and quiet are True."""
        config = Config()
        config.set("verbose", True)
        config.set("quiet", True)
        with pytest.raises(ConfigError, match="Cannot use both verbose and quiet"):
            config.validate()

    def test_load_all_configs_no_files(self, tmp_path):
        """Test load_all_configs when no config files exist."""
        config = Config()
        config.load_all_configs(working_dir=tmp_path)
        # Should still have defaults
        assert config.get("max_depth") == 10

    def test_load_all_configs_with_local(self, tmp_path):
        """Test load_all_configs loads local config file."""
        local_config = tmp_path / ".gittyup.yaml"
        with open(local_config, "w") as f:
            yaml.dump({"max_depth": 20}, f)

        config = Config()
        config.load_all_configs(working_dir=tmp_path)
        assert config.get("max_depth") == 20

    def test_priority_order(self, tmp_path):
        """Test that CLI args override file configs."""
        # Create a config file
        config_file = tmp_path / ".gittyup.yaml"
        with open(config_file, "w") as f:
            yaml.dump({"max_depth": 20, "verbose": True}, f)

        config = Config()
        config.load_from_file(config_file)
        assert config.get("max_depth") == 20

        # CLI args should override
        config.merge_cli_args(max_depth=30)
        assert config.get("max_depth") == 30
        assert config.get("verbose") is True  # Unchanged

    def test_user_config_path(self):
        """Test getting user config path."""
        config = Config()
        user_path = config._get_user_config_path()
        assert isinstance(user_path, Path)
        assert "gittyup" in str(user_path)
        assert "config.yaml" in str(user_path)

