"""Visualization functions and reusable components for the financial dashboard app."""

import plotly.express as px
import pandas as pd
import streamlit as st
import plotly.graph_objs as go
import html
from utils.design_tokens import (
    # Color tokens
    BRAND_PRIMARY, BRAND_SUCCESS, BRAND_ERROR, NEUTRAL_500,
    BACKGROUND_PRIMARY, BORDER_PRIMARY, TEXT_PRIMARY, TEXT_SECONDARY, TEXT_TERTIARY,
    SHADOW_SM, SHADOW_MD, SHADOW_LG,
    # Typography tokens
    FONT_SIZE_XS, FONT_SIZE_SM, FONT_SIZE_4XL, FONT_SIZE_5XL,
    FONT_WEIGHT_MEDIUM, FONT_WEIGHT_SEMIBOLD, FONT_WEIGHT_BOLD, FONT_WEIGHT_EXTRABOLD,
    LINE_HEIGHT_TIGHT, LETTER_SPACING_WIDER,
    # Spacing tokens
    SPACE_2, SPACE_4, SPACE_6,
    # Border radius tokens
    BORDER_RADIUS_XL,
    # Transition tokens
    TRANSITION_NORMAL,
    # Utility functions
    get_change_color, get_emphasis_color, get_background_gradient, get_border_color,
    get_card_base_styles, get_emphasis_card_styles, get_card_title_styles,
    get_emphasis_card_title_styles, get_card_metric_styles, get_card_caption_styles,
    get_card_change_styles, get_emphasis_accent_bar
)

# --- Time Series and Breakdown Visualizations ---
def create_asset_type_time_series(df, asset_type):
    """Create time series line and area charts for a given asset type by platform."""
    type_df = df[df['Asset_Type'] == asset_type]
    if type_df.empty:
        return None, None
    # Derive month from Timestamp
    type_df = type_df.copy()
    type_df['Month'] = type_df['Timestamp'].dt.to_period('M').dt.to_timestamp()
    # Monthly values by platform
    platform_trends = type_df.pivot_table(
        index='Month',
        columns='Platform',
        values='Value',
        aggfunc='sum'
    ).reset_index()
    # Line chart: value by platform
    fig_value = px.line(platform_trends, 
                       x='Month', 
                       y=platform_trends.columns[1:].tolist(),
                       title=f'{asset_type} - Monthly Values by Platform',
                       labels={'value': 'Value (GBP)', 'Month': 'Month', 'variable': 'Platform'})
    # Area chart: platform composition
    fig_composition = px.area(platform_trends,
                            x='Month',
                            y=platform_trends.columns[1:].tolist(),
                            title=f'{asset_type} - Platform Composition Over Time',
                            labels={'value': 'Value (GBP)', 'Month': 'Month', 'variable': 'Platform'})
    return fig_value, fig_composition

def create_asset_type_breakdown(df, asset_type):
    """Create pie and bar charts for platform and asset breakdowns for a given asset type."""
    type_df = df[df['Asset_Type'] == asset_type]
    if type_df.empty:
        return None, None
    # Derive month from Timestamp
    type_df = type_df.copy()
    type_df['Month'] = type_df['Timestamp'].dt.to_period('M').dt.to_timestamp()
    # Latest snapshot
    latest_month = type_df['Month'].max()
    latest_df = type_df[type_df['Month'] == latest_month]
    # Platform distribution pie chart
    platform_df = latest_df.groupby('Platform')['Value'].sum().reset_index()
    fig_platform = px.pie(platform_df,
                         values='Value',
                         names='Platform',
                         title=f'{asset_type} - Current Platform Distribution')
    # Asset distribution bar chart (for investments)
    if 'Asset' in type_df.columns and asset_type == 'Investments':
        asset_df = latest_df.groupby(['Platform', 'Asset'])['Value'].sum().reset_index()
        fig_asset = px.bar(asset_df,
                          x='Platform',
                          y='Value',
                          color='Asset',
                          title=f'{asset_type} - Current Asset Distribution by Platform',
                          labels={'Value': 'Value (GBP)', 'Platform': 'Platform', 'Asset': 'Asset'})
    else:
        fig_asset = None
    return fig_platform, fig_asset

