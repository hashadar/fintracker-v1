"""Main Streamlit application for financial dashboard."""

import streamlit as st
import pandas as pd
from utils import (
    CUSTOM_STYLE,
    PAGE_TITLE,
    load_data,
)
from utils.data_loader import save_data

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
st.markdown(f"""
    <h1 style='text-align: center; margin-bottom: 1rem;'>{PAGE_TITLE}</h1>
    """, unsafe_allow_html=True)

st.markdown(
    "<p style='text-align: center; margin-bottom: 2rem;'>Welcome to your personal financial dashboard.</p>",
    unsafe_allow_html=True
)

st.markdown("---")

st.markdown("## Welcome to FinTracker!")
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

# --- Sidebar for Data Management ---
st.sidebar.title("FinTracker")
st.sidebar.markdown("Navigate your dashboard using the links above.")
st.sidebar.markdown("---")
st.sidebar.header("Data Management")

uploaded_file = st.sidebar.file_uploader(
    "Upload new data (Excel)", type=["xlsx"], key="main_app_uploader"
)

if uploaded_file:
    try:
        new_data_df = pd.read_excel(uploaded_file)
        required_cols = ["Timestamp", "Asset_Type", "Asset_Name", "Value"]

        if not all(col in new_data_df.columns for col in required_cols):
            st.sidebar.error(
                f"Uploaded file is missing required columns. It must contain: {', '.join(required_cols)}"
            )
        else:
            df = load_data()
            if df is not None:
                # Combine and save data
                combined_df = pd.concat([df, new_data_df], ignore_index=True)
                combined_df["Timestamp"] = pd.to_datetime(combined_df["Timestamp"])
                combined_df = combined_df.sort_values(by="Timestamp").reset_index(drop=True)
                save_data(combined_df)

                # Clear cache and rerun to reflect updates
                load_data.clear()
                st.sidebar.success("Data uploaded and saved successfully!")
                st.toast("Dashboard is refreshing with new data...")
                st.rerun()
            else:
                st.sidebar.error("Could not load existing data to append the new data.")

    except Exception as e:
        st.sidebar.error(f"Error processing uploaded file: {e}")