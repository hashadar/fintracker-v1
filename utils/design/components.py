import streamlit as st
from .tokens import BRAND_SUCCESS, BRAND_ERROR
from .cards import emphasis_card, complex_emphasis_card, simple_card


def create_metric_grid(metrics_list, cols=4):
    """
    Display a list of metric cards in a responsive grid layout.
    Args:
        metrics_list (list of callables): Each item is a function that renders a metric card (e.g., a lambda or partial).
        cols (int): Number of columns in the grid.
    """
    columns = st.columns(cols)
    for i, metric in enumerate(metrics_list):
        with columns[i % cols]:
            # Add container with consistent height for better alignment
            st.markdown('<div style="height: 100%; display: flex; flex-direction: column;">', unsafe_allow_html=True)
            metric()
            st.markdown('</div>', unsafe_allow_html=True)


def create_chart_grid(charts_list, cols=2):
    """
    Display a list of charts in a responsive grid layout.
    Args:
        charts_list (list of callables): Each item is a function that renders a chart (e.g., a lambda or partial).
        cols (int): Number of columns in the grid.
    """
    columns = st.columns(cols)
    for i, chart in enumerate(charts_list):
        with columns[i % cols]:
            chart()


def create_section_header(title, icon="📊"):
    """
    Render a standardized section header with an optional icon.
    Args:
        title (str): Section title.
        icon (str): Emoji or icon to display before the title.
    """
    st.markdown(f"### {icon} {title}")


def create_page_header(title, description):
    """
    Render a standardized page header with a title and description.
    Args:
        title (str): Page title.
        description (str): Short description or subtitle.
    """
    st.markdown(f"""
        <h1 style='margin-bottom:0.5rem'>{title}</h1>
        <p style='color:var(--text-secondary);margin-bottom:2rem'>{description}</p>
    """, unsafe_allow_html=True)


def create_time_period_breadcrumb(latest_month, prev_month, ytd_start_month, display_date_format="%B %Y"):
    """
    Create a standardized time period breadcrumb showing latest month, previous month, and YTD start.
    
    Args:
        latest_month: Latest month datetime or period object
        prev_month: Previous month datetime or period object
        ytd_start_month: YTD start month datetime or period object
        display_date_format: Date format string for displaying dates
    """
    if latest_month is None:
        st.caption("📅 No data available")
        return
    
    # Build the breadcrumb with all three periods
    breadcrumb_text = (
        f"📅 Latest Month: {latest_month.strftime(display_date_format)} | "
        f"Previous Month: {prev_month.strftime(display_date_format) if prev_month is not None else 'N/A'} | "
        f"YTD Start: {ytd_start_month.strftime(display_date_format) if ytd_start_month is not None else 'N/A'}"
    )
    st.caption(breadcrumb_text)


