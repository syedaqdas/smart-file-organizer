# Changelog

All notable changes to **Smart File Organizer** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2026-10-23

### Added
- **AI Storage Assistant**: Integrated heuristic intelligence engine analyzing folder health, top space hogs, stale files, and actionable cleanup advice.
- **Premium SaaS Dashboard UI**: Redesigned Streamlit interface with hero header, status badges, modern typography, responsive cards, and custom CSS.
- **Brand Assets**: Custom high-resolution project logo (`assets/logo.png`) and comprehensive UI screenshot suite (`assets/screenshots/`).
- **Open Source Documentation**: Comprehensive `CONTRIBUTING.md`, `LICENSE`, `.gitignore`, and detailed `README.md`.
- **Conflict Protection & Auto-Renaming**: Collision detection that appends incremental counters (e.g. `file (1).ext`) without data loss.
- **One-Click Undo Engine**: Reversible move transactions with audit log and empty directory pruning.

### Changed
- Refactored `scanner.py` with path traversal protections and intelligent internal directory exclusions.
- Optimized Plotly visualization charts with consistent palette and responsive dimensions.
- Enhanced error handling across filesystem operations (`PermissionError`, `OSError`, locked files).

### Fixed
- Fixed directory recursion edge case where pre-existing category folders could be recursively re-nested.
- Handled Windows vs POSIX path normalization across platforms.

---

## [1.0.0] - 2026-10-22

### Added
- Initial release of **Smart File Organizer**.
- Streamlit web interface with real-time directory scanning.
- File categorization for Images, Videos, Documents, Code files, Archives, Audio, and Others.
- Dry-run preview mode before moving files.
- Plotly donut chart and storage bar chart.
- Unit test suite with Pytest.
