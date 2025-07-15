"""Monthly metrics calculation functions for portfolio analysis."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calculate_monthly_metrics(df):
    """
    Calculate comprehensive monthly portfolio metrics.
    
    Args:
        df (pd.DataFrame): DataFrame with 'Timestamp', 'Value' columns
        
    Returns:
        pd.DataFrame: Monthly metrics DataFrame
    """
    if df is None or df.empty:
        return pd.DataFrame()
    
    # Ensure timestamp is datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Group by month and calculate portfolio value
    df['Month'] = df['Timestamp'].dt.to_period('M')
    monthly_data = df.groupby('Month').agg({
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
    
    return monthly_data

def calculate_ytd_metrics(df, current_date=None):
    """
    Calculate Year-to-Date metrics.
    
    Args:
        df (pd.DataFrame): Monthly metrics DataFrame
        current_date (datetime): Current date for YTD calculation
        
    Returns:
        dict: YTD metrics
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

def calculate_qtd_metrics(df, current_date=None):
    """
    Calculate Quarter-to-Date metrics.
    
    Args:
        df (pd.DataFrame): Monthly metrics DataFrame
        current_date (datetime): Current date for QTD calculation
        
    Returns:
        dict: QTD metrics
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

def calculate_annualized_metrics(df, periods_per_year=12):
    """
    Calculate annualized metrics from monthly data.
    
    Args:
        df (pd.DataFrame): Monthly metrics DataFrame
        periods_per_year (int): Number of periods per year (12 for monthly)
        
    Returns:
        pd.DataFrame: DataFrame with annualized metrics
    """
    if df is None or df.empty:
        return pd.DataFrame()
    
    df = df.copy()
    
    # Annualize returns
    df['Annualized_Return'] = (1 + df['Monthly_Return']) ** periods_per_year - 1
    
    # Annualize volatility (already annualized in monthly_metrics)
    df['Annualized_Volatility'] = df['Rolling_12M_Volatility']
    
    # Annualize Sharpe ratio (already annualized in monthly_metrics)
    df['Annualized_Sharpe'] = df['Sharpe_Ratio']
    
    # Calculate annualized Sortino ratio
    negative_returns = df['Monthly_Return'].where(df['Monthly_Return'] < 0, 0)
    df['Downside_Deviation'] = negative_returns.rolling(12).std() * np.sqrt(periods_per_year)
    df['Sortino_Ratio'] = (
        df['Excess_Return'].rolling(12).mean() / 
        df['Downside_Deviation']
    ) * np.sqrt(periods_per_year)
    
    return df

def calculate_rolling_metrics(df, window=12):
    """
    Calculate rolling metrics with adaptive window.
    
    Args:
        df (pd.DataFrame): Monthly metrics DataFrame
        window (int): Rolling window size in months
        
    Returns:
        pd.DataFrame: DataFrame with rolling metrics
    """
    if df is None or df.empty:
        return pd.DataFrame()
    
    df = df.copy()
    
    # Adaptive rolling window based on data availability
    actual_window = min(window, len(df))
    
    # Rolling return
    df[f'Rolling_{actual_window}M_Return'] = df['Portfolio_Value'].pct_change(actual_window)
    
    # Rolling volatility
    df[f'Rolling_{actual_window}M_Volatility'] = (
        df['Monthly_Return'].rolling(actual_window).std() * np.sqrt(12)
    )
    
    # Rolling Sharpe ratio
    df[f'Rolling_{actual_window}M_Sharpe'] = (
        df['Excess_Return'].rolling(actual_window).mean() / 
        df['Monthly_Return'].rolling(actual_window).std()
    ) * np.sqrt(12)
    
    # Rolling Sortino ratio
    negative_returns = df['Monthly_Return'].where(df['Monthly_Return'] < 0, 0)
    df[f'Rolling_{actual_window}M_Sortino'] = (
        df['Excess_Return'].rolling(actual_window).mean() / 
        negative_returns.rolling(actual_window).std()
    ) * np.sqrt(12)
    
    # Rolling maximum drawdown
    df[f'Rolling_{actual_window}M_Max_Drawdown'] = (
        df['Drawdown'].rolling(actual_window).min()
    )
    
    return df 