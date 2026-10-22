"""Unit tests for the AI Storage Assistant module."""

from datetime import datetime, timedelta
from pathlib import Path
import pytest

from organizer.scanner import ScanSummary, FileInfo
from organizer.assistant import analyze_storage, StorageInsight, AssistantAnalysis


def test_assistant_empty_summary():
    """Verify assistant handles empty folders gracefully."""
    empty_summary = ScanSummary(folder_path=Path("/tmp/empty"))
    analysis = analyze_storage(empty_summary)

    assert analysis.total_files == 0
    assert "empty" in analysis.summary_headline.lower()
    assert len(analysis.insights) == 0


def test_assistant_heavy_media_and_stale_files():
    """Verify assistant detects heavy media categories and stale files."""
    old_time = datetime.now() - timedelta(days=120)
    recent_time = datetime.now() - timedelta(days=2)

    files = [
        FileInfo(
            path=Path("/tmp/movie.mp4"),
            relative_path=Path("movie.mp4"),
            name="movie.mp4",
            extension=".mp4",
            size_bytes=100 * 1024 * 1024,  # 100 MB
            size_formatted="100.00 MB",
            modified_time=old_time,
            category="Videos",
            suggested_folder="Videos",
        ),
        FileInfo(
            path=Path("/tmp/notes.txt"),
            relative_path=Path("notes.txt"),
            name="notes.txt",
            extension=".txt",
            size_bytes=1024,
            size_formatted="1.00 KB",
            modified_time=recent_time,
            category="Documents",
            suggested_folder="Documents",
        ),
    ]

    summary = ScanSummary(
        folder_path=Path("/tmp"),
        total_files=2,
        total_size_bytes=100 * 1024 * 1024 + 1024,
        category_counts={"Videos": 1, "Documents": 1},
        category_sizes={"Videos": 100 * 1024 * 1024, "Documents": 1024},
        files=files,
    )

    analysis = analyze_storage(summary, stale_days_threshold=90)

    assert analysis.total_files == 2
    assert len(analysis.stale_files) == 1
    assert analysis.stale_files[0].name == "movie.mp4"
    assert len(analysis.largest_files) == 2
    assert analysis.largest_files[0].name == "movie.mp4"

    # Should detect heavy video concentration
    titles = [ins.title for ins in analysis.insights]
    assert any("Video" in t for t in titles)
    assert any("Stale" in t for t in titles)


def test_assistant_duplicate_names():
    """Verify detection of duplicate filename clashes in different directories."""
    files = [
        FileInfo(
            path=Path("/tmp/folderA/image.png"),
            relative_path=Path("folderA/image.png"),
            name="image.png",
            extension=".png",
            size_bytes=2048,
            size_formatted="2.00 KB",
            modified_time=datetime.now(),
            category="Images",
            suggested_folder="Images",
        ),
        FileInfo(
            path=Path("/tmp/folderB/image.png"),
            relative_path=Path("folderB/image.png"),
            name="image.png",
            extension=".png",
            size_bytes=4096,
            size_formatted="4.00 KB",
            modified_time=datetime.now(),
            category="Images",
            suggested_folder="Images",
        ),
    ]

    summary = ScanSummary(
        folder_path=Path("/tmp"),
        total_files=2,
        total_size_bytes=6144,
        category_counts={"Images": 2},
        category_sizes={"Images": 6144},
        files=files,
    )

    analysis = analyze_storage(summary)
    assert len(analysis.duplicate_names) == 1
    assert "image.png" in analysis.duplicate_names
    assert len(analysis.duplicate_names["image.png"]) == 2
