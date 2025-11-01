"""
Tests for the repository scanner module.
"""

import pytest
import tempfile
from pathlib import Path
from gittyup.scanner import RepositoryScanner
from gittyup.exceptions import ScanError


class TestRepositoryScanner:
    """Test suite for RepositoryScanner class."""

    def test_init_default_excludes(self):
        """Test that default exclude patterns are set."""
        scanner = RepositoryScanner(root_path=".")
        assert "node_modules" in scanner.exclude_patterns
        assert "venv" in scanner.exclude_patterns
        assert "__pycache__" in scanner.exclude_patterns

    def test_init_custom_excludes(self):
        """Test that custom exclude patterns are added."""
        scanner = RepositoryScanner(
            root_path=".", exclude_patterns=["custom1", "custom2"]
        )
        assert "custom1" in scanner.exclude_patterns
        assert "custom2" in scanner.exclude_patterns
        # Default excludes should still be present
        assert "node_modules" in scanner.exclude_patterns

    def test_scan_nonexistent_path(self):
        """Test that scanning a nonexistent path raises ScanError."""
        scanner = RepositoryScanner(root_path="/nonexistent/path/12345")
        with pytest.raises(ScanError, match="Path does not exist"):
            scanner.scan()

    def test_scan_file_not_directory(self, tmp_path):
        """Test that scanning a file raises ScanError."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")
        
        scanner = RepositoryScanner(root_path=str(test_file))
        with pytest.raises(ScanError, match="not a directory"):
            scanner.scan()

    def test_scan_empty_directory(self, tmp_path):
        """Test scanning an empty directory."""
        scanner = RepositoryScanner(root_path=str(tmp_path))
        repos = scanner.scan()
        assert repos == []

    def test_scan_single_git_repo(self, tmp_path):
        """Test scanning a directory with a single Git repository."""
        # Create a fake .git directory
        git_dir = tmp_path / ".git"
        git_dir.mkdir()
        
        scanner = RepositoryScanner(root_path=str(tmp_path))
        repos = scanner.scan()
        
        assert len(repos) == 1
        assert repos[0] == tmp_path

    def test_scan_nested_repos(self, tmp_path):
        """Test scanning nested repositories."""
        # Create nested structure: root/project1/.git and root/project2/.git
        project1 = tmp_path / "project1"
        project1.mkdir()
        (project1 / ".git").mkdir()
        
        project2 = tmp_path / "project2"
        project2.mkdir()
        (project2 / ".git").mkdir()
        
        scanner = RepositoryScanner(root_path=str(tmp_path))
        repos = scanner.scan()
        
        assert len(repos) == 2
        assert project1 in repos
        assert project2 in repos

    def test_scan_excludes_patterns(self, tmp_path):
        """Test that excluded patterns are not scanned."""
        # Create structure with node_modules
        node_modules = tmp_path / "node_modules" / "package"
        node_modules.mkdir(parents=True)
        (node_modules / ".git").mkdir()
        
        # Create a normal repo
        project = tmp_path / "project"
        project.mkdir()
        (project / ".git").mkdir()
        
        scanner = RepositoryScanner(root_path=str(tmp_path))
        repos = scanner.scan()
        
        # Should only find project, not node_modules
        assert len(repos) == 1
        assert project in repos
        assert node_modules not in repos

    def test_scan_excludes_hidden_dirs(self, tmp_path):
        """Test that hidden directories (starting with .) are excluded."""
        # Create hidden directory with git repo
        hidden_dir = tmp_path / ".hidden" / "repo"
        hidden_dir.mkdir(parents=True)
        (hidden_dir / ".git").mkdir()
        
        # Create a normal repo
        project = tmp_path / "project"
        project.mkdir()
        (project / ".git").mkdir()
        
        scanner = RepositoryScanner(root_path=str(tmp_path))
        repos = scanner.scan()
        
        # Should only find project, not hidden directory
        assert len(repos) == 1
        assert project in repos

    def test_scan_respects_max_depth(self, tmp_path):
        """Test that max_depth is respected."""
        # Create deep nested structure
        deep = tmp_path / "level1" / "level2" / "level3"
        deep.mkdir(parents=True)
        (deep / ".git").mkdir()
        
        # Scanner with max_depth=2 should not find the repo
        scanner = RepositoryScanner(root_path=str(tmp_path), max_depth=2)
        repos = scanner.scan()
        assert len(repos) == 0
        
        # Scanner with max_depth=3 should find it
        scanner = RepositoryScanner(root_path=str(tmp_path), max_depth=3)
        repos = scanner.scan()
        assert len(repos) == 1

    def test_is_git_repository(self, tmp_path):
        """Test is_git_repository method."""
        # Create a git repo
        git_dir = tmp_path / ".git"
        git_dir.mkdir()
        
        scanner = RepositoryScanner(root_path=str(tmp_path))
        assert scanner.is_git_repository(tmp_path) is True
        
        # Test non-git directory
        non_git = tmp_path / "not-a-repo"
        non_git.mkdir()
        assert scanner.is_git_repository(non_git) is False

    def test_scan_doesnt_descend_into_git_repos(self, tmp_path):
        """Test that scanner doesn't descend into .git directories."""
        # Create repo with nested structure inside .git
        git_dir = tmp_path / ".git" / "nested" / "deep"
        git_dir.mkdir(parents=True)
        (git_dir / ".git").mkdir()  # This should not be found
        
        scanner = RepositoryScanner(root_path=str(tmp_path))
        repos = scanner.scan()
        
        # Should only find the top-level repo
        assert len(repos) == 1
        assert repos[0] == tmp_path

    def test_scan_returns_sorted_list(self, tmp_path):
        """Test that scan returns a sorted list of repositories."""
        # Create repos in non-alphabetical order
        (tmp_path / "zebra").mkdir()
        (tmp_path / "zebra" / ".git").mkdir()
        
        (tmp_path / "alpha").mkdir()
        (tmp_path / "alpha" / ".git").mkdir()
        
        (tmp_path / "beta").mkdir()
        (tmp_path / "beta" / ".git").mkdir()
        
        scanner = RepositoryScanner(root_path=str(tmp_path))
        repos = scanner.scan()
        
        # Check that results are sorted
        assert len(repos) == 3
        assert repos[0].name == "alpha"
        assert repos[1].name == "beta"
        assert repos[2].name == "zebra"

