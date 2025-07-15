"""
Design tokens for the financial dashboard app.
Single source of truth for colors, spacing, typography, and other design variables.
"""

# =============================================================================
# COLOR TOKENS
# =============================================================================

# Brand Colors
BRAND_PRIMARY = "#3b82f6"      # Blue
BRAND_SECONDARY = "#8b5cf6"    # Purple
BRAND_SUCCESS = "#10b981"      # Green
BRAND_WARNING = "#f59e0b"      # Amber
BRAND_ERROR = "#ef4444"        # Red
BRAND_INFO = "#06b6d4"         # Cyan

# Neutral Colors
NEUTRAL_50 = "#f9fafb"
NEUTRAL_100 = "#f3f4f6"
NEUTRAL_200 = "#e5e7eb"
NEUTRAL_300 = "#d1d5db"
NEUTRAL_400 = "#9ca3af"
NEUTRAL_500 = "#6b7280"
NEUTRAL_600 = "#4b5563"
NEUTRAL_700 = "#374151"
NEUTRAL_800 = "#1f2937"
NEUTRAL_900 = "#111827"

# Semantic Colors
SUCCESS_LIGHT = "#d1fae5"
SUCCESS_DARK = "#065f46"
WARNING_LIGHT = "#fef3c7"
WARNING_DARK = "#92400e"
ERROR_LIGHT = "#fee2e2"
ERROR_DARK = "#991b1b"
INFO_LIGHT = "#cffafe"
INFO_DARK = "#0e7490"

# Background Colors
BACKGROUND_PRIMARY = "#ffffff"
BACKGROUND_SECONDARY = NEUTRAL_50
BACKGROUND_TERTIARY = NEUTRAL_100
BACKGROUND_EMPHASIS = f"{BRAND_PRIMARY}15"  # 15% opacity

# Border Colors
BORDER_PRIMARY = NEUTRAL_200
BORDER_SECONDARY = NEUTRAL_300
BORDER_EMPHASIS = f"{BRAND_PRIMARY}30"  # 30% opacity

# Text Colors
TEXT_PRIMARY = NEUTRAL_800
TEXT_SECONDARY = NEUTRAL_600
TEXT_TERTIARY = NEUTRAL_500
TEXT_MUTED = NEUTRAL_400
TEXT_INVERSE = NEUTRAL_50

# Shadow Colors
SHADOW_LIGHT = "rgba(0, 0, 0, 0.08)"
SHADOW_MEDIUM = "rgba(0, 0, 0, 0.12)"
SHADOW_HEAVY = "rgba(0, 0, 0, 0.16)"
SHADOW_EMPHASIS = f"rgba(59, 130, 246, 0.15)"  # Brand primary with opacity

# =============================================================================
# TYPOGRAPHY TOKENS
# =============================================================================

# Font Sizes
FONT_SIZE_XS = "0.75rem"      # 12px
FONT_SIZE_SM = "0.875rem"     # 14px
FONT_SIZE_BASE = "1rem"       # 16px
FONT_SIZE_LG = "1.125rem"     # 18px
FONT_SIZE_XL = "1.25rem"      # 20px
FONT_SIZE_2XL = "1.5rem"      # 24px
FONT_SIZE_3XL = "1.875rem"    # 30px
FONT_SIZE_4XL = "2.25rem"     # 36px
FONT_SIZE_5XL = "3rem"        # 48px

# Font Weights
FONT_WEIGHT_NORMAL = "400"
FONT_WEIGHT_MEDIUM = "500"
FONT_WEIGHT_SEMIBOLD = "600"
FONT_WEIGHT_BOLD = "700"
FONT_WEIGHT_EXTRABOLD = "800"

# Line Heights
LINE_HEIGHT_TIGHT = "1.2"
LINE_HEIGHT_NORMAL = "1.5"
LINE_HEIGHT_RELAXED = "1.75"

# Letter Spacing
LETTER_SPACING_TIGHT = "-0.025em"
LETTER_SPACING_NORMAL = "0em"
LETTER_SPACING_WIDE = "0.025em"
LETTER_SPACING_WIDER = "0.05em"
LETTER_SPACING_WIDEST = "0.1em"

