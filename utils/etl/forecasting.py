"""Forecasting and scenario analysis functions."""

import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def create_enhanced_forecast_scenarios(df, periods=12, scenarios=1000, confidence_levels=[0.05, 0.25, 0.5, 0.75, 0.95]):
    """
    Create enhanced forecast scenarios using Monte Carlo simulation.
    
    Args:
        df (pd.DataFrame): Monthly metrics DataFrame
        periods (int): Number of periods to forecast
        scenarios (int): Number of Monte Carlo scenarios
        confidence_levels (list): Confidence levels for percentiles
        
    Returns:
        dict: Forecast scenarios and statistics
    """
    if df is None or df.empty:
        return {}
    
    # Get monthly returns
    returns = df['Monthly_Return'].dropna()
    
    if len(returns) < 12:
        return {}
    
    # Calculate historical statistics
    mean_return = returns.mean()
    std_return = returns.std()
    skewness = returns.skew()
    kurtosis = returns.kurtosis()
    
    # Get current portfolio value
    current_value = df['Portfolio_Value'].iloc[-1]
    
    # Generate Monte Carlo scenarios
    scenarios_data = []
    
    for scenario in range(scenarios):
        # Generate random returns using historical distribution
        if abs(skewness) < 0.5 and abs(kurtosis) < 1:
            # Use normal distribution if data is approximately normal
            random_returns = np.random.normal(mean_return, std_return, periods)
        else:
            # Use t-distribution or other non-normal distribution
            df_t = max(2, int(6 / (kurtosis + 3)))  # Degrees of freedom
            random_returns = np.random.standard_t(df_t, periods) * std_return + mean_return
        
        # Calculate cumulative returns and portfolio values
        cumulative_returns = (1 + random_returns).cumprod()
        portfolio_values = current_value * cumulative_returns
        
        # Store scenario data
        scenario_data = {
            'Scenario': scenario,
            'Final_Value': portfolio_values[-1],
            'Total_Return': cumulative_returns[-1] - 1,
            'Annualized_Return': (cumulative_returns[-1] ** (12/periods)) - 1,
            'Max_Drawdown': calculate_scenario_drawdown(portfolio_values),
            'Volatility': random_returns.std() * np.sqrt(12),
            'Sharpe_Ratio': (random_returns.mean() * 12 - 0.02) / (random_returns.std() * np.sqrt(12))
        }
        
        scenarios_data.append(scenario_data)
    
    scenarios_df = pd.DataFrame(scenarios_data)
    
    # Calculate percentiles
    percentiles = {}
    for level in confidence_levels:
        percentiles[f'P{int(level*100)}'] = {
            'Final_Value': np.percentile(scenarios_df['Final_Value'], level * 100),
            'Total_Return': np.percentile(scenarios_df['Total_Return'], level * 100),
            'Annualized_Return': np.percentile(scenarios_df['Annualized_Return'], level * 100),
            'Max_Drawdown': np.percentile(scenarios_df['Max_Drawdown'], level * 100),
            'Volatility': np.percentile(scenarios_df['Volatility'], level * 100),
            'Sharpe_Ratio': np.percentile(scenarios_df['Sharpe_Ratio'], level * 100)
        }
    
    # Calculate expected values
    expected_values = {
        'Final_Value': scenarios_df['Final_Value'].mean(),
        'Total_Return': scenarios_df['Total_Return'].mean(),
        'Annualized_Return': scenarios_df['Annualized_Return'].mean(),
        'Max_Drawdown': scenarios_df['Max_Drawdown'].mean(),
        'Volatility': scenarios_df['Volatility'].mean(),
        'Sharpe_Ratio': scenarios_df['Sharpe_Ratio'].mean()
    }
    
    # Calculate probability of positive returns
    prob_positive = (scenarios_df['Total_Return'] > 0).mean()
    prob_beat_inflation = (scenarios_df['Annualized_Return'] > 0.02).mean()  # Assuming 2% inflation
    
    return {
        'scenarios': scenarios_df,
        'percentiles': percentiles,
        'expected_values': expected_values,
        'probabilities': {
            'positive_return': prob_positive,
            'beat_inflation': prob_beat_inflation
        },
        'historical_stats': {
            'mean_return': mean_return,
            'std_return': std_return,
            'skewness': skewness,
            'kurtosis': kurtosis
        },
        'current_value': current_value,
        'forecast_periods': periods
    }

def calculate_scenario_drawdown(portfolio_values):
    """Calculate maximum drawdown for a scenario."""
    peak = portfolio_values[0]
    max_dd = 0
    
    for value in portfolio_values:
        if value > peak:
            peak = value
        dd = (value - peak) / peak
        max_dd = min(max_dd, dd)
    
    return max_dd

