import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from utils import (
    load_data,
    calculate_allocation_metrics
)
from utils.design.cards import simple_card, complex_emphasis_card, complex_card, emphasis_card
from utils.charts import create_time_series_chart, create_bar_chart, create_histogram, create_pie_chart
from utils.design.tokens import (
    BRAND_PRIMARY, BRAND_SUCCESS, BRAND_WARNING, BRAND_ERROR, BRAND_INFO
)
from utils.design.components import create_page_header, create_section_header, create_metric_grid, create_chart_grid

# Page configuration
st.set_page_config(page_title="All Assets - FinTracker", layout="wide")

# Load data
df = load_data()

if df is not None and not df.empty:
    create_page_header(
        title="📊 All Assets Analytics",
        description="Comprehensive analysis across all asset types (Cash, Investments, Pensions)"
    )
    
    # Calculate allocation metrics
    allocation_metrics, latest_month, prev_month, ytd_start_month = calculate_allocation_metrics(df)
    
    # Display time period info
    st.caption(
        f"📅 Latest Month: {latest_month.strftime('%B %Y')} | "
        f"Previous Month: {prev_month.strftime('%B %Y') if prev_month is not None else 'N/A'} | "
        f"YTD Start: {ytd_start_month.strftime('%B %Y') if ytd_start_month is not None else 'N/A'}"
    )
    
    # --- Portfolio Summary Cards ---
    create_section_header("Portfolio Summary", icon="🎯")
    
    # Main portfolio total card
    total_metrics = allocation_metrics.get('Total', {})
    complex_emphasis_card(
        title="Total Portfolio Value",
        metric=f"£{total_metrics.get('current', 0):,.2f}",
        mom_change=(f"£{total_metrics.get('mom_increase', 0):+,.2f} MoM" if total_metrics.get('mom_increase') is not None else None),
        ytd_change=(f"£{total_metrics.get('ytd_increase', 0):+,.2f} YTD" if total_metrics.get('ytd_increase') is not None else None),
        caption=f"Complete financial position as of {latest_month.strftime('%B %Y')}",
        mom_color="normal" if total_metrics.get('mom_increase', 0) >= 0 else "inverse",
        ytd_color="normal" if total_metrics.get('ytd_increase', 0) >= 0 else "inverse",
        emphasis_color=BRAND_PRIMARY
    )
    
    # Asset type breakdown cards using metric grid
    cash_metrics = allocation_metrics.get('Cash', {})
    investment_metrics = allocation_metrics.get('Investments', {})
    pension_metrics = allocation_metrics.get('Pensions', {})
    create_metric_grid([
        lambda: complex_card(
            title="Cash Position",
            metric=f"£{cash_metrics.get('current', 0):,.2f}",
            mom_change=(f"{cash_metrics.get('mom_pct_increase', 0):+.2f}% MoM" if cash_metrics.get('mom_pct_increase') is not None else None),
            ytd_change=(f"{cash_metrics.get('ytd_pct_increase', 0):+.2f}% YTD" if cash_metrics.get('ytd_pct_increase') is not None else None),
            caption=f"{cash_metrics.get('allocation', 0):.1f}% of portfolio",
            mom_color="normal" if cash_metrics.get('mom_pct_increase', 0) >= 0 else "inverse",
            ytd_color="normal" if cash_metrics.get('ytd_pct_increase', 0) >= 0 else "inverse"
        ),
        lambda: complex_card(
            title="Investment Portfolio",
            metric=f"£{investment_metrics.get('current', 0):,.2f}",
            mom_change=(f"{investment_metrics.get('mom_pct_increase', 0):+.2f}% MoM" if investment_metrics.get('mom_pct_increase') is not None else None),
            ytd_change=(f"{investment_metrics.get('ytd_pct_increase', 0):+.2f}% YTD" if investment_metrics.get('ytd_pct_increase') is not None else None),
            caption=f"{investment_metrics.get('allocation', 0):.1f}% of portfolio",
            mom_color="normal" if investment_metrics.get('mom_pct_increase', 0) >= 0 else "inverse",
            ytd_color="normal" if investment_metrics.get('ytd_pct_increase', 0) >= 0 else "inverse"
        ),
        lambda: complex_card(
            title="Pension Value",
            metric=f"£{pension_metrics.get('current', 0):,.2f}",
            mom_change=(f"{pension_metrics.get('mom_pct_increase', 0):+.2f}% MoM" if pension_metrics.get('mom_pct_increase') is not None else None),
            ytd_change=(f"{pension_metrics.get('ytd_pct_increase', 0):+.2f}% YTD" if pension_metrics.get('ytd_pct_increase') is not None else None),
            caption=f"{pension_metrics.get('allocation', 0):.1f}% of portfolio",
            mom_color="normal" if pension_metrics.get('mom_pct_increase', 0) >= 0 else "inverse",
            ytd_color="normal" if pension_metrics.get('ytd_pct_increase', 0) >= 0 else "inverse"
        )
    ], cols=3)
    
    st.markdown("---")
    
    # --- Performance Analytics ---
    create_section_header("Performance Analytics", icon="📈")
    
    # Prepare data for performance analysis
    df_copy = df.copy()
    df_copy['Month'] = df_copy['Timestamp'].dt.to_period('M').dt.to_timestamp()
    
    # Monthly portfolio totals
    monthly_totals = df_copy.groupby('Month')['Value'].sum().reset_index()
    monthly_totals['RollingAvg'] = monthly_totals['Value'].rolling(window=3).mean()
    monthly_totals['RollingStd'] = monthly_totals['Value'].rolling(window=3).std()
    monthly_totals['MoM'] = monthly_totals['Value'].pct_change()
    
    # Calculate drawdown
    running_max = monthly_totals['Value'].cummax()
    monthly_totals['Drawdown'] = (monthly_totals['Value'] - running_max) / running_max
    
    # Performance metrics using metric grid
    max_drawdown = monthly_totals['Drawdown'].min()
    avg_monthly_return = monthly_totals['MoM'].mean()
    
    def get_best_month_card():
        if not monthly_totals['MoM'].dropna().empty:
            best_month = monthly_totals.loc[monthly_totals['MoM'].idxmax()]
            return lambda: simple_card(
                title="Best Month",
                metric=f"{best_month['MoM']:.2%}",
                caption=f"{best_month['Month'].strftime('%b %Y')}"
            )
        else:
            return lambda: simple_card(
                title="Best Month",
                metric="N/A",
                caption="Not enough data"
            )
    
    def get_worst_month_card():
        if not monthly_totals['MoM'].dropna().empty:
            worst_month = monthly_totals.loc[monthly_totals['MoM'].idxmin()]
            return lambda: simple_card(
                title="Worst Month",
                metric=f"{worst_month['MoM']:.2%}",
                caption=f"{worst_month['Month'].strftime('%b %Y')}"
            )
        else:
            return lambda: simple_card(
                title="Worst Month",
                metric="N/A",
                caption="Not enough data"
            )
    
    create_metric_grid([
        lambda: simple_card(
            title="Maximum Drawdown",
            metric=f"{max_drawdown:.2%}",
            caption="Largest peak-to-trough decline"
        ),
        get_best_month_card(),
        get_worst_month_card(),
        lambda: simple_card(
            title="Avg Monthly Return",
            metric=f"{avg_monthly_return:.2%}",
            caption="Mean monthly performance"
        )
    ], cols=4)
    
    # Performance charts using chart grid
    def create_portfolio_value_chart():
        st.markdown("**Portfolio Value & Rolling Average**")
        fig_value = create_time_series_chart(
            monthly_totals, 
            x_col='Month', 
            y_cols=['Value', 'RollingAvg'],
            title="Portfolio Value & Rolling Average"
        )
        st.plotly_chart(fig_value, use_container_width=True)
    
    def create_returns_distribution_chart():
        st.markdown("**Monthly Returns Distribution**")
        mom_clean = monthly_totals[['Month', 'MoM']].dropna()
        if not mom_clean.empty:
            fig_returns = create_histogram(
                mom_clean, 
                x_col='MoM',
                title="Monthly Returns Distribution",
                nbins=10
            )
            fig_returns.update_xaxes(tickformat='.2%')
            st.plotly_chart(fig_returns, use_container_width=True)
        else:
            st.info("Not enough data for returns distribution")
    
    create_chart_grid([create_portfolio_value_chart, create_returns_distribution_chart], cols=2)
    
    # Drawdown and volatility charts using chart grid
    def create_drawdown_chart():
        st.markdown("**Drawdown Over Time**")
        fig_drawdown = create_time_series_chart(
            monthly_totals, 
            x_col='Month', 
            y_cols=['Drawdown'],
            title="Drawdown Over Time"
        )
        fig_drawdown.update_yaxes(tickformat='.2%')
        st.plotly_chart(fig_drawdown, use_container_width=True)
    
    def create_volatility_chart():
        st.markdown("**Rolling Volatility (3-Month)**")
        fig_vol = create_time_series_chart(
            monthly_totals, 
            x_col='Month', 
            y_cols=['RollingStd'],
            title="Rolling Volatility (3-Month)"
        )
        st.plotly_chart(fig_vol, use_container_width=True)
    
    create_chart_grid([create_drawdown_chart, create_volatility_chart], cols=2)
    
    st.markdown("---")
    
    # --- Asset Allocation Analysis ---
    create_section_header("Asset Allocation Analysis", icon="🏗️")
    
    # Current allocation pie chart
    def create_allocation_pie_chart():
        st.markdown("**Current Asset Allocation**")
        allocation_data = []
        for asset_type, metrics in allocation_metrics.items():
            if asset_type != 'Total':
                allocation_data.append({
                    'Asset Type': asset_type,
                    'Value': metrics.get('current', 0),
                    'Allocation': metrics.get('allocation', 0)
                })
        if allocation_data:
            allocation_df = pd.DataFrame(allocation_data)
            fig_allocation = create_pie_chart(
                allocation_df,
                names_col='Asset Type',
                values_col='Value',
                title="Current Asset Allocation"
            )
            st.plotly_chart(fig_allocation, use_container_width=True)
        else:
            st.info("No allocation data available")
    
    def create_allocation_changes_chart():
        st.markdown("**Allocation Changes (MoM)**")
        allocation_changes = []
        for asset_type, metrics in allocation_metrics.items():
            if asset_type != 'Total':
                allocation_changes.append({
                    'Asset Type': asset_type,
                    'Allocation Change': metrics.get('allocation_change', 0)
                })
        if allocation_changes:
            changes_df = pd.DataFrame(allocation_changes)
            fig_changes = create_bar_chart(
                changes_df,
                x_col='Asset Type',
                y_col='Allocation Change',
                title="Allocation Changes (MoM)"
            )
            fig_changes.update_yaxes(tickformat='.2f')
            fig_changes.update_traces(marker_color=['green' if x >= 0 else 'red' for x in changes_df['Allocation Change']])
            st.plotly_chart(fig_changes, use_container_width=True)
        else:
            st.info("No allocation change data available")
    
    create_chart_grid([create_allocation_pie_chart, create_allocation_changes_chart], cols=2)
    
    # Platform breakdown
    st.markdown("**Platform Distribution**")
    latest_data = df_copy[df_copy['Month'] == latest_month]
    platform_breakdown = latest_data.groupby('Platform')['Value'].sum().reset_index()
    
    if not platform_breakdown.empty:
        fig_platform = create_bar_chart(
            platform_breakdown,
            x_col='Platform',
            y_col='Value',
            title="Platform Distribution"
        )
        st.plotly_chart(fig_platform, use_container_width=True)
    else:
        st.info("No platform data available")
    
    st.markdown("---")
    
    # --- Summary Statistics ---
    create_section_header("Summary Statistics", icon="📊")
    
    total_platforms = df['Platform'].nunique()
    total_assets = df['Asset'].nunique() if 'Asset' in df.columns else 0
    months_tracked = df['Timestamp'].dt.to_period('M').nunique()
    latest_records = len(df[df['Timestamp'].dt.to_period('M') == latest_month])
    
    create_metric_grid([
        lambda: simple_card(
            title="Total Platforms",
            metric=str(total_platforms),
            caption="Unique financial platforms"
        ),
        lambda: simple_card(
            title="Total Assets",
            metric=str(total_assets),
            caption="Unique asset types"
        ),
        lambda: simple_card(
            title="Months Tracked",
            metric=str(months_tracked),
            caption="Historical data period"
        ),
        lambda: simple_card(
            title="Latest Records",
            metric=str(latest_records),
            caption=f"Records in {latest_month.strftime('%B %Y')}"
        )
    ], cols=4)

else:
    st.error("❌ Data could not be loaded. Please check your data file.")
    st.info("💡 Make sure you have uploaded data through the sidebar on the Home page.") 