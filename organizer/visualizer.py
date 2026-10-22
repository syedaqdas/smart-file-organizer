"""Plotly visualization suite for file distributions and storage metrics.

Generates responsive, modern charts for file counts, storage breakdown,
and before/after statistical comparisons.
"""

from typing import Dict, List, Optional
import plotly.graph_objects as go
import plotly.express as px

from .categories import CATEGORY_COLORS, CATEGORY_ICONS
from .scanner import format_file_size, FileInfo


def create_distribution_pie_chart(category_counts: Dict[str, int]) -> go.Figure:
    """Builds an interactive donut chart of file distribution by category.

    Args:
        category_counts: Dictionary mapping category name to file count.

    Returns:
        Plotly Figure object.
    """
    # Filter out categories with zero files
    active = {cat: count for cat, count in category_counts.items() if count > 0}

    if not active:
        # Return empty state figure
        fig = go.Figure()
        fig.add_annotation(
            text="No files discovered yet",
            showarrow=False,
            font=dict(size=16, color="#9CA3AF"),
        )
        fig.update_layout(
            height=340,
            margin=dict(l=20, r=20, t=30, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        return fig

    labels = list(active.keys())
    values = list(active.values())
    labels_with_icons = [f"{CATEGORY_ICONS.get(cat, '📁')} {cat}" for cat in labels]
    colors = [CATEGORY_COLORS.get(cat, "#94A3B8") for cat in labels]
    total_files = sum(values)

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels_with_icons,
                values=values,
                hole=0.55,
                marker=dict(colors=colors, line=dict(color="#FFFFFF", width=2)),
                textinfo="label+percent",
                hovertemplate="<b>%{label}</b><br>Count: %{value} files<br>Share: %{percent}<extra></extra>",
                textfont=dict(size=12),
            )
        ]
    )

    fig.update_layout(
        title=dict(
            text="<b>File Distribution by Category</b>",
            font=dict(size=15, color="#1F2937"),
            x=0.05,
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(size=11),
        ),
        annotations=[
            dict(
                text=f"<b>{total_files}</b><br><span style='font-size:11px;color:#6B7280;'>Files</span>",
                x=0.5,
                y=0.5,
                font=dict(size=18, color="#111827"),
                showarrow=False,
            )
        ],
        height=360,
        margin=dict(l=20, r=20, t=50, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def create_size_bar_chart(category_sizes: Dict[str, int]) -> go.Figure:
    """Builds a horizontal bar chart displaying storage consumption per category.

    Args:
        category_sizes: Dictionary mapping category name to byte count.

    Returns:
        Plotly Figure object.
    """
    active = {cat: size for cat, size in category_sizes.items() if size > 0}

    if not active:
        fig = go.Figure()
        fig.add_annotation(
            text="No storage data to display",
            showarrow=False,
            font=dict(size=16, color="#9CA3AF"),
        )
        fig.update_layout(
            height=340,
            margin=dict(l=20, r=20, t=30, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        return fig

    # Sort categories descending by size
    sorted_items = sorted(active.items(), key=lambda x: x[1], reverse=True)
    cats = [item[0] for item in sorted_items]
    sizes_bytes = [item[1] for item in sorted_items]

    # Convert to MB for numeric axis scaling
    sizes_mb = [round(b / (1024 * 1024), 2) for b in sizes_bytes]
    formatted_labels = [format_file_size(b) for b in sizes_bytes]
    labels_with_icons = [f"{CATEGORY_ICONS.get(cat, '📁')} {cat}" for cat in cats]
    colors = [CATEGORY_COLORS.get(cat, "#94A3B8") for cat in cats]

    fig = go.Figure(
        data=[
            go.Bar(
                x=sizes_mb,
                y=labels_with_icons,
                orientation="h",
                marker=dict(
                    color=colors,
                    line=dict(color="rgba(0,0,0,0.1)", width=1),
                    opacity=0.9,
                ),
                text=formatted_labels,
                textposition="auto",
                hovertemplate="<b>%{y}</b><br>Size: %{text}<extra></extra>",
            )
        ]
    )

    fig.update_layout(
        title=dict(
            text="<b>Storage Consumption by Category</b>",
            font=dict(size=15, color="#1F2937"),
            x=0.05,
        ),
        xaxis=dict(
            title="Size (Megabytes)",
            gridcolor="#F3F4F6",
            zerolinecolor="#E5E7EB",
        ),
        yaxis=dict(autorange="reversed"),  # Largest at top
        height=360,
        margin=dict(l=20, r=30, t=50, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def create_comparison_chart(before_counts: Dict[str, int], after_counts: Dict[str, int]) -> go.Figure:
    """Builds a grouped bar chart comparing file counts before vs after organization.

    Args:
        before_counts: Category counts before organization.
        after_counts: Category counts after organization.

    Returns:
        Plotly Figure object.
    """
    categories = sorted(list(set(before_counts.keys()).union(set(after_counts.keys()))))
    before_vals = [before_counts.get(cat, 0) for cat in categories]
    after_vals = [after_counts.get(cat, 0) for cat in categories]
    cat_labels = [f"{CATEGORY_ICONS.get(c, '📁')} {c}" for c in categories]

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            name="Scanned",
            x=cat_labels,
            y=before_vals,
            marker_color="#94A3B8",
        )
    )
    fig.add_trace(
        go.Bar(
            name="Organized",
            x=cat_labels,
            y=after_vals,
            marker_color="#10B981",
        )
    )

    fig.update_layout(
        barmode="group",
        title=dict(text="<b>Before vs After Organization</b>", font=dict(size=15)),
        yaxis=dict(title="Number of Files"),
        height=320,
        margin=dict(l=20, r=20, t=50, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
    )

    return fig
