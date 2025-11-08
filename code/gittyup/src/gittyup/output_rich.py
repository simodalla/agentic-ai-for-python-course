"""
Enhanced output formatting with Rich library.

Provides progress bars, tables, and beautiful formatting.
"""

from typing import Optional
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich.panel import Panel
from rich import box


class RichOutputFormatter:
    """Enhanced output formatter using Rich library."""

    def __init__(self, verbose: bool = False, quiet: bool = False):
        """
        Initialize the Rich output formatter.

        Args:
            verbose: Show detailed output
            quiet: Minimal output (only errors and summary)
        """
        self.console = Console()
        self.verbose = verbose
        self.quiet = quiet

    def print_banner(self) -> None:
        """Print the application banner."""
        if self.quiet:
            return

        banner = Panel.fit(
            "[bold cyan]🚀 Gitty Up 🚀[/bold cyan]\n[cyan]Keeping Your Repos Up to Date[/cyan]",
            border_style="cyan",
            padding=(0, 2),
        )
        self.console.print()
        self.console.print(banner)
        self.console.print()

    def print_scanning(self, path: str) -> None:
        """Print scanning message."""
        if not self.quiet:
            self.console.print(f"[blue]🔍 Scanning for repositories in:[/blue] [bold]{path}[/bold]")

    def print_found_repos(self, count: int) -> None:
        """Print number of repositories found."""
        if self.quiet:
            return

        if count == 0:
            self.console.print("[yellow]⚠️  No repositories found[/yellow]")
        elif count == 1:
            self.console.print("[green]✓ Found 1 repository[/green]")
        else:
            self.console.print(f"[green]✓ Found {count} repositories[/green]")

    def print_updating(self) -> None:
        """Print updating message."""
        if not self.quiet:
            self.console.print("\n[blue]📥 Updating repositories...[/blue]\n")

    def create_progress_bar(self) -> Progress:
        """
        Create a progress bar for repository updates.

        Returns:
            Progress instance
        """
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=self.console,
            transient=False,
        )

    def print_success(self, repo_path: Path, message: str, verbose: bool = False) -> None:
        """Print success message for a repository."""
        if self.quiet and not verbose:
            return

        repo_name = repo_path.name
        if self.verbose or verbose:
            self.console.print(f"[green]✓[/green] [bold]{repo_name:30}[/bold] {message}")
        else:
            self.console.print(f"[green]✓[/green] [bold]{repo_name:30}[/bold] {message}")

    def print_warning(self, repo_path: Path, message: str) -> None:
        """Print warning message for a repository."""
        if self.quiet:
            return

        repo_name = repo_path.name
        self.console.print(f"[yellow]⚠[/yellow] [bold]{repo_name:30}[/bold] {message}")

    def print_error(self, repo_path: Path, message: str) -> None:
        """Print error message for a repository (always shown)."""
        repo_name = repo_path.name
        self.console.print(f"[red]✗[/red] [bold]{repo_name:30}[/bold] {message}")

    def print_skipped(self, repo_path: Path, reason: str) -> None:
        """Print skipped message for a repository."""
        if self.quiet:
            return

        repo_name = repo_path.name
        self.console.print(f"[dim]○[/dim] [bold]{repo_name:30}[/bold] Skipped: {reason}")

    def print_summary_table(
        self,
        total: int,
        updated: int,
        skipped: int,
        errors: int,
        elapsed_time: float,
    ) -> None:
        """Print summary as a formatted table."""
        table = Table(title="Summary", box=box.ROUNDED, show_header=False)
        table.add_column("Metric", style="cyan", justify="left")
        table.add_column("Value", justify="right")

        table.add_row("Total repositories", str(total))

        if updated > 0:
            table.add_row("[green]✓ Updated[/green]", f"[green]{updated}[/green]")

        if skipped > 0:
            table.add_row("[yellow]○ Skipped[/yellow]", f"[yellow]{skipped}[/yellow]")

        if errors > 0:
            table.add_row("[red]✗ Errors[/red]", f"[red]{errors}[/red]")

        table.add_row("⏱️  Time elapsed", f"{elapsed_time:.2f}s")

        self.console.print()
        self.console.print(table)
        self.console.print()

    def print_summary(
        self,
        total: int,
        updated: int,
        skipped: int,
        errors: int,
        elapsed_time: float,
    ) -> None:
        """Print summary of operations."""
        # Use table format for better visual appeal
        self.print_summary_table(total, updated, skipped, errors, elapsed_time)

    def print_error_message(self, message: str) -> None:
        """Print a general error message."""
        self.console.print(f"\n[bold red]ERROR:[/bold red] {message}\n")

    def print_info(self, message: str) -> None:
        """Print an informational message."""
        if not self.quiet:
            self.console.print(f"[blue]ℹ️  {message}[/blue]")

    def print_verbose(self, message: str) -> None:
        """Print a verbose message (only shown in verbose mode)."""
        if self.verbose:
            self.console.print(f"[dim]{message}[/dim]")

    def print_config_info(self, config_path: Optional[Path]) -> None:
        """Print configuration file information."""
        if self.verbose and config_path:
            self.console.print(f"[dim]Using configuration: {config_path}[/dim]")

    def print_log_info(self, log_path: Optional[Path]) -> None:
        """Print log file information."""
        if self.verbose and log_path:
            self.console.print(f"[dim]Logging to: {log_path}[/dim]")
