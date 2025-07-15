"""Main Streamlit application for financial dashboard."""

import streamlit as st
import pandas as pd
import os
from utils import (
    load_data,
    calculate_asset_type_metrics
)
from utils.design.cards import simple_card, complex_emphasis_card, complex_card, emphasis_card
from utils.design.tokens import CUSTOM_STYLE
from utils.design.components import create_page_header, create_section_header, create_metric_grid

PAGE_TITLE = "FinTracker - Personal Financial Dashboard"

# Set page config
st.set_page_config(
    page_title="FinTracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
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
        # Get the latest month's data
        raw_data['Timestamp'] = pd.to_datetime(raw_data['Timestamp'], dayfirst=True)
        latest_month = raw_data['Timestamp'].dt.to_period('M').max()
        latest_data = raw_data[raw_data['Timestamp'].dt.to_period('M') == latest_month]
        
        if not latest_data.empty:
            # Calculate asset type breakdown for latest month
            asset_type_values = latest_data.groupby('Asset_Type')['Value'].sum()
            total_value = float(latest_data['Value'].sum())
            
            # Display portfolio summary using metric grid for consistent layout
            cash_value = float(asset_type_values.get('Cash', 0))
            cash_pct = (cash_value / total_value) * 100 if total_value > 0 else 0
            investment_value = float(asset_type_values.get('Investments', 0))
            investment_pct = (investment_value / total_value) * 100 if total_value > 0 else 0
            pension_value = float(asset_type_values.get('Pensions', 0))
            pension_pct = (pension_value / total_value) * 100 if total_value > 0 else 0
            
            create_metric_grid([
                lambda: emphasis_card(
                    title="Total Portfolio Value",
                    metric=f"£{total_value:,.0f}",
                    caption=f"Latest month: {latest_month.strftime('%B %Y')}"
                ),
                lambda: simple_card(
                    title="Cash",
                    metric=f"£{cash_value:,.0f}",
                    caption=f"{cash_pct:.1f}% of portfolio"
                ),
                lambda: simple_card(
                    title="Investments",
                    metric=f"£{investment_value:,.0f}",
                    caption=f"{investment_pct:.1f}% of portfolio"
                ),
                lambda: simple_card(
                    title="Pensions",
                    metric=f"£{pension_value:,.0f}",
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