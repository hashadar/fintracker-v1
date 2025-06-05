import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
from utils.visualizations import kpi_card
from utils import load_data

# Load data at the top of the page
df = load_data()

# Ensure data is loaded before rendering the page
if df is not None:
    st.header("All Assets Deep Dive")
    all_df = df.copy()
    all_df['Month'] = all_df['Timestamp'].dt.to_period('M').dt.to_timestamp()
    all_monthly = all_df.groupby('Month')['Value'].sum().reset_index()
    all_monthly['RollingAvg'] = all_monthly['Value'].rolling(window=3).mean()
    all_monthly['RollingStd'] = all_monthly['Value'].rolling(window=3).std()
    running_max = all_monthly['Value'].cummax()
    drawdown = (all_monthly['Value'] - running_max) / running_max
    all_monthly['Drawdown'] = drawdown
    all_monthly['MoM'] = all_monthly['Value'].pct_change()
    
    # Ensure there's enough data for best/worst month calculation
    if not all_monthly['MoM'].dropna().empty:
        best_month = all_monthly.loc[all_monthly['MoM'].idxmax()]
        worst_month = all_monthly.loc[all_monthly['MoM'].idxmin()]
    else:
        best_month = None
        worst_month = None
        
    max_drawdown = drawdown.min()

    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        kpi_card(
            label="Max Drawdown",
            value=f"{max_drawdown:.2%}",
            help_text="The largest peak-to-trough decline in portfolio value."
        )
    with kpi2:
        kpi_card(
            label="Best Month (MoM %)",
            value=f"{best_month['Month'].strftime('%b %Y')}: {best_month['MoM']*100:.2f}%" if best_month is not None else "N/A",
            help_text="The month with the highest percentage growth."
        )
    with kpi3:
        kpi_card(
            label="Worst Month (MoM %)",
            value=f"{worst_month['Month'].strftime('%b %Y')}: {worst_month['MoM']*100:.2f}%" if worst_month is not None else "N/A",
            help_text="The month with the largest percentage decline."
        )
        
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Value & 3-Month Rolling Avg**")
        st.plotly_chart(
            px.line(all_monthly, x='Month', y=['Value', 'RollingAvg'],
                    labels={'value': 'Value (GBP)', 'Month': 'Month'},
                    title=None),
            use_container_width=True
        )
    with col2:
        st.markdown("**Rolling Volatility (Std Dev)**")
        st.plotly_chart(
            px.line(all_monthly, x='Month', y='RollingStd', labels={'RollingStd': 'Std Dev', 'Month': 'Month'}, title=None),
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
            px.line(all_monthly, x='Month', y='Drawdown', labels={'Drawdown': 'Drawdown', 'Month': 'Month'}, title=None),
            use_container_width=True
        )
        
    st.markdown("---")

    st.download_button(
        label="Download All Assets Monthly Data as CSV",
        data=all_monthly.to_csv(index=False),
        file_name="all_assets_monthly.csv",
        mime="text/csv"
    )
else:
    st.error("Data could not be loaded. Please check your data file.") 