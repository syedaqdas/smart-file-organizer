"""Unit tests for the organizer execution engine."""

from pathlib import Path
import pytest

from organizer.scanner import scan_directory
from organizer.organizer import (
    generate_move_plan,
    execute_move_plan,
    undo_last_moves,
    _resolve_unique_destination,
)


def test_dry_run_does_not_modify_disk(tmp_path: Path):
    """Verify preview/dry-run mode does not move files."""
    test_file = tmp_path / "picture.jpg"
    test_file.write_text("dummy picture data")

    summary = scan_directory(tmp_path)
    plan = generate_move_plan(summary)

    assert len(plan) == 1
    assert plan[0].category == "Images"
    assert plan[0].target_folder_name == "Images"

    report = execute_move_plan(plan, dry_run=True)

    assert report.dry_run is True
    assert report.total_moved == 1
    assert report.total_errors == 0
    # The file should still be at original location!
    assert test_file.exists()
    assert not (tmp_path / "Images" / "picture.jpg").exists()


def test_live_execution_organizes_files(tmp_path: Path):
    """Verify live run creates directories and relocates files properly."""
    img = tmp_path / "photo.png"
    doc = tmp_path / "notes.txt"
    code = tmp_path / "script.py"

    img.write_text("image content")
    doc.write_text("doc content")
    code.write_text("print('hello')")

    summary = scan_directory(tmp_path)
    plan = generate_move_plan(summary)
    report = execute_move_plan(plan, dry_run=False)

    assert report.total_moved == 3
    assert report.total_errors == 0

    # Original root files should have moved
    assert not img.exists()
    assert not doc.exists()
    assert not code.exists()

    # Destination files must exist
    dest_img = tmp_path / "Images" / "photo.png"
    dest_doc = tmp_path / "Documents" / "notes.txt"
    dest_code = tmp_path / "Code files" / "script.py"

    assert dest_img.exists()
    assert dest_doc.exists()
    assert dest_code.exists()


def test_collision_resolution(tmp_path: Path):
    """Verify collision resolution renames colliding filenames without data loss."""
    # Pre-create a file in target folder
    target_img_dir = tmp_path / "Images"
    target_img_dir.mkdir(parents=True, exist_ok=True)
    existing_img = target_img_dir / "sunset.jpg"
    existing_img.write_text("existing image")

    # Now have another file in root with identical name
    incoming_img = tmp_path / "sunset.jpg"
    incoming_img.write_text("incoming new image")

    summary = scan_directory(tmp_path)
    plan = generate_move_plan(summary)

    # Only incoming_img should be planned to move (existing_img is inside Images)
    assert len(plan) == 1
    assert plan[0].is_collision_renamed is True
    assert plan[0].destination_path.name == "sunset (1).jpg"

    report = execute_move_plan(plan, dry_run=False)
    assert report.total_moved == 1
    assert report.total_errors == 0

    # Both files must coexist without overwriting
    assert existing_img.exists()
    assert existing_img.read_text() == "existing image"

    renamed_dest = target_img_dir / "sunset (1).jpg"
    assert renamed_dest.exists()
    assert renamed_dest.read_text() == "incoming new image"


def test_undo_restoration(tmp_path: Path):
    """Verify that undo completely reverts organized files to original locations."""
    f1 = tmp_path / "file1.pdf"
    f2 = tmp_path / "file2.zip"
    f1.write_text("pdf data")
    f2.write_text("zip data")

    summary = scan_directory(tmp_path)
    plan = generate_move_plan(summary)
    report = execute_move_plan(plan, dry_run=False)

    assert (tmp_path / "Documents" / "file1.pdf").exists()
    assert (tmp_path / "Archives" / "file2.zip").exists()

    # Perform undo
    restored, errors, logs = undo_last_moves(report.undo_records)

    assert restored == 2
    assert errors == 0
    # Files should be back in original locations
    assert f1.exists()
    assert f2.exists()
    # Empty folders should have been cleaned up
    assert not (tmp_path / "Documents").exists()
    assert not (tmp_path / "Archives").exists()
