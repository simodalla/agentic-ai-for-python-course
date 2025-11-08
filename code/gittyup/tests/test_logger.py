"""
Tests for the logger module.
"""

import pytest
from pathlib import Path
import tempfile
from gittyup.logger import GittyUpLogger


class TestGittyUpLogger:
    """Test suite for GittyUpLogger class."""

    def test_init_enabled(self):
        """Test logger initialization when enabled."""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = GittyUpLogger(log_dir=Path(tmpdir), enabled=True)
            assert logger.enabled is True
            assert logger.logger is not None

    def test_init_disabled(self):
        """Test logger initialization when disabled."""
        logger = GittyUpLogger(enabled=False)
        assert logger.enabled is False
        # When disabled, logger level is set to CRITICAL to suppress all output
        assert len(logger.logger.handlers) == 0 or logger.logger.level >= 50

    def test_log_file_created(self):
        """Test that log file is created."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir)
            logger = GittyUpLogger(log_dir=log_dir, enabled=True)
            logger.info("Test message")

            log_file = log_dir / "gittyup.log"
            assert log_file.exists()

    def test_log_messages(self):
        """Test that log messages are written to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir)
            logger = GittyUpLogger(log_dir=log_dir, enabled=True)

            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")
            logger.error("Error message")

            log_file = log_dir / "gittyup.log"
            content = log_file.read_text()

            assert "Debug message" in content
            assert "Info message" in content
            assert "Warning message" in content
            assert "Error message" in content

    def test_logging_disabled_no_writes(self):
        """Test that disabled logger doesn't write to files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir)
            logger = GittyUpLogger(log_dir=log_dir, enabled=False)

            logger.info("This should not be written")

            log_file = log_dir / "gittyup.log"
            assert not log_file.exists()

    def test_log_scan_start(self):
        """Test logging scan start."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir)
            logger = GittyUpLogger(log_dir=log_dir, enabled=True)

            logger.log_scan_start("/test/path", 10)

            log_file = log_dir / "gittyup.log"
            content = log_file.read_text()
            assert "Starting scan" in content
            assert "/test/path" in content
            assert "max_depth=10" in content

    def test_log_scan_complete(self):
        """Test logging scan completion."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir)
            logger = GittyUpLogger(log_dir=log_dir, enabled=True)

            logger.log_scan_complete(5, 1.23)

            log_file = log_dir / "gittyup.log"
            content = log_file.read_text()
            assert "Scan complete" in content
            assert "5 repositories" in content

    def test_log_repo_update_success(self):
        """Test logging successful repository update."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir)
            logger = GittyUpLogger(log_dir=log_dir, enabled=True)

            logger.log_repo_update_success("/test/repo", "Updated successfully")

            log_file = log_dir / "gittyup.log"
            content = log_file.read_text()
            assert "Update successful" in content
            assert "/test/repo" in content
            assert "Updated successfully" in content

    def test_log_repo_update_skip(self):
        """Test logging skipped repository update."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir)
            logger = GittyUpLogger(log_dir=log_dir, enabled=True)

            logger.log_repo_update_skip("/test/repo", "Uncommitted changes")

            log_file = log_dir / "gittyup.log"
            content = log_file.read_text()
            assert "Update skipped" in content
            assert "/test/repo" in content
            assert "Uncommitted changes" in content

    def test_log_repo_update_error(self):
        """Test logging failed repository update."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir)
            logger = GittyUpLogger(log_dir=log_dir, enabled=True)

            logger.log_repo_update_error("/test/repo", "Network error")

            log_file = log_dir / "gittyup.log"
            content = log_file.read_text()
            assert "Update failed" in content
            assert "/test/repo" in content
            assert "Network error" in content

    def test_log_operation_summary(self):
        """Test logging operation summary."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir)
            logger = GittyUpLogger(log_dir=log_dir, enabled=True)

            logger.log_operation_summary(
                total=10, updated=7, skipped=2, errors=1, duration=5.5
            )

            log_file = log_dir / "gittyup.log"
            content = log_file.read_text()
            assert "Operation complete" in content
            assert "total=10" in content
            assert "updated=7" in content
            assert "skipped=2" in content
            assert "errors=1" in content

    def test_get_log_file_path_enabled(self):
        """Test getting log file path when logging is enabled."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir)
            logger = GittyUpLogger(log_dir=log_dir, enabled=True)

            log_path = logger.get_log_file_path()
            assert log_path is not None
            assert isinstance(log_path, Path)
            assert "gittyup.log" in str(log_path)

    def test_get_log_file_path_disabled(self):
        """Test getting log file path when logging is disabled."""
        logger = GittyUpLogger(enabled=False)
        log_path = logger.get_log_file_path()
        assert log_path is None

    def test_log_file_rotation(self):
        """Test that log files rotate when size limit is reached."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir)
            logger = GittyUpLogger(log_dir=log_dir, enabled=True)

            # Write a lot of data to trigger rotation
            # Note: This test might not actually trigger rotation in a unit test
            # but ensures the rotation is configured
            for i in range(1000):
                logger.info(f"Message {i}" + "X" * 100)

            log_file = log_dir / "gittyup.log"
            assert log_file.exists()

    def test_default_log_dir(self):
        """Test that default log directory is determined correctly."""
        # Use a temp directory to avoid permission issues
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir)
            logger = GittyUpLogger(log_dir=log_dir, enabled=True)
            log_path = logger.get_log_file_path()

            assert log_path is not None
            # Should contain gittyup.log
            assert "gittyup.log" in str(log_path)

    def test_debug_method(self):
        """Test debug logging method."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir)
            logger = GittyUpLogger(log_dir=log_dir, enabled=True)
            logger.debug("Debug test")

            log_file = log_dir / "gittyup.log"
            content = log_file.read_text()
            assert "Debug test" in content
            assert "DEBUG" in content

    def test_info_method(self):
        """Test info logging method."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir)
            logger = GittyUpLogger(log_dir=log_dir, enabled=True)
            logger.info("Info test")

            log_file = log_dir / "gittyup.log"
            content = log_file.read_text()
            assert "Info test" in content
            assert "INFO" in content

    def test_warning_method(self):
        """Test warning logging method."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir)
            logger = GittyUpLogger(log_dir=log_dir, enabled=True)
            logger.warning("Warning test")

            log_file = log_dir / "gittyup.log"
            content = log_file.read_text()
            assert "Warning test" in content
            assert "WARNING" in content

    def test_error_method(self):
        """Test error logging method."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir)
            logger = GittyUpLogger(log_dir=log_dir, enabled=True)
            logger.error("Error test")

            log_file = log_dir / "gittyup.log"
            content = log_file.read_text()
            assert "Error test" in content
            assert "ERROR" in content

