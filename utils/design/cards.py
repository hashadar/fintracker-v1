"""Card components for the financial dashboard app."""

import html

import streamlit as st

from .tokens import (  # Color tokens; Typography tokens; Spacing tokens; Border radius tokens; Shadow tokens; Transition tokens; Utility functions
    BRAND_PRIMARY,
    FONT_SIZE_4XL,
    FONT_SIZE_5XL,
    get_card_base_styles,
    get_card_caption_styles,
    get_card_change_styles,
    get_card_metric_styles,
    get_card_title_styles,
    get_change_color,
    get_emphasis_accent_bar,
    get_emphasis_card_styles,
    get_emphasis_card_title_styles,
)

# --- Card Components ---


def simple_card(title, metric, caption=None):
    """
    Simple card component for displaying a single metric.

    Args:
        title (str): Card title
        metric (str): Main metric value
        caption (str, optional): Caption text below metric
    """
    # Ensure all inputs are strings and stripped, then escape HTML to prevent injection
    title = html.escape(str(title).strip()) if title else ""
    metric = html.escape(str(metric).strip()) if metric else ""
    caption = html.escape(str(caption).strip()) if caption else ""

    # Build HTML with conditional caption rendering
    card_html = f"""
    <div style="{get_card_base_styles()}">
        <div style="{get_card_title_styles()}">{title}</div>
        <div style="{get_card_metric_styles(FONT_SIZE_4XL)}">{metric}</div>
        {f'<div style="{get_card_caption_styles()}">{caption}</div>' if caption else ''}
    </div>
    """
    st.markdown(card_html.strip(), unsafe_allow_html=True)


def emphasis_card(title, metric, caption=None, emphasis_color=BRAND_PRIMARY):
    """
    Emphasis card component with highlighted styling to call attention.

    Args:
        title (str): Card title
        metric (str): Main metric value
        caption (str, optional): Caption text below metric
        emphasis_color (str): Color for emphasis styling
    """
    # Ensure all inputs are strings and stripped, then escape HTML to prevent injection
    title = html.escape(str(title).strip()) if title else ""
    metric = html.escape(str(metric).strip()) if metric else ""
    caption = html.escape(str(caption).strip()) if caption else ""

    # Build HTML with emphasis styling and conditional caption rendering
    card_html = f"""
    <div style="{get_emphasis_card_styles(emphasis_color)}">
        <div style="{get_emphasis_accent_bar(emphasis_color)}"></div>
        <div style="{get_emphasis_card_title_styles(emphasis_color)}">{title}</div>
        <div style="{get_card_metric_styles(FONT_SIZE_5XL)}">{metric}</div>
        {f'<div style="{get_card_caption_styles()}">{caption}</div>' if caption else ''}
    </div>
    """
    st.markdown(card_html.strip(), unsafe_allow_html=True)


def complex_card(
    title,
    metric,
    mom_change=None,
    ytd_change=None,
    caption=None,
    mom_color="normal",
    ytd_color="normal",
):
    """
    Complex card component displaying metric with MoM and YTD changes.

    Args:
        title (str): Card title
        metric (str): Main metric value
        mom_change (str, optional): Month-over-month change
        ytd_change (str, optional): Year-to-date change
        caption (str, optional): Caption text below metric
        mom_color (str): Color for MoM change ("normal", "inverse")
        ytd_color (str): Color for YTD change ("normal", "inverse")
    """
    # Ensure all inputs are strings and stripped, then escape HTML to prevent injection
    title = html.escape(str(title).strip()) if title else ""
    metric = html.escape(str(metric).strip()) if metric else ""

    # Handle caption
    caption_str = str(caption).strip() if caption is not None else ""
    if caption_str:
        caption_html = (
            f'<div style="{get_card_caption_styles()}">{html.escape(caption_str)}</div>'
        )
    else:
        caption_html = ""

    # Build change indicators
    changes_parts = []

    if mom_change is not None:
        mom_color_style = get_change_color(mom_color)
        changes_parts.append(
            f'<span style="color: {mom_color_style};">{html.escape(str(mom_change))}</span>'
        )

    if ytd_change is not None:
        ytd_color_style = get_change_color(ytd_color)
        changes_parts.append(
            f'<span style="color: {ytd_color_style};">{html.escape(str(ytd_change))}</span>'
        )

    if changes_parts:
        changes_html = (
            f'<div style="{get_card_change_styles()}">{" | ".join(changes_parts)}</div>'
        )
    else:
        changes_html = ""

    # Build final card HTML
    card_html = f"""
    <div style="{get_card_base_styles()}">
        <div style="{get_card_title_styles()}">{title}</div>
        <div style="{get_card_metric_styles(FONT_SIZE_4XL)}">{metric}</div>
        {changes_html}
        {caption_html}
    </div>
    """
    st.markdown(card_html.strip(), unsafe_allow_html=True)


def complex_emphasis_card(
    title,
    metric,
    mom_change=None,
    ytd_change=None,
    caption=None,
    mom_color="normal",
    ytd_color="normal",
    emphasis_color=BRAND_PRIMARY,
):
    """
    Complex emphasis card component with highlighted styling and change indicators.

    Args:
        title (str): Card title
        metric (str): Main metric value
        mom_change (str, optional): Month-over-month change
        ytd_change (str, optional): Year-to-date change
        caption (str, optional): Caption text below metric
        mom_color (str): Color for MoM change ("normal", "inverse")
        ytd_color (str): Color for YTD change ("normal", "inverse")
        emphasis_color (str): Color for emphasis styling
    """
    # Ensure all inputs are strings and stripped, then escape HTML to prevent injection
    title = html.escape(str(title).strip()) if title else ""
    metric = html.escape(str(metric).strip()) if metric else ""

    # Handle caption
    caption_str = str(caption).strip() if caption is not None else ""
    if caption_str:
        caption_html = (
            f'<div style="{get_card_caption_styles()}">{html.escape(caption_str)}</div>'
        )
    else:
        caption_html = ""

    # Build change indicators
    changes_parts = []

    if mom_change is not None:
        mom_color_style = get_change_color(mom_color)
        changes_parts.append(
            f'<span style="color: {mom_color_style};">{html.escape(str(mom_change))}</span>'
        )

    if ytd_change is not None:
        ytd_color_style = get_change_color(ytd_color)
        changes_parts.append(
            f'<span style="color: {ytd_color_style};">{html.escape(str(ytd_change))}</span>'
        )

    if changes_parts:
        changes_html = (
            f'<div style="{get_card_change_styles()}">{" | ".join(changes_parts)}</div>'
        )
    else:
        changes_html = ""

    # Build final card HTML with emphasis styling
    card_html = f"""
    <div style="{get_emphasis_card_styles(emphasis_color)}">
        <div style="{get_emphasis_accent_bar(emphasis_color)}"></div>
        <div style="{get_emphasis_card_title_styles(emphasis_color)}">{title}</div>
        <div style="{get_card_metric_styles(FONT_SIZE_5XL)}">{metric}</div>
        {changes_html}
        {caption_html}
    </div>
    """
    st.markdown(card_html.strip(), unsafe_allow_html=True)
