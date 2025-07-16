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


def get_time_period_data(df: pd.DataFrame, period_type: str = 'latest') -> pd.DataFrame:
    """
    Get data for specific time periods.
    
    Args:
        df: Input DataFrame with 'Timestamp' column
        period_type: Type of period ('latest', 'previous', 'ytd_start')
    
    Returns:
        DataFrame for the specified time period
    """
    if df is None or df.empty:
        return pd.DataFrame()
    
    df_copy = df.copy()
    df_copy['Month'] = df_copy['Timestamp'].dt.to_period('M')
    
    if period_type == 'latest':
        latest_month = df_copy['Month'].max()
        return df_copy[df_copy['Month'] == latest_month]
    
    elif period_type == 'previous':
        latest_month = df_copy['Month'].max()
        previous_month = df_copy[df_copy['Month'] < latest_month]['Month'].max()
        if pd.notna(previous_month):
            return df_copy[df_copy['Month'] == previous_month]
        return pd.DataFrame()
    
    elif period_type == 'ytd_start':
        latest_month = df_copy['Month'].max()
        current_year = latest_month.year
        ytd_start_month = df_copy[df_copy['Month'].dt.year == current_year]['Month'].min()
        if pd.notna(ytd_start_month):
            return df_copy[df_copy['Month'] == ytd_start_month]
        return pd.DataFrame()
    
    else:
        raise ValueError(f"Unknown period_type: {period_type}. Use 'latest', 'previous', or 'ytd_start'")


def calculate_percentage_changes(df: pd.DataFrame, value_col: str = 'Value') -> pd.DataFrame:
    """
    Calculate MoM and YTD percentage changes.
    
    Args:
        df: Input DataFrame with 'Timestamp' and value column
        value_col: Name of the value column to calculate changes for
    
    Returns:
        DataFrame with percentage change columns added
    """
    if df is None or df.empty:
        return pd.DataFrame()
    
    df_copy = df.copy()
    df_copy['Month'] = df_copy['Timestamp'].dt.to_period('M')
    
    # Ensure value column is numeric
    df_copy[value_col] = pd.to_numeric(df_copy[value_col], errors='coerce')
    
    # Calculate monthly totals
    monthly_totals = df_copy.groupby('Month')[value_col].sum().reset_index()
    
    # Calculate MoM percentage change
    monthly_totals['MoM_Pct_Change'] = monthly_totals[value_col].pct_change()
    
    # Calculate YTD percentage change
    latest_month = monthly_totals['Month'].max()
    current_year = latest_month.year
    ytd_start_month = monthly_totals[monthly_totals['Month'].dt.year == current_year]['Month'].min()
    
    if pd.notna(ytd_start_month):
        ytd_start_value = monthly_totals[monthly_totals['Month'] == ytd_start_month][value_col].iloc[0]
        monthly_totals['YTD_Pct_Change'] = (monthly_totals[value_col] - ytd_start_value) / ytd_start_value
    else:
        monthly_totals['YTD_Pct_Change'] = None
    
    # Convert Period to timestamp for JSON serialization
    monthly_totals['Month'] = monthly_totals['Month'].dt.to_timestamp()
    
    return monthly_totals


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


def prepare_chart_data(df: pd.DataFrame, x_col: str = 'Month', y_col: str = 'Value',
                      chart_type: str = 'time_series') -> pd.DataFrame:
    """
    Prepare data specifically for charting with common transformations.
    
    Args:
        df: Input DataFrame
        x_col: Column to use for x-axis
        y_col: Column to use for y-axis
        chart_type: Type of chart ('time_series', 'bar', 'pie')
    
    Returns:
        DataFrame prepared for the specified chart type
    """
    if df is None or df.empty:
        return pd.DataFrame()
    
    df_copy = df.copy()
    
    if chart_type == 'time_series':
        # Ensure proper datetime format for time series
        if x_col == 'Month' and 'Month' in df_copy.columns:
            df_copy['Month'] = df_copy['Month'].dt.to_timestamp()
        elif x_col == 'Timestamp':
            df_copy[x_col] = pd.to_datetime(df_copy[x_col])
        
        # Sort by x-axis for proper time series display
        df_copy = df_copy.sort_values(x_col)
    
    elif chart_type == 'bar':
        # For bar charts, ensure categorical data is properly formatted
        if x_col in df_copy.columns:
            df_copy[x_col] = df_copy[x_col].astype(str)
    
    elif chart_type == 'pie':
        # For pie charts, ensure we have the right columns
        if y_col not in df_copy.columns:
            raise ValueError(f"Column '{y_col}' not found in DataFrame for pie chart")
    
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


