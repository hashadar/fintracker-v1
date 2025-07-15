"""Risk metrics calculation functions."""

import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime

def sortino_ratio(returns, risk_free_rate=0.02, periods_per_year=12):
    """
    Calculate Sortino ratio.
    
    Args:
        returns (pd.Series): Return series
        risk_free_rate (float): Risk-free rate (annual)
        periods_per_year (int): Number of periods per year
        
    Returns:
        float: Sortino ratio
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

def calculate_var(returns, confidence_level=0.05):
    """
    Calculate Value at Risk (VaR).
    
    Args:
        returns (pd.Series): Return series
        confidence_level (float): Confidence level (e.g., 0.05 for 95% VaR)
        
    Returns:
        float: VaR value
    """
    if returns is None or len(returns) == 0:
        return np.nan
    
    return np.percentile(returns, confidence_level * 100)

def calculate_cvar(returns, confidence_level=0.05):
    """
    Calculate Conditional Value at Risk (CVaR) / Expected Shortfall.
    
    Args:
        returns (pd.Series): Return series
        confidence_level (float): Confidence level (e.g., 0.05 for 95% CVaR)
        
    Returns:
        float: CVaR value
    """
    if returns is None or len(returns) == 0:
        return np.nan
    
    var = calculate_var(returns, confidence_level)
    return returns[returns <= var].mean()

def detect_regime(returns, window=12, threshold=0.5):
    """
    Detect market regime using rolling volatility and return characteristics.
    
    Args:
        returns (pd.Series): Return series
        window (int): Rolling window size
        threshold (float): Threshold for regime classification
        
    Returns:
        pd.Series: Regime labels
    """
    if returns is None or len(returns) < window:
        return pd.Series(['Insufficient Data'] * len(returns))
    
    # Calculate rolling metrics
    rolling_vol = returns.rolling(window).std() * np.sqrt(12)
    rolling_return = returns.rolling(window).mean() * 12
    rolling_skew = returns.rolling(window).skew()
    
    # Initialize regime series
    regime = pd.Series(['Normal'] * len(returns), index=returns.index)
    
    # Define regime thresholds
    vol_threshold = rolling_vol.quantile(threshold)
    return_threshold = rolling_return.quantile(1 - threshold)
    
    # Classify regimes
    for i in range(window, len(returns)):
        if rolling_vol.iloc[i] > vol_threshold:
            if rolling_return.iloc[i] < -return_threshold:
                regime.iloc[i] = 'High Volatility - Low Return'
            elif rolling_return.iloc[i] > return_threshold:
                regime.iloc[i] = 'High Volatility - High Return'
            else:
                regime.iloc[i] = 'High Volatility'
        else:
            if rolling_return.iloc[i] < -return_threshold:
                regime.iloc[i] = 'Low Volatility - Low Return'
            elif rolling_return.iloc[i] > return_threshold:
                regime.iloc[i] = 'Low Volatility - High Return'
            else:
                regime.iloc[i] = 'Normal'
    
    return regime

def calculate_rolling_risk_metrics(returns, window=12, risk_free_rate=0.02):
    """
    Calculate rolling risk metrics.
    
    Args:
        returns (pd.Series): Return series
        window (int): Rolling window size
        risk_free_rate (float): Risk-free rate (annual)
        
    Returns:
        pd.DataFrame: Rolling risk metrics
    """
    if returns is None or len(returns) < window:
        return pd.DataFrame()
    
    metrics = []
    
    for i in range(window, len(returns)):
        window_returns = returns.iloc[i-window:i]
        
        # Calculate metrics for this window
        volatility = window_returns.std() * np.sqrt(12)
        sharpe = (window_returns.mean() * 12 - risk_free_rate) / volatility
        sortino = sortino_ratio(window_returns, risk_free_rate)
        var_95 = calculate_var(window_returns, 0.05)
        cvar_95 = calculate_cvar(window_returns, 0.05)
        max_drawdown = calculate_max_drawdown(window_returns)
        
        metrics.append({
            'Date': returns.index[i],
            'Rolling_Volatility': volatility,
            'Rolling_Sharpe': sharpe,
            'Rolling_Sortino': sortino,
            'Rolling_VaR_95': var_95,
            'Rolling_CVaR_95': cvar_95,
            'Rolling_Max_Drawdown': max_drawdown
        })
    
    return pd.DataFrame(metrics)

def calculate_max_drawdown(returns):
    """
    Calculate maximum drawdown from return series.
    
    Args:
        returns (pd.Series): Return series
        
    Returns:
        float: Maximum drawdown
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

def calculate_ulcer_index(returns, window=14):
    """
    Calculate Ulcer Index - a measure of downside risk.
    
    Args:
        returns (pd.Series): Return series
        window (int): Rolling window size
        
    Returns:
        float: Ulcer Index
    """
    if returns is None or len(returns) == 0:
        return np.nan
    
    # Convert returns to cumulative values
    cumulative = (1 + returns).cumprod()
    
    # Calculate running maximum
    running_max = cumulative.expanding().max()
    
    # Calculate drawdown
    drawdown = (cumulative - running_max) / running_max
    
    # Calculate Ulcer Index
    ulcer_index = np.sqrt((drawdown ** 2).rolling(window).mean().iloc[-1])
    
    return ulcer_index

