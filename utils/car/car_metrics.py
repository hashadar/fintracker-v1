import pandas as pd
from datetime import datetime

def get_latest_valuation(valuations_df, car_id):
    """Retrieves the most recent valuation for a specific car."""
    car_valuations = valuations_df[valuations_df['CarID'] == car_id].copy()
    if car_valuations.empty:
        return None
    car_valuations['Date'] = pd.to_datetime(car_valuations['Date'])
    return car_valuations.sort_values(by='Date', ascending=False).iloc[0]

def calculate_outstanding_finance(finance_agreement, payments_df):
    """Calculates the outstanding balance on a finance agreement."""
    if finance_agreement is None or finance_agreement.empty:
        return 0
        
    agreement = finance_agreement.iloc[0]
    total_paid = payments_df[payments_df['FinanceID'] == agreement['FinanceID']]['Amount'].sum()
    
    # Simple model: Amount Financed - Total Paid.
    # A more complex model could account for interest.
    outstanding = agreement['AmountFinanced'] - total_paid
    return max(outstanding, 0) # Cannot be negative

def calculate_total_costs(expenses_df, car_id):
    """Calculates the total cost of ownership from the expenses log."""
    car_expenses = expenses_df[expenses_df['CarID'] == car_id]
    if car_expenses.empty:
        return {}
    
    total_cost = car_expenses['Cost'].sum()
    cost_by_category = car_expenses.groupby('Category')['Cost'].sum().to_dict()
    
    return {
        "total_cost": total_cost,
        "by_category": cost_by_category
    }

def calculate_total_contribution(finance_agreement, payments_df):
    """Calculates the user's total contribution: Deposit + Part Exchange + Payments."""
    if finance_agreement is None:
        return 0
    
    deposit = finance_agreement.get('DepositAmount', 0)
    part_exchange = finance_agreement.get('PartExchangeValue', 0)
    
    finance_id = finance_agreement.get('FinanceID')
    total_payments = payments_df[payments_df['FinanceID'] == finance_id]['Amount'].sum()
    
    return deposit + part_exchange + total_payments

def get_key_dates(key_dates_df, car_id):
    """Gets all key dates for a specific car and calculates days remaining."""
    car_key_dates = key_dates_df[key_dates_df['CarID'] == car_id].copy()
    if car_key_dates.empty:
        return []
    
    car_key_dates['DaysRemaining'] = (car_key_dates['ExpiryDate'] - datetime.now()).dt.days
    return car_key_dates.to_dict('records')

def get_car_details(cars_df, car_id):
    """Retrieves the master details for a specific car."""
    details = cars_df[cars_df['CarID'] == car_id]
    if details.empty:
        return None
    return details.iloc[0]

def get_finance_agreement(finance_df, car_id):
    """Retrieves the finance agreement for a specific car."""
    agreement = finance_df[finance_df['CarID'] == car_id]
    if agreement.empty:
        return None
    # Return as a dictionary for easier access
    return agreement.iloc[0].to_dict()