def create_stress_test_scenarios(df, stress_levels=[0.1, 0.2, 0.3]):
    """
    Create stress test scenarios with different market conditions.
    
    Args:
        df (pd.DataFrame): Monthly metrics DataFrame
        stress_levels (list): Stress levels as multipliers
        
    Returns:
        dict: Stress test results
    """
    if df is None or df.empty:
        return {}
    
    # Get historical statistics
    returns = df['Monthly_Return'].dropna()
    mean_return = returns.mean()
    std_return = returns.std()
    current_value = df['Portfolio_Value'].iloc[-1]
    
    stress_results = {}
    
    for stress_level in stress_levels:
        # Create stressed scenarios
        stressed_mean = mean_return * (1 - stress_level)  # Reduce expected returns
        stressed_std = std_return * (1 + stress_level)    # Increase volatility
        
        # Generate stressed returns
        stressed_returns = np.random.normal(stressed_mean, stressed_std, 12)
        stressed_cumulative = (1 + stressed_returns).cumprod()
        stressed_final_value = current_value * stressed_cumulative[-1]
        
        stress_results[f'Stress_{int(stress_level*100)}%'] = {
            'stressed_mean_return': stressed_mean,
            'stressed_volatility': stressed_std * np.sqrt(12),
            'final_value': stressed_final_value,
            'total_return': stressed_cumulative[-1] - 1,
            'annualized_return': stressed_cumulative[-1] - 1,
            'max_drawdown': calculate_scenario_drawdown(current_value * stressed_cumulative)
        }
    
    return stress_results

def create_regime_based_forecasts(df, regimes=['Bull', 'Bear', 'Sideways']):
    """
    Create regime-based forecasts.
    
    Args:
        df (pd.DataFrame): Monthly metrics DataFrame
        regimes (list): Market regimes to consider
        
    Returns:
        dict: Regime-based forecasts
    """
    if df is None or df.empty:
        return {}
    
    returns = df['Monthly_Return'].dropna()
    current_value = df['Portfolio_Value'].iloc[-1]
    
    regime_forecasts = {}
    
    # Define regime characteristics
    regime_params = {
        'Bull': {'mean_mult': 1.5, 'vol_mult': 0.8, 'prob': 0.3},
        'Bear': {'mean_mult': -0.5, 'vol_mult': 1.5, 'prob': 0.2},
        'Sideways': {'mean_mult': 0.8, 'vol_mult': 1.0, 'prob': 0.5}
    }
    
    for regime in regimes:
        params = regime_params[regime]
        
        # Calculate regime-specific parameters
        base_mean = returns.mean()
        base_std = returns.std()
        
        regime_mean = base_mean * params['mean_mult']
        regime_std = base_std * params['vol_mult']
        
        # Generate regime-specific returns
        regime_returns = np.random.normal(regime_mean, regime_std, 12)
        regime_cumulative = (1 + regime_returns).cumprod()
        regime_final_value = current_value * regime_cumulative[-1]
        
        regime_forecasts[regime] = {
            'mean_return': regime_mean,
            'volatility': regime_std * np.sqrt(12),
            'final_value': regime_final_value,
            'total_return': regime_cumulative[-1] - 1,
            'annualized_return': regime_cumulative[-1] - 1,
            'probability': params['prob'],
            'max_drawdown': calculate_scenario_drawdown(current_value * regime_cumulative)
        }
    
    return regime_forecasts

def create_asset_allocation_forecasts(df, asset_allocations):
    """
    Create forecasts for different asset allocations.
    
    Args:
        df (pd.DataFrame): Asset metrics DataFrame
        asset_allocations (dict): Dictionary of asset allocations
        
    Returns:
        dict: Asset allocation forecasts
    """
    if df is None or df.empty:
        return {}
    
    # Get asset-level statistics
    asset_stats = {}
    for (asset, platform), group in df.groupby(['Asset', 'Platform']):
        returns = group['Asset_Return'].dropna()
        if len(returns) > 0:
            asset_stats[(asset, platform)] = {
                'mean_return': returns.mean(),
                'volatility': returns.std(),
                'correlation': returns.corr(df.groupby('Month')['Portfolio_Value'].sum().pct_change())
            }
    
    allocation_forecasts = {}
    
    for allocation_name, weights in asset_allocations.items():
        # Calculate portfolio statistics
        portfolio_mean = 0
        portfolio_var = 0
        
        for (asset, platform), weight in weights.items():
            if (asset, platform) in asset_stats:
                stats = asset_stats[(asset, platform)]
                portfolio_mean += weight * stats['mean_return']
                portfolio_var += (weight * stats['volatility']) ** 2
        
        # Add correlation terms (simplified)
        portfolio_std = np.sqrt(portfolio_var)
        
        # Generate forecast
        forecast_returns = np.random.normal(portfolio_mean, portfolio_std, 12)
        forecast_cumulative = (1 + forecast_returns).cumprod()
        
        allocation_forecasts[allocation_name] = {
            'expected_return': portfolio_mean * 12,
            'volatility': portfolio_std * np.sqrt(12),
            'sharpe_ratio': (portfolio_mean * 12 - 0.02) / (portfolio_std * np.sqrt(12)),
            'final_value_multiplier': forecast_cumulative[-1],
            'total_return': forecast_cumulative[-1] - 1
        }
    
    return allocation_forecasts

