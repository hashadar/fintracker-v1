import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
from utils import (
    load_data,
    calculate_allocation_metrics,
    create_asset_type_time_series,
    create_asset_type_breakdown,
    display_asset_type_metrics,
    calculate_asset_type_metrics
)
from utils.visualizations import kpi_card

# Load data at the top of the page
df = load_data()

# Ensure data is loaded before rendering the page
if df is not None:
    st.header("All Assets Overview")
    allocation_metrics, latest_month, prev_month, ytd_start_month = calculate_allocation_metrics(df)
    st.caption(f"Latest Month: {latest_month.strftime('%B %Y')} | Previous Month: {prev_month.strftime('%B %Y') if prev_month is not None else 'N/A'} | YTD Start: {ytd_start_month.strftime('%B %Y') if ytd_start_month is not None else 'N/A'}")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        kpi_card(
            label="Grand Total",
            value=f"£{allocation_metrics['Total']['current']:,.2f}",
            mom_delta=(f"£{allocation_metrics['Total']['mom_increase']:,.2f} MoM" if allocation_metrics['Total']['mom_increase'] is not None else None),
            ytd_delta=(f"£{allocation_metrics['Total']['ytd_increase']:,.2f} YTD" if allocation_metrics['Total']['ytd_increase'] is not None else None),
            mom_color="normal" if allocation_metrics['Total']['mom_increase'] is not None and allocation_metrics['Total']['mom_increase'] >= 0 else "inverse",
            ytd_color="normal" if allocation_metrics['Total']['ytd_increase'] is not None and allocation_metrics['Total']['ytd_increase'] >= 0 else "inverse"
        )
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
                px.pie(latest_alloc, values='Value', names='Asset_Type', title=f'Asset Type Allocation ({latest_month.strftime('%B %Y')})'),
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
    with st.expander("Raw Data View", expanded=False):
        st.dataframe(df, use_container_width=True)
else:
    st.error("Data could not be loaded. Please check your data file.") 