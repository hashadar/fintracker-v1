"""Asset-level metrics calculation functions."""

import pandas as pd
import numpy as np
from datetime import datetime

def calculate_asset_metrics(df):
    """
    Calculate comprehensive asset-level metrics.
    
    Args:
        df (pd.DataFrame): DataFrame with 'Timestamp', 'Asset', 'Platform', 'Value' columns
        
    Returns:
        pd.DataFrame: Asset metrics DataFrame
    """
    if df is None or df.empty:
        return pd.DataFrame()
    
    # Ensure timestamp is datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Group by month and asset to get monthly values
    df['Month'] = df['Timestamp'].dt.to_period('M')
    asset_monthly = df.groupby(['Month', 'Asset', 'Platform']).agg({
        'Value': 'sum',
        'Timestamp': 'last'
    }).reset_index()
    
    # Calculate portfolio value per month
    portfolio_monthly = asset_monthly.groupby('Month')['Value'].sum().reset_index()
    portfolio_monthly.columns = ['Month', 'Portfolio_Value']
    
    # Merge portfolio values with asset data
    asset_monthly = asset_monthly.merge(portfolio_monthly, on='Month')
    
    # Calculate asset weights
    asset_monthly['Weight'] = asset_monthly['Value'] / asset_monthly['Portfolio_Value']
    
    # Calculate asset returns
    asset_monthly = asset_monthly.sort_values(['Asset', 'Month'])
    asset_monthly['Asset_Return'] = asset_monthly.groupby('Asset')['Value'].pct_change()
    
    # Calculate rolling metrics for each asset
    asset_metrics = []
    
    for asset, group in asset_monthly.groupby('Asset'):
        group = group.sort_values('Month')
        
        # Calculate rolling volatility (12-month)
        group['Rolling_12M_Volatility'] = group['Asset_Return'].rolling(12).std() * np.sqrt(12)
        
        # Calculate rolling beta (12-month)
        group['Rolling_12M_Beta'] = calculate_asset_beta(group, asset_monthly)
        
        # Calculate weight changes
        group['Weight_Change'] = group['Weight'].diff()
        group['Weight_Change_3M'] = group['Weight'].diff(3)
        group['Weight_Change_12M'] = group['Weight'].diff(12)
        
        # Calculate volatility contribution
        group['Volatility_Contribution'] = group['Weight'] * group['Rolling_12M_Volatility']
        
        # Calculate return contribution
        group['Return_Contribution'] = group['Weight'] * group['Asset_Return']
        
        # Calculate Sharpe ratio for asset
        risk_free_rate = 0.02
        group['Asset_Excess_Return'] = group['Asset_Return'] - risk_free_rate/12
        group['Asset_Sharpe'] = (
            group['Asset_Excess_Return'].rolling(12).mean() / 
            group['Asset_Return'].rolling(12).std()
        ) * np.sqrt(12)
        
        # Calculate Sortino ratio for asset
        negative_returns = group['Asset_Return'].where(group['Asset_Return'] < 0, 0)
        group['Asset_Downside_Deviation'] = negative_returns.rolling(12).std() * np.sqrt(12)
        group['Asset_Sortino'] = (
            group['Asset_Excess_Return'].rolling(12).mean() / 
            group['Asset_Downside_Deviation']
        ) * np.sqrt(12)
        
        # Calculate maximum drawdown for asset
        group['Asset_Peak_Value'] = group['Value'].expanding().max()
        group['Asset_Drawdown'] = (group['Value'] - group['Asset_Peak_Value']) / group['Asset_Peak_Value']
        group['Asset_Max_Drawdown'] = group['Asset_Drawdown'].expanding().min()
        
        asset_metrics.append(group)
    
    if asset_metrics:
        result = pd.concat(asset_metrics, ignore_index=True)
        
        # Add month info
        result['Year'] = result['Month'].dt.year
        result['Month_Num'] = result['Month'].dt.month
        result['Month_Name'] = result['Month'].dt.strftime('%B')
        
        return result
    else:
        return pd.DataFrame()

def calculate_asset_beta(asset_group, portfolio_data):
    """
    Calculate beta for a specific asset against the portfolio.
    
    Args:
        asset_group (pd.DataFrame): Asset-specific data
        portfolio_data (pd.DataFrame): Portfolio-level data
        
    Returns:
        pd.Series: Beta values
    """
    if len(asset_group) < 2:
        return pd.Series([np.nan] * len(asset_group))
    
    # Calculate portfolio returns
    portfolio_returns = portfolio_data.groupby('Month')['Portfolio_Value'].sum().pct_change()
    
    # Merge with asset data
    asset_returns = asset_group[['Month', 'Asset_Return']].set_index('Month')
    portfolio_returns = portfolio_returns.reset_index()
    
    # Calculate rolling beta
    beta_values = []
    
    for i, row in asset_group.iterrows():
        month = row['Month']
        
        # Get historical data up to this month
        historical_asset = asset_group[asset_group['Month'] <= month]
        historical_portfolio = portfolio_returns[portfolio_returns['Month'] <= month]
        
        if len(historical_asset) >= 12 and len(historical_portfolio) >= 12:
            # Use last 12 months for beta calculation
            asset_returns_12m = historical_asset['Asset_Return'].tail(12)
            portfolio_returns_12m = historical_portfolio['Portfolio_Value'].tail(12)
            
            # Calculate covariance and variance
            covariance = np.cov(asset_returns_12m, portfolio_returns_12m)[0, 1]
            portfolio_variance = np.var(portfolio_returns_12m)
            
            if portfolio_variance > 0:
                beta = covariance / portfolio_variance
            else:
                beta = np.nan
        else:
            beta = np.nan
        
        beta_values.append(beta)
    
    return pd.Series(beta_values, index=asset_group.index)

