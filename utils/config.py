"""
Configuration constants for the FinTracker application.

This module contains application behavior and business logic constants,
separate from visual design tokens which are in tokens.py.
"""

# Asset Types and Classifications
ASSET_TYPES = {
    "CASH": "Cash",
    "INVESTMENTS": "Investments",
    "PENSIONS": "Pensions",
    "PROPERTY": "Property",
    "VEHICLES": "Vehicles",
    "OTHER": "Other",
}

# Date and Currency Formats
DATE_FORMAT = "%Y-%m-%d"
DISPLAY_DATE_FORMAT = "%B %Y"
SHORT_DATE_FORMAT = "%b %Y"
CURRENCY_FORMAT = "£{:,.2f}"
CURRENCY_SYMBOL = "£"
PERCENTAGE_FORMAT = "{:.1f}%"

# Business Logic Constants
RISK_FREE_RATE = 0.05  # 5% annual risk-free rate
DEFAULT_FORECAST_PERIODS = 12  # months
DEFAULT_ROLLING_WINDOW = 12  # months for rolling averages


# Page Layout Constants
PAGE_TITLE = "FinTracker - Personal Finance Dashboard"
PAGE_ICON = "💰"
LAYOUT = "wide"
INITIAL_SIDEBAR_STATE = "expanded"

# Data Processing Constants
MIN_DATA_POINTS_FOR_FORECAST = 6
SEASONAL_PERIODS = 12  # monthly seasonality
CONFIDENCE_LEVEL = 0.95

# ==============================================================================
# DATA SOURCE CONFIGURATIONS
# ==============================================================================

BALANCE_SHEET_CONFIG = {
    "sheet_name": "Balance Sheet",
    "required_columns": ["Platform", "Asset", "Value", "Timestamp"],
    "optional_columns": ["Token Amount"],
    "currency_columns": ["Value"],
    "numeric_columns": ["Token Amount"],
    "date_columns": ["Timestamp"],
}

PENSION_CASHFLOWS_CONFIG = {
    "sheet_name": "Pension Cashflows",
    "required_columns": ["Platform", "Asset", "Value", "Timestamp", "Cashflow Type"],
    "optional_columns": ["Description", "Notes"],
    "currency_columns": ["Value"],
    "numeric_columns": [],
    "date_columns": ["Timestamp"],
}

CAR_ASSETS_CONFIG = {
    "sheet_name": "Car Assets",
    "required_columns": [
        "Timestamp",
        "Platform",
        "Asset",
        "Loan_Status",
        "Loan_Balance",
        "Car_Value",
        "Mileage",
    ],
    "optional_columns": ["Notes"],
    "currency_columns": ["Loan_Balance", "Car_Value"],
    "numeric_columns": ["Mileage"],
    "date_columns": ["Timestamp"],
}

CAR_PAYMENTS_CONFIG = {
    "sheet_name": "Car Payments",
    "required_columns": [
        "Timestamp",
        "Platform",
        "Asset",
        "Payment_Amount",
        "Payment_Type",
    ],
    "optional_columns": ["Notes"],
    "currency_columns": ["Payment_Amount"],
    "numeric_columns": [],
    "date_columns": ["Timestamp"],
}

CAR_EXPENSES_CONFIG = {
    "sheet_name": "Car Expenses",
    "required_columns": [
        "Timestamp",
        "Asset",
        "Expense_Type",
        "Amount",
        "Platform/Provider",
    ],
    "optional_columns": ["Notes"],
    "currency_columns": ["Amount"],
    "numeric_columns": [],
    "date_columns": ["Timestamp"],
}


# ==============================================================================
# DATA VALIDATION AND CLASSIFICATION MAPPINGS
# ==============================================================================

PLATFORM_TO_ASSET_TYPE = {
    "IBKR": "Investments",
    "HSBC": "Cash",
    "Wise": "Cash",
    "Coinbase": "Investments",
    "Wahed": "Pensions",
    "Standard Life": "Pensions",
    "MotoNovo": "Vehicles",
    "Owned": "Vehicles",
}

