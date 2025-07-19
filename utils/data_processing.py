"""Data processing utilities for the financial dashboard app."""

import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Union, Tuple
from datetime import datetime
from .config import (
    ASSET_TYPES, DEFAULT_ROLLING_WINDOW, RISK_FREE_RATE, CONFIDENCE_LEVEL,
    VOLATILITY_WINDOW, VAR_CONFIDENCE_LEVEL, MAX_DRAWDOWN_WINDOW,
    MIN_DATA_POINTS_FOR_FORECAST, SEASONAL_PERIODS,
    CAR_LOAN_STATUSES, CAR_PAYMENT_TYPES, CAR_EXPENSE_TYPES,
    DEFAULT_CAR_FORECAST_PERIODS, CAR_DEPRECIATION_RATE, CAR_MAINTENANCE_FREQUENCY
)


def filter_by_asset_type(df: pd.DataFrame, asset_type: str) -> pd.DataFrame:
    """
    Filter data by asset type.
    
    Args:
        df: Input DataFrame with 'Asset_Type' column
        asset_type: Asset type to filter by (e.g., 'Cash', 'Investments', 'Pensions')
    
    Returns:
        Filtered DataFrame containing only the specified asset type
    """
    if df is None or df.empty:
        return pd.DataFrame()
    
    return df[df['Asset_Type'] == asset_type].copy()


