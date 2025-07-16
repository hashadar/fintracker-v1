"""Data loading and preprocessing functions for the financial dashboard app."""

import pandas as pd
import streamlit as st
import numpy as np
from datetime import datetime, timedelta
import os
from .asset_classifier import classify_asset_types
from ..config import SHEET_NAME, DATE_COLUMN, AMOUNT_COLUMN, CATEGORY_COLUMN, DESCRIPTION_COLUMN

# Google Sheets imports
try:
    import gspread
    from google.oauth2.service_account import Credentials
    from google.auth.exceptions import GoogleAuthError
    GOOGLE_SHEETS_AVAILABLE = True
except ImportError:
    GOOGLE_SHEETS_AVAILABLE = False

def _load_from_google_sheets():
    """Load data from Google Sheets with optimized column selection."""
    if not GOOGLE_SHEETS_AVAILABLE:
        st.error("Google Sheets dependencies not installed. Please install: pip install gspread google-auth google-auth-oauthlib google-auth-httplib2")
        return None
    
    try:
        # Get configuration from Streamlit secrets
        google_config = st.secrets.get("google_sheets", {})
        spreadsheet_id = google_config.get("spreadsheet_id")
        
        if not spreadsheet_id:
            st.error("Google Sheets configuration error. Please check your setup.")
            return None
        
        # Set up authentication
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        # Try to get credentials from secrets
        service_account_info = google_config.get("service_account_info")
        if service_account_info:
            creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
        else:
            # Try credentials file path
            credentials_path = google_config.get("credentials_path")
            if credentials_path and os.path.exists(credentials_path):
                creds = Credentials.from_service_account_file(credentials_path, scopes=scopes)
            else:
                st.error("Google Sheets service account credentials not configured. Please set in .streamlit/secrets.toml")
                return None
        
        # Connect to Google Sheets
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(spreadsheet_id)
        
        # Get the first worksheet (or specify by name)
        worksheet_name = google_config.get("worksheet_name", SHEET_NAME)
        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.get_worksheet(0)  # Get first worksheet
        
        # Get headers first to identify column positions
        headers = worksheet.row_values(1)
        
        # Define required columns and their positions
        required_columns = ['Platform', 'Asset', 'Value', 'Timestamp', 'Token Amount']
        column_positions = {}
        
        for col in required_columns:
            try:
                col_idx = headers.index(col) + 1  # gspread uses 1-based indexing
                column_positions[col] = col_idx
            except ValueError:
                if col in ['Platform', 'Asset', 'Value', 'Timestamp']:  # Essential columns
                    st.error(f"Required column '{col}' not found in data")
                    return None
        
        # Get all data rows (skip header)
        all_values = worksheet.get_all_values()
        
        if len(all_values) <= 1:  # Only header or empty
            st.warning("No data found")
            return None
        
        # Extract only the columns we need
        data_rows = []
        for i, row in enumerate(all_values[1:], 2):  # Skip header row, start counting from 2
            if len(row) >= max(column_positions.values()):  # Ensure row has enough columns
                data_row = {}
                for col, pos in column_positions.items():
                    data_row[col] = row[pos - 1] if pos <= len(row) else None
                data_rows.append(data_row)
        
        if not data_rows:
            st.warning("No valid data rows found")
            return None
        
        # Convert to DataFrame
        df = pd.DataFrame(data_rows)
        
        # Clean up data types with currency handling
        if 'Value' in df.columns:
            # Handle currency symbols and commas in Value column
            df['Value'] = df['Value'].astype(str).str.replace('£', '').str.replace(',', '').str.strip()
            df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
        
        if 'Token Amount' in df.columns:
            df['Token Amount'] = pd.to_numeric(df['Token Amount'], errors='coerce')
        
        # Remove rows with missing essential data
        essential_cols = ['Platform', 'Asset', 'Value', 'Timestamp']
        df_cleaned = df.dropna(subset=essential_cols)
        
        if df_cleaned.empty:
            st.warning("No valid data after cleaning")
            return None
        
        return df_cleaned
        
    except Exception as e:
        st.error(f"Error loading data from Google Sheets: {str(e)}")
        return None

@st.cache_data
def load_data():
    """Load and preprocess the financial data from Google Sheets. Adds asset type and ensures one entry per platform-asset per month."""
    try:
        # Load from Google Sheets
        df = _load_from_google_sheets()
        
        if df is None:
            st.error("Failed to load data")
            return None
        
        # Convert Timestamp to datetime
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], dayfirst=True)
        
        # Ensure Value column is numeric
        if 'Value' in df.columns:
            df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
            # Remove rows where Value couldn't be converted to numeric
            df = df.dropna(subset=['Value'])
        
        # Check if Asset_Type column exists, if not classify assets
        if 'Asset_Type' not in df.columns:
            df = classify_asset_types(df)
        
        # Ensure one entry per asset per month (using month from Timestamp)
        month_period = df['Timestamp'].dt.to_period('M')
        monthly_asset_counts = df.groupby([month_period, 'Asset']).size()
        if (monthly_asset_counts > 1).any():
            st.info("Using latest entry for duplicate assets per month")
            df = df.assign(Month=month_period)
            df = df.sort_values('Timestamp').groupby(['Month', 'Asset']).last().reset_index()
            df = df.drop(columns=['Month'])
        
        return df
    except Exception as e:
        st.error(f"Error processing data: {str(e)}")
        return None

def filter_data_by_date_range(df, start_date=None, end_date=None):
    """Filter data by date range."""
    if df is None:
        return None
    
    filtered_df = df.copy()
    
    if start_date:
        filtered_df = filtered_df[filtered_df['Timestamp'] >= start_date]
    
    if end_date:
        filtered_df = filtered_df[filtered_df['Timestamp'] <= end_date]
    
    return filtered_df

def get_month_range(df):
    """Get the month range from the data."""
    if df is None or df.empty:
        return None, None
    
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    min_date = df['Timestamp'].min()
    max_date = df['Timestamp'].max()
    
    return min_date, max_date

def get_available_data_files():
    """Get list of available data files in raw and staging directories."""
    files = {
        'raw': [],
        'staging': []
    }
    
    # Check raw directory
    raw_dir = "data/raw"
    if os.path.exists(raw_dir):
        files['raw'] = [f for f in os.listdir(raw_dir) if f.endswith('.xlsx')]
    
    # Check staging directory
    staging_dir = "data/staging"
    if os.path.exists(staging_dir):
        files['staging'] = [f for f in os.listdir(staging_dir) if f.endswith('.xlsx')]
    
    return files 