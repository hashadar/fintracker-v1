# FinTracker v2.1.0

A financial dashboard and analytics application built with Streamlit for tracking and analyzing personal financial assets, now with cashflow tracking, forecasting capabilities, and comprehensive vehicle tracking.

## Overview

FinTracker is a financial dashboard that provides insights into your financial portfolio. The application connects to Google Sheets to load your financial data and automatically categorizes assets into Cash, Investments, and Pensions.

**This version introduces our first integration with cashflow data, allowing for more accurate performance metrics and powerful forecasting features, plus comprehensive vehicle tracking for both financed and owned vehicles.**

## Current Features

- **Multi-Asset Tracking**: Monitor cash, investments, pensions, and vehicles with dedicated dashboard pages
- **Google Sheets Integration**: Direct connection to Google Sheets for asset values, cashflow data, and vehicle tracking
- **Vehicle Tracking**: Comprehensive tracking for both financed and owned vehicles with loan payments, expenses, and mileage
- **Pension Cashflow Tracking**: Track contributions, fees, and transfers for pension accounts
- **Actual Returns Calculation**: Pension performance metrics now account for cash inflows and outflows, providing a true investment return
- **Interactive Pension Forecasting**: Forecast future pension growth with a simple Monte Carlo simulation, adjustable for contributions and market returns
- **Vehicle Analytics**: Stacked area charts for monthly costs, equity position tracking, and cost per mile analysis
- **Automatic Asset Classification**: Assets are categorized based on their names and platforms
- **Interactive Dashboards**: Charts, tables, and metrics for each asset type, now including grouped bar charts for easier comparison
- **Monthly Data Processing**: Handles monthly snapshots with automatic deduplication
- **Performance Metrics**: Returns, volatility, drawdown, and other financial metrics
- **Modular Architecture**: Clean, maintainable codebase with reusable components
- **Design System**: Consistent UI with centralized design tokens and card components
- **Centralized Configuration & Validation**: All business logic, formatting, and chart styling are managed in config and design tokens, with automatic validation on startup
- **Componentized Summary Cards & Analytics**: All summary statistics, analytics, and time period breadcrumbs are now reusable components
- **Legacy Cleanup**: Unused functions and components have been removed for clarity and maintainability
- **Import & Serialization Fixes**: All import errors and pandas serialization issues have been resolved

## Architecture

The application follows a modular architecture with clear separation of concerns:

```
utils/
├── design/           # UI components and design tokens
│   ├── cards.py     # Reusable card components
│   ├── components.py # Layout components
│   └── tokens.py    # Design tokens (colors, spacing, fonts)
├── charts/          # Chart creation and formatting
│   ├── base.py      # Base chart functions
│   ├── formatting.py # Axis and data formatting
│   └── asset_types.py # Asset-specific charts
├── etl/             # Data loading and asset classification
│   ├── data_loader.py
│   └── asset_classifier.py
├── data_processing.py # Data processing utilities
└── config.py        # Centralized configuration constants
```

## Data Structure

The application expects Google Sheets data with these columns:
- `Timestamp`: Date of the record (d/m/y format)
- `Platform`: Platform or account name (e.g., "Monzo", "Vanguard")
- `Asset`: Specific asset name
- `Value`: Monetary value in pounds sterling
- `Token Amount`: Optional field for crypto assets

The application also supports a `Pension Cashflows` sheet with the following columns:
- `Timestamp`: Date of the cashflow event
- `Platform`: Pension provider name
- `Asset`: Specific pension product/scheme
- `Value`: Monetary value of the cashflow
- `Cashflow Type`: The type of cashflow (e.g., 'Contribution', 'Fee', 'Transfer')
- `Description`: A description of the cashflow (e.g., 'Employer contribution')

### Vehicle Tracking Sheets

The application supports three additional Google Sheets for vehicle tracking:

**Car Assets Sheet:**
- `Timestamp`: Date of the record
- `Asset`: Vehicle name (e.g., "BMW X3")
- `Car_Value`: Current market value of the vehicle
- `Loan_Balance`: Outstanding loan balance (0 for owned vehicles)
- `Loan_Status`: "Financed" or "Owned"
- `Mileage`: Current mileage reading

**Car Payments Sheet:**
- `Timestamp`: Date of the payment
- `Asset`: Vehicle name
- `Payment_Amount`: Payment amount
- `Payment_Type`: Type of payment (e.g., "Regular", "Extra")

**Car Expenses Sheet:**
- `Timestamp`: Date of the expense
- `Asset`: Vehicle name
- `Amount`: Expense amount
- `Expense_Type`: Type of expense (e.g., "Insurance", "Fuel", "Maintenance")

## Installation

1. Clone the repository and navigate to the directory
2. Create a virtual environment: `python -m venv .venv`
3. Activate the environment: `.\.venv\Scripts\Activate.ps1`
4. Install dependencies: `pip install -r requirements.txt`

## Setup

1. Create a Google Sheets service account and download the JSON credentials
2. Create `.streamlit/secrets.toml` with your Google Sheets configuration
3. Share your Google Sheet with the service account email
4. Run the app: `streamlit run Home.py`

## Pages

- **Home**: Portfolio overview and summary metrics
- **All Assets**: Complete portfolio analysis
- **Cash**: Cash assets dashboard
- **Investments**: Investment assets dashboard  
- **Pensions**: Pension assets dashboard
- **Vehicles**: Vehicle tracking dashboard with loan payments, expenses, and mileage analytics

## Dependencies

- streamlit
- pandas
- numpy
- plotly
- gspread
- google-auth

## Development

The codebase is fully standardized:

- **Design System**: Centralized design tokens and reusable UI components
- **Chart System**: Modular chart creation with wrapper functions for common patterns
- **Layout Components**: Consistent page layouts across all dashboard pages
- **Configuration & Validation**: All business logic, formatting, and chart styling are managed in config and design tokens, with automatic validation
- **Code Organization**: Clean separation of concerns with dedicated modules
- **Commit Messages**: Follow conventional commit standards for a clear and organized history (e.g., `feat:`, `fix:`, `docs:`).

## License

This project is licensed under the terms of the license included in the repository.

---

*Author: hasha dar*