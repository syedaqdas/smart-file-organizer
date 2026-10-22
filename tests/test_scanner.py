"""Unit tests for the scanner module."""

from pathlib import Path
import tempfile
import pytest

from organizer.categories import get_category_for_file, build_extension_map
from organizer.scanner import scan_directory, format_file_size, FileInfo, ScanSummary


def test_category_matching():
    """Verify that file extensions match their expected categories."""
    assert get_category_for_file(Path("photo.jpg")) == "Images"
    assert get_category_for_file(Path("logo.png")) == "Images"
    assert get_category_for_file(Path("clip.mp4")) == "Videos"
    assert get_category_for_file(Path("movie.mkv")) == "Videos"
    assert get_category_for_file(Path("paper.pdf")) == "Documents"
    assert get_category_for_file(Path("notes.docx")) == "Documents"
    assert get_category_for_file(Path("readme.txt")) == "Documents"
    assert get_category_for_file(Path("app.py")) == "Code files"
    assert get_category_for_file(Path("script.js")) == "Code files"
    assert get_category_for_file(Path("Main.java")) == "Code files"
    assert get_category_for_file(Path("index.html")) == "Code files"
    assert get_category_for_file(Path("data.zip")) == "Archives"
    assert get_category_for_file(Path("bundle.rar")) == "Archives"
    assert get_category_for_file(Path("audio.mp3")) == "Audio"
    assert get_category_for_file(Path("unknown.xyz123")) == "Others"


def test_format_file_size():
    """Verify human-readable byte formatting."""
    assert format_file_size(0) == "0 B"
    assert format_file_size(500) == "500 B"
    assert format_file_size(1024) == "1.00 KB"
    assert format_file_size(1024 * 1024) == "1.00 MB"
    assert format_file_size(1024 * 1024 * 5 + 500) == "5.00 MB"


def test_scan_directory_basic(tmp_path: Path):
    """Test standard scanning of a messy folder."""
    # Create sample files
    (tmp_path / "img1.png").write_text("fake image content")
    (tmp_path / "doc1.pdf").write_text("fake pdf content")
    (tmp_path / "code1.py").write_text("print(1)")
    (tmp_path / "archive1.zip").write_text("fake zip")
    (tmp_path / "random.bin").write_text("binary data")

    summary = scan_directory(tmp_path, recursive=False)

    assert summary.total_files == 5
    assert summary.category_counts["Images"] == 1
    assert summary.category_counts["Documents"] == 1
    assert summary.category_counts["Code files"] == 1
    assert summary.category_counts["Archives"] == 1
    assert summary.category_counts["Others"] == 1
    assert summary.total_size_bytes > 0
    assert len(summary.errors) == 0


def test_scan_directory_hidden_files(tmp_path: Path):
    """Test that hidden and system files are skipped by default."""
    (tmp_path / "normal.txt").write_text("text")
    (tmp_path / ".DS_Store").write_text("mac junk")
    (tmp_path / "desktop.ini").write_text("windows junk")

    summary = scan_directory(tmp_path, skip_hidden=True)
    assert summary.total_files == 1
    assert summary.files[0].name == "normal.txt"


def test_scan_nonexistent_directory():
    """Verify error handling on invalid path."""
    fake_path = Path("Z:/definitely_does_not_exist_xyz123456")
    summary = scan_directory(fake_path)
    assert summary.total_files == 0
    assert len(summary.errors) > 0
