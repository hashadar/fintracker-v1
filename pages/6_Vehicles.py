"""Vehicle tracking dashboard for FinTracker application."""

import streamlit as st

from utils import (
    CURRENCY_FORMAT,
    calculate_vehicle_metrics,
    calculate_vehicle_summary_metrics,
    load_car_assets,
    load_car_expenses,
    load_car_payments,
)
from utils.design.cards import (
    complex_emphasis_card,
    simple_card,
)
from utils.design.components import (
    create_metric_grid,
    create_page_header,
    create_section_header,
)
from utils.design.tokens import (
    BRAND_PRIMARY,
)

# Page configuration
st.set_page_config(
    page_title="Vehicle Tracking - FinTracker",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Page header
create_page_header(
    title="Vehicle Tracking",
    description="Comprehensive tracking of vehicular assets, loans, and operating costs",
)

# Load car data
car_assets_df = load_car_assets()
car_payments_df = load_car_payments()
car_expenses_df = load_car_expenses()

# Check if data is available
if car_assets_df is None or car_assets_df.empty:
    st.warning(
        "No car assets data found. Please ensure your Google Sheets contains the 'Car Assets' worksheet."
    )
    st.stop()

# Calculate vehicle summary metrics
vehicle_summary = calculate_vehicle_summary_metrics(car_assets_df)

# --- Vehicle Summary Section ---
st.markdown("---")
create_section_header("Vehicle Summary", icon="🚗")

# Main vehicle portfolio card
complex_emphasis_card(
    title="TOTAL VEHICLE PORTFOLIO",
    metric=vehicle_summary["vehicle_names_display"],
    mom_change=f"{vehicle_summary['latest_mileage']:,.0f} latest mileage",
    caption="Vehicle portfolio",
    emphasis_color=BRAND_PRIMARY,
)

# Vehicle metrics cards using metric grid
create_metric_grid(
    [
        lambda: simple_card(
            "Total Car Value",
            CURRENCY_FORMAT.format(vehicle_summary["total_car_value"]),
            "Current market value",
        ),
        lambda: simple_card(
            "Total Equity",
            CURRENCY_FORMAT.format(vehicle_summary["total_equity"]),
            "Net vehicle value",
        ),
        lambda: simple_card(
            "Outstanding Loan Balance",
            CURRENCY_FORMAT.format(vehicle_summary["total_loan_balance"]),
            "Total debt remaining",
        ),
        lambda: simple_card(
            "YTD Mileage",
            f"{vehicle_summary['ytd_mileage']:,.0f} miles",
            "Year-to-date mileage",
        ),
    ],
    cols=4,
)

# --- Vehicle Analytics Section ---
st.markdown("---")

# Use the standardized vehicle analytics component
from utils.design.components import create_vehicle_analytics_charts

create_vehicle_analytics_charts(car_assets_df, car_expenses_df, car_payments_df)

# --- Vehicle Metrics Section ---
st.markdown("---")
create_section_header("Vehicle Metrics", icon="📊")

# Calculate vehicle metrics
vehicle_metrics = calculate_vehicle_metrics(
    car_assets_df, car_expenses_df, car_payments_df
)

# Create metric grid for vehicle metrics
create_metric_grid(
    [
        lambda: simple_card(
            "Latest Loan Payment",
            CURRENCY_FORMAT.format(vehicle_metrics["latest_loan_payment"]),
            "Most recent payment amount",
        ),
        lambda: simple_card(
            "Latest Monthly Expenses",
            CURRENCY_FORMAT.format(vehicle_metrics["latest_monthly_expenses"]),
            "Last month's operating costs",
        ),
        lambda: simple_card(
            "Latest Month Total",
            CURRENCY_FORMAT.format(vehicle_metrics["latest_month_combined_costs"]),
            "Combined loan + expenses",
        ),
        lambda: simple_card(
            "Cost per Mile",
            CURRENCY_FORMAT.format(vehicle_metrics["cost_per_mile"]),
            "YTD total cost per mile",
        ),
    ],
    cols=4,
)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.9em;'>
        Vehicle tracking data is loaded from Google Sheets. 
        Ensure your sheets contain the required worksheets: 'Car Assets', 'Car Payments', and 'Car Expenses'.
    </div>
    """,
    unsafe_allow_html=True,
)
