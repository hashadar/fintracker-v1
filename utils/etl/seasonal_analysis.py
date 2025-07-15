"""Seasonal analysis functions for financial data."""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def calculate_seasonal_analysis(df):
    """
    Calculate comprehensive seasonal analysis.
    
    Args:
        df (pd.DataFrame): Monthly metrics DataFrame
        
    Returns:
        dict: Seasonal analysis results
    """
    if df is None or df.empty:
        return {}
    
    # Ensure we have enough data for seasonal analysis
    if len(df) < 12:
        return {'error': 'Insufficient data for seasonal analysis (need at least 12 months)'}
    
    # Calculate monthly seasonality
    monthly_seasonality = calculate_monthly_seasonality(df)
    
    # Calculate quarterly seasonality
    quarterly_seasonality = calculate_quarterly_seasonality(df)
    
    # Calculate yearly seasonality
    yearly_seasonality = calculate_yearly_seasonality(df)
    
    # Calculate cyclical patterns
    cyclical_patterns = calculate_cyclical_patterns(df)
    
    # Calculate seasonal decomposition
    seasonal_decomposition = decompose_seasonal_patterns(df)
    
    return {
        'monthly_seasonality': monthly_seasonality,
        'quarterly_seasonality': quarterly_seasonality,
        'yearly_seasonality': yearly_seasonality,
        'cyclical_patterns': cyclical_patterns,
        'seasonal_decomposition': seasonal_decomposition
    }

def calculate_monthly_seasonality(df):
    """
    Calculate monthly seasonality patterns.
    
    Args:
        df (pd.DataFrame): Monthly metrics DataFrame
        
    Returns:
        dict: Monthly seasonality results
    """
    if df is None or df.empty:
        return {}
    
    # Group by month and calculate average metrics
    monthly_stats = df.groupby('Month_Num').agg({
        'Monthly_Return': ['mean', 'std', 'count'],
        'Portfolio_Value': 'mean',
        'Rolling_12M_Volatility': 'mean',
        'Sharpe_Ratio': 'mean'
    }).round(4)
    
    # Flatten column names
    monthly_stats.columns = ['_'.join(col).strip() for col in monthly_stats.columns]
    
    # Calculate best and worst months
    best_month_return = monthly_stats['Monthly_Return_mean'].idxmax()
    worst_month_return = monthly_stats['Monthly_Return_mean'].idxmax()
    
    # Calculate positive return probability by month
    positive_prob = df.groupby('Month_Num')['Monthly_Return'].apply(lambda x: (x > 0).mean())
    
    # Calculate volatility by month
    volatility_by_month = df.groupby('Month_Num')['Monthly_Return'].std() * np.sqrt(12)
    
    return {
        'monthly_statistics': monthly_stats,
        'best_month_return': best_month_return,
        'worst_month_return': worst_month_return,
        'positive_return_probability': positive_prob.to_dict(),
        'volatility_by_month': volatility_by_month.to_dict(),
        'month_names': {
            1: 'January', 2: 'February', 3: 'March', 4: 'April',
            5: 'May', 6: 'June', 7: 'July', 8: 'August',
            9: 'September', 10: 'October', 11: 'November', 12: 'December'
        }
    }

