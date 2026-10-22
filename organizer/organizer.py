"""File organization execution engine with preview, collision resolution, and rollback.

This module safely plans and executes moving files into their designated category folders,
with duplicate name collision resolution, path traversal defense, detailed audit logging,
and one-click undo support.
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, List, Optional, Set, Tuple
import shutil
import os

from .scanner import ScanSummary, FileInfo


@dataclass
class MovePlanItem:
    """Represents a planned file movement."""
    file_info: FileInfo
    source_path: Path
    destination_path: Path
    category: str
    target_folder_name: str
    is_already_in_place: bool = False
    is_collision_renamed: bool = False
    original_target_name: str = ""
    status: str = "PENDING"  # PENDING, SIMULATED, COMPLETED, SKIPPED, FAILED
    error_message: Optional[str] = None

    @property
    def display_status(self) -> str:
        """User-friendly status label."""
        if self.is_already_in_place:
            return "Already Organized"
        if self.is_collision_renamed:
            return "Rename & Move (Conflict)"
        return "Move"


@dataclass
class OrganizationReport:
    """Summary report of an organization or preview execution."""
    timestamp: datetime = field(default_factory=datetime.now)
    dry_run: bool = False
    total_planned: int = 0
    total_moved: int = 0
    total_skipped: int = 0
    total_errors: int = 0
    items: List[MovePlanItem] = field(default_factory=list)
    undo_records: List[Tuple[Path, Path]] = field(default_factory=list)  # (current_dest, original_src)
    logs: List[Dict[str, str]] = field(default_factory=list)

    @property
    def formatted_time(self) -> str:
        """Formatted timestamp."""
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S")

    def to_summary_dict(self) -> Dict[str, any]:
        """Dictionary summary of the operation."""
        return {
            "Timestamp": self.formatted_time,
            "Mode": "Preview (Dry Run)" if self.dry_run else "Executed",
            "Total Planned": self.total_planned,
            "Successfully Moved": self.total_moved,
            "Skipped": self.total_skipped,
            "Errors": self.total_errors,
        }


def _resolve_unique_destination(
    target_folder: Path,
    original_filename: str,
    reserved_destinations: Set[Path]
) -> Tuple[Path, bool]:
    """Generates a non-conflicting destination path by appending an incremental index if needed.

    Args:
        target_folder: The directory where the file will reside.
        original_filename: The base filename with extension (e.g. 'doc.pdf').
        reserved_destinations: Set of paths already claimed in current plan or on disk.

    Returns:
        Tuple of (resolved_path, was_renamed_boolean).
    """
    stem = Path(original_filename).stem
    suffix = Path(original_filename).suffix

    candidate = target_folder / original_filename
    if candidate not in reserved_destinations and not candidate.exists():
        reserved_destinations.add(candidate)
        return candidate, False

    # Name collision exists; append incremental suffix: "stem (1).ext", "stem (2).ext", etc.
    counter = 1
    while True:
        candidate_name = f"{stem} ({counter}){suffix}"
        candidate = target_folder / candidate_name
        if candidate not in reserved_destinations and not candidate.exists():
            reserved_destinations.add(candidate)
            return candidate, True
        counter += 1


def generate_move_plan(
    summary: ScanSummary,
    category_folder_names: Optional[Dict[str, str]] = None,
) -> List[MovePlanItem]:
    """Prepares an actionable, collision-safe movement plan for all scanned files.

    Args:
        summary: ScanSummary containing discovered files and target directory.
        category_folder_names: Optional overrides for category directory names.

    Returns:
        List of MovePlanItem objects describing intended source -> destination.
    """
    plan: List[MovePlanItem] = []
    reserved_destinations: Set[Path] = set()
    folder_mapping = category_folder_names or {}
    base_folder = summary.folder_path

    for file_info in summary.files:
        src = file_info.path
        cat = file_info.category
        folder_name = folder_mapping.get(cat, cat)
        target_dir = (base_folder / folder_name).resolve()

        # Path traversal guard: ensure target_dir is strictly inside base_folder
        try:
            target_dir.relative_to(base_folder.resolve())
        except ValueError:
            # Illegal folder mapping attempting directory escape
            target_dir = base_folder / cat

        # Check if file is already in the target folder
        if src.parent.resolve() == target_dir:
            item = MovePlanItem(
                file_info=file_info,
                source_path=src,
                destination_path=src,
                category=cat,
                target_folder_name=folder_name,
                is_already_in_place=True,
                status="SKIPPED",
            )
            plan.append(item)
            continue

        # Resolve destination path with conflict avoidance
        dest, was_renamed = _resolve_unique_destination(
            target_folder=target_dir,
            original_filename=file_info.name,
            reserved_destinations=reserved_destinations
        )

        item = MovePlanItem(
            file_info=file_info,
            source_path=src,
            destination_path=dest,
            category=cat,
            target_folder_name=folder_name,
            is_already_in_place=False,
            is_collision_renamed=was_renamed,
            original_target_name=file_info.name,
            status="PENDING",
        )
        plan.append(item)

    return plan


def execute_move_plan(
    plan: List[MovePlanItem],
    dry_run: bool = False,
    progress_callback: Optional[Callable[[int, int, str], None]] = None,
) -> OrganizationReport:
    """Executes or simulates the planned file movements.

    Args:
        plan: List of MovePlanItem items generated by generate_move_plan.
        dry_run: If True, tests actions without touching the filesystem.
        progress_callback: Optional callback func(current_index, total_count, filename).

    Returns:
        OrganizationReport detailing success, skips, errors, and undo history.
    """
    report = OrganizationReport(dry_run=dry_run, total_planned=len(plan))
    total_items = len(plan)

    for idx, item in enumerate(plan, start=1):
        if progress_callback:
            progress_callback(idx, total_items, item.source_path.name)

        if item.is_already_in_place:
            item.status = "SKIPPED"
            report.total_skipped += 1
            report.items.append(item)
            report.logs.append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "file": item.source_path.name,
                "status": "Skipped",
                "message": "File is already in the target category folder.",
            })
            continue

        # Dry run simulation mode
        if dry_run:
            item.status = "SIMULATED"
            report.total_moved += 1
            report.items.append(item)
            note = f"Would move to {item.destination_path.parent.name}/{item.destination_path.name}"
            if item.is_collision_renamed:
                note += " (renamed to resolve conflict)"
            report.logs.append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "file": item.source_path.name,
                "status": "Simulated",
                "message": note,
            })
            continue

        # Live execution mode
        try:
            # 1. Ensure target directory exists
            item.destination_path.parent.mkdir(parents=True, exist_ok=True)

            # 2. Verify source still exists
            if not item.source_path.exists():
                raise FileNotFoundError(f"Source file not found: {item.source_path}")

            # 3. Move file safely
            shutil.move(str(item.source_path), str(item.destination_path))

            # 4. Record success and undo entry
            item.status = "COMPLETED"
            report.total_moved += 1
            report.undo_records.append((item.destination_path, item.source_path))

            msg = f"Moved to {item.destination_path.parent.name}/{item.destination_path.name}"
            if item.is_collision_renamed:
                msg += f" (Renamed from '{item.original_target_name}' to prevent collision)"

            report.logs.append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "file": item.source_path.name,
                "status": "Success",
                "message": msg,
            })

        except (PermissionError, OSError, Exception) as err:
            item.status = "FAILED"
            item.error_message = str(err)
            report.total_errors += 1
            report.logs.append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "file": item.source_path.name,
                "status": "Error",
                "message": f"Move failed: {err}",
            })

        report.items.append(item)

    return report


def undo_last_moves(
    undo_records: List[Tuple[Path, Path]],
    progress_callback: Optional[Callable[[int, int, str], None]] = None,
) -> Tuple[int, int, List[Dict[str, str]]]:
    """Reverts files from their current location back to their original paths.

    Args:
        undo_records: List of tuples (current_dest_path, original_source_path).
        progress_callback: Optional progress reporter callback.

    Returns:
        Tuple of (restored_count, error_count, log_entries).
    """
    restored = 0
    errors = 0
    logs: List[Dict[str, str]] = []
    total = len(undo_records)

    # Revert in reverse order of moves
    for idx, (current_path, original_path) in enumerate(reversed(undo_records), start=1):
        if progress_callback:
            progress_callback(idx, total, current_path.name)

        try:
            if not current_path.exists():
                logs.append({
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "file": current_path.name,
                    "status": "Skipped",
                    "message": f"File no longer exists at {current_path}",
                })
                errors += 1
                continue

            # Ensure original directory exists
            original_path.parent.mkdir(parents=True, exist_ok=True)

            # Move back
            shutil.move(str(current_path), str(original_path))
            restored += 1
            logs.append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "file": current_path.name,
                "status": "Restored",
                "message": f"Restored back to {original_path}",
            })

            # Clean up empty parent folder if it's now empty
            parent_dir = current_path.parent
            try:
                if parent_dir.exists() and not any(parent_dir.iterdir()):
                    parent_dir.rmdir()
            except OSError:
                pass  # Directory not empty or permissions restrict removal

        except Exception as err:
            errors += 1
            logs.append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "file": current_path.name,
                "status": "Error",
                "message": f"Undo failed: {err}",
            })

    return restored, errors, logs
