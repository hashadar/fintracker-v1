"""Utility modules for the financial dashboard app."""

from .etl.data_loader import load_data, load_pension_cashflows, filter_data_by_date_range, get_month_range
from .etl.asset_classifier import classify_asset_types, get_asset_classification_rules
from .config import (
    ASSET_TYPES, ASSET_SUBTYPES, DATE_FORMAT, DISPLAY_DATE_FORMAT, SHORT_DATE_FORMAT, CURRENCY_FORMAT, PERCENTAGE_FORMAT,
    RISK_FREE_RATE, DEFAULT_FORECAST_PERIODS, DEFAULT_ROLLING_WINDOW, PAGE_TITLE, PAGE_ICON, 
    LAYOUT, INITIAL_SIDEBAR_STATE, MIN_DATA_POINTS_FOR_FORECAST, SEASONAL_PERIODS, CONFIDENCE_LEVEL, 
    SHEET_NAME, DATE_COLUMN, AMOUNT_COLUMN, CATEGORY_COLUMN, DESCRIPTION_COLUMN, VOLATILITY_WINDOW, 
    VAR_CONFIDENCE_LEVEL, MAX_DRAWDOWN_WINDOW, BENCHMARK_RETURN, INFLATION_RATE, validate_config,
    PENSION_CASHFLOW_SHEET, CASHFLOW_TYPE_COLUMN, NOTES_COLUMN, CASHFLOW_TYPES, CASHFLOW_DESCRIPTIONS
)
from .data_processing import (
    filter_by_asset_type,
    get_latest_month_data,
    get_monthly_aggregation,
    calculate_rolling_metrics,
    get_asset_breakdown,
    calculate_asset_type_metrics,
    calculate_allocation_metrics,
    create_allocation_time_series,
    get_asset_type_time_periods,
    create_platform_trends_data,
    create_platform_allocation_time_series,
    calculate_actual_pension_returns,
    get_cumulative_pension_cashflows,
    calculate_actual_mom_changes,
    forecast_pension_growth
)
from .charts import create_asset_type_time_series, create_asset_type_breakdown
from .design import simple_card, emphasis_card, complex_card, complex_emphasis_card, create_metric_grid, create_chart_grid, create_section_header, create_page_header, create_pension_asset_analysis, create_pension_forecast_section
from .design.tokens import (
    # Color tokens
    BRAND_PRIMARY, BRAND_SECONDARY, BRAND_SUCCESS, BRAND_WARNING, BRAND_ERROR, BRAND_INFO,
    NEUTRAL_50, NEUTRAL_100, NEUTRAL_200, NEUTRAL_300, NEUTRAL_400, NEUTRAL_500,
    NEUTRAL_600, NEUTRAL_700, NEUTRAL_800, NEUTRAL_900,
    BACKGROUND_PRIMARY, BACKGROUND_SECONDARY, BACKGROUND_TERTIARY,
    BORDER_PRIMARY, BORDER_SECONDARY,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_TERTIARY, TEXT_MUTED, TEXT_INVERSE,
    # Typography tokens
    FONT_SIZE_XS, FONT_SIZE_SM, FONT_SIZE_BASE, FONT_SIZE_LG, FONT_SIZE_XL,
    FONT_SIZE_2XL, FONT_SIZE_3XL, FONT_SIZE_4XL, FONT_SIZE_5XL,
    FONT_WEIGHT_NORMAL, FONT_WEIGHT_MEDIUM, FONT_WEIGHT_SEMIBOLD, FONT_WEIGHT_BOLD, FONT_WEIGHT_EXTRABOLD,
    LINE_HEIGHT_TIGHT, LINE_HEIGHT_NORMAL, LINE_HEIGHT_RELAXED,
    LETTER_SPACING_TIGHT, LETTER_SPACING_NORMAL, LETTER_SPACING_WIDE, LETTER_SPACING_WIDER, LETTER_SPACING_WIDEST,
    # Spacing tokens
    SPACE_1, SPACE_2, SPACE_3, SPACE_4, SPACE_5, SPACE_6, SPACE_8, SPACE_10, SPACE_12, SPACE_16, SPACE_20,
    # Border radius tokens
    BORDER_RADIUS_SM, BORDER_RADIUS_MD, BORDER_RADIUS_LG, BORDER_RADIUS_XL, BORDER_RADIUS_2XL, BORDER_RADIUS_FULL,
    # Shadow tokens
    SHADOW_SM, SHADOW_MD, SHADOW_LG, SHADOW_XL, SHADOW_2XL,
    # Transition tokens
    TRANSITION_FAST, TRANSITION_NORMAL, TRANSITION_SLOW,
    # Chart configuration tokens
    CHART_TEMPLATE, CHART_FONT_FAMILY, CHART_FONT_SIZE, CHART_HEIGHT, CHART_MARGIN,
    CHART_GRID_COLOR, CHART_AXIS_LINE_COLOR, CHART_AXIS_LINE_WIDTH, CHART_GRID_WIDTH,
    CHART_PLOT_BGCOLOR, CHART_PAPER_BGCOLOR, CHART_COLORS,
    # Utility functions
    get_change_color, get_emphasis_color, get_background_gradient, get_border_color,
    get_card_base_styles, get_emphasis_card_styles, get_card_title_styles,
    get_emphasis_card_title_styles, get_card_metric_styles, get_card_caption_styles,
    get_card_change_styles, get_emphasis_accent_bar
)