def calculate_quarterly_seasonality(df):
    """
    Calculate quarterly seasonality patterns.
    
    Args:
        df (pd.DataFrame): Monthly metrics DataFrame
        
    Returns:
        dict: Quarterly seasonality results
    """
    if df is None or df.empty:
        return {}
    
    # Add quarter column
    df_copy = df.copy()
    df_copy['Quarter'] = df_copy['Month_Num'].apply(lambda x: (x - 1) // 3 + 1)
    
    # Group by quarter and calculate average metrics
    quarterly_stats = df_copy.groupby('Quarter').agg({
        'Monthly_Return': ['mean', 'std', 'count'],
        'Portfolio_Value': 'mean',
        'Rolling_12M_Volatility': 'mean',
        'Sharpe_Ratio': 'mean'
    }).round(4)
    
    # Flatten column names
    quarterly_stats.columns = ['_'.join(col).strip() for col in quarterly_stats.columns]
    
    # Calculate best and worst quarters
    best_quarter_return = quarterly_stats['Monthly_Return_mean'].idxmax()
    worst_quarter_return = quarterly_stats['Monthly_Return_mean'].idxmin()
    
    # Calculate positive return probability by quarter
    positive_prob = df_copy.groupby('Quarter')['Monthly_Return'].apply(lambda x: (x > 0).mean())
    
    return {
        'quarterly_statistics': quarterly_stats,
        'best_quarter_return': best_quarter_return,
        'worst_quarter_return': worst_quarter_return,
        'positive_return_probability': positive_prob.to_dict(),
        'quarter_names': {1: 'Q1', 2: 'Q2', 3: 'Q3', 4: 'Q4'}
    }

def calculate_yearly_seasonality(df):
    """
    Calculate yearly seasonality patterns.
    
    Args:
        df (pd.DataFrame): Monthly metrics DataFrame
        
    Returns:
        dict: Yearly seasonality results
    """
    if df is None or df.empty:
        return {}
    
    # Group by year and calculate metrics
    yearly_stats = df.groupby('Year').agg({
        'Monthly_Return': ['mean', 'std', 'sum'],
        'Portfolio_Value': ['mean', 'last'],
        'Rolling_12M_Volatility': 'mean',
        'Sharpe_Ratio': 'mean'
    }).round(4)
    
    # Flatten column names
    yearly_stats.columns = ['_'.join(col).strip() for col in yearly_stats.columns]
    
    # Calculate year-over-year growth
    yearly_stats['YoY_Growth'] = yearly_stats['Portfolio_Value_last'].pct_change()
    
    # Calculate best and worst years
    best_year_return = yearly_stats['Monthly_Return_sum'].idxmax()
    worst_year_return = yearly_stats['Monthly_Return_sum'].idxmin()
    
    # Calculate positive return probability by year
    positive_prob = df.groupby('Year')['Monthly_Return'].apply(lambda x: (x > 0).mean())
    
    return {
        'yearly_statistics': yearly_stats,
        'best_year_return': best_year_return,
        'worst_year_return': worst_year_return,
        'positive_return_probability': positive_prob.to_dict(),
        'total_years': len(yearly_stats)
    }

def calculate_cyclical_patterns(df):
    """
    Calculate cyclical patterns in the data.
    
    Args:
        df (pd.DataFrame): Monthly metrics DataFrame
        
    Returns:
        dict: Cyclical patterns results
    """
    if df is None or df.empty:
        return {}
    
    # Calculate rolling correlations to identify cycles
    returns = df['Monthly_Return'].dropna()
    
    if len(returns) < 24:
        return {'error': 'Insufficient data for cyclical analysis'}
    
    # Calculate autocorrelation
    autocorr = calculate_autocorrelation(returns, max_lag=12)
    
    # Calculate moving averages to identify trends
    ma_3m = returns.rolling(3).mean()
    ma_6m = returns.rolling(6).mean()
    ma_12m = returns.rolling(12).mean()
    
    # Identify cyclical turning points
    turning_points = identify_turning_points(returns)
    
    # Calculate cycle length
    cycle_length = calculate_cycle_length(returns)
    
    return {
        'autocorrelation': autocorr,
        'moving_averages': {
            '3m_ma': ma_3m.to_dict(),
            '6m_ma': ma_6m.to_dict(),
            '12m_ma': ma_12m.to_dict()
        },
        'turning_points': turning_points,
        'cycle_length': cycle_length
    }

def calculate_autocorrelation(returns, max_lag=12):
    """
    Calculate autocorrelation for different lags.
    
    Args:
        returns (pd.Series): Return series
        max_lag (int): Maximum lag to calculate
        
    Returns:
        dict: Autocorrelation results
    """
    autocorr = {}
    
    for lag in range(1, min(max_lag + 1, len(returns))):
        if lag < len(returns):
            autocorr[lag] = returns.autocorr(lag=lag)
    
    return autocorr

def identify_turning_points(returns):
    """
    Identify turning points in the return series.
    
    Args:
        returns (pd.Series): Return series
        
    Returns:
        dict: Turning points information
    """
    if len(returns) < 3:
        return {}
    
    peaks = []
    troughs = []
    
    for i in range(1, len(returns) - 1):
        if returns.iloc[i] > returns.iloc[i-1] and returns.iloc[i] > returns.iloc[i+1]:
            peaks.append(i)
        elif returns.iloc[i] < returns.iloc[i-1] and returns.iloc[i] < returns.iloc[i+1]:
            troughs.append(i)
    
    return {
        'peaks': peaks,
        'troughs': troughs,
        'peak_count': len(peaks),
        'trough_count': len(troughs),
        'total_turning_points': len(peaks) + len(troughs)
    }

def calculate_cycle_length(returns):
    """
    Calculate average cycle length.
    
    Args:
        returns (pd.Series): Return series
        
    Returns:
        dict: Cycle length information
    """
    turning_points = identify_turning_points(returns)
    
    if turning_points['total_turning_points'] < 2:
        return {'average_cycle_length': np.nan}
    
    # Calculate distances between turning points
    all_points = sorted(turning_points['peaks'] + turning_points['troughs'])
    distances = [all_points[i+1] - all_points[i] for i in range(len(all_points)-1)]
    
    if distances:
        avg_cycle_length = np.mean(distances)
        std_cycle_length = np.std(distances)
    else:
        avg_cycle_length = std_cycle_length = np.nan
    
    return {
        'average_cycle_length': avg_cycle_length,
        'cycle_length_std': std_cycle_length,
        'min_cycle_length': min(distances) if distances else np.nan,
        'max_cycle_length': max(distances) if distances else np.nan
    }

def decompose_seasonal_patterns(df):
    """
    Decompose time series into trend, seasonal, and residual components.
    
    Args:
        df (pd.DataFrame): Monthly metrics DataFrame
        
    Returns:
        dict: Decomposition results
    """
    if df is None or df.empty or len(df) < 12:
        return {}
    
    # Use returns for decomposition
    returns = df['Monthly_Return'].dropna()
    
    if len(returns) < 12:
        return {}
    
    # Simple decomposition using moving averages
    # Trend component (12-month moving average)
    trend = returns.rolling(12, center=True).mean()
    
    # Detrended series
    detrended = returns - trend
    
    # Seasonal component (average by month)
    seasonal = detrended.groupby(df['Month_Num']).mean()
    
    # Residual component
    seasonal_values = seasonal.reindex(df['Month_Num']).values
    residual = detrended - seasonal_values
    
    # Calculate decomposition statistics
    decomposition_stats = {
        'trend_variance': trend.var(),
        'seasonal_variance': seasonal.var(),
        'residual_variance': residual.var(),
        'total_variance': returns.var(),
        'trend_strength': trend.var() / returns.var() if returns.var() > 0 else 0,
        'seasonal_strength': seasonal.var() / returns.var() if returns.var() > 0 else 0,
        'residual_strength': residual.var() / returns.var() if returns.var() > 0 else 0
    }
    
    return {
        'trend': trend.to_dict(),
        'seasonal': seasonal.to_dict(),
        'residual': residual.to_dict(),
        'decomposition_stats': decomposition_stats
    }

def calculate_seasonal_anomalies(df):
    """
    Calculate seasonal anomalies (deviations from seasonal patterns).
    
    Args:
        df (pd.DataFrame): Monthly metrics DataFrame
        
    Returns:
        dict: Seasonal anomalies
    """
    if df is None or df.empty:
        return {}
    
    # Calculate expected seasonal returns
    seasonal_means = df.groupby('Month_Num')['Monthly_Return'].mean()
    
    # Calculate anomalies
    anomalies = []
    for idx, row in df.iterrows():
        expected_return = seasonal_means[row['Month_Num']]
        actual_return = row['Monthly_Return']
        anomaly = actual_return - expected_return
        anomalies.append({
            'date': row['Timestamp'],
            'month': row['Month_Num'],
            'expected_return': expected_return,
            'actual_return': actual_return,
            'anomaly': anomaly,
            'anomaly_std': anomaly / df['Monthly_Return'].std() if df['Monthly_Return'].std() > 0 else 0
        })
    
    anomalies_df = pd.DataFrame(anomalies)
    
    # Identify significant anomalies
    significant_anomalies = anomalies_df[abs(anomalies_df['anomaly_std']) > 2]
    
    return {
        'all_anomalies': anomalies_df,
        'significant_anomalies': significant_anomalies,
        'anomaly_statistics': {
            'mean_anomaly': anomalies_df['anomaly'].mean(),
            'std_anomaly': anomalies_df['anomaly'].std(),
            'max_positive_anomaly': anomalies_df['anomaly'].max(),
            'max_negative_anomaly': anomalies_df['anomaly'].min(),
            'significant_anomaly_count': len(significant_anomalies)
        }
    }

def create_seasonal_forecast(df, forecast_periods=12):
    """
    Create seasonal forecast based on historical patterns.
    
    Args:
        df (pd.DataFrame): Monthly metrics DataFrame
        forecast_periods (int): Number of periods to forecast
        
    Returns:
        dict: Seasonal forecast
    """
    if df is None or df.empty:
        return {}
    
    # Get seasonal patterns
    seasonal_means = df.groupby('Month_Num')['Monthly_Return'].mean()
    seasonal_stds = df.groupby('Month_Num')['Monthly_Return'].std()
    
    # Get trend component
    returns = df['Monthly_Return'].dropna()
    trend = returns.rolling(12, center=True).mean().iloc[-1] if len(returns) >= 12 else returns.mean()
    
    # Generate forecast
    forecast = []
    current_month = df['Month_Num'].iloc[-1]
    
    for i in range(forecast_periods):
        next_month = ((current_month + i) % 12) + 1
        
        # Combine trend and seasonal components
        seasonal_component = seasonal_means.get(next_month, 0)
        forecast_return = trend + seasonal_component
        
        # Add some randomness based on historical volatility
        seasonal_vol = seasonal_stds.get(next_month, returns.std())
        forecast_return += np.random.normal(0, seasonal_vol)
        
        forecast.append({
            'period': i + 1,
            'month': next_month,
            'forecast_return': forecast_return,
            'trend_component': trend,
            'seasonal_component': seasonal_component
        })
    
    return {
        'forecast': forecast,
        'seasonal_patterns': seasonal_means.to_dict(),
        'trend_component': trend
    } 