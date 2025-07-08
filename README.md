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

Claude potential new ETL structure:

# Technical Specification: Monthly Equity Tracker ETL Pipeline & Metrics Engine

## Overview

This document outlines the technical requirements for an ETL pipeline designed specifically for **monthly snapshot data**, where each asset-platform combination has at most one entry per month.

## Data Model & Constraints

### Input Schema
```
Platform: string          # Brokerage/bank identifier
Asset: string            # Asset name or type
Value: float             # Current value in GBP
Timestamp: float         # Excel serial date number (monthly snapshot)
Token Amount: float      # Quantity (nullable, for crypto)
```

### Monthly Data Structure
- **Frequency**: One snapshot per asset-platform per month
- **Snapshot Date**: Derived from timestamp, normalized to month
- **Key Constraint**: (Platform, Asset, Year-Month) is unique

### Derived Time Dimensions
```python
snapshot_date: date       # Actual date of snapshot
snapshot_month: int      # Month (1-12)
snapshot_year: int       # Year
snapshot_yearmonth: str  # YYYY-MM format
months_since_start: int  # Months from first snapshot
```

## Core ETL Transformations

### 1. Monthly Snapshot Normalization
```python
# Group all records by year-month
# Verify single entry per asset-platform-month
# Handle multiple snapshots in same month (take latest)
def normalize_to_monthly(df):
    df['yearmonth'] = df['datetime'].dt.to_period('M')
    return df.groupby(['Platform', 'Asset', 'yearmonth']).last()
```

### 2. Complete Monthly Time Series
Create a complete monthly grid:
```
For each month M in [first_snapshot, last_snapshot]:
    For each asset A ever observed:
        If A not in M:
            Forward-fill from most recent month
            Mark as imputed
```

## Monthly Metrics Framework

### Portfolio-Level Metrics

#### 1. Monthly Portfolio Value
```
TPV(m) = Σ Value(i,m) for all assets i in month m
```

#### 2. Month-over-Month (MoM) Return
```
MoM_Return(m) = (TPV(m) - TPV(m-1)) / TPV(m-1)
MoM_Log_Return(m) = ln(TPV(m) / TPV(m-1))
```

#### 3. Compound Monthly Growth Rate (CMGR)
```
CMGR = (TPV(last) / TPV(first))^(1/n_months) - 1
```

#### 4. Annualized Return
```
Annual_Return = (1 + CMGR)^12 - 1
```

### Rolling Window Metrics

#### 1. Rolling Returns (3M, 6M, 12M)
```
Rolling_3M_Return(m) = (TPV(m) - TPV(m-3)) / TPV(m-3)
Rolling_6M_Return(m) = (TPV(m) - TPV(m-6)) / TPV(m-6)
Rolling_12M_Return(m) = (TPV(m) - TPV(m-12)) / TPV(m-12)
```

#### 2. Rolling Volatility
```
Rolling_Vol_12M(m) = σ(monthly_returns[m-11:m])
Annualized_Vol = Rolling_Vol_12M * √12
```

#### 3. Rolling Sharpe Ratio
```
Rolling_Sharpe_12M(m) = (μ(returns[m-11:m]) * 12) / (σ(returns[m-11:m]) * √12)
```

### Year-to-Date (YTD) Metrics
For each month m:
```
YTD_Return(m) = (TPV(m) - TPV(Dec_prev_year)) / TPV(Dec_prev_year)
YTD_Months = Number of months in current year up to m
YTD_Avg_Monthly_Return = YTD_Return / YTD_Months
YTD_High = max(TPV(j)) for j in [Jan, m]
YTD_Drawdown = (TPV(m) - YTD_High) / YTD_High
```

### Quarter Metrics
```
Quarter_Start_Month = First month of current quarter
QTD_Return(m) = (TPV(m) - TPV(Quarter_Start)) / TPV(Quarter_Start)
Quarterly_Return = Return for complete quarters only
```

### Statistical Metrics (Monthly-Adjusted)

#### 1. Monthly Volatility
```
σ_monthly = √(Σ(r_i - μ)² / (n-1))
where r_i are monthly returns
```

