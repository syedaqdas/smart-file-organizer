"""Asset generator for Smart File Organizer.

Generates high-resolution project branding, logo, and realistic screenshot mockups
for GitHub documentation and portfolio presentation.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math
import os


def get_default_font(size: int = 16):
    """Loads a clean system font or falls back to PIL default font."""
    try:
        # Standard clean Windows font
        return ImageFont.truetype("arial.ttf", size)
    except IOError:
        try:
            return ImageFont.truetype("segoeui.ttf", size)
        except IOError:
            return ImageFont.load_default()


def get_bold_font(size: int = 16):
    """Loads a bold system font or falls back to standard."""
    try:
        return ImageFont.truetype("arialbd.ttf", size)
    except IOError:
        try:
            return ImageFont.truetype("segoeuib.ttf", size)
        except IOError:
            return get_default_font(size)


def create_project_logo(output_path: Path):
    """Generates a professional 512x512 application logo."""
    size = (512, 512)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Background rounded container with modern vibrant gradient effect
    # Dark slate / Indigo gradient background
    draw.rounded_rectangle([(16, 16), (496, 496)], radius=96, fill="#0F172A")

    # Subtle inner border
    draw.rounded_rectangle([(18, 18), (494, 494)], radius=94, outline="#334155", width=3)

    # Gradient-like ambient glow circle in top-right
    for r in range(160, 40, -10):
        alpha = int(35 * (1 - r / 160))
        draw.ellipse([(340 - r, 140 - r), (340 + r, 140 + r)], fill=(99, 102, 241, alpha))

    # 2. Main Folder Icon Graphic
    # Folder Back Tab
    draw.rounded_rectangle([(110, 150), (230, 210)], radius=18, fill="#4F46E5")
    # Folder Body
    draw.rounded_rectangle([(110, 180), (402, 360)], radius=26, fill="#3B82F6")
    # Folder Front Slant flap
    draw.rounded_rectangle([(110, 225), (402, 360)], radius=24, fill="#2563EB")

    # 3. Dynamic Energy Spark / Lightning in center
    spark_points = [
        (265, 230),
        (235, 290),
        (255, 290),
        (240, 345),
        (285, 280),
        (262, 280),
    ]
    draw.polygon(spark_points, fill="#FACC15")

    # Little spark accents
    draw.ellipse([(330, 245), (342, 257)], fill="#FDE047")
    draw.ellipse([(175, 305), (185, 315)], fill="#60A5FA")

    # 4. Text Label at bottom: "SMART FILE ORGANIZER"
    font_bold = get_bold_font(24)
    font_sub = get_default_font(16)

    title = "SMART FILE ORGANIZER"
    draw.text((256, 400), title, fill="#FFFFFF", font=font_bold, anchor="mm")

    tagline = "AUTOMATED INTELLIGENT WORKSPACE"
    draw.text((256, 432), tagline, fill="#94A3B8", font=font_sub, anchor="mm")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, "PNG")


def _draw_mock_browser_frame(draw, width, height, title="Smart File Organizer - Dashboard"):
    """Draws a modern SaaS window / browser header with traffic lights."""
    # Base background
    draw.rectangle([(0, 0), (width, height)], fill="#F8FAFC")

    # Top Navigation Bar
    draw.rectangle([(0, 0), (width, 54)], fill="#0F172A")

    # Traffic light circles
    draw.ellipse([(20, 20), (32, 32)], fill="#EF4444")
    draw.ellipse([(40, 20), (52, 52)], fill="#F59E0B")
    draw.ellipse([(60, 20), (72, 32)], fill="#10B981")

    # URL / Title Bar
    draw.rounded_rectangle([(100, 12), (width - 120, 42)], radius=8, fill="#1E293B")
    font = get_default_font(13)
    draw.text((120, 20), f"🔒 localhost:8501 — {title}", fill="#94A3B8", font=font)


def _draw_mock_sidebar(draw, height):
    """Draws the Streamlit sidebar on the left."""
    draw.rectangle([(0, 54), (280, height)], fill="#1E293B")

    # Logo / Header in sidebar
    font_brand = get_bold_font(18)
    draw.text((24, 80), "📁 File Organizer", fill="#FFFFFF", font=font_brand)

    font_muted = get_default_font(12)
    draw.text((24, 106), "Smart Workspace Suite", fill="#94A3B8", font=font_muted)

    # Sidebar inputs
    draw.text((24, 145), "TARGET DIRECTORY", fill="#64748B", font=get_bold_font(11))
    draw.rounded_rectangle([(24, 165), (256, 205)], radius=6, fill="#0F172A", outline="#334155")
    draw.text((36, 178), "C:/Users/Alex/Downloads", fill="#E2E8F0", font=font_muted)

    # Preset location buttons
    draw.rounded_rectangle([(24, 220), (135, 252)], radius=6, fill="#334155")
    draw.text((44, 228), "📥 Downloads", fill="#FFFFFF", font=font_muted)

    draw.rounded_rectangle([(145, 220), (256, 252)], radius=6, fill="#334155")
    draw.text((165, 228), "🖥️ Desktop", fill="#FFFFFF", font=font_muted)

    # Scan button
    draw.rounded_rectangle([(24, 275), (256, 320)], radius=8, fill="#2563EB")
    draw.text((80, 288), "🔍 Scan Folder", fill="#FFFFFF", font=get_bold_font(14))

    # Demo sandbox button
    draw.rounded_rectangle([(24, 335), (256, 375)], radius=8, fill="#475569")
    draw.text((45, 347), "✨ Create Messy Demo", fill="#FFFFFF", font=font_muted)


def create_dashboard_screenshot(output_path: Path):
    """Generates the main dashboard screenshot."""
    w, h = 1200, 720
    img = Image.new("RGBA", (w, h), "#F8FAFC")
    draw = ImageDraw.Draw(img)

    _draw_mock_browser_frame(draw, w, h, "Dashboard & Analytics")
    _draw_mock_sidebar(draw, h)

    font_title = get_bold_font(28)
    font_sub = get_default_font(15)
    font_card_num = get_bold_font(26)
    font_card_lbl = get_bold_font(12)

    # Main Area Content
    draw.text((320, 80), "📂 Smart File Organizer", fill="#0F172A", font=font_title)
    draw.text((320, 118), "Automated categorization, duplicate conflict prevention, and storage analytics.", fill="#64748B", font=font_sub)

    # 4 Metric Cards
    cards = [
        ("DISCOVERED FILES", "248", "#2563EB", 320),
        ("TOTAL STORAGE", "4.82 GB", "#10B981", 535),
        ("CATEGORIES DETECTED", "6 Types", "#8B5CF6", 750),
        ("CONFLICTS RESOLVED", "14 Files", "#F59E0B", 965),
    ]

    for lbl, val, color, x in cards:
        draw.rounded_rectangle([(x, 155), (x + 195, 245)], radius=12, fill="#FFFFFF", outline="#E2E8F0", width=1)
        draw.rounded_rectangle([(x, 155), (x + 195, 159)], radius=2, fill=color)
        draw.text((x + 20, 175), lbl, fill="#64748B", font=font_card_lbl)
        draw.text((x + 20, 198), val, fill="#0F172A", font=font_card_num)

    # Donut Chart Mockup (Left)
    draw.rounded_rectangle([(320, 270), (730, 670)], radius=14, fill="#FFFFFF", outline="#E2E8F0")
    draw.text((345, 290), "File Distribution by Category", fill="#1E293B", font=get_bold_font(16))

    # Outer circle & donut segments
    center = (525, 470)
    draw.ellipse([(center[0] - 120, center[1] - 120), (center[0] + 120, center[1] + 120)], fill="#3B82F6")
    draw.pieslice([(center[0] - 120, center[1] - 120), (center[0] + 120, center[1] + 120)], start=0, end=110, fill="#10B981")
    draw.pieslice([(center[0] - 120, center[1] - 120), (center[0] + 120, center[1] + 120)], start=110, end=190, fill="#EC4899")
    draw.pieslice([(center[0] - 120, center[1] - 120), (center[0] + 120, center[1] + 120)], start=190, end=260, fill="#8B5CF6")
    draw.pieslice([(center[0] - 120, center[1] - 120), (center[0] + 120, center[1] + 120)], start=260, end=310, fill="#F59E0B")
    # Inner cutout for donut
    draw.ellipse([(center[0] - 70, center[1] - 70), (center[0] + 70, center[1] + 70)], fill="#FFFFFF")
    draw.text((center[0], center[1] - 10), "248", fill="#0F172A", font=get_bold_font(24), anchor="mm")
    draw.text((center[0], center[1] + 16), "Total Files", fill="#64748B", font=get_default_font(12), anchor="mm")

    # Storage Bar Chart Mockup (Right)
    draw.rounded_rectangle([(755, 270), (1160, 670)], radius=14, fill="#FFFFFF", outline="#E2E8F0")
    draw.text((780, 290), "Storage Consumption by Category", fill="#1E293B", font=get_bold_font(16))

    bars = [
        ("🎬 Videos", "2.65 GB", 260, "#EC4899"),
        ("🖼️ Images", "1.10 GB", 170, "#3B82F6"),
        ("📄 Documents", "640 MB", 110, "#10B981"),
        ("📦 Archives", "380 MB", 75, "#F59E0B"),
        ("💻 Code files", "52 MB", 30, "#8B5CF6"),
    ]

    by = 350
    for label, size_lbl, b_len, col in bars:
        draw.text((780, by), label, fill="#334155", font=get_bold_font(13))
        draw.rounded_rectangle([(780, by + 22), (780 + b_len, by + 44)], radius=6, fill=col)
        draw.text((790 + b_len, by + 25), size_lbl, fill="#64748B", font=get_default_font(12))
        by += 60

    img.save(output_path, "PNG")


def create_file_scan_screenshot(output_path: Path):
    """Generates the file scan table screenshot."""
    w, h = 1200, 720
    img = Image.new("RGBA", (w, h), "#F8FAFC")
    draw = ImageDraw.Draw(img)

    _draw_mock_browser_frame(draw, w, h, "Discovered Files")
    _draw_mock_sidebar(draw, h)

    draw.text((320, 80), "Discovered Files & Categorization", fill="#0F172A", font=get_bold_font(24))
    draw.text((320, 115), "Instant categorization based on file signature and extension mapping.", fill="#64748B", font=get_default_font(14))

    # Search & Filter bar
    draw.rounded_rectangle([(320, 150), (620, 185)], radius=6, fill="#FFFFFF", outline="#CBD5E1")
    draw.text((335, 160), "🔍 Search filename...", fill="#94A3B8", font=get_default_font(13))

    draw.rounded_rectangle([(640, 150), (800, 185)], radius=6, fill="#FFFFFF", outline="#CBD5E1")
    draw.text((655, 160), "Category: All ▾", fill="#334155", font=get_default_font(13))

    # Table Container
    draw.rounded_rectangle([(320, 205), (1160, 680)], radius=10, fill="#FFFFFF", outline="#E2E8F0")

    # Table Header
    draw.rectangle([(321, 206), (1159, 245)], fill="#F1F5F9")
    headers = [
        ("FILE NAME", 340),
        ("CATEGORY", 640),
        ("TARGET FOLDER", 780),
        ("SIZE", 940),
        ("EXTENSION", 1050),
    ]
    for h_text, hx in headers:
        draw.text((hx, 218), h_text, fill="#475569", font=get_bold_font(11))

    # Table Rows
    rows = [
        ("vacation_sunset.jpg", "🖼️ Images", "Images/", "2.4 MB", ".jpg", "#EFF6FF", "#1D4ED8"),
        ("quarterly_report.pdf", "📄 Documents", "Documents/", "840 KB", ".pdf", "#ECFDF5", "#047857"),
        ("screen_recording.mp4", "🎬 Videos", "Videos/", "145.2 MB", ".mp4", "#FDF2F8", "#BE185D"),
        ("backend_server.py", "💻 Code files", "Code files/", "12 KB", ".py", "#F5F3FF", "#6D28D9"),
        ("client_assets.zip", "📦 Archives", "Archives/", "88.6 MB", ".zip", "#FFFBEB", "#B45309"),
        ("podcast_interview.mp3", "🎵 Audio", "Audio/", "34.1 MB", ".mp3", "#ECFEFF", "#0E7490"),
        ("firmware_patch.bin", "📁 Others", "Others/", "4.2 MB", ".bin", "#F3F4F6", "#374151"),
    ]

    ry = 255
    for name, cat, fld, sz, ext, badge_bg, badge_fg in rows:
        draw.line([(321, ry), (1159, ry)], fill="#F1F5F9", width=1)
        draw.text((340, ry + 12), name, fill="#1E293B", font=get_default_font(13))

        # Category Badge
        draw.rounded_rectangle([(640, ry + 8), (750, ry + 32)], radius=6, fill=badge_bg)
        draw.text((648, ry + 12), cat, fill=badge_fg, font=get_bold_font(11))

        draw.text((780, ry + 12), fld, fill="#475569", font=get_default_font(13))
        draw.text((940, ry + 12), sz, fill="#0F172A", font=get_bold_font(12))
        draw.text((1050, ry + 12), ext, fill="#64748B", font=get_default_font(12))
        ry += 48

    img.save(output_path, "PNG")


def create_analytics_screenshot(output_path: Path):
    """Generates the analytics and AI assistant screenshot."""
    w, h = 1200, 720
    img = Image.new("RGBA", (w, h), "#F8FAFC")
    draw = ImageDraw.Draw(img)

    _draw_mock_browser_frame(draw, w, h, "AI Storage Assistant & Analytics")
    _draw_mock_sidebar(draw, h)

    draw.text((320, 80), "🧠 AI Storage Assistant & Insights", fill="#0F172A", font=get_bold_font(24))
    draw.text((320, 115), "Automated storage heuristics, space-hog detection, and cleanup recommendations.", fill="#64748B", font=get_default_font(14))

    # AI Recommendation Cards
    insights = [
        ("🎬 Heavy Video Storage Concentration", "Videos occupy 55.4% (2.65 GB) of total space. Consider moving high-res media to cloud storage.", "#EC4899", "High Impact"),
        ("⏳ 28 Stale Files Detected (> 90 Days)", "Found 28 files totaling 620 MB that have not been modified recently. Archiving them clears clutter.", "#F59E0B", "Medium Impact"),
        ("🛡️ Duplicate Filename Groups Protected", "3 duplicate filename clashes detected across subfolders. Collision resolution will auto-suffix them.", "#10B981", "Safe Guard"),
    ]

    iy = 160
    for title, desc, tag_col, tag_text in insights:
        draw.rounded_rectangle([(320, iy), (1160, iy + 85)], radius=10, fill="#FFFFFF", outline="#E2E8F0")
        draw.rounded_rectangle([(320, iy), (328, iy + 85)], radius=2, fill=tag_col)

        draw.text((350, iy + 16), title, fill="#0F172A", font=get_bold_font(15))
        draw.text((350, iy + 45), desc, fill="#64748B", font=get_default_font(13))

        # Tag
        draw.rounded_rectangle([(1040, iy + 18), (1140, iy + 42)], radius=6, fill="#F1F5F9")
        draw.text((1050, iy + 22), tag_text, fill=tag_col, font=get_bold_font(10))
        iy += 105

    # Top Space Hogs Section
    draw.text((320, 490), "Top Storage Consumers (Space Hogs)", fill="#1E293B", font=get_bold_font(18))

    draw.rounded_rectangle([(320, 525), (1160, 680)], radius=10, fill="#FFFFFF", outline="#E2E8F0")
    hogs = [
        ("1", "raw_client_presentation_recording.mp4", "1.45 GB", "Videos", "#EC4899"),
        ("2", "quarterly_full_archive_backup.zip", "820 MB", "Archives", "#F59E0B"),
        ("3", "raw_photo_session_bundle.tar.gz", "450 MB", "Archives", "#F59E0B"),
    ]

    hy = 540
    for rank, name, sz, cat, col in hogs:
        draw.rounded_rectangle([(340, hy), (365, hy + 25)], radius=12, fill="#E2E8F0")
        draw.text((348, hy + 4), rank, fill="#1E293B", font=get_bold_font(12))
        draw.text((380, hy + 4), name, fill="#1E293B", font=get_bold_font(13))
        draw.text((950, hy + 4), cat, fill=col, font=get_bold_font(12))
        draw.text((1080, hy + 4), sz, fill="#0F172A", font=get_bold_font(13))
        hy += 42

    img.save(output_path, "PNG")


def create_preview_screenshot(output_path: Path):
    """Generates the preview / dry run mode screenshot."""
    w, h = 1200, 720
    img = Image.new("RGBA", (w, h), "#F8FAFC")
    draw = ImageDraw.Draw(img)

    _draw_mock_browser_frame(draw, w, h, "Preview Mode (Dry Run)")
    _draw_mock_sidebar(draw, h)

    draw.text((320, 80), "👁️ Preview Mode (Dry Run)", fill="#0F172A", font=get_bold_font(24))
    draw.text((320, 115), "Verify exact source ➔ destination movement paths before applying changes.", fill="#64748B", font=get_default_font(14))

    # Conflict warning banner
    draw.rounded_rectangle([(320, 150), (1160, 205)], radius=8, fill="#FEF3C7", outline="#FDE68A")
    draw.text((340, 162), "🛡️ Conflict Protection Active", fill="#92400E", font=get_bold_font(14))
    draw.text((340, 184), "2 duplicate files detected. They will be safely auto-renamed (e.g. filename (1).ext) to avoid overwriting.", fill="#B45309", font=get_default_font(12))

    # Preview Plan Table
    draw.rounded_rectangle([(320, 225), (1160, 675)], radius=10, fill="#FFFFFF", outline="#E2E8F0")

    draw.rectangle([(321, 226), (1159, 265)], fill="#F8FAFC")
    draw.text((340, 238), "ORIGINAL FILE", fill="#64748B", font=get_bold_font(11))
    draw.text((600, 238), "CATEGORY", fill="#64748B", font=get_bold_font(11))
    draw.text((750, 238), "ACTION", fill="#64748B", font=get_bold_font(11))
    draw.text((920, 238), "TARGET DESTINATION", fill="#64748B", font=get_bold_font(11))

    preview_rows = [
        ("vacation_sunset.jpg", "Images", "Move", "Images/vacation_sunset.jpg", "#2563EB", False),
        ("vacation_sunset.jpg", "Images", "Rename & Move (Conflict)", "Images/vacation_sunset (1).jpg", "#D97706", True),
        ("report_draft.docx", "Documents", "Move", "Documents/report_draft.docx", "#2563EB", False),
        ("report_draft.docx", "Documents", "Rename & Move (Conflict)", "Documents/report_draft (1).docx", "#D97706", True),
        ("analysis.py", "Code files", "Move", "Code files/analysis.py", "#2563EB", False),
        ("project_bundle.zip", "Archives", "Move", "Archives/project_bundle.zip", "#2563EB", False),
    ]

    py = 280
    for orig, cat, act, target, col, is_conflict in preview_rows:
        draw.line([(321, py), (1159, py)], fill="#F1F5F9", width=1)
        draw.text((340, py + 14), orig, fill="#1E293B", font=get_bold_font(13))
        draw.text((600, py + 14), cat, fill="#64748B", font=get_default_font(13))

        # Action pill
        pill_bg = "#FEF3C7" if is_conflict else "#EFF6FF"
        draw.rounded_rectangle([(750, py + 8), (900, py + 34)], radius=6, fill=pill_bg)
        draw.text((758, py + 12), act, fill=col, font=get_bold_font(11))

        draw.text((920, py + 14), target, fill="#0F172A", font=get_default_font(13))
        py += 52

    img.save(output_path, "PNG")


def create_organized_result_screenshot(output_path: Path):
    """Generates the execution result & undo screenshot."""
    w, h = 1200, 720
    img = Image.new("RGBA", (w, h), "#F8FAFC")
    draw = ImageDraw.Draw(img)

    _draw_mock_browser_frame(draw, w, h, "Organization Execution & Audit Log")
    _draw_mock_sidebar(draw, h)

    draw.text((320, 80), "🎉 Organization Completed Successfully!", fill="#0F172A", font=get_bold_font(24))
    draw.text((320, 115), "All files relocated safely into category directories with zero data loss.", fill="#64748B", font=get_default_font(14))

    # Success Banner with Undo Button
    draw.rounded_rectangle([(320, 150), (1160, 220)], radius=10, fill="#ECFDF5", outline="#A7F3D0")
    draw.text((345, 172), "✅ 248 Files Organized Successfully | 0 Errors | 14 Renamed Safe", fill="#065F46", font=get_bold_font(15))
    draw.text((345, 195), "Audit manifest logged. You can click 'Undo All Moves' anytime to restore files to initial state.", fill="#047857", font=get_default_font(12))

    draw.rounded_rectangle([(980, 165), (1135, 205)], radius=8, fill="#10B981")
    draw.text((1005, 178), "⏪ Undo Moves", fill="#FFFFFF", font=get_bold_font(13))

    # Execution Audit Log Table
    draw.rounded_rectangle([(320, 240), (1160, 680)], radius=10, fill="#FFFFFF", outline="#E2E8F0")
    draw.rectangle([(321, 241), (1159, 280)], fill="#F8FAFC")
    draw.text((340, 253), "TIMESTAMP", fill="#64748B", font=get_bold_font(11))
    draw.text((450, 253), "FILE", fill="#64748B", font=get_bold_font(11))
    draw.text((700, 253), "STATUS", fill="#64748B", font=get_bold_font(11))
    draw.text((820, 253), "DESTINATION & REMARKS", fill="#64748B", font=get_bold_font(11))

    log_rows = [
        ("01:40:12", "vacation_sunset.jpg", "Success", "Moved to Images/vacation_sunset.jpg"),
        ("01:40:12", "vacation_sunset.jpg", "Success", "Moved to Images/vacation_sunset (1).jpg (Conflict protected)"),
        ("01:40:13", "financial_plan_q3.xlsx", "Success", "Moved to Documents/financial_plan_q3.xlsx"),
        ("01:40:13", "demo_recording.mp4", "Success", "Moved to Videos/demo_recording.mp4"),
        ("01:40:14", "core_engine.py", "Success", "Moved to Code files/core_engine.py"),
        ("01:40:14", "desktop.ini", "Skipped", "Protected system file skipped"),
        ("01:40:15", "archive_backup.rar", "Success", "Moved to Archives/archive_backup.rar"),
    ]

    ly = 295
    for ts, fn, st_lbl, rem in log_rows:
        draw.line([(321, ly), (1159, ly)], fill="#F1F5F9", width=1)
        draw.text((340, ly + 12), ts, fill="#64748B", font=get_default_font(12))
        draw.text((450, ly + 12), fn, fill="#1E293B", font=get_bold_font(13))

        st_col = "#10B981" if st_lbl == "Success" else "#64748B"
        draw.text((700, ly + 12), f"● {st_lbl}", fill=st_col, font=get_bold_font(12))

        draw.text((820, ly + 12), rem, fill="#334155", font=get_default_font(12))
        ly += 48

    img.save(output_path, "PNG")


def generate_all_assets():
    """Generates logo, screenshots, and sets up asset directories."""
    base_dir = Path(__file__).resolve().parent.parent
    assets_dir = base_dir / "assets"
    screenshots_dir = assets_dir / "screenshots"
    demo_dir = assets_dir / "demo"

    assets_dir.mkdir(parents=True, exist_ok=True)
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    demo_dir.mkdir(parents=True, exist_ok=True)

    print("Generating project logo...")
    create_project_logo(assets_dir / "logo.png")

    print("Generating screenshot mockups...")
    create_dashboard_screenshot(screenshots_dir / "dashboard.png")
    create_file_scan_screenshot(screenshots_dir / "file_scan.png")
    create_analytics_screenshot(screenshots_dir / "analytics.png")
    create_preview_screenshot(screenshots_dir / "preview_mode.png")
    create_organized_result_screenshot(screenshots_dir / "organized_result.png")

    print(f"All assets successfully created under {assets_dir}")


if __name__ == "__main__":
    generate_all_assets()
