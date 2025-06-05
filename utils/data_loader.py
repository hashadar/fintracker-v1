"""Data loading and preprocessing functions for the financial dashboard app."""

import pandas as pd
import streamlit as st
from .constants import ASSET_TYPES

@st.cache_data
def load_data():
    """Load and preprocess the financial data from Excel. Adds asset type and ensures one entry per platform-asset per month."""
    try:
        df = pd.read_excel("202506_equity_hd.xlsx", sheet_name=0)
        
        # Convert Timestamp to datetime
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        
        # Add asset type category based on platform
        df['Asset_Type'] = df['Platform'].apply(lambda x: next(
            (k for k, v in ASSET_TYPES.items() if x in v), 'Other'))
        
        # Ensure one entry per platform-asset per month (using month from Timestamp)
        month_period = df['Timestamp'].dt.to_period('M')
        monthly_platform_asset_counts = df.groupby([month_period, 'Platform', 'Asset']).size()
        if (monthly_platform_asset_counts > 1).any():
            st.warning("Multiple entries found for some platform-asset combinations in a month. Using the latest entry.")
            df = df.assign(Month=month_period)
            df = df.sort_values('Timestamp').groupby(['Month', 'Platform', 'Asset']).last().reset_index()
            df = df.drop(columns=['Month'])
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.write("Available columns:", df.columns.tolist())
        return None

def filter_data_by_date_range(df, start_month, end_month):
    """Filter data by selected month range (using month derived from Timestamp)."""
    month_period = df['Timestamp'].dt.to_period('M').dt.to_timestamp()
    start_date = pd.to_datetime(start_month, format="%B %Y")
    end_date = pd.to_datetime(end_month, format="%B %Y")
    return df[(month_period >= start_date) & (month_period <= end_date)]

def get_month_range(df):
    """Get the range of months available in the data (using month derived from Timestamp)."""
    months = df['Timestamp'].dt.to_period('M').dt.to_timestamp()
    months = pd.Series(months.unique()).sort_values()
    min_month = months.min()
    max_month = months.max()
    month_options = [month.strftime("%B %Y") for month in months]
    return month_options, min_month, max_month 