# --- KPI Card Component ---
def create_pie_chart(df, names, values, title):
    """Creates a standard pie chart."""
    fig = px.pie(df, names=names, values=values, title=title, hole=0.3)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def create_bar_chart(df, x, y, title, labels):
    """Creates a standard bar chart."""
    fig = px.bar(df, x=x, y=y, title=title, labels=labels)
    return fig

def kpi_card(label, value, mom_delta=None, ytd_delta=None, mom_color=None, ytd_color=None, help_text=None):
    """
    Reusable KPI card component for consistent metric display.
    It can display month-over-month/year-to-date deltas and an optional subtitle/help text.
    """
    
    def delta_html(delta, color):
        if delta is None:
            return ''
        
        c = NEUTRAL_500  # Default color
        if color == 'normal':
            c = BRAND_SUCCESS
        elif color == 'inverse':
            c = BRAND_ERROR
        return f"<span style='color: {c}; font-weight: 500;'>{html.escape(str(delta))}</span>"

    mom_html = delta_html(mom_delta, mom_color)
    ytd_html = delta_html(ytd_delta, ytd_color)
    
    subtext_parts = []
    if mom_html:
        subtext_parts.append(mom_html)
    if ytd_html:
        subtext_parts.append(ytd_html)
    
    subtext_final = " | ".join(subtext_parts)
    
    if not subtext_final and help_text:
        subtext_final = html.escape(str(help_text))

    card_html = f"""
    <div style="
        background-color: var(--background-color);
        border: 1px solid var(--border-color);
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 1rem;
    ">
        <h3 style="font-size: 1rem; font-weight: normal; margin: 0; color: #666;">{html.escape(str(label))}</h3>
        <p style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0;">{html.escape(str(value))}</p>
        <div style="font-size: 1rem; color: #888; margin-top: 0.2rem;">{subtext_final}</div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

# --- NEW REUSABLE CARD COMPONENTS ---

def simple_card(title, metric, caption=None):
    """
    Simple card component for displaying a single metric.
    """
    # Ensure all inputs are strings and stripped, then escape HTML to prevent injection
    title = html.escape(str(title).strip()) if title else ""
    metric = html.escape(str(metric).strip()) if metric else ""
    caption = html.escape(str(caption).strip()) if caption else ""
    
    # Build HTML with conditional caption rendering (only if caption exists)
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

def complex_card(title, metric, mom_change=None, ytd_change=None, caption=None, mom_color="normal", ytd_color="normal"):
    """
    Complex card component displaying metric with MoM and YTD changes.
    """
    # Ensure all inputs are strings and stripped, then escape HTML to prevent injection
    title = html.escape(str(title).strip()) if title else ""
    metric = html.escape(str(metric).strip()) if metric else ""
    
    # Handle caption: check if it's already HTML (from previous processing) or needs escaping
    caption_str = str(caption).strip() if caption is not None else ""
    if caption_str and caption_str.startswith('<div'):
        caption_html = caption_str  # Already processed HTML
    elif caption_str:
        caption_html = f'<div style="{get_card_caption_styles()}">{html.escape(caption_str)}</div>'
    else:
        caption_html = ""
    
    # Process change indicators with HTML escaping
    mom_change = html.escape(str(mom_change).strip()) if mom_change else ""
    ytd_change = html.escape(str(ytd_change).strip()) if ytd_change else ""

    # Get color hex values for change indicators
    mom_color_hex = get_change_color(mom_color)
    ytd_color_hex = get_change_color(ytd_color)
    
    # Build changes HTML only if at least one change indicator exists
    changes_html = ""
    if mom_change or ytd_change:
        changes_parts = []
        if mom_change:
            changes_parts.append(f'<span style="color: {mom_color_hex}; font-weight: {FONT_WEIGHT_SEMIBOLD};">{mom_change}</span>')
        if ytd_change:
            changes_parts.append(f'<span style="color: {ytd_color_hex}; font-weight: {FONT_WEIGHT_SEMIBOLD};">{ytd_change}</span>')
        changes_html = f'<div style="{get_card_change_styles()}">{" | ".join(changes_parts)}</div>'
    
    # Combine changes and caption: only render if at least one is non-empty
    content_html = ''
    if changes_html and caption_html:
        content_html = f'{changes_html}{caption_html}'
    elif changes_html:
        content_html = changes_html
    elif caption_html:
        content_html = caption_html
    
    # Build final card HTML
    card_html = f"""
    <div style="{get_card_base_styles()}">
        <div style="{get_card_title_styles()}">{title}</div>
        <div style="{get_card_metric_styles(FONT_SIZE_4XL)}">{metric}</div>
        {content_html}
    </div>
    """
    st.markdown(card_html.strip(), unsafe_allow_html=True)

def complex_emphasis_card(title, metric, mom_change=None, ytd_change=None, caption=None, mom_color="normal", ytd_color="normal", emphasis_color=BRAND_PRIMARY):
    """
    Complex emphasis card component with highlighted styling and change indicators.
    """
    # Ensure all inputs are strings and stripped, then escape HTML to prevent injection
    title = html.escape(str(title).strip()) if title else ""
    metric = html.escape(str(metric).strip()) if metric else ""
    
    # Handle caption: check if it's already HTML (from previous processing) or needs escaping
    caption_str = str(caption).strip() if caption is not None else ""
    if caption_str and caption_str.startswith('<div'):
        caption_html = caption_str  # Already processed HTML
    elif caption_str:
        caption_html = f'<div style="{get_card_caption_styles()}">{html.escape(caption_str)}</div>'
    else:
        caption_html = ""
    
    # Process change indicators with HTML escaping
    mom_change = html.escape(str(mom_change).strip()) if mom_change else ""
    ytd_change = html.escape(str(ytd_change).strip()) if ytd_change else ""

    # Get color hex values for change indicators
    mom_color_hex = get_change_color(mom_color)
    ytd_color_hex = get_change_color(ytd_color)
    
    # Build changes HTML only if at least one change indicator exists
    changes_html = ""
    if mom_change or ytd_change:
        changes_parts = []
        if mom_change:
            changes_parts.append(f'<span style="color: {mom_color_hex}; font-weight: {FONT_WEIGHT_SEMIBOLD};">{mom_change}</span>')
        if ytd_change:
            changes_parts.append(f'<span style="color: {ytd_color_hex}; font-weight: {FONT_WEIGHT_SEMIBOLD};">{ytd_change}</span>')
        changes_html = f'<div style="{get_card_change_styles()}">{" | ".join(changes_parts)}</div>'
    
    # Combine changes and caption: only render if at least one is non-empty
    content_html = ''
    if changes_html and caption_html:
        content_html = f'{changes_html}{caption_html}'
    elif changes_html:
        content_html = changes_html
    elif caption_html:
        content_html = caption_html
    
    # Build final card HTML with emphasis styling
    card_html = f"""
    <div style="{get_emphasis_card_styles(emphasis_color)}">
        <div style="{get_emphasis_accent_bar(emphasis_color)}"></div>
        <div style="{get_emphasis_card_title_styles(emphasis_color)}">{title}</div>
        <div style="{get_card_metric_styles(FONT_SIZE_5XL)}">{metric}</div>
        {content_html}
    </div>
    """
    st.markdown(card_html.strip(), unsafe_allow_html=True)

# --- Asset Type Metrics Display ---
def display_asset_type_metrics(metrics, asset_type):
    """Display metrics for an asset type in a formatted header (HTML)."""
    if metrics is None:
        return
    return f"""
        <div class='asset-type-header'>
            <h2>{html.escape(str(asset_type))}</h2>
            <div style='display: flex; justify-content: space-between;'>
                <div>Latest Value: £{metrics['latest_value']:,.2f}</div>
                <div>MoM Change: {metrics['mom_change']:+.1f}%</div>
                <div>Platforms: {html.escape(str(metrics['platforms']))}</div>
                <div>Assets: {html.escape(str(metrics['assets']))}</div>
                <div>Months Tracked: {html.escape(str(metrics['months_tracked']))}</div>
            </div>
        </div>
    """ 