def create_asset_summary_cards(asset_metrics, asset_type_name, emphasis_color, currency_format):
    """
    Create standardized asset summary cards section with main emphasis card and metric grid.
    
    Args:
        asset_metrics (dict): Dictionary containing asset metrics with keys:
            - latest_value: Current total value
            - mom_change: Month-over-month change percentage (can be None)
            - ytd_change: Year-to-date change percentage (can be None)
            - platforms: Number of platforms/providers
            - assets: Number of assets/instruments
            - months_tracked: Number of months tracked
        asset_type_name (str): Name of the asset type (e.g., "Cash Position", "Investment Portfolio", "Pension Portfolio")
        emphasis_color (str): Color for the emphasis card styling
        currency_format (str): Currency format string for formatting values
    """
    
    # Main asset total card
    complex_emphasis_card(
        title=f"Total {asset_type_name}",
        metric=currency_format.format(asset_metrics['latest_value']),
        mom_change=(f"{asset_metrics['mom_change']:+.2f}% MoM" if asset_metrics['mom_change'] is not None else None),
        ytd_change=None,  # Will calculate YTD separately if needed
        caption=f"{asset_type_name.lower()} across {asset_metrics['platforms']} {'providers' if 'pension' in asset_type_name.lower() else 'platforms'}",
        mom_color="normal" if asset_metrics['mom_change'] is not None and asset_metrics['mom_change'] >= 0 else "inverse",
        emphasis_color=emphasis_color
    )
    
    # Asset metrics cards using metric grid
    def get_ytd_card():
        if asset_metrics.get('ytd_change') is not None:
            # Use green for positive, red for negative
            ytd_color = BRAND_SUCCESS if asset_metrics['ytd_change'] >= 0 else BRAND_ERROR
            return lambda: emphasis_card(
                title="YTD Change",
                metric=f"{asset_metrics['ytd_change']:+.2f}%",
                caption="Year-to-date change",
                emphasis_color=ytd_color
            )
        else:
            return lambda: simple_card(
                title="YTD Change",
                metric="N/A",
                caption="Not enough data"
            )
    
    # Determine the appropriate labels based on asset type
    platform_label = "Providers" if "pension" in asset_type_name.lower() else "Platforms"
    asset_label = "Schemes" if "pension" in asset_type_name.lower() else "Assets"
    
    create_metric_grid([
        get_ytd_card(),
        lambda: simple_card(
            title=platform_label,
            metric=str(asset_metrics['platforms']),
            caption=f"{asset_type_name.lower()} {'providers' if 'pension' in asset_type_name.lower() else 'accounts'}"
        ),
        lambda: simple_card(
            title=asset_label,
            metric=str(asset_metrics['assets']),
            caption=f"{asset_type_name.lower()} {'schemes' if 'pension' in asset_type_name.lower() else 'instruments'}"
        ),
        lambda: simple_card(
            title="Months Tracked",
            metric=str(asset_metrics['months_tracked']),
            caption="Historical period"
        )
    ], cols=4) 


def create_summary_statistics(df, latest_month, display_date_format="%B %Y"):
    """
    Create standardized summary statistics section with key metrics.
    
    Args:
        df (DataFrame): The main data DataFrame
        latest_month: Latest month datetime or period object
        display_date_format (str): Date format string for displaying dates
    """
    from .cards import simple_card
    
    # Calculate summary statistics
    total_platforms = df['Platform'].nunique()
    total_assets = df['Asset'].nunique() if 'Asset' in df.columns else 0
    months_tracked = df['Timestamp'].dt.to_period('M').nunique()
    latest_records = len(df[df['Timestamp'].dt.to_period('M') == latest_month])
    
    # Create section header
    create_section_header("Summary Statistics", icon="📊")
    
    # Create metric grid with summary cards
    create_metric_grid([
        lambda: simple_card(
            title="Total Platforms",
            metric=str(total_platforms),
            caption="Unique financial platforms"
        ),
        lambda: simple_card(
            title="Total Assets",
            metric=str(total_assets),
            caption="Unique asset types"
        ),
        lambda: simple_card(
            title="Months Tracked",
            metric=str(months_tracked),
            caption="Historical data period"
        ),
        lambda: simple_card(
            title="Latest Records",
            metric=str(latest_records),
            caption=f"Records in {latest_month.strftime(display_date_format)}"
        )
    ], cols=4) 


