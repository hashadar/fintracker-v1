import plotly.express as px
import plotly.graph_objs as go

from utils.design.tokens import (  # Chart configuration tokens
    CHART_AXIS_LINE_COLOR,
    CHART_AXIS_LINE_WIDTH,
    CHART_FONT_FAMILY,
    CHART_FONT_SIZE,
    CHART_GRID_COLOR,
    CHART_GRID_WIDTH,
    CHART_HEIGHT,
    CHART_MARGIN,
    CHART_PAPER_BGCOLOR,
    CHART_PLOT_BGCOLOR,
    CHART_TEMPLATE,
    NEUTRAL_500,
)

# --- Base Chart Functions ---


def create_time_series_chart(
    df,
    x_col,
    y_cols,
    x_label="Month",
    y_label="Value",
    x_format=None,
    y_format=None,
    height=CHART_HEIGHT,
    show_legend=True,
    confidence_band=None,
):
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
        confidence_band (dict): A dictionary with 'lower' and 'upper' keys for confidence bands.
    """
    if df.empty or not y_cols:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16, color=NEUTRAL_500),
        )
        fig.update_layout(
            height=height,
            font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
            plot_bgcolor=CHART_PLOT_BGCOLOR,
            paper_bgcolor=CHART_PAPER_BGCOLOR,
            margin=CHART_MARGIN,
        )
        return fig
    fig = px.line(df, x=x_col, y=y_cols, height=height, template=CHART_TEMPLATE)

    # Add confidence band if provided
    if (
        confidence_band
        and confidence_band["lower"] in df.columns
        and confidence_band["upper"] in df.columns
    ):
        fig.add_trace(
            go.Scatter(
                x=df[x_col],
                y=df[confidence_band["upper"]],
                fill=None,
                mode="lines",
                line=dict(color="rgba(0,0,0,0)"),
                showlegend=False,
            )
        )
        fig.add_trace(
            go.Scatter(
                x=df[x_col],
                y=df[confidence_band["lower"]],
                fill="tonexty",
                mode="lines",
                line=dict(color="rgba(0,0,0,0)"),
                fillcolor="rgba(0,100,80,0.2)",
                showlegend=False,
            )
        )

    fig.update_layout(
        font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
        plot_bgcolor=CHART_PLOT_BGCOLOR,
        paper_bgcolor=CHART_PAPER_BGCOLOR,
        margin=CHART_MARGIN,
        showlegend=show_legend,
        hovermode="x unified",
    )
    fig.update_xaxes(
        title_text=x_label,
        showgrid=True,
        gridwidth=CHART_GRID_WIDTH,
        gridcolor=CHART_GRID_COLOR,
        zeroline=False,
        showline=True,
        linecolor=CHART_AXIS_LINE_COLOR,
        linewidth=CHART_AXIS_LINE_WIDTH,
    )
    fig.update_yaxes(
        title_text=y_label,
        showgrid=True,
        gridwidth=CHART_GRID_WIDTH,
        gridcolor=CHART_GRID_COLOR,
        zeroline=False,
        showline=True,
        linecolor=CHART_AXIS_LINE_COLOR,
        linewidth=CHART_AXIS_LINE_WIDTH,
    )

    # Apply formatting if specified
    if x_format or y_format:
        from .formatting import apply_consistent_axis_formatting

        fig = apply_consistent_axis_formatting(
            fig, x_format=x_format, y_format=y_format, x_label=x_label, y_label=y_label
        )

    return fig


def create_bar_chart(
    df,
    x_col,
    y_cols,
    x_label=None,
    y_label="Value",
    color_col=None,
    x_format=None,
    y_format=None,
    height=CHART_HEIGHT,
    orientation="v",
):
    """
    Create a standardized bar chart.

    Args:
        df: Input DataFrame
        x_col: Column to use for x-axis
        y_cols: Column (str) or list of columns (list) to use for y-axis. A list creates grouped bars.
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
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16, color=NEUTRAL_500),
        )
        fig.update_layout(
            height=height,
            font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
            plot_bgcolor=CHART_PLOT_BGCOLOR,
            paper_bgcolor=CHART_PAPER_BGCOLOR,
            margin=CHART_MARGIN,
        )
        return fig

    # Use x_col name as default x_label if not provided
    if x_label is None:
        x_label = x_col

    fig = px.bar(
        df,
        x=x_col,
        y=y_cols,
        color=color_col,
        height=height,
        orientation=orientation,
        template=CHART_TEMPLATE,
    )

    is_grouped = isinstance(y_cols, list) and len(y_cols) > 1

    fig.update_layout(
        font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
        plot_bgcolor=CHART_PLOT_BGCOLOR,
        paper_bgcolor=CHART_PAPER_BGCOLOR,
        margin=CHART_MARGIN,
        showlegend=(color_col is not None) or is_grouped,
        hovermode="x unified",
        barmode="group" if is_grouped else "relative",
    )
    fig.update_xaxes(
        title_text=x_label,
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor=CHART_AXIS_LINE_COLOR,
        linewidth=CHART_AXIS_LINE_WIDTH,
    )
    fig.update_yaxes(
        title_text=y_label,
        showgrid=True,
        gridwidth=CHART_GRID_WIDTH,
        gridcolor=CHART_GRID_COLOR,
        zeroline=False,
        showline=True,
        linecolor=CHART_AXIS_LINE_COLOR,
        linewidth=CHART_AXIS_LINE_WIDTH,
    )

    # Apply formatting if specified
    if x_format or y_format:
        from .formatting import apply_consistent_axis_formatting

        fig = apply_consistent_axis_formatting(
            fig, x_format=x_format, y_format=y_format, x_label=x_label, y_label=y_label
        )

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
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16, color=NEUTRAL_500),
        )
        fig.update_layout(
            height=height,
            font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
            plot_bgcolor=CHART_PLOT_BGCOLOR,
            paper_bgcolor=CHART_PAPER_BGCOLOR,
            margin=CHART_MARGIN,
        )
        return fig
    fig = px.pie(
        df,
        names=names_col,
        values=values_col,
        hole=hole,
        height=height,
        template=CHART_TEMPLATE,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(
        font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
        plot_bgcolor=CHART_PLOT_BGCOLOR,
        paper_bgcolor=CHART_PAPER_BGCOLOR,
        margin=CHART_MARGIN,
        showlegend=True,
    )
    return fig


def create_histogram(
    df,
    x_col,
    x_label=None,
    y_label="Frequency",
    x_format=None,
    height=CHART_HEIGHT,
    nbins=10,
):
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
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16, color=NEUTRAL_500),
        )
        fig.update_layout(
            height=height,
            font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
            plot_bgcolor=CHART_PLOT_BGCOLOR,
            paper_bgcolor=CHART_PAPER_BGCOLOR,
            margin=CHART_MARGIN,
        )
        return fig

    # Use x_col name as default x_label if not provided
    if x_label is None:
        x_label = x_col

    fig = px.histogram(df, x=x_col, nbins=nbins, height=height, template=CHART_TEMPLATE)
    fig.update_layout(
        font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
        plot_bgcolor=CHART_PLOT_BGCOLOR,
        paper_bgcolor=CHART_PAPER_BGCOLOR,
        margin=CHART_MARGIN,
        showlegend=False,
    )
    fig.update_xaxes(
        title_text=x_label,
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor=CHART_AXIS_LINE_COLOR,
        linewidth=CHART_AXIS_LINE_WIDTH,
    )
    fig.update_yaxes(
        title_text=y_label,
        showgrid=True,
        gridwidth=CHART_GRID_WIDTH,
        gridcolor=CHART_GRID_COLOR,
        zeroline=False,
        showline=True,
        linecolor=CHART_AXIS_LINE_COLOR,
        linewidth=CHART_AXIS_LINE_WIDTH,
    )

    # Apply formatting if specified
    if x_format:
        from .formatting import apply_consistent_axis_formatting

        fig = apply_consistent_axis_formatting(
            fig, x_format=x_format, x_label=x_label, y_label=y_label
        )

    return fig


