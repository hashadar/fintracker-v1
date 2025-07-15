import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from utils import (
    load_data,
    calculate_asset_type_metrics
)
from utils.design.cards import simple_card, complex_emphasis_card, complex_card, emphasis_card
from utils.charts import create_time_series_chart, create_bar_chart, create_pie_chart, create_histogram, create_asset_type_time_series, create_asset_type_breakdown
from utils.design.tokens import (
    BRAND_PRIMARY, BRAND_SUCCESS, BRAND_WARNING, BRAND_ERROR, BRAND_INFO
)
from utils.design.components import create_page_header, create_section_header, create_metric_grid, create_chart_grid

# Page configuration
st.set_page_config(page_title="Pensions - FinTracker", layout="wide")

# Load data
df = load_data()

if df is not None and not df.empty:
    # Filter for pension assets
    pension_df = df[df['Asset_Type'] == 'Pensions'].copy()
    
    if not pension_df.empty:
        create_page_header(
            title="🏦 Pension Assets Dashboard",
            description="Comprehensive analysis of your pension positions and long-term retirement planning"
        )
        
        # Calculate pension-specific metrics
        pension_metrics = calculate_asset_type_metrics(df, 'Pensions')
        
        # Get latest month for display
        latest_month = pension_df['Timestamp'].dt.to_period('M').max()
        
        # Display time period info
        st.caption(f"📅 Latest Month: {latest_month.strftime('%B %Y')}")
        
        # --- Pension Summary Cards ---
        create_section_header("Pension Portfolio Summary", icon="🎯")
        
        # Main pension total card
        complex_emphasis_card(
            title="Total Pension Portfolio",
            metric=f"£{pension_metrics['latest_value']:,.2f}",
            mom_change=(f"{pension_metrics['mom_change']:+.2f}%" if pension_metrics['mom_change'] is not None else None),
            ytd_change=None,  # Will calculate YTD separately
            caption=f"Pension portfolio across {pension_metrics['platforms']} providers",
            mom_color="normal" if pension_metrics['mom_change'] is not None and pension_metrics['mom_change'] >= 0 else "inverse",
            emphasis_color=BRAND_INFO
        )
        
        # Pension metrics cards using metric grid
        def get_mom_growth_card():
            if pension_metrics['mom_change'] is not None:
                return lambda: simple_card(
                    title="MoM Growth",
                    metric=f"{pension_metrics['mom_change']:+.2f}%",
                    caption="Month-over-month growth"
                )
            else:
                return lambda: simple_card(
                    title="MoM Growth",
                    metric="N/A",
                    caption="Not enough data"
                )
        
        create_metric_grid([
            lambda: simple_card(
                title="Providers",
                metric=str(pension_metrics['platforms']),
                caption="Pension providers"
            ),
            lambda: simple_card(
                title="Schemes",
                metric=str(pension_metrics['assets']),
                caption="Pension schemes"
            ),
            lambda: simple_card(
                title="Months Tracked",
                metric=str(pension_metrics['months_tracked']),
                caption="Historical period"
            ),
            get_mom_growth_card()
        ], cols=4)
        
        st.markdown("---")
        
        # --- Long-term Growth Analysis ---
        create_section_header("Long-term Growth Analysis", icon="📈")
        
        # Prepare data for growth analysis
        pension_df['Month'] = pension_df['Timestamp'].dt.to_period('M').dt.to_timestamp()
        monthly_pensions = pension_df.groupby('Month')['Value'].sum().reset_index()
        monthly_pensions['RollingAvg'] = monthly_pensions['Value'].rolling(window=6).mean()  # 6-month average for pensions
        monthly_pensions['RollingStd'] = monthly_pensions['Value'].rolling(window=6).std()
        monthly_pensions['MoM'] = monthly_pensions['Value'].pct_change()
        
        # Calculate cumulative growth
        if len(monthly_pensions) > 1:
            first_value = monthly_pensions['Value'].iloc[0]
            monthly_pensions['CumulativeGrowth'] = (monthly_pensions['Value'] - first_value) / first_value
            monthly_pensions['CumulativeGrowthPct'] = monthly_pensions['CumulativeGrowth'] * 100
        
        # Growth metrics using metric grid
        def get_total_growth_card():
            if len(monthly_pensions) > 1:
                total_growth = ((monthly_pensions['Value'].iloc[-1] - monthly_pensions['Value'].iloc[0]) / monthly_pensions['Value'].iloc[0]) * 100
                return lambda: simple_card(
                    title="Total Growth",
                    metric=f"{total_growth:.1f}%",
                    caption="Since tracking began"
                )
            else:
                return lambda: simple_card(
                    title="Total Growth",
                    metric="N/A",
                    caption="Not enough data"
                )
        
        def get_avg_monthly_growth_card():
            if len(monthly_pensions) > 1:
                avg_monthly_growth = monthly_pensions['MoM'].mean() * 100
                return lambda: simple_card(
                    title="Avg Monthly Growth",
                    metric=f"{avg_monthly_growth:.2f}%",
                    caption="Mean monthly growth"
                )
            else:
                return lambda: simple_card(
                    title="Avg Monthly Growth",
                    metric="N/A",
                    caption="Not enough data"
                )
        
        def get_best_month_card():
            if len(monthly_pensions) > 1:
                best_month = monthly_pensions.loc[monthly_pensions['MoM'].idxmax()]
                return lambda: simple_card(
                    title="Best Month",
                    metric=f"{best_month['MoM']:.2%}",
                    caption=f"{best_month['Month'].strftime('%b %Y')}"
                )
            else:
                return lambda: simple_card(
                    title="Best Month",
                    metric="N/A",
                    caption="Not enough data"
                )
        
        def get_worst_month_card():
            if len(monthly_pensions) > 1:
                worst_month = monthly_pensions.loc[monthly_pensions['MoM'].idxmin()]
                return lambda: simple_card(
                    title="Worst Month",
                    metric=f"{worst_month['MoM']:.2%}",
                    caption=f"{worst_month['Month'].strftime('%b %Y')}"
                )
            else:
                return lambda: simple_card(
                    title="Worst Month",
                    metric="N/A",
                    caption="Not enough data"
                )
        
        create_metric_grid([
            get_total_growth_card(),
            get_avg_monthly_growth_card(),
            get_best_month_card(),
            get_worst_month_card()
        ], cols=4)
        
        # Growth charts using chart grid
        def create_pension_value_chart():
            st.markdown("**Pension Portfolio Value**")
            fig_value = create_time_series_chart(
                monthly_pensions, 
                x_col='Month', 
                y_cols=['Value', 'RollingAvg'],
                title="Pension Portfolio Value"
            )
            if fig_value:
                st.plotly_chart(fig_value, use_container_width=True)
        
        def create_cumulative_growth_chart():
            if len(monthly_pensions) > 1:
                st.markdown("**Cumulative Growth**")
                fig_growth = create_time_series_chart(
                    monthly_pensions, 
                    x_col='Month', 
                    y_cols=['CumulativeGrowthPct'],
                    title="Cumulative Growth"
                )
                if fig_growth:
                    fig_growth.update_yaxes(tickformat='.1f')
                    st.plotly_chart(fig_growth, use_container_width=True)
            else:
                st.info("Not enough data for cumulative growth")
        
        create_chart_grid([create_pension_value_chart, create_cumulative_growth_chart], cols=2)
        
        # Monthly growth and volatility charts using chart grid
        def create_monthly_growth_chart():
            st.markdown("**Monthly Growth Rates**")
            mom_clean = monthly_pensions[['Month', 'MoM']].dropna()
            if not mom_clean.empty:
                fig_mom = create_bar_chart(
                    mom_clean,
                    x_col='Month',
                    y_col='MoM',
                    title="Monthly Growth Rates"
                )
                if fig_mom:
                    fig_mom.update_yaxes(tickformat='.2%')
                    fig_mom.update_traces(marker_color=['green' if x >= 0 else 'red' for x in mom_clean['MoM']])
                    st.plotly_chart(fig_mom, use_container_width=True)
            else:
                st.info("Not enough data for monthly growth")
        
        def create_volatility_chart():
            st.markdown("**Rolling Volatility (6-Month)**")
            fig_vol = create_time_series_chart(
                monthly_pensions, 
                x_col='Month', 
                y_cols=['RollingStd'],
                title="Rolling Volatility (6-Month)"
            )
            if fig_vol:
                st.plotly_chart(fig_vol, use_container_width=True)
        
        create_chart_grid([create_monthly_growth_chart, create_volatility_chart], cols=2)
        
        st.markdown("---")
        
        # --- Provider Analysis ---
        create_section_header("Provider Analysis", icon="🏢")
        
        # Provider distribution using chart grid
        provider_breakdown = pd.DataFrame([
            {'Provider': provider, 'Value': value}
            for provider, value in pension_metrics['latest_platform_breakdown'].items()
        ])
        
        def create_provider_pie_chart():
            st.markdown("**Current Provider Distribution**")
            if not provider_breakdown.empty:
                fig_provider = create_pie_chart(
                    provider_breakdown,
                    names_col='Provider',
                    values_col='Value',
                    title="Current Provider Distribution"
                )
                if fig_provider:
                    st.plotly_chart(fig_provider, use_container_width=True)
            else:
                st.info("No provider data available")
        
        def create_provider_bar_chart():
            st.markdown("**Provider Values**")
            if not provider_breakdown.empty:
                fig_provider_bar = create_bar_chart(
                    provider_breakdown,
                    x_col='Provider',
                    y_col='Value',
                    title="Provider Values"
                )
                if fig_provider_bar:
                    st.plotly_chart(fig_provider_bar, use_container_width=True)
            else:
                st.info("No provider data available")
        
        create_chart_grid([create_provider_pie_chart, create_provider_bar_chart], cols=2)
        
        # Provider performance over time
        st.markdown("**Provider Performance Over Time**")
        fig_value, fig_composition = create_asset_type_time_series(df, 'Pensions')
        
        if fig_value is not None:
            def create_pension_values_chart():
                st.markdown("**Pension Values by Provider**")
                st.plotly_chart(fig_value, use_container_width=True)
            
            def create_provider_composition_chart():
                st.markdown("**Provider Composition Over Time**")
                st.plotly_chart(fig_composition, use_container_width=True)
            
            create_chart_grid([create_pension_values_chart, create_provider_composition_chart], cols=2)
        else:
            st.info("Not enough data for provider time series analysis")
        
        st.markdown("---")
        
        # --- Retirement Planning Metrics ---
        create_section_header("Retirement Planning Metrics", icon="🎯")
        
        # Calculate retirement planning metrics using metric grid
        total_portfolio = df[df['Timestamp'].dt.to_period('M') == latest_month]['Value'].sum()
        pension_percentage = (pension_metrics['latest_value'] / total_portfolio * 100) if total_portfolio > 0 else 0
        
        def get_monthly_growth_card():
            if len(monthly_pensions) > 1:
                value_changes = monthly_pensions['Value'].diff().dropna()
                avg_monthly_change = value_changes.mean()
                return lambda: simple_card(
                    title="Est. Monthly Growth",
                    metric=f"£{avg_monthly_change:,.2f}",
                    caption="Average monthly increase"
                )
            else:
                return lambda: simple_card(
                    title="Est. Monthly Growth",
                    metric="N/A",
                    caption="Not enough data"
                )
        
        def get_annual_growth_card():
            if len(monthly_pensions) > 1:
                avg_monthly_rate = monthly_pensions['MoM'].mean()
                annual_rate = ((1 + avg_monthly_rate) ** 12 - 1) * 100
                return lambda: simple_card(
                    title="Projected Annual Growth",
                    metric=f"{annual_rate:.1f}%",
                    caption="Based on monthly average"
                )
            else:
                return lambda: simple_card(
                    title="Projected Annual Growth",
                    metric="N/A",
                    caption="Not enough data"
                )
        
        def get_years_tracked_card():
            if len(monthly_pensions) > 1:
                years_tracked = len(monthly_pensions) / 12
                return lambda: simple_card(
                    title="Years Tracked",
                    metric=f"{years_tracked:.1f}",
                    caption="Historical data period"
                )
            else:
                return lambda: simple_card(
                    title="Years Tracked",
                    metric="N/A",
                    caption="Not enough data"
                )
        
        create_metric_grid([
            lambda: simple_card(
                title="Pension Allocation",
                metric=f"{pension_percentage:.1f}%",
                caption="Of total portfolio"
            ),
            get_monthly_growth_card(),
            get_annual_growth_card(),
            get_years_tracked_card()
        ], cols=4)
        
        # Pension growth distribution using chart grid
        def create_value_distribution_chart():
            st.markdown("**Pension Value Distribution**")
            fig_dist = create_histogram(
                monthly_pensions,
                x_col='Value',
                title="Pension Value Distribution",
                nbins=10
            )
            if fig_dist:
                st.plotly_chart(fig_dist, use_container_width=True)
        
        def create_growth_distribution_chart():
            st.markdown("**Monthly Growth Distribution**")
            mom_clean = monthly_pensions[['Month', 'MoM']].dropna()
            if not mom_clean.empty:
                fig_growth_dist = create_histogram(
                    mom_clean,
                    x_col='MoM',
                    title="Monthly Growth Distribution",
                    nbins=8
                )
                if fig_growth_dist:
                    fig_growth_dist.update_xaxes(tickformat='.2%')
                    st.plotly_chart(fig_growth_dist, use_container_width=True)
            else:
                st.info("Not enough data for growth distribution")
        
        create_chart_grid([create_value_distribution_chart, create_growth_distribution_chart], cols=2)
        
        st.markdown("---")
        
        # --- Pension Scheme Analysis ---
        create_section_header("Pension Scheme Analysis", icon="📋")
        
        # Scheme breakdown (if Asset column exists)
        if 'Asset' in pension_df.columns:
            latest_pension_data = pension_df[pension_df['Month'] == latest_month]
            
            def create_scheme_distribution_chart():
                st.markdown("**Current Scheme Distribution**")
                scheme_breakdown = latest_pension_data.groupby('Asset')['Value'].sum().reset_index()
                if not scheme_breakdown.empty:
                    fig_scheme = px.pie(
                        scheme_breakdown,
                        values='Value',
                        names='Asset',
                        title=None,
                        hole=0.3
                    )
                    fig_scheme.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig_scheme, use_container_width=True)
                else:
                    st.info("No scheme data available")
            
            def create_scheme_provider_chart():
                st.markdown("**Scheme Values by Provider**")
                scheme_provider_breakdown = latest_pension_data.groupby(['Platform', 'Asset'])['Value'].sum().reset_index()
                if not scheme_provider_breakdown.empty:
                    fig_scheme_provider = px.bar(
                        scheme_provider_breakdown,
                        x='Platform',
                        y='Value',
                        color='Asset',
                        title=None,
                        labels={'Value': 'Value (GBP)', 'Platform': 'Provider', 'Asset': 'Scheme'}
                    )
                    st.plotly_chart(fig_scheme_provider, use_container_width=True)
                else:
                    st.info("No scheme-provider data available")
            
            create_chart_grid([create_scheme_distribution_chart, create_scheme_provider_chart], cols=2)
            
            # Scheme performance over time
            st.markdown("**Scheme Performance Over Time**")
            scheme_time_series = pension_df.groupby(['Month', 'Asset'])['Value'].sum().reset_index()
            
            if not scheme_time_series.empty:
                fig_scheme_time = px.line(
                    scheme_time_series,
                    x='Month',
                    y='Value',
                    color='Asset',
                    labels={'Value': 'Value (GBP)', 'Month': 'Month', 'Asset': 'Scheme'},
                    title=None
                )
                st.plotly_chart(fig_scheme_time, use_container_width=True)
            else:
                st.info("Not enough data for scheme time series analysis")
        else:
            st.info("Scheme breakdown not available - Asset column not found in data")
        
        st.markdown("---")
        
        # --- Pension Insights ---
        create_section_header("Pension Insights", icon="💡")
        
        # Generate insights based on data
        insights = []
        
        if pension_percentage > 50:
            insights.append("🏦 **High Pension Allocation**: Your pensions represent over 50% of your portfolio. This suggests a strong focus on retirement planning.")
        elif pension_percentage < 10:
            insights.append("⚠️ **Low Pension Allocation**: Your pensions are below 10% of your portfolio. Consider increasing pension contributions for retirement security.")
        else:
            insights.append("✅ **Balanced Pension Position**: Your pension allocation appears well-balanced for retirement planning.")
        
        if pension_metrics['mom_change'] is not None and pension_metrics['mom_change'] > 3:
            insights.append("📈 **Strong Pension Growth**: Your pensions have shown strong growth this month.")
        elif pension_metrics['mom_change'] is not None and pension_metrics['mom_change'] < -3:
            insights.append("📉 **Pension Decline**: Your pensions have declined this month. This may be normal market volatility.")
        
        if len(monthly_pensions) > 1:
            total_growth = ((monthly_pensions['Value'].iloc[-1] - monthly_pensions['Value'].iloc[0]) / monthly_pensions['Value'].iloc[0]) * 100
            if total_growth > 20:
                insights.append("🚀 **Excellent Long-term Growth**: Your pensions have grown significantly since tracking began.")
            elif total_growth < 5:
                insights.append("📊 **Moderate Growth**: Your pensions have shown moderate growth. Consider reviewing contribution levels.")
        
        if len(monthly_pensions) > 1:
            avg_monthly_rate = monthly_pensions['MoM'].mean()
            annual_rate = ((1 + avg_monthly_rate) ** 12 - 1) * 100
            if annual_rate > 8:
                insights.append("⭐ **Strong Annual Growth**: Your projected annual growth rate is excellent for retirement planning.")
            elif annual_rate < 3:
                insights.append("⚠️ **Low Growth Rate**: Your projected annual growth rate is below typical pension growth expectations.")
        
        if len(insights) > 0:
            for insight in insights:
                st.markdown(insight)
        else:
            st.info("No specific insights available with current data.")
    
    else:
        st.error("❌ No pension data found in your portfolio.")
        st.info("💡 Make sure your data includes assets classified as 'Pensions' type.")

else:
    st.error("❌ Data could not be loaded. Please check your data file.")
    st.info("💡 Make sure you have uploaded data through the sidebar on the Home page.") 