# =============================================================================
# SPACING TOKENS
# =============================================================================

# Base spacing unit (4px)
SPACE_1 = "0.25rem"   # 4px
SPACE_2 = "0.5rem"    # 8px
SPACE_3 = "0.75rem"   # 12px
SPACE_4 = "1rem"      # 16px
SPACE_5 = "1.25rem"   # 20px
SPACE_6 = "1.5rem"    # 24px
SPACE_8 = "2rem"      # 32px
SPACE_10 = "2.5rem"   # 40px
SPACE_12 = "3rem"     # 48px
SPACE_16 = "4rem"     # 64px
SPACE_20 = "5rem"     # 80px

# =============================================================================
# BORDER RADIUS TOKENS
# =============================================================================

BORDER_RADIUS_SM = "0.25rem"   # 4px
BORDER_RADIUS_MD = "0.375rem"  # 6px
BORDER_RADIUS_LG = "0.5rem"    # 8px
BORDER_RADIUS_XL = "0.75rem"   # 12px
BORDER_RADIUS_2XL = "1rem"     # 16px
BORDER_RADIUS_FULL = "9999px"

# =============================================================================
# SHADOW TOKENS
# =============================================================================

SHADOW_SM = f"0 1px 2px 0 {SHADOW_LIGHT}"
SHADOW_MD = f"0 4px 6px -1px {SHADOW_LIGHT}, 0 2px 4px -1px {SHADOW_LIGHT}"
SHADOW_LG = f"0 10px 15px -3px {SHADOW_LIGHT}, 0 4px 6px -2px {SHADOW_LIGHT}"
SHADOW_XL = f"0 20px 25px -5px {SHADOW_LIGHT}, 0 10px 10px -5px {SHADOW_LIGHT}"
SHADOW_2XL = f"0 25px 50px -12px {SHADOW_LIGHT}"

# =============================================================================
# TRANSITION TOKENS
# =============================================================================

TRANSITION_FAST = "0.15s ease"
TRANSITION_NORMAL = "0.2s ease"
TRANSITION_SLOW = "0.3s ease"

# =============================================================================
# Z-INDEX TOKENS
# =============================================================================

Z_INDEX_DROPDOWN = "1000"
Z_INDEX_STICKY = "1020"
Z_INDEX_FIXED = "1030"
Z_INDEX_MODAL_BACKDROP = "1040"
Z_INDEX_MODAL = "1050"
Z_INDEX_POPOVER = "1060"
Z_INDEX_TOOLTIP = "1070"

# =============================================================================
# CHART CONFIGURATION TOKENS
# =============================================================================

# Chart Template
CHART_TEMPLATE = "plotly_white"

# Chart Typography
CHART_FONT_FAMILY = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
CHART_FONT_SIZE = 12

# Chart Dimensions
CHART_HEIGHT = 400
CHART_MARGIN = dict(l=50, r=50, t=50, b=50)

# Chart Colors
CHART_GRID_COLOR = NEUTRAL_200
CHART_AXIS_LINE_COLOR = NEUTRAL_300
CHART_AXIS_LINE_WIDTH = 1
CHART_GRID_WIDTH = 1

# Chart Background
CHART_PLOT_BGCOLOR = 'rgba(0,0,0,0)'
CHART_PAPER_BGCOLOR = 'rgba(0,0,0,0)'

# =============================================================================
# CARD SPECIFIC TOKENS
# =============================================================================

# Card Padding
CARD_PADDING_SM = SPACE_4
CARD_PADDING_MD = SPACE_6
CARD_PADDING_LG = SPACE_8

# Card Border Width
CARD_BORDER_WIDTH_NORMAL = "1px"
CARD_BORDER_WIDTH_EMPHASIS = "2px"

# Card Title Styles
CARD_TITLE_FONT_SIZE = FONT_SIZE_SM
CARD_TITLE_FONT_WEIGHT = FONT_WEIGHT_MEDIUM
CARD_TITLE_COLOR = TEXT_SECONDARY
CARD_TITLE_LETTER_SPACING = LETTER_SPACING_WIDER
CARD_TITLE_TEXT_TRANSFORM = "uppercase"

