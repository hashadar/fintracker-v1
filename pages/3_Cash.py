import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from utils import (
    load_data,
    calculate_asset_type_metrics
)
from utils.design.cards import simple_card, complex_emphasis_card, complex_card, emphasis_card
from utils.charts import create_time_series_chart, create_bar_chart, create_pie_chart, create_histogram, create_box_plot, create_asset_type_time_series, create_asset_type_breakdown
from utils.design.tokens import (
    BRAND_PRIMARY, BRAND_SUCCESS, BRAND_WARNING, BRAND_ERROR, BRAND_INFO
)
from utils.design.components import create_page_header, create_section_header, create_metric_grid, create_chart_grid

# Page configuration
st.set_page_config(page_title="Cash - FinTracker", layout="wide")

# Load data
df = load_data()

if df is not None and not df.empty:
    # Filter for cash assets
    cash_df = df[df['Asset_Type'] == 'Cash'].copy()
    
    if not cash_df.empty:
        create_page_header(
            title="💰 Cash Assets Dashboard",
            description="Comprehensive analysis of your cash positions and liquidity"
        )
        
        # Calculate cash-specific metrics
        cash_metrics = calculate_asset_type_metrics(df, 'Cash')
        
        # Get latest month for display
        latest_month = cash_df['Timestamp'].dt.to_period('M').max()
        
        # Display time period info
        st.caption(f"📅 Latest Month: {latest_month.strftime('%B %Y')}")
        
        # --- Cash Summary Cards ---
        create_section_header("Cash Position Summary", icon="💳")
        
        # Main cash total card
        complex_emphasis_card(
            title="Total Cash Position",
            metric=f"£{cash_metrics['latest_value']:,.2f}",
            mom_change=(f"{cash_metrics['mom_change']:+.2f}%" if cash_metrics['mom_change'] is not None else None),
            ytd_change=None,  # Cash doesn't typically have YTD growth like investments
            caption=f"Total liquid cash across {cash_metrics['platforms']} platforms",
            mom_color="normal" if cash_metrics['mom_change'] is not None and cash_metrics['mom_change'] >= 0 else "inverse",
            emphasis_color=BRAND_SUCCESS
        )
        
        # Cash metrics cards using metric grid
        def get_mom_change_card():
            if cash_metrics['mom_change'] is not None:
                return lambda: simple_card(
                    title="MoM Change",
                    metric=f"{cash_metrics['mom_change']:+.2f}%",
                    caption="Month-over-month change"
                )
            else:
                return lambda: simple_card(
                    title="MoM Change",
                    metric="N/A",
                    caption="Not enough data"
                )
        
        create_metric_grid([
            lambda: simple_card(
                title="Platforms",
                metric=str(cash_metrics['platforms']),
                caption="Cash accounts"
            ),
            lambda: simple_card(
                title="Assets",
                metric=str(cash_metrics['assets']),
                caption="Cash instruments"
            ),
            lambda: simple_card(
                title="Months Tracked",
                metric=str(cash_metrics['months_tracked']),
                caption="Historical period"
            ),
            get_mom_change_card()
        ], cols=4)
        
        st.markdown("---")
        
        # --- Platform Breakdown ---
        create_section_header("Platform Analysis", icon="🏦")
        
        # Platform distribution using chart grid
        platform_breakdown = pd.DataFrame([
            {'Platform': platform, 'Value': value}
            for platform, value in cash_metrics['latest_platform_breakdown'].items()
        ])
        
        def create_platform_pie_chart():
            st.markdown("**Current Platform Distribution**")
            if not platform_breakdown.empty:
                fig_platform = create_pie_chart(
                    platform_breakdown,
                    names_col='Platform',
                    values_col='Value',
                    title="Current Platform Distribution"
                )
                st.plotly_chart(fig_platform, use_container_width=True)
            else:
                st.info("No platform data available")
        
        def create_platform_bar_chart():
            st.markdown("**Platform Values**")
            if not platform_breakdown.empty:
                fig_platform_bar = create_bar_chart(
                    platform_breakdown,
                    x_col='Platform',
                    y_col='Value',
                    title="Platform Values"
                )
                st.plotly_chart(fig_platform_bar, use_container_width=True)
            else:
                st.info("No platform data available")
        
        create_chart_grid([create_platform_pie_chart, create_platform_bar_chart], cols=2)
        
        st.markdown("---")
        
        # --- Time Series Analysis ---
        create_section_header("Cash Trends Over Time", icon="📈")
        
        # Create time series charts
        fig_value, fig_composition = create_asset_type_time_series(df, 'Cash')
        
        def create_cash_values_chart():
            st.markdown("**Cash Values by Platform**")
            st.plotly_chart(fig_value, use_container_width=True)
        
        def create_platform_composition_chart():
            st.markdown("**Platform Composition Over Time**")
            st.plotly_chart(fig_composition, use_container_width=True)
        
        create_chart_grid([create_cash_values_chart, create_platform_composition_chart], cols=2)
        
        # Monthly cash totals
        cash_df['Month'] = cash_df['Timestamp'].dt.to_period('M').dt.to_timestamp()
        monthly_cash = cash_df.groupby('Month')['Value'].sum().reset_index()
        monthly_cash['RollingAvg'] = monthly_cash['Value'].rolling(window=3).mean()
        monthly_cash['MoM'] = monthly_cash['Value'].pct_change()
        
        def create_total_cash_chart():
            st.markdown("**Total Cash Over Time**")
            fig_total = create_time_series_chart(
                monthly_cash,
                x_col='Month',
                y_cols=['Value', 'RollingAvg'],
                title="Total Cash Over Time"
            )
            st.plotly_chart(fig_total, use_container_width=True)
        
        def create_monthly_changes_chart():
            st.markdown("**Monthly Cash Changes**")
            mom_clean = monthly_cash[['Month', 'MoM']].dropna()
            if not mom_clean.empty:
                fig_mom = create_bar_chart(
                    mom_clean,
                    x_col='Month',
                    y_col='MoM',
                    title="Monthly Cash Changes"
                )
                fig_mom.update_yaxes(tickformat='.2%')
                fig_mom.update_traces(marker_color=['green' if x >= 0 else 'red' for x in mom_clean['MoM']])
                st.plotly_chart(fig_mom, use_container_width=True)
            else:
                st.info("Not enough data for monthly changes")
        
        create_chart_grid([create_total_cash_chart, create_monthly_changes_chart], cols=2)
        
        st.markdown("---")
        
        # --- Liquidity Analysis ---
        create_section_header("Liquidity Analysis", icon="💧")
        
        # Calculate liquidity metrics using metric grid
        total_portfolio = df[df['Timestamp'].dt.to_period('M') == latest_month]['Value'].sum()
        cash_percentage = (cash_metrics['latest_value'] / total_portfolio * 100) if total_portfolio > 0 else 0
        avg_cash = monthly_cash['Value'].mean()
        cash_volatility = monthly_cash['Value'].std()
        cash_range = monthly_cash['Value'].max() - monthly_cash['Value'].min()
        
        create_metric_grid([
            lambda: simple_card(
                title="Cash Allocation",
                metric=f"{cash_percentage:.1f}%",
                caption="Of total portfolio"
            ),
            lambda: simple_card(
                title="Average Cash",
                metric=f"£{avg_cash:,.2f}",
                caption="Mean monthly balance"
            ),
            lambda: simple_card(
                title="Cash Volatility",
                metric=f"£{cash_volatility:,.2f}",
                caption="Standard deviation"
            ),
            lambda: simple_card(
                title="Cash Range",
                metric=f"£{cash_range:,.2f}",
                caption="Max - Min balance"
            )
        ], cols=4)
        
        # Cash distribution analysis using chart grid
        def create_cash_distribution_chart():
            st.markdown("**Cash Balance Distribution**")
            fig_dist = create_histogram(
                monthly_cash,
                x_col='Value',
                title="Cash Balance Distribution",
                nbins=10
            )
            st.plotly_chart(fig_dist, use_container_width=True)
        
        def create_cash_box_plot():
            st.markdown("**Cash Balance Box Plot**")
            fig_box = create_box_plot(
                monthly_cash,
                y_col='Value',
                title="Cash Balance Box Plot"
            )
            st.plotly_chart(fig_box, use_container_width=True)
        
        create_chart_grid([create_cash_distribution_chart, create_cash_box_plot], cols=2)
        
        st.markdown("---")
        
        # --- Cash Flow Patterns ---
        create_section_header("Cash Flow Patterns", icon="🔄")
        
        # Analyze cash flow patterns
        if len(monthly_cash) > 1:
            # Calculate cash flow (change in cash)
            monthly_cash['CashFlow'] = monthly_cash['Value'].diff()
            
            def create_monthly_cash_flow_chart():
                st.markdown("**Monthly Cash Flow**")
                cash_flow_clean = monthly_cash[['Month', 'CashFlow']].dropna()
                if not cash_flow_clean.empty:
                    fig_flow = create_bar_chart(
                        cash_flow_clean,
                        x_col='Month',
                        y_col='CashFlow',
                        title="Monthly Cash Flow"
                    )
                    fig_flow.update_traces(marker_color=['green' if x >= 0 else 'red' for x in cash_flow_clean['CashFlow']])
                    st.plotly_chart(fig_flow, use_container_width=True)
                else:
                    st.info("Not enough data for cash flow analysis")
            
            def create_cash_flow_distribution_chart():
                st.markdown("**Cash Flow Distribution**")
                cash_flow_clean = monthly_cash[['Month', 'CashFlow']].dropna()
                if not cash_flow_clean.empty:
                    fig_flow_dist = create_histogram(
                        cash_flow_clean,
                        x_col='CashFlow',
                        title="Cash Flow Distribution",
                        nbins=8
                    )
                    st.plotly_chart(fig_flow_dist, use_container_width=True)
                else:
                    st.info("Not enough data for cash flow distribution")
            
            create_chart_grid([create_monthly_cash_flow_chart, create_cash_flow_distribution_chart], cols=2)
            
            # Cash flow metrics using metric grid
            cash_flow_clean = monthly_cash[['Month', 'CashFlow']].dropna()
            positive_flows = cash_flow_clean[cash_flow_clean['CashFlow'] > 0]['CashFlow'].sum()
            negative_flows = abs(cash_flow_clean[cash_flow_clean['CashFlow'] < 0]['CashFlow'].sum())
            net_flow = cash_flow_clean['CashFlow'].sum()
            avg_flow = cash_flow_clean['CashFlow'].mean()
            
            create_metric_grid([
                lambda: simple_card(
                    title="Total Inflows",
                    metric=f"£{positive_flows:,.2f}",
                    caption="Positive cash flows"
                ),
                lambda: simple_card(
                    title="Total Outflows",
                    metric=f"£{negative_flows:,.2f}",
                    caption="Negative cash flows"
                ),
                lambda: simple_card(
                    title="Net Cash Flow",
                    metric=f"£{net_flow:,.2f}",
                    caption="Net change over period"
                ),
                lambda: simple_card(
                    title="Avg Monthly Flow",
                    metric=f"£{avg_flow:,.2f}",
                    caption="Mean monthly change"
                )
            ], cols=4)
        else:
            st.info("Not enough data for cash flow analysis")
        
        st.markdown("---")
        
        # --- Cash Management Insights ---
        create_section_header("Cash Management Insights", icon="💡")
        
        # Generate insights based on data
        insights = []
        
        if cash_percentage > 20:
            insights.append("⚠️ **High Cash Allocation**: Your cash represents over 20% of your portfolio. Consider if this aligns with your investment strategy.")
        elif cash_percentage < 5:
            insights.append("⚠️ **Low Cash Allocation**: Your cash is below 5% of your portfolio. Ensure you have adequate emergency funds.")
        else:
            insights.append("✅ **Balanced Cash Position**: Your cash allocation appears well-balanced for liquidity needs.")
        
        if cash_metrics['mom_change'] is not None and cash_metrics['mom_change'] > 10:
            insights.append("📈 **Strong Cash Growth**: Your cash position has grown significantly this month.")
        elif cash_metrics['mom_change'] is not None and cash_metrics['mom_change'] < -10:
            insights.append("📉 **Cash Decline**: Your cash position has decreased significantly this month.")
        
        if cash_volatility > avg_cash * 0.3:
            insights.append("📊 **High Cash Volatility**: Your cash balance shows significant month-to-month variation.")
        
        if len(insights) > 0:
            for insight in insights:
                st.markdown(insight)
        else:
            st.info("No specific insights available with current data.")
    
    else:
        st.error("❌ No cash data found in your portfolio.")
        st.info("💡 Make sure your data includes assets classified as 'Cash' type.")

else:
    st.error("❌ Data could not be loaded. Please check your data file.")
    st.info("💡 Make sure you have uploaded data through the sidebar on the Home page.") 