def calculate_asset_concentration(df):
    """
    Calculate asset concentration metrics.
    
    Args:
        df (pd.DataFrame): Asset metrics DataFrame
        
    Returns:
        dict: Concentration metrics
    """
    if df is None or df.empty:
        return {}
    
    # Get latest month data
    latest_month = df['Month'].max()
    latest_data = df[df['Month'] == latest_month]
    
    if latest_data.empty:
        return {}
    
    # Calculate concentration metrics
    weights = latest_data['Weight'].dropna()
    
    concentration_metrics = {
        'total_assets': len(weights),
        'largest_position_weight': weights.max() if len(weights) > 0 else 0,
        'top_5_positions_weight': weights.nlargest(5).sum() if len(weights) >= 5 else weights.sum(),
        'top_10_positions_weight': weights.nlargest(10).sum() if len(weights) >= 10 else weights.sum(),
        'herfindahl_index': (weights ** 2).sum() if len(weights) > 0 else 0,
        'effective_number_of_assets': 1 / (weights ** 2).sum() if len(weights) > 0 else 0,
        'weighted_average_volatility': (weights * latest_data['Rolling_12M_Volatility']).sum() if len(weights) > 0 else 0
    }
    
    return concentration_metrics

def calculate_asset_correlation_matrix(df):
    """
    Calculate correlation matrix between assets.
    
    Args:
        df (pd.DataFrame): Asset metrics DataFrame
        
    Returns:
        pd.DataFrame: Correlation matrix
    """
    if df is None or df.empty:
        return pd.DataFrame()
    
    # Pivot data to get asset returns as columns
    returns_pivot = df.pivot_table(
        values='Asset_Return', 
        index='Month', 
        columns='Asset', 
        aggfunc='mean'
    )
    
    # Calculate correlation matrix
    correlation_matrix = returns_pivot.corr()
    
    return correlation_matrix

def calculate_asset_performance_ranking(df, metric='Asset_Return', periods=[1, 3, 6, 12]):
    """
    Calculate asset performance rankings over different periods.
    
    Args:
        df (pd.DataFrame): Asset metrics DataFrame
        metric (str): Metric to rank by
        periods (list): List of periods in months
        
    Returns:
        dict: Performance rankings
    """
    if df is None or df.empty:
        return {}
    
    rankings = {}
    
    for period in periods:
        # Calculate cumulative return over the period
        asset_performance = []
        
        for asset, group in df.groupby('Asset'):
            group = group.sort_values('Month')
            
            if len(group) >= period:
                # Calculate cumulative return over the period
                start_value = group['Value'].iloc[-period]
                end_value = group['Value'].iloc[-1]
                cumulative_return = (end_value - start_value) / start_value
                
                asset_performance.append({
                    'Asset': asset,
                    'Cumulative_Return': cumulative_return,
                    'Final_Weight': group['Weight'].iloc[-1],
                    'Final_Value': end_value
                })
        
        if asset_performance:
            performance_df = pd.DataFrame(asset_performance)
            performance_df = performance_df.sort_values('Cumulative_Return', ascending=False)
            performance_df['Rank'] = range(1, len(performance_df) + 1)
            
            rankings[f'{period}M'] = performance_df
    
    return rankings

def calculate_asset_risk_metrics(df):
    """
    Calculate comprehensive risk metrics for each asset.
    
    Args:
        df (pd.DataFrame): Asset metrics DataFrame
        
    Returns:
        pd.DataFrame: Asset risk metrics
    """
    if df is None or df.empty:
        return pd.DataFrame()
    
    risk_metrics = []
    
    for asset, group in df.groupby('Asset'):
        group = group.sort_values('Month')
        
        if len(group) < 12:
            continue
        
        # Calculate Value at Risk (VaR)
        returns = group['Asset_Return'].dropna()
        if len(returns) > 0:
            var_95 = np.percentile(returns, 5)
            var_99 = np.percentile(returns, 1)
            
            # Calculate Conditional VaR (CVaR)
            cvar_95 = returns[returns <= var_95].mean()
            cvar_99 = returns[returns <= var_99].mean()
        else:
            var_95 = var_99 = cvar_95 = cvar_99 = np.nan
        
        # Calculate downside deviation
        negative_returns = returns[returns < 0]
        downside_deviation = negative_returns.std() * np.sqrt(12) if len(negative_returns) > 0 else np.nan
        
        # Calculate maximum drawdown
        max_drawdown = group['Asset_Max_Drawdown'].min() if 'Asset_Max_Drawdown' in group.columns else np.nan
        
        # Calculate Calmar ratio
        avg_return = returns.mean() * 12 if len(returns) > 0 else np.nan
        calmar_ratio = avg_return / abs(max_drawdown) if max_drawdown != 0 and not pd.isna(max_drawdown) else np.nan
        
        risk_metrics.append({
            'Asset': asset,
            'VaR_95': var_95,
            'VaR_99': var_99,
            'CVaR_95': cvar_95,
            'CVaR_99': cvar_99,
            'Downside_Deviation': downside_deviation,
            'Max_Drawdown': max_drawdown,
            'Calmar_Ratio': calmar_ratio,
            'Volatility': group['Rolling_12M_Volatility'].iloc[-1] if 'Rolling_12M_Volatility' in group.columns else np.nan,
            'Sharpe_Ratio': group['Asset_Sharpe'].iloc[-1] if 'Asset_Sharpe' in group.columns else np.nan,
            'Sortino_Ratio': group['Asset_Sortino'].iloc[-1] if 'Asset_Sortino' in group.columns else np.nan
        })
    
    return pd.DataFrame(risk_metrics) 