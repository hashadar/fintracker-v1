"""Main Streamlit application for financial dashboard."""

# Streamlit app for financial dashboard and deep-dive analytics
# Author: hasha dar
#
# This script provides:
# - An overview dashboard for all assets
# - Deep-dive analysis pages for Cash, Investments, Pensions, and All Assets
# - Compact, information-rich layouts with KPI cards and advanced time series analytics

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from utils import (
    ASSET_TYPES,
    CUSTOM_STYLE,
    PAGE_TITLE,
    PAGE_DESCRIPTION,
    load_data,
    filter_data_by_date_range,
    get_month_range,
    calculate_asset_type_metrics,
    calculate_overall_metrics,
    calculate_allocation_metrics,
    create_asset_type_time_series,
    create_asset_type_breakdown,
    display_asset_type_metrics
)
from utils.visualizations import kpi_card

# Set page config
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
st.markdown(CUSTOM_STYLE, unsafe_allow_html=True)

# Title and description
st.markdown(f"""
    <h1 style='text-align: center; margin-bottom: 1rem;'>{PAGE_TITLE}</h1>
    <p style='text-align: center; margin-bottom: 2rem;'>{PAGE_DESCRIPTION}</p>
    """, unsafe_allow_html=True)

def main():
    # Load data
    df = load_data()
    if df is None:
        st.error("Failed to load data. Please check the data file.")
        return
    
    # Sidebar: Only month range selector
    st.sidebar.header("Filters")
    month_options, min_month, max_month = get_month_range(df)
    current_start_idx = 0
    current_end_idx = len(month_options) - 1
    start_month, end_month = st.sidebar.select_slider(
        "Select Month Range",
        options=month_options,
        value=(month_options[current_start_idx], month_options[current_end_idx])
    )
    df = filter_data_by_date_range(df, start_month, end_month)
    
    # Add sidebar navigation for deep-dive pages
    page = st.sidebar.radio(
        "Go to page:",
        ["Overview", "Cash Deep Dive", "Investments Deep Dive", "Pensions Deep Dive", "All Assets Deep Dive"]
    )

    if page == "Overview":
        # --- ALL ASSETS OVERVIEW ---
        st.header("All Assets Overview")
        allocation_metrics, latest_month, prev_month, ytd_start_month = calculate_allocation_metrics(df)
        st.caption(f"Latest Month: {latest_month.strftime('%B %Y')} | Previous Month: {prev_month.strftime('%B %Y') if prev_month is not pd.NaT else 'N/A'} | YTD Start: {ytd_start_month.strftime('%B %Y') if ytd_start_month is not pd.NaT else 'N/A'}")
        col1, col2, col3, col4 = st.columns(4)
        # Grand Total
        with col1:
            kpi_card(
                label="Grand Total",
                value=f"£{allocation_metrics['Total']['current']:,.2f}",
                mom_delta=(f"£{allocation_metrics['Total']['mom_increase']:,.2f} MoM" if allocation_metrics['Total']['mom_increase'] is not None else None),
                ytd_delta=(f"£{allocation_metrics['Total']['ytd_increase']:,.2f} YTD" if allocation_metrics['Total']['ytd_increase'] is not None else None),
                mom_color="normal" if allocation_metrics['Total']['mom_increase'] is not None and allocation_metrics['Total']['mom_increase'] >= 0 else "inverse",
                ytd_color="normal" if allocation_metrics['Total']['ytd_increase'] is not None and allocation_metrics['Total']['ytd_increase'] >= 0 else "inverse"
            )
        # Cash
        cash = allocation_metrics.get('Cash', {})
        with col2:
            kpi_card(
                label="Current Cash Position",
                value=f"£{cash.get('current', 0):,.2f}",
                mom_delta=(f"{cash.get('mom_pct_increase', 0):+.2f}% MoM" if cash.get('mom_pct_increase') is not None else None),
                ytd_delta=(f"{cash.get('ytd_pct_increase', 0):+.2f}% YTD" if cash.get('ytd_pct_increase') is not None else None),
                mom_color="normal" if cash.get('mom_pct_increase', 0) >= 0 else "inverse",
                ytd_color="normal" if cash.get('ytd_pct_increase', 0) >= 0 else "inverse"
            )
            kpi_card(
                label="Current Cash Allocation",
                value=f"{cash.get('allocation', 0):.2f}%",
                mom_delta=(f"{cash.get('allocation_change', 0):+.2f}% MoM" if cash.get('allocation_change') is not None else None),
                ytd_delta=(f"{cash.get('ytd_allocation_change', 0):+.2f}% YTD" if cash.get('ytd_allocation_change') is not None else None),
                mom_color="normal" if cash.get('allocation_change', 0) >= 0 else "inverse",
                ytd_color="normal" if cash.get('ytd_allocation_change', 0) >= 0 else "inverse"
            )
        # Pension
        pension = allocation_metrics.get('Pensions', {})
        with col3:
            kpi_card(
                label="Current Pension Position",
                value=f"£{pension.get('current', 0):,.2f}",
                mom_delta=(f"{pension.get('mom_pct_increase', 0):+.2f}% MoM" if pension.get('mom_pct_increase') is not None else None),
                ytd_delta=(f"{pension.get('ytd_pct_increase', 0):+.2f}% YTD" if pension.get('ytd_pct_increase') is not None else None),
                mom_color="normal" if pension.get('mom_pct_increase', 0) >= 0 else "inverse",
                ytd_color="normal" if pension.get('ytd_pct_increase', 0) >= 0 else "inverse"
            )
            kpi_card(
                label="Current Pension Allocation",
                value=f"{pension.get('allocation', 0):.2f}%",
                mom_delta=(f"{pension.get('allocation_change', 0):+.2f}% MoM" if pension.get('allocation_change') is not None else None),
                ytd_delta=(f"{pension.get('ytd_allocation_change', 0):+.2f}% YTD" if pension.get('ytd_allocation_change') is not None else None),
                mom_color="normal" if pension.get('allocation_change', 0) >= 0 else "inverse",
                ytd_color="normal" if pension.get('ytd_allocation_change', 0) >= 0 else "inverse"
            )
        # Investments
        invest = allocation_metrics.get('Investments', {})
        with col4:
            kpi_card(
                label="Current Investment Position",
                value=f"£{invest.get('current', 0):,.2f}",
                mom_delta=(f"{invest.get('mom_pct_increase', 0):+.2f}% MoM" if invest.get('mom_pct_increase') is not None else None),
                ytd_delta=(f"{invest.get('ytd_pct_increase', 0):+.2f}% YTD" if invest.get('ytd_pct_increase') is not None else None),
                mom_color="normal" if invest.get('mom_pct_increase', 0) >= 0 else "inverse",
                ytd_color="normal" if invest.get('ytd_pct_increase', 0) >= 0 else "inverse"
            )
            kpi_card(
                label="Current Investment Allocation",
                value=f"{invest.get('allocation', 0):.2f}%",
                mom_delta=(f"{invest.get('allocation_change', 0):+.2f}% MoM" if invest.get('allocation_change') is not None else None),
                ytd_delta=(f"{invest.get('ytd_allocation_change', 0):+.2f}% YTD" if invest.get('ytd_allocation_change') is not None else None),
                mom_color="normal" if invest.get('allocation_change', 0) >= 0 else "inverse",
                ytd_color="normal" if invest.get('ytd_allocation_change', 0) >= 0 else "inverse"
            )
        st.markdown("---")

        # --- ALL ASSETS GRAPHS & ANALYSIS ---
        st.subheader("All Assets - Trends and Allocation")
        if not df.empty:
            df_month = df.copy()
            df_month['Month'] = df_month['Timestamp'].dt.to_period('M').dt.to_timestamp()
            total_trend = df_month.groupby('Month')['Value'].sum().reset_index()
            comp_trend = df_month.groupby(['Month', 'Asset_Type'])['Value'].sum().reset_index()
            comp_pivot = comp_trend.pivot(index='Month', columns='Asset_Type', values='Value').fillna(0)
            latest_month = df_month['Month'].max()
            latest_alloc = df_month[df_month['Month'] == latest_month].groupby('Asset_Type')['Value'].sum().reset_index()
            # Use columns for compact layout
            col1, col2, col3 = st.columns([2,2,1])
            with col1:
                st.plotly_chart(
                    px.line(total_trend, x='Month', y='Value', title='Total Portfolio Value Over Time', labels={'Value': 'Total Value (GBP)', 'Month': 'Month'}),
                    use_container_width=True
                )
            with col2:
                st.plotly_chart(
                    px.area(comp_pivot, x=comp_pivot.index, y=comp_pivot.columns, title='Asset Type Composition Over Time', labels={'value': 'Value (GBP)', 'Month': 'Month', 'variable': 'Asset Type'}),
                    use_container_width=True
                )
            with col3:
                st.plotly_chart(
                    px.pie(latest_alloc, values='Value', names='Asset_Type', title=f'Asset Type Allocation ({latest_month.strftime("%B %Y")})'),
                    use_container_width=True
                )
        st.markdown("---")

        # --- TABS FOR EACH ASSET TYPE ---
        tabs = st.tabs(["Cash", "Investments", "Pensions"])
        for tab, asset_type in zip(tabs, ["Cash", "Investments", "Pensions"]):
            with tab:
                metrics = calculate_asset_type_metrics(df, asset_type)
                if metrics is None:
                    st.info(f"No data for {asset_type}.")
                    continue
                st.markdown(display_asset_type_metrics(metrics, asset_type), unsafe_allow_html=True)
                if metrics['latest_platform_breakdown']:
                    st.markdown("#### Latest Month Platform Breakdown")
                    platform_cols = st.columns(len(metrics['latest_platform_breakdown']))
                    for (platform, value), col in zip(metrics['latest_platform_breakdown'].items(), platform_cols):
                        with col:
                            st.metric(
                                label=platform,
                                value=f"£{value:,.2f}",
                                delta=None
                            )
                # Time series and area charts
                fig_value, fig_composition = create_asset_type_time_series(df, asset_type)
                fig_platform, fig_asset = create_asset_type_breakdown(df, asset_type)
                charts = [fig for fig in [fig_value, fig_composition, fig_platform, fig_asset] if fig is not None]
                if len(charts) == 4:
                    row1, row2 = st.columns(2), st.columns(2)
                    with row1[0]:
                        st.plotly_chart(fig_value, use_container_width=True)
                    with row1[1]:
                        st.plotly_chart(fig_composition, use_container_width=True)
                    with row2[0]:
                        st.plotly_chart(fig_platform, use_container_width=True)
                    with row2[1]:
                        st.plotly_chart(fig_asset, use_container_width=True)
                elif len(charts) == 3:
                    col1, col2, col3 = st.columns(3)
                    figs = [fig for fig in [fig_value, fig_composition, fig_platform, fig_asset] if fig is not None]
                    with col1:
                        st.plotly_chart(figs[0], use_container_width=True)
                    with col2:
                        st.plotly_chart(figs[1], use_container_width=True)
                    with col3:
                        st.plotly_chart(figs[2], use_container_width=True)
                elif len(charts) == 2:
                    col1, col2 = st.columns(2)
                    figs = [fig for fig in [fig_value, fig_composition, fig_platform, fig_asset] if fig is not None]
                    with col1:
                        st.plotly_chart(figs[0], use_container_width=True)
                    with col2:
                        st.plotly_chart(figs[1], use_container_width=True)
                elif len(charts) == 1:
                    st.plotly_chart(charts[0], use_container_width=True)
                st.markdown("---")
        # Raw data view in an expander
        with st.expander("Raw Data View", expanded=False):
            st.dataframe(df, use_container_width=True)

    elif page == "Cash Deep Dive":
        st.header("Cash Deep Dive")
        cash_df = df[df['Asset_Type'] == 'Cash'].copy()
        if cash_df.empty:
            st.info("No cash data available.")
        else:
            # Derive month
            cash_df['Month'] = cash_df['Timestamp'].dt.to_period('M').dt.to_timestamp()
            cash_monthly = cash_df.groupby('Month')['Value'].sum().reset_index()
            cash_monthly['RollingAvg'] = cash_monthly['Value'].rolling(window=3).mean()
            cash_monthly['RollingStd'] = cash_monthly['Value'].rolling(window=3).std()
            running_max = cash_monthly['Value'].cummax()
            drawdown = (cash_monthly['Value'] - running_max) / running_max
            cash_monthly['Drawdown'] = drawdown
            cash_monthly['MoM'] = cash_monthly['Value'].pct_change()
            best_month = cash_monthly.loc[cash_monthly['MoM'].idxmax()]
            worst_month = cash_monthly.loc[cash_monthly['MoM'].idxmin()]
            max_drawdown = drawdown.min()
            # KPI cards in a row
            kpi1, kpi2, kpi3 = st.columns(3)
            with kpi1:
                kpi_card(
                    label="Max Drawdown",
                    value=f"{max_drawdown:.2%}",
                    mom_delta=None,
                    ytd_delta=None
                )
            with kpi2:
                kpi_card(
                    label="Best Month (MoM %)",
                    value=f"{best_month['Month'].strftime('%b %Y')}: {best_month['MoM']*100:.2f}%",
                    mom_delta=None,
                    ytd_delta=None
                )
            with kpi3:
                kpi_card(
                    label="Worst Month (MoM %)",
                    value=f"{worst_month['Month'].strftime('%b %Y')}: {worst_month['MoM']*100:.2f}%",
                    mom_delta=None,
                    ytd_delta=None
                )
            # Charts in 3 columns
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**Value & 3-Month Rolling Avg**")
                st.plotly_chart(
                    px.line(cash_monthly, x='Month', y=['Value', 'RollingAvg'],
                            labels={'value': 'Value (GBP)', 'Month': 'Month'},
                            title=None),
                    use_container_width=True
                )
            with col2:
                st.markdown("**Rolling Volatility (Std Dev)**")
                st.plotly_chart(
                    px.line(cash_monthly, x='Month', y='RollingStd', labels={'RollingStd': 'Std Dev', 'Month': 'Month'}, title=None),
                    use_container_width=True
                )
            with col3:
                st.markdown("**MoM % Change Over Time**")
                mom_clean = cash_monthly[['Month', 'MoM']].dropna()
                if mom_clean.empty:
                    st.info("Not enough data for a meaningful time series.")
                else:
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=mom_clean['Month'], y=mom_clean['MoM'], mode='lines+markers'))
                    fig.update_layout(yaxis_tickformat='.2%', xaxis_title='Month', yaxis_title='MoM % Change', showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
            # Boxplot and Drawdown in two columns below
            col4, col5 = st.columns(2)
            with col4:
                st.markdown("**Boxplot of Monthly Value**")
                st.plotly_chart(
                    px.box(cash_monthly, y='Value', title=None),
                    use_container_width=True
                )
            with col5:
                st.markdown("**Drawdown Over Time**")
                st.plotly_chart(
                    px.line(cash_monthly, x='Month', y='Drawdown', labels={'Drawdown': 'Drawdown', 'Month': 'Month'}, title=None),
                    use_container_width=True,
                    height=200
                )
            # Downloadable data
            st.download_button(
                label="Download Cash Monthly Data as CSV",
                data=cash_monthly.to_csv(index=False),
                file_name="cash_monthly.csv",
                mime="text/csv"
            )

    elif page == "Investments Deep Dive":
        st.header("Investments Deep Dive")
        inv_df = df[df['Asset_Type'] == 'Investments'].copy()
        if inv_df.empty:
            st.info("No investments data available.")
        else:
            inv_df['Month'] = inv_df['Timestamp'].dt.to_period('M').dt.to_timestamp()
            inv_monthly = inv_df.groupby('Month')['Value'].sum().reset_index()
            inv_monthly['RollingAvg'] = inv_monthly['Value'].rolling(window=3).mean()
            inv_monthly['RollingStd'] = inv_monthly['Value'].rolling(window=3).std()
            running_max = inv_monthly['Value'].cummax()
            drawdown = (inv_monthly['Value'] - running_max) / running_max
            inv_monthly['Drawdown'] = drawdown
            inv_monthly['MoM'] = inv_monthly['Value'].pct_change()
            best_month = inv_monthly.loc[inv_monthly['MoM'].idxmax()]
            worst_month = inv_monthly.loc[inv_monthly['MoM'].idxmin()]
            max_drawdown = drawdown.min()
            kpi1, kpi2, kpi3 = st.columns(3)
            with kpi1:
                kpi_card(
                    label="Max Drawdown",
                    value=f"{max_drawdown:.2%}",
                    mom_delta=None,
                    ytd_delta=None
                )
            with kpi2:
                kpi_card(
                    label="Best Month (MoM %)",
                    value=f"{best_month['Month'].strftime('%b %Y')}: {best_month['MoM']*100:.2f}%",
                    mom_delta=None,
                    ytd_delta=None
                )
            with kpi3:
                kpi_card(
                    label="Worst Month (MoM %)",
                    value=f"{worst_month['Month'].strftime('%b %Y')}: {worst_month['MoM']*100:.2f}%",
                    mom_delta=None,
                    ytd_delta=None
                )
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**Value & 3-Month Rolling Avg**")
                st.plotly_chart(
                    px.line(inv_monthly, x='Month', y=['Value', 'RollingAvg'],
                            labels={'value': 'Value (GBP)', 'Month': 'Month'},
                            title=None),
                    use_container_width=True
                )
            with col2:
                st.markdown("**Rolling Volatility (Std Dev)**")
                st.plotly_chart(
                    px.line(inv_monthly, x='Month', y='RollingStd', labels={'RollingStd': 'Std Dev', 'Month': 'Month'}, title=None),
                    use_container_width=True
                )
            with col3:
                st.markdown("**MoM % Change Over Time**")
                mom_clean = inv_monthly[['Month', 'MoM']].dropna()
                if mom_clean.empty:
                    st.info("Not enough data for a meaningful time series.")
                else:
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=mom_clean['Month'], y=mom_clean['MoM'], mode='lines+markers'))
                    fig.update_layout(yaxis_tickformat='.2%', xaxis_title='Month', yaxis_title='MoM % Change', showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
            col4, col5 = st.columns(2)
            with col4:
                st.markdown("**Boxplot of Monthly Value**")
                st.plotly_chart(
                    px.box(inv_monthly, y='Value', title=None),
                    use_container_width=True
                )
            with col5:
                st.markdown("**Drawdown Over Time**")
                st.plotly_chart(
                    px.line(inv_monthly, x='Month', y='Drawdown', labels={'Drawdown': 'Drawdown', 'Month': 'Month'}, title=None),
                    use_container_width=True,
                    height=200
                )
            st.download_button(
                label="Download Investments Monthly Data as CSV",
                data=inv_monthly.to_csv(index=False),
                file_name="investments_monthly.csv",
                mime="text/csv"
            )

    elif page == "Pensions Deep Dive":
        st.header("Pensions Deep Dive")
        pen_df = df[df['Asset_Type'] == 'Pensions'].copy()
        if pen_df.empty:
            st.info("No pensions data available.")
        else:
            pen_df['Month'] = pen_df['Timestamp'].dt.to_period('M').dt.to_timestamp()
            pen_monthly = pen_df.groupby('Month')['Value'].sum().reset_index()
            pen_monthly['RollingAvg'] = pen_monthly['Value'].rolling(window=3).mean()
            pen_monthly['RollingStd'] = pen_monthly['Value'].rolling(window=3).std()
            running_max = pen_monthly['Value'].cummax()
            drawdown = (pen_monthly['Value'] - running_max) / running_max
            pen_monthly['Drawdown'] = drawdown
            pen_monthly['MoM'] = pen_monthly['Value'].pct_change()
            best_month = pen_monthly.loc[pen_monthly['MoM'].idxmax()]
            worst_month = pen_monthly.loc[pen_monthly['MoM'].idxmin()]
            max_drawdown = drawdown.min()
            kpi1, kpi2, kpi3 = st.columns(3)
            with kpi1:
                kpi_card(
                    label="Max Drawdown",
                    value=f"{max_drawdown:.2%}",
                    mom_delta=None,
                    ytd_delta=None
                )
            with kpi2:
                kpi_card(
                    label="Best Month (MoM %)",
                    value=f"{best_month['Month'].strftime('%b %Y')}: {best_month['MoM']*100:.2f}%",
                    mom_delta=None,
                    ytd_delta=None
                )
            with kpi3:
                kpi_card(
                    label="Worst Month (MoM %)",
                    value=f"{worst_month['Month'].strftime('%b %Y')}: {worst_month['MoM']*100:.2f}%",
                    mom_delta=None,
                    ytd_delta=None
                )
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**Value & 3-Month Rolling Avg**")
                st.plotly_chart(
                    px.line(pen_monthly, x='Month', y=['Value', 'RollingAvg'],
                            labels={'value': 'Value (GBP)', 'Month': 'Month'},
                            title=None),
                    use_container_width=True
                )
            with col2:
                st.markdown("**Rolling Volatility (Std Dev)**")
                st.plotly_chart(
                    px.line(pen_monthly, x='Month', y='RollingStd', labels={'RollingStd': 'Std Dev', 'Month': 'Month'}, title=None),
                    use_container_width=True
                )
            with col3:
                st.markdown("**MoM % Change Over Time**")
                mom_clean = pen_monthly[['Month', 'MoM']].dropna()
                if mom_clean.empty:
                    st.info("Not enough data for a meaningful time series.")
                else:
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=mom_clean['Month'], y=mom_clean['MoM'], mode='lines+markers'))
                    fig.update_layout(yaxis_tickformat='.2%', xaxis_title='Month', yaxis_title='MoM % Change', showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
            col4, col5 = st.columns(2)
            with col4:
                st.markdown("**Boxplot of Monthly Value**")
                st.plotly_chart(
                    px.box(pen_monthly, y='Value', title=None),
                    use_container_width=True
                )
            with col5:
                st.markdown("**Drawdown Over Time**")
                st.plotly_chart(
                    px.line(pen_monthly, x='Month', y='Drawdown', labels={'Drawdown': 'Drawdown', 'Month': 'Month'}, title=None),
                    use_container_width=True,
                    height=200
                )
            st.download_button(
                label="Download Pensions Monthly Data as CSV",
                data=pen_monthly.to_csv(index=False),
                file_name="pensions_monthly.csv",
                mime="text/csv"
            )

    elif page == "All Assets Deep Dive":
        st.header("All Assets Deep Dive")
        all_df = df.copy()
        all_df['Month'] = all_df['Timestamp'].dt.to_period('M').dt.to_timestamp()
        all_monthly = all_df.groupby('Month')['Value'].sum().reset_index()
        all_monthly['RollingAvg'] = all_monthly['Value'].rolling(window=3).mean()
        all_monthly['RollingStd'] = all_monthly['Value'].rolling(window=3).std()
        running_max = all_monthly['Value'].cummax()
        drawdown = (all_monthly['Value'] - running_max) / running_max
        all_monthly['Drawdown'] = drawdown
        all_monthly['MoM'] = all_monthly['Value'].pct_change()
        best_month = all_monthly.loc[all_monthly['MoM'].idxmax()]
        worst_month = all_monthly.loc[all_monthly['MoM'].idxmin()]
        max_drawdown = drawdown.min()
        kpi1, kpi2, kpi3 = st.columns(3)
        with kpi1:
            kpi_card(
                label="Max Drawdown",
                value=f"{max_drawdown:.2%}",
                mom_delta=None,
                ytd_delta=None
            )
        with kpi2:
            kpi_card(
                label="Best Month (MoM %)",
                value=f"{best_month['Month'].strftime('%b %Y')}: {best_month['MoM']*100:.2f}%",
                mom_delta=None,
                ytd_delta=None
            )
        with kpi3:
            kpi_card(
                label="Worst Month (MoM %)",
                value=f"{worst_month['Month'].strftime('%b %Y')}: {worst_month['MoM']*100:.2f}%",
                mom_delta=None,
                ytd_delta=None
            )
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Value & 3-Month Rolling Avg**")
            st.plotly_chart(
                px.line(all_monthly, x='Month', y=['Value', 'RollingAvg'],
                        labels={'value': 'Value (GBP)', 'Month': 'Month'},
                        title=None),
                use_container_width=True
            )
        with col2:
            st.markdown("**Rolling Volatility (Std Dev)**")
            st.plotly_chart(
                px.line(all_monthly, x='Month', y='RollingStd', labels={'RollingStd': 'Std Dev', 'Month': 'Month'}, title=None),
                use_container_width=True
            )
        with col3:
            st.markdown("**MoM % Change Over Time**")
            mom_clean = all_monthly[['Month', 'MoM']].dropna()
            if mom_clean.empty:
                st.info("Not enough data for a meaningful time series.")
            else:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=mom_clean['Month'], y=mom_clean['MoM'], mode='lines+markers'))
                fig.update_layout(yaxis_tickformat='.2%', xaxis_title='Month', yaxis_title='MoM % Change', showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
        col4, col5 = st.columns(2)
        with col4:
            st.markdown("**Boxplot of Monthly Value**")
            st.plotly_chart(
                px.box(all_monthly, y='Value', title=None),
                use_container_width=True
            )
        with col5:
            st.markdown("**Drawdown Over Time**")
            st.plotly_chart(
                px.line(all_monthly, x='Month', y='Drawdown', labels={'Drawdown': 'Drawdown', 'Month': 'Month'}, title=None),
                use_container_width=True,
                height=200
            )
        st.download_button(
            label="Download All Assets Monthly Data as CSV",
            data=all_monthly.to_csv(index=False),
            file_name="all_assets_monthly.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()