ASSET_TO_ASSET_TYPE = {
    "ON BNS SAVER": "Cash",
    "BTC": "Investments",
    "ETH": "Investments",
    "SOL": "Investments",
    "Wahed SIPP": "Pensions",
    "SL Pension": "Pensions",
    "IBKR Total Portfolio": "Investments",
    "Wise Savings": "Cash",
    "Porsche Taycan 4S": "Vehicles",
}

BALANCE_SHEET_VALID_VALUES = {
    "Platform": ["IBKR", "HSBC", "Wise", "Coinbase", "Wahed", "Standard Life"],
    "Asset": [
        "ON BNS SAVER",
        "BTC",
        "ETH",
        "SOL",
        "Wahed SIPP",
        "SL Pension",
        "IBKR Total Portfolio",
        "Wise Savings",
    ],
}

PENSION_CASHFLOWS_VALID_VALUES = {
    "Platform": ["Wahed", "Standard Life"],
    "Asset": ["Wahed SIPP", "SL Pension"],
}

CAR_ASSETS_VALID_VALUES = {
    "Platform": ["MotoNovo", "Owned"],
    "Asset": ["Porsche Taycan 4S"],
    "Loan_Status": ["Financed", "Owned"],
}

CAR_PAYMENTS_VALID_VALUES = {
    "Platform": ["MotoNovo"],
    "Asset": ["Porsche Taycan 4S"],
    "Payment_Type": ["Monthly Payment"],
}

CAR_EXPENSES_VALID_VALUES = {
    "Asset": ["Porsche Taycan 4S"],
    "Expense_Type": [
        "Insurance",
        "Road Tax",
        "Parking",
        "Maintenance",
        "Fuel_Charging",
        "Cleaning",
    ],
}

# Car loan status options
CAR_LOAN_STATUSES = {"FINANCED": "Financed", "OWNED": "Owned"}

# Cashflow Types
CASHFLOW_TYPES = {"CONTRIBUTION": "Contribution", "FEE": "Fee", "TRANSFER": "Transfer"}

# Risk Metrics Configuration
VOLATILITY_WINDOW = 12  # months for volatility calculation
VAR_CONFIDENCE_LEVEL = 0.95
MAX_DRAWDOWN_WINDOW = 12  # months for max drawdown calculation

# Performance Metrics
BENCHMARK_RETURN = 0.08  # 8% annual benchmark return
INFLATION_RATE = 0.025  # 2.5% annual inflation rate

# Car tracking constants
DEFAULT_CAR_FORECAST_PERIODS = 12  # months
CAR_DEPRECIATION_RATE = 0.15  # 15% annual depreciation
CAR_MAINTENANCE_FREQUENCY = 12  # months between services


