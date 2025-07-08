import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
from utils import (
    load_data,
    calculate_allocation_metrics,
    simple_card,
    complex_emphasis_card,
    complex_card,
    # Design tokens
    BRAND_PRIMARY, BRAND_SUCCESS, BRAND_WARNING, BRAND_ERROR
)

# Load data at the top of the page
df = load_data()

if df is not None:
    st.header("All Assets Overview")
    # --- All Assets Metrics (from old All Assets page) ---
    all_df = df.copy()
    all_df['Month'] = all_df['Timestamp'].dt.to_period('M').dt.to_timestamp()
    all_monthly = all_df.groupby('Month')['Value'].sum().reset_index()
    all_monthly['RollingAvg'] = all_monthly['Value'].rolling(window=3).mean()
    all_monthly['RollingStd'] = all_monthly['Value'].rolling(window=3).std()
    running_max = all_monthly['Value'].cummax()
    drawdown = (all_monthly['Value'] - running_max) / running_max
    all_monthly['Drawdown'] = drawdown
    all_monthly['MoM'] = all_monthly['Value'].pct_change()
    # Identify best and worst months for MoM change
    if not all_monthly['MoM'].dropna().empty:
        best_month = all_monthly.loc[all_monthly['MoM'].idxmax()]
        worst_month = all_monthly.loc[all_monthly['MoM'].idxmin()]
    else:
        best_month = None
        worst_month = None
    max_drawdown = drawdown.min()

    # --- Top summary cards: drawdown, best/worst month (no change indicators, just value+caption) ---
    col1, col2, col3 = st.columns(3)
    with col1:
        simple_card(
            title="Maximum Drawdown",
            metric=str(f"{float(max_drawdown):.2%}"),
            caption="Largest peak-to-trough decline in portfolio value"
        )
    with col2:
        if best_month is not None:
            simple_card(
                title="Best Month",
                metric=str(f"{float(best_month['MoM'])*100:.2f}%"),
                caption=str(f"{best_month['Month'].strftime('%b %Y')} - Highest growth")
            )
        else:
            simple_card(
                title="Best Month",
                metric="N/A",
                caption="Not enough data"
            )
    with col3:
        if worst_month is not None:
            simple_card(
                title="Worst Month",
                metric=str(f"{float(worst_month['MoM'])*100:.2f}%"),
                caption=str(f"{worst_month['Month'].strftime('%b %Y')} - Largest decline")
            )
        else:
            simple_card(
                title="Worst Month",
                metric="N/A",
                caption="Not enough data"
            )
    st.markdown("---")

    # --- Performance charts: value, volatility, MoM change ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Value & 3-Month Rolling Avg**")
        st.plotly_chart(
            px.line(
                all_monthly, x='Month', y=['Value', 'RollingAvg'],
                labels={'value': 'Value (GBP)', 'Month': 'Month'},
                title=None
            ),
            use_container_width=True
        )
    with col2:
        st.markdown("**Rolling Volatility (Std Dev)**")
        st.plotly_chart(
            px.line(
                all_monthly, x='Month', y='RollingStd',
                labels={'RollingStd': 'Std Dev', 'Month': 'Month'},
                title=None
            ),
            use_container_width=True
        )
    with col3:
        st.markdown("**MoM % Change Over Time**")
        mom_clean = all_monthly[['Month', 'MoM']].dropna()
        if mom_clean.empty:
            st.info("Not enough data for a meaningful time series.")
        else:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=mom_clean['Month'], y=mom_clean['MoM'], mode='lines+markers'))
            fig.update_layout(yaxis_tickformat='.2%', xaxis_title='Month', yaxis_title='MoM % Change', showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

    # --- Distribution and drawdown charts ---
    col4, col5 = st.columns(2)
    with col4:
        st.markdown("**Boxplot of Monthly Value**")
        st.plotly_chart(
            px.box(all_monthly, y='Value', title=None),
            use_container_width=True
        )
    with col5:
        st.markdown("**Drawdown Over Time**")
        st.plotly_chart(
            px.line(
                all_monthly, x='Month', y='Drawdown',
                labels={'Drawdown': 'Drawdown', 'Month': 'Month'},
                title=None
            ),
            use_container_width=True
        )
    st.markdown("---")

    # --- Download button for monthly data ---
    st.download_button(
        label="Download All Assets Monthly Data as CSV",
        data=all_monthly.to_csv(index=False),
        file_name="all_assets_monthly.csv",
        mime="text/csv"
    )
    st.markdown("---")

    # --- Asset Type Cards: Portfolio total (emphasis), then each asset type (complex) ---
    allocation_metrics, latest_month, prev_month, ytd_start_month = calculate_allocation_metrics(df)
    st.caption(
        f"Latest Month: {latest_month.strftime('%B %Y')} | Previous Month: {prev_month.strftime('%B %Y') if prev_month is not None else 'N/A'} | YTD Start: {ytd_start_month.strftime('%B %Y') if ytd_start_month is not None else 'N/A'}"
    )
    # Portfolio total card (shows value, MoM, YTD, emphasis)
    complex_emphasis_card(
        title="Portfolio Total",
        metric=f"£{allocation_metrics['Total']['current']:,.2f}",
        mom_change=(f"£{allocation_metrics['Total']['mom_increase']:,.2f} MoM" if allocation_metrics['Total']['mom_increase'] is not None else None),
        ytd_change=(f"£{allocation_metrics['Total']['ytd_increase']:,.2f} YTD" if allocation_metrics['Total']['ytd_increase'] is not None else None),
        caption=f"Total financial position as of {latest_month.strftime('%B %Y')}",
        mom_color="normal" if allocation_metrics['Total']['mom_increase'] is not None and allocation_metrics['Total']['mom_increase'] >= 0 else "inverse",
        ytd_color="normal" if allocation_metrics['Total']['ytd_increase'] is not None and allocation_metrics['Total']['ytd_increase'] >= 0 else "inverse",
        emphasis_color=BRAND_PRIMARY
    )
    # Asset type cards (Cash, Pensions, Investments) with change tracking
    col1, col2, col3 = st.columns(3)
    cash = allocation_metrics.get('Cash', {})
    with col1:
        complex_card(
            title="Cash Position",
            metric=f"£{cash.get('current', 0):,.2f}",
            mom_change=(f"{cash.get('mom_pct_increase', 0):+.2f}% MoM" if cash.get('mom_pct_increase') is not None else None),
            ytd_change=(f"{cash.get('ytd_pct_increase', 0):+.2f}% YTD" if cash.get('ytd_pct_increase') is not None else None),
            caption=f"{cash.get('allocation', 0):.1f}% of portfolio",
            mom_color="normal" if cash.get('mom_pct_increase', 0) >= 0 else "inverse",
            ytd_color="normal" if cash.get('ytd_pct_increase', 0) >= 0 else "inverse"
        )
    pension = allocation_metrics.get('Pensions', {})
    with col2:
        complex_card(
            title="Pension Value",
            metric=f"£{pension.get('current', 0):,.2f}",
            mom_change=(f"{pension.get('mom_pct_increase', 0):+.2f}% MoM" if pension.get('mom_pct_increase') is not None else None),
            ytd_change=(f"{pension.get('ytd_pct_increase', 0):+.2f}% YTD" if pension.get('ytd_pct_increase') is not None else None),
            caption=f"{pension.get('allocation', 0):.1f}% of portfolio",
            mom_color="normal" if pension.get('mom_pct_increase', 0) >= 0 else "inverse",
            ytd_color="normal" if pension.get('ytd_pct_increase', 0) >= 0 else "inverse"
        )
    invest = allocation_metrics.get('Investments', {})
    with col3:
        complex_card(
            title="Investment Portfolio",
            metric=f"£{invest.get('current', 0):,.2f}",
            mom_change=(f"{invest.get('mom_pct_increase', 0):+.2f}% MoM" if invest.get('mom_pct_increase') is not None else None),
            ytd_change=(f"{invest.get('ytd_pct_increase', 0):+.2f}% YTD" if invest.get('ytd_pct_increase') is not None else None),
            caption=f"{invest.get('allocation', 0):.1f}% of portfolio",
            mom_color="normal" if invest.get('mom_pct_increase', 0) >= 0 else "inverse",
            ytd_color="normal" if invest.get('ytd_pct_increase', 0) >= 0 else "inverse"
        )
else:
    st.error("Data could not be loaded. Please check your data file.") 