def calculate_drawdown(df: pd.DataFrame, value_col: str = 'Value') -> pd.DataFrame:
    """
    Calculate drawdown metrics for portfolio analysis.
    
    Args:
        df: Input DataFrame with monthly aggregated data
        value_col: Name of the value column to calculate drawdown for
    
    Returns:
        DataFrame with drawdown metrics added
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
    
    # Sort by month
    df_copy = df_copy.sort_values('Month')
    
    # Calculate running maximum
    df_copy['Running_Max'] = df_copy[value_col].cummax()
    
    # Calculate drawdown
    df_copy['Drawdown'] = (df_copy[value_col] - df_copy['Running_Max']) / df_copy['Running_Max']
    
    # Calculate drawdown duration
    df_copy['Drawdown_Duration'] = 0
    in_drawdown = False
    duration = 0
    
    for i, row in df_copy.iterrows():
        if row['Drawdown'] < 0:
            if not in_drawdown:
                in_drawdown = True
                duration = 1
            else:
                duration += 1
        else:
            in_drawdown = False
            duration = 0
        
        df_copy.at[i, 'Drawdown_Duration'] = duration
    
    return df_copy


def get_performance_metrics(df: pd.DataFrame, value_col: str = 'Value') -> Dict[str, float]:
    """
    Calculate key performance metrics from monthly data.
    
    Args:
        df: Input DataFrame with monthly aggregated data
        value_col: Name of the value column to calculate metrics for
    
    Returns:
        Dictionary containing performance metrics
    """
    if df is None or df.empty:
        return {}
    
    df_copy = df.copy()
    
    # Ensure we have monthly data
    if 'Month' not in df_copy.columns:
        df_copy['Month'] = df_copy['Timestamp'].dt.to_period('M')
        df_copy = df_copy.groupby('Month')[value_col].sum().reset_index()
    
    # Sort by month
    df_copy = df_copy.sort_values('Month')
    
    # Calculate returns
    df_copy['Returns'] = df_copy[value_col].pct_change()
    
    # Calculate metrics
    metrics = {
        'total_return': (df_copy[value_col].iloc[-1] / df_copy[value_col].iloc[0]) - 1,
        'avg_monthly_return': df_copy['Returns'].mean(),
        'volatility': df_copy['Returns'].std(),
        'sharpe_ratio': df_copy['Returns'].mean() / df_copy['Returns'].std() if df_copy['Returns'].std() != 0 else 0,
        'max_drawdown': df_copy['Returns'].min(),
        'best_month': df_copy['Returns'].max(),
        'worst_month': df_copy['Returns'].min(),
        'positive_months': (df_copy['Returns'] > 0).sum(),
        'total_months': len(df_copy)
    }
    
    return metrics


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


# Monthly Metrics Functions (moved from ETL)
def calculate_monthly_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate comprehensive monthly portfolio metrics.
    
    Args:
        df: DataFrame with 'Timestamp', 'Value' columns
        
    Returns:
        Monthly metrics DataFrame
    """
    if df is None or df.empty:
        return pd.DataFrame()
    
    # Ensure timestamp is datetime
    df_copy = df.copy()
    df_copy['Timestamp'] = pd.to_datetime(df_copy['Timestamp'])
    
    # Group by month and calculate portfolio value
    df_copy['Month'] = df_copy['Timestamp'].dt.to_period('M')
    monthly_data = df_copy.groupby('Month').agg({
        'Value': 'sum',
        'Timestamp': 'last'
    }).reset_index()
    
    # Sort by month to ensure chronological order
    monthly_data = monthly_data.sort_values('Month')
    
    # Calculate returns
    monthly_data['Portfolio_Value'] = monthly_data['Value']
    monthly_data['Monthly_Return'] = monthly_data['Portfolio_Value'].pct_change()
    monthly_data['Cumulative_Return'] = (1 + monthly_data['Monthly_Return']).cumprod() - 1
    
    # Calculate rolling metrics
    monthly_data['Rolling_3M_Return'] = monthly_data['Portfolio_Value'].pct_change(3)
    monthly_data['Rolling_6M_Return'] = monthly_data['Portfolio_Value'].pct_change(6)
    monthly_data['Rolling_12M_Return'] = monthly_data['Portfolio_Value'].pct_change(12)
    
    # Calculate volatility (rolling 12-month)
    monthly_data['Rolling_12M_Volatility'] = monthly_data['Monthly_Return'].rolling(12).std() * np.sqrt(12)
    
    # Calculate Sharpe ratio (assuming risk-free rate of 2%)
    risk_free_rate = 0.02
    monthly_data['Excess_Return'] = monthly_data['Monthly_Return'] - risk_free_rate/12
    monthly_data['Sharpe_Ratio'] = (
        monthly_data['Excess_Return'].rolling(12).mean() / 
        monthly_data['Monthly_Return'].rolling(12).std()
    ) * np.sqrt(12)
    
    # Calculate maximum drawdown
    monthly_data['Peak_Value'] = monthly_data['Portfolio_Value'].expanding().max()
    monthly_data['Drawdown'] = (monthly_data['Portfolio_Value'] - monthly_data['Peak_Value']) / monthly_data['Peak_Value']
    monthly_data['Max_Drawdown'] = monthly_data['Drawdown'].expanding().min()
    
    # Calculate Calmar ratio
    monthly_data['Calmar_Ratio'] = (
        monthly_data['Rolling_12M_Return'] / 
        abs(monthly_data['Max_Drawdown'].rolling(12).min())
    )
    
    # Add month info
    monthly_data['Year'] = monthly_data['Month'].dt.year
    monthly_data['Month_Num'] = monthly_data['Month'].dt.month
    monthly_data['Month_Name'] = monthly_data['Month'].dt.strftime('%B')
    
    # Convert Period to timestamp for JSON serialization
    monthly_data['Month'] = monthly_data['Month'].dt.to_timestamp()
    
    return monthly_data


