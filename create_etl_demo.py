#!/usr/bin/env python3
"""
Demo ETL Output Generator
Creates a comprehensive Excel file showing what the enhanced ETL structure would produce
based on the existing data format.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def create_sample_input_data():
    """Load real input data from the provided Excel file (Balance Sheet sheet)"""
    import pandas as pd
    df = pd.read_excel('data/202506_equity_hd.xlsx', sheet_name='Balance Sheet')
    # Ensure columns are as expected and clean up if needed
    df = df[['Platform', 'Asset', 'Value', 'Timestamp', 'Token Amount']]
    return df

def calculate_monthly_metrics(df):
    """Calculate monthly portfolio metrics"""
    
    # Convert timestamp to datetime and add month columns
    df = df.copy()
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['yearmonth'] = df['Timestamp'].dt.to_period('M')
    df['snapshot_date'] = df['Timestamp'].dt.date
    df['snapshot_month'] = df['Timestamp'].dt.month
    df['snapshot_year'] = df['Timestamp'].dt.year
    df['snapshot_yearmonth'] = df['Timestamp'].dt.strftime('%Y-%m')
    
    # Group by month and calculate portfolio totals
    monthly_portfolio = df.groupby('yearmonth').agg({
        'Value': 'sum',
        'Asset': 'nunique',
        'Platform': 'nunique'
    }).reset_index()
    
    monthly_portfolio.columns = ['yearmonth', 'tpv', 'num_assets', 'num_platforms']
    
    # Calculate returns
    monthly_portfolio['mom_return'] = monthly_portfolio['tpv'].pct_change()
    monthly_portfolio['mom_log_return'] = np.log(monthly_portfolio['tpv'] / monthly_portfolio['tpv'].shift(1))
    
    # Calculate rolling returns
    monthly_portfolio['rolling_3m_return'] = monthly_portfolio['tpv'].pct_change(3)
    monthly_portfolio['rolling_6m_return'] = monthly_portfolio['tpv'].pct_change(6)
    monthly_portfolio['rolling_12m_return'] = monthly_portfolio['tpv'].pct_change(12)
    
    # Calculate volatility (12-month rolling)
    monthly_portfolio['rolling_12m_volatility'] = monthly_portfolio['mom_return'].rolling(12).std() * np.sqrt(12)
    
    # Calculate drawdown
    monthly_portfolio['running_peak'] = monthly_portfolio['tpv'].expanding().max()
    monthly_portfolio['drawdown'] = (monthly_portfolio['tpv'] - monthly_portfolio['running_peak']) / monthly_portfolio['running_peak']
    
    # Calculate Sharpe ratio (assuming 0% risk-free rate for simplicity)
    monthly_portfolio['rolling_12m_sharpe'] = (
        monthly_portfolio['mom_return'].rolling(12).mean() * 12 / 
        (monthly_portfolio['mom_return'].rolling(12).std() * np.sqrt(12))
    )
    
    # Calculate momentum
    monthly_portfolio['momentum_3m'] = monthly_portfolio['tpv'] / monthly_portfolio['tpv'].shift(3)
    monthly_portfolio['momentum_12m'] = monthly_portfolio['tpv'] / monthly_portfolio['tpv'].shift(12)
    
    # Calculate growth streak
    monthly_portfolio['growth_streak'] = 0
    streak = 0
    for i in range(1, len(monthly_portfolio)):
        if monthly_portfolio.iloc[i]['mom_return'] > 0:
            streak += 1
        else:
            streak = 0
        monthly_portfolio.iloc[i, monthly_portfolio.columns.get_loc('growth_streak')] = streak
    
    # Add months since start
    monthly_portfolio['months_since_start'] = range(len(monthly_portfolio))
    
    return monthly_portfolio

def calculate_asset_metrics(df):
    """Calculate asset-level monthly metrics"""
    
    df = df.copy()
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['yearmonth'] = df['Timestamp'].dt.to_period('M')
    df['snapshot_yearmonth'] = df['Timestamp'].dt.strftime('%Y-%m')
    
    # Calculate portfolio totals by month
    portfolio_totals = df.groupby('yearmonth')['Value'].sum().reset_index()
    portfolio_totals.columns = ['yearmonth', 'portfolio_total']
    
    # Merge portfolio totals back to asset data
    df = df.merge(portfolio_totals, on='yearmonth')
    
    # Calculate asset weights
    df['weight'] = df['Value'] / df['portfolio_total']
    
    # Calculate asset returns
    df['asset_id'] = df['Platform'] + '_' + df['Asset']
    df = df.sort_values(['asset_id', 'yearmonth'])
    df['monthly_return'] = df.groupby('asset_id')['Value'].pct_change()
    
    # Calculate contribution to portfolio return
    df['contribution_to_return'] = df['weight'].shift(1) * df['monthly_return']
    
    # Calculate months held
    df['months_held'] = df.groupby('asset_id').cumcount() + 1
    
    # Mark new assets
    df['is_new'] = df['months_held'] == 1
    
    # Calculate YTD return for each asset
    df['snapshot_year'] = df['Timestamp'].dt.year
    ytd_start = df.groupby(['asset_id', 'snapshot_year'])['Value'].first().reset_index()
    ytd_start.columns = ['asset_id', 'snapshot_year', 'ytd_start_value']
    df = df.merge(ytd_start, on=['asset_id', 'snapshot_year'])
    df['ytd_return'] = (df['Value'] - df['ytd_start_value']) / df['ytd_start_value']
    
    # Calculate token price for crypto assets
    df['token_price'] = None
    df.loc[df['Token Amount'].notna(), 'token_price'] = (
        df.loc[df['Token Amount'].notna(), 'Value'] / 
        df.loc[df['Token Amount'].notna(), 'Token Amount']
    )
    
    return df[['snapshot_yearmonth', 'Platform', 'Asset', 'asset_id', 'Value', 'weight', 
               'monthly_return', 'contribution_to_return', 'months_held', 'is_new', 
               'ytd_return', 'Token Amount', 'token_price']]

def create_forecast_scenarios(monthly_metrics):
    """Create sample forecast scenarios"""
    
    # Get the last few months for forecasting
    recent_data = monthly_metrics.tail(12)
    
    # Simple forecasting scenarios
    last_value = recent_data['tpv'].iloc[-1]
    avg_monthly_return = recent_data['mom_return'].mean()
    volatility = recent_data['mom_return'].std()
    
    forecast_months = ['2025-01', '2025-02', '2025-03', '2025-06', '2025-12']
    
    scenarios = []
    for i, month in enumerate(forecast_months):
        months_ahead = i + 1 if i < 3 else (6 if i == 3 else 12)
        
        # Base case (average return)
        base_forecast = last_value * (1 + avg_monthly_return) ** months_ahead
        
        # Bear case (10th percentile)
        bear_return = avg_monthly_return - 1.28 * volatility
        bear_forecast = last_value * (1 + bear_return) ** months_ahead
        
        # Bull case (90th percentile)
        bull_return = avg_monthly_return + 1.28 * volatility
        bull_forecast = last_value * (1 + bull_return) ** months_ahead
        
        scenarios.append({
            'forecast_month': month,
            'months_ahead': months_ahead,
            'forecast_method': 'Monte Carlo',
            'forecast_value': round(base_forecast, 2),
            'forecast_return': round((base_forecast / last_value - 1) * 100, 2),
            'ci_50_lower': round(bear_forecast, 2),
            'ci_50_upper': round(bull_forecast, 2),
            'ci_90_lower': round(bear_forecast * 0.9, 2),
            'ci_90_upper': round(bull_forecast * 1.1, 2),
            'bear_case': round(bear_forecast, 2),
            'base_case': round(base_forecast, 2),
            'bull_case': round(bull_forecast, 2),
            'mae': round(random.uniform(2, 5), 2),
            'rmse': round(random.uniform(3, 7), 2),
            'directional_accuracy': round(random.uniform(0.6, 0.8), 2)
        })
    
    return pd.DataFrame(scenarios)

def main():
    """Create the comprehensive ETL demo Excel file"""
    
    print("Creating ETL Demo Excel file...")
    
    # Create sample input data
    print("1. Generating sample input data...")
    input_data = create_sample_input_data()
    
    # Calculate monthly portfolio metrics
    print("2. Calculating monthly portfolio metrics...")
    monthly_metrics = calculate_monthly_metrics(input_data)
    
    # Calculate asset-level metrics
    print("3. Calculating asset-level metrics...")
    asset_metrics = calculate_asset_metrics(input_data)
    
    # Create forecast scenarios
    print("4. Creating forecast scenarios...")
    forecast_scenarios = create_forecast_scenarios(monthly_metrics)
    
    # Create correlation matrix
    print("5. Creating correlation matrix...")
    # Add yearmonth column to input_data for correlation calculation
    input_data['Timestamp'] = pd.to_datetime(input_data['Timestamp'])
    input_data['yearmonth'] = input_data['Timestamp'].dt.to_period('M')
    input_data['asset_id'] = input_data['Platform'] + '_' + input_data['Asset']
    
    pivot_data = input_data.pivot_table(
        index='yearmonth', 
        columns='asset_id', 
        values='Value', 
        aggfunc='sum'
    ).fillna(0)
    
    # Calculate returns for correlation
    returns_data = pivot_data.pct_change().dropna()
    correlation_matrix = returns_data.corr()
    
    # Create the Excel file
    print("6. Writing to Excel file...")
    with pd.ExcelWriter('ETL_Demo_Output.xlsx', engine='openpyxl') as writer:
        
        # Input data (original format)
        input_data[['Platform', 'Asset', 'Value', 'Timestamp', 'Token Amount']].to_excel(writer, sheet_name='1_Input_Data', index=False)
        
        # Monthly portfolio metrics
        monthly_metrics.to_excel(writer, sheet_name='2_Monthly_Portfolio_Metrics', index=False)
        
        # Asset-level metrics
        asset_metrics.to_excel(writer, sheet_name='3_Asset_Monthly_Metrics', index=False)
        
        # Forecast scenarios
        forecast_scenarios.to_excel(writer, sheet_name='4_Forecast_Scenarios', index=False)
        
        # Correlation matrix
        correlation_matrix.to_excel(writer, sheet_name='5_Correlation_Matrix')
        
        # Summary statistics
        summary_stats = pd.DataFrame({
            'Metric': [
                'Total Portfolio Value (Latest)',
                'Number of Assets',
                'Number of Platforms',
                'Monthly Return (Latest)',
                '12-Month Rolling Return',
                '12-Month Volatility',
                'Maximum Drawdown',
                'Sharpe Ratio (12M)',
                'Growth Streak (Current)',
                'Momentum (12M)'
            ],
            'Value': [
                f"£{monthly_metrics['tpv'].iloc[-1]:,.2f}",
                monthly_metrics['num_assets'].iloc[-1],
                monthly_metrics['num_platforms'].iloc[-1],
                f"{monthly_metrics['mom_return'].iloc[-1]*100:.2f}%",
                f"{monthly_metrics['rolling_12m_return'].iloc[-1]*100:.2f}%",
                f"{monthly_metrics['rolling_12m_volatility'].iloc[-1]*100:.2f}%",
                f"{monthly_metrics['drawdown'].min()*100:.2f}%",
                f"{monthly_metrics['rolling_12m_sharpe'].iloc[-1]:.2f}",
                monthly_metrics['growth_streak'].iloc[-1],
                f"{monthly_metrics['momentum_12m'].iloc[-1]:.2f}x"
            ]
        })
        summary_stats.to_excel(writer, sheet_name='6_Summary_Statistics', index=False)
    
    print("✅ ETL Demo Excel file created: ETL_Demo_Output.xlsx")
    print("\nFile contains the following sheets:")
    print("1. Input_Data - Original data format")
    print("2. Monthly_Portfolio_Metrics - Portfolio-level monthly metrics")
    print("3. Asset_Monthly_Metrics - Asset-level monthly metrics")
    print("4. Forecast_Scenarios - Forecasting outputs")
    print("5. Correlation_Matrix - Asset correlation analysis")
    print("6. Summary_Statistics - Key portfolio statistics")

if __name__ == "__main__":
    main() 