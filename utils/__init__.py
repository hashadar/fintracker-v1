"""Financial dashboard utility functions."""

from .etl.data_loader import load_data, filter_data_by_date_range, get_month_range
from .metrics import calculate_asset_type_metrics, calculate_allocation_metrics
from .charts import create_asset_type_time_series, create_asset_type_breakdown
from .design import simple_card, emphasis_card, complex_card, complex_emphasis_card, create_metric_grid, create_chart_grid, create_section_header, create_page_header
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
    # Utility functions
    get_change_color, get_emphasis_color, get_background_gradient, get_border_color,
    get_card_base_styles, get_emphasis_card_styles, get_card_title_styles,
    get_emphasis_card_title_styles, get_card_metric_styles, get_card_caption_styles,
    get_card_change_styles, get_emphasis_accent_bar
)

__all__ = [
    'load_data',
    'filter_data_by_date_range',
    'get_month_range',
    'calculate_asset_type_metrics',
    'calculate_allocation_metrics',
    'create_asset_type_time_series',
    'create_asset_type_breakdown',
    'create_metric_grid',
    'create_chart_grid',
    'create_section_header',
    'create_page_header',

    'simple_card',
    'emphasis_card',
    'complex_card',
    'complex_emphasis_card',
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
    'get_change_color', 'get_emphasis_color', 'get_background_gradient', 'get_border_color',
    'get_card_base_styles', 'get_emphasis_card_styles', 'get_card_title_styles',
    'get_emphasis_card_title_styles', 'get_card_metric_styles', 'get_card_caption_styles',
    'get_card_change_styles', 'get_emphasis_accent_bar'
] 