def get_latest_month_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get data for the most recent month.
    
    Args:
        df: Input DataFrame with 'Timestamp' column
    
    Returns:
        DataFrame containing only the latest month's data
    """
    if df is None or df.empty:
        return pd.DataFrame()
    
    df_copy = df.copy()
    df_copy['Month'] = df_copy['Timestamp'].dt.to_period('M')
    latest_month = df_copy['Month'].max()
    
    return df_copy[df_copy['Month'] == latest_month]


def get_monthly_aggregation(df: pd.DataFrame, group_by_cols: Optional[List[str]] = None, 
                          value_col: str = 'Value') -> pd.DataFrame:
    """
    Aggregate data by month with optional grouping.
    
    Args:
        df: Input DataFrame with 'Timestamp' column
        group_by_cols: Additional columns to group by (e.g., ['Asset_Type', 'Platform'])
        value_col: Name of the value column to aggregate
    
    Returns:
        Aggregated DataFrame with monthly totals
    """
    if df is None or df.empty:
        return pd.DataFrame()
    
    df_copy = df.copy()
    df_copy['Month'] = df_copy['Timestamp'].dt.to_period('M')
    
    # Ensure value column is numeric
    df_copy[value_col] = pd.to_numeric(df_copy[value_col], errors='coerce')
    
    # Define grouping columns
    group_cols = ['Month']
    if group_by_cols:
        group_cols.extend(group_by_cols)
    
    # Aggregate
    aggregated = df_copy.groupby(group_cols)[value_col].sum().reset_index()
    
    # Convert Period to timestamp for JSON serialization
    aggregated['Month'] = aggregated['Month'].dt.to_timestamp()
    
    return aggregated


def calculate_rolling_metrics(df: pd.DataFrame, window: int = DEFAULT_ROLLING_WINDOW, 
                            value_col: str = 'Value') -> pd.DataFrame:
    """
    Calculate rolling averages and standard deviations.
    
    Args:
        df: Input DataFrame with monthly aggregated data
        window: Rolling window size (default: 3 months)
        value_col: Name of the value column to calculate rolling metrics for
    
    Returns:
        DataFrame with rolling metrics added
    """
    if df is None or df.empty:
        return pd.DataFrame()
    
    df_copy = df.copy()
    
    # Ensure we have monthly data
    if 'Month' not in df_copy.columns:
        df_copy['Month'] = df_copy['Timestamp'].dt.to_period('M')
        df_copy = df_copy.groupby('Month')[value_col].sum().reset_index()
    
    # Convert Period to timestamp for JSON serialization
    if df_copy['Month'].dtype == 'object' or hasattr(df_copy['Month'].iloc[0], 'freq'):
        df_copy['Month'] = df_copy['Month'].dt.to_timestamp()
    
    # Sort by month to ensure proper rolling calculation
    df_copy = df_copy.sort_values('Month')
    
    # Calculate rolling metrics
    df_copy[f'Rolling_{window}M_Avg'] = df_copy[value_col].rolling(window=window).mean()
    df_copy[f'Rolling_{window}M_Std'] = df_copy[value_col].rolling(window=window).std()
    df_copy[f'Rolling_{window}M_Volatility'] = df_copy[f'Rolling_{window}M_Std'] / df_copy[f'Rolling_{window}M_Avg']
    
    return df_copy


def get_asset_breakdown(df: pd.DataFrame, breakdown_type: str = 'platform') -> pd.DataFrame:
    """
    Get asset breakdown by platform or asset type.
    
    Args:
        df: Input DataFrame
        breakdown_type: Type of breakdown ('platform', 'asset_type', 'asset')
    
    Returns:
        DataFrame with breakdown data
    """
    if df is None or df.empty:
        return pd.DataFrame()
    
    df_copy = df.copy()
    
    if breakdown_type == 'platform':
        breakdown_col = 'Platform'
    elif breakdown_type == 'asset_type':
        breakdown_col = 'Asset_Type'
    elif breakdown_type == 'asset':
        breakdown_col = 'Asset'
    else:
        raise ValueError(f"Unknown breakdown_type: {breakdown_type}")
    
    if breakdown_col not in df_copy.columns:
        return pd.DataFrame()
    
    # Get latest month data for current breakdown
    latest_data = get_latest_month_data(df_copy)
    
    if latest_data.empty:
        return pd.DataFrame()
    
    # Calculate breakdown
    breakdown = latest_data.groupby(breakdown_col)['Value'].sum().reset_index()
    breakdown['Percentage'] = (breakdown['Value'] / breakdown['Value'].sum()) * 100
    
    return breakdown.sort_values('Value', ascending=False)


def calculate_asset_type_metrics(df: pd.DataFrame, asset_type: str) -> Dict[str, Union[float, int, str, None]]:
    """
    Calculate comprehensive metrics for a specific asset type.
    
    Args:
        df: Input DataFrame with 'Asset_Type', 'Timestamp', 'Value', 'Platform', 'Asset' columns
        asset_type: Asset type to calculate metrics for (e.g., 'Cash', 'Investments', 'Pensions')
    
    Returns:
        Dictionary containing asset type metrics
    """
    if df is None or df.empty:
        return {
            'latest_value': 0.0,
            'mom_change': None,
            'ytd_change': None,
            'platforms': 0,
            'assets': 0,
            'months_tracked': 0,
            'avg_monthly_value': 0.0,
            'max_value': 0.0,
            'min_value': 0.0,
            'volatility': 0.0
        }
    
    # Filter data for the specific asset type
    asset_df = filter_by_asset_type(df, asset_type)
    
    if asset_df.empty:
        return {
            'latest_value': 0.0,
            'mom_change': None,
            'ytd_change': None,
            'platforms': 0,
            'assets': 0,
            'months_tracked': 0,
            'avg_monthly_value': 0.0,
            'max_value': 0.0,
            'min_value': 0.0,
            'volatility': 0.0
        }
    
    # Ensure timestamp is datetime
    asset_df['Timestamp'] = pd.to_datetime(asset_df['Timestamp'])
    asset_df['Month'] = asset_df['Timestamp'].dt.to_period('M')
    
    # Get latest month data
    latest_month = asset_df['Month'].max()
    latest_data = asset_df[asset_df['Month'] == latest_month]
    latest_value = latest_data['Value'].sum()
    
    # Calculate MoM change
    previous_month = asset_df[asset_df['Month'] < latest_month]['Month'].max()
    mom_change = None
    if pd.notna(previous_month):
        previous_data = asset_df[asset_df['Month'] == previous_month]
        previous_value = previous_data['Value'].sum()
        if previous_value > 0:
            mom_change = ((latest_value - previous_value) / previous_value) * 100
    
    # Calculate YTD change
    current_year = latest_month.year
    ytd_start_month = asset_df[asset_df['Month'].dt.year == current_year]['Month'].min()
    ytd_change = None
    if pd.notna(ytd_start_month):
        ytd_start_data = asset_df[asset_df['Month'] == ytd_start_month]
        ytd_start_value = ytd_start_data['Value'].sum()
        if ytd_start_value > 0:
            ytd_change = ((latest_value - ytd_start_value) / ytd_start_value) * 100
    
    # Calculate monthly aggregated values for additional metrics
    monthly_agg = get_monthly_aggregation(asset_df)
    
    # Calculate metrics
    metrics = {
        'latest_value': float(latest_value),
        'mom_change': mom_change,
        'ytd_change': ytd_change,
        'platforms': int(latest_data['Platform'].nunique()),
        'assets': int(latest_data['Asset'].nunique()),
        'months_tracked': int(asset_df['Month'].nunique()),
        'avg_monthly_value': float(monthly_agg['Value'].mean()) if not monthly_agg.empty else 0.0,
        'max_value': float(monthly_agg['Value'].max()) if not monthly_agg.empty else 0.0,
        'min_value': float(monthly_agg['Value'].min()) if not monthly_agg.empty else 0.0,
        'volatility': float(monthly_agg['Value'].std()) if not monthly_agg.empty else 0.0
    }
    
    return metrics


def calculate_actual_pension_returns(asset_df: pd.DataFrame, cashflows_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate actual percentage returns for pension assets by removing cashflow impact.
    Uses the formula: Return = (End Value - Start Value - Net Cashflow) / Start Value
    """
    if asset_df is None or asset_df.empty:
        return pd.DataFrame()

    # --- 1. Prepare Asset Data ---
    asset_copy = asset_df.copy()
    asset_copy['Month'] = asset_copy['Timestamp'].dt.to_period('M').dt.to_timestamp()
    asset_monthly = asset_copy.groupby(['Month', 'Asset'])['Value'].last().reset_index()

    # --- 2. Prepare Cashflow Data ---
    if cashflows_df is not None and not cashflows_df.empty:
        cashflow_copy = cashflows_df.copy()
        cashflow_copy['Month'] = cashflow_copy['Timestamp'].dt.to_period('M').dt.to_timestamp()
        cashflow_monthly = cashflow_copy.groupby(['Month', 'Asset'])['Value'].sum().reset_index()
        cashflow_monthly = cashflow_monthly.rename(columns={'Value': 'Net_Cashflow'})
    else:
        cashflow_monthly = pd.DataFrame(columns=['Month', 'Asset', 'Net_Cashflow'])

    # --- 3. Combine Data and Calculate Returns ---
    all_returns = []
    for asset in asset_monthly['Asset'].unique():
        # Isolate data for one asset
        single_asset_values = asset_monthly[asset_monthly['Asset'] == asset].sort_values('Month')
        single_asset_cashflows = cashflow_monthly[cashflow_monthly['Asset'] == asset]

        # Merge asset values with their corresponding cashflows
        merged_df = pd.merge(single_asset_values, single_asset_cashflows, on=['Month', 'Asset'], how='left')
        merged_df['Net_Cashflow'] = merged_df['Net_Cashflow'].fillna(0)

        # Get Start Value (which is the End Value of the previous month)
        merged_df['Start_Value'] = merged_df['Value'].shift(1)

        # Drop the first row for each asset as it has no previous month to compare against
        merged_df = merged_df.dropna(subset=['Start_Value'])

        if merged_df.empty:
            continue
            
        # Rename columns for clarity before calculation
        merged_df = merged_df.rename(columns={'Value': 'End_Value'})

        # Calculate actual return using the correct formula
        def calculate_return(row):
            if row['Start_Value'] > 0:
                # (End - Start - Cashflow) / Start
                return (row['End_Value'] - row['Start_Value'] - row['Net_Cashflow']) / row['Start_Value']
            return 0.0

        merged_df['Actual_Return'] = merged_df.apply(calculate_return, axis=1)
        all_returns.append(merged_df)

    if not all_returns:
        return pd.DataFrame()

    final_returns_df = pd.concat(all_returns, ignore_index=True)
    
    # Ensure all required columns are present for downstream components
    final_returns_df['Value_Before_Cashflow'] = final_returns_df['End_Value'] - final_returns_df['Net_Cashflow']
    final_returns_df['Current_Value'] = final_returns_df['End_Value']
    final_returns_df['Current_Cashflow'] = final_returns_df['Net_Cashflow']

    return final_returns_df