# Card Metric Styles
CARD_METRIC_FONT_SIZE_SIMPLE = FONT_SIZE_4XL
CARD_METRIC_FONT_SIZE_EMPHASIS = FONT_SIZE_5XL
CARD_METRIC_FONT_WEIGHT = FONT_WEIGHT_BOLD
CARD_METRIC_COLOR = TEXT_PRIMARY
CARD_METRIC_LINE_HEIGHT = LINE_HEIGHT_TIGHT

# Card Caption Styles
CARD_CAPTION_FONT_SIZE = FONT_SIZE_XS
CARD_CAPTION_COLOR = TEXT_TERTIARY
CARD_CAPTION_MARGIN_TOP = SPACE_3

# Card Change Styles
CARD_CHANGE_FONT_SIZE = FONT_SIZE_SM
CARD_CHANGE_FONT_WEIGHT = FONT_WEIGHT_SEMIBOLD
CARD_CHANGE_MARGIN_TOP = SPACE_3

# =============================================================================
# COLOR UTILITY FUNCTIONS
# =============================================================================

def get_change_color(color_type: str) -> str:
    """
    Get the appropriate color for change indicators.
    
    Args:
        color_type (str): Type of color change ("normal", "inverse")
    
    Returns:
        str: CSS color value
    """
    if color_type == "normal":
        return BRAND_SUCCESS
    elif color_type == "inverse":
        return BRAND_ERROR
    else:
        return NEUTRAL_500

def get_emphasis_color(color_name: str = "primary") -> str:
    """
    Get emphasis color based on name.
    
    Args:
        color_name (str): Color name ("primary", "success", "warning", "error", "info")
    
    Returns:
        str: CSS color value
    """
    color_map = {
        "primary": BRAND_PRIMARY,
        "success": BRAND_SUCCESS,
        "warning": BRAND_WARNING,
        "error": BRAND_ERROR,
        "info": BRAND_INFO
    }
    return color_map.get(color_name, BRAND_PRIMARY)

def get_background_gradient(color: str, opacity_start: str = "15", opacity_end: str = "08") -> str:
    """
    Create a background gradient string.
    
    Args:
        color (str): Base color
        opacity_start (str): Starting opacity percentage
        opacity_end (str): Ending opacity percentage
    
    Returns:
        str: CSS gradient string
    """
    return f"linear-gradient(135deg, {color}{opacity_start} 0%, {color}{opacity_end} 100%)"

def get_border_color(color: str, opacity: str = "30") -> str:
    """
    Create a border color with opacity.
    
    Args:
        color (str): Base color
        opacity (str): Opacity percentage
    
    Returns:
        str: CSS color with opacity
    """
    return f"{color}{opacity}"

# =============================================================================
# CARD STYLE UTILITY FUNCTIONS
# =============================================================================

def get_card_base_styles() -> str:
    """Get base card styles."""
    return f"background: {BACKGROUND_PRIMARY}; border: {CARD_BORDER_WIDTH_NORMAL} solid {BORDER_PRIMARY}; border-radius: {BORDER_RADIUS_LG}; padding: {CARD_PADDING_MD}; box-shadow: {SHADOW_SM}; transition: {TRANSITION_NORMAL}; min-height: 120px; display: flex; flex-direction: column; justify-content: center;"

def get_emphasis_card_styles(emphasis_color: str = BRAND_PRIMARY) -> str:
    """Get emphasis card styles."""
    return f"background: {BACKGROUND_PRIMARY}; border: {CARD_BORDER_WIDTH_EMPHASIS} solid {emphasis_color}; border-radius: {BORDER_RADIUS_LG}; padding: {CARD_PADDING_MD}; box-shadow: {SHADOW_MD}; transition: {TRANSITION_NORMAL}; position: relative; min-height: 140px; display: flex; flex-direction: column; justify-content: center;"