def calculate_gain_to_pain_ratio(returns):
    """
    Calculate Gain-to-Pain ratio.
    
    Args:
        returns (pd.Series): Return series
        
    Returns:
        float: Gain-to-Pain ratio
    """
    if returns is None or len(returns) == 0:
        return np.nan
    
    gains = returns[returns > 0].sum()
    losses = abs(returns[returns < 0].sum())
    
    if losses == 0:
        return np.inf if gains > 0 else np.nan
    
    return gains / losses

def calculate_calmar_ratio(returns, window=12):
    """
    Calculate Calmar ratio.
    
    Args:
        returns (pd.Series): Return series
        window (int): Rolling window size
        
    Returns:
        float: Calmar ratio
    """
    if returns is None or len(returns) < window:
        return np.nan
    
    # Calculate annualized return
    annual_return = returns.mean() * 12
    
    # Calculate maximum drawdown
    max_dd = calculate_max_drawdown(returns)
    
    if max_dd == 0:
        return np.nan
    
    return annual_return / abs(max_dd)

def calculate_treynor_ratio(returns, market_returns, risk_free_rate=0.02):
    """
    Calculate Treynor ratio.
    
    Args:
        returns (pd.Series): Portfolio return series
        market_returns (pd.Series): Market return series
        risk_free_rate (float): Risk-free rate (annual)
        
    Returns:
        float: Treynor ratio
    """
    if returns is None or market_returns is None or len(returns) == 0:
        return np.nan
    
    # Calculate beta
    covariance = np.cov(returns, market_returns)[0, 1]
    market_variance = np.var(market_returns)
    
    if market_variance == 0:
        return np.nan
    
    beta = covariance / market_variance
    
    if beta == 0:
        return np.nan
    
    # Calculate Treynor ratio
    excess_return = returns.mean() * 12 - risk_free_rate
    treynor = excess_return / beta
    
    return treynor

def calculate_information_ratio(returns, benchmark_returns):
    """
    Calculate Information ratio.
    
    Args:
        returns (pd.Series): Portfolio return series
        benchmark_returns (pd.Series): Benchmark return series
        
    Returns:
        float: Information ratio
    """
    if returns is None or benchmark_returns is None or len(returns) == 0:
        return np.nan
    
    # Calculate active returns
    active_returns = returns - benchmark_returns
    
    # Calculate Information ratio
    information_ratio = active_returns.mean() / active_returns.std()
    
    return information_ratio

def calculate_jensen_alpha(returns, market_returns, risk_free_rate=0.02):
    """
    Calculate Jensen's Alpha.
    
    Args:
        returns (pd.Series): Portfolio return series
        market_returns (pd.Series): Market return series
        risk_free_rate (float): Risk-free rate (annual)
        
    Returns:
        float: Jensen's Alpha
    """
    if returns is None or market_returns is None or len(returns) == 0:
        return np.nan
    
    # Calculate beta
    covariance = np.cov(returns, market_returns)[0, 1]
    market_variance = np.var(market_returns)
    
    if market_variance == 0:
        return np.nan
    
    beta = covariance / market_variance
    
    # Calculate Jensen's Alpha
    portfolio_return = returns.mean() * 12
    market_return = market_returns.mean() * 12
    
    alpha = portfolio_return - (risk_free_rate + beta * (market_return - risk_free_rate))
    
    return alpha

def calculate_risk_metrics_summary(returns, risk_free_rate=0.02):
    """
    Calculate comprehensive risk metrics summary.
    
    Args:
        returns (pd.Series): Return series
        risk_free_rate (float): Risk-free rate (annual)
        
    Returns:
        dict: Risk metrics summary
    """
    if returns is None or len(returns) == 0:
        return {}
    
    # Basic statistics
    mean_return = returns.mean() * 12
    volatility = returns.std() * np.sqrt(12)
    
    # Risk metrics
    sharpe_ratio = (mean_return - risk_free_rate) / volatility if volatility > 0 else np.nan
    sortino_ratio_val = sortino_ratio(returns, risk_free_rate)
    var_95 = calculate_var(returns, 0.05)
    cvar_95 = calculate_cvar(returns, 0.05)
    max_drawdown = calculate_max_drawdown(returns)
    calmar_ratio = calculate_calmar_ratio(returns)
    ulcer_index = calculate_ulcer_index(returns)
    gain_to_pain = calculate_gain_to_pain_ratio(returns)
    
    # Additional statistics
    skewness = returns.skew()
    kurtosis = returns.kurtosis()
    
    summary = {
        'Mean_Return': mean_return,
        'Volatility': volatility,
        'Sharpe_Ratio': sharpe_ratio,
        'Sortino_Ratio': sortino_ratio_val,
        'VaR_95': var_95,
        'CVaR_95': cvar_95,
        'Max_Drawdown': max_drawdown,
        'Calmar_Ratio': calmar_ratio,
        'Ulcer_Index': ulcer_index,
        'Gain_to_Pain_Ratio': gain_to_pain,
        'Skewness': skewness,
        'Kurtosis': kurtosis,
        'Total_Return': (1 + returns).prod() - 1,
        'Positive_Days': (returns > 0).sum(),
        'Negative_Days': (returns < 0).sum(),
        'Total_Days': len(returns)
    }
    
    return summary 