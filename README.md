# FinTracker

A financial dashboard and analytics application built with Streamlit for tracking and analysing personal financial assets.

## Overview

FinTracker is a financial dashboard that provides insights into your financial portfolio. The application is structured as a multi-page Streamlit app, with dedicated pages for different asset classes.

### Key Features

-   **Multi-Asset Tracking**: Monitor cash, investments, and pensions with dedicated deep-dive pages.
-   **Car Equity Tracker**: A detailed dashboard for tracking vehicle equity, costs, depreciation, and PNL.
-   **Interactive Dashboards**: All pages feature interactive charts and tables to explore your data.
-   **Excel-Powered**: Data is managed through simple and transparent Excel files.

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

1.  **`202506_equity_hd.xlsx`**: For general financial assets (cash, investments, pensions). It requires the following columns:
    *   `Timestamp`: Date of the record.
    *   `Asset_Type`: Category of the asset (e.g., "Cash", "Investments").
    *   `Platform`: Specific platform or account name.
    *   `Value`: Monetary value of the asset.

2.  **`car_data.xlsx`**: For the Car Equity Tracker. This file and its required multi-sheet structure are generated automatically by the application. The "Cars" page contains a detailed in-app guide on how to populate this file.

## Financial Data ETL Process

For the main financial assets, the application processes data through a simple ETL pipeline:

1.  **Extract**: Data is extracted from `202506_equity_hd.xlsx`.
2.  **Transform**:
    -   Timestamps are converted to datetime format.
    -   Assets are categorised into types (Cash, Investments, Pensions).
    -   Data is aggregated to ensure one entry per platform-asset per month.
3.  **Load**: Processed data is cached for performance and used to generate metrics and visualizations on demand.

## Project Structure

-   `Home.py`: The main landing page for the application.
-   `pages/`: Directory containing the individual dashboard pages (Overview, Cash, Investments, Pensions, All Assets, Cars).
-   `utils/`: General utility modules for the main financial dashboards.
-   `utils/car/`: Utility modules specific to the Car Equity Tracker.
-   `car_equity_development_plan.md`: The detailed development plan for the car equity feature.
-   `requirements.txt`: Python package dependencies.

## Development Roadmap

### Completed

-   **Multi-page Application Refactor**: The application has been successfully restructured into a modern, multi-page Streamlit app.
-   **Car Equity Tracker**: A comprehensive module for tracking vehicle finance, costs, and equity has been implemented.

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

## License

This project is licensed under the terms of the license included in the repository.

## Support

For support, please open an issue in the GitHub repository.

---

*Author: hasha dar*