def create_box_plot(
    df, y_cols, y_label="Value", y_format=None, height=CHART_HEIGHT, color_col=None
):
    """
    Create a standardized box plot chart.

    Args:
        df: Input DataFrame
        y_cols: Column to use for y-axis
        y_label: Label for y-axis (default: "Value")
        y_format: Format type for y-axis ('currency', 'percentage', 'date', 'number')
        height: Chart height
        color_col: Column to use for color coding
    """
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16, color=NEUTRAL_500),
        )
        fig.update_layout(
            height=height,
            font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
            plot_bgcolor=CHART_PLOT_BGCOLOR,
            paper_bgcolor=CHART_PAPER_BGCOLOR,
            margin=CHART_MARGIN,
        )
        return fig
    fig = px.box(df, y=y_cols, color=color_col, height=height, template=CHART_TEMPLATE)
    fig.update_layout(
        font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
        plot_bgcolor=CHART_PLOT_BGCOLOR,
        paper_bgcolor=CHART_PAPER_BGCOLOR,
        margin=CHART_MARGIN,
        showlegend=color_col is not None,
    )
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor=CHART_AXIS_LINE_COLOR,
        linewidth=CHART_AXIS_LINE_WIDTH,
    )
    fig.update_yaxes(
        title_text=y_label,
        showgrid=True,
        gridwidth=CHART_GRID_WIDTH,
        gridcolor=CHART_GRID_COLOR,
        zeroline=False,
        showline=True,
        linecolor=CHART_AXIS_LINE_COLOR,
        linewidth=CHART_AXIS_LINE_WIDTH,
    )

    # Apply formatting if specified
    if y_format:
        from .formatting import apply_consistent_axis_formatting

        fig = apply_consistent_axis_formatting(fig, y_format=y_format, y_label=y_label)

    return fig


