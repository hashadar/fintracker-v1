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
st.set_page_config(page_title="Investments - FinTracker", layout="wide")

# Load data
df = load_data()

if df is not None and not df.empty:
    # Filter for investment assets
    investment_df = df[df['Asset_Type'] == 'Investments'].copy()
    
    if not investment_df.empty:
        create_page_header(
            title="📈 Investment Portfolio Dashboard",
            description="Comprehensive analysis of your investment performance and asset allocation"
        )
        
        # Calculate investment-specific metrics
        investment_metrics = calculate_asset_type_metrics(df, 'Investments')
        
        # Get latest month for display
        latest_month = investment_df['Timestamp'].dt.to_period('M').max()
        
        # Display time period info
        st.caption(f"📅 Latest Month: {latest_month.strftime('%B %Y')}")
        
        # --- Investment Summary Cards ---
        create_section_header("Investment Portfolio Summary", icon="🎯")
        
        # Main investment total card
        complex_emphasis_card(
            title="Total Investment Portfolio",
            metric=f"£{investment_metrics['latest_value']:,.2f}",
            mom_change=(f"{investment_metrics['mom_change']:+.2f}%" if investment_metrics['mom_change'] is not None else None),
            ytd_change=None,  # Will calculate YTD separately
            caption=f"Investment portfolio across {investment_metrics['platforms']} platforms",
            mom_color="normal" if investment_metrics['mom_change'] is not None and investment_metrics['mom_change'] >= 0 else "inverse",
            emphasis_color=BRAND_PRIMARY
        )
        
        # Investment metrics cards using metric grid
        def get_mom_return_card():
            if investment_metrics['mom_change'] is not None:
                return lambda: simple_card(
                    title="MoM Return",
                    metric=f"{investment_metrics['mom_change']:+.2f}%",
                    caption="Month-over-month return"
                )
            else:
                return lambda: simple_card(
                    title="MoM Return",
                    metric="N/A",
                    caption="Not enough data"
                )
        
        create_metric_grid([
            lambda: simple_card(
                title="Platforms",
                metric=str(investment_metrics['platforms']),
                caption="Investment accounts"
            ),
            lambda: simple_card(
                title="Assets",
                metric=str(investment_metrics['assets']),
                caption="Investment instruments"
            ),
            lambda: simple_card(
                title="Months Tracked",
                metric=str(investment_metrics['months_tracked']),
                caption="Historical period"
            ),
            get_mom_return_card()
        ], cols=4)
        
        st.markdown("---")
        
        # --- Performance Analytics ---
        create_section_header("Performance Analytics", icon="📊")
        
        # Prepare data for performance analysis
        investment_df['Month'] = investment_df['Timestamp'].dt.to_period('M').dt.to_timestamp()
        monthly_investments = investment_df.groupby('Month')['Value'].sum().reset_index()
        monthly_investments['RollingAvg'] = monthly_investments['Value'].rolling(window=3).mean()
        monthly_investments['RollingStd'] = monthly_investments['Value'].rolling(window=3).std()
        monthly_investments['MoM'] = monthly_investments['Value'].pct_change()
        
        # Calculate drawdown
        running_max = monthly_investments['Value'].cummax()
        monthly_investments['Drawdown'] = (monthly_investments['Value'] - running_max) / running_max
        
        # Performance metrics using metric grid
        max_drawdown = monthly_investments['Drawdown'].min()
        avg_monthly_return = monthly_investments['MoM'].mean()
        
        def get_best_month_card():
            if not monthly_investments['MoM'].dropna().empty:
                best_month = monthly_investments.loc[monthly_investments['MoM'].idxmax()]
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
            if not monthly_investments['MoM'].dropna().empty:
                worst_month = monthly_investments.loc[monthly_investments['MoM'].idxmin()]
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
            lambda: simple_card(
                title="Max Drawdown",
                metric=f"{max_drawdown:.2%}",
                caption="Largest peak-to-trough decline"
            ),
            get_best_month_card(),
            get_worst_month_card(),
            lambda: simple_card(
                title="Avg Monthly Return",
                metric=f"{avg_monthly_return:.2%}",
                caption="Mean monthly performance"
            )
        ], cols=4)
        
        # Performance charts using chart grid
        def create_investment_value_chart():
            st.markdown("**Investment Portfolio Value**")
            fig_value = create_time_series_chart(
                monthly_investments, 
                x_col='Month', 
                y_cols=['Value', 'RollingAvg'],
                title="Investment Portfolio Value"
            )
            if fig_value:
                st.plotly_chart(fig_value, use_container_width=True)
        
        def create_returns_distribution_chart():
            st.markdown("**Monthly Returns Distribution**")
            mom_clean = monthly_investments[['Month', 'MoM']].dropna()
            if not mom_clean.empty:
                fig_returns = create_histogram(
                    mom_clean, 
                    x_col='MoM',
                    title="Monthly Returns Distribution",
                    nbins=10
                )
                if fig_returns:
                    fig_returns.update_xaxes(tickformat='.2%')
                    st.plotly_chart(fig_returns, use_container_width=True)
            else:
                st.info("Not enough data for returns distribution")
        
        create_chart_grid([create_investment_value_chart, create_returns_distribution_chart], cols=2)
        
        # Drawdown and volatility charts using chart grid
        def create_drawdown_chart():
            st.markdown("**Drawdown Over Time**")
            fig_drawdown = create_time_series_chart(
                monthly_investments, 
                x_col='Month', 
                y_cols=['Drawdown'],
                title="Drawdown Over Time"
            )
            if fig_drawdown:
                fig_drawdown.update_yaxes(tickformat='.2%')
            st.plotly_chart(fig_drawdown, use_container_width=True)
        
        def create_volatility_chart():
            st.markdown("**Rolling Volatility (3-Month)**")
            fig_vol = create_time_series_chart(
                monthly_investments, 
                x_col='Month', 
                y_cols=['RollingStd'],
                title="Rolling Volatility (3-Month)"
            )
            if fig_vol:
                st.plotly_chart(fig_vol, use_container_width=True)
        
        create_chart_grid([create_drawdown_chart, create_volatility_chart], cols=2)
        
        st.markdown("---")
        
        # --- Platform Analysis ---
        create_section_header("Platform Analysis", icon="🏦")
        
        # Platform distribution using chart grid
        platform_breakdown = pd.DataFrame([
            {'Platform': platform, 'Value': value}
            for platform, value in investment_metrics['latest_platform_breakdown'].items()
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
                if fig_platform:
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
                if fig_platform_bar:
                    st.plotly_chart(fig_platform_bar, use_container_width=True)
            else:
                st.info("No platform data available")
        
        create_chart_grid([create_platform_pie_chart, create_platform_bar_chart], cols=2)
        
        # Platform performance over time
        st.markdown("**Platform Performance Over Time**")
        fig_value, fig_composition = create_asset_type_time_series(df, 'Investments')
        
        if fig_value is not None:
            def create_investment_values_chart():
                st.markdown("**Investment Values by Platform**")
                st.plotly_chart(fig_value, use_container_width=True)
            
            def create_platform_composition_chart():
                st.markdown("**Platform Composition Over Time**")
                st.plotly_chart(fig_composition, use_container_width=True)
            
            create_chart_grid([create_investment_values_chart, create_platform_composition_chart], cols=2)
        else:
            st.info("Not enough data for platform time series analysis")
        
        st.markdown("---")
        
        # --- Asset Allocation Analysis ---
        create_section_header("Asset Allocation Analysis", icon="🏗️")
        
        # Asset breakdown (if Asset column exists)
        if 'Asset' in investment_df.columns:
            latest_investment_data = investment_df[investment_df['Month'] == latest_month]
            
            def create_asset_distribution_chart():
                st.markdown("**Current Asset Distribution**")
                asset_breakdown = latest_investment_data.groupby('Asset')['Value'].sum().reset_index()
                if not asset_breakdown.empty:
                    fig_asset = create_pie_chart(
                        asset_breakdown,
                        names_col='Asset',
                        values_col='Value',
                        title="Current Asset Distribution"
                    )
                    if fig_asset:
                        st.plotly_chart(fig_asset, use_container_width=True)
                else:
                    st.info("No asset data available")
            
            def create_asset_platform_chart():
                st.markdown("**Asset Values by Platform**")
                asset_platform_breakdown = latest_investment_data.groupby(['Platform', 'Asset'])['Value'].sum().reset_index()
                if not asset_platform_breakdown.empty:
                    fig_asset_platform = create_bar_chart(
                        asset_platform_breakdown,
                        x_col='Platform',
                        y_col='Value',
                        color_col='Asset',
                        title="Asset Values by Platform"
                    )
                    if fig_asset_platform:
                        st.plotly_chart(fig_asset_platform, use_container_width=True)
                else:
                    st.info("No asset-platform data available")
            
            create_chart_grid([create_asset_distribution_chart, create_asset_platform_chart], cols=2)
            
            # Asset performance over time
            st.markdown("**Asset Performance Over Time**")
            asset_time_series = investment_df.groupby(['Month', 'Asset'])['Value'].sum().reset_index()
            
            if not asset_time_series.empty:
                # Get unique assets for y_cols
                unique_assets = asset_time_series['Asset'].unique()
                asset_pivot = asset_time_series.pivot(index='Month', columns='Asset', values='Value').reset_index()
                
                fig_asset_time = create_time_series_chart(
                    asset_pivot,
                    x_col='Month',
                    y_cols=unique_assets.tolist(),
                    title="Asset Performance Over Time"
                )
                if fig_asset_time:
                    st.plotly_chart(fig_asset_time, use_container_width=True)
            else:
                st.info("Not enough data for asset time series analysis")
        else:
            st.info("Asset breakdown not available - Asset column not found in data")
        
        st.markdown("---")
        
        # --- Risk Analysis ---
        create_section_header("Risk Analysis", icon="⚠️")
        
        # Calculate risk metrics using metric grid
        total_portfolio = df[df['Timestamp'].dt.to_period('M') == latest_month]['Value'].sum()
        investment_percentage = (investment_metrics['latest_value'] / total_portfolio * 100) if total_portfolio > 0 else 0
        investment_volatility = monthly_investments['Value'].std()
        
        def get_sharpe_ratio_card():
            if not monthly_investments['MoM'].dropna().empty:
                sharpe_ratio = monthly_investments['MoM'].mean() / monthly_investments['MoM'].std() if monthly_investments['MoM'].std() > 0 else 0
                return lambda: simple_card(
                    title="Sharpe Ratio",
                    metric=f"{sharpe_ratio:.3f}",
                    caption="Risk-adjusted return"
                )
            else:
                return lambda: simple_card(
                    title="Sharpe Ratio",
                    metric="N/A",
                    caption="Not enough data"
                )
        
        def get_var_card():
            if not monthly_investments['MoM'].dropna().empty:
                var_95 = monthly_investments['MoM'].quantile(0.05)
                return lambda: simple_card(
                    title="VaR (95%)",
                    metric=f"{var_95:.2%}",
                    caption="Value at Risk"
                )
            else:
                return lambda: simple_card(
                    title="VaR (95%)",
                    metric="N/A",
                    caption="Not enough data"
                )
        
        create_metric_grid([
            lambda: simple_card(
                title="Investment Allocation",
                metric=f"{investment_percentage:.1f}%",
                caption="Of total portfolio"
            ),
            lambda: simple_card(
                title="Portfolio Volatility",
                metric=f"£{investment_volatility:,.2f}",
                caption="Standard deviation"
            ),
            get_sharpe_ratio_card(),
            get_var_card()
        ], cols=4)
        
        # Risk distribution charts using chart grid
        def create_value_distribution_chart():
            st.markdown("**Investment Value Distribution**")
            fig_dist = px.histogram(
                monthly_investments,
                x='Value',
                nbins=10,
                labels={'Value': 'Investment Value (GBP)', 'count': 'Frequency'},
                title=None
            )
            st.plotly_chart(fig_dist, use_container_width=True)
        
        def create_returns_box_plot():
            st.markdown("**Monthly Returns Box Plot**")
            mom_clean = monthly_investments[['Month', 'MoM']].dropna()
            if not mom_clean.empty:
                fig_box = px.box(
                    mom_clean,
                    y='MoM',
                    labels={'MoM': 'Monthly Return'},
                    title=None
                )
                fig_box.update_yaxes(tickformat='.2%')
                st.plotly_chart(fig_box, use_container_width=True)
            else:
                st.info("Not enough data for returns box plot")
        
        create_chart_grid([create_value_distribution_chart, create_returns_box_plot], cols=2)
        
        st.markdown("---")
        
        # --- Investment Insights ---
        create_section_header("Investment Insights", icon="💡")
        
        # Generate insights based on data
        insights = []
        
        if investment_percentage > 70:
            insights.append("📈 **High Investment Allocation**: Your investments represent over 70% of your portfolio. This suggests an aggressive investment strategy.")
        elif investment_percentage < 20:
            insights.append("📉 **Low Investment Allocation**: Your investments are below 20% of your portfolio. Consider if this aligns with your long-term goals.")
        else:
            insights.append("✅ **Balanced Investment Position**: Your investment allocation appears well-balanced.")
        
        if investment_metrics['mom_change'] is not None and investment_metrics['mom_change'] > 5:
            insights.append("🚀 **Strong Investment Performance**: Your investments have shown strong growth this month.")
        elif investment_metrics['mom_change'] is not None and investment_metrics['mom_change'] < -5:
            insights.append("📉 **Investment Decline**: Your investments have declined this month. Review your strategy if this continues.")
        
        if not monthly_investments['MoM'].dropna().empty:
            sharpe_ratio = monthly_investments['MoM'].mean() / monthly_investments['MoM'].std() if monthly_investments['MoM'].std() > 0 else 0
            if sharpe_ratio > 1:
                insights.append("⭐ **Excellent Risk-Adjusted Returns**: Your Sharpe ratio indicates strong risk-adjusted performance.")
            elif sharpe_ratio < 0:
                insights.append("⚠️ **Poor Risk-Adjusted Returns**: Your Sharpe ratio suggests poor risk-adjusted performance.")
        
        if max_drawdown < -0.15:
            insights.append("⚠️ **Significant Drawdown**: Your portfolio has experienced a significant drawdown. Consider risk management strategies.")
        
        if len(insights) > 0:
            for insight in insights:
                st.markdown(insight)
        else:
            st.info("No specific insights available with current data.")
    
    else:
        st.error("❌ No investment data found in your portfolio.")
        st.info("💡 Make sure your data includes assets classified as 'Investments' type.")

else:
    st.error("❌ Data could not be loaded. Please check your data file.")
    st.info("💡 Make sure you have uploaded data through the sidebar on the Home page.") 