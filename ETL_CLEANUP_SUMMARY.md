# ETL Module Cleanup Summary

## Overview
The ETL module has been cleaned up to focus only on core data loading and transformation responsibilities, while moving data processing functions to the appropriate `data_processing.py` module.

## Changes Made

### Files Removed from ETL Module
- `utils/etl/monthly_metrics.py` - Moved functions to `data_processing.py`
- `utils/etl/asset_metrics.py` - Moved functions to `data_processing.py`  
- `utils/etl/risk_metrics.py` - Moved functions to `data_processing.py`
- `utils/etl/forecasting.py` - Removed (not currently used)
- `utils/etl/seasonal_analysis.py` - Removed (not currently used)

### Files Retained in ETL Module
- `utils/etl/data_loader.py` - Core Google Sheets data loading
- `utils/etl/asset_classifier.py` - Asset classification logic
- `utils/etl/__init__.py` - Updated exports

### Functions Moved to Data Processing
The following functions were moved from ETL to `utils/data_processing.py`:

#### Monthly Metrics Functions
- `calculate_monthly_metrics()` - Comprehensive monthly portfolio metrics
- `calculate_ytd_metrics()` - Year-to-Date metrics calculation
- `calculate_qtd_metrics()` - Quarter-to-Date metrics calculation

#### Risk Metrics Functions
- `sortino_ratio()` - Sortino ratio calculation
- `calculate_var()` - Value at Risk calculation
- `calculate_cvar()` - Conditional Value at Risk calculation
- `calculate_max_drawdown()` - Maximum drawdown calculation

#### Asset Type Metrics Functions
- `calculate_asset_type_metrics()` - Comprehensive metrics for specific asset types (Cash, Investments, Pensions)

### Updated Exports
- `utils/__init__.py` - Updated to export functions from their new locations
- `utils/etl/__init__.py` - Simplified to only export core ETL functions

## Current ETL Module Responsibilities

### Core ETL Functions (Remain in ETL)
1. **Data Loading** (`data_loader.py`)
   - `load_data()` - Load data from Google Sheets
   - `filter_data_by_date_range()` - Filter by date range
   - `get_month_range()` - Get available date range

2. **Data Transformation** (`asset_classifier.py`)
   - `classify_asset_types()` - Classify assets into types
   - `get_asset_classification_rules()` - Get classification rules

### Data Processing Functions (Moved to data_processing.py)
1. **Basic Data Operations**
   - Filtering by asset type
   - Getting latest month data
   - Time period data extraction
   - Percentage change calculations

2. **Aggregation and Metrics**
   - Monthly aggregation
   - Rolling metrics calculation
   - Performance metrics
   - Drawdown calculations

3. **Advanced Analytics**
   - Monthly metrics with returns, volatility, Sharpe ratio
   - YTD and QTD metrics
   - Risk metrics (VaR, CVaR, Sortino ratio)
   - Asset type specific metrics

## Benefits of This Cleanup

1. **Clear Separation of Concerns**
   - ETL focuses on data loading and basic transformation
   - Data processing handles analytics and metrics

2. **Reduced Duplication**
   - Eliminated duplicate functionality between modules
   - Consolidated similar functions in one location

3. **Improved Maintainability**
   - Easier to find and modify data processing functions
   - Clearer module boundaries

4. **Better Organization**
   - Functions are grouped by their logical purpose
   - Easier to understand what each module does

## Usage
All functions are still available through the main `utils` import:

```python
from utils import (
    # ETL functions
    load_data, classify_asset_types,
    
    # Data processing functions
    calculate_monthly_metrics, sortino_ratio, calculate_var,
    calculate_asset_type_metrics
)
```

The cleanup maintains backward compatibility while providing a cleaner, more organized codebase.

## Fixes Applied
- **Missing Function**: Added `calculate_asset_type_metrics()` to `data_processing.py` and exported it from `utils/__init__.py`
- **Import Errors**: Resolved all import errors by ensuring all required functions are properly exported 