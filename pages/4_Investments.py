import streamlit as st
from utils import (
    load_data,
    filter_by_asset_type,
    calculate_asset_type_metrics,
    get_asset_type_time_periods,
    ASSET_TYPES,
    DISPLAY_DATE_FORMAT,
    CURRENCY_FORMAT
)
from utils.design.tokens import BRAND_PRIMARY
from utils.design.components import (
    create_page_header,
    create_section_header,
    create_asset_summary_cards,
    create_time_period_breadcrumb,
    create_portfolio_analytics_charts,
    create_investment_asset_analysis
)

# Page configuration
st.set_page_config(page_title="Investments - FinTracker", layout="wide")

# Load data
df = load_data()

if df is not None and not df.empty:
    # Filter for investment assets using new data processing component
    investment_df = filter_by_asset_type(df, ASSET_TYPES['INVESTMENTS'])
    
    if not investment_df.empty:
        create_page_header(
            title="📈 Investment Portfolio Dashboard",
            description="Comprehensive analysis of your investment performance and asset allocation"
        )
        
        # Calculate investment-specific metrics
        investment_metrics = calculate_asset_type_metrics(df, ASSET_TYPES['INVESTMENTS'])
        
        # Get time periods for display
        latest_month, prev_month, ytd_start_month = get_asset_type_time_periods(df, ASSET_TYPES['INVESTMENTS'])
        
        # Display time period info
        create_time_period_breadcrumb(
            latest_month=latest_month,
            prev_month=prev_month,
            ytd_start_month=ytd_start_month,
            display_date_format=DISPLAY_DATE_FORMAT
        )
        
        # --- Investment Summary Cards ---
        create_section_header("Investment Portfolio Summary", icon="🎯")
        
        # Use the new reusable component
        create_asset_summary_cards(
            asset_metrics=investment_metrics,
            asset_type_name="Investment Portfolio",
            emphasis_color=BRAND_PRIMARY,
            currency_format=CURRENCY_FORMAT
        )
        
        st.markdown("---")
        
        # --- Portfolio Analytics ---
        create_portfolio_analytics_charts(df, asset_type=ASSET_TYPES['INVESTMENTS'], section_title="Investment Analytics", section_icon="📈")
        
        st.markdown("---")
        
        # --- Asset-Level Analysis ---
        create_investment_asset_analysis(df, asset_type=ASSET_TYPES['INVESTMENTS'])
        
        st.markdown("---")
    
    else:
        st.error("❌ No investment data found in your portfolio.")
        st.info(f"💡 Make sure your data includes assets classified as '{ASSET_TYPES['INVESTMENTS']}' type.")

else:
    st.error("❌ Data could not be loaded. Please check your data file.")
    st.info("💡 Make sure you have uploaded data through the sidebar on the Home page.") 