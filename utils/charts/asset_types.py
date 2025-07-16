"""Asset type specific chart functions for the financial dashboard app."""

import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from utils.charts.base import create_time_series_chart, create_area_chart
from utils.charts.formatting import get_chart_label
from utils.data_processing import filter_by_asset_type, get_latest_month_data, get_monthly_aggregation, create_platform_trends_data
from utils.design.tokens import (
    NEUTRAL_500,
    CHART_TEMPLATE, CHART_FONT_FAMILY, CHART_FONT_SIZE, CHART_HEIGHT, CHART_MARGIN,
    CHART_PLOT_BGCOLOR, CHART_PAPER_BGCOLOR
)
from ..config import ASSET_TYPES

def create_asset_type_time_series(df, asset_type):
    """
    Create time series line and area charts for a given asset type by platform.
    
    Args:
        df (pd.DataFrame): Full dataset
        asset_type (str): Asset type to filter (Cash, Investments, Pensions)
    
    Returns:
        tuple: (line_chart, area_chart) - both are valid Figure objects
    """
    type_df = filter_by_asset_type(df, asset_type)
    if type_df.empty:
        # Return empty figures with messages
        line_fig = go.Figure()
        line_fig.add_annotation(
            text=f"No {asset_type} data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=NEUTRAL_500)
        )
        line_fig.update_layout(
            title=f'{asset_type} - Monthly Values by Platform',
            height=CHART_HEIGHT,
            font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
            plot_bgcolor=CHART_PLOT_BGCOLOR,
            paper_bgcolor=CHART_PAPER_BGCOLOR,
            margin=CHART_MARGIN
        )
        
        area_fig = go.Figure()
        area_fig.add_annotation(
            text=f"No {asset_type} data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=NEUTRAL_500)
        )
        area_fig.update_layout(
            title=f'{asset_type} - Platform Composition Over Time',
            height=CHART_HEIGHT,
            font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
            plot_bgcolor=CHART_PLOT_BGCOLOR,
            paper_bgcolor=CHART_PAPER_BGCOLOR,
            margin=CHART_MARGIN
        )
        
        return line_fig, area_fig
    
    # Prepare data using new data processing component
    platform_trends = create_platform_trends_data(type_df)
    
    if platform_trends.empty or len(platform_trends.columns) < 2:
        # Return empty figures with messages
        line_fig = go.Figure()
        line_fig.add_annotation(
            text=f"No {asset_type} platform data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=NEUTRAL_500)
        )
        line_fig.update_layout(
            title=f'{asset_type} - Monthly Values by Platform',
            height=CHART_HEIGHT,
            font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
            plot_bgcolor=CHART_PLOT_BGCOLOR,
            paper_bgcolor=CHART_PAPER_BGCOLOR,
            margin=CHART_MARGIN
        )
        
        area_fig = go.Figure()
        area_fig.add_annotation(
            text=f"No {asset_type} platform data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=NEUTRAL_500)
        )
        area_fig.update_layout(
            title=f'{asset_type} - Platform Composition Over Time',
            height=CHART_HEIGHT,
            font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
            plot_bgcolor=CHART_PLOT_BGCOLOR,
            paper_bgcolor=CHART_PAPER_BGCOLOR,
            margin=CHART_MARGIN
        )
        
        return line_fig, area_fig
    
    # Create charts using base functions
    y_cols = platform_trends.columns[1:].tolist()
    
    line_chart = create_time_series_chart(
        platform_trends,
        x_col='Month',
        y_cols=y_cols,
        x_label=get_chart_label('month'),
        y_label=get_chart_label('value'),
        y_format='currency'
    )
    
    area_chart = create_area_chart(
        platform_trends,
        x_col='Month',
        y_cols=y_cols,
        x_label=get_chart_label('month'),
        y_label=get_chart_label('value'),
        y_format='currency'
    )
    
    return line_chart, area_chart