def calculate_ytd_metrics(df: pd.DataFrame, current_date: Optional[datetime] = None) -> Dict[str, float]:
    """
    Calculate Year-to-Date metrics.
    
    Args:
        df: Monthly metrics DataFrame
        current_date: Current date for YTD calculation
        
    Returns:
        YTD metrics dictionary
    """
    if df is None or df.empty:
        return {}
    
    if current_date is None:
        current_date = datetime.now()
    
    current_year = current_date.year
    
    # Filter for current year
    ytd_data = df[df['Year'] == current_year].copy()
    
    if ytd_data.empty:
        return {}
    
    # Calculate YTD metrics
    ytd_metrics = {
        'ytd_return': ytd_data['Cumulative_Return'].iloc[-1] if len(ytd_data) > 0 else 0,
        'ytd_volatility': ytd_data['Monthly_Return'].std() * np.sqrt(12) if len(ytd_data) > 1 else 0,
        'ytd_sharpe': ytd_data['Sharpe_Ratio'].iloc[-1] if len(ytd_data) > 0 else 0,
        'ytd_max_drawdown': ytd_data['Max_Drawdown'].iloc[-1] if len(ytd_data) > 0 else 0,
        'ytd_calmar': ytd_data['Calmar_Ratio'].iloc[-1] if len(ytd_data) > 0 else 0,
        'ytd_months': len(ytd_data),
        'current_portfolio_value': ytd_data['Portfolio_Value'].iloc[-1] if len(ytd_data) > 0 else 0
    }
    
    return ytd_metrics


