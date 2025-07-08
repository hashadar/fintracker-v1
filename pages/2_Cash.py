import streamlit as st
from utils import (
    load_data,
    calculate_asset_type_metrics,
    create_asset_type_time_series,
    create_asset_type_breakdown,
    # New card components
    complex_emphasis_card,
    simple_card,
    # Design tokens
    BRAND_PRIMARY, BRAND_SUCCESS, BRAND_WARNING
)

# Load data at the top of the page
df = load_data()

# Ensure data is loaded before rendering the page
if df is not None:
    asset_type = 'Cash'
    st.header(f"{asset_type} Deep Dive")

    # Filter data for the specific asset type
    asset_df = df[df['Asset_Type'] == asset_type].copy()

    if asset_df.empty:
        st.warning(f"No data available for asset type: {asset_type}")
    else:
        # --- METRICS ---
        metrics = calculate_asset_type_metrics(df, asset_type)
        if metrics:
            # Main cash position with emphasis (shows value, MoM, YTD)
            complex_emphasis_card(
                title="Total Cash Position",
                metric=f"£{metrics['latest_value']:,.2f}",
                mom_change=f"{metrics['mom_change']:+.1f}% MoM",
                ytd_change=f"{metrics.get('ytd_change', 0):+.1f}% YTD",
                caption=f"Latest value as of {metrics.get('latest_month', 'N/A')}",
                mom_color="normal" if metrics['mom_change'] >= 0 else "inverse",
                ytd_color="normal" if metrics.get('ytd_change', 0) >= 0 else "inverse",
                emphasis_color=BRAND_SUCCESS
            )
            # Additional summary stats (counts, tracked months) use simple_card
            col1, col2, col3 = st.columns(3)
            with col1:
                simple_card(
                    title="Number of Platforms",
                    metric=str(metrics['platforms']),
                    caption="Active cash platforms"
                )
            with col2:
                simple_card(
                    title="Number of Assets",
                    metric=str(metrics['assets']),
                    caption="Cash accounts tracked"
                )
            with col3:
                simple_card(
                    title="Months Tracked",
                    metric=str(metrics['months_tracked']),
                    caption="Data history length"
                )

            # Platform breakdown with new cards
            if metrics.get('latest_platform_breakdown'):
                st.markdown("---")
                st.subheader("Platform Breakdown")
                platform_cols = st.columns(len(metrics['latest_platform_breakdown']))
                for (platform, value), col in zip(metrics['latest_platform_breakdown'].items(), platform_cols):
                    with col:
                        simple_card(
                            title=platform,
                            metric=f"£{value:,.2f}",
                            caption=f"{(value/metrics['latest_value']*100):.1f}% of total"
                        )
        else:
            st.info("No summary metrics could be calculated.")

        st.markdown("---")

        # --- CHARTS ---
        fig_value, fig_composition = create_asset_type_time_series(df, asset_type)
        fig_platform, fig_asset = create_asset_type_breakdown(df, asset_type)

        charts = [fig for fig in [fig_value, fig_composition, fig_platform, fig_asset] if fig is not None]

        if len(charts) >= 2:
            row1_cols = st.columns(2)
            if charts[0]:
                with row1_cols[0]:
                    st.plotly_chart(charts[0], use_container_width=True)
            if charts[1]:
                with row1_cols[1]:
                    st.plotly_chart(charts[1], use_container_width=True)

            if len(charts) >= 4:
                row2_cols = st.columns(2)
                if charts[2]:
                    with row2_cols[0]:
                        st.plotly_chart(charts[2], use_container_width=True)
                if charts[3]:
                    with row2_cols[1]:
                        st.plotly_chart(charts[3], use_container_width=True)
            elif len(charts) == 3 and charts[2]:
                 st.plotly_chart(charts[2], use_container_width=True)

        elif charts:
            st.plotly_chart(charts[0], use_container_width=True)

        st.markdown("---")

        # --- RAW DATA ---
        with st.expander("Raw Data View"):
            st.dataframe(asset_df, use_container_width=True)
else:
    st.error("Data could not be loaded. Please check your data file.") 