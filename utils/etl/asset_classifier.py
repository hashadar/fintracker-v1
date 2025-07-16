"""Asset classification functions for categorizing financial assets."""

import pandas as pd
import re
from ..config import ASSET_TYPES, ASSET_SUBTYPES

def get_asset_classification_rules():
    """Get the rules for classifying assets into different asset types."""
    
    # Define classification rules based primarily on asset names and patterns
    classification_rules = {
        ASSET_TYPES['CASH']: {
            'exact_matches': [
                'GBP', 'USD', 'EUR', 'Cash', 'Current Account', 'Savings Account',
                'Checking Account', 'Money Market', 'Liquid', 'Instant Access',
                'GBP Cash', 'USD Cash', 'EUR Cash', 'Pound Sterling', 'Dollar', 'Euro'
            ],
            'patterns': [
                r'\b(cash|currency|money|bank|account|savings|checking|liquid)\b',
                r'\b(gbp|usd|eur|pound|dollar|euro)\b',
                r'\b(current|instant access|money market)\b'
            ],
            'platforms': ['HSBC', 'Wise', 'Revolut', 'Monzo', 'Starling', 'Barclays', 'Santander']
        },
        ASSET_TYPES['PENSIONS']: {
            'exact_matches': [
                'Pension', 'SIPP', 'Retirement', '401k', 'IRA', 'Roth IRA',
                'Workplace Pension', 'Personal Pension', 'Defined Benefit',
                'Defined Contribution', 'Annuity', 'NEST', 'Auto Enrolment'
            ],
            'patterns': [
                r'\b(pension|retirement|sip|401k|ira|annuity)\b',
                r'\b(defined benefit|defined contribution|workplace pension)\b',
                r'\b(nest|auto enrolment|employer pension)\b'
            ],
            'platforms': ['Wahed', 'Standard Life', 'Aviva', 'Scottish Widows', 'Legal & General', 'NEST']
        },
        ASSET_TYPES['INVESTMENTS']: {
            'exact_matches': [
                'Stock', 'ETF', 'Mutual Fund', 'Bond', 'Crypto', 'Bitcoin', 'Ethereum',
                'Index Fund', 'Equity', 'Shares', 'Commodity', 'Real Estate', 'Property',
                'Gold', 'Silver', 'Oil', 'Gas', 'REIT', 'Investment Trust', 'Fund',
                'BTC', 'ETH', 'ADA', 'DOT', 'SOL', 'BNB', 'USDT', 'USDC'
            ],
            'patterns': [
                r'\b(stock|etf|fund|bond|crypto|bitcoin|ethereum|index|equity|share)\b',
                r'\b(commodity|real estate|property|gold|silver|oil|gas|reit)\b',
                r'\b(investment|trading|portfolio|asset|security)\b',
                r'\b(btc|eth|ada|dot|sol|bnb|usdt|usdc)\b'
            ],
            'platforms': ['Coinbase', 'IBKR', 'Trading212', 'Vanguard', 'Fidelity', 'Hargreaves Lansdown', 'AJ Bell']
        }
    }
    
    return classification_rules