#### 2. Annualized Volatility
```
σ_annual = σ_monthly * √12
```

#### 3. Downside Deviation (Monthly)
```
σ_downside = √(Σ min(0, r_i - MAR)² / n)
where MAR = Minimum Acceptable Return (monthly)
```

#### 4. Maximum Drawdown (Peak-to-Trough)
```
Running_Peak(m) = max(TPV(i)) for all i ≤ m
Drawdown(m) = (TPV(m) - Running_Peak(m)) / Running_Peak(m)
Max_Drawdown = min(Drawdown(m)) for all m
Recovery_Time = Months from trough to new peak
```

#### 5. Calmar Ratio (Monthly)
```
Calmar = (CMGR * 12) / |Max_Drawdown|
```

#### 6. Monthly Value at Risk
```
VaR_95_monthly = 5th percentile of monthly returns
VaR_95_annual = VaR_95_monthly * √12 (assuming normal distribution)
```

### Growth Analysis

#### 1. Trend Decomposition
```
TPV(m) = Trend(m) + Seasonal(m) + Residual(m)
Trend: 12-month moving average
Seasonal: Average deviation by calendar month
```

#### 2. Growth Persistence
```
Growth_Streak = Consecutive months of positive MoM growth
Decline_Streak = Consecutive months of negative MoM growth
Hit_Rate = Percentage of positive growth months
```

#### 3. Momentum Indicators
```
Momentum_3M = TPV(m) / TPV(m-3)
Momentum_12M = TPV(m) / TPV(m-12)
Momentum_Score = Weighted average of multiple periods
```

### Asset-Level Monthly Metrics

#### 1. Asset Monthly Returns
```
Asset_Return(i,m) = (Value(i,m) - Value(i,m-1)) / Value(i,m-1)
```

#### 2. Contribution to Portfolio Return
```
Weight(i,m-1) = Value(i,m-1) / TPV(m-1)
Contribution(i,m) = Weight(i,m-1) * Asset_Return(i,m)
Verify: Σ Contribution(i,m) ≈ Portfolio_Return(m)
```

#### 3. Asset Persistence Metrics
```
Months_Held = Count of months asset appears
Holding_Period_Return = (Value_last - Value_first) / Value_first
Average_Weight = Mean(Weight(i,m)) for all m
Max_Weight = Max(Weight(i,m)) for all m
```

### Correlation & Diversification (Monthly)

#### 1. Asset Correlation Matrix
```
ρ(i,j) = Correlation of monthly returns between assets i and j
Required: Minimum 12 months of overlapping data
```

#### 2. Portfolio Diversification Metrics
```
Average_Correlation = Mean of pairwise correlations
Diversification_Ratio = σ(weighted_avg) / σ(portfolio)
Principal_Component_Weight = Weight of first PC in variance
```

## Monthly Forecasting Methods

### 1. Simple Moving Average Forecast
```
SMA_Forecast(m+1) = Mean(TPV[m-11:m])
SMA_Growth_Rate = Mean(MoM_Returns[m-11:m])
```

### 2. Exponential Smoothing (Monthly)
```
EMA(m) = α * TPV(m) + (1-α) * EMA(m-1)
Forecast(m+h) = EMA(m) * (1 + trend)^h
```

### 3. Seasonal Naive Forecast
```
Seasonal_Forecast(m+1) = TPV(m-11) * Growth_Factor
Growth_Factor = Median yearly growth rate
```

### 4. Linear Regression on Time
```
TPV(m) = β₀ + β₁ * months_since_start + ε
Forecast(m+h) = β₀ + β₁ * (months_since_start + h)
```

### 5. ARIMA for Monthly Data
```
Typical models for monthly financial data:
ARIMA(1,1,1): AR(1) with differencing and MA(1)
SARIMA(1,1,1)(1,1,1)12: With monthly seasonality
```

### 6. Monte Carlo Simulation (Monthly)
```
1. Fit distribution to monthly returns
2. Generate N scenarios of h months
3. For each path: TPV(m+h) = TPV(m) * ∏(1 + r_i)
4. Calculate percentiles for confidence intervals
```

