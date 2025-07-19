"""Main Streamlit application for financial dashboard."""

import streamlit as st

from utils import (
    INITIAL_SIDEBAR_STATE,
    LAYOUT,
    PAGE_ICON,
    PAGE_TITLE,
    load_car_assets,
    load_car_expenses,
    load_car_payments,
    load_data,
    load_pension_cashflows,
)
from utils.design.components import (
    create_page_header,
    create_section_header,
)
from utils.design.tokens import CUSTOM_STYLE

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
    title=PAGE_TITLE, description="Welcome to your personal financial dashboard."
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

# --- Data Status Section ---
st.markdown("---")
create_section_header("Data Load Status", icon="📊")

data_sources = {
    "Balance Sheet": load_data,
    "Pension Cashflows": load_pension_cashflows,
    "Car Assets": load_car_assets,
    "Car Payments": load_car_payments,
    "Car Expenses": load_car_expenses,
}

status_cols = st.columns(len(data_sources))

for (source_name, loader_func), col in zip(data_sources.items(), status_cols):
    with col:
        try:
            df = loader_func()
            if df is not None and not df.empty:
                st.success(f"**{source_name}**\n\n_{len(df)} records_")
            else:
                st.error(f"**{source_name}**\n\n_No data_")
        except Exception as e:
            st.error(f"**{source_name}**\n\n_Failed_")


# --- Sidebar for Data Management ---
st.sidebar.title("FinTracker")
st.sidebar.markdown("Navigate your dashboard using the links above.")
st.sidebar.markdown("---")
st.sidebar.header("Data Connection")

# Check overall data status for the main 'load_data' function
if "data_status" not in st.session_state:
    raw_data = load_data()
    st.session_state["data_status"] = (
        "success" if raw_data is not None and not raw_data.empty else "fail"
    )

if st.session_state.get("data_status") == "success":
    st.sidebar.success("✅ Main data loaded")
else:
    st.sidebar.error("❌ Main data failed")

if st.sidebar.button("🔄 Reload All Data"):
    # Clear all cached data before reloading
    st.cache_data.clear()
    st.session_state["data_status"] = None
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **Data Source:** Google Sheets\n\nTo update your data, edit your Google Sheets document directly."
)
