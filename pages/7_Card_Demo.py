"""Demo page showcasing the new reusable card components with design tokens."""

import streamlit as st
from utils import (
    simple_card,
    emphasis_card,
    complex_card,
    complex_emphasis_card,
    # Design tokens
    BRAND_PRIMARY, BRAND_SECONDARY, BRAND_SUCCESS, BRAND_WARNING, BRAND_ERROR, BRAND_INFO
)

st.set_page_config(
    page_title="Card Components Demo",
    page_icon="🎴",
    layout="wide"
)

st.title("🎴 Card Components Demo")
st.markdown("This page demonstrates the new reusable card components with design tokens for consistent data display across the app.")

st.markdown("---")

# Simple Cards Section
st.header("📋 Simple Cards")
st.markdown("Use these for displaying single metrics without change indicators.")

col1, col2, col3, col4 = st.columns(4)

with col1:
    simple_card(
        title="Total Assets",
        metric="£125,430",
        caption="Latest value as of Dec 2024"
    )

with col2:
    simple_card(
        title="Number of Platforms",
        metric="8",
        caption="Active financial platforms"
    )

with col3:
    simple_card(
        title="Months Tracked",
        metric="24",
        caption="Data history length"
    )

with col4:
    simple_card(
        title="Average Monthly Growth",
        metric="2.4%",
        caption="Compound monthly return"
    )

st.markdown("---")

# Emphasis Cards Section
st.header("🎯 Emphasis Cards")
st.markdown("Use these to highlight important metrics that need attention.")

col1, col2, col3 = st.columns(3)

with col1:
    emphasis_card(
        title="Portfolio Total",
        metric="£125,430",
        caption="Your complete financial position",
        emphasis_color=BRAND_PRIMARY  # Blue
    )

with col2:
    emphasis_card(
        title="Monthly Savings Goal",
        metric="£2,500",
        caption="Target monthly contribution",
        emphasis_color=BRAND_SUCCESS  # Green
    )

with col3:
    emphasis_card(
        title="Emergency Fund",
        metric="£15,000",
        caption="6 months of expenses covered",
        emphasis_color=BRAND_WARNING  # Amber
    )

st.markdown("---")

# Complex Cards Section
st.header("📊 Complex Cards")
st.markdown("Use these for metrics with month-over-month and year-to-date changes.")

col1, col2 = st.columns(2)

with col1:
    complex_card(
        title="Cash Position",
        metric="£25,430",
        mom_change="+£1,200 MoM",
        ytd_change="+£8,500 YTD",
        caption="Across all cash accounts",
        mom_color="normal",  # Green for positive
        ytd_color="normal"   # Green for positive
    )

with col2:
    complex_card(
        title="Investment Portfolio",
        metric="£85,000",
        mom_change="-£2,100 MoM",
        ytd_change="+£12,300 YTD",
        caption="Market volatility impact",
        mom_color="inverse",  # Red for negative
        ytd_color="normal"    # Green for positive
    )

col3, col4 = st.columns(2)

with col3:
    complex_card(
        title="Pension Value",
        metric="£15,000",
        mom_change="+£500 MoM",
        ytd_change="+£3,200 YTD",
        caption="Employer contributions included",
        mom_color="normal",
        ytd_color="normal"
    )

with col4:
    complex_card(
        title="Total Allocation",
        metric="20.3%",
        mom_change="-1.2% MoM",
        ytd_change="+2.1% YTD",
        caption="Cash as % of total portfolio",
        mom_color="inverse",
        ytd_color="normal"
    )

st.markdown("---")

# Complex Emphasis Cards Section
st.header("🔥 Complex Emphasis Cards")
st.markdown("Use these for the most important metrics that need both highlighting and change tracking.")

col1, col2 = st.columns(2)

with col1:
    complex_emphasis_card(
        title="Net Worth",
        metric="£125,430",
        mom_change="+£1,800 MoM",
        ytd_change="+£24,000 YTD",
        caption="Total financial position",
        mom_color="normal",
        ytd_color="normal",
        emphasis_color=BRAND_SECONDARY  # Purple
    )

with col2:
    complex_emphasis_card(
        title="Monthly Growth Rate",
        metric="1.4%",
        mom_change="-0.3% MoM",
        ytd_change="+0.8% YTD",
        caption="Portfolio performance",
        mom_color="inverse",
        ytd_color="normal",
        emphasis_color=BRAND_ERROR  # Red
    )

st.markdown("---")

# Design Tokens Showcase
st.header("🎨 Design Tokens Showcase")
st.markdown("Demonstrating the color palette and emphasis options available through design tokens.")

# Color Palette
st.subheader("Color Palette")
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    emphasis_card(
        title="Primary",
        metric="Blue",
        caption=BRAND_PRIMARY,
        emphasis_color=BRAND_PRIMARY
    )

with col2:
    emphasis_card(
        title="Secondary",
        metric="Purple",
        caption=BRAND_SECONDARY,
        emphasis_color=BRAND_SECONDARY
    )

