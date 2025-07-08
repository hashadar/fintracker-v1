# Utility Modules

This directory contains general utility modules that support the main financial dashboard application.
For utilities specific to car equity tracking, please see [`utils/car/README.md`](car/README.md).

## Modules

### `data_loader.py`
Handles loading and preprocessing for the main financial dataset:
- Loads financial data from the primary Excel file (e.g., `202506_equity_hd.xlsx`).
- Converts timestamps to datetime format.
- Categorises assets based on predefined types (Cash, Investments, Pensions).
- Ensures data integrity, for instance, by handling potential duplicate entries for the same asset on the same date.
- Provides date range filtering functions for the main dataset.
- Handles saving updated data back to the primary Excel file.

### `metrics.py`
Calculates financial metrics and analytics for the main dataset:
- **Asset type-specific metrics**: Latest value, month-over-month change, platform counts, asset counts, months tracked
- **Overall portfolio metrics**: Total value, aggregate MoM/YTD changes, unique combinations count
- **Allocation metrics**: Percentage breakdown by asset type, allocation changes over time, MoM/YTD increases
- **Platform and asset breakdowns** within each asset type for detailed analysis

### `visualizations.py`
Creates reusable visual components and charts for the dashboard:
- **Card Components**: Four standardized card types for consistent metric display
  - `simple_card`: Basic metric with title, value, and optional caption
  - `emphasis_card`: Highlighted card for important metrics
  - `complex_card`: Metric with MoM and YTD change indicators
  - `complex_emphasis_card`: Emphasis card with change indicators
- **Chart Functions**: Plotly charts for time series, breakdowns, and data visualization
- **HTML Escaping**: Automatic HTML escaping for all user-facing text to prevent injection

### `design_tokens.py`
Defines the application's design system and styling constants:
- **Color Palette**: Brand colors, neutral colors, success/error states
- **Typography**: Font sizes, weights, line heights, letter spacing
- **Spacing**: Consistent spacing values for margins, padding, and layout
- **Card Styling**: Pre-built style functions for all card components
- **Responsive Design**: Breakpoints and responsive layout tokens

### `constants.py`
Defines application-wide constants and configurations:
- Predefined asset type categories (e.g., `ASSET_TYPES = ["Cash", "Investments", "Pensions"]`).
- Custom CSS styling for the Streamlit dashboard for a consistent look and feel.
- Default page configuration details like titles or shared descriptions.

## Card Component System

### Usage Guidelines

The card components provide a consistent way to display metrics across all dashboard pages:

```python
from utils import simple_card, complex_card, complex_emphasis_card

# For summary metrics without change tracking
simple_card("Maximum Drawdown", "£2,500", "Peak to trough decline")

# For metrics with change indicators
complex_card("Portfolio Total", "£50,000", "+2.5%", "+12.3%", "MoM | YTD")

# For most important metrics with emphasis
complex_emphasis_card("Total Assets", "£75,000", "+3.1%", "+15.2%", "MoM | YTD")
```

### Key Features

- **Automatic HTML Escaping**: All text inputs are automatically escaped to prevent HTML injection
- **Conditional Rendering**: Captions and change indicators only render when provided
- **Consistent Styling**: All cards use the same design tokens for consistent appearance
- **Responsive Design**: Cards adapt to different screen sizes automatically

## Design System

The application uses a centralized design system defined in `design_tokens.py`:

- **Colors**: Brand primary, secondary, success, error, and neutral color palettes
- **Typography**: Consistent font sizes from XS to 5XL with appropriate weights
- **Spacing**: Standardized spacing values (4px, 6px, 8px, etc.)
- **Layout**: Responsive breakpoints and layout tokens

### Style Functions

```python
from utils.design_tokens import get_card_base_styles, get_change_color

# Get pre-built styles for cards
base_styles = get_card_base_styles()
change_color = get_change_color("normal")  # Returns hex color for change indicators
```

## Usage

These modules are imported and used by the main application (`Home.py`) and the various page modules in the `pages/` directory. Each module provides specific, reusable functionality:

1. `data_loader.py` is used for initial loading, saving, and filtering of the main financial data.
2. `metrics.py` provides the calculation engine for financial metrics displayed on the dashboard.
3. `visualizations.py` supplies tools for creating consistent charts and card components.
4. `design_tokens.py` provides the design system and styling constants.
5. `constants.py` centralises shared configurations and static values.

## Data Flow Example (Main Data)

1. Data is loaded and preprocessed by `data_loader.load_data()`.
2. User interactions (e.g., date range selection) might trigger data refiltering via `data_loader` functions.
3. Relevant subsets of data are passed to page modules (e.g., `pages/cash.py`).
4. Page modules use `metrics.py` to calculate necessary financial figures for display.
5. `visualizations.py` is then used to generate charts and card components based on these metrics.
6. `design_tokens.py` provides consistent styling throughout this process.
7. `constants.py` provides underlying definitions (like asset types) used throughout the application.

## Best Practices

- **Use Card Components**: Always use the standardized card components for metric display
- **Follow Design System**: Use design tokens for colors, spacing, and typography
- **HTML Safety**: All user-facing text is automatically escaped, but be mindful of data sources
- **Performance**: Metrics are calculated on-demand and cached where appropriate
- **Consistency**: Follow the established patterns for data processing and visualization 