def create_area_chart(
    df,
    x_col,
    y_cols,
    x_label="Month",
    y_label="Value",
    x_format=None,
    y_format=None,
    height=CHART_HEIGHT,
    stacked=False,
):
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
        stacked: Whether to create a stacked area chart (default: False)
    """
    if df.empty or not y_cols:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16, color=NEUTRAL_500),
        )
        fig.update_layout(
            height=height,
            font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
            plot_bgcolor=CHART_PLOT_BGCOLOR,
            paper_bgcolor=CHART_PAPER_BGCOLOR,
            margin=CHART_MARGIN,
        )
        return fig
    if stacked:
        # For stacked area chart, use go.Figure with stackgroup
        fig = go.Figure()

        # Sort the dataframe by x_col to ensure proper stacking
        df_sorted = df.sort_values(x_col)

        for col in y_cols:
            fig.add_trace(
                go.Scatter(
                    x=df_sorted[x_col],
                    y=df_sorted[col],
                    name=col,
                    fill="tonexty",
                    stackgroup="one",
                    mode="lines",
                )
            )

        fig.update_layout(
            height=height,
            template=CHART_TEMPLATE,
            font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
            plot_bgcolor=CHART_PLOT_BGCOLOR,
            paper_bgcolor=CHART_PAPER_BGCOLOR,
            margin=CHART_MARGIN,
            showlegend=True,
            hovermode="x unified",
        )

        fig.update_xaxes(
            title_text=x_label,
            showgrid=True,
            gridwidth=CHART_GRID_WIDTH,
            gridcolor=CHART_GRID_COLOR,
            zeroline=False,
            showline=True,
            linecolor=CHART_AXIS_LINE_COLOR,
            linewidth=CHART_AXIS_LINE_WIDTH,
        )
        fig.update_yaxes(
            title_text=y_label,
            showgrid=True,
            gridwidth=CHART_GRID_WIDTH,
            gridcolor=CHART_GRID_COLOR,
            zeroline=False,
            showline=True,
            linecolor=CHART_AXIS_LINE_COLOR,
            linewidth=CHART_AXIS_LINE_WIDTH,
        )

        # Apply formatting if specified
        if x_format or y_format:
            from .formatting import apply_consistent_axis_formatting

            fig = apply_consistent_axis_formatting(
                fig,
                x_format=x_format,
                y_format=y_format,
                x_label=x_label,
                y_label=y_label,
            )

        return fig
    else:
        fig = px.area(df, x=x_col, y=y_cols, height=height, template=CHART_TEMPLATE)
    fig.update_layout(
        font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
        plot_bgcolor=CHART_PLOT_BGCOLOR,
        paper_bgcolor=CHART_PAPER_BGCOLOR,
        margin=CHART_MARGIN,
        showlegend=True,
        hovermode="x unified",
    )
    fig.update_xaxes(
        title_text=x_label,
        showgrid=True,
        gridwidth=CHART_GRID_WIDTH,
        gridcolor=CHART_GRID_COLOR,
        zeroline=False,
        showline=True,
        linecolor=CHART_AXIS_LINE_COLOR,
        linewidth=CHART_AXIS_LINE_WIDTH,
    )
    fig.update_yaxes(
        title_text=y_label,
        showgrid=True,
        gridwidth=CHART_GRID_WIDTH,
        gridcolor=CHART_GRID_COLOR,
        zeroline=False,
        showline=True,
        linecolor=CHART_AXIS_LINE_COLOR,
        linewidth=CHART_AXIS_LINE_WIDTH,
    )

    # Apply formatting if specified
    if x_format or y_format:
        from .formatting import apply_consistent_axis_formatting

        fig = apply_consistent_axis_formatting(
            fig, x_format=x_format, y_format=y_format, x_label=x_label, y_label=y_label
        )

    return fig