__all__ = [
    # Configuration constants
    'ASSET_TYPES', 'ASSET_SUBTYPES', 'DATE_FORMAT', 'DISPLAY_DATE_FORMAT', 'SHORT_DATE_FORMAT', 'CURRENCY_FORMAT', 'PERCENTAGE_FORMAT',
    'RISK_FREE_RATE', 'DEFAULT_FORECAST_PERIODS', 'DEFAULT_ROLLING_WINDOW', 'PAGE_TITLE', 'PAGE_ICON', 
    'LAYOUT', 'INITIAL_SIDEBAR_STATE', 'MIN_DATA_POINTS_FOR_FORECAST', 'SEASONAL_PERIODS', 'CONFIDENCE_LEVEL', 
    'SHEET_NAME', 'DATE_COLUMN', 'AMOUNT_COLUMN', 'CATEGORY_COLUMN', 'DESCRIPTION_COLUMN', 'VOLATILITY_WINDOW', 
    'VAR_CONFIDENCE_LEVEL', 'MAX_DRAWDOWN_WINDOW', 'BENCHMARK_RETURN', 'INFLATION_RATE', 'validate_config',
    'PENSION_CASHFLOW_SHEET', 'CASHFLOW_TYPE_COLUMN', 'NOTES_COLUMN', 'CASHFLOW_TYPES', 'CASHFLOW_DESCRIPTIONS',
    
    # ETL functions (core data loading and transformation)
    'load_data',
    'load_pension_cashflows',
    'filter_data_by_date_range',
    'get_month_range',
    'classify_asset_types',
    'get_asset_classification_rules',
    
    # Data processing functions
    'filter_by_asset_type',
    'get_latest_month_data',
    'get_monthly_aggregation',
    'calculate_rolling_metrics',
    'get_asset_breakdown',
    'calculate_asset_type_metrics',
    'calculate_allocation_metrics',
    'create_allocation_time_series',
    'get_asset_type_time_periods',
    'create_platform_trends_data',
    'create_platform_allocation_time_series',
    # Pension cashflow analytics
    'calculate_actual_pension_returns',
    'get_cumulative_pension_cashflows',
    'calculate_actual_mom_changes',
    'forecast_pension_growth',

    # Chart functions
    'create_asset_type_time_series',
    'create_asset_type_breakdown',

    # Design functions
    'simple_card',
    'emphasis_card',
    'complex_card',
    'complex_emphasis_card',
    'create_metric_grid',
    'create_chart_grid',
    'create_section_header',
    'create_page_header',
    'create_pension_asset_analysis',
    'create_pension_forecast_section',

    # Design tokens
    'BRAND_PRIMARY', 'BRAND_SECONDARY', 'BRAND_SUCCESS', 'BRAND_WARNING', 'BRAND_ERROR', 'BRAND_INFO',
    'NEUTRAL_50', 'NEUTRAL_100', 'NEUTRAL_200', 'NEUTRAL_300', 'NEUTRAL_400', 'NEUTRAL_500',
    'NEUTRAL_600', 'NEUTRAL_700', 'NEUTRAL_800', 'NEUTRAL_900',
    'BACKGROUND_PRIMARY', 'BACKGROUND_SECONDARY', 'BACKGROUND_TERTIARY',
    'BORDER_PRIMARY', 'BORDER_SECONDARY',
    'TEXT_PRIMARY', 'TEXT_SECONDARY', 'TEXT_TERTIARY', 'TEXT_MUTED', 'TEXT_INVERSE',
    'FONT_SIZE_XS', 'FONT_SIZE_SM', 'FONT_SIZE_BASE', 'FONT_SIZE_LG', 'FONT_SIZE_XL',
    'FONT_SIZE_2XL', 'FONT_SIZE_3XL', 'FONT_SIZE_4XL', 'FONT_SIZE_5XL',
    'FONT_WEIGHT_NORMAL', 'FONT_WEIGHT_MEDIUM', 'FONT_WEIGHT_SEMIBOLD', 'FONT_WEIGHT_BOLD', 'FONT_WEIGHT_EXTRABOLD',
    'LINE_HEIGHT_TIGHT', 'LINE_HEIGHT_NORMAL', 'LINE_HEIGHT_RELAXED',
    'LETTER_SPACING_TIGHT', 'LETTER_SPACING_NORMAL', 'LETTER_SPACING_WIDE', 'LETTER_SPACING_WIDER', 'LETTER_SPACING_WIDEST',
    'SPACE_1', 'SPACE_2', 'SPACE_3', 'SPACE_4', 'SPACE_5', 'SPACE_6', 'SPACE_8', 'SPACE_10', 'SPACE_12', 'SPACE_16', 'SPACE_20',
    'BORDER_RADIUS_SM', 'BORDER_RADIUS_MD', 'BORDER_RADIUS_LG', 'BORDER_RADIUS_XL', 'BORDER_RADIUS_2XL', 'BORDER_RADIUS_FULL',
    'SHADOW_SM', 'SHADOW_MD', 'SHADOW_LG', 'SHADOW_XL', 'SHADOW_2XL',
    'TRANSITION_FAST', 'TRANSITION_NORMAL', 'TRANSITION_SLOW',
    # Chart configuration tokens
    'CHART_TEMPLATE', 'CHART_FONT_FAMILY', 'CHART_FONT_SIZE', 'CHART_HEIGHT', 'CHART_MARGIN',
    'CHART_GRID_COLOR', 'CHART_AXIS_LINE_COLOR', 'CHART_AXIS_LINE_WIDTH', 'CHART_GRID_WIDTH',
    'CHART_PLOT_BGCOLOR', 'CHART_PAPER_BGCOLOR', 'CHART_COLORS',
    'get_change_color', 'get_emphasis_color', 'get_background_gradient', 'get_border_color',
    'get_card_base_styles', 'get_emphasis_card_styles', 'get_card_title_styles',
    'get_emphasis_card_title_styles', 'get_card_metric_styles', 'get_card_caption_styles',
    'get_card_change_styles', 'get_emphasis_accent_bar'
]

# Validate configuration on module import
try:
    validation_result = validate_config()
    if not validation_result['valid']:
        import warnings
        warnings.warn(f"Configuration validation failed: {validation_result['errors']}")
    if validation_result['warnings']:
        import warnings
        for warning in validation_result['warnings']:
            warnings.warn(f"Configuration warning: {warning}")
except Exception as e:
    import warnings
    warnings.warn(f"Configuration validation error: {str(e)}") 