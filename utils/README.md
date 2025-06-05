# Utility Modules

This directory contains utility modules that support the main financial dashboard application.

## Modules

### data_loader.py
Handles data loading and preprocessing:
- Loads financial data from Excel files
- Converts timestamps to datetime format
- Categorises assets based on platform
- Ensures data integrity (one entry per platform-asset per month)
- Provides date range filtering functions

### metrics.py
Calculates financial metrics and analytics:
- Asset type-specific metrics (latest value, MoM change, platform counts)
- Overall portfolio metrics
- Allocation metrics (current position, MoM and YTD changes)
- Platform and asset breakdowns

### visualizations.py
Creates visual components and charts:
- Time series visualisations (line and area charts)
- Platform and asset breakdown charts
- KPI card component for metric display
- Asset type metric display formatting

### constants.py
Defines application-wide constants:
- Asset type mappings (platform categorisation)
- Custom styling for the dashboard
- Page configuration (title, description)

## Usage

These modules are imported and used by the main application (`app.py`). Each module provides specific functionality:

1. `data_loader.py` is used for initial data loading and filtering
2. `metrics.py` provides the calculations for all dashboard metrics
3. `visualizations.py` creates the visual components
4. `constants.py` provides shared configuration

## Data Flow

1. Data is loaded via `data_loader.py`
2. Metrics are calculated using `metrics.py`
3. Visualisations are created using `visualizations.py`
4. Constants from `constants.py` are used throughout the application 