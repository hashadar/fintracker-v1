# FinTracker

A financial dashboard and analytics application built with Streamlit for tracking and analysing personal financial assets.

## Overview

FinTracker is a financial dashboard that provides insights into your financial portfolio. The application is structured as a multi-page Streamlit app, with dedicated pages for different asset classes and a comprehensive car equity tracker.

### Key Features

-   **Multi-Asset Tracking**: Monitor cash, investments, and pensions with dedicated deep-dive pages.
-   **Car Equity Tracker**: A detailed dashboard for tracking vehicle equity, costs, depreciation, and PNL.
-   **Interactive Dashboards**: All pages feature interactive charts and tables to explore your data.
-   **Excel-Powered**: Data is managed through simple and transparent Excel files.
-   **Consistent UI Components**: Reusable card components for consistent metric display across all pages.

## Data Privacy

This repository is configured to exclude financial data files from version control. The `.gitignore` file is set up to ignore:

-   Excel files (`*.xlsx`, `*.xls`)
-   CSV files (`*.csv`)

Your financial data files will remain on your local machine and will not be committed to the repository.

## Installation

1.  Clone the repository:
    ```powershell
    git clone https://github.com/yourusername/fintracker-v1.git
    cd fintracker-v1
    ```

2.  Create a virtual environment (recommended):
    ```powershell
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    ```

3.  Install dependencies:
    ```powershell
    pip install -r requirements.txt
    ```

## Usage

1.  Start the Streamlit application:
    ```powershell
    streamlit run Home.py
    ```

2.  Open your web browser and navigate to the URL shown in the terminal (typically `http://localhost:8501`).

3.  Use the sidebar to navigate between the Home page and the different asset dashboards.

## Data Structure

The application uses two main data files:

1.  **`data/202506_equity_hd.xlsx`**: For general financial assets (cash, investments, pensions). It requires the following columns:
    *   `Timestamp`: Date of the record.
    *   `Asset_Type`: Category of the asset (e.g., "Cash", "Investments").
    *   `Platform`: Specific platform or account name.
    *   `Value`: Monetary value of the asset.

2.  **`data/car_data.xlsx`**: For the Car Equity Tracker. This file and its required multi-sheet structure are generated automatically by the application. The "Cars" page contains a detailed in-app guide on how to populate this file.

## UI Components

### Card Components

The application uses a set of reusable card components for consistent metric display:

- **`simple_card`**: Basic metric display with title, value, and optional caption
- **`emphasis_card`**: Highlighted card with emphasis styling for important metrics
- **`complex_card`**: Metric with Month-over-Month (MoM) and Year-to-Date (YTD) change indicators
- **`complex_emphasis_card`**: Emphasis card with change indicators

#### Usage Guidelines

- Use `simple_card` for summary metrics without change tracking (e.g., "Maximum Drawdown", "Best Month")
- Use `complex_card` for metrics with change indicators (e.g., asset type totals with MoM/YTD changes)
- Use `emphasis_card` or `complex_emphasis_card` for the most important metrics (e.g., portfolio total)
- All card components automatically handle HTML escaping and conditional rendering

### Design System

The application uses a consistent design system with:
- **Design Tokens**: Centralized color, spacing, and typography definitions
- **Responsive Layout**: Cards and components adapt to different screen sizes
- **Accessibility**: Proper contrast ratios and semantic HTML structure

## Financial Data ETL Process

For the main financial assets, the application processes data through a simple ETL pipeline:

1.  **Extract**: Data is extracted from `data/202506_equity_hd.xlsx`.
2.  **Transform**:
    -   Timestamps are converted to datetime format.
    -   Assets are categorised into types (Cash, Investments, Pensions).
    -   Data is aggregated to ensure one entry per platform-asset per month.
    -   Month-over-Month and Year-to-Date changes are calculated.
3.  **Load**: Processed data is cached for performance and used to generate metrics and visualizations on demand.

## Project Structure

```
fintracker-v1/
├── Home.py                 # Main landing page
├── pages/                  # Dashboard pages
│   ├── 1_Overview.py      # Portfolio overview with summary cards
│   ├── 2_Cash.py          # Cash assets dashboard
│   ├── 3_Investments.py   # Investment assets dashboard
│   ├── 4_Pensions.py      # Pension assets dashboard
│   ├── 6_Cars.py          # Car equity tracker
│   └── 7_Card_Demo.py     # Card component demonstration
├── utils/                  # Utility modules
│   ├── __init__.py        # Module exports
│   ├── metrics.py         # Financial metrics calculations
│   ├── visualizations.py  # Card components and charts
│   ├── design_tokens.py   # Design system constants
│   ├── data_loader.py     # Data loading and processing
│   └── car/               # Car-specific utilities
│       ├── car_metrics.py      # Car financial calculations
│       ├── car_forecasting.py  # Depreciation and cost forecasting
│       └── car_data_manager.py # Car data file management
├── data/                  # Data files (gitignored)
└── requirements.txt       # Python dependencies
```

## Development Roadmap

### Completed

-   **Multi-page Application Refactor**: The application has been successfully restructured into a modern, multi-page Streamlit app.
-   **Car Equity Tracker**: A comprehensive module for tracking vehicle finance, costs, and equity has been implemented.
-   **Card Component System**: Reusable card components with consistent styling and HTML escaping.
-   **Design System**: Centralized design tokens and consistent UI patterns.

### Future Work

-   **Enhanced Data Integration**:
    -   Implement proper tracking of cash flows (inflows and outflows).
    -   Integrate bank and financial institution APIs for automated data collection.
-   **Application Features**:
    -   Add a dedicated settings and configuration page.
    -   Allow data exports to CSV/Excel.
-   **Analytics**:
    -   Implement comparison periods (e.g., year-over-year).
    -   Add support for multiple currencies.

## Dependencies

-   streamlit
-   pandas
-   numpy
-   plotly
-   openpyxl

## Contributing

Contributions are welcome. Please submit a Pull Request.

### Development Guidelines

- Follow the established card component patterns for new metric displays
- Use the design tokens from `utils/design_tokens.py` for consistent styling
- Add concise, meaningful comments to important logic in utility functions
- Ensure all user-facing text is properly HTML-escaped

## License

This project is licensed under the terms of the license included in the repository.

## Support

For support, please open an issue in the GitHub repository.

---

*Author: hasha dar*