def create_rolling_forecasts(df, window=12, forecast_periods=6):
    """
    Create rolling forecasts to test forecast accuracy.
    
    Args:
        df (pd.DataFrame): Monthly metrics DataFrame
        window (int): Rolling window size
        forecast_periods (int): Number of periods to forecast
        
    Returns:
        dict: Rolling forecast results
    """
    if df is None or df.empty or len(df) < window + forecast_periods:
        return {}
    
    rolling_forecasts = []
    
    for i in range(window, len(df) - forecast_periods):
        # Get historical data
        historical_data = df.iloc[i-window:i]
        actual_data = df.iloc[i:i+forecast_periods]
        
        # Calculate forecast
        historical_returns = historical_data['Monthly_Return'].dropna()
        forecast_mean = historical_returns.mean()
        forecast_std = historical_returns.std()
        
        # Generate forecast
        forecast_returns = np.random.normal(forecast_mean, forecast_std, forecast_periods)
        forecast_cumulative = (1 + forecast_returns).cumprod()
        
        # Calculate actual results
        actual_cumulative = (1 + actual_data['Monthly_Return']).cumprod()
        
        # Store results
        rolling_forecasts.append({
            'forecast_date': historical_data.index[-1],
            'forecast_return': forecast_cumulative[-1] - 1,
            'actual_return': actual_cumulative[-1] - 1,
            'forecast_error': (forecast_cumulative[-1] - actual_cumulative[-1]) / actual_cumulative[-1],
            'forecast_volatility': forecast_std * np.sqrt(12),
            'actual_volatility': actual_data['Monthly_Return'].std() * np.sqrt(12)
        })
    
    if rolling_forecasts:
        results_df = pd.DataFrame(rolling_forecasts)
        
        # Calculate forecast accuracy metrics
        mae = abs(results_df['forecast_error']).mean()
        rmse = np.sqrt((results_df['forecast_error'] ** 2).mean())
        hit_rate = (results_df['forecast_error'].abs() < 0.1).mean()  # Within 10%
        
        return {
            'rolling_forecasts': results_df,
            'accuracy_metrics': {
                'mae': mae,
                'rmse': rmse,
                'hit_rate': hit_rate
            }
        }
    
    return {}

def create_forecast_summary(forecast_results):
    """
    Create a summary of all forecast results.
    
    Args:
        forecast_results (dict): Dictionary containing all forecast results
        
    Returns:
        dict: Forecast summary
    """
    summary = {}
    
    # Monte Carlo scenarios
    if 'monte_carlo' in forecast_results:
        mc = forecast_results['monte_carlo']
        summary['monte_carlo'] = {
            'expected_final_value': mc['expected_values']['Final_Value'],
            'expected_return': mc['expected_values']['Annualized_Return'],
            'probability_positive': mc['probabilities']['positive_return'],
            'worst_case_5%': mc['percentiles']['P5']['Final_Value'],
            'best_case_95%': mc['percentiles']['P95']['Final_Value']
        }
    
    # Stress tests
    if 'stress_tests' in forecast_results:
        stress = forecast_results['stress_tests']
        summary['stress_tests'] = {}
        for stress_level, results in stress.items():
            summary['stress_tests'][stress_level] = {
                'final_value': results['final_value'],
                'return': results['annualized_return'],
                'drawdown': results['max_drawdown']
            }
    
    # Regime forecasts
    if 'regime_forecasts' in forecast_results:
        regime = forecast_results['regime_forecasts']
        summary['regime_forecasts'] = {}
        for regime_name, results in regime.items():
            summary['regime_forecasts'][regime_name] = {
                'expected_return': results['annualized_return'],
                'probability': results['probability'],
                'final_value': results['final_value']
            }
    
    return summary 