def create_portfolio_analytics_charts(df, asset_type=None, section_title="Portfolio Analytics", section_icon="📈"):
    """
    Create standardized portfolio analytics charts section.
    
    Args:
        df (DataFrame): The main data DataFrame
        asset_type (str, optional): Asset type to filter by (e.g., 'Cash', 'Investments', 'Pensions')
        section_title (str): Title for the analytics section
        section_icon (str): Icon for the section header
    """
    from utils import (
        get_monthly_aggregation, calculate_rolling_metrics, create_allocation_time_series, create_platform_allocation_time_series
    )
    from utils.charts import (
        create_time_series_chart, create_bar_chart, get_chart_label
    )
    
    # Create section header
    create_section_header(section_title, icon=section_icon)
    
    # Filter data by asset type if specified
    if asset_type:
        from utils import filter_by_asset_type
        filtered_df = filter_by_asset_type(df, asset_type)
    else:
        filtered_df = df
    
    # Prepare data for analysis
    monthly_totals = get_monthly_aggregation(filtered_df)
    monthly_totals = calculate_rolling_metrics(monthly_totals, window=3)
    monthly_totals['MoM'] = monthly_totals['Value'].pct_change()
    
    # Create allocation time series data (only for all assets view)
    allocation_df = None
    if asset_type is None:
        allocation_df = create_allocation_time_series(df)
    
    # Portfolio charts using chart grid
    def create_portfolio_value_chart():
        st.markdown("**Portfolio Value & Rolling Average**")
        fig_value = create_time_series_chart(
            monthly_totals, 
            x_col='Month', 
            y_cols=['Value', 'Rolling_3M_Avg'],
            x_label=get_chart_label('month'),
            y_label=get_chart_label('value'),
            y_format='currency'
        )
        st.plotly_chart(fig_value, use_container_width=True)

    def create_allocation_time_series_chart():
        st.markdown("**Asset Allocation Over Time**")
        if allocation_df is not None and not allocation_df.empty:
            # Get the allocation columns (excluding 'Month')
            allocation_cols = [col for col in allocation_df.columns if 'Allocation %' in col]
            fig_allocation = create_time_series_chart(
                allocation_df,
                x_col='Month',
                y_cols=allocation_cols,
                x_label=get_chart_label('month'),
                y_label='Allocation %',
                y_format='percentage'
            )
            st.plotly_chart(fig_allocation, use_container_width=True)
        else:
            st.info("No allocation time series data available")

    def create_current_allocation_pie_chart():
        st.markdown("**Current Asset Allocation**")
        if asset_type is None:
            # For all assets view, show asset type allocation
            from utils import calculate_allocation_metrics
            allocation_metrics, _, _, _ = calculate_allocation_metrics(df)
            
            allocation_data = []
            for asset_type_name, metrics in allocation_metrics.items():
                if asset_type_name != 'Total':
                    allocation_data.append({
                        'Asset Type': asset_type_name,
                        'Value': metrics.get('current', 0),
                        'Allocation': metrics.get('allocation', 0)
                    })
            if allocation_data:
                import pandas as pd
                allocation_df = pd.DataFrame(allocation_data)
                from utils.charts import create_pie_chart
                fig_allocation = create_pie_chart(
                    allocation_df,
                    names_col='Asset Type',
                    values_col='Value'
                )
                st.plotly_chart(fig_allocation, use_container_width=True)
            else:
                st.info("No allocation data available")
        else:
            # For specific asset type, show platform allocation
            from utils import get_asset_breakdown
            platform_breakdown = get_asset_breakdown(filtered_df, 'platform')
            if not platform_breakdown.empty:
                from utils.charts import create_pie_chart
                fig_platform = create_pie_chart(
                    platform_breakdown,
                    names_col='Platform',
                    values_col='Value'
                )
                st.plotly_chart(fig_platform, use_container_width=True)
            else:
                st.info(f"No platform data available for {asset_type}")
    
    def create_total_portfolio_mom_chart():
        st.markdown("**Total Portfolio Month-over-Month Change**")
        mom_clean = monthly_totals[['Month', 'MoM']].dropna()
        if not mom_clean.empty:
            fig_mom = create_bar_chart(
                mom_clean,
                x_col='Month',
                y_col='MoM',
                x_label=get_chart_label('month'),
                y_label=get_chart_label('percentage_change'),
                y_format='percentage'
            )
            fig_mom.update_traces(marker_color=['green' if x >= 0 else 'red' for x in mom_clean['MoM']])
            st.plotly_chart(fig_mom, use_container_width=True)
        else:
            st.info("Not enough data for monthly changes")

    def create_platform_allocation_time_series_chart():
        st.markdown("**Platform Allocation Over Time**")
        platform_allocation_df = create_platform_allocation_time_series(df, asset_type)
        if platform_allocation_df is not None and not platform_allocation_df.empty:
            platform_cols = [col for col in platform_allocation_df.columns if col != 'Month']
            fig_platform_allocation = create_time_series_chart(
                platform_allocation_df,
                x_col='Month',
                y_cols=platform_cols,
                x_label=get_chart_label('month'),
                y_label='Platform Allocation %',
                y_format='percentage'
            )
            st.plotly_chart(fig_platform_allocation, use_container_width=True)
        else:
            st.info("No platform allocation time series data available")

    # Create charts based on asset type
    if asset_type is None:
        # All assets view - show allocation time series and asset type pie chart
        create_chart_grid([create_portfolio_value_chart, create_allocation_time_series_chart], cols=2)
        create_chart_grid([create_total_portfolio_mom_chart, create_current_allocation_pie_chart], cols=2)
    else:
        # Specific asset type view - show platform allocation time series and platform pie chart
        create_chart_grid([create_portfolio_value_chart, create_platform_allocation_time_series_chart], cols=2)
        create_chart_grid([create_total_portfolio_mom_chart, create_current_allocation_pie_chart], cols=2) 


