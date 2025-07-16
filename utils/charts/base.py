import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from utils.design.tokens import (
    BRAND_PRIMARY, BRAND_SUCCESS, BRAND_ERROR, BRAND_WARNING, BRAND_INFO,
    NEUTRAL_50, NEUTRAL_100, NEUTRAL_200, NEUTRAL_300, NEUTRAL_400, NEUTRAL_500,
    NEUTRAL_600, NEUTRAL_700, NEUTRAL_800, NEUTRAL_900,
    BACKGROUND_PRIMARY, BACKGROUND_SECONDARY, BACKGROUND_TERTIARY,
    BORDER_PRIMARY, BORDER_SECONDARY,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_TERTIARY, TEXT_MUTED, TEXT_INVERSE,
    FONT_SIZE_XS, FONT_SIZE_SM, FONT_SIZE_BASE, FONT_SIZE_LG, FONT_SIZE_XL,
    FONT_SIZE_2XL, FONT_SIZE_3XL, FONT_SIZE_4XL, FONT_SIZE_5XL,
    FONT_WEIGHT_NORMAL, FONT_WEIGHT_MEDIUM, FONT_WEIGHT_SEMIBOLD, FONT_WEIGHT_BOLD, FONT_WEIGHT_EXTRABOLD,
    LINE_HEIGHT_TIGHT, LINE_HEIGHT_NORMAL, LINE_HEIGHT_RELAXED,
    LETTER_SPACING_TIGHT, LETTER_SPACING_NORMAL, LETTER_SPACING_WIDE, LETTER_SPACING_WIDER, LETTER_SPACING_WIDEST,
    SPACE_1, SPACE_2, SPACE_3, SPACE_4, SPACE_5, SPACE_6, SPACE_8, SPACE_10, SPACE_12, SPACE_16, SPACE_20,
    BORDER_RADIUS_SM, BORDER_RADIUS_MD, BORDER_RADIUS_LG, BORDER_RADIUS_XL, BORDER_RADIUS_2XL, BORDER_RADIUS_FULL,
    SHADOW_SM, SHADOW_MD, SHADOW_LG, SHADOW_XL, SHADOW_2XL,
    TRANSITION_FAST, TRANSITION_NORMAL, TRANSITION_SLOW,
    get_change_color, get_emphasis_color, get_background_gradient, get_border_color,
    get_card_base_styles, get_emphasis_card_styles, get_card_title_styles,
    get_emphasis_card_title_styles, get_card_metric_styles, get_card_caption_styles,
    get_card_change_styles, get_emphasis_accent_bar,
    # Chart configuration tokens
    CHART_TEMPLATE, CHART_FONT_FAMILY, CHART_FONT_SIZE, CHART_HEIGHT, CHART_MARGIN,
    CHART_GRID_COLOR, CHART_AXIS_LINE_COLOR, CHART_AXIS_LINE_WIDTH, CHART_GRID_WIDTH,
    CHART_PLOT_BGCOLOR, CHART_PAPER_BGCOLOR
)

# --- Base Chart Functions ---

def create_time_series_chart(df, x_col, y_cols, x_label="Month", y_label="Value", 
                           x_format=None, y_format=None, height=CHART_HEIGHT, show_legend=True):
    """
    Create a standardized time series line chart.
    
    Args:
        df: Input DataFrame
        x_col: Column to use for x-axis
        y_cols: List of columns to plot on y-axis
        x_label: Label for x-axis (default: "Month")
        y_label: Label for y-axis (default: "Value")
        x_format: Format type for x-axis ('currency', 'percentage', 'date', 'number')
        y_format: Format type for y-axis ('currency', 'percentage', 'date', 'number')
        height: Chart height
        show_legend: Whether to show legend
    """
    if df.empty or not y_cols:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=NEUTRAL_500)
        )
        fig.update_layout(
            height=height,
            font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
            plot_bgcolor=CHART_PLOT_BGCOLOR,
            paper_bgcolor=CHART_PAPER_BGCOLOR,
            margin=CHART_MARGIN
        )
        return fig
    fig = px.line(
        df, 
        x=x_col, 
        y=y_cols,
        height=height,
        template=CHART_TEMPLATE
    )
    fig.update_layout(
        font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
        plot_bgcolor=CHART_PLOT_BGCOLOR,
        paper_bgcolor=CHART_PAPER_BGCOLOR,
        margin=CHART_MARGIN,
        showlegend=show_legend,
        hovermode='x unified'
    )
    fig.update_xaxes(
        title_text=x_label,
        showgrid=True, 
        gridwidth=CHART_GRID_WIDTH, 
        gridcolor=CHART_GRID_COLOR,
        zeroline=False,
        showline=True,
        linecolor=CHART_AXIS_LINE_COLOR,
        linewidth=CHART_AXIS_LINE_WIDTH
    )
    fig.update_yaxes(
        title_text=y_label,
        showgrid=True, 
        gridwidth=CHART_GRID_WIDTH, 
        gridcolor=CHART_GRID_COLOR,
        zeroline=False,
        showline=True,
        linecolor=CHART_AXIS_LINE_COLOR,
        linewidth=CHART_AXIS_LINE_WIDTH
    )
    
    # Apply formatting if specified
    if x_format or y_format:
        from .formatting import apply_consistent_axis_formatting
        fig = apply_consistent_axis_formatting(fig, x_format=x_format, y_format=y_format, 
                                             x_label=x_label, y_label=y_label)
    
    return fig

