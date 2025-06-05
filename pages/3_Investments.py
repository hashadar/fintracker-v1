import streamlit as st
from utils import (
    load_data,
    calculate_asset_type_metrics,
    create_asset_type_time_series,
    create_asset_type_breakdown,
    display_asset_type_metrics
)

# Load data at the top of the page
df = load_data()

# Ensure data is loaded before rendering the page
if df is not None:
    asset_type = 'Investments'
    st.header(f"{asset_type} Deep Dive")

    # Filter data for the specific asset type
    asset_df = df[df['Asset_Type'] == asset_type].copy()

    if asset_df.empty:
        st.warning(f"No data available for asset type: {asset_type}")
    else:
        # --- METRICS ---
        metrics = calculate_asset_type_metrics(df, asset_type)
        if metrics:
            st.markdown(display_asset_type_metrics(metrics, asset_type), unsafe_allow_html=True)

            if metrics.get('latest_platform_breakdown'):
                st.markdown("#### Latest Month Platform Breakdown")
                platform_cols = st.columns(len(metrics['latest_platform_breakdown']))
                for (platform, value), col in zip(metrics['latest_platform_breakdown'].items(), platform_cols):
                    with col:
                        st.metric(label=platform, value=f"£{value:,.2f}")
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