"""Demo data generator for Smart File Organizer.

Creates a sandbox folder with simulated messy files across all required categories
so users can immediately test the scanning, preview, collision handling, and organization features.
"""

from pathlib import Path
from typing import Dict, List
import os


DEMO_FILES: Dict[str, List[Dict[str, any]]] = {
    "Images": [
        {"name": "vacation_sunset.jpg", "content": b"\xFF\xD8\xFF\xE0\x00\x10JFIF" + b"demo_jpg_data" * 200},
        {"name": "app_screenshot.png", "content": b"\x89PNG\r\n\x1a\n" + b"demo_png_data" * 150},
        {"name": "family_portrait.jpeg", "content": b"\xFF\xD8\xFF\xE0\x00\x10JFIF" + b"demo_jpeg" * 100},
        {"name": "company_logo.svg", "content": b"<svg xmlns='http://www.w3.org/2000/svg'><circle r='10'/></svg>"},
    ],
    "Videos": [
        {"name": "screen_recording_demo.mp4", "content": b"\x00\x00\x00 ftypisom" + b"demo_mp4_bytes" * 500},
        {"name": "holiday_clip.mkv", "content": b"\x1A\x45\xDF\xA3" + b"demo_mkv_bytes" * 400},
    ],
    "Documents": [
        {"name": "quarterly_financial_report.pdf", "content": b"%PDF-1.5 demo financial report text content" * 100},
        {"name": "project_requirements.docx", "content": b"PK\x03\x04 demo word document xml content" * 80},
        {"name": "quick_notes.txt", "content": b"Buy groceries\nSchedule dentist appointment\nShip project v1.0"},
        {"name": "budget_forecast.xlsx", "content": b"PK\x03\x04 demo excel workbook content" * 60},
    ],
    "Code files": [
        {"name": "backend_server.py", "content": b"# Server script\nimport http.server\nprint('Server ready')\n"},
        {"name": "main.js", "content": b"// Client code\nconsole.log('Smart File Organizer active');\n"},
        {"name": "CustomerService.java", "content": b"public class CustomerService { public static void main(String[] args){} }\n"},
        {"name": "index.html", "content": b"<!DOCTYPE html><html><head><title>App</title></head><body>Hello</body></html>"},
        {"name": "styles.css", "content": b"body { font-family: sans-serif; margin: 0; padding: 20px; }\n"},
    ],
    "Archives": [
        {"name": "client_backup_2024.zip", "content": b"PK\x03\x04 demo zip archive container" * 120},
        {"name": "raw_footage_bundle.rar", "content": b"Rar!\x1a\x07\x00 demo rar archive payload" * 100},
    ],
    "Others": [
        {"name": "firmware_patch_v2.bin", "content": b"\x00\xFF\xAA\x55" * 150},
        {"name": "system_cache.dat", "content": b"RAW_CACHE_DATA_STREAM" * 80},
    ]
}


def create_demo_messy_folder(target_dir: Path | str) -> Path:
    """Populates the specified directory with realistic mock messy files across all categories.

    Args:
        target_dir: Destination directory where demo files will be placed.

    Returns:
        Path of the created demo folder.
    """
    dest = Path(target_dir).resolve()
    dest.mkdir(parents=True, exist_ok=True)

    created_count = 0
    for category, file_list in DEMO_FILES.items():
        for file_meta in file_list:
            file_path = dest / file_meta["name"]
            # Write binary or string content
            content = file_meta["content"]
            if isinstance(content, str):
                content = content.encode("utf-8")
            file_path.write_bytes(content)
            created_count += 1

    # Also add a nested messy subfolder with a name collision to demo collision handling and recursion!
    sub_messy = dest / "random_downloads"
    sub_messy.mkdir(exist_ok=True)
    # Same filename as top-level vacation_sunset.jpg to test collision renaming resolution!
    (sub_messy / "vacation_sunset.jpg").write_bytes(b"duplicate name image from another folder")
    (sub_messy / "draft_presentation.pptx").write_bytes(b"PK\x03\x04 presentation slides")

    return dest
