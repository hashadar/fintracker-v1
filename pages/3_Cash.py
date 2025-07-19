import streamlit as st

from utils import (
    ASSET_TYPES,
    CURRENCY_FORMAT,
    DISPLAY_DATE_FORMAT,
    calculate_asset_type_metrics,
    filter_by_asset_type,
    get_asset_type_time_periods,
    load_data,
)
from utils.design.components import (
    create_asset_summary_cards,
    create_page_header,
    create_portfolio_analytics_charts,
    create_section_header,
    create_time_period_breadcrumb,
)
from utils.design.tokens import BRAND_SUCCESS

# Page configuration
st.set_page_config(page_title="Cash - FinTracker", layout="wide")

# Load data
df = load_data()

if df is not None and not df.empty:
    # Filter for cash assets using new data processing component
    cash_df = filter_by_asset_type(df, ASSET_TYPES["CASH"])

    if not cash_df.empty:
        create_page_header(
            title="💰 Cash Assets Dashboard",
            description="Comprehensive analysis of your cash positions and liquidity",
        )

        # Calculate cash-specific metrics
        cash_metrics = calculate_asset_type_metrics(df, ASSET_TYPES["CASH"])

        # Get time periods for display
        latest_month, prev_month, ytd_start_month = get_asset_type_time_periods(
            df, ASSET_TYPES["CASH"]
        )

        # Display time period info
        create_time_period_breadcrumb(
            latest_month=latest_month,
            prev_month=prev_month,
            ytd_start_month=ytd_start_month,
            display_date_format=DISPLAY_DATE_FORMAT,
        )

        # --- Cash Summary Cards ---
        create_section_header("Cash Position Summary", icon="💳")

        # Use the new reusable component
        create_asset_summary_cards(
            asset_metrics=cash_metrics,
            asset_type_name="Cash Position",
            emphasis_color=BRAND_SUCCESS,
            currency_format=CURRENCY_FORMAT,
        )

        st.markdown("---")

        # --- Portfolio Analytics ---
        create_portfolio_analytics_charts(
            df,
            asset_type=ASSET_TYPES["CASH"],
            section_title="Cash Analytics",
            section_icon="📈",
        )

    else:
        st.error("❌ No cash data found in your portfolio.")
        st.info(
            f"💡 Make sure your data includes assets classified as '{ASSET_TYPES['CASH']}' type."
        )

else:
    st.error("❌ Data could not be loaded. Please check your data file.")
    st.info("💡 Make sure you have uploaded data through the sidebar on the Home page.")