def calculate_qtd_metrics(df: pd.DataFrame, current_date: Optional[datetime] = None) -> Dict[str, float]:
    """
    Calculate Quarter-to-Date metrics.
    
    Args:
        df: Monthly metrics DataFrame
        current_date: Current date for QTD calculation
        
    Returns:
        QTD metrics dictionary
    """
    if df is None or df.empty:
        return {}
    
    if current_date is None:
        current_date = datetime.now()
    
    current_year = current_date.year
    current_quarter = (current_date.month - 1) // 3 + 1
    
    # Determine quarter start month
    quarter_start_month = (current_quarter - 1) * 3 + 1
    
    # Filter for current quarter
    qtd_data = df[
        (df['Year'] == current_year) & 
        (df['Month_Num'] >= quarter_start_month)
    ].copy()
    
    if qtd_data.empty:
        return {}
    
    # Get portfolio value at start of quarter
    if len(qtd_data) > 1:
        quarter_start_value = qtd_data['Portfolio_Value'].iloc[0]
        quarter_end_value = qtd_data['Portfolio_Value'].iloc[-1]
        qtd_return = (quarter_end_value - quarter_start_value) / quarter_start_value
    else:
        qtd_return = 0
    
    # Calculate QTD metrics
    qtd_metrics = {
        'qtd_return': qtd_return,
        'qtd_volatility': qtd_data['Monthly_Return'].std() * np.sqrt(12) if len(qtd_data) > 1 else 0,
        'qtd_months': len(qtd_data),
        'quarter_start_value': qtd_data['Portfolio_Value'].iloc[0] if len(qtd_data) > 0 else 0,
        'quarter_end_value': qtd_data['Portfolio_Value'].iloc[-1] if len(qtd_data) > 0 else 0,
        'current_quarter': current_quarter
    }
    
    return qtd_metrics


# Risk Metrics Functions (moved from ETL)
def sortino_ratio(returns: pd.Series, risk_free_rate: float = RISK_FREE_RATE, periods_per_year: int = 12) -> float:
    """
    Calculate Sortino ratio.
    
    Args:
        returns: Return series
        risk_free_rate: Risk-free rate (annual)
        periods_per_year: Number of periods per year
        
    Returns:
        Sortino ratio
    """
    if returns is None or len(returns) == 0:
        return np.nan
    
    # Calculate excess returns
    excess_returns = returns - risk_free_rate / periods_per_year
    
    # Calculate downside deviation
    negative_returns = returns[returns < 0]
    if len(negative_returns) == 0:
        return np.nan
    
    downside_deviation = negative_returns.std() * np.sqrt(periods_per_year)
    
    if downside_deviation == 0:
        return np.nan
    
    # Calculate Sortino ratio
    sortino = (excess_returns.mean() * periods_per_year) / downside_deviation
    
    return sortino


def calculate_var(returns: pd.Series, confidence_level: float = VAR_CONFIDENCE_LEVEL) -> float:
    """
    Calculate Value at Risk (VaR).
    
    Args:
        returns: Return series
        confidence_level: Confidence level (e.g., 0.05 for 95% VaR)
        
    Returns:
        VaR value
    """
    if returns is None or len(returns) == 0:
        return np.nan
    
    return np.percentile(returns, confidence_level * 100)


def calculate_cvar(returns: pd.Series, confidence_level: float = VAR_CONFIDENCE_LEVEL) -> float:
    """
    Calculate Conditional Value at Risk (CVaR) / Expected Shortfall.
    
    Args:
        returns: Return series
        confidence_level: Confidence level (e.g., 0.05 for 95% CVaR)
        
    Returns:
        CVaR value
    """
    if returns is None or len(returns) == 0:
        return np.nan
    
    var = calculate_var(returns, confidence_level)
    return returns[returns <= var].mean()


def calculate_max_drawdown(returns: pd.Series) -> float:
    """
    Calculate maximum drawdown from return series.
    
    Args:
        returns: Return series
        
    Returns:
        Maximum drawdown
    """
    if returns is None or len(returns) == 0:
        return np.nan
    
    # Convert returns to cumulative values
    cumulative = (1 + returns).cumprod()
    
    # Calculate running maximum
    running_max = cumulative.expanding().max()
    
    # Calculate drawdown
    drawdown = (cumulative - running_max) / running_max
    
    return drawdown.min() 