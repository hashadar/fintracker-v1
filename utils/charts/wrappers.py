from .base import create_time_series_chart, create_bar_chart
from .formatting import format_currency_axis, format_percentage_axis
import pandas as pd

# --- Chart Wrapper Functions ---

def create_percentage_chart(df, x_col, y_col, title=None, chart_type='bar', decimals=1, **kwargs):
    """
    Create a bar or line chart with percentage formatting on y-axis.
    chart_type: 'bar' or 'line'
    """
    if chart_type == 'bar':
        fig = create_bar_chart(df, x_col, y_col, title=title, **kwargs)
    else:
        fig = create_time_series_chart(df, x_col, [y_col], title=title, **kwargs)
    format_percentage_axis(fig, axis='y', decimals=decimals)
    return fig

def create_currency_chart(df, x_col, y_col, title=None, chart_type='bar', **kwargs):
    """
    Create a bar or line chart with currency formatting on y-axis.
    chart_type: 'bar' or 'line'
    """
    if chart_type == 'bar':
        fig = create_bar_chart(df, x_col, y_col, title=title, **kwargs)
    else:
        fig = create_time_series_chart(df, x_col, [y_col], title=title, **kwargs)
    format_currency_axis(fig, axis='y')
    return fig

def create_time_series_with_rolling(df, x_col, y_col, title=None, window=6, **kwargs):
    """
    Create a time series chart with rolling average line.
    """
    df = df.copy()
    rolling_col = f"{y_col}_RollingAvg"
    df[rolling_col] = df[y_col].rolling(window=window).mean()
    fig = create_time_series_chart(df, x_col, [y_col, rolling_col], title=title, **kwargs)
    return fig 