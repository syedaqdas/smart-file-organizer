"""Smart File Organizer - Premium Streamlit Web Application.

A modern, robust desktop/web tool that automatically scans, categorizes,
previews, and organizes messy folders with Plotly analytics, conflict resolution,
and an intelligent AI Storage Assistant.
"""

from pathlib import Path
from typing import Dict, List, Optional
import os
import pandas as pd
import streamlit as st

from organizer.categories import (
    DEFAULT_CATEGORIES,
    CATEGORY_COLORS,
    CATEGORY_ICONS,
)
from organizer.scanner import scan_directory, ScanSummary
from organizer.organizer import (
    generate_move_plan,
    execute_move_plan,
    undo_last_moves,
    OrganizationReport,
)
from organizer.assistant import (
    analyze_storage,
    AssistantAnalysis,
)
from organizer.visualizer import (
    create_distribution_pie_chart,
    create_size_bar_chart,
    create_comparison_chart,
)
from utils.demo_data import create_demo_messy_folder


# ------------------------------------------------------------------------------
# Streamlit Page Configuration & Styling
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Smart File Organizer | SaaS Edition",
    page_icon="assets/logo.png" if Path("assets/logo.png").exists() else "📁",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
    /* Global layout & typography refinement */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .hero-container {
        display: flex;
        align-items: center;
        gap: 20px;
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        padding: 24px 28px;
        border-radius: 16px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(15, 23, 42, 0.15);
        color: #FFFFFF;
    }

    .hero-title {
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin: 0;
        color: #F8FAFC;
    }

    .hero-subtitle {
        font-size: 0.95rem;
        color: #94A3B8;
        margin-top: 4px;
        margin-bottom: 0;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.15);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 9999px;
        padding: 4px 12px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.06);
    }

    .metric-title {
        font-size: 0.8rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }

    .metric-val {
        font-size: 1.85rem;
        font-weight: 700;
        color: #0F172A;
        margin-top: 6px;
    }

    .insight-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #3B82F6;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }

    .insight-card.warning { border-left-color: #F59E0B; }
    .insight-card.cleanup { border-left-color: #EC4899; }
    .insight-card.tip { border-left-color: #10B981; }

    .insight-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-weight: 600;
        font-size: 1rem;
        color: #1E293B;
        margin-bottom: 4px;
    }

    .insight-desc {
        font-size: 0.88rem;
        color: #475569;
        line-height: 1.5;
        margin: 0;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        border-bottom: 1px solid #E2E8F0;
        padding-bottom: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        font-weight: 600;
        font-size: 0.92rem;
        border-radius: 8px;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# Session State Initialization
# ------------------------------------------------------------------------------
if "scan_summary" not in st.session_state:
    st.session_state.scan_summary = None
if "move_plan" not in st.session_state:
    st.session_state.move_plan = None
if "last_report" not in st.session_state:
    st.session_state.last_report = None
if "undo_records" not in st.session_state:
    st.session_state.undo_records = []
if "target_folder" not in st.session_state:
    st.session_state.target_folder = str(Path.cwd())
if "category_rules" not in st.session_state:
    st.session_state.category_rules = {k: list(v) for k, v in DEFAULT_CATEGORIES.items()}
if "folder_names" not in st.session_state:
    st.session_state.folder_names = {k: k for k in list(DEFAULT_CATEGORIES.keys()) + ["Others"]}


# ------------------------------------------------------------------------------
# Sidebar Controls & Navigation
# ------------------------------------------------------------------------------
with st.sidebar:
    logo_path = Path("assets/logo.png")
    if logo_path.exists():
        st.image(str(logo_path), width=110)
    else:
        st.markdown("### 📁 Smart File Organizer")

    st.markdown("#### ⚡ Workspace Control")
    st.caption("Scan, categorize, and organize directories with enterprise safety.")

    st.markdown("---")
    st.subheader("1. Select Directory")

    folder_input = st.text_input(
        "Target Folder Path",
        value=st.session_state.target_folder,
        help="Paste or enter the absolute path to the directory you want to organize.",
    )
    st.session_state.target_folder = folder_input

    # Quick preset selection shortcuts
    st.markdown("**Quick Shortcuts:**")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        if st.button("📥 Downloads", use_container_width=True):
            downloads = Path.home() / "Downloads"
            if downloads.exists():
                st.session_state.target_folder = str(downloads)
                st.rerun()
        if st.button("📑 Documents", use_container_width=True):
            docs = Path.home() / "Documents"
            if docs.exists():
                st.session_state.target_folder = str(docs)
                st.rerun()
    with col_p2:
        if st.button("🖥️ Desktop", use_container_width=True):
            desktop = Path.home() / "Desktop"
            if desktop.exists():
                st.session_state.target_folder = str(desktop)
                st.rerun()
        if st.button("📍 Current Dir", use_container_width=True):
            st.session_state.target_folder = str(Path.cwd())
            st.rerun()

    # Instant Demo Sandbox Generator
    st.markdown("---")
    st.markdown("**🧪 Instant Sandbox Environment:**")
    if st.button("✨ Create Messy Demo Folder", use_container_width=True, type="secondary"):
        with st.spinner("Generating sandbox files..."):
            demo_path = Path.cwd() / "demo_messy_folder"
            create_demo_messy_folder(demo_path)
            st.session_state.target_folder = str(demo_path)
            st.session_state.scan_summary = scan_directory(
                demo_path,
                recursive=False,
                skip_hidden=True,
                custom_categories=st.session_state.category_rules,
                category_folder_names=st.session_state.folder_names,
            )
            st.session_state.move_plan = generate_move_plan(
                st.session_state.scan_summary,
                category_folder_names=st.session_state.folder_names,
            )
            st.success("Sandbox populated and scanned automatically!")
            st.rerun()

    st.markdown("---")
    st.subheader("2. Scan Filters")
    recursive_scan = st.checkbox(
        "Scan Subdirectories (Recursive)",
        value=False,
        help="If enabled, files in nested subfolders will also be collected and categorized.",
    )
    skip_hidden_files = st.checkbox(
        "Skip Hidden & System Files",
        value=True,
        help="Ignore dotfiles (.git, .DS_Store), desktop.ini, and OS artifacts.",
    )

    st.markdown("---")
    scan_clicked = st.button("🔍 Scan Directory", use_container_width=True, type="primary")

    if scan_clicked:
        if not st.session_state.target_folder.strip():
            st.error("Please enter a valid folder path.")
        else:
            with st.spinner("Analyzing target directory..."):
                summary = scan_directory(
                    st.session_state.target_folder,
                    recursive=recursive_scan,
                    skip_hidden=skip_hidden_files,
                    custom_categories=st.session_state.category_rules,
                    category_folder_names=st.session_state.folder_names,
                )
                st.session_state.scan_summary = summary
                st.session_state.move_plan = generate_move_plan(
                    summary,
                    category_folder_names=st.session_state.folder_names,
                )
                st.rerun()

    st.markdown("---")
    st.caption("🔒 Conflict Protection Active | v1.1.0")


# ------------------------------------------------------------------------------
# Hero Landing Header
# ------------------------------------------------------------------------------
hero_html = f"""
<div class="hero-container">
    <div style="flex: 1;">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 6px;">
            <h1 class="hero-title">Smart File Organizer</h1>
            <span class="status-pill">● Conflict Protected</span>
            <span style="background: rgba(255,255,255,0.1); padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 600;">v1.1.0</span>
        </div>
        <p class="hero-subtitle">Automated intelligent file categorization, duplicate collision prevention, and storage analytics.</p>
    </div>
</div>
"""
st.markdown(hero_html, unsafe_allow_html=True)

summary: Optional[ScanSummary] = st.session_state.scan_summary

# ------------------------------------------------------------------------------
# Main Application Tabs
# ------------------------------------------------------------------------------
tab_overview, tab_assistant, tab_preview, tab_organize, tab_undo, tab_settings = st.tabs([
    "📊 Scan & Analytics",
    "🧠 AI Storage Assistant",
    "👁️ Preview (Dry Run)",
    "🚀 Organize Files",
    "⏪ Undo & Rollback",
    "⚙️ Rules & Settings",
])


# ==============================================================================
# TAB 1: Scan & Analytics
# ==============================================================================
with tab_overview:
    if not summary:
        st.info("👋 Select a folder path on the sidebar and click **'🔍 Scan Directory'** (or test instantly with **'✨ Create Messy Demo Folder'**).")
    elif summary.errors:
        for err in summary.errors:
            st.error(f"⚠️ {err}")
    else:
        st.markdown(f"**Target Directory:** `{summary.folder_path}`")

        # Metric Cards Row
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(
                f'<div class="metric-card"><div class="metric-title">Discovered Files</div><div class="metric-val">{summary.total_files}</div></div>',
                unsafe_allow_html=True,
            )
        with m2:
            st.markdown(
                f'<div class="metric-card"><div class="metric-title">Total Size</div><div class="metric-val">{summary.total_size_formatted}</div></div>',
                unsafe_allow_html=True,
            )
        with m3:
            active_cats = sum(1 for c in summary.category_counts.values() if c > 0)
            st.markdown(
                f'<div class="metric-card"><div class="metric-title">Categories Found</div><div class="metric-val">{active_cats}</div></div>',
                unsafe_allow_html=True,
            )
        with m4:
            plan = st.session_state.move_plan or []
            collisions = sum(1 for p in plan if p.is_collision_renamed)
            st.markdown(
                f'<div class="metric-card"><div class="metric-title">Conflicts Resolved</div><div class="metric-val">{collisions}</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Plotly Charts
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            donut_fig = create_distribution_pie_chart(summary.category_counts)
            st.plotly_chart(donut_fig, use_container_width=True)

        with col_c2:
            bar_fig = create_size_bar_chart(summary.category_sizes)
            st.plotly_chart(bar_fig, use_container_width=True)

        # Discovered Files Table
        st.subheader("Discovered Files")
        df_records = summary.to_dict_list()
        if df_records:
            df = pd.DataFrame(df_records)

            c_filter1, c_filter2 = st.columns([1, 2])
            with c_filter1:
                all_found_cats = ["All"] + sorted(list({r["Category"] for r in df_records}))
                selected_cat = st.selectbox("Filter by Category", all_found_cats)
            with c_filter2:
                search_query = st.text_input("Search filename", placeholder="Type to filter...")

            filtered_df = df
            if selected_cat != "All":
                filtered_df = filtered_df[filtered_df["Category"] == selected_cat]
            if search_query.strip():
                filtered_df = filtered_df[filtered_df["Name"].str.contains(search_query.strip(), case=False, na=False)]

            st.dataframe(
                filtered_df[["Name", "Category", "Target Folder", "Size", "Extension", "Modified"]],
                use_container_width=True,
                height=320,
            )
        else:
            st.warning("No files discovered matching filter criteria in this folder.")


# ==============================================================================
# TAB 2: AI Storage Assistant (Optional Feature)
# ==============================================================================
with tab_assistant:
    st.subheader("🧠 AI Storage Assistant")
    st.write(
        "Heuristic storage intelligence that identifies space hogs, stale assets, "
        "and duplicate name clashes to recommend actionable optimizations."
    )

    if not summary or summary.total_files == 0:
        st.info("Scan a folder to receive personalized AI storage and organization insights.")
    else:
        # Run assistant analysis
        analysis: AssistantAnalysis = analyze_storage(summary, stale_days_threshold=90)

        st.markdown(
            f"""
            <div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 10px; padding: 14px 18px; margin-bottom: 20px;">
                <span style="font-weight: 600; color: #1E40AF;">💡 Executive Summary:</span>
                <span style="color: #1E3A8A; margin-left: 6px;">{analysis.summary_headline}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("#### Actionable Recommendations")
        for ins in analysis.insights:
            saving_badge = f"<span style='background:#DCFCE7; color:#15803D; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:600;'>Save ~{ins.potential_savings}</span>" if ins.potential_savings else ""
            impact_badge = f"<span style='background:#F1F5F9; color:#475569; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:600;'>Impact: {ins.impact}</span>"
            card_html = f"""
            <div class="insight-card {ins.type}">
                <div class="insight-header">
                    <span>{ins.icon} {ins.title}</span>
                    <div style="display:flex; gap:6px;">{saving_badge} {impact_badge}</div>
                </div>
                <p class="insight-desc">{ins.description}</p>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)

        st.markdown("---")

        # Largest Files Space Hogs
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            st.markdown("#### 🐘 Top Space Hogs")
            if analysis.largest_files:
                hog_data = [
                    {
                        "Filename": f.name,
                        "Category": f"{CATEGORY_ICONS.get(f.category, '📁')} {f.category}",
                        "Size": f.size_formatted,
                    }
                    for f in analysis.largest_files
                ]
                st.dataframe(pd.DataFrame(hog_data), use_container_width=True, height=220)
            else:
                st.caption("No large files detected.")

        with col_h2:
            st.markdown("#### ⏳ Stale Files (> 90 Days Old)")
            if analysis.stale_files:
                stale_data = [
                    {
                        "Filename": f.name,
                        "Category": f.category,
                        "Size": f.size_formatted,
                        "Last Modified": f.modified_formatted,
                    }
                    for f in analysis.stale_files[:10]
                ]
                st.dataframe(pd.DataFrame(stale_data), use_container_width=True, height=220)
                if len(analysis.stale_files) > 10:
                    st.caption(f"Showing 10 of {len(analysis.stale_files)} total stale files.")
            else:
                st.caption("All files were updated recently within the last 90 days.")


# ==============================================================================
# TAB 3: Preview Mode (Dry Run)
# ==============================================================================
with tab_preview:
    st.subheader("👁️ Preview Mode (Dry Run)")
    st.write(
        "Inspect exact source ➔ destination movement paths **before** committing changes to disk. "
        "Identical filenames will automatically be renamed to avoid overwriting existing data."
    )

    plan = st.session_state.move_plan

    if not plan:
        st.info("Please scan a folder in the sidebar to generate a preview movement plan.")
    else:
        collision_count = sum(1 for item in plan if item.is_collision_renamed)
        if collision_count > 0:
            st.warning(
                f"🛡️ **Conflict Protection Alert:** {collision_count} file(s) collide with existing target files. "
                "They will be safely renamed (e.g. `filename (1).ext`) without loss of data."
            )

        preview_data = []
        for item in plan:
            preview_data.append({
                "Original File": item.file_info.name,
                "Category": f"{CATEGORY_ICONS.get(item.category, '📁')} {item.category}",
                "Source Directory": str(item.source_path.parent.name or item.source_path.parent),
                "Destination Folder": item.target_folder_name,
                "Action": item.display_status,
                "Target Filename": item.destination_path.name,
                "Size": item.file_info.size_formatted,
            })

        preview_df = pd.DataFrame(preview_data)
        st.dataframe(preview_df, use_container_width=True, height=380)

        if st.button("🧪 Simulate Execution (Zero Disk Writes)", type="secondary"):
            sim_report = execute_move_plan(plan, dry_run=True)
            st.session_state.last_report = sim_report
            st.success(
                f"Simulation complete: {sim_report.total_moved} operations simulated with 0 errors and zero disk modifications."
            )


# ==============================================================================
# TAB 4: Organize Files
# ==============================================================================
with tab_organize:
    st.subheader("🚀 Organize Files")

    plan = st.session_state.move_plan

    if not plan:
        st.info("Please scan a folder first to generate an execution plan.")
    else:
        st.write(f"Ready to organize **{len(plan)}** files inside `{st.session_state.target_folder}`.")

        st.markdown(
            """
            > **Enterprise Safety Guarantees:**
            > - Automatic folder creation for each category.
            > - Zero data loss: Collision handling resolves duplicate filenames automatically.
            > - One-click undo rollback supported for every executed transaction.
            """
        )

        col_run1, col_run2 = st.columns([1, 3])
        with col_run1:
            execute_btn = st.button("🚀 Start Organizing Now", type="primary", use_container_width=True)

        if execute_btn:
            progress_bar = st.progress(0)
            status_text = st.empty()

            def progress_update(current: int, total: int, filename: str):
                pct = int((current / total) * 100)
                progress_bar.progress(pct)
                status_text.text(f"Moving ({current}/{total}): {filename}")

            report = execute_move_plan(plan, dry_run=False, progress_callback=progress_update)
            progress_bar.progress(100)
            status_text.text("Organization completed!")

            st.session_state.last_report = report
            if report.undo_records:
                st.session_state.undo_records.extend(report.undo_records)

            if report.total_errors == 0:
                st.balloons()
                st.success(f"🎉 Successfully organized {report.total_moved} files into category folders!")
            else:
                st.warning(f"Organized {report.total_moved} files with {report.total_errors} errors. See logs below.")

        last_rep: OrganizationReport = st.session_state.last_report
        if last_rep and not last_rep.dry_run:
            st.markdown("---")
            st.subheader("Execution Results & Audit Report")

            r1, r2, r3, r4 = st.columns(4)
            with r1:
                st.metric("Total Planned", last_rep.total_planned)
            with r2:
                st.metric("Successfully Moved", last_rep.total_moved)
            with r3:
                st.metric("Skipped", last_rep.total_skipped)
            with r4:
                st.metric("Errors", last_rep.total_errors)

            if summary:
                after_counts = {cat: 0 for cat in summary.category_counts}
                for item in last_rep.items:
                    if item.status == "COMPLETED":
                        after_counts[item.category] = after_counts.get(item.category, 0) + 1

                comp_fig = create_comparison_chart(summary.category_counts, after_counts)
                st.plotly_chart(comp_fig, use_container_width=True)

            with st.expander("📋 Move Audit Log", expanded=False):
                log_df = pd.DataFrame(last_rep.logs)
                if not log_df.empty:
                    st.dataframe(log_df, use_container_width=True)
                    csv_bytes = log_df.to_csv(index=False).encode("utf-8")
                    st.download_button("📥 Export Audit Log to CSV", csv_bytes, "organization_audit_log.csv", "text/csv")


# ==============================================================================
# TAB 5: Undo & Rollback
# ==============================================================================
with tab_undo:
    st.subheader("⏪ Undo & Rollback")
    st.write(
        "Need to revert? You can safely restore all moved files to their exact initial locations. "
        "Empty category directories created during the operation will also be automatically removed."
    )

    undo_list = st.session_state.undo_records

    if not undo_list:
        st.info("No recorded file moves available for rollback in this session.")
    else:
        st.warning(f"There are **{len(undo_list)}** recorded moves ready to be restored.")

        col_u1, col_u2 = st.columns([1, 3])
        with col_u1:
            undo_clicked = st.button("⏪ Undo All Moves", type="primary", use_container_width=True)

        if undo_clicked:
            progress_bar = st.progress(0)
            status_text = st.empty()

            def undo_progress(current: int, total: int, filename: str):
                pct = int((current / total) * 100)
                progress_bar.progress(pct)
                status_text.text(f"Restoring ({current}/{total}): {filename}")

            restored, errors, undo_logs = undo_last_moves(undo_list, progress_callback=undo_progress)
            progress_bar.progress(100)
            status_text.text("Rollback completed!")

            st.session_state.undo_records = []
            st.success(f"Restored {restored} files back to their original locations! (Errors: {errors})")

            with st.expander("Rollback Log Details"):
                st.dataframe(pd.DataFrame(undo_logs), use_container_width=True)


# ==============================================================================
# TAB 6: Rules & Settings
# ==============================================================================
with tab_settings:
    st.subheader("⚙️ Custom Categories & Folder Names")
    st.write("Customize which extensions map to which folder, or rename target folders.")

    col_s1, col_s2 = st.columns(2)

    with col_s1:
        st.markdown("#### Category Folder Names")
        folder_names = dict(st.session_state.folder_names)
        for cat in list(DEFAULT_CATEGORIES.keys()) + ["Others"]:
            current_name = folder_names.get(cat, cat)
            new_name = st.text_input(f"Folder for '{cat}'", value=current_name, key=f"fld_{cat}")
            folder_names[cat] = new_name.strip() or cat
        st.session_state.folder_names = folder_names

    with col_s2:
        st.markdown("#### Extensions per Category")
        rules = dict(st.session_state.category_rules)
        for cat, exts in DEFAULT_CATEGORIES.items():
            ext_str = ", ".join(rules.get(cat, exts))
            new_ext_str = st.text_area(f"{cat} Extensions", value=ext_str, height=68, key=f"ext_{cat}")
            cleaned = [e.strip() for e in new_ext_str.split(",") if e.strip()]
            rules[cat] = cleaned
        st.session_state.category_rules = rules

    if st.button("🔄 Reset Categories to Defaults"):
        st.session_state.category_rules = {k: list(v) for k, v in DEFAULT_CATEGORIES.items()}
        st.session_state.folder_names = {k: k for k in list(DEFAULT_CATEGORIES.keys()) + ["Others"]}
        st.success("Reset settings to default successfully!")
        st.rerun()
