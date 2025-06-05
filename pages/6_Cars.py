import streamlit as st
import pandas as pd
import plotly.express as px
from utils.car.car_data_manager import check_and_generate_car_data_file, load_car_data, populate_with_test_data, DATA_MODEL_GUIDE
from utils.car.car_metrics import get_all_car_metrics
from utils.car.car_forecasting import forecast_depreciation
from utils.visualizations import kpi_card

st.set_page_config(layout="wide")

# --- Page Setup and Data Loading ---
st.title("🚗 Car Equity Tracker")
CAR_DATA_FILE = "car_data.xlsx"
check_and_generate_car_data_file(CAR_DATA_FILE)
car_data = load_car_data(CAR_DATA_FILE)

# --- Helper Function for UI ---
def display_data_model_explanation():
    with st.expander("How to Edit Your Car Data", expanded=False):
        st.markdown("""
        This dashboard is powered by the `car_data.xlsx` file in the app's root directory. You can edit this file directly to manage your car data. 
        
        **Key Concepts:**
        - **Primary Key (PK)**: A unique identifier for a row in a sheet (e.g., `CarID` in the `Cars` sheet). It must be unique.
        - **Foreign Key (FK)**: A key used to link two sheets together (e.g., `CarID` in the `Expenses` sheet links back to a specific car in the `Cars` sheet).
        
        Below is a guide to the required structure for each sheet.
        """)
        for sheet_name, definition in DATA_MODEL_GUIDE.items():
            st.markdown(f"### `{sheet_name}` Sheet")
            st.markdown(definition['description'])
            
            # Create a DataFrame from the column definitions for display
            guide_df = pd.DataFrame(definition['columns'])
            guide_df['Key'] = guide_df.apply(
                lambda row: 'Primary Key' if row.get('pk') == True else ('Links to ' + str(row.get('fk')) if pd.notna(row.get('fk')) else ''),
                axis=1
            )
            # Reorder and rename for clarity
            display_df = guide_df[['name', 'type', 'definition', 'Key']].rename(columns={
                'name': 'Field Name',
                'type': 'Data Type',
                'definition': 'Definition'
            })
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)


# --- Main Page Logic ---
if car_data is None:
    st.error("There was an error loading the car data file. Please check the file format.")
    display_data_model_explanation()

elif car_data == "empty":
    st.info("Your car data file is empty. Add data to `car_data.xlsx` to get started, or use the button below to add sample data.")
    if st.button("Populate with Sample Data"):
        populate_with_test_data(CAR_DATA_FILE)
        st.rerun()
    display_data_model_explanation()

