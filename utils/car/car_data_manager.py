import pandas as pd
import os
import streamlit as st
from datetime import datetime

# A detailed, user-facing guide to the data model. This is the single source of truth.
DATA_MODEL_GUIDE = {
    "Cars": {
        "description": "Stores the master record for each vehicle.",
        "columns": [
            {"name": "CarID", "type": "Integer", "definition": "Primary Key. A unique ID for each car.", "pk": True},
            {"name": "Make", "type": "Text", "definition": "The manufacturer of the car."},
            {"name": "Model", "type": "Text", "definition": "The specific model of the car."},
            {"name": "Year", "type": "Integer", "definition": "The registration year of the car."},
            {"name": "VIN", "type": "Text", "definition": "Vehicle Identification Number (optional)."},
            {"name": "PurchaseDate", "type": "Date (YYYY-MM-DD)", "definition": "The date the car was acquired."},
            {"name": "PurchasePrice", "type": "Number", "definition": "The total cost to acquire the car."},
            {"name": "InitialMileage", "type": "Integer", "definition": "The car's mileage at the time of purchase."}
        ]
    },
    "FinanceAgreements": {
        "description": "Tracks finance details. Assumes one primary finance agreement per car for simplicity.",
        "columns": [
            {"name": "FinanceID", "type": "Integer", "definition": "Primary Key. A unique ID for the agreement.", "pk": True},
            {"name": "CarID", "type": "Integer", "definition": "Foreign Key linking to the 'Cars' sheet.", "fk": "Cars.CarID"},
            {"name": "Provider", "type": "Text", "definition": "The name of the finance company."},
            {"name": "Type", "type": "Text", "definition": "The type of finance (e.g., PCP, HP, Loan)."},
            {"name": "StartDate", "type": "Date (YYYY-MM-DD)", "definition": "The start date of the agreement."},
            {"name": "EndDate", "type": "Date (YYYY-MM-DD)", "definition": "The end date of the agreement."},
            {"name": "AmountFinanced", "type": "Number", "definition": "The total loan amount, including any fees rolled in."},
            {"name": "InterestRate_APR", "type": "Number", "definition": "The Annual Percentage Rate of the agreement (e.g., 5.9)."},
            {"name": "DepositAmount", "type": "Number", "definition": "The cash deposit paid by the user towards the purchase."},
            {"name": "PartExchangeValue", "type": "Number", "definition": "The value of any vehicle traded in as part of the deal."},
            {"name": "MonthlyPayment", "type": "Number", "definition": "The fixed monthly payment amount."},
            {"name": "BalloonPayment", "type": "Number", "definition": "The final optional balloon payment (for PCP/Lease)."}
        ]
    },
    "Valuations": {
        "description": "Logs the car's market value over time to track depreciation.",
        "columns": [
            {"name": "ValuationID", "type": "Integer", "definition": "Primary Key. A unique ID for the valuation.", "pk": True},
            {"name": "CarID", "type": "Integer", "definition": "Foreign Key linking to the 'Cars' sheet.", "fk": "Cars.CarID"},
            {"name": "Date", "type": "Date (YYYY-MM-DD)", "definition": "The date the valuation was recorded."},
            {"name": "Value", "type": "Number", "definition": "The market value of the car on the given date."},
            {"name": "Mileage", "type": "Integer", "definition": "The car's mileage when it was valued."},
            {"name": "Source", "type": "Text", "definition": "Where the valuation came from (e.g., AutoTrader)."}
        ]
    },
    "Expenses": {
        "description": "A log for all running costs to calculate the total cost of ownership.",
        "columns": [
            {"name": "ExpenseID", "type": "Integer", "definition": "Primary Key. A unique ID for the expense.", "pk": True},
            {"name": "CarID", "type": "Integer", "definition": "Foreign Key linking to the 'Cars' sheet.", "fk": "Cars.CarID"},
            {"name": "Date", "type": "Date (YYYY-MM-DD)", "definition": "The date the expense was incurred."},
            {"name": "Category", "type": "Text", "definition": "Type of expense (e.g., Maintenance, Fuel, Tax)."},
            {"name": "Description", "type": "Text", "definition": "A brief description of the expense."},
            {"name": "Cost", "type": "Number", "definition": "The monetary value of the expense."},
            {"name": "Mileage", "type": "Integer", "definition": "The car's mileage at the time of the expense."}
        ]
    },
    "FinancePayments": {
        "description": "A record of every payment made. Separated from expenses for clear finance tracking.",
        "columns": [
            {"name": "PaymentID", "type": "Integer", "definition": "Primary Key. A unique ID for the payment.", "pk": True},
            {"name": "FinanceID", "type": "Integer", "definition": "Foreign Key linking to 'FinanceAgreements'.", "fk": "FinanceAgreements.FinanceID"},
            {"name": "PaymentDate", "type": "Date (YYYY-MM-DD)", "definition": "The date the payment was made."},
            {"name": "Amount", "type": "Number", "definition": "The amount paid."}
        ]
    },
    "KeyDates": {
        "description": "Stores important recurring dates for countdowns on the dashboard.",
        "columns": [
            {"name": "KeyDateID", "type": "Integer", "definition": "Primary Key. A unique ID for the key date.", "pk": True},
            {"name": "CarID", "type": "Integer", "definition": "Foreign Key linking to the 'Cars' sheet.", "fk": "Cars.CarID"},
            {"name": "DateType", "type": "Text", "definition": "The type of event (e.g., MOT, Insurance, Tax)."},
            {"name": "ExpiryDate", "type": "Date (YYYY-MM-DD)", "definition": "The date the event or policy expires."},
            {"name": "Notes", "type": "Text", "definition": "Optional notes (e.g., Policy Number)."}
        ]
    },
}

