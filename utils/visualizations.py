"""Visualization functions and reusable components for the financial dashboard app."""

import plotly.express as px
import pandas as pd
import streamlit as st
import plotly.graph_objs as go

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
        
        c = '#888'  # Default color
        if color == 'normal':
            c = 'green'
        elif color == 'inverse':
            c = 'red'
        return f"<span style='color: {c}; font-weight: 500;'>{delta}</span>"

    mom_html = delta_html(mom_delta, mom_color)
    ytd_html = delta_html(ytd_delta, ytd_color)
    
    subtext_parts = []
    if mom_html:
        subtext_parts.append(mom_html)
    if ytd_html:
        subtext_parts.append(ytd_html)
    
    subtext_final = " | ".join(subtext_parts)
    
    if not subtext_final and help_text:
        subtext_final = help_text

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
        <h3 style="font-size: 1rem; font-weight: normal; margin: 0; color: #666;">{label}</h3>
        <p style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0;">{value}</p>
        <div style="font-size: 1rem; color: #888; margin-top: 0.2rem;">{subtext_final}</div>
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