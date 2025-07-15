import streamlit as st


def create_metric_grid(metrics_list, cols=4):
    """
    Display a list of metric cards in a responsive grid layout.
    Args:
        metrics_list (list of callables): Each item is a function that renders a metric card (e.g., a lambda or partial).
        cols (int): Number of columns in the grid.
    """
    columns = st.columns(cols)
    for i, metric in enumerate(metrics_list):
        with columns[i % cols]:
            # Add container with consistent height for better alignment
            st.markdown('<div style="height: 100%; display: flex; flex-direction: column;">', unsafe_allow_html=True)
            metric()
            st.markdown('</div>', unsafe_allow_html=True)


def create_chart_grid(charts_list, cols=2):
    """
    Display a list of charts in a responsive grid layout.
    Args:
        charts_list (list of callables): Each item is a function that renders a chart (e.g., a lambda or partial).
        cols (int): Number of columns in the grid.
    """
    columns = st.columns(cols)
    for i, chart in enumerate(charts_list):
        with columns[i % cols]:
            chart()


def create_section_header(title, icon="📊"):
    """
    Render a standardized section header with an optional icon.
    Args:
        title (str): Section title.
        icon (str): Emoji or icon to display before the title.
    """
    st.markdown(f"### {icon} {title}")


def create_page_header(title, description):
    """
    Render a standardized page header with a title and description.
    Args:
        title (str): Page title.
        description (str): Short description or subtitle.
    """
    st.markdown(f"""
        <h1 style='margin-bottom:0.5rem'>{title}</h1>
        <p style='color:var(--text-secondary);margin-bottom:2rem'>{description}</p>
    """, unsafe_allow_html=True) 