def get_card_title_styles() -> str:
    """Get card title styles."""
    return f"font-size: {CARD_TITLE_FONT_SIZE}; font-weight: {CARD_TITLE_FONT_WEIGHT}; color: {CARD_TITLE_COLOR}; letter-spacing: {CARD_TITLE_LETTER_SPACING}; text-transform: {CARD_TITLE_TEXT_TRANSFORM}; margin-bottom: {SPACE_3}; line-height: {LINE_HEIGHT_TIGHT};"

def get_emphasis_card_title_styles(emphasis_color: str = BRAND_PRIMARY) -> str:
    """Get emphasis card title styles."""
    return f"font-size: {CARD_TITLE_FONT_SIZE}; font-weight: {CARD_TITLE_FONT_WEIGHT}; color: {emphasis_color}; letter-spacing: {CARD_TITLE_LETTER_SPACING}; text-transform: {CARD_TITLE_TEXT_TRANSFORM}; margin-bottom: {SPACE_3}; line-height: {LINE_HEIGHT_TIGHT};"

def get_card_metric_styles(font_size: str = CARD_METRIC_FONT_SIZE_SIMPLE) -> str:
    """Get card metric styles."""
    return f"font-size: {font_size}; font-weight: {CARD_METRIC_FONT_WEIGHT}; color: {CARD_METRIC_COLOR}; line-height: {CARD_METRIC_LINE_HEIGHT}; margin-bottom: {SPACE_3};"

def get_card_caption_styles() -> str:
    """Get card caption styles."""
    return f"font-size: {CARD_CAPTION_FONT_SIZE}; color: {CARD_CAPTION_COLOR}; margin-top: {CARD_CAPTION_MARGIN_TOP}; line-height: {LINE_HEIGHT_TIGHT};"

def get_card_change_styles() -> str:
    """Get card change styles."""
    return f"font-size: {CARD_CHANGE_FONT_SIZE}; font-weight: {CARD_CHANGE_FONT_WEIGHT}; margin-top: {CARD_CHANGE_MARGIN_TOP}; line-height: {LINE_HEIGHT_TIGHT};"

def get_emphasis_accent_bar(emphasis_color: str = BRAND_PRIMARY) -> str:
    """Get emphasis accent bar styles."""
    return f"position: absolute; top: 0; left: 0; right: 0; height: 4px; background: {emphasis_color}; border-radius: {BORDER_RADIUS_LG} {BORDER_RADIUS_LG} 0 0;"

# =============================================================================
# GLOBAL STYLES
# =============================================================================

CUSTOM_STYLE = f"""
    <style>
    .main {{
        padding: 2rem;
    }}
    div[data-testid="stMetricValue"] {{
        font-size: 1.5rem;
        font-weight: bold;
    }}
    div[data-testid="stMetricLabel"] {{
        font-size: 1rem;
        font-weight: normal;
    }}
    div[data-testid="stMetricDelta"] {{
        font-size: 1rem;
    }}
    div[data-testid="stMetricContainer"] {{
        background-color: {BACKGROUND_PRIMARY};
        border: 1px solid {BORDER_PRIMARY};
        padding: 1rem;
        border-radius: {BORDER_RADIUS_LG};
        box-shadow: {SHADOW_SM};
    }}
    .asset-type-header {{
        background-color: {BACKGROUND_PRIMARY};
        padding: 1rem;
        border-radius: {BORDER_RADIUS_LG};
        margin: 1rem 0;
        border: 1px solid {BORDER_PRIMARY};
    }}
    
    /* Card spacing improvements */
    .stMarkdown > div {{
        margin-bottom: 1rem;
    }}
    
    /* Ensure consistent card heights in grids */
    [data-testid="column"] > div {{
        height: 100%;
        display: flex;
        flex-direction: column;
    }}
    
    /* Consistent line height for card elements */
    .stMarkdown > div > div {{
        line-height: 1.2 !important;
    }}
    
    /* Better vertical rhythm for card elements */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        line-height: 1.2 !important;
    }}
    
    .stMarkdown p {{
        margin-bottom: 0.75rem;
        line-height: 1.2 !important;
    }}
    </style>
    """ 