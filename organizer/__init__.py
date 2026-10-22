"""Smart File Organizer package.

A modular, robust tool for categorizing, previewing, and organizing messy directories.
"""

from .categories import (
    DEFAULT_CATEGORIES,
    CATEGORY_COLORS,
    CATEGORY_ICONS,
    get_category_for_file,
    build_extension_map,
)
from .scanner import scan_directory, FileInfo, ScanSummary, format_file_size
from .organizer import (
    generate_move_plan,
    execute_move_plan,
    undo_last_moves,
    MovePlanItem,
    OrganizationReport,
)
from .assistant import (
    analyze_storage,
    AssistantAnalysis,
    StorageInsight,
)
from .visualizer import (
    create_distribution_pie_chart,
    create_size_bar_chart,
    create_comparison_chart,
)

__all__ = [
    "DEFAULT_CATEGORIES",
    "CATEGORY_COLORS",
    "CATEGORY_ICONS",
    "get_category_for_file",
    "build_extension_map",
    "scan_directory",
    "FileInfo",
    "ScanSummary",
    "format_file_size",
    "generate_move_plan",
    "execute_move_plan",
    "undo_last_moves",
    "MovePlanItem",
    "OrganizationReport",
    "analyze_storage",
    "AssistantAnalysis",
    "StorageInsight",
    "create_distribution_pie_chart",
    "create_size_bar_chart",
    "create_comparison_chart",
]
