# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.html).

---

## [2.2.0] - 2025-07-20

### Added
- **Code Quality Tooling**: Integrated `black` for standardized code formatting and `Ruff` for high-speed linting, import sorting, and automatic error correction.
- **Homepage Data Status**: The homepage now features a dynamic status section that reports the load status and record count for each individual data source.

### Changed
- **Data Loading Refactoring**: Completely refactored the data loading pipeline in `utils/etl/data_loader.py`. All data loading and cleaning logic is now centralized into generic, reusable functions that are driven by sheet-specific configurations.
- **Configuration-Driven Validation**: The data loader now uses centralized validation rules from `utils/config.py` to check for unexpected values in the source data and provide warnings.
- **Simplified Asset Classification**: Replaced the complex, rule-based asset classifier with a simple, lookup-based system that uses mappings defined in `utils/config.py`.
- **Improved Data Reloading**: The "Reload Data" button now clears all of Streamlit's caches to ensure fresh data is always loaded.
- **Code Formatting**: Applied `black` and `Ruff` to the entire codebase to standardize formatting and resolve linting errors.

### Removed
- **Unused Configuration**: Removed several unused variables from `utils/config.py` to reduce clutter.

## [2.1.0] - 2025-07-19

### Added
- **Vehicle Tracking System**: Comprehensive vehicle tracking for both financed and owned vehicles
- **Vehicle Dashboard**: Dedicated page with summary metrics, analytics charts, and cost analysis
- **Loan Payment Tracking**: Track vehicle loan payments with support for different payment types
- **Vehicle Expense Tracking**: Monitor operating costs including insurance, fuel, maintenance, and other expenses
- **Mileage Tracking**: Track vehicle mileage with YTD calculations and cost per mile analysis
- **Vehicle Equity Analysis**: Calculate and track vehicle equity position over time
- **Stacked Area Charts**: Monthly combined costs visualization with loan payments and expenses
- **Cost Per Mile Metrics**: YTD cost per mile calculation including both loan payments and operating expenses
- **Vehicle Summary Metrics**: Total car value, equity, loan balance, and latest mileage tracking

### Changed
- **Enhanced Data Processing**: Added vehicle-specific data processing functions with YTD mileage calculations
- **Improved Analytics Components**: Created reusable vehicle analytics component with standardized chart grid
- **Code Organization**: Moved all vehicle calculations to data processing module for better maintainability
- **Design System**: Extended design system to support vehicle tracking UI components

---

## [2.0.0] - 2025-07-17

### Added
- **Pension Cashflow Tracking**: Integrated a new `Pension Cashflows` Google Sheet to track contributions, fees, and transfers.
- **Actual Returns Calculation**: Implemented true return calculations for pensions, which factor out the impact of cashflows to provide a clear measure of investment performance.
- **Interactive Pension Forecasting**: Added a "Pension Growth Forecast" section with a Monte Carlo simulation to project future values. Users can adjust the forecast horizon, expected return, and future monthly contributions.
- **Development Standards**: Added a note to the `README.md` encouraging the use of conventional commit messages.
- **Changelog**: Created this `CHANGELOG.md` file to track version history.

### Changed
- **Grouped Bar Charts**: Refactored the "Month-over-Month Changes" bar charts for both investments and pensions to be grouped instead of stacked, allowing for clearer side-by-side asset comparison.
- **Project Version**: Updated project version to `2.0.0` across all `README.md` files.
- **Documentation**: Updated all `README.md` files to reflect the new cashflow and forecasting features and data requirements.

---

## [1.0.0] - 2025-06-06

### Added
- **Initial Alpha Release**: Core application functionality and design system.
- **Asset Tracking**: Implemented tracking for Cash, Investments, and Pensions from Google Sheets.
- **Interactive Dashboards**: Created dedicated pages with interactive charts and metrics for each asset type.
- **Standardized Codebase**: Established a modular architecture with a centralized design system, configuration, and reusable components for charts and UI elements.