def classify_asset_types(df):
    """
    Classify assets into Cash, Investments, Pensions based primarily on Asset column.
    Platform is used as secondary metadata for classification.
    
    Args:
        df (pd.DataFrame): DataFrame with 'Asset' and 'Platform' columns
        
    Returns:
        pd.DataFrame: DataFrame with added 'Asset_Type' column
    """
    if df is None or df.empty:
        return df
    
    df = df.copy()
    
    # Initialize Asset_Type column
    df['Asset_Type'] = ASSET_TYPES['OTHER']
    
    # Get classification rules
    rules = get_asset_classification_rules()
    
    # Classify based on Asset name patterns first (primary classification)
    for asset_type, rule_set in rules.items():
        # Check exact matches in Asset column
        if 'exact_matches' in rule_set:
            for exact_match in rule_set['exact_matches']:
                exact_mask = df['Asset'].str.contains(exact_match, case=False, na=False)
                df.loc[exact_mask, 'Asset_Type'] = asset_type
        
        # Check pattern matches in Asset column
        if 'patterns' in rule_set:
            for pattern in rule_set['patterns']:
                pattern_mask = df['Asset'].str.contains(pattern, case=False, na=False, regex=True)
                df.loc[pattern_mask, 'Asset_Type'] = asset_type
    
    # Use Platform as secondary classification for unclassified assets
    unclassified_mask = df['Asset_Type'] == ASSET_TYPES['OTHER']
    if unclassified_mask.any():
        for asset_type, rule_set in rules.items():
            if 'platforms' in rule_set:
                platform_mask = unclassified_mask & df['Platform'].isin(rule_set['platforms'])
                df.loc[platform_mask, 'Asset_Type'] = asset_type
    
    # Special handling for common asset patterns
    # Crypto assets
    crypto_patterns = [r'\b(btc|eth|ada|dot|sol|bnb|usdt|usdc)\b']
    for pattern in crypto_patterns:
        crypto_mask = df['Asset'].str.contains(pattern, case=False, na=False, regex=True)
        df.loc[crypto_mask, 'Asset_Type'] = ASSET_TYPES['INVESTMENTS']
    
    # Stock/ETF patterns
    stock_patterns = [r'\b(inc|corp|ltd|plc|co|company|stock|shares)\b']
    for pattern in stock_patterns:
        stock_mask = df['Asset'].str.contains(pattern, case=False, na=False, regex=True)
        df.loc[stock_mask, 'Asset_Type'] = ASSET_TYPES['INVESTMENTS']
    
    # Currency patterns
    currency_patterns = [r'\b(gbp|usd|eur|gbp|pound|dollar|euro)\b']
    for pattern in currency_patterns:
        currency_mask = df['Asset'].str.contains(pattern, case=False, na=False, regex=True)
        df.loc[currency_mask, 'Asset_Type'] = ASSET_TYPES['CASH']
    
    return df

def get_asset_type_summary(df):
    """
    Get a summary of asset type classifications.
    
    Args:
        df (pd.DataFrame): DataFrame with 'Asset_Type' column
        
    Returns:
        dict: Summary statistics for each asset type
    """
    if df is None or df.empty or 'Asset_Type' not in df.columns:
        return {}
    
    summary = {}
    
    # Count assets by type
    asset_type_counts = df['Asset_Type'].value_counts()
    
    # Value by asset type
    asset_type_values = df.groupby('Asset_Type')['Value'].sum()
    
    # Platform distribution by asset type
    platform_distribution = df.groupby(['Asset_Type', 'Platform'])['Value'].sum().unstack(fill_value=0)
    
    # Asset distribution by asset type
    asset_distribution = df.groupby(['Asset_Type', 'Asset'])['Value'].sum().unstack(fill_value=0)
    
    summary = {
        'counts': asset_type_counts.to_dict(),
        'values': asset_type_values.to_dict(),
        'platform_distribution': platform_distribution.to_dict(),
        'asset_distribution': asset_distribution.to_dict(),
        'total_assets': len(df),
        'total_value': df['Value'].sum(),
        'unique_platforms': df['Platform'].nunique(),
        'unique_assets': df['Asset'].nunique()
    }
    
    return summary

def validate_asset_classification(df):
    """
    Validate the asset classification and provide insights.
    
    Args:
        df (pd.DataFrame): DataFrame with 'Asset_Type' column
        
    Returns:
        dict: Validation results and recommendations
    """
    if df is None or df.empty:
        return {'error': 'No data provided'}
    
    validation_results = {
        'total_assets': len(df),
        'classified_assets': len(df[df['Asset_Type'] != ASSET_TYPES['OTHER']]),
        'unclassified_assets': len(df[df['Asset_Type'] == ASSET_TYPES['OTHER']]),
        'classification_rate': len(df[df['Asset_Type'] != ASSET_TYPES['OTHER']]) / len(df) * 100,
        'asset_type_distribution': df['Asset_Type'].value_counts().to_dict(),
        'unclassified_assets_list': df[df['Asset_Type'] == ASSET_TYPES['OTHER']][['Asset', 'Platform']].to_dict('records'),
        'recommendations': []
    }
    
    # Generate recommendations
    if validation_results['unclassified_assets'] > 0:
        validation_results['recommendations'].append(
            f"Review {validation_results['unclassified_assets']} unclassified assets"
        )
    
    if validation_results['classification_rate'] < 90:
        validation_results['recommendations'].append(
            "Consider adding more classification rules to improve coverage"
        )
    
    # Check for unusual classifications
    for asset_type in [ASSET_TYPES['CASH'], ASSET_TYPES['INVESTMENTS'], ASSET_TYPES['PENSIONS']]:
        if asset_type not in validation_results['asset_type_distribution']:
            validation_results['recommendations'].append(
                f"No assets classified as {asset_type} - verify classification rules"
            )
    
    return validation_results 