### 7. Regime-Based Forecasting
```
Identify regimes: Bull (μ > 0, low σ), Bear (μ < 0, high σ)
Estimate transition probabilities
Forecast based on current regime and transition matrix
```

## Output Data Structures

### 1. Monthly Metrics DataFrame
```python
monthly_metrics = {
    'yearmonth': 'YYYY-MM',
    'snapshot_date': date,
    'months_since_start': int,
    
    # Portfolio values
    'tpv': float,
    'num_assets': int,
    'num_platforms': int,
    
    # Returns
    'mom_return': float,
    'mom_log_return': float,
    'ytd_return': float,
    'qtd_return': float,
    'rolling_3m_return': float,
    'rolling_6m_return': float,
    'rolling_12m_return': float,
    
    # Volatility metrics
    'rolling_12m_volatility': float,
    'rolling_12m_downside_vol': float,
    'ytd_volatility': float,
    
    # Risk metrics
    'drawdown': float,
    'months_since_peak': int,
    'rolling_12m_sharpe': float,
    'rolling_12m_sortino': float,
    
    # Growth metrics
    'growth_streak': int,
    'momentum_3m': float,
    'momentum_12m': float,
    
    # Concentration
    'herfindahl_index': float,
    'effective_assets': float,
    
    # Forecasts
    'forecast_next_month': float,
    'forecast_3m': float,
    'forecast_12m': float,
    'forecast_confidence_lower': float,
    'forecast_confidence_upper': float
}
```

### 2. Asset Monthly Metrics DataFrame
```python
asset_metrics = {
    'yearmonth': 'YYYY-MM',
    'platform': str,
    'asset': str,
    'asset_id': str,
    
    # Values and weights
    'value': float,
    'weight': float,
    'weight_change': float,
    
    # Returns
    'monthly_return': float,
    'contribution_to_return': float,
    'ytd_return': float,
    
    # Tracking
    'months_held': int,
    'is_new': bool,
    'is_imputed': bool,
    
    # Crypto specific
    'token_amount': float,
    'token_price': float,
    'price_return': float,
    'quantity_return': float
}
```

### 3. Forecast Scenarios DataFrame
```python
forecast_scenarios = {
    'forecast_month': 'YYYY-MM',
    'months_ahead': int,
    'forecast_method': str,
    
    # Point estimates
    'forecast_value': float,
    'forecast_return': float,
    
    # Confidence intervals
    'ci_50_lower': float,
    'ci_50_upper': float,
    'ci_90_lower': float,
    'ci_90_upper': float,
    
    # Scenario analysis
    'bear_case': float,  # 10th percentile
    'base_case': float,  # 50th percentile
    'bull_case': float,  # 90th percentile
    
    # Model quality (backtested)
    'mae': float,  # Mean absolute error
    'rmse': float, # Root mean square error
    'directional_accuracy': float
}
```

## Implementation Considerations

### Monthly Data Handling
1. **Sparse Data**: Handle months where not all assets are updated
2. **Alignment**: Ensure all metrics align to month boundaries
3. **Minimum History**: Most metrics require 12+ months of data
4. **Seasonality**: Account for month-of-year effects

### Computational Efficiency
```python
# Pre-compute monthly returns matrix
returns_matrix = pivot(asset_returns, index='yearmonth', columns='asset_id')

# Vectorized portfolio calculations
portfolio_returns = (returns_matrix * weights_matrix).sum(axis=1)

# Rolling calculations using pandas
rolling_stats = returns_matrix.rolling(12).agg(['mean', 'std', 'skew'])
```

### Data Quality Checks
1. **Monotonic Dates**: Ensure chronological ordering
2. **Duplicate Detection**: One entry per asset-platform-month
3. **Outlier Detection**: Flag suspicious monthly changes (>50%)
4. **Completeness**: Track data coverage by asset and month

### Edge Cases
1. **New Assets**: First month has no return
2. **Exited Assets**: Handle assets that disappear
3. **Short History**: Gracefully degrade metrics requiring history
4. **Single Asset Months**: Handle concentration edge cases

This specification provides a comprehensive framework for analyzing monthly equity snapshots with appropriate metrics, forecasting methods, and data structures optimized for monthly frequency data.