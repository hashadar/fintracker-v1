from .base import create_time_series_chart
from .formatting import get_chart_label
from utils.config import DEFAULT_ROLLING_WINDOW
import pandas as pd

# --- Chart Wrapper Functions ---

def create_time_series_with_rolling(df, x_col, y_col, x_label=None, y_label=None, 
                                   x_format=None, y_format=None, window=DEFAULT_ROLLING_WINDOW, **kwargs):
    """
    Create a time series chart with rolling average line.
    
    Args:
        df: Input DataFrame
        x_col: Column to use for x-axis
        y_col: Column to use for y-axis
        x_label: Label for x-axis (default: "Month")
        y_label: Label for y-axis (default: "Value")
        x_format: Format type for x-axis ('currency', 'percentage', 'date', 'number')
        y_format: Format type for y-axis ('currency', 'percentage', 'date', 'number')
        window: Rolling window size (default from config)
        **kwargs: Additional arguments passed to chart creation
    """
    # Set default labels
    if x_label is None:
        x_label = get_chart_label('month')
    if y_label is None:
        y_label = get_chart_label('value')
    
    df = df.copy()
    rolling_col = f"{y_col}_RollingAvg"
    df[rolling_col] = df[y_col].rolling(window=window).mean()
    
    fig = create_time_series_chart(df, x_col, [y_col, rolling_col], 
                                  x_label=x_label, y_label=y_label,
                                  x_format=x_format, y_format=y_format, **kwargs)
    return fig 