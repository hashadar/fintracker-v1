# Application Pages

This directory contains the individual Python scripts that serve as the pages for the multi-page Streamlit application.

## Naming Convention

The files are named using a `NUMBER_NAME.py` convention. Streamlit uses this naming scheme to automatically create a sidebar for navigation, ordering the pages based on the number and using the file name (with underscores replaced by spaces) as the display title.

For example, `2_All_Assets.py` becomes the second link in the sidebar, displayed as "All Assets".

## Pages

-   `Home.py`: The main dashboard for the financial portfolio, showing top-level metrics and visualizations.
-   `2_All_Assets.py`: A comprehensive analysis across all asset types (Cash, Investments, Pensions) with portfolio summary, performance analytics, and allocation analysis.
-   `3_Cash.py`: A detailed deep-dive into cash assets with platform analysis, time series trends, and liquidity metrics.
-   `4_Investments.py`: A detailed deep-dive into investment assets with performance analytics, risk analysis, and asset allocation breakdowns.
-   `5_Pensions.py`: A detailed deep-dive into pension assets with long-term growth analysis, retirement planning metrics, and scheme analysis.
-   `7_Card_Demo.py`: Development/testing page for card components (to be removed in production).

## Standardization

All pages now use:
- Centralized configuration constants for asset types, formatting, and business logic
- Standardized layout components (headers, sections, metric grids, chart grids)
- Consistent chart styling and formatting
- Reusable data processing functions
- Automatic configuration validation

## Page Features

Each page provides:
- Portfolio summary with key metrics
- Performance analytics with charts
- Asset allocation breakdowns
- Time series analysis
- Platform and asset distribution
- Risk and performance metrics 