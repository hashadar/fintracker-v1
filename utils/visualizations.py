"""Visualization functions and reusable components for the financial dashboard app."""

import plotly.express as px
import pandas as pd
import streamlit as st

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
def kpi_card(label, value, mom_delta=None, ytd_delta=None, mom_color=None, ytd_color=None, help_text=None):
    """Reusable KPI card/box component for consistent metric display, with both MoM and YTD deltas."""
    def delta_html(delta, color):
        if delta is None:
            return ''
        c = 'black'
        if color == 'normal':
            c = 'green'
        elif color == 'inverse':
            c = 'red'
        return f"<span style='color: {c}; font-weight: 500;'>{delta}</span>"
    mom_html = delta_html(mom_delta, mom_color)
    ytd_html = delta_html(ytd_delta, ytd_color)
    subtext = ''
    if mom_html or ytd_html:
        subtext = f"<div style='font-size: 1.1rem; margin-top: 0.2rem;'>"
        subtext += mom_html if mom_html else ''
        subtext += (' | ' if mom_html and ytd_html else '')
        subtext += ytd_html if ytd_html else ''
        subtext += "</div>"
    card_html = f"""
    <div style='display: flex; flex-direction: column; align-items: flex-start; background: #f8f9fa; border-radius: 10px; padding: 1.2rem 1.5rem; margin: 0.5rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.04); min-width: 180px;'>
        <div style='font-size: 1.1rem; color: #666;'>{label}</div>
        <div style='font-size: 2rem; font-weight: bold; color: #222;'>{value}</div>
        {subtext}
        {f"<div style='font-size: 0.95rem; color: #888; margin-top: 0.2rem;'>{help_text}</div>" if help_text else ''}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

# --- Asset Type Metrics Display ---
def display_asset_type_metrics(metrics, asset_type):
    """Display metrics for an asset type in a formatted header (HTML)."""
    if metrics is None:
        return
    return f"""
        <div class='asset-type-header'>
            <h2>{asset_type}</h2>
            <div style='display: flex; justify-content: space-between;'>
                <div>Latest Value: £{metrics['latest_value']:,.2f}</div>
                <div>MoM Change: {metrics['mom_change']:+.1f}%</div>
                <div>Platforms: {metrics['platforms']}</div>
                <div>Assets: {metrics['assets']}</div>
                <div>Months Tracked: {metrics['months_tracked']}</div>
            </div>
        </div>
    """ 