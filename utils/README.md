# Utility Modules

This directory contains general utility modules that support the main financial dashboard application.
For utilities specific to car equity tracking, please see [`utils/car/README.md`](car/README.md).

## Modules

### `data_loader.py`
Handles loading and preprocessing for the main financial dataset:
- Loads financial data from the primary Excel file (e.g., `master_data.xlsx`).
- Converts timestamps to datetime format.
- Categorises assets based on predefined types (Cash, Investments, Pensions).
- Ensures data integrity, for instance, by handling potential duplicate entries for the same asset on the same date.
- Provides date range filtering functions for the main dataset.
- Handles saving updated data back to the primary Excel file.

### `metrics.py`
Calculates financial metrics and analytics for the main dataset:
- Asset type-specific metrics (e.g., latest value, month-over-month change, counts of unique platforms).
- Overall portfolio metrics (e.g., total value, aggregate MoM/YTD changes).
- Allocation metrics (e.g., percentage breakdown by asset type, changes in allocation).
- Platform and asset breakdowns within each asset type.

### `visualizations.py`
Creates reusable visual components and charts for the dashboard:
- Standardised Key Performance Indicator (KPI) card component for displaying metrics.
- Functions to generate various Plotly charts for time series, breakdowns, etc., used across different dashboard pages.
- May include helper functions for formatting data for display.

### `constants.py`
Defines application-wide constants and configurations not specific to a single feature:
- Predefined asset type categories (e.g., `ASSET_TYPES = ["Cash", "Investments", "Pensions"]`).
- Custom CSS styling for the Streamlit dashboard for a consistent look and feel.
- Default page configuration details like titles or shared descriptions if any.

## Usage

These modules are imported and used by the main application (`app.py`) and the various page modules in the `pages/` directory. Each module provides specific, reusable functionality:

1. `data_loader.py` is used for initial loading, saving, and filtering of the main financial data.
2. `metrics.py` provides the calculation engine for financial metrics displayed on the dashboard.
3. `visualizations.py` supplies tools for creating consistent charts and visual elements.
4. `constants.py` centralises shared configurations and static values.

## Data Flow Example (Main Data)

1. Data is loaded and preprocessed by `data_loader.load_data()`.
2. User interactions (e.g., date range selection) might trigger data refiltering via `data_loader` functions.
3. Relevant subsets of data are passed to page modules (e.g., `pages/cash.py`).
4. Page modules use `metrics.py` to calculate necessary financial figures for display.
5. `visualizations.py` is then used to generate charts and KPI cards based on these metrics.
6. `constants.py` provides underlying definitions (like asset types) and styling throughout this process. 