import pandas as pd
import numpy as np

def forecast_depreciation(valuations_df, car_id, future_periods):
    """
    Forecasts future car value using a simple linear regression on historical valuations.
    """
    car_valuations = valuations_df[valuations_df['CarID'] == car_id].copy()
    car_valuations['Date'] = pd.to_datetime(car_valuations['Date'])
    car_valuations = car_valuations.sort_values(by='Date')

    if len(car_valuations) < 2:
        return None  # Not enough data to forecast

    # Use days from first valuation as the independent variable
    start_date = car_valuations['Date'].min()
    car_valuations['Days'] = (car_valuations['Date'] - start_date).dt.days
    
    # Fit a linear model (y = mx + c)
    X = car_valuations['Days']
    y = car_valuations['Value']
    coeffs = np.polyfit(X, y, 1)
    m, c = coeffs[0], coeffs[1]

    # Generate future dates
    last_date = car_valuations['Date'].max()
    future_dates = pd.to_datetime([last_date + pd.DateOffset(months=i) for i in range(1, future_periods + 1)])
    
    # Predict future values
    last_day = car_valuations['Days'].max()
    future_days = (future_dates - start_date).days
    predicted_values = m * np.array(future_days) + c

    forecast_df = pd.DataFrame({
        'Date': future_dates,
        'ForecastValue': predicted_values
    })

    return forecast_df

def forecast_costs(expenses_df, car_id, future_periods):
    """
    Forecasts future monthly costs based on historical average monthly spend.
    """
    car_expenses = expenses_df[expenses_df['CarID'] == car_id].copy()
    if car_expenses.empty:
        return None

    car_expenses['Date'] = pd.to_datetime(car_expenses['Date'])
    car_expenses.set_index('Date', inplace=True)
    
    # Calculate average monthly cost
    monthly_costs = car_expenses['Cost'].resample('M').sum()
    if len(monthly_costs) == 0:
        return None
        
    avg_monthly_cost = monthly_costs.mean()

    # Generate future dates and costs
    last_date = car_expenses.index.max()
    future_dates = pd.to_datetime([last_date + pd.DateOffset(months=i) for i in range(1, future_periods + 1)])
    
    forecast_df = pd.DataFrame({
        'Date': future_dates,
        'ForecastCost': [avg_monthly_cost] * future_periods
    })
    
    return forecast_df 