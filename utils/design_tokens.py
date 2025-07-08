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
CARD_CAPTION_MARGIN_TOP = SPACE_2

# Card Change Styles
CARD_CHANGE_FONT_SIZE = FONT_SIZE_SM
CARD_CHANGE_FONT_WEIGHT = FONT_WEIGHT_SEMIBOLD
CARD_CHANGE_MARGIN_TOP = SPACE_2

# =============================================================================
# COLOR UTILITY FUNCTIONS
# =============================================================================

def get_change_color(color_type: str) -> str:
    """
    Get the appropriate color for change indicators.
    
    Args:
        color_type: "normal" (positive), "inverse" (negative), or "neutral"
    
    Returns:
        Hex color code
    """
    if color_type == "normal":
        return BRAND_SUCCESS
    elif color_type == "inverse":
        return BRAND_ERROR
    else:
        return NEUTRAL_500

def get_emphasis_color(color_name: str = "primary") -> str:
    """
    Get emphasis color by name.
    
    Args:
        color_name: "primary", "secondary", "success", "warning", "error", "info"
    
    Returns:
        Hex color code
    """
    emphasis_colors = {
        "primary": BRAND_PRIMARY,
        "secondary": BRAND_SECONDARY,
        "success": BRAND_SUCCESS,
        "warning": BRAND_WARNING,
        "error": BRAND_ERROR,
        "info": BRAND_INFO
    }
    return emphasis_colors.get(color_name, BRAND_PRIMARY)

def get_background_gradient(color: str, opacity_start: str = "15", opacity_end: str = "08") -> str:
    """
    Generate a gradient background string for emphasis cards.
    
    Args:
        color: Base color hex code
        opacity_start: Starting opacity percentage
        opacity_end: Ending opacity percentage
    
    Returns:
        CSS gradient string
    """
    return f"linear-gradient(135deg, {color}{opacity_start}, {color}{opacity_end})"

def get_border_color(color: str, opacity: str = "30") -> str:
    """
    Generate a border color with opacity.
    
    Args:
        color: Base color hex code
        opacity: Opacity percentage
    
    Returns:
        Color with opacity
    """
    return f"{color}{opacity}"

# =============================================================================
# STYLE UTILITY FUNCTIONS
# =============================================================================

def get_card_base_styles() -> str:
    """Get base styles for all cards."""
    return f"background-color: {BACKGROUND_PRIMARY}; border: {CARD_BORDER_WIDTH_NORMAL} solid {BORDER_PRIMARY}; padding: {CARD_PADDING_MD}; border-radius: {BORDER_RADIUS_XL}; box-shadow: {SHADOW_MD}; text-align: center; margin-bottom: {SPACE_4}; transition: all {TRANSITION_NORMAL};"

def get_emphasis_card_styles(emphasis_color: str = BRAND_PRIMARY) -> str:
    """Get styles for emphasis cards."""
    return f"background: {get_background_gradient(emphasis_color)}; border: {CARD_BORDER_WIDTH_EMPHASIS} solid {get_border_color(emphasis_color)}; padding: {CARD_PADDING_MD}; border-radius: {BORDER_RADIUS_XL}; box-shadow: {SHADOW_LG}; text-align: center; margin-bottom: {SPACE_4}; transition: all {TRANSITION_NORMAL}; position: relative;"

def get_card_title_styles() -> str:
    """Get styles for card titles."""
    return f"font-size: {CARD_TITLE_FONT_SIZE}; font-weight: {CARD_TITLE_FONT_WEIGHT}; color: {CARD_TITLE_COLOR}; margin-bottom: {SPACE_2}; text-transform: {CARD_TITLE_TEXT_TRANSFORM}; letter-spacing: {CARD_TITLE_LETTER_SPACING};"

def get_emphasis_card_title_styles(emphasis_color: str = BRAND_PRIMARY) -> str:
    """Get styles for emphasis card titles."""
    return f"font-size: {CARD_TITLE_FONT_SIZE}; font-weight: {FONT_WEIGHT_SEMIBOLD}; color: {emphasis_color}; margin-bottom: {SPACE_2}; text-transform: {CARD_TITLE_TEXT_TRANSFORM}; letter-spacing: {CARD_TITLE_LETTER_SPACING};"

def get_card_metric_styles(font_size: str = CARD_METRIC_FONT_SIZE_SIMPLE) -> str:
    """Get styles for card metrics."""
    return f"font-size: {font_size}; font-weight: {CARD_METRIC_FONT_WEIGHT}; color: {CARD_METRIC_COLOR}; margin: {SPACE_2} 0; line-height: {CARD_METRIC_LINE_HEIGHT};"

def get_card_caption_styles() -> str:
    """Get styles for card captions."""
    return f"font-size: {CARD_CAPTION_FONT_SIZE}; color: {CARD_CAPTION_COLOR}; margin-top: {CARD_CAPTION_MARGIN_TOP};"

def get_card_change_styles() -> str:
    """Get styles for card change indicators."""
    return f"font-size: {CARD_CHANGE_FONT_SIZE}; margin-top: {CARD_CHANGE_MARGIN_TOP};"

def get_emphasis_accent_bar(emphasis_color: str = BRAND_PRIMARY) -> str:
    """Get styles for the top accent bar on emphasis cards."""
    return f"position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, {emphasis_color}, {emphasis_color}80); border-radius: {BORDER_RADIUS_XL} {BORDER_RADIUS_XL} 0 0;" 