def create_bar_chart(df, x_col, y_col, x_label=None, y_label="Value", color_col=None, 
                    x_format=None, y_format=None, height=CHART_HEIGHT, orientation='v'):
    """
    Create a standardized bar chart.
    
    Args:
        df: Input DataFrame
        x_col: Column to use for x-axis
        y_col: Column to use for y-axis
        x_label: Label for x-axis (default: uses x_col name)
        y_label: Label for y-axis (default: "Value")
        color_col: Column to use for color coding
        x_format: Format type for x-axis ('currency', 'percentage', 'date', 'number')
        y_format: Format type for y-axis ('currency', 'percentage', 'date', 'number')
        height: Chart height
        orientation: Chart orientation ('v' for vertical, 'h' for horizontal)
    """
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=NEUTRAL_500)
        )
        fig.update_layout(
            height=height,
            font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
            plot_bgcolor=CHART_PLOT_BGCOLOR,
            paper_bgcolor=CHART_PAPER_BGCOLOR,
            margin=CHART_MARGIN
        )
        return fig
    
    # Use x_col name as default x_label if not provided
    if x_label is None:
        x_label = x_col
    
    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        height=height,
        orientation=orientation,
        template=CHART_TEMPLATE
    )
    fig.update_layout(
        font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
        plot_bgcolor=CHART_PLOT_BGCOLOR,
        paper_bgcolor=CHART_PAPER_BGCOLOR,
        margin=CHART_MARGIN,
        showlegend=color_col is not None,
        hovermode='x unified'
    )
    fig.update_xaxes(
        title_text=x_label,
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor=CHART_AXIS_LINE_COLOR,
        linewidth=CHART_AXIS_LINE_WIDTH
    )
    fig.update_yaxes(
        title_text=y_label,
        showgrid=True,
        gridwidth=CHART_GRID_WIDTH,
        gridcolor=CHART_GRID_COLOR,
        zeroline=False,
        showline=True,
        linecolor=CHART_AXIS_LINE_COLOR,
        linewidth=CHART_AXIS_LINE_WIDTH
    )
    
    # Apply formatting if specified
    if x_format or y_format:
        from .formatting import apply_consistent_axis_formatting
        fig = apply_consistent_axis_formatting(fig, x_format=x_format, y_format=y_format, 
                                             x_label=x_label, y_label=y_label)
    
    return fig

def create_pie_chart(df, names_col, values_col, height=CHART_HEIGHT, hole=0.3):
    """
    Create a standardized pie chart.
    
    Args:
        df: Input DataFrame
        names_col: Column to use for pie slice names
        values_col: Column to use for pie slice values
        height: Chart height
        hole: Hole size for donut chart (0.3 = 30% hole)
    """
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=NEUTRAL_500)
        )
        fig.update_layout(
            height=height,
            font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
            plot_bgcolor=CHART_PLOT_BGCOLOR,
            paper_bgcolor=CHART_PAPER_BGCOLOR,
            margin=CHART_MARGIN
        )
        return fig
    fig = px.pie(
        df,
        names=names_col,
        values=values_col,
        hole=hole,
        height=height,
        template=CHART_TEMPLATE
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
        plot_bgcolor=CHART_PLOT_BGCOLOR,
        paper_bgcolor=CHART_PAPER_BGCOLOR,
        margin=CHART_MARGIN,
        showlegend=True
    )
    return fig

def create_histogram(df, x_col, x_label=None, y_label="Frequency", x_format=None, 
                    height=CHART_HEIGHT, nbins=10):
    """
    Create a standardized histogram chart.
    
    Args:
        df: Input DataFrame
        x_col: Column to use for x-axis
        x_label: Label for x-axis (default: uses x_col name)
        y_label: Label for y-axis (default: "Frequency")
        x_format: Format type for x-axis ('currency', 'percentage', 'date', 'number')
        height: Chart height
        nbins: Number of bins for histogram
    """
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=NEUTRAL_500)
        )
        fig.update_layout(
            height=height,
            font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
            plot_bgcolor=CHART_PLOT_BGCOLOR,
            paper_bgcolor=CHART_PAPER_BGCOLOR,
            margin=CHART_MARGIN
        )
        return fig
    
    # Use x_col name as default x_label if not provided
    if x_label is None:
        x_label = x_col
    
    fig = px.histogram(
        df,
        x=x_col,
        nbins=nbins,
        height=height,
        template=CHART_TEMPLATE
    )
    fig.update_layout(
        font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
        plot_bgcolor=CHART_PLOT_BGCOLOR,
        paper_bgcolor=CHART_PAPER_BGCOLOR,
        margin=CHART_MARGIN,
        showlegend=False
    )
    fig.update_xaxes(
        title_text=x_label,
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor=CHART_AXIS_LINE_COLOR,
        linewidth=CHART_AXIS_LINE_WIDTH
    )
    fig.update_yaxes(
        title_text=y_label,
        showgrid=True,
        gridwidth=CHART_GRID_WIDTH,
        gridcolor=CHART_GRID_COLOR,
        zeroline=False,
        showline=True,
        linecolor=CHART_AXIS_LINE_COLOR,
        linewidth=CHART_AXIS_LINE_WIDTH
    )
    
    # Apply formatting if specified
    if x_format:
        from .formatting import apply_consistent_axis_formatting
        fig = apply_consistent_axis_formatting(fig, x_format=x_format, x_label=x_label, y_label=y_label)
    
    return fig

