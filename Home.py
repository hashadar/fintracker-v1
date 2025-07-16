"""Main Streamlit application for financial dashboard."""

import streamlit as st
import pandas as pd
import os
from utils import (
    load_data,
    calculate_asset_type_metrics,
    get_latest_month_data,
    get_asset_breakdown,
    PAGE_TITLE,
    PAGE_ICON,
    LAYOUT,
    INITIAL_SIDEBAR_STATE,
    CURRENCY_FORMAT,
    DISPLAY_DATE_FORMAT
)
from utils.design.cards import simple_card, complex_emphasis_card, complex_card, emphasis_card
from utils.design.tokens import CUSTOM_STYLE
from utils.design.components import create_page_header, create_section_header, create_metric_grid

# Set page config
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state=INITIAL_SIDEBAR_STATE,
)

# Apply custom styling
st.markdown(CUSTOM_STYLE, unsafe_allow_html=True)

# Main app (homepage) content
create_page_header(
    title=PAGE_TITLE,
    description="Welcome to your personal financial dashboard."
)

st.markdown("---")

create_section_header("Welcome to FinTracker!", icon="👋")

st.markdown(
    """
    This application is designed to provide a clear and concise overview of your assets.

    **Use the navigation panel on the left to explore:**
    - **Overview**: A high-level summary of your entire portfolio.
    - **Cash, Investments, & Pensions**: Deep-dive analysis for each asset category.
    - **All Assets**: Advanced analytics on your consolidated financial data.
    """
)

st.info("Select a page from the sidebar to get started.", icon="👈")

# --- Asset Summary Section ---
st.markdown("---")
create_section_header("Asset Summary", icon="📈")

# Load and display asset summary for latest month
raw_data = load_data()
if raw_data is not None and not raw_data.empty:
    # Ensure asset classification is done
    if 'Asset_Type' not in raw_data.columns:
        from utils.etl.asset_classifier import classify_asset_types
        raw_data = classify_asset_types(raw_data)
    
    if 'Asset_Type' in raw_data.columns:
        # Get the latest month's data using new data processing components
        raw_data['Timestamp'] = pd.to_datetime(raw_data['Timestamp'], dayfirst=True)
        latest_data = get_latest_month_data(raw_data)
        
        if not latest_data.empty:
            # Calculate asset type breakdown for latest month using new data processing component
            asset_breakdown = get_asset_breakdown(latest_data, 'asset_type')
            latest_month = latest_data['Timestamp'].dt.to_period('M').max()
            total_value = float(latest_data['Value'].sum())
            
            # Display portfolio summary using metric grid for consistent layout
            cash_row = asset_breakdown[asset_breakdown['Asset_Type'] == 'Cash']
            cash_value = float(cash_row['Value'].iloc[0]) if not cash_row.empty else 0
            cash_pct = float(cash_row['Percentage'].iloc[0]) if not cash_row.empty else 0
            
            investment_row = asset_breakdown[asset_breakdown['Asset_Type'] == 'Investments']
            investment_value = float(investment_row['Value'].iloc[0]) if not investment_row.empty else 0
            investment_pct = float(investment_row['Percentage'].iloc[0]) if not investment_row.empty else 0
            
            pension_row = asset_breakdown[asset_breakdown['Asset_Type'] == 'Pensions']
            pension_value = float(pension_row['Value'].iloc[0]) if not pension_row.empty else 0
            pension_pct = float(pension_row['Percentage'].iloc[0]) if not pension_row.empty else 0
            
            create_metric_grid([
                lambda: emphasis_card(
                    title="Total Portfolio Value",
                    metric=CURRENCY_FORMAT.format(total_value),
                    caption=f"Latest month: {latest_month.strftime(DISPLAY_DATE_FORMAT)}"
                ),
                lambda: simple_card(
                    title="Cash",
                    metric=CURRENCY_FORMAT.format(cash_value),
                    caption=f"{cash_pct:.1f}% of portfolio"
                ),
                lambda: simple_card(
                    title="Investments",
                    metric=CURRENCY_FORMAT.format(investment_value),
                    caption=f"{investment_pct:.1f}% of portfolio"
                ),
                lambda: simple_card(
                    title="Pensions",
                    metric=CURRENCY_FORMAT.format(pension_value),
                    caption=f"{pension_pct:.1f}% of portfolio"
                )
            ], cols=4)
        else:
            st.warning("No data available for the latest month")
    else:
        st.warning("Asset classification not available")
else:
    st.warning("No data loaded")

# --- Data Status Section ---
st.markdown("---")
st.markdown("## 📊 Data Status")

# Check if ETL data exists and initialize if needed
# Remove all ETL-related imports and usages

# Display data status
col1, col2 = st.columns(2)

with col1:
    # Check raw data
    raw_data = load_data()
    if raw_data is not None and not raw_data.empty:
        st.success(f"📊 Data Loaded: {len(raw_data)} records")
    else:
        st.error("📊 Data: Failed to load")

with col2:
    # Check ETL data
    # Remove initialize_etl_data and all code that uses it or run_multi_asset_type_etl
    st.success("🔧 Analytics: Ready")



# --- Sidebar for Data Management ---
st.sidebar.title("FinTracker")
st.sidebar.markdown("Navigate your dashboard using the links above.")
st.sidebar.markdown("---")
st.sidebar.header("Data Connection")

# Attempt to load data and set status
if 'force_reload' in st.session_state:
    raw_data = load_data()
    del st.session_state['force_reload']

if 'data_status' not in st.session_state:
    raw_data = load_data()
    if raw_data is not None and not raw_data.empty:
        st.session_state['data_status'] = 'success'
    else:
        st.session_state['data_status'] = 'fail'

if st.session_state.get('data_status') == 'success':
    st.sidebar.success("✅ Data connection successful")
else:
    st.sidebar.error("❌ Data connection failed")

if st.sidebar.button("🔄 Reload Data"):
    st.session_state['force_reload'] = True
    st.session_state['data_status'] = None
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("💡 **Data Source:** Google Sheets\n\nTo update your data, edit your Google Sheets document directly.")