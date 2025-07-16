# Formatting helpers for charts

from utils.design.tokens import CHART_FONT_SIZE, CHART_LABELS
from utils.config import CURRENCY_FORMAT, SHORT_DATE_FORMAT, CURRENCY_SYMBOL

def format_currency_axis(fig, axis='y', currency_symbol=CURRENCY_SYMBOL):
    """
    Format the specified axis (default y) as currency using config format.
    
    Args:
        fig: Plotly figure object
        axis: Which axis to format ('x' or 'y')
        currency_symbol: Currency symbol to use (default from config)
    """
    if axis == 'y':
        fig.update_yaxes(
            tickprefix=currency_symbol, 
            separatethousands=True, 
            tickformat=',.2f', 
            tickfont=dict(size=CHART_FONT_SIZE)
        )
    elif axis == 'x':
        fig.update_xaxes(
            tickprefix=currency_symbol, 
            separatethousands=True, 
            tickformat=',.2f', 
            tickfont=dict(size=CHART_FONT_SIZE)
        )
    return fig

def format_number_axis(fig, axis='y', decimals=0, separator=True):
    """
    Format the specified axis as numbers with optional thousands separator.
    
    Args:
        fig: Plotly figure object
        axis: Which axis to format ('x' or 'y')
        decimals: Number of decimal places (default: 0)
        separator: Whether to use thousands separator (default: True)
    """
    if separator:
        fmt = f',.{decimals}f'
    else:
        fmt = f'.{decimals}f'
    
    if axis == 'y':
        fig.update_yaxes(
            separatethousands=separator,
            tickformat=fmt,
            tickfont=dict(size=CHART_FONT_SIZE)
        )
    elif axis == 'x':
        fig.update_xaxes(
            separatethousands=separator,
            tickformat=fmt,
            tickfont=dict(size=CHART_FONT_SIZE)
        )
    return fig

def get_chart_label(label_key, default=None):
    """
    Get a chart label from the configuration.
    
    Args:
        label_key: Key to look up in CHART_LABELS
        default: Default value if key not found
    
    Returns:
        Label string or default value
    """
    return CHART_LABELS.get(label_key, default or label_key)

def apply_consistent_axis_formatting(fig, x_format=None, y_format=None, 
                                   x_label=None, y_label=None):
    """
    Apply consistent formatting to both axes of a chart.
    
    Args:
        fig: Plotly figure object
        x_format: Format type for x-axis ('currency', 'percentage', 'date', 'number')
        y_format: Format type for y-axis ('currency', 'percentage', 'date', 'number')
        x_label: Label for x-axis
        y_label: Label for y-axis
    
    Returns:
        Updated figure object
    """
    # Apply x-axis formatting
    if x_format == 'currency':
        format_currency_axis(fig, axis='x')
    elif x_format == 'percentage':
        format_percentage_axis(fig, axis='x')
    elif x_format == 'date':
        format_date_axis(fig, axis='x')
    elif x_format == 'number':
        format_number_axis(fig, axis='x')
    
    # Apply y-axis formatting
    if y_format == 'currency':
        format_currency_axis(fig, axis='y')
    elif y_format == 'percentage':
        format_percentage_axis(fig, axis='y')
    elif y_format == 'date':
        format_date_axis(fig, axis='y')
    elif y_format == 'number':
        format_number_axis(fig, axis='y')
    
    # Apply labels if provided
    if x_label:
        fig.update_xaxes(title_text=x_label)
    if y_label:
        fig.update_yaxes(title_text=y_label)
    
    return fig

def format_percentage_axis(fig, axis='y', decimals=1):
    """
    Format the specified axis (default y) as percentage.
    
    Args:
        fig: Plotly figure object
        axis: Which axis to format ('x' or 'y')
        decimals: Number of decimal places (default: 1)
    """
    fmt = f'.{decimals}%'
    if axis == 'y':
        fig.update_yaxes(
            tickformat=fmt, 
            tickfont=dict(size=CHART_FONT_SIZE)
        )
    elif axis == 'x':
        fig.update_xaxes(
            tickformat=fmt, 
            tickfont=dict(size=CHART_FONT_SIZE)
        )
    return fig

def format_date_axis(fig, axis='x', date_format=SHORT_DATE_FORMAT):
    """
    Format the specified axis (default x) as date with the given format.
    
    Args:
        fig: Plotly figure object
        axis: Which axis to format ('x' or 'y')
        date_format: Date format string (default from config)
    """
    if axis == 'x':
        fig.update_xaxes(
            tickformatstops=[dict(dtickrange=[None, None], value=date_format)], 
            tickfont=dict(size=CHART_FONT_SIZE)
        )
    elif axis == 'y':
        fig.update_yaxes(
            tickformatstops=[dict(dtickrange=[None, None], value=date_format)], 
            tickfont=dict(size=CHART_FONT_SIZE)
        )
    return fig 