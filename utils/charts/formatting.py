# Formatting helpers for charts

from utils.design.tokens import CHART_FONT_SIZE

def format_currency_axis(fig, axis='y'):
    """
    Format the specified axis (default y) as GBP currency.
    """
    if axis == 'y':
        fig.update_yaxes(tickprefix='£', separatethousands=True, tickformat=',.2f', tickfont=dict(size=CHART_FONT_SIZE))
    elif axis == 'x':
        fig.update_xaxes(tickprefix='£', separatethousands=True, tickformat=',.2f', tickfont=dict(size=CHART_FONT_SIZE))
    return fig

def format_percentage_axis(fig, axis='y', decimals=1):
    """
    Format the specified axis (default y) as percentage.
    """
    fmt = f'.{decimals}%'
    if axis == 'y':
        fig.update_yaxes(tickformat=fmt, tickfont=dict(size=CHART_FONT_SIZE))
    elif axis == 'x':
        fig.update_xaxes(tickformat=fmt, tickfont=dict(size=CHART_FONT_SIZE))
    return fig

def format_date_axis(fig, axis='x', date_format='%b %Y'):
    """
    Format the specified axis (default x) as date with the given format.
    """
    if axis == 'x':
        fig.update_xaxes(tickformatstops=[dict(dtickrange=[None, None], value=date_format)], tickfont=dict(size=CHART_FONT_SIZE))
    elif axis == 'y':
        fig.update_yaxes(tickformatstops=[dict(dtickrange=[None, None], value=date_format)], tickfont=dict(size=CHART_FONT_SIZE))
    return fig 