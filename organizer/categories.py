"""File categorization rules and extension mappings.

This module defines standard categories, file extensions, and visual themes
(colors & icons) used across the Smart File Organizer.
"""

from typing import Dict, List, Optional
import os
from pathlib import Path

# Standard category to extensions mapping
DEFAULT_CATEGORIES: Dict[str, List[str]] = {
    "Images": [
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp",
        ".tiff", ".tif", ".ico", ".raw", ".heic", ".psd"
    ],
    "Videos": [
        ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm",
        ".m4v", ".3gp", ".mpeg", ".mpg", ".vob"
    ],
    "Documents": [
        ".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx",
        ".ppt", ".csv", ".rtf", ".odt", ".ods", ".odp", ".epub",
        ".md", ".pages", ".numbers", ".key"
    ],
    "Code files": [
        ".py", ".js", ".jsx", ".ts", ".tsx", ".html", ".css", ".scss",
        ".java", ".c", ".cpp", ".h", ".hpp", ".cs", ".go", ".rs",
        ".php", ".rb", ".swift", ".kt", ".kts", ".sh", ".bash",
        ".sql", ".json", ".xml", ".yaml", ".yml", ".toml", ".ini",
        ".env", ".bat", ".cmd", ".ps1"
    ],
    "Archives": [
        ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz",
        ".tgz", ".iso", ".dmg", ".pkg", ".deb"
    ],
    "Audio": [
        ".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma", ".opus"
    ],
}

# Distinct modern color palette for Plotly charts and badges
CATEGORY_COLORS: Dict[str, str] = {
    "Images": "#3B82F6",      # Blue
    "Videos": "#EC4899",      # Pink
    "Documents": "#10B981",   # Emerald green
    "Code files": "#8B5CF6",  # Purple
    "Archives": "#F59E0B",    # Amber
    "Audio": "#06B6D4",       # Cyan
    "Others": "#6B7280",      # Cool gray
}

# Intuitive emojis for UI display
CATEGORY_ICONS: Dict[str, str] = {
    "Images": "🖼️",
    "Videos": "🎬",
    "Documents": "📄",
    "Code files": "💻",
    "Archives": "📦",
    "Audio": "🎵",
    "Others": "📁",
}


def build_extension_map(categories: Optional[Dict[str, List[str]]] = None) -> Dict[str, str]:
    """Inverts category -> extensions dict to extension -> category lookup map for O(1) checks.

    Args:
        categories: Custom or default categories dictionary.

    Returns:
        Dict mapping lowercase extensions (e.g. '.jpg') to category name (e.g. 'Images').
    """
    cats = categories if categories is not None else DEFAULT_CATEGORIES
    ext_map: Dict[str, str] = {}
    for cat_name, extensions in cats.items():
        for ext in extensions:
            clean_ext = ext.lower().strip()
            if not clean_ext.startswith("."):
                clean_ext = f".{clean_ext}"
            ext_map[clean_ext] = cat_name
    return ext_map


def get_category_for_file(
    file_path: Path,
    custom_categories: Optional[Dict[str, List[str]]] = None
) -> str:
    """Determines the appropriate category for a given file based on its extension.

    Args:
        file_path: Path object or string of the file.
        custom_categories: Optional dictionary overriding default categories.

    Returns:
        Category name string (e.g. 'Images', 'Documents', or 'Others').
    """
    ext = file_path.suffix.lower()
    ext_map = build_extension_map(custom_categories)
    return ext_map.get(ext, "Others")
