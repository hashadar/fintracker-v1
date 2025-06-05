# FinTracker

A financial dashboard and analytics application built with Streamlit for tracking and analysing personal financial assets.

## Data Privacy

This repository is configured to exclude financial data files from version control. The following files are ignored:
- Excel files (*.xlsx, *.xls)
- CSV files (*.csv)
- Financial data directories

To use the application:
1. Place your financial data files in the project directory
2. Ensure the files follow the required data structure
3. The files will remain local and will not be committed to the repository

## Overview

FinTracker is a financial dashboard that provides insights into financial portfolios, including cash positions, investments, and pensions. The application offers overviews and detailed analytics for each asset type.

## ETL Process

The application processes financial data through the following ETL pipeline:

1. **Extract**
   - Data is extracted from Excel files (e.g., `202506_equity_hd.xlsx`)
   - Required columns: Timestamp, Platform, Asset, Value

2. **Transform**
   - Timestamps are converted to datetime format
   - Assets are categorised into types (Cash, Investments, Pensions)
   - Data is aggregated to ensure one entry per platform-asset per month
   - Duplicate entries are resolved by using the latest value

3. **Load**
   - Processed data is cached for performance
   - Data is filtered based on selected date ranges
   - Metrics are calculated in real-time
   - Visualisations are generated on demand

## Features

- 📊 Dashboard: Visualisation of financial portfolio
- 💰 Asset Type Tracking: Monitor cash, investments, and pensions
- 📈 Performance Metrics: Track month-over-month and year-to-date changes
- 🔍 Analysis: Detailed breakdowns for each asset type
- 📱 Responsive Design: Interface that works on all devices
- 📅 Date Range Selection: Analyse data for any time period

## Key Metrics Tracked

- Total Portfolio Value
- Asset Allocation Percentages
- Month-over-Month (MoM) Changes
- Year-to-Date (YTD) Performance
- Platform-specific Breakdowns
- Asset Type Composition

## Installation

1. Clone the repository:
```powershell
git clone https://github.com/yourusername/fintracker-v1.git
cd fintracker-v1
```

2. Create a virtual environment (recommended):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:
```powershell
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit application:
```powershell
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Use the sidebar to:
   - Select date ranges for analysis
   - Navigate between different views (Overview, Cash Deep Dive, etc.)
   - Filter and analyse specific asset types

## Data Structure

The application requires financial data in an Excel file format with the following structure:
- Timestamp: Date of the record
- Asset_Type: Category of the asset (Cash, Investments, Pensions)
- Platform: Specific platform or account name
- Value: Monetary value of the asset

## Project Structure

- `app.py`: Main Streamlit application
- `utils/`: Utility modules (see [utils/README.md](utils/README.md) for details)
  - `data_loader.py`: Data loading and preprocessing
  - `metrics.py`: Financial calculations
  - `visualizations.py`: Chart and component creation
  - `constants.py`: Application configuration

## Development Roadmap

### Data Collection and Integration
- Implement proper tracking of cash flows (inflows and outflows)
- Integrate bank APIs for automated data collection
- Add support for financial institution APIs (e.g., investment platforms)
- Develop car equity tracking module
  - Track vehicle value depreciation
  - Monitor maintenance costs
  - Financial information such as equity

### Application Architecture
- Refactor into a multi-page application
  - Separate pages for different asset types
  - Dedicated pages for analysis and reporting
  - Settings and configuration page
- Componentise the application
  - Create reusable dashboard components
  - Develop standardised chart components
  - Implement consistent styling system

### Analytics and Metrics
- Consolidate financial metrics
  - Standardise calculation methods
  - Implement proper metric documentation
  - Add validation and error handling
- Enhance data slicing capabilities
  - Add custom date range analysis
  - Implement comparison periods
  - Support multiple currency tracking
  - Add export functionality for reports

## Dependencies

- streamlit: Web application framework
- pandas: Data manipulation and analysis
- numpy: Numerical computing
- plotly: Interactive visualisations
- openpyxl: Excel file handling

## Contributing

Contributions are welcome. Please submit a Pull Request.

## License

This project is licensed under the terms of the license included in the repository.

## Support

For support, please open an issue in the GitHub repository.

---

Author: hasha dar