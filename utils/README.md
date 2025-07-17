# Utility Modules v1.2.0

This directory contains general utility modules that support the main financial dashboard application.

**All configuration, chart styling, and validation are now fully centralized and standardized.**

## Modules

### `etl/`
- `data_loader.py`: Loads and preprocesses financial data from Google Sheets
- `asset_classifier.py`: Classifies assets by type and platform

### `data_processing.py`
- Data processing utilities for filtering, aggregation, rolling metrics, drawdown, and performance calculations

### `charts/`
- `base.py`: Base chart functions (time series, bar, pie, area, etc.)
- `wrappers.py`: Chart wrapper functions for common patterns
- `formatting.py`: Axis and data formatting helpers
- `asset_types.py`: Asset-specific chart functions

### `design/`
- `cards.py`: Reusable card components
- `components.py`: Layout components
- `tokens.py`: Design tokens (colors, spacing, fonts, chart config)

### `config.py`
- Centralized configuration constants for asset types, business logic, formatting, and Google Sheets integration
- Includes automatic configuration validation

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

The application uses a centralized design system defined in `design/tokens.py`:

- **Colors**: Brand primary, secondary, success, error, and neutral color palettes
- **Typography**: Consistent font sizes from XS to 5XL with appropriate weights
- **Spacing**: Standardized spacing values (4px, 6px, 8px, etc.)
- **Layout**: Responsive breakpoints and layout tokens

### Style Functions

```python
from utils.design.tokens import get_card_base_styles, get_change_color

# Get pre-built styles for cards
base_styles = get_card_base_styles()
change_color = get_change_color("normal")  # Returns hex color for change indicators
```

## Usage

These modules are imported and used by the main application (`Home.py`) and the various page modules in the `pages/` directory. Each module provides specific, reusable functionality:

1. `etl/data_loader.py` is used for initial loading and filtering of the main financial data.
2. `etl/asset_classifier.py` classifies assets by type and platform.
3. `data_processing.py` provides the calculation engine for financial metrics and analytics.
4. `charts/` supplies tools for creating consistent charts and formatting.
5. `design/` provides the design system, card components, and layout utilities.
6. `config.py` centralizes all configuration and validation.

## Data Flow Example (Main Data)

1. Data is loaded and preprocessed by `data_loader.load_data()`.
2. User interactions (e.g., date range selection) might trigger data refiltering via `data_loader` functions.
3. Relevant subsets of data are passed to page modules (e.g., `pages/cash.py`).
4. Page modules use `data_processing.py` to calculate necessary financial figures for display.
5. `charts/` is then used to generate charts and card components based on these metrics.
6. `design/tokens.py` provides consistent styling throughout this process.
7. `config.py` provides underlying definitions (like asset types) and validation used throughout the application.

## Best Practices

- **Use Card Components**: Always use the standardized card components for metric display
- **Follow Design System**: Use design tokens for colors, spacing, and typography
- **HTML Safety**: All user-facing text is automatically escaped, but be mindful of data sources
- **Performance**: Metrics are calculated on-demand and cached where appropriate
- **Consistency**: Follow the established patterns for data processing and visualization 