else:
    # --- Car Selection ---
    car_list = car_data["Cars"]["Make"] + " " + car_data["Cars"]["Model"]
    car_ids = car_data["Cars"]["CarID"]
    car_map = dict(zip(car_list, car_ids))

    selected_car_name = st.selectbox("Select a Car to View", options=car_list)
    selected_car_id = car_map[selected_car_name]
    
    # --- Metrics and KPIs ---
    metrics = get_all_car_metrics(car_data, selected_car_id)
    if metrics:
        st.header(f"Dashboard for {selected_car_name}")

        # --- Combined Finance Breakdown Section ---
        st.markdown("---")
        breakdown_cols = st.columns(2)

        with breakdown_cols[0]:
            st.subheader("Finance Agreement Details")
            finance_details = metrics.get('finance_details') or {}
            
            # Prepare data for the finance details table
            finance_table_data = {
                'Detail': [
                    'Purchase Price', 'Deposit Paid', 'Part Exchange Value', 'Amount Financed', '---',
                    'Finance Provider', 'Agreement Type', 'Start Date', 'End Date', '---',
                    'Interest Rate (APR)', 'Monthly Payment', 'Balloon Payment'
                ],
                'Value': [
                    f"£{metrics['details'].get('PurchasePrice', 0):,.2f}",
                    f"£{finance_details.get('DepositAmount', 0):,.2f}",
                    f"£{finance_details.get('PartExchangeValue', 0):,.2f}",
                    f"£{finance_details.get('AmountFinanced', 0):,.2f}",
                    '', # Separator
                    finance_details.get('Provider', 'N/A'),
                    finance_details.get('Type', 'N/A'),
                    finance_details.get('StartDate', pd.NaT).strftime('%Y-%m-%d') if pd.notna(finance_details.get('StartDate')) else 'N/A',
                    finance_details.get('EndDate', pd.NaT).strftime('%Y-%m-%d') if pd.notna(finance_details.get('EndDate')) else 'N/A',
                    '', # Separator
                    f"{finance_details.get('InterestRate_APR', 0):.2f}%",
                    f"£{finance_details.get('MonthlyPayment', 0):,.2f}",
                    f"£{finance_details.get('BalloonPayment', 0):,.2f}",
                ]
            }
            finance_df = pd.DataFrame(finance_table_data)

            st.dataframe(
                finance_df,
                use_container_width=True,
                hide_index=True
            )

        with breakdown_cols[1]:
            st.subheader("Live Financials Summary")
            
            total_contribution = metrics.get('total_contribution', 0)
            total_running_costs = metrics.get('total_costs', {}).get('total_cost', 0)
            grand_total_outlay = total_contribution + total_running_costs

            live_financials_data = {
                'Metric': [
                    'Total Purchase and Finance Contribution',
                    'Total Running Costs',
                    '---',
                    '**Grand Total Outlay**'
                ],
                'Value': [
                    f"£{total_contribution:,.2f}",
                    f"£{total_running_costs:,.2f}",
                    '',
                    f"**£{grand_total_outlay:,.2f}**"
                ]
            }
            live_financials_df = pd.DataFrame(live_financials_data)
            st.dataframe(live_financials_df, use_container_width=True, hide_index=True)

        # Key Dates Countdown Row
        st.markdown("---")
        key_date_cols = st.columns(len(metrics['key_dates']) or 1)
        if metrics['key_dates']:
            for i, key_date in enumerate(metrics['key_dates']):
                with key_date_cols[i]:
                    kpi_card(
                        f"{key_date['DateType']} Renewal",
                        f"{key_date['DaysRemaining']} days",
                        help_text=f"Expires on {key_date['ExpiryDate'].strftime('%Y-%m-%d')}"
                    )
        else:
            st.info("No key dates found. Add them to the 'KeyDates' sheet.")

        # --- Charts and Visualizations ---
        st.markdown("---")
        chart_cols = st.columns([2, 1])

        with chart_cols[0]:
            st.subheader("Depreciation Curve")
            
            # Historical valuations
            valuations_df = car_data['Valuations'][car_data['Valuations']['CarID'] == selected_car_id]
            
            # Forecasted valuations
            forecast_df = forecast_depreciation(car_data['Valuations'], selected_car_id, 12)
            
            if not valuations_df.empty:
                fig = px.line(valuations_df, x='Date', y='Value', title="Valuation Over Time", markers=True)
                if forecast_df is not None:
                    fig.add_scatter(x=forecast_df['Date'], y=forecast_df['ForecastValue'], mode='lines', name='Forecast', line=dict(dash='dash'))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Add valuations to the 'Valuations' sheet to see the depreciation curve.")

        with chart_cols[1]:
            st.subheader("Cost Breakdown")
            costs_by_cat = metrics['total_costs'].get('by_category')
            if costs_by_cat:
                fig = px.pie(
                    names=list(costs_by_cat.keys()), 
                    values=list(costs_by_cat.values()),
                    title="Running Costs by Category"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No expense data found.")

        # --- Cumulative Cost Chart ---
        st.markdown("---")
        st.subheader("Cumulative Outlay Over Time")
        cumulative_costs_df = metrics.get('cumulative_costs_df')
        
        if cumulative_costs_df is not None and not cumulative_costs_df.empty:
            df_melted = cumulative_costs_df.melt(
                id_vars='Date', 
                value_vars=['Total Purchase and Finance Contribution', 'Total Running Costs', 'Grand Total Outlay'],
                var_name='Cost Type', 
                value_name='Cumulative Amount'
            )
            
            fig = px.line(
                df_melted, 
                x='Date', 
                y='Cumulative Amount', 
                color='Cost Type',
                title="How Your Costs Have Accumulated Over Time",
                labels={'Cumulative Amount': 'Cumulative Amount (£)'}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Not enough data to display cumulative costs over time.")

        # --- PNL & Performance Section ---
        st.markdown("---")
        st.subheader("Performance & PNL Summary")
        pnl_metrics = metrics.get('pnl_metrics')
        if pnl_metrics:
            pnl_data = {
                'Metric': [
                    'Overall PNL (Paper)',
                    'Total Cost of Ownership',
                    'Depreciation To Date',
                    'Total Interest Paid',
                    'Cost Per Mile',
                    'Equity as % of Value'
                ],
                'Value': [
                    f"£{pnl_metrics.get('net_position', 0):,.2f}",
                    f"£{pnl_metrics.get('total_cost_of_ownership', 0):,.2f}",
                    f"£{pnl_metrics.get('depreciation', 0):,.2f}",
                    f"£{pnl_metrics.get('total_interest_paid', 0):,.2f}",
                    f"£{pnl_metrics.get('cost_per_mile', 0):,.2f}",
                    f"{pnl_metrics.get('equity_pct', 0):.2f}%"
                ]
            }
            pnl_df = pd.DataFrame(pnl_data)
            st.dataframe(pnl_df, use_container_width=True, hide_index=True)
            st.caption("Overall PNL = Current Equity - Total Contribution (Deposit + Part Ex + Payments)")
        else:
            st.info("Not enough data to calculate PNL metrics.")

    else:
        st.error("Could not retrieve metrics for the selected car.")

    # --- Data Model Explanation ---
    display_data_model_explanation() 