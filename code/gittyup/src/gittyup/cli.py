"""
Command-line interface for Gitty Up.

This module provides the main CLI entry point and command handling.
"""

import time
from pathlib import Path
import click
from .scanner import RepositoryScanner
from .git_operations import GitOperations
from .output import OutputFormatter
from .exceptions import GittyUpError, GitNotFoundError, ScanError


@click.command()
@click.argument(
    "path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    default=".",
    required=False,
)
@click.option(
    "--max-depth",
    type=int,
    default=10,
    help="Maximum directory depth to traverse",
    show_default=True,
)
@click.option(
    "--exclude",
    multiple=True,
    help="Directory patterns to exclude (can be used multiple times)",
)
@click.option(
    "--skip-dirty",
    is_flag=True,
    default=True,
    help="Skip repositories with uncommitted changes (default)",
)
@click.option(
    "--no-skip-dirty",
    is_flag=True,
    help="Update even if there are uncommitted changes",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would happen without making changes",
)
@click.version_option(version="0.1.0", prog_name="gittyup")
def main(
    path: str,
    max_depth: int,
    exclude: tuple,
    skip_dirty: bool,
    no_skip_dirty: bool,
    dry_run: bool,
) -> None:
    """
    Gitty Up - Update all Git repositories in a directory tree.

    Scans PATH (default: current directory) for Git repositories and
    pulls changes from their remote repositories.

    Examples:

    \b
        gittyup                    # Update repos in current directory
        gittyup ~/projects         # Update repos in ~/projects
        gittyup --dry-run          # See what would happen
        gittyup --exclude venv     # Exclude specific directories
    """
    # Handle skip_dirty flag
    if no_skip_dirty:
        skip_dirty = False

    # Start timer
    start_time = time.time()

    # Print banner
    OutputFormatter.print_banner()

    # Check if Git is available
    try:
        GitOperations.ensure_git_available()
    except GitNotFoundError as e:
        OutputFormatter.print_error_message(str(e))
        raise SystemExit(1)

    # Scan for repositories
    OutputFormatter.print_scanning(path)
    
    try:
        scanner = RepositoryScanner(
            root_path=path,
            max_depth=max_depth,
            exclude_patterns=list(exclude) if exclude else None,
        )
        repositories = scanner.scan()
    except ScanError as e:
        OutputFormatter.print_error_message(f"Scanning error: {e}")
        raise SystemExit(1)

    OutputFormatter.print_found_repos(len(repositories))

    if len(repositories) == 0:
        return

    # Update repositories
    if dry_run:
        OutputFormatter.print_info("DRY RUN MODE - No changes will be made")
    
    OutputFormatter.print_updating()

    # Counters for summary
    updated_count = 0
    skipped_count = 0
    error_count = 0

    for repo in repositories:
        repo_name = repo.name

        # Check repository status if skip_dirty is enabled
        if skip_dirty:
            is_clean, status_msg = GitOperations.get_repository_status(repo)
            if not is_clean:
                OutputFormatter.print_skipped(repo, status_msg)
                skipped_count += 1
                continue

        # Check if repository has upstream
        if not GitOperations.has_upstream(repo):
            OutputFormatter.print_skipped(repo, "No upstream configured")
            skipped_count += 1
            continue

        # Pull changes (or simulate in dry-run mode)
        if dry_run:
            OutputFormatter.print_info(f"Would pull {repo_name}")
            continue

        success, message = GitOperations.pull_repository(repo)

        if success:
            if "Already up to date" in message:
                OutputFormatter.print_success(repo, message)
            else:
                OutputFormatter.print_success(repo, message)
            updated_count += 1
        else:
            OutputFormatter.print_error(repo, message)
            error_count += 1

    # Calculate elapsed time
    elapsed_time = time.time() - start_time

    # Print summary
    if not dry_run:
        OutputFormatter.print_summary(
            total=len(repositories),
            updated=updated_count,
            skipped=skipped_count,
            errors=error_count,
            elapsed_time=elapsed_time,
        )

    # Exit with error code if there were errors
    if error_count > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

