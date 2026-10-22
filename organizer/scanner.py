"""Directory scanning and file metadata extraction.

This module inspects target folders, categorizes discovered files,
gathers file system statistics (size, modification date), and handles
access errors and symlink loops gracefully.
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set
import os

from .categories import get_category_for_file, DEFAULT_CATEGORIES


# Files and directories that should typically be ignored during scans
DEFAULT_IGNORED_NAMES: Set[str] = {
    ".git", ".svn", ".hg", ".DS_Store", "desktop.ini", "Thumbs.db",
    "$RECYCLE.BIN", "System Volume Information", "node_modules", ".venv", "venv",
    "__pycache__", ".pytest_cache", ".idea", ".vscode", "assets"
}


def format_file_size(size_bytes: int) -> str:
    """Converts a raw byte count into a human-readable string (e.g. 1.25 MB).

    Args:
        size_bytes: Non-negative integer of bytes.

    Returns:
        Formatted string with proper unit (B, KB, MB, GB, TB).
    """
    if size_bytes < 0:
        return "0 B"
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0 or unit == "TB":
            return f"{size_bytes:.2f} {unit}" if unit != "B" else f"{size_bytes} B"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


@dataclass
class FileInfo:
    """Metadata container for a single file discovered during scan."""
    path: Path
    relative_path: Path
    name: str
    extension: str
    size_bytes: int
    size_formatted: str
    modified_time: datetime
    category: str
    suggested_folder: str

    @property
    def modified_formatted(self) -> str:
        """Formatted modification timestamp."""
        return self.modified_time.strftime("%Y-%m-%d %H:%M:%S")


@dataclass
class ScanSummary:
    """Aggregated scan statistics and discovered files."""
    folder_path: Path
    total_files: int = 0
    total_size_bytes: int = 0
    category_counts: Dict[str, int] = field(default_factory=dict)
    category_sizes: Dict[str, int] = field(default_factory=dict)
    files: List[FileInfo] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    @property
    def total_size_formatted(self) -> str:
        """Formatted aggregate size of all scanned files."""
        return format_file_size(self.total_size_bytes)

    def to_dict_list(self) -> List[Dict]:
        """Converts files list into records suitable for pandas DataFrame display."""
        return [
            {
                "Name": f.name,
                "Category": f.category,
                "Target Folder": f.suggested_folder,
                "Size": f.size_formatted,
                "Size (Bytes)": f.size_bytes,
                "Extension": f.extension or "(none)",
                "Modified": f.modified_formatted,
                "Path": str(f.path),
            }
            for f in self.files
        ]


def scan_directory(
    folder_path: Path | str,
    recursive: bool = False,
    skip_hidden: bool = True,
    custom_categories: Optional[Dict[str, List[str]]] = None,
    category_folder_names: Optional[Dict[str, str]] = None,
) -> ScanSummary:
    """Scans the designated directory and collects file information.

    Args:
        folder_path: The directory path to scan.
        recursive: If True, recursively scans nested subdirectories.
        skip_hidden: If True, skips dotfiles and known system files.
        custom_categories: Optional custom category definitions.
        category_folder_names: Optional mapping from category name to folder name.

    Returns:
        ScanSummary with aggregated counts, sizes, and file details.
    """
    target_path = Path(folder_path).resolve()
    summary = ScanSummary(folder_path=target_path)

    if not target_path.exists():
        summary.errors.append(f"Directory does not exist: {target_path}")
        return summary

    if not target_path.is_dir():
        summary.errors.append(f"Path is not a directory: {target_path}")
        return summary

    # Build folder name mapping for categories
    folder_names = category_folder_names or {}
    active_categories = custom_categories or DEFAULT_CATEGORIES
    target_category_dirs = {
        folder_names.get(cat, cat).lower()
        for cat in list(active_categories.keys()) + ["Others"]
    }

    # Initialize counters for all known categories
    all_cat_keys = list(active_categories.keys()) + ["Others"]
    for cat in all_cat_keys:
        summary.category_counts[cat] = 0
        summary.category_sizes[cat] = 0

    try:
        iterator = target_path.rglob("*") if recursive else target_path.iterdir()
    except (PermissionError, OSError) as e:
        summary.errors.append(f"Unable to read directory {target_path}: {e}")
        return summary

    for item in iterator:
        try:
            # Skip directories; we only organize files
            # Protect against broken symlinks
            if not item.is_file():
                continue

            # Hidden/system file filtering
            if skip_hidden:
                if item.name.startswith(".") or item.name in DEFAULT_IGNORED_NAMES:
                    continue
                # Also check parent parts if recursive
                if any(part.startswith(".") or part in DEFAULT_IGNORED_NAMES for part in item.parent.parts):
                    continue

            # Defensive guard: Do not organize the app's own source code if repo root is scanned
            if item.name in {"app.py", "requirements.txt", "README.md", "LICENSE", "CONTRIBUTING.md", "CHANGELOG.md"}:
                if (target_path / "organizer").exists() and (target_path / "app.py").exists():
                    # Running inside project root; keep core repo files protected
                    continue

            # If scanning root, prevent reorganizing files that are already inside a category folder
            # when those category folders are in target_path
            rel = item.relative_to(target_path)
            if len(rel.parts) > 1 and rel.parts[0].lower() in target_category_dirs:
                # File is already inside an organized category folder
                continue

            stat = item.stat()
            size = stat.st_size
            mod_time = datetime.fromtimestamp(stat.st_mtime)

            cat = get_category_for_file(item, custom_categories)
            folder_name = folder_names.get(cat, cat)

            file_info = FileInfo(
                path=item,
                relative_path=rel,
                name=item.name,
                extension=item.suffix.lower(),
                size_bytes=size,
                size_formatted=format_file_size(size),
                modified_time=mod_time,
                category=cat,
                suggested_folder=folder_name,
            )

            summary.files.append(file_info)
            summary.total_files += 1
            summary.total_size_bytes += size
            summary.category_counts[cat] = summary.category_counts.get(cat, 0) + 1
            summary.category_sizes[cat] = summary.category_sizes.get(cat, 0) + size

        except (PermissionError, FileNotFoundError, OSError) as err:
            summary.errors.append(f"Failed to access '{item.name}': {err}")

    return summary
