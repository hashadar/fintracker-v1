import streamlit as st

from utils import (
    ASSET_TYPES,
    CURRENCY_FORMAT,
    DISPLAY_DATE_FORMAT,
    calculate_allocation_metrics,
    load_data,
)
from utils.design.cards import complex_card, complex_emphasis_card
from utils.design.components import (
    create_metric_grid,
    create_page_header,
    create_portfolio_analytics_charts,
    create_section_header,
    create_summary_statistics,
    create_time_period_breadcrumb,
)
from utils.design.tokens import BRAND_PRIMARY

# Page configuration
st.set_page_config(page_title="All Assets - FinTracker", layout="wide")

# Load data
df = load_data()

if df is not None and not df.empty:
    create_page_header(
        title="📊 All Assets Analytics",
        description="Comprehensive analysis across all asset types (Cash, Investments, Pensions)",
    )

    # Calculate allocation metrics
    allocation_metrics, latest_month, prev_month, ytd_start_month = (
        calculate_allocation_metrics(df)
    )

    # Display time period info
    create_time_period_breadcrumb(
        latest_month=latest_month,
        prev_month=prev_month,
        ytd_start_month=ytd_start_month,
        display_date_format=DISPLAY_DATE_FORMAT,
    )

    # --- Portfolio Summary Cards ---
    create_section_header("Portfolio Summary", icon="🎯")

    # Main portfolio total card
    total_metrics = allocation_metrics.get("Total", {})
    complex_emphasis_card(
        title="Total Portfolio Value",
        metric=CURRENCY_FORMAT.format(total_metrics.get("current", 0)),
        mom_change=(
            f"{CURRENCY_FORMAT.format(total_metrics.get('mom_increase', 0))} MoM"
            if total_metrics.get("mom_increase") is not None
            else None
        ),
        ytd_change=(
            f"{CURRENCY_FORMAT.format(total_metrics.get('ytd_increase', 0))} YTD"
            if total_metrics.get("ytd_increase") is not None
            else None
        ),
        caption=f"Complete financial position as of {latest_month.strftime(DISPLAY_DATE_FORMAT)}",
        mom_color="normal" if total_metrics.get("mom_increase", 0) >= 0 else "inverse",
        ytd_color="normal" if total_metrics.get("ytd_increase", 0) >= 0 else "inverse",
        emphasis_color=BRAND_PRIMARY,
    )

    # Asset type breakdown cards using metric grid
    cash_metrics = allocation_metrics.get(ASSET_TYPES["CASH"], {})
    investment_metrics = allocation_metrics.get(ASSET_TYPES["INVESTMENTS"], {})
    pension_metrics = allocation_metrics.get(ASSET_TYPES["PENSIONS"], {})
    create_metric_grid(
        [
            lambda: complex_card(
                title="Cash Position",
                metric=CURRENCY_FORMAT.format(cash_metrics.get("current", 0)),
                mom_change=(
                    f"{cash_metrics.get('mom_pct_increase', 0):+.2f}% MoM"
                    if cash_metrics.get("mom_pct_increase") is not None
                    else None
                ),
                ytd_change=(
                    f"{cash_metrics.get('ytd_pct_increase', 0):+.2f}% YTD"
                    if cash_metrics.get("ytd_pct_increase") is not None
                    else None
                ),
                caption=f"{cash_metrics.get('allocation', 0):.1f}% of portfolio",
                mom_color=(
                    "normal"
                    if cash_metrics.get("mom_pct_increase", 0) >= 0
                    else "inverse"
                ),
                ytd_color=(
                    "normal"
                    if cash_metrics.get("ytd_pct_increase", 0) >= 0
                    else "inverse"
                ),
            ),
            lambda: complex_card(
                title="Investment Portfolio",
                metric=CURRENCY_FORMAT.format(investment_metrics.get("current", 0)),
                mom_change=(
                    f"{investment_metrics.get('mom_pct_increase', 0):+.2f}% MoM"
                    if investment_metrics.get("mom_pct_increase") is not None
                    else None
                ),
                ytd_change=(
                    f"{investment_metrics.get('ytd_pct_increase', 0):+.2f}% YTD"
                    if investment_metrics.get("ytd_pct_increase") is not None
                    else None
                ),
                caption=f"{investment_metrics.get('allocation', 0):.1f}% of portfolio",
                mom_color=(
                    "normal"
                    if investment_metrics.get("mom_pct_increase", 0) >= 0
                    else "inverse"
                ),
                ytd_color=(
                    "normal"
                    if investment_metrics.get("ytd_pct_increase", 0) >= 0
                    else "inverse"
                ),
            ),
            lambda: complex_card(
                title="Pension Value",
                metric=CURRENCY_FORMAT.format(pension_metrics.get("current", 0)),
                mom_change=(
                    f"{pension_metrics.get('mom_pct_increase', 0):+.2f}% MoM"
                    if pension_metrics.get("mom_pct_increase") is not None
                    else None
                ),
                ytd_change=(
                    f"{pension_metrics.get('ytd_pct_increase', 0):+.2f}% YTD"
                    if pension_metrics.get("ytd_pct_increase") is not None
                    else None
                ),
                caption=f"{pension_metrics.get('allocation', 0):.1f}% of portfolio",
                mom_color=(
                    "normal"
                    if pension_metrics.get("mom_pct_increase", 0) >= 0
                    else "inverse"
                ),
                ytd_color=(
                    "normal"
                    if pension_metrics.get("ytd_pct_increase", 0) >= 0
                    else "inverse"
                ),
            ),
        ],
        cols=3,
    )

    st.markdown("---")

    # --- Portfolio Analytics ---
    create_portfolio_analytics_charts(
        df, asset_type=None, section_title="Portfolio Analytics", section_icon="📈"
    )

    st.markdown("---")

    # --- Summary Statistics ---
    create_summary_statistics(df, latest_month, DISPLAY_DATE_FORMAT)

else:
    st.error("❌ Data could not be loaded. Please check your data file.")
    st.info("💡 Make sure you have uploaded data through the sidebar on the Home page.")
