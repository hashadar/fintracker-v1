"""Data processing utilities for the financial dashboard app."""

import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Union, Tuple
from datetime import datetime
from .config import (
    ASSET_TYPES, DEFAULT_ROLLING_WINDOW, RISK_FREE_RATE, CONFIDENCE_LEVEL,
    VOLATILITY_WINDOW, VAR_CONFIDENCE_LEVEL, MAX_DRAWDOWN_WINDOW,
    MIN_DATA_POINTS_FOR_FORECAST, SEASONAL_PERIODS
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