def create_asset_type_breakdown(df, asset_type):
    """
    Create pie and bar charts for platform and asset breakdowns for a given asset type.
    
    Args:
        df (pd.DataFrame): Full dataset
        asset_type (str): Asset type to filter (Cash, Investments, Pensions)
    
    Returns:
        tuple: (platform_chart, asset_chart) - both are valid Figure objects
    """
    type_df = filter_by_asset_type(df, asset_type)
    if type_df.empty:
        # Return empty figures with messages
        platform_fig = go.Figure()
        platform_fig.add_annotation(
            text=f"No {asset_type} data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=NEUTRAL_500)
        )
        platform_fig.update_layout(
            title=f'{asset_type} - Current Platform Distribution',
            height=CHART_HEIGHT,
            font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
            plot_bgcolor=CHART_PLOT_BGCOLOR,
            paper_bgcolor=CHART_PAPER_BGCOLOR,
            margin=CHART_MARGIN
        )
        
        asset_fig = go.Figure()
        asset_fig.add_annotation(
            text=f"No {asset_type} data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=NEUTRAL_500)
        )
        asset_fig.update_layout(
            title=f'{asset_type} - Current Asset Distribution',
            height=CHART_HEIGHT,
            font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
            plot_bgcolor=CHART_PLOT_BGCOLOR,
            paper_bgcolor=CHART_PAPER_BGCOLOR,
            margin=CHART_MARGIN
        )
        
        return platform_fig, asset_fig
    
    # Get latest month data using new data processing component
    latest_data = get_latest_month_data(type_df)
    
    if latest_data.empty:
        # Return empty figures with messages
        platform_fig = go.Figure()
        platform_fig.add_annotation(
            text=f"No {asset_type} data for latest month",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=NEUTRAL_500)
        )
        platform_fig.update_layout(
            title=f'{asset_type} - Current Platform Distribution',
            height=CHART_HEIGHT,
            font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
            plot_bgcolor=CHART_PLOT_BGCOLOR,
            paper_bgcolor=CHART_PAPER_BGCOLOR,
            margin=CHART_MARGIN
        )
        
        asset_fig = go.Figure()
        asset_fig.add_annotation(
            text=f"No {asset_type} data for latest month",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=NEUTRAL_500)
        )
        asset_fig.update_layout(
            title=f'{asset_type} - Current Asset Distribution',
            height=CHART_HEIGHT,
            font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
            plot_bgcolor=CHART_PLOT_BGCOLOR,
            paper_bgcolor=CHART_PAPER_BGCOLOR,
            margin=CHART_MARGIN
        )
        
        return platform_fig, asset_fig
    
    # Platform breakdown
    platform_breakdown = latest_data.groupby('Platform')['Value'].sum().reset_index()
    
    # Asset breakdown (if Asset column exists)
    if 'Asset' in latest_data.columns:
        asset_breakdown = latest_data.groupby('Asset')['Value'].sum().reset_index()
    else:
        asset_breakdown = pd.DataFrame()
    
    # Create charts
    if not platform_breakdown.empty:
        platform_chart = px.pie(
            platform_breakdown,
            values='Value',
            names='Platform',
            title=f'{asset_type} - Current Platform Distribution'
        )
        platform_chart.update_traces(textposition='inside', textinfo='percent+label')
        platform_chart.update_layout(
            font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
            plot_bgcolor=CHART_PLOT_BGCOLOR,
            paper_bgcolor=CHART_PAPER_BGCOLOR,
            margin=CHART_MARGIN,
            showlegend=True
        )
    else:
        platform_chart = go.Figure()
        platform_chart.add_annotation(
            text="No platform data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=NEUTRAL_500)
        )
        platform_chart.update_layout(
            title=f'{asset_type} - Current Platform Distribution',
            height=CHART_HEIGHT,
            font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
            plot_bgcolor=CHART_PLOT_BGCOLOR,
            paper_bgcolor=CHART_PAPER_BGCOLOR,
            margin=CHART_MARGIN
        )
    
    if not asset_breakdown.empty:
        asset_chart = px.pie(
            asset_breakdown,
            values='Value',
            names='Asset',
            title=f'{asset_type} - Current Asset Distribution'
        )
        asset_chart.update_traces(textposition='inside', textinfo='percent+label')
        asset_chart.update_layout(
            font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
            plot_bgcolor=CHART_PLOT_BGCOLOR,
            paper_bgcolor=CHART_PAPER_BGCOLOR,
            margin=CHART_MARGIN,
            showlegend=True
        )
    else:
        asset_chart = go.Figure()
        asset_chart.add_annotation(
            text="No asset data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=NEUTRAL_500)
        )
        asset_chart.update_layout(
            title=f'{asset_type} - Current Asset Distribution',
            height=CHART_HEIGHT,
            font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
            plot_bgcolor=CHART_PLOT_BGCOLOR,
            paper_bgcolor=CHART_PAPER_BGCOLOR,
            margin=CHART_MARGIN
        )
    
    return platform_chart, asset_chart 