def get_cumulative_pension_cashflows(cashflows_df: pd.DataFrame) -> pd.DataFrame:
    """
    Get cumulative cashflows by asset over time.
    
    Args:
        cashflows_df: DataFrame with pension cashflow data
    
    Returns:
        DataFrame with columns: Month, Asset, Cumulative_Cashflow
    """
    if cashflows_df is None or cashflows_df.empty:
        return pd.DataFrame()
    
    df = cashflows_df.copy()
    df['Month'] = df['Timestamp'].dt.to_period('M')
    monthly_cashflows = df.groupby(['Month', 'Asset'])['Value'].sum().reset_index()
    monthly_cashflows['Month'] = monthly_cashflows['Month'].dt.to_timestamp()
    
    # Calculate cumulative cashflows
    cumulative_data = []
    for asset in monthly_cashflows['Asset'].unique():
        asset_data = monthly_cashflows[monthly_cashflows['Asset'] == asset].sort_values('Month')
        asset_data['Cumulative_Cashflow'] = asset_data['Value'].cumsum()
        cumulative_data.append(asset_data[['Month', 'Asset', 'Cumulative_Cashflow']])
    
    if cumulative_data:
        return pd.concat(cumulative_data, ignore_index=True)
    else:
        return pd.DataFrame()


def calculate_actual_mom_changes(asset_df: pd.DataFrame, cashflows_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate actual month-over-month percentage changes by removing cashflow impact.
    
    Args:
        asset_df: DataFrame with pension asset data
        cashflows_df: DataFrame with pension cashflow data
    
    Returns:
        DataFrame with columns: Month, Asset, Actual_MoM_Change
    """
    actual_returns = calculate_actual_pension_returns(asset_df, cashflows_df)
    
    if actual_returns.empty:
        return pd.DataFrame()
    
    # The actual returns are already the MoM changes
    mom_data = actual_returns[['Month', 'Asset', 'Actual_Return']].copy()
    mom_data = mom_data.rename(columns={'Actual_Return': 'Actual_MoM_Change'})
    
    return mom_data


def calculate_allocation_metrics(df: pd.DataFrame) -> Tuple[Dict[str, Dict[str, Union[float, None]]], pd.Timestamp, Optional[pd.Timestamp], Optional[pd.Timestamp]]:
    """
    Calculate comprehensive allocation metrics for all asset types.
    
    Args:
        df: Input DataFrame with 'Asset_Type', 'Timestamp', 'Value' columns
    
    Returns:
        Tuple containing:
        - Dictionary of allocation metrics for each asset type
        - Latest month timestamp
        - Previous month timestamp (or None)
        - YTD start month timestamp (or None)
    """
    if df is None or df.empty:
        return {}, pd.Timestamp.now(), None, None
    
    # Ensure timestamp is datetime
    df_copy = df.copy()
    df_copy['Timestamp'] = pd.to_datetime(df_copy['Timestamp'])
    df_copy['Month'] = df_copy['Timestamp'].dt.to_period('M')
    
    # Get time periods
    latest_month = df_copy['Month'].max()
    previous_month = df_copy[df_copy['Month'] < latest_month]['Month'].max()
    current_year = latest_month.year
    ytd_start_month = df_copy[df_copy['Month'].dt.year == current_year]['Month'].min()
    
    # Convert periods to timestamps
    latest_month_ts = latest_month.to_timestamp()
    previous_month_ts = previous_month.to_timestamp() if pd.notna(previous_month) else None
    ytd_start_month_ts = ytd_start_month.to_timestamp() if pd.notna(ytd_start_month) else None
    
    # Get latest month data
    latest_data = df_copy[df_copy['Month'] == latest_month]
    total_current = latest_data['Value'].sum()
    
    # Calculate metrics for each asset type
    allocation_metrics = {}
    
    # Total portfolio metrics
    if pd.notna(previous_month):
        previous_data = df_copy[df_copy['Month'] == previous_month]
        total_previous = previous_data['Value'].sum()
        mom_increase = total_current - total_previous if total_previous > 0 else None
    else:
        mom_increase = None
    
    if pd.notna(ytd_start_month):
        ytd_start_data = df_copy[df_copy['Month'] == ytd_start_month]
        total_ytd_start = ytd_start_data['Value'].sum()
        ytd_increase = total_current - total_ytd_start if total_ytd_start > 0 else None
    else:
        ytd_increase = None
    
    allocation_metrics['Total'] = {
        'current': float(total_current),
        'mom_increase': mom_increase,
        'ytd_increase': ytd_increase
    }
    
    # Asset type specific metrics
    for asset_type in [ASSET_TYPES['CASH'], ASSET_TYPES['INVESTMENTS'], ASSET_TYPES['PENSIONS']]:
        asset_data = latest_data[latest_data['Asset_Type'] == asset_type]
        current_value = asset_data['Value'].sum()
        allocation_pct = (current_value / total_current * 100) if total_current > 0 else 0
        
        # MoM change
        mom_pct_increase = None
        if pd.notna(previous_month):
            prev_asset_data = df_copy[(df_copy['Month'] == previous_month) & (df_copy['Asset_Type'] == asset_type)]
            prev_value = prev_asset_data['Value'].sum()
            if prev_value > 0:
                mom_pct_increase = ((current_value - prev_value) / prev_value) * 100
        
        # YTD change
        ytd_pct_increase = None
        if pd.notna(ytd_start_month):
            ytd_asset_data = df_copy[(df_copy['Month'] == ytd_start_month) & (df_copy['Asset_Type'] == asset_type)]
            ytd_start_value = ytd_asset_data['Value'].sum()
            if ytd_start_value > 0:
                ytd_pct_increase = ((current_value - ytd_start_value) / ytd_start_value) * 100
        
        allocation_metrics[asset_type] = {
            'current': float(current_value),
            'allocation': float(allocation_pct),
            'mom_pct_increase': mom_pct_increase,
            'ytd_pct_increase': ytd_pct_increase
        }
    
    return allocation_metrics, latest_month_ts, previous_month_ts, ytd_start_month_ts


def get_asset_type_time_periods(df: pd.DataFrame, asset_type: str) -> Tuple[pd.Timestamp, Optional[pd.Timestamp], Optional[pd.Timestamp]]:
    """
    Get time periods (latest, previous, YTD start) for a specific asset type.
    
    Args:
        df: Input DataFrame with 'Asset_Type', 'Timestamp', 'Value' columns
        asset_type: Asset type to get time periods for
    
    Returns:
        Tuple containing:
        - Latest month timestamp
        - Previous month timestamp (or None)
        - YTD start month timestamp (or None)
    """
    if df is None or df.empty:
        return pd.Timestamp.now(), None, None
    
    # Filter data for the specific asset type
    asset_df = filter_by_asset_type(df, asset_type)
    
    if asset_df.empty:
        return pd.Timestamp.now(), None, None
    
    # Ensure timestamp is datetime
    asset_df_copy = asset_df.copy()
    asset_df_copy['Timestamp'] = pd.to_datetime(asset_df_copy['Timestamp'])
    asset_df_copy['Month'] = asset_df_copy['Timestamp'].dt.to_period('M')
    
    # Get time periods
    latest_month = asset_df_copy['Month'].max()
    previous_month = asset_df_copy[asset_df_copy['Month'] < latest_month]['Month'].max()
    current_year = latest_month.year
    ytd_start_month = asset_df_copy[asset_df_copy['Month'].dt.year == current_year]['Month'].min()
    
    # Convert periods to timestamps
    latest_month_ts = latest_month.to_timestamp()
    previous_month_ts = previous_month.to_timestamp() if pd.notna(previous_month) else None
    ytd_start_month_ts = ytd_start_month.to_timestamp() if pd.notna(ytd_start_month) else None
    
    return latest_month_ts, previous_month_ts, ytd_start_month_ts


def create_platform_trends_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create platform trends data for time series charts.
    
    Args:
        df: Input DataFrame with 'Timestamp', 'Platform', and 'Value' columns
    
    Returns:
        DataFrame with Month as index and Platform columns for charting
    """
    if df is None or df.empty:
        return pd.DataFrame()
    
    df_copy = df.copy()
    df_copy['Month'] = df_copy['Timestamp'].dt.to_period('M').dt.to_timestamp()
    
    # Create pivot table for platform trends
    platform_trends = df_copy.pivot_table(
        index='Month',
        columns='Platform',
        values='Value',
        aggfunc='sum'
    ).reset_index()
    
    return platform_trends


def create_allocation_time_series(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create allocation time series data showing percentage allocation by asset type over time.
    
    Args:
        df: Input DataFrame with 'Asset_Type', 'Timestamp', 'Value' columns
    
    Returns:
        DataFrame with Month as index and allocation percentage columns for each asset type
    """
    if df is None or df.empty:
        return pd.DataFrame()
    
    df_copy = df.copy()
    df_copy['Timestamp'] = pd.to_datetime(df_copy['Timestamp'])
    df_copy['Month'] = df_copy['Timestamp'].dt.to_period('M')
    
    # Calculate monthly allocation percentages for each asset type
    allocation_time_series = []
    for month in df_copy['Month'].unique():
        month_data = df_copy[df_copy['Month'] == month]
        total_value = month_data['Value'].sum()
        
        month_allocation = {'Month': month.to_timestamp()}  # Convert Period to timestamp
        for asset_type in [ASSET_TYPES['CASH'], ASSET_TYPES['INVESTMENTS'], ASSET_TYPES['PENSIONS']]:
            asset_value = month_data[month_data['Asset_Type'] == asset_type]['Value'].sum()
            allocation_pct = (asset_value / total_value) if total_value > 0 else 0  # Return as decimal (0.255 for 25.5%)
            month_allocation[f'{asset_type} Allocation %'] = allocation_pct
        
        allocation_time_series.append(month_allocation)
    
    allocation_df = pd.DataFrame(allocation_time_series)
    
    # Sort by month for proper time series display
    if not allocation_df.empty:
        allocation_df = allocation_df.sort_values('Month')
    
    return allocation_df 


def create_platform_allocation_time_series(df: pd.DataFrame, asset_type: str) -> pd.DataFrame:
    """
    Create a time series DataFrame of allocation % by platform for a given asset type.
    Args:
        df: Input DataFrame with 'Timestamp', 'Asset_Type', 'Platform', 'Value'
        asset_type: Asset type to filter (e.g., 'Cash')
    Returns:
        DataFrame with columns: Month, one column per platform, values as decimals (0.25 for 25%)
    """
    if df is None or df.empty:
        return pd.DataFrame()
    df_copy = df.copy()
    df_copy = df_copy[df_copy['Asset_Type'] == asset_type]
    if df_copy.empty:
        return pd.DataFrame()
    df_copy['Month'] = df_copy['Timestamp'].dt.to_period('M')
    allocation_time_series = []
    for month in df_copy['Month'].unique():
        month_data = df_copy[df_copy['Month'] == month]
        total_value = month_data['Value'].sum()
        month_allocation = {'Month': month.to_timestamp()}
        for platform in month_data['Platform'].unique():
            platform_value = month_data[month_data['Platform'] == platform]['Value'].sum()
            allocation_pct = (platform_value / total_value) if total_value > 0 else 0
            month_allocation[platform] = allocation_pct
        allocation_time_series.append(month_allocation)
    allocation_df = pd.DataFrame(allocation_time_series)
    if not allocation_df.empty:
        allocation_df = allocation_df.sort_values('Month')
    return allocation_df 


def forecast_pension_growth(
    historical_df: pd.DataFrame,
    forecast_years: int,
    monthly_contribution: float,
    annual_return_rate: float,
    annual_volatility: float = 0.15,
    confidence_level: float = 0.90
) -> pd.DataFrame:
    """
    Forecasts pension growth using a simple Monte Carlo simulation.

    Args:
        historical_df (pd.DataFrame): DataFrame with historical monthly values. Must contain 'Month' and 'Value' columns.
        forecast_years (int): The number of years to forecast.
        monthly_contribution (float): The planned future monthly contribution.
        annual_return_rate (float): The expected average annual return (as a decimal, e.g., 0.07 for 7%).
        annual_volatility (float): The expected annual volatility (standard deviation).
        confidence_level (float): The confidence level for the upper and lower bounds (e.g., 0.90 for 90%).

    Returns:
        pd.DataFrame: A DataFrame containing the full projection with columns 
                      ['Month', 'Type', 'Projected_Value', 'Lower_Bound', 'Upper_Bound'].
    """
    if historical_df.empty:
        return pd.DataFrame()

    # --- 1. Prepare Parameters ---
    last_historical_month = historical_df['Month'].max()
    last_historical_value = historical_df[historical_df['Month'] == last_historical_month]['Value'].iloc[0]
    
    monthly_return_rate = (1 + annual_return_rate)**(1/12) - 1
    monthly_volatility = annual_volatility / np.sqrt(12)
    
    num_months = forecast_years * 12
    num_simulations = 500  # Number of Monte Carlo simulations to run
    
    # --- 2. Run Monte Carlo Simulation ---
    all_simulations = np.zeros((num_months + 1, num_simulations))
    all_simulations[0, :] = last_historical_value

    for t in range(1, num_months + 1):
        # Generate random returns for this month across all simulations
        random_returns = np.random.normal(monthly_return_rate, monthly_volatility, num_simulations)
        # Calculate the new value for each simulation
        all_simulations[t, :] = all_simulations[t-1, :] * (1 + random_returns) + monthly_contribution

    # --- 3. Aggregate Results ---
    projection_df = pd.DataFrame(all_simulations)
    
    # Calculate median, lower, and upper bounds
    lower_percentile = (1 - confidence_level) / 2
    upper_percentile = 1 - lower_percentile
    
    median_projection = projection_df.quantile(q=0.5, axis=1)
    lower_bound = projection_df.quantile(q=lower_percentile, axis=1)
    upper_bound = projection_df.quantile(q=upper_percentile, axis=1)

    # --- 4. Format Output DataFrame ---
    forecast_dates = pd.to_datetime([last_historical_month + pd.DateOffset(months=i) for i in range(num_months + 1)])
    
    forecast_results = pd.DataFrame({
        'Month': forecast_dates,
        'Projected_Value': median_projection,
        'Lower_Bound': lower_bound,
        'Upper_Bound': upper_bound
    })

    # Combine with historical data for a continuous chart
    historical_formatted = historical_df[['Month', 'Value']].copy()
    historical_formatted.rename(columns={'Value': 'Projected_Value'}, inplace=True)
    historical_formatted['Type'] = 'Historical'
    
    forecast_results['Type'] = 'Forecast'
    
    # Ensure the first forecast point aligns with the last historical point
    forecast_results.loc[0, 'Projected_Value'] = last_historical_value
    forecast_results.loc[0, 'Lower_Bound'] = last_historical_value
    forecast_results.loc[0, 'Upper_Bound'] = last_historical_value

    final_df = pd.concat([historical_formatted.iloc[:-1], forecast_results], ignore_index=True)

    return final_df 

# Car-specific data processing functions

def calculate_car_equity(car_assets_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate equity for each car based on loan status.
    
    Args:
        car_assets_df: DataFrame with car assets data including Loan_Status, Car_Value, Loan_Balance
    
    Returns:
        DataFrame with equity calculations added
    """
    if car_assets_df is None or car_assets_df.empty:
        return pd.DataFrame()
    
    df = car_assets_df.copy()
    
    # Calculate equity based on loan status
    def calculate_equity(row):
        if pd.isna(row['Car_Value']):
            return None
        
        if row['Loan_Status'] == CAR_LOAN_STATUSES['OWNED']:
            return row['Car_Value']  # 100% equity for owned vehicles
        elif row['Loan_Status'] == CAR_LOAN_STATUSES['FINANCED']:
            loan_balance = row['Loan_Balance'] if pd.notna(row['Loan_Balance']) else 0
            return row['Car_Value'] - loan_balance
        else:
            return None
    
    df['Equity'] = df.apply(calculate_equity, axis=1)
    df['Equity_Percentage'] = (df['Equity'] / df['Car_Value'] * 100).where(df['Car_Value'] > 0)
    df['LTV_Ratio'] = (df['Loan_Balance'] / df['Car_Value'] * 100).where(
        (df['Loan_Status'] == CAR_LOAN_STATUSES['FINANCED']) & (df['Car_Value'] > 0)
    )
    
    return df

def calculate_car_monthly_costs(car_expenses_df: pd.DataFrame, car_payments_df: pd.DataFrame, 
                               car_assets_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate monthly car costs including loan payments and operating expenses.
    
    Args:
        car_expenses_df: DataFrame with car expenses data
        car_payments_df: DataFrame with car payments data
        car_assets_df: DataFrame with car assets data
    
    Returns:
        DataFrame with monthly cost breakdown
    """
    if car_expenses_df is None or car_expenses_df.empty:
        return pd.DataFrame()
    
    # Prepare expenses data
    expenses_df = car_expenses_df.copy()
    expenses_df['Month'] = expenses_df['Timestamp'].dt.to_period('M')
    
    # Group expenses by month and type
    monthly_expenses = expenses_df.groupby(['Month', 'Expense_Type'])['Amount'].sum().reset_index()
    
    # Pivot to get expense types as columns
    monthly_expenses_pivot = monthly_expenses.pivot_table(
        index='Month',
        columns='Expense_Type',
        values='Amount',
        aggfunc='sum',
        fill_value=0
    ).reset_index()
    
    # Add loan payments if available
    if car_payments_df is not None and not car_payments_df.empty:
        payments_df = car_payments_df.copy()
        payments_df['Month'] = payments_df['Timestamp'].dt.to_period('M')
        
        # Include all payment types (not just regular) to ensure we capture all loan payments
        monthly_loan_payments = payments_df.groupby('Month')['Payment_Amount'].sum().reset_index()
        
        # Merge with expenses
        monthly_expenses_pivot = monthly_expenses_pivot.merge(
            monthly_loan_payments, on='Month', how='left'
        )
        monthly_expenses_pivot['Loan_Payment'] = monthly_expenses_pivot['Payment_Amount'].fillna(0)
        monthly_expenses_pivot = monthly_expenses_pivot.drop('Payment_Amount', axis=1)
    else:
        monthly_expenses_pivot['Loan_Payment'] = 0
    
    # Calculate total monthly costs
    expense_columns = [col for col in monthly_expenses_pivot.columns 
                      if col not in ['Month', 'Loan_Payment']]
    monthly_expenses_pivot['Total'] = monthly_expenses_pivot[expense_columns + ['Loan_Payment']].sum(axis=1)
    
    # Convert Month back to timestamp
    monthly_expenses_pivot['Month'] = monthly_expenses_pivot['Month'].dt.to_timestamp()
    
    return monthly_expenses_pivot



def get_car_equity_trends(car_assets_df: pd.DataFrame) -> pd.DataFrame:
    """
    Create equity trends over time for cars.
    
    Args:
        car_assets_df: DataFrame with car assets data
    
    Returns:
        DataFrame with equity trends over time
    """
    if car_assets_df is None or car_assets_df.empty:
        return pd.DataFrame()
    
    # Calculate equity for all data points
    df_with_equity = calculate_car_equity(car_assets_df)
    
    if df_with_equity.empty:
        return pd.DataFrame()
    
    # Create time series of equity by car
    equity_trends = df_with_equity.groupby(['Timestamp', 'Asset'])['Equity'].sum().reset_index()
    
    # Pivot to get cars as columns
    equity_pivot = equity_trends.pivot_table(
        index='Timestamp',
        columns='Asset',
        values='Equity',
        aggfunc='sum'
    ).reset_index()
    
    return equity_pivot


def _calculate_ytd_mileage(car_assets_df: pd.DataFrame) -> float:
    """
    Helper function to calculate YTD mileage for vehicles.
    
    Args:
        car_assets_df: DataFrame with car assets data
    
    Returns:
        Total YTD mileage across all vehicles
    """
    from datetime import datetime
    
    if car_assets_df is None or car_assets_df.empty:
        return 0.0
    
    current_year = datetime.now().year
    
    # Get first mileage reading of the year for each vehicle
    ytd_start_data = car_assets_df[car_assets_df['Timestamp'].dt.year == current_year].copy()
    if ytd_start_data.empty:
        return 0.0
    
    # Group by vehicle and get the earliest reading of the year
    first_readings = ytd_start_data.groupby('Asset')['Mileage'].first().reset_index()
    
    # Get latest data for each car
    car_assets_with_equity = calculate_car_equity(car_assets_df)
    latest_car_data = car_assets_with_equity.groupby('Asset').last().reset_index()
    latest_readings = latest_car_data[['Asset', 'Mileage']]
    
    # Merge to get first and latest readings for each vehicle
    mileage_comparison = latest_readings.merge(first_readings, on='Asset', suffixes=('_latest', '_first'))
    
    # Calculate YTD mileage for each vehicle
    mileage_comparison['ytd_mileage'] = mileage_comparison['Mileage_latest'] - mileage_comparison['Mileage_first']
    return mileage_comparison['ytd_mileage'].sum()


def calculate_vehicle_metrics(car_assets_df: pd.DataFrame, car_expenses_df: pd.DataFrame, 
                            car_payments_df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate comprehensive vehicle metrics for dashboard display.
    
    Args:
        car_assets_df: DataFrame with car assets data
        car_expenses_df: DataFrame with car expenses data
        car_payments_df: DataFrame with car payments data
    
    Returns:
        Dictionary with vehicle metrics
    """
    from datetime import datetime
    
    metrics = {
        'latest_loan_payment': 0.0,
        'latest_monthly_expenses': 0.0,
        'latest_month_combined_costs': 0.0,
        'cost_per_mile': 0.0
    }
    
    # Get latest loan payment
    if car_payments_df is not None and not car_payments_df.empty:
        latest_payment = car_payments_df.sort_values('Timestamp').iloc[-1]
        metrics['latest_loan_payment'] = latest_payment['Payment_Amount'] if pd.notna(latest_payment['Payment_Amount']) else 0.0
    
    # Get latest monthly expenses
    if car_expenses_df is not None and not car_expenses_df.empty:
        # Get the latest month with expenses
        car_expenses_df_copy = car_expenses_df.copy()
        car_expenses_df_copy['Month'] = car_expenses_df_copy['Timestamp'].dt.to_period('M')
        latest_month = car_expenses_df_copy['Month'].max()
        latest_month_expenses = car_expenses_df_copy[car_expenses_df_copy['Month'] == latest_month]
        metrics['latest_monthly_expenses'] = latest_month_expenses['Amount'].sum() if not latest_month_expenses.empty else 0.0
    
    # Calculate combined loan + expenses for latest month
    metrics['latest_month_combined_costs'] = metrics['latest_loan_payment'] + metrics['latest_monthly_expenses']
    
    # Calculate YTD mileage for cost per mile calculation
    ytd_mileage = _calculate_ytd_mileage(car_assets_df)
    
    # Calculate cost per mile (including loan payments and expenses)
    total_ytd_costs = 0.0
    current_year = datetime.now().year
    
    if car_expenses_df is not None and not car_expenses_df.empty:
        # Get YTD expenses
        ytd_expenses = car_expenses_df[car_expenses_df['Timestamp'].dt.year == current_year]
        total_ytd_costs += ytd_expenses['Amount'].sum() if not ytd_expenses.empty else 0.0

    if car_payments_df is not None and not car_payments_df.empty:
        # Get YTD loan payments
        ytd_payments = car_payments_df[car_payments_df['Timestamp'].dt.year == current_year]
        total_ytd_costs += ytd_payments['Payment_Amount'].sum() if not ytd_payments.empty else 0.0

    # Calculate cost per mile
    if ytd_mileage > 0:
        metrics['cost_per_mile'] = total_ytd_costs / ytd_mileage
    
    return metrics 


def calculate_vehicle_summary_metrics(car_assets_df: pd.DataFrame) -> Dict[str, Union[float, int, str]]:
    """
    Calculate comprehensive vehicle summary metrics for dashboard display.
    
    Args:
        car_assets_df: DataFrame with car assets data
    
    Returns:
        Dictionary with vehicle summary metrics
    """
    from datetime import datetime
    
    metrics = {
        'total_car_value': 0.0,
        'total_equity': 0.0,
        'total_loan_balance': 0.0,
        'financed_count': 0,
        'owned_count': 0,
        'vehicle_names_display': "No vehicles",
        'ytd_mileage': 0,
        'latest_mileage': 0
    }
    
    if car_assets_df is None or car_assets_df.empty:
        return metrics
    
    # Calculate equity for all cars
    car_assets_with_equity = calculate_car_equity(car_assets_df)
    
    # Get latest data for each car
    latest_car_data = car_assets_with_equity.groupby('Asset').last().reset_index()
    
    # Calculate summary metrics
    metrics['total_car_value'] = latest_car_data['Car_Value'].sum() if not latest_car_data['Car_Value'].isna().all() else 0.0
    metrics['total_equity'] = latest_car_data['Equity'].sum() if not latest_car_data['Equity'].isna().all() else 0.0
    metrics['total_loan_balance'] = latest_car_data['Loan_Balance'].sum() if not latest_car_data['Loan_Balance'].isna().all() else 0.0
    
    # Count vehicles by status
    from utils import CAR_LOAN_STATUSES
    metrics['financed_count'] = len(latest_car_data[latest_car_data['Loan_Status'] == CAR_LOAN_STATUSES['FINANCED']])
    metrics['owned_count'] = len(latest_car_data[latest_car_data['Loan_Status'] == CAR_LOAN_STATUSES['OWNED']])
    
    # Get vehicle names for display
    vehicle_names = latest_car_data['Asset'].tolist()
    metrics['vehicle_names_display'] = ", ".join(vehicle_names) if vehicle_names else "No vehicles"
    
    # Calculate YTD mileage using helper function
    metrics['ytd_mileage'] = _calculate_ytd_mileage(car_assets_df)
    
    # Calculate latest total mileage
    if not car_assets_df.empty:
        latest_mileage_data = car_assets_df.groupby('Asset')['Mileage'].max()
        metrics['latest_mileage'] = latest_mileage_data.sum()
    
    return metrics 