def create_investment_asset_analysis(df, asset_type=None):
    """
    Create detailed investment asset analysis with allocation time series, MoM changes, and returns distribution.
    
    Args:
        df (DataFrame): The main data DataFrame
        asset_type (str, optional): Asset type to filter (default: Investments)
    """
    from utils import filter_by_asset_type, get_monthly_aggregation, calculate_rolling_metrics
    from utils.charts import create_time_series_chart, create_bar_chart, create_box_plot, get_chart_label
    import pandas as pd
    
    # Create section header
    create_section_header("Asset-Level Analysis", icon="📊")
    
    # Filter for investment assets
    investment_df = filter_by_asset_type(df, asset_type)
    
    if investment_df.empty:
        st.info("No investment data available for asset analysis")
        return
    
    # Prepare monthly data by asset
    investment_df['Month'] = investment_df['Timestamp'].dt.to_period('M')
    monthly_by_asset = investment_df.groupby(['Month', 'Asset'])['Value'].sum().reset_index()
    monthly_by_asset['Month'] = monthly_by_asset['Month'].dt.to_timestamp()
    
    if monthly_by_asset.empty:
        st.info("No monthly asset data available")
        return
    
    # 1. Percentage Returns Over Time
    def create_asset_returns_time_series():
        st.markdown("**Percentage Returns Over Time**")
        
        # Calculate percentage returns for each asset over time
        returns_data = []
        for asset in monthly_by_asset['Asset'].unique():
            asset_data = monthly_by_asset[monthly_by_asset['Asset'] == asset].sort_values('Month')
            asset_data['Return'] = asset_data['Value'].pct_change()
            asset_data['Asset'] = asset
            returns_data.append(asset_data[['Month', 'Asset', 'Return']])
        
        if returns_data:
            returns_df = pd.concat(returns_data, ignore_index=True)
            returns_clean = returns_df.dropna()
            
            if not returns_clean.empty:
                # Pivot to get assets as columns
                returns_pivot = returns_clean.pivot(index='Month', columns='Asset', values='Return')
                returns_pivot = returns_pivot.reset_index()
                
                # Get asset columns (excluding Month)
                asset_cols = [col for col in returns_pivot.columns if col != 'Month']
                
                fig_returns = create_time_series_chart(
                    returns_pivot,
                    x_col='Month',
                    y_cols=asset_cols,
                    x_label=get_chart_label('month'),
                    y_label='Percentage Return',
                    y_format='percentage'
                )
                st.plotly_chart(fig_returns, use_container_width=True)
            else:
                st.info("Not enough data for returns analysis")
        else:
            st.info("No returns data available")

    # 2. Asset Allocation Over Time (Percentage)
    def create_asset_allocation_time_series():
        st.markdown("**Asset Allocation Over Time**")
        
        # Calculate percentage allocation for each asset over time
        allocation_data = []
        for month in monthly_by_asset['Month'].unique():
            month_data = monthly_by_asset[monthly_by_asset['Month'] == month]
            total_value = month_data['Value'].sum()
            month_allocation = {'Month': month}
            for asset in month_data['Asset'].unique():
                asset_value = month_data[month_data['Asset'] == asset]['Value'].iloc[0]
                allocation_pct = (asset_value / total_value) if total_value > 0 else 0
                month_allocation[asset] = allocation_pct
            allocation_data.append(month_allocation)
        allocation_df = pd.DataFrame(allocation_data)
        if not allocation_df.empty:
            asset_cols = [col for col in allocation_df.columns if col != 'Month']
            fig_allocation = create_time_series_chart(
                allocation_df,
                x_col='Month',
                y_cols=asset_cols,
                x_label=get_chart_label('month'),
                y_label='Asset Allocation %',
                y_format='percentage'
            )
            st.plotly_chart(fig_allocation, use_container_width=True)
        else:
            st.info("No allocation data available")

    # 3. Changes Bar Chart
    def create_mom_changes_chart():
        st.markdown("**Month-over-Month Changes by Asset**")
        
        # Calculate MoM changes for each asset
        mom_data = []
        for asset in monthly_by_asset['Asset'].unique():
            asset_data = monthly_by_asset[monthly_by_asset['Asset'] == asset].sort_values('Month')
            asset_data['MoM'] = asset_data['Value'].pct_change()
            
            # Add asset name to each row
            asset_data['Asset'] = asset
            mom_data.append(asset_data[['Month', 'Asset', 'MoM']])
        
        if mom_data:
            mom_df = pd.concat(mom_data, ignore_index=True)
            mom_clean = mom_df.dropna()
            
            if not mom_clean.empty:
                # Create bar chart with asset as color
                fig_mom = create_bar_chart(
                    mom_clean,
                    x_col='Month',
                    y_col='MoM',
                    color_col='Asset',
                    x_label=get_chart_label('month'),
                    y_label=get_chart_label('percentage_change'),
                    y_format='percentage'
                )
                st.plotly_chart(fig_mom, use_container_width=True)
            else:
                st.info("Not enough data for MoM analysis")
        else:
            st.info("No MoM data available")
    
    # 3. Returns Distribution Box Plot
    def create_returns_boxplot():
        st.markdown("**Returns Distribution by Asset**")
        
        # Calculate returns for each asset
        returns_data = []
        for asset in monthly_by_asset['Asset'].unique():
            asset_data = monthly_by_asset[monthly_by_asset['Asset'] == asset].sort_values('Month')
            asset_data['Return'] = asset_data['Value'].pct_change()
            asset_data['Asset'] = asset
            returns_data.append(asset_data[['Asset', 'Return']])
        
        if returns_data:
            returns_df = pd.concat(returns_data, ignore_index=True)
            returns_clean = returns_df.dropna()
            
            if not returns_clean.empty:
                fig_box = create_box_plot(
                    returns_clean,
                    y_col='Return',
                    color_col='Asset',
                    y_label=get_chart_label('percentage_change'),
                    y_format='percentage'
                )
                st.plotly_chart(fig_box, use_container_width=True)
            else:
                st.info("Not enough data for returns analysis")
        else:
            st.info("No returns data available")
    
    # Create charts in 2x2 grid layout
    create_chart_grid([create_asset_returns_time_series, create_asset_allocation_time_series], cols=2)
    create_chart_grid([create_mom_changes_chart, create_returns_boxplot], cols=2) 