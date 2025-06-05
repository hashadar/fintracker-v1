"""Constants used throughout the application."""

# Asset type mappings
ASSET_TYPES = {
    'Pensions': ['Wahed', 'Standard Life'],
    'Investments': ['Coinbase', 'IBKR'],
    'Cash': ['HSBC', 'Wise']
}

# Custom styling that works in both light and dark modes
CUSTOM_STYLE = """
    <style>
    .main {
        padding: 2rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.5rem;
        font-weight: bold;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 1rem;
        font-weight: normal;
    }
    div[data-testid="stMetricDelta"] {
        font-size: 1rem;
    }
    div[data-testid="stMetricContainer"] {
        background-color: var(--background-color);
        border: 1px solid var(--border-color);
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .asset-type-header {
        background-color: var(--background-color);
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border: 1px solid var(--border-color);
    }
    </style>
    """

# Page title and description
PAGE_TITLE = "Monthly Financial Position Dashboard"
PAGE_DESCRIPTION = "Monthly snapshot analysis of your financial positions" 