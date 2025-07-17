import streamlit as st
from utils import (
    load_data,
    load_pension_cashflows,
    calculate_asset_type_metrics,
    filter_by_asset_type,
    get_asset_type_time_periods,
    ASSET_TYPES,
    CURRENCY_FORMAT,
    DISPLAY_DATE_FORMAT
)
from utils.design.tokens import BRAND_INFO
from utils.design.components import (
    create_page_header,
    create_section_header,
    create_asset_summary_cards,
    create_time_period_breadcrumb,
    create_pension_asset_analysis
)

# Page configuration
st.set_page_config(page_title="Pensions - FinTracker", layout="wide")

# Load data
df = load_data()
cashflows_df = load_pension_cashflows()

if df is not None and not df.empty:
    # Filter for pension assets using new data processing component
    pension_df = filter_by_asset_type(df, ASSET_TYPES['PENSIONS'])
    
    if not pension_df.empty:
        create_page_header(
            title="🏦 Pension Assets Dashboard",
            description="Comprehensive analysis of your pension positions and long-term retirement planning"
        )
        
        # Calculate pension-specific metrics
        pension_metrics = calculate_asset_type_metrics(df, ASSET_TYPES['PENSIONS'])
        
        # Get time periods for display
        latest_month, prev_month, ytd_start_month = get_asset_type_time_periods(df, ASSET_TYPES['PENSIONS'])
        
        # Display time period info
        create_time_period_breadcrumb(
            latest_month=latest_month,
            prev_month=prev_month,
            ytd_start_month=ytd_start_month,
            display_date_format=DISPLAY_DATE_FORMAT
        )
        
        # --- Pension Summary Cards ---
        create_section_header("Pension Portfolio Summary", icon="🎯")
        
        # Use the new reusable component
        create_asset_summary_cards(
            asset_metrics=pension_metrics,
            asset_type_name="Pension Portfolio",
            emphasis_color=BRAND_INFO,
            currency_format=CURRENCY_FORMAT
        )
        
        st.markdown("---")
        
        # --- Portfolio Analytics (Reusable) ---
        from utils.design.components import create_portfolio_analytics_charts
        create_portfolio_analytics_charts(pension_df, asset_type=ASSET_TYPES['PENSIONS'])
        
        # --- Asset-Level Analysis (with Cashflow Data) ---
        create_pension_asset_analysis(pension_df, cashflows_df, asset_type=ASSET_TYPES['PENSIONS'])

        st.markdown("---")

        # --- Pension Growth Forecast ---
        from utils.design.components import create_pension_forecast_section
        create_pension_forecast_section(pension_df, cashflows_df)
    
    else:
        st.error("❌ No pension data found in your portfolio.")
        st.info(f"💡 Make sure your data includes assets classified as '{ASSET_TYPES['PENSIONS']}' type.")

else:
    st.error("❌ Data could not be loaded. Please check your data file.")
    st.info("💡 Make sure you have uploaded data through the sidebar on the Home page.") 