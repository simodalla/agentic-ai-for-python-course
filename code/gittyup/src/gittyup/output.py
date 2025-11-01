"""
Output formatting module for beautiful console output.

This module provides colored and formatted output for the CLI,
making it easy to understand the status of operations.
"""

from typing import List
from pathlib import Path
import colorama
from colorama import Fore, Style

# Initialize colorama for cross-platform colored output
colorama.init(autoreset=True)


class OutputFormatter:
    """Handles formatted console output with colors."""

    @staticmethod
    def print_banner() -> None:
        """Print the application banner."""
        banner = f"""
{Fore.CYAN}{Style.BRIGHT}╔═══════════════════════════════════════╗
║           🚀 Gitty Up 🚀             ║
║   Keeping Your Repos Up to Date      ║
╚═══════════════════════════════════════╝{Style.RESET_ALL}
"""
        print(banner)

    @staticmethod
    def print_scanning(path: str) -> None:
        """Print scanning message."""
        print(f"\n{Fore.BLUE}🔍 Scanning for repositories in: {Style.BRIGHT}{path}{Style.RESET_ALL}")

    @staticmethod
    def print_found_repos(count: int) -> None:
        """Print number of repositories found."""
        if count == 0:
            print(f"{Fore.YELLOW}⚠️  No repositories found{Style.RESET_ALL}")
        elif count == 1:
            print(f"{Fore.GREEN}✓ Found 1 repository{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}✓ Found {count} repositories{Style.RESET_ALL}")

    @staticmethod
    def print_updating() -> None:
        """Print updating message."""
        print(f"\n{Fore.BLUE}📥 Updating repositories...{Style.RESET_ALL}\n")

    @staticmethod
    def print_success(repo_path: Path, message: str) -> None:
        """Print success message for a repository."""
        repo_name = repo_path.name
        print(f"{Fore.GREEN}✓ {Style.BRIGHT}{repo_name:<30}{Style.RESET_ALL} {message}")

    @staticmethod
    def print_warning(repo_path: Path, message: str) -> None:
        """Print warning message for a repository."""
        repo_name = repo_path.name
        print(f"{Fore.YELLOW}⚠ {Style.BRIGHT}{repo_name:<30}{Style.RESET_ALL} {message}")

    @staticmethod
    def print_error(repo_path: Path, message: str) -> None:
        """Print error message for a repository."""
        repo_name = repo_path.name
        print(f"{Fore.RED}✗ {Style.BRIGHT}{repo_name:<30}{Style.RESET_ALL} {message}")

    @staticmethod
    def print_skipped(repo_path: Path, reason: str) -> None:
        """Print skipped message for a repository."""
        repo_name = repo_path.name
        print(f"{Fore.LIGHTBLACK_EX}○ {Style.BRIGHT}{repo_name:<30}{Style.RESET_ALL} Skipped: {reason}")

    @staticmethod
    def print_summary(
        total: int,
        updated: int,
        skipped: int,
        errors: int,
        elapsed_time: float
    ) -> None:
        """Print summary of operations."""
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT}Summary:{Style.RESET_ALL}")
        print(f"  Total repositories: {total}")
        
        if updated > 0:
            print(f"  {Fore.GREEN}✓ Updated: {updated}{Style.RESET_ALL}")
        
        if skipped > 0:
            print(f"  {Fore.YELLOW}○ Skipped: {skipped}{Style.RESET_ALL}")
        
        if errors > 0:
            print(f"  {Fore.RED}✗ Errors: {errors}{Style.RESET_ALL}")
        
        print(f"  ⏱️  Time elapsed: {elapsed_time:.2f}s")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

    @staticmethod
    def print_error_message(message: str) -> None:
        """Print a general error message."""
        print(f"\n{Fore.RED}{Style.BRIGHT}ERROR:{Style.RESET_ALL} {message}\n")

    @staticmethod
    def print_info(message: str) -> None:
        """Print an informational message."""
        print(f"{Fore.BLUE}ℹ️  {message}{Style.RESET_ALL}")