# --- Internal definitions derived from the guide ---
SHEET_DEFINITIONS = {
    sheet: {
        "columns": [col["name"] for col in details["columns"]],
        "dtypes": {
            col["name"]: int for col in details["columns"] if col["type"] == "Integer"
        }
    } for sheet, details in DATA_MODEL_GUIDE.items()
}
# Add float/number and date types
for sheet, details in DATA_MODEL_GUIDE.items():
    SHEET_DEFINITIONS[sheet]["dtypes"].update({
        col["name"]: float for col in details["columns"] if col["type"] == "Number"
    })

DATE_COLUMNS = [
    col["name"] for details in DATA_MODEL_GUIDE.values() 
    for col in details["columns"] if "Date" in col["type"]
]

def create_car_data_template(file_path):
    """Creates a blank car_data.xlsx file with the required sheets and headers."""
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        for sheet_name, definition in SHEET_DEFINITIONS.items():
            pd.DataFrame(columns=definition["columns"]).to_excel(writer, sheet_name=sheet_name, index=False)
    st.success(f"Car data template created at {file_path}")

def check_and_generate_car_data_file(file_path="data/car_data.xlsx"):
    """Checks if the car data Excel file exists. If not, it generates a new template."""
    if not os.path.exists(file_path):
        create_car_data_template(file_path)

@st.cache_data
def load_car_data(file_path="data/car_data.xlsx"):
    """
    Loads car data from the specified Excel file, performs validation, and converts types.
    Returns a dictionary of DataFrames, one for each sheet.
    """
    if not os.path.exists(file_path):
        return None  # No file exists

    try:
        xls = pd.ExcelFile(file_path)
        data = {}
        is_empty = True

        # Initial validation: Check if all expected sheets are present
        for sheet_name in SHEET_DEFINITIONS.keys():
            if sheet_name not in xls.sheet_names:
                st.error(f"Validation Error: Sheet '{sheet_name}' is missing from {file_path}.")
                return None

        for sheet_name, definition in SHEET_DEFINITIONS.items():
            df = pd.read_excel(xls, sheet_name=sheet_name)

            # Validate columns
            if not all(col in df.columns for col in definition["columns"]):
                st.error(f"Validation Error: Sheet '{sheet_name}' is missing required columns.")
                return None
            
            if not df.empty:
                is_empty = False

            # Convert data types
            for col, dtype in definition["dtypes"].items():
                if col in df.columns:
                    df[col] = df[col].astype(dtype, errors='ignore')
            
            # Convert date columns
            for col in DATE_COLUMNS:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors='coerce')

            data[sheet_name] = df
        
        if is_empty:
            return "empty"

        return data

    except Exception as e:
        st.error(f"An error occurred while loading or validating the car data file: {e}")
        return None

def populate_with_test_data(file_path="data/car_data.xlsx"):
    """Overwrites the existing Excel file with sample test data."""
    today = datetime.now()
    test_data = {
        "Cars": pd.DataFrame([{
            "CarID": 1, "Make": "Honda", "Model": "Civic", "Year": 2022, "VIN": "ABC123XYZ",
            "PurchaseDate": datetime(2022, 1, 15), "PurchasePrice": 25000, "InitialMileage": 100
        }]),
        "FinanceAgreements": pd.DataFrame([{
            "FinanceID": 101, "CarID": 1, "Provider": "Honda Finance", "Type": "PCP",
            "StartDate": datetime(2022, 1, 15), "EndDate": datetime(2025, 1, 15),
            "AmountFinanced": 20000, "InterestRate_APR": 5.9, "DepositAmount": 4000,
            "PartExchangeValue": 1000, "MonthlyPayment": 350, "BalloonPayment": 8000
        }]),
        "Valuations": pd.DataFrame([
            {"ValuationID": 201, "CarID": 1, "Date": datetime(2023, 1, 15), "Value": 22000, "Mileage": 10000, "Source": "AutoTrader"},
            {"ValuationID": 202, "CarID": 1, "Date": datetime(2024, 1, 15), "Value": 19500, "Mileage": 20000, "Source": "Dealer"}
        ]),
        "Expenses": pd.DataFrame([
            {"ExpenseID": 301, "CarID": 1, "Date": datetime(2022, 3, 20), "Category": "Maintenance", "Description": "First Service", "Cost": 150, "Mileage": 5000},
            {"ExpenseID": 302, "CarID": 1, "Date": datetime(2022, 4, 1), "Category": "Insurance", "Description": "Annual Premium", "Cost": 600, "Mileage": 5500},
            {"ExpenseID": 303, "CarID": 1, "Date": datetime(2023, 4, 1), "Category": "Insurance", "Description": "Annual Premium", "Cost": 650, "Mileage": 15500},
            {"ExpenseID": 304, "CarID": 1, "Date": datetime(2024, 1, 5), "Category": "Fuel", "Description": "50L", "Cost": 75, "Mileage": 19800},
        ]),
        "FinancePayments": pd.DataFrame([
            {"PaymentID": 401, "FinanceID": 101, "PaymentDate": datetime(2022, 2, 15), "Amount": 350},
            {"PaymentID": 402, "FinanceID": 101, "PaymentDate": datetime(2022, 3, 15), "Amount": 350}
        ]),
        "KeyDates": pd.DataFrame([
            {"KeyDateID": 501, "CarID": 1, "DateType": "MOT", "ExpiryDate": today + pd.DateOffset(years=1), "Notes": "Due with service"},
            {"KeyDateID": 502, "CarID": 1, "DateType": "Insurance", "ExpiryDate": today + pd.DateOffset(years=2), "Notes": "Policy #XYZ"}
        ])
    }
    
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        for sheet_name, df in test_data.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    st.success("Test data has been populated successfully!")
    # Clear cache after populating
    st.cache_data.clear() 