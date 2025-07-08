"""Metric calculation functions for the financial dashboard app."""

import pandas as pd

# --- Asset Type Metrics ---
def calculate_asset_type_metrics(df, asset_type):
    """Calculate summary metrics for a specific asset type (latest value, MoM change, platforms, assets, etc.)."""
    type_df = df[df['Asset_Type'] == asset_type]
    if type_df.empty:
        return None
    
    # Derive month from Timestamp for grouping
    type_df = type_df.copy()
    type_df['Month'] = type_df['Timestamp'].dt.to_period('M')
    
    # Get the latest and previous month's data for change calculations
    latest_month = type_df['Month'].max()
    prev_month = type_df[type_df['Month'] < latest_month]['Month'].max()
    
    # Calculate total value for latest and previous month
    latest_df = type_df[type_df['Month'] == latest_month]
    prev_df = type_df[type_df['Month'] == prev_month] if pd.notna(prev_month) else None
    latest_value = latest_df['Value'].sum()
    prev_value = prev_df['Value'].sum() if prev_df is not None else None
    
    # Calculate MoM percentage change (handles None values gracefully)
    mom_change = ((latest_value - prev_value) / prev_value * 100) if prev_value is not None else None
    
    metrics = {
        'latest_value': latest_value,
        'prev_value': prev_value,
        'mom_change': mom_change,
        'platforms': type_df['Platform'].nunique(),  # Count unique platforms
        'assets': type_df['Asset'].nunique() if 'Asset' in type_df.columns else 0,  # Count unique assets
        'months_tracked': len(type_df['Month'].unique()),  # Track data history length
        'latest_platform_breakdown': latest_df.groupby('Platform')['Value'].sum().to_dict()  # Platform allocation
    }
    return metrics

# --- Overall Metrics ---
def calculate_overall_metrics(df):
    """Calculate overall metrics for the dashboard (latest total, MoM change, etc.)."""
    df = df.copy()
    df['Month'] = df['Timestamp'].dt.to_period('M')
    
    # Get latest and previous month for portfolio-wide change calculations
    latest_month = df['Month'].max()
    prev_month = df[df['Month'] < latest_month]['Month'].max()
    
    latest_df = df[df['Month'] == latest_month]
    prev_df = df[df['Month'] == prev_month] if pd.notna(prev_month) else None
    
    # Calculate total portfolio values
    latest_total = latest_df['Value'].sum()
    prev_total = prev_df['Value'].sum() if prev_df is not None else None
    
    # Calculate MoM percentage change for entire portfolio
    mom_change = ((latest_total - prev_total) / prev_total * 100) if prev_total is not None else None
    
    return {
        'latest_total': latest_total,
        'mom_change': mom_change,
        'latest_month': latest_month,
        'unique_combinations': len(latest_df)  # Count of unique asset-platform combinations
    }

# --- Allocation, MoM, and YTD Metrics ---
def calculate_allocation_metrics(df):
    """Calculate current position, allocation, MoM and YTD changes for each asset type and total."""
    df = df.copy()
    df['Month'] = df['Timestamp'].dt.to_period('M')
    
    # Get key time periods for analysis
    latest_month = df['Month'].max()
    prev_month = df[df['Month'] < latest_month]['Month'].max()
    latest_year = latest_month.year
    ytd_start_month = df[df['Month'].dt.year == latest_year]['Month'].min()  # First month of current year
    
    # Filter data for each time period
    latest_df = df[df['Month'] == latest_month]
    prev_df = df[df['Month'] == prev_month] if pd.notna(prev_month) else None
    ytd_df = df[df['Month'] == ytd_start_month] if pd.notna(ytd_start_month) else None
    
    # Calculate total portfolio values for each period
    total_latest = latest_df['Value'].sum()
    total_prev = prev_df['Value'].sum() if prev_df is not None else None
    total_ytd = ytd_df['Value'].sum() if ytd_df is not None else None
    
    # Process each asset type
    asset_types = latest_df['Asset_Type'].unique()
    metrics = {}
    for asset_type in asset_types:
        # Get values for each time period
        latest_val = latest_df[latest_df['Asset_Type'] == asset_type]['Value'].sum()
        prev_val = prev_df[prev_df['Asset_Type'] == asset_type]['Value'].sum() if prev_df is not None else 0
        ytd_val = ytd_df[ytd_df['Asset_Type'] == asset_type]['Value'].sum() if ytd_df is not None else 0
        
        # Calculate allocation percentages (what % of portfolio this asset type represents)
        allocation = (latest_val / total_latest * 100) if total_latest else 0
        prev_allocation = (prev_val / total_prev * 100) if total_prev else 0
        ytd_allocation = (ytd_val / total_ytd * 100) if total_ytd else 0
        
        # Calculate absolute and percentage changes
        mom_increase = latest_val - prev_val
        mom_pct_increase = ((mom_increase / prev_val) * 100) if prev_val else None
        ytd_increase = latest_val - ytd_val
        ytd_pct_increase = ((ytd_increase / ytd_val) * 100) if ytd_val else None
        
        # Calculate allocation changes (how portfolio mix has shifted)
        allocation_change = allocation - prev_allocation if prev_allocation else None
        ytd_allocation_change = allocation - ytd_allocation if ytd_allocation else None
        
        metrics[asset_type] = {
            'current': latest_val,
            'allocation': allocation,
            'mom_increase': mom_increase,
            'mom_pct_increase': mom_pct_increase,
            'allocation_change': allocation_change,
            'ytd_increase': ytd_increase,
            'ytd_pct_increase': ytd_pct_increase,
            'ytd_allocation_change': ytd_allocation_change
        }
    
    # Calculate grand total metrics for the entire portfolio
    total_mom_increase = total_latest - total_prev if total_prev is not None else None
    total_mom_pct_increase = ((total_mom_increase / total_prev) * 100) if total_prev else None
    total_ytd_increase = total_latest - total_ytd if total_ytd is not None else None
    total_ytd_pct_increase = ((total_ytd_increase / total_ytd) * 100) if total_ytd else None
    
    metrics['Total'] = {
        'current': total_latest,
        'mom_increase': total_mom_increase,
        'mom_pct_increase': total_mom_pct_increase,
        'ytd_increase': total_ytd_increase,
        'ytd_pct_increase': total_ytd_pct_increase
    }
    return metrics, latest_month, prev_month, ytd_start_month 