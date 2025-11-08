"""
Command-line interface for Gitty Up.

This module provides the main CLI entry point and command handling.
"""

import time
from pathlib import Path
from typing import Optional
import click
from .scanner import RepositoryScanner
from .git_operations import GitOperations
from .output import OutputFormatter
from .output_rich import RichOutputFormatter
from .config import Config, ConfigError
from .logger import GittyUpLogger
from .exceptions import GitNotFoundError, ScanError


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
    help="Maximum directory depth to traverse",
)
@click.option(
    "--exclude",
    multiple=True,
    help="Directory patterns to exclude (can be used multiple times)",
)
@click.option(
    "--skip-dirty/--no-skip-dirty",
    default=None,
    help="Skip repositories with uncommitted changes",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would happen without making changes",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Show detailed output",
)
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    help="Minimal output (errors and summary only)",
)
@click.option(
    "--no-color",
    is_flag=True,
    help="Disable colored output",
)
@click.option(
    "--config",
    type=click.Path(exists=True, dir_okay=False),
    help="Path to configuration file",
)
@click.option(
    "--no-log",
    is_flag=True,
    help="Disable file logging",
)
@click.version_option(version="0.2.0", prog_name="gittyup")
def main(
    path: str,
    max_depth: Optional[int],
    exclude: tuple,
    skip_dirty: Optional[bool],
    dry_run: bool,
    verbose: bool,
    quiet: bool,
    no_color: bool,
    config: Optional[str],
    no_log: bool,
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
        gittyup -v                 # Verbose output
        gittyup -q                 # Quiet mode
    """
    # Validate incompatible options
    if verbose and quiet:
        click.echo("Error: Cannot use both --verbose and --quiet simultaneously")
        raise SystemExit(1)

    # Initialize configuration
    cfg = Config()

    try:
        # Load config from files (if not disabled)
        if config:
            # Load specific config file
            cfg.load_from_file(Path(config))
        else:
            # Load from default locations
            cfg.load_all_configs(working_dir=Path(path))

        # Merge CLI arguments (highest priority)
        cli_args = {
            "max_depth": max_depth,
            "exclude_patterns": list(exclude) if exclude else None,
            "skip_dirty": skip_dirty,
            "verbose": verbose,
            "quiet": quiet,
        }
        cfg.merge_cli_args(**cli_args)

        # Validate configuration
        cfg.validate()

    except ConfigError as e:
        click.echo(f"Configuration error: {e}")
        raise SystemExit(1)

    # Initialize logger
    logger = GittyUpLogger(enabled=not no_log)
    logger.info("Starting Gitty Up v0.2.0")
    logger.info(f"Scanning path: {path}")

    # Initialize output formatter
    if no_color or cfg.get("quiet"):
        # Use basic output formatter for no-color mode
        output = OutputFormatter()
        use_rich = False
    else:
        # Use Rich output formatter for enhanced experience
        try:
            output = RichOutputFormatter(
                verbose=cfg.get("verbose", False),
                quiet=cfg.get("quiet", False),
            )
            use_rich = True
        except Exception:
            # Fallback to basic formatter if Rich fails
            output = OutputFormatter()
            use_rich = False

    # Start timer
    start_time = time.time()

    # Print banner
    output.print_banner()

    # Show configuration info in verbose mode
    if cfg.get("verbose") and use_rich:
        if config:
            output.print_config_info(Path(config))
        log_path = logger.get_log_file_path()
        if log_path:
            output.print_log_info(log_path)

    # Check if Git is available
    try:
        GitOperations.ensure_git_available()
        logger.info("Git is available")
    except GitNotFoundError as e:
        error_msg = str(e)
        output.print_error_message(error_msg)
        logger.error(f"Git not available: {error_msg}")
        raise SystemExit(1)

    # Scan for repositories
    output.print_scanning(path)
    logger.log_scan_start(path, cfg.get("max_depth"))

    try:
        scanner = RepositoryScanner(
            root_path=path,
            max_depth=cfg.get("max_depth"),
            exclude_patterns=cfg.get("exclude_patterns"),
        )
        repositories = scanner.scan()
        scan_duration = time.time() - start_time
        logger.log_scan_complete(len(repositories), scan_duration)

    except ScanError as e:
        error_msg = f"Scanning error: {e}"
        output.print_error_message(error_msg)
        logger.error(error_msg)
        raise SystemExit(1)

    output.print_found_repos(len(repositories))

    if len(repositories) == 0:
        logger.info("No repositories found, exiting")
        return

    # Update repositories
    if dry_run:
        output.print_info("DRY RUN MODE - No changes will be made")
        logger.info("Running in dry-run mode")

    output.print_updating()

    # Counters for summary
    updated_count = 0
    skipped_count = 0
    error_count = 0

    # Get configuration values
    skip_dirty_repos = cfg.get("skip_dirty", True)
    timeout = cfg.get("timeout_seconds", 30)
    show_uptodate = cfg.get("show_uptodate", True)

    for repo in repositories:
        repo_name = repo.name
        logger.log_repo_update_start(str(repo))

        # Check repository status if skip_dirty is enabled
        if skip_dirty_repos and not dry_run:
            is_clean, status_msg = GitOperations.get_repository_status(repo)
            if not is_clean:
                output.print_skipped(repo, status_msg)
                logger.log_repo_update_skip(str(repo), status_msg)
                skipped_count += 1
                continue

        # Check if repository has upstream
        if not GitOperations.has_upstream(repo):
            reason = "No upstream configured"
            output.print_skipped(repo, reason)
            logger.log_repo_update_skip(str(repo), reason)
            skipped_count += 1
            continue

        # Pull changes (or simulate in dry-run mode)
        if dry_run:
            if cfg.get("verbose"):
                output.print_info(f"Would pull {repo_name}")
            logger.debug(f"Dry-run: would pull {repo_name}")
            continue

        success, message = GitOperations.pull_repository(repo, timeout=timeout)

        if success:
            # Check if already up to date
            if "Already up to date" in message:
                if show_uptodate or cfg.get("verbose"):
                    output.print_success(repo, message)
                logger.log_repo_update_success(str(repo), message)
            else:
                output.print_success(repo, message)
                logger.log_repo_update_success(str(repo), message)
            updated_count += 1
        else:
            output.print_error(repo, message)
            logger.log_repo_update_error(str(repo), message)
            error_count += 1

    # Calculate elapsed time
    elapsed_time = time.time() - start_time

    # Log operation summary
    logger.log_operation_summary(
        total=len(repositories),
        updated=updated_count,
        skipped=skipped_count,
        errors=error_count,
        duration=elapsed_time,
    )

    # Print summary
    if not dry_run:
        output.print_summary(
            total=len(repositories),
            updated=updated_count,
            skipped=skipped_count,
            errors=error_count,
            elapsed_time=elapsed_time,
        )

    # Exit with error code if there were errors
    if error_count > 0:
        logger.error(f"Operation completed with {error_count} errors")
        raise SystemExit(1)

    logger.info("Operation completed successfully")


if __name__ == "__main__":
    main()
