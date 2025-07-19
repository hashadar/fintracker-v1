"""Data loading and preprocessing functions for the financial dashboard app."""

import os

import pandas as pd
import streamlit as st

from ..config import (
    BALANCE_SHEET_CONFIG,
    BALANCE_SHEET_VALID_VALUES,
    CAR_ASSETS_CONFIG,
    CAR_ASSETS_VALID_VALUES,
    CAR_EXPENSES_CONFIG,
    CAR_EXPENSES_VALID_VALUES,
    CAR_PAYMENTS_CONFIG,
    CAR_PAYMENTS_VALID_VALUES,
    PENSION_CASHFLOWS_CONFIG,
    PENSION_CASHFLOWS_VALID_VALUES,
)
from .asset_classifier import classify_asset_types

# Google Sheets imports
try:
    import gspread
    from google.auth.exceptions import GoogleAuthError
    from google.oauth2.service_account import Credentials

    GOOGLE_SHEETS_AVAILABLE = True
except ImportError:
    GOOGLE_SHEETS_AVAILABLE = False


def _connect_to_google_sheets():
    """Establish connection to Google Sheets and return the client."""
    if not GOOGLE_SHEETS_AVAILABLE:
        st.error(
            "Google Sheets dependencies not installed. Please install: pip install gspread google-auth google-auth-oauthlib google-auth-httplib2"
        )
        return None

    try:
        google_config = st.secrets.get("google_sheets", {})
        spreadsheet_id = google_config.get("spreadsheet_id")

        if not spreadsheet_id:
            st.error("Google Sheets configuration error. Please check your setup.")
            return None

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        service_account_info = google_config.get("service_account_info")
        if service_account_info:
            creds = Credentials.from_service_account_info(
                service_account_info, scopes=scopes
            )
        else:
            credentials_path = google_config.get("credentials_path")
            if credentials_path and os.path.exists(credentials_path):
                creds = Credentials.from_service_account_file(
                    credentials_path, scopes=scopes
                )
            else:
                st.error(
                    "Google Sheets service account credentials not configured. Please set in .streamlit/secrets.toml"
                )
                return None

        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Failed to connect to Google Sheets: {str(e)}")
        return None


def _fetch_data_from_sheet(client, config):
    """Fetch data from a specific worksheet using the provided configuration."""
    try:
        spreadsheet_id = st.secrets.get("google_sheets", {}).get("spreadsheet_id")
        spreadsheet = client.open_by_key(spreadsheet_id)

        worksheet_name = config["sheet_name"]
        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            st.warning(f"Worksheet '{worksheet_name}' not found.")
            return None

        all_values = worksheet.get_all_values()
        if len(all_values) <= 1:
            st.warning(f"No data found in '{worksheet_name}'.")
            return None

        headers = all_values[0]
        data = all_values[1:]

        df = pd.DataFrame(data, columns=headers)

        # Validate required columns
        for col in config["required_columns"]:
            if col not in df.columns:
                st.error(f"Required column '{col}' not found in '{worksheet_name}'.")
                return None

        return df

    except Exception as e:
        st.error(f"Error fetching data from '{config['sheet_name']}': {str(e)}")
        return None


def _validate_data(df, validation_config):
    """Validate data against a dictionary of allowed values."""
    if df is None or validation_config is None:
        return

    for column, valid_values in validation_config.items():
        if column in df.columns:
            invalid_values = df[~df[column].isin(valid_values)][column].unique()
            if len(invalid_values) > 0:
                st.warning(
                    f"Unexpected values found in column '{column}': {', '.join(map(str, invalid_values))}"
                )


def _clean_and_process_data(df, config, validation_config=None):
    """Clean and process the DataFrame based on the provided configuration."""
    if df is None:
        return None

    # Handle currency and numeric columns
    for col in config["currency_columns"]:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace("£", "")
                .str.replace(",", "")
                .str.strip()
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in config["numeric_columns"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Handle date columns
    for col in config["date_columns"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")

    # Validate data before dropping rows
    if validation_config:
        _validate_data(df, validation_config)

    # Drop rows with NaN in required columns after processing
    df = df.dropna(subset=config["required_columns"])

    if df.empty:
        st.warning(
            f"No valid data remains for '{config['sheet_name']}' after cleaning."
        )
        return None

    return df


def _load_and_process_sheet(config, validation_config=None):
    """Generic function to load, clean, and process a sheet."""
    client = _connect_to_google_sheets()
    if client is None:
        return None

    df = _fetch_data_from_sheet(client, config)
    if df is None:
        return None

    return _clean_and_process_data(df, config, validation_config)


@st.cache_data
def load_data():
    """Load and preprocess the financial data from the Balance Sheet."""
    try:
        df = _load_and_process_sheet(BALANCE_SHEET_CONFIG, BALANCE_SHEET_VALID_VALUES)

        if df is None:
            st.error("Failed to load data from Balance Sheet.")
            return None

        if "Asset_Type" not in df.columns:
            df = classify_asset_types(df)

        month_period = df["Timestamp"].dt.to_period("M")
        monthly_asset_counts = df.groupby([month_period, "Asset"]).size()
        if (monthly_asset_counts > 1).any():
            st.info("Using latest entry for duplicate assets per month.")
            df = df.assign(Month=month_period)
            df = (
                df.sort_values("Timestamp")
                .groupby(["Month", "Asset"])
                .last()
                .reset_index()
            )
            df = df.drop(columns=["Month"])

        return df
    except Exception as e:
        st.error(f"Error processing data: {str(e)}")
        return None


@st.cache_data
def load_pension_cashflows():
    """Load and preprocess pension cashflow data."""
    return _load_and_process_sheet(
        PENSION_CASHFLOWS_CONFIG, PENSION_CASHFLOWS_VALID_VALUES
    )


@st.cache_data
def load_car_assets():
    """Load and preprocess car assets data."""
    return _load_and_process_sheet(CAR_ASSETS_CONFIG, CAR_ASSETS_VALID_VALUES)


@st.cache_data
def load_car_payments():
    """Load and preprocess car payments data."""
    return _load_and_process_sheet(CAR_PAYMENTS_CONFIG, CAR_PAYMENTS_VALID_VALUES)


@st.cache_data
def load_car_expenses():
    """Load and preprocess car expenses data."""
    return _load_and_process_sheet(CAR_EXPENSES_CONFIG, CAR_EXPENSES_VALID_VALUES)


def filter_data_by_date_range(df, start_date=None, end_date=None):
    """Filter data by date range."""
    if df is None:
        return None

    filtered_df = df.copy()

    if start_date:
        filtered_df = filtered_df[filtered_df["Timestamp"] >= start_date]

    if end_date:
        filtered_df = filtered_df[filtered_df["Timestamp"] <= end_date]

    return filtered_df


def get_month_range(df):
    """Get the month range from the data."""
    if df is None or df.empty:
        return None, None

    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    min_date = df["Timestamp"].min()
    max_date = df["Timestamp"].max()

    return min_date, max_date


def get_available_data_files():
    """Get list of available data files in raw and staging directories."""
    files = {"raw": [], "staging": []}

    # Check raw directory
    raw_dir = "data/raw"
    if os.path.exists(raw_dir):
        files["raw"] = [f for f in os.listdir(raw_dir) if f.endswith(".xlsx")]

    # Check staging directory
    staging_dir = "data/staging"
    if os.path.exists(staging_dir):
        files["staging"] = [f for f in os.listdir(staging_dir) if f.endswith(".xlsx")]

    return files
