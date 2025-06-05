# Car Utility Modules

This directory contains utility modules specifically designed for the **Car Equity Tracker** feature. These modules handle all the backend logic, from data management to financial calculations and forecasting.

## Modules

### `car_data_manager.py`
This module is the data backbone of the car tracker. It manages the `car_data.xlsx` file.

- **File Generation**: If `car_data.xlsx` does not exist, it automatically creates a new file with the correct sheets (`Cars`, `FinanceAgreements`, `Valuations`, `Expenses`, `FinancePayments`, `KeyDates`) and headers.
- **Data Loading**: It loads all sheets from the Excel file into a dictionary of Pandas DataFrames.
- **Schema Validation**: Upon loading, it validates the data against a predefined schema to ensure data integrity (correct data types, non-null columns, etc.).
- **Sample Data**: It includes a function to populate the Excel file with sample data for demonstration and testing purposes.

### `car_metrics.py`
This module centralizes all financial calculations and metric computations for the vehicles. It takes the raw data from the `car_data_manager` and transforms it into meaningful insights.

- **Equity Calculation**: Calculates the current equity of a vehicle (`Latest Valuation - Outstanding Finance`).
- **Cost Analysis**: Computes various cost metrics, including:
    - Total Contribution (Deposit + Part-Exchange + Finance Payments).
    - Total Running Costs (Sum of all expenses).
    - Total Cost of Ownership (Contribution + Running Costs).
- **PNL Calculation**: Determines the "paper" profit or loss (`Current Equity - Total Contribution`).
- **Date Calculations**: Calculates key countdowns, such as time to finance agreement renewal.
- **Data Aggregation**: Provides functions to create summary tables and time-series data for charting.

### `car_forecasting.py`
This module provides predictive analytics for the car tracker.

- **Depreciation Forecasting**: Uses historical valuation data to forecast future vehicle depreciation.
- **Cost Forecasting**: Analyzes historical expenses to predict future running costs.

## Data Flow

1.  The `pages/6_Cars.py` dashboard first calls `car_data_manager.load_car_data()` to get the vehicle data. This step also handles the initial creation and validation of the `car_data.xlsx` file.
2.  The loaded DataFrames are then passed to functions in `car_metrics.py` to compute all the necessary financial metrics for the selected car.
3.  The historical data is passed to `car_forecasting.py` to generate future predictions for depreciation and costs.
4.  The results from `car_metrics.py` and `car_forecasting.py` are then used by the dashboard to display tables, KPIs, and charts. 