def create_box_plot(df, y_col, y_label="Value", y_format=None, height=CHART_HEIGHT, color_col=None):
    """
    Create a standardized box plot chart.
    
    Args:
        df: Input DataFrame
        y_col: Column to use for y-axis
        y_label: Label for y-axis (default: "Value")
        y_format: Format type for y-axis ('currency', 'percentage', 'date', 'number')
        height: Chart height
        color_col: Column to use for color coding
    """
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=NEUTRAL_500)
        )
        fig.update_layout(
            height=height,
            font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
            plot_bgcolor=CHART_PLOT_BGCOLOR,
            paper_bgcolor=CHART_PAPER_BGCOLOR,
            margin=CHART_MARGIN
        )
        return fig
    fig = px.box(
        df,
        y=y_col,
        color=color_col,
        height=height,
        template=CHART_TEMPLATE
    )
    fig.update_layout(
        font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
        plot_bgcolor=CHART_PLOT_BGCOLOR,
        paper_bgcolor=CHART_PAPER_BGCOLOR,
        margin=CHART_MARGIN,
        showlegend=color_col is not None
    )
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor=CHART_AXIS_LINE_COLOR,
        linewidth=CHART_AXIS_LINE_WIDTH
    )
    fig.update_yaxes(
        title_text=y_label,
        showgrid=True,
        gridwidth=CHART_GRID_WIDTH,
        gridcolor=CHART_GRID_COLOR,
        zeroline=False,
        showline=True,
        linecolor=CHART_AXIS_LINE_COLOR,
        linewidth=CHART_AXIS_LINE_WIDTH
    )
    
    # Apply formatting if specified
    if y_format:
        from .formatting import apply_consistent_axis_formatting
        fig = apply_consistent_axis_formatting(fig, y_format=y_format, y_label=y_label)
    
    return fig

def create_area_chart(df, x_col, y_cols, x_label="Month", y_label="Value", 
                     x_format=None, y_format=None, height=CHART_HEIGHT):
    """
    Create a standardized area chart.
    
    Args:
        df: Input DataFrame
        x_col: Column to use for x-axis
        y_cols: List of columns to plot on y-axis
        x_label: Label for x-axis (default: "Month")
        y_label: Label for y-axis (default: "Value")
        x_format: Format type for x-axis ('currency', 'percentage', 'date', 'number')
        y_format: Format type for y-axis ('currency', 'percentage', 'date', 'number')
        height: Chart height
    """
    if df.empty or not y_cols:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=NEUTRAL_500)
        )
        fig.update_layout(
            height=height,
            font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
            plot_bgcolor=CHART_PLOT_BGCOLOR,
            paper_bgcolor=CHART_PAPER_BGCOLOR,
            margin=CHART_MARGIN
        )
        return fig
    fig = px.area(
        df,
        x=x_col,
        y=y_cols,
        height=height,
        template=CHART_TEMPLATE
    )
    fig.update_layout(
        font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
        plot_bgcolor=CHART_PLOT_BGCOLOR,
        paper_bgcolor=CHART_PAPER_BGCOLOR,
        margin=CHART_MARGIN,
        showlegend=True,
        hovermode='x unified'
    )
    fig.update_xaxes(
        title_text=x_label,
        showgrid=True, 
        gridwidth=CHART_GRID_WIDTH, 
        gridcolor=CHART_GRID_COLOR,
        zeroline=False,
        showline=True,
        linecolor=CHART_AXIS_LINE_COLOR,
        linewidth=CHART_AXIS_LINE_WIDTH
    )
    fig.update_yaxes(
        title_text=y_label,
        showgrid=True, 
        gridwidth=CHART_GRID_WIDTH, 
        gridcolor=CHART_GRID_COLOR,
        zeroline=False,
        showline=True,
        linecolor=CHART_AXIS_LINE_COLOR,
        linewidth=CHART_AXIS_LINE_WIDTH
    )
    
    # Apply formatting if specified
    if x_format or y_format:
        from .formatting import apply_consistent_axis_formatting
        fig = apply_consistent_axis_formatting(fig, x_format=x_format, y_format=y_format, 
                                             x_label=x_label, y_label=y_label)
    
    return fig 