def validate_config():
    """
    Validate configuration constants to ensure they are properly defined and have valid values.

    Returns:
        dict: Validation results with 'valid' boolean and 'errors' list
    """
    from datetime import datetime

    errors = []
    warnings = []

    # Validate asset types
    if not isinstance(ASSET_TYPES, dict) or not ASSET_TYPES:
        errors.append("ASSET_TYPES must be a non-empty dictionary")
    else:
        for key, value in ASSET_TYPES.items():
            if not isinstance(value, str) or not value.strip():
                errors.append(f"ASSET_TYPES['{key}'] must be a non-empty string")

    # Validate date formats
    date_formats = [DATE_FORMAT, DISPLAY_DATE_FORMAT, SHORT_DATE_FORMAT]
    test_date = datetime.now()
    for format_name, date_format in [
        ("DATE_FORMAT", DATE_FORMAT),
        ("DISPLAY_DATE_FORMAT", DISPLAY_DATE_FORMAT),
        ("SHORT_DATE_FORMAT", SHORT_DATE_FORMAT),
    ]:
        try:
            test_date.strftime(date_format)
        except ValueError:
            errors.append(f"{format_name} '{date_format}' is not a valid date format")

    # Validate currency format
    try:
        CURRENCY_FORMAT.format(1234.56)
    except (ValueError, TypeError):
        errors.append(
            f"CURRENCY_FORMAT '{CURRENCY_FORMAT}' is not a valid format string"
        )

    # Validate percentage format
    try:
        PERCENTAGE_FORMAT.format(12.34)
    except (ValueError, TypeError):
        errors.append(
            f"PERCENTAGE_FORMAT '{PERCENTAGE_FORMAT}' is not a valid format string"
        )

    # Validate business logic constants
    if not isinstance(RISK_FREE_RATE, (int, float)) or RISK_FREE_RATE < 0:
        errors.append("RISK_FREE_RATE must be a non-negative number")

    if not isinstance(DEFAULT_FORECAST_PERIODS, int) or DEFAULT_FORECAST_PERIODS <= 0:
        errors.append("DEFAULT_FORECAST_PERIODS must be a positive integer")

    if not isinstance(DEFAULT_ROLLING_WINDOW, int) or DEFAULT_ROLLING_WINDOW <= 0:
        errors.append("DEFAULT_ROLLING_WINDOW must be a positive integer")

    if (
        not isinstance(MIN_DATA_POINTS_FOR_FORECAST, int)
        or MIN_DATA_POINTS_FOR_FORECAST <= 0
    ):
        errors.append("MIN_DATA_POINTS_FOR_FORECAST must be a positive integer")

    if not isinstance(SEASONAL_PERIODS, int) or SEASONAL_PERIODS <= 0:
        errors.append("SEASONAL_PERIODS must be a positive integer")

    if not isinstance(CONFIDENCE_LEVEL, (int, float)) or not (0 < CONFIDENCE_LEVEL < 1):
        errors.append("CONFIDENCE_LEVEL must be between 0 and 1")

    if not isinstance(VAR_CONFIDENCE_LEVEL, (int, float)) or not (
        0 < VAR_CONFIDENCE_LEVEL < 1
    ):
        errors.append("VAR_CONFIDENCE_LEVEL must be between 0 and 1")

    if not isinstance(VOLATILITY_WINDOW, int) or VOLATILITY_WINDOW <= 0:
        errors.append("VOLATILITY_WINDOW must be a positive integer")

    if not isinstance(MAX_DRAWDOWN_WINDOW, int) or MAX_DRAWDOWN_WINDOW <= 0:
        errors.append("MAX_DRAWDOWN_WINDOW must be a positive integer")

    if not isinstance(BENCHMARK_RETURN, (int, float)):
        errors.append("BENCHMARK_RETURN must be a number")

    if not isinstance(INFLATION_RATE, (int, float)) or INFLATION_RATE < 0:
        errors.append("INFLATION_RATE must be a non-negative number")

    # Validate string constants
    string_constants = {
        "PAGE_TITLE": PAGE_TITLE,
        "PAGE_ICON": PAGE_ICON,
        "LAYOUT": LAYOUT,
        "INITIAL_SIDEBAR_STATE": INITIAL_SIDEBAR_STATE,
    }

    for name, value in string_constants.items():
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{name} must be a non-empty string")

    # Validate layout constants
    if LAYOUT not in ["wide", "centered"]:
        warnings.append(f"LAYOUT '{LAYOUT}' is not a standard Streamlit layout value")

    if INITIAL_SIDEBAR_STATE not in ["expanded", "collapsed", "auto"]:
        warnings.append(
            f"INITIAL_SIDEBAR_STATE '{INITIAL_SIDEBAR_STATE}' is not a standard Streamlit value"
        )

    # Check for potential issues
    if DEFAULT_ROLLING_WINDOW > DEFAULT_FORECAST_PERIODS:
        warnings.append(
            "DEFAULT_ROLLING_WINDOW is larger than DEFAULT_FORECAST_PERIODS"
        )

    if MIN_DATA_POINTS_FOR_FORECAST > DEFAULT_ROLLING_WINDOW:
        warnings.append(
            "MIN_DATA_POINTS_FOR_FORECAST is larger than DEFAULT_ROLLING_WINDOW"
        )

    return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}
