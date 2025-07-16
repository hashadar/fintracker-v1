# FinTracker v1.1.0

A financial dashboard and analytics application built with Streamlit for tracking and analyzing personal financial assets.

## Overview

FinTracker is a financial dashboard that provides insights into your financial portfolio. The application connects to Google Sheets to load your financial data and automatically categorizes assets into Cash, Investments, and Pensions.

**All configuration, chart styling, and validation are now fully centralized and standardized for maintainability and safety.**

## Current Features

- **Multi-Asset Tracking**: Monitor cash, investments, and pensions with dedicated dashboard pages
- **Google Sheets Integration**: Direct connection to Google Sheets for data management
- **Automatic Asset Classification**: Assets are categorized based on their names and platforms
- **Interactive Dashboards**: Charts, tables, and metrics for each asset type
- **Monthly Data Processing**: Handles monthly snapshots with automatic deduplication
- **Performance Metrics**: Returns, volatility, drawdown, and other financial metrics
- **Modular Architecture**: Clean, maintainable codebase with reusable components
- **Design System**: Consistent UI with centralized design tokens and card components
- **Centralized Configuration & Validation**: All business logic, formatting, and chart styling are managed in config and design tokens, with automatic validation on startup

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
│   ├── wrappers.py  # Chart wrapper functions
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

## License

This project is licensed under the terms of the license included in the repository.

---

*Author: hasha dar*