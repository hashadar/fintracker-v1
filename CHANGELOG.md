# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.html).

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