with col3:
    emphasis_card(
        title="Success",
        metric="Green",
        caption=BRAND_SUCCESS,
        emphasis_color=BRAND_SUCCESS
    )

with col4:
    emphasis_card(
        title="Warning",
        metric="Amber",
        caption=BRAND_WARNING,
        emphasis_color=BRAND_WARNING
    )

with col5:
    emphasis_card(
        title="Error",
        metric="Red",
        caption=BRAND_ERROR,
        emphasis_color=BRAND_ERROR
    )

with col6:
    emphasis_card(
        title="Info",
        metric="Cyan",
        caption=BRAND_INFO,
        emphasis_color=BRAND_INFO
    )

st.markdown("---")

# Usage Examples Section
st.header("💡 Usage Examples")
st.markdown("Here's how to use these components with design tokens in your code:")

with st.expander("Code Examples", expanded=False):
    st.code("""
# Import design tokens
from utils import (
    simple_card, emphasis_card, complex_card, complex_emphasis_card,
    BRAND_PRIMARY, BRAND_SUCCESS, BRAND_WARNING, BRAND_ERROR, BRAND_SECONDARY
)

# Simple card for basic metrics
simple_card(
    title="Total Assets",
    metric="£125,430",
    caption="Latest value as of Dec 2024"
)

# Emphasis card with brand colors
emphasis_card(
    title="Portfolio Total",
    metric="£125,430",
    caption="Your complete financial position",
    emphasis_color=BRAND_PRIMARY  # Use design token
)

# Complex card with semantic colors
complex_card(
    title="Cash Position",
    metric="£25,430",
    mom_change="+£1,200 MoM",
    ytd_change="+£8,500 YTD",
    caption="Across all cash accounts",
    mom_color="normal",  # Automatically uses BRAND_SUCCESS
    ytd_color="normal"   # Automatically uses BRAND_SUCCESS
)

# Complex emphasis card for key metrics
complex_emphasis_card(
    title="Net Worth",
    metric="£125,430",
    mom_change="+£1,800 MoM",
    ytd_change="+£24,000 YTD",
    caption="Total financial position",
    mom_color="normal",
    ytd_color="normal",
    emphasis_color=BRAND_SECONDARY  # Use design token
)
    """, language="python")

st.markdown("---")

# Design Guidelines
st.header("🎨 Design Guidelines")
st.markdown("""
### Card Hierarchy:
1. **Simple Cards** - For basic metrics, counts, and static values
2. **Emphasis Cards** - For important metrics that need visual prominence
3. **Complex Cards** - For metrics with change tracking (MoM/YTD)
4. **Complex Emphasis Cards** - For the most critical metrics with both prominence and change tracking

### Color Guidelines:
- **Design Tokens**: Always use design tokens instead of hardcoded colors
- **Normal**: Automatically uses `BRAND_SUCCESS` (green) for positive changes
- **Inverse**: Automatically uses `BRAND_ERROR` (red) for negative changes  
- **Neutral**: Automatically uses `NEUTRAL_500` (gray) for neutral changes
- **Emphasis Colors**: Use brand tokens (`BRAND_PRIMARY`, `BRAND_SECONDARY`, etc.)

### Typography:
- **Title**: Small, uppercase, letter-spaced (uses `FONT_SIZE_SM`)
- **Metric**: Large, bold (uses `FONT_SIZE_4XL` for simple/complex, `FONT_SIZE_5XL` for emphasis)
- **Caption**: Small, muted (uses `FONT_SIZE_XS`)

### Layout:
- All cards are center-aligned
- Consistent padding and border radius (uses `SPACE_6` and `BORDER_RADIUS_XL`)
- Subtle shadows for depth (uses `SHADOW_MD`)
- Responsive design that works in columns
- Smooth transitions (uses `TRANSITION_NORMAL`)

### Benefits of Design Tokens:
- **Consistency**: All components use the same design system
- **Maintainability**: Change colors/spacing in one place
- **Scalability**: Easy to add new colors or modify existing ones
- **Semantic**: Colors have meaning (success, warning, error, etc.)
- **Accessibility**: Proper contrast ratios and color relationships
""")

st.markdown("---")

# Token System Benefits
st.header("🔧 Token System Benefits")
st.markdown("""
### Single Source of Truth:
- All colors, spacing, typography, and other design variables are defined in `utils/design_tokens.py`
- No more hardcoded values scattered throughout the codebase
- Easy to maintain and update design system

### Semantic Color System:
- Colors have meaning: success (green), warning (amber), error (red), etc.
- Automatic color selection based on context (positive/negative changes)
- Consistent color usage across all components

### Scalable Design System:
- Easy to add new colors or modify existing ones
- Utility functions for generating gradients, borders, and other effects
- Pre-built style functions for common patterns

### Developer Experience:
- IntelliSense support for all design tokens
- Clear naming conventions
- Comprehensive documentation
- Type hints for better IDE support
""") 