def get_all_car_metrics(data, car_id):
    """A master function to consolidate all metrics for a given car."""
    if data is None or car_id is None:
        return None

    # --- Filter DataFrames for the selected car ---
    car_details_series = get_car_details(data['Cars'], car_id)
    if car_details_series is None:
        return {"error": "Car ID not found."}
    car_details = car_details_series.to_dict()

    finance_agreement = get_finance_agreement(data['FinanceAgreements'], car_id)
    
    car_payments = data['FinancePayments'][data['FinancePayments']['FinanceID'] == finance_agreement['FinanceID']] if finance_agreement else pd.DataFrame(columns=['Amount'])
    car_expenses = data['Expenses'][data['Expenses']['CarID'] == car_id]
    car_valuations = data['Valuations'][data['Valuations']['CarID'] == car_id]
    car_key_dates = data['KeyDates'][data['KeyDates']['CarID'] == car_id]

    # --- Core Calculations ---
    latest_valuation_series = get_latest_valuation(car_valuations, car_id)
    latest_valuation = latest_valuation_series['Value'] if latest_valuation_series is not None else 0
    latest_mileage = latest_valuation_series['Mileage'] if latest_valuation_series is not None else car_details.get('InitialMileage', 0)

    outstanding_finance = calculate_outstanding_finance(pd.DataFrame([finance_agreement] if finance_agreement else []), car_payments)
    equity = latest_valuation - outstanding_finance
    
    total_costs_dict = calculate_total_costs(car_expenses, car_id)
    total_contribution = calculate_total_contribution(finance_agreement, car_payments)
    
    key_dates = get_key_dates(car_key_dates, car_id)

    # --- PNL Calculations ---
    pnl_metrics = {}
    purchase_price = car_details.get('PurchasePrice', 0)
    initial_mileage = car_details.get('InitialMileage', 0)
    
    # Depreciation
    pnl_metrics['depreciation'] = purchase_price - latest_valuation if latest_valuation > 0 else 0
    
    # Interest Paid (Simplified Model)
    amount_financed = finance_agreement.get('AmountFinanced', 0) if finance_agreement else 0
    total_payments_sum = car_payments['Amount'].sum()
    principal_paid = amount_financed - outstanding_finance
    pnl_metrics['total_interest_paid'] = total_payments_sum - principal_paid if total_payments_sum > principal_paid else 0

    # Total Cost of Ownership - revised to be the total cash outlay
    pnl_metrics['total_cost_of_ownership'] = total_contribution + total_costs_dict.get('total_cost', 0)

    # Net Position (PNL) - defined as Equity vs. Total Contribution
    pnl_metrics['net_position'] = equity - total_contribution
    
    # Cost per mile
    miles_driven = latest_mileage - initial_mileage
    pnl_metrics['cost_per_mile'] = pnl_metrics['total_cost_of_ownership'] / miles_driven if miles_driven > 0 else 0
    
    # Equity %
    pnl_metrics['equity_pct'] = (equity / latest_valuation) * 100 if latest_valuation > 0 else 0

    # --- Cumulative Costs for Charting ---
    cumulative_costs_df = calculate_cumulative_costs_over_time(
        finance_agreement, car_payments, car_expenses, car_id
    )

    return {
        "details": car_details,
        "finance_details": finance_agreement,
        "latest_valuation": latest_valuation,
        "outstanding_finance": outstanding_finance,
        "equity": equity,
        "total_costs": total_costs_dict,
        "total_contribution": total_contribution,
        "key_dates": key_dates,
        "pnl_metrics": pnl_metrics,
        "cumulative_costs_df": cumulative_costs_df
    }

def calculate_cumulative_costs_over_time(finance_agreement, payments_df, expenses_df, car_id):
    """Calculates the cumulative contributions and running costs over time."""
    
    # Get purchase contributions
    contributions = []
    if finance_agreement:
        purchase_date = finance_agreement.get('StartDate')
        if pd.notna(purchase_date):
            if finance_agreement.get('DepositAmount', 0) > 0:
                contributions.append({'Date': purchase_date, 'Type': 'Contribution', 'Amount': finance_agreement['DepositAmount']})
            if finance_agreement.get('PartExchangeValue', 0) > 0:
                contributions.append({'Date': purchase_date, 'Type': 'Contribution', 'Amount': finance_agreement['PartExchangeValue']})

    # Get finance payments
    finance_payments = payments_df[['PaymentDate', 'Amount']].copy()
    finance_payments.rename(columns={'PaymentDate': 'Date'}, inplace=True)
    finance_payments['Type'] = 'Contribution'

    # Get running costs
    running_costs = expenses_df[expenses_df['CarID'] == car_id][['Date', 'Cost']].copy()
    running_costs.rename(columns={'Cost': 'Amount'}, inplace=True)
    running_costs['Type'] = 'Running Cost'
    
    # Combine all transactions
    all_transactions = pd.concat([
        pd.DataFrame(contributions),
        finance_payments,
        running_costs
    ], ignore_index=True)
    
    if all_transactions.empty:
        return pd.DataFrame(columns=['Date', 'Total Purchase and Finance Contribution', 'Total Running Costs', 'Grand Total Outlay'])
        
    all_transactions['Date'] = pd.to_datetime(all_transactions['Date'])
    all_transactions = all_transactions.sort_values('Date')
    
    # Calculate cumulative sums
    all_transactions['Total Purchase and Finance Contribution'] = all_transactions[all_transactions['Type'] == 'Contribution']['Amount'].cumsum()
    all_transactions['Total Running Costs'] = all_transactions[all_transactions['Type'] == 'Running Cost']['Amount'].cumsum()
    
    # Forward fill to carry the cumulative values forward
    all_transactions.fillna(method='ffill', inplace=True)
    all_transactions.fillna(0, inplace=True) # Fill any initial NaNs with 0
    
    all_transactions['Grand Total Outlay'] = all_transactions['Total Purchase and Finance Contribution'] + all_transactions['Total Running Costs']
    
    return all_transactions[['Date', 'Total Purchase and Finance Contribution', 'Total Running Costs', 'Grand Total Outlay']] 