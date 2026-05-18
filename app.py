import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Macro Market Tracker", page_icon="📈", layout="wide")
st.title("📈 Advanced Macro-Market Analytics Platform")

# --- 1. DATA LOADING & ENGINEERING ---
@st.cache_data
def load_all_data():
    try:
        df_fed = pd.read_csv('data/fed_funds_rate.csv', index_col='Date', parse_dates=True)
        df_cpi = pd.read_csv('data/cpi.csv', index_col='Date', parse_dates=True)
        df_unrate = pd.read_csv('data/unemployment.csv', index_col='Date', parse_dates=True)
        df_gdp = pd.read_csv('data/gdp.csv', index_col='Date', parse_dates=True).rename(columns={'Value': 'GDP'})
        
        df_cpi['Inflation_Rate'] = df_cpi['Value'].pct_change(periods=12) * 100
        
        market_data = {
            'S&P 500': pd.read_csv('data/sp500.csv', index_col='Date', parse_dates=True),
            'NASDAQ': pd.read_csv('data/nasdaq.csv', index_col='Date', parse_dates=True),
            'Dow Jones': pd.read_csv('data/djia.csv', index_col='Date', parse_dates=True)
        }
        return df_fed, df_cpi, df_unrate, df_gdp, market_data
    except FileNotFoundError:
        st.error("Missing data. Please run the pipeline.")
        return None, None, None, None, None

df_fed, df_cpi, df_unrate, df_gdp, market_data = load_all_data()

# TradingView-Style Config for Plotly
tv_config = {
    'scrollZoom': True,          # Enables mouse wheel zoom
    'displayModeBar': True,      # Keeps the toolbar visible
    'modeBarButtonsToRemove': ['lasso2d', 'select2d'] # Cleans up unnecessary tools
}

# --- 2. FRONT-END UI ---
if market_data:
    tab_market, tab_macro = st.tabs(["📊 Market Deep Dive", "🏦 Macro & Economic Ratios"])
    
    # === TAB 1: MARKET DEEP DIVE ===
    with tab_market:
        col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)
        with col_ctrl1:
            selected_index = st.selectbox("Select Market Index:", list(market_data.keys()))
        with col_ctrl2:
            show_sma = st.checkbox("Show 50-Day & 200-Day Moving Averages")
        with col_ctrl3:
            normalize = st.checkbox("Normalize to % Growth (Compare All)")

        df_selected = market_data[selected_index].copy()
        fig_market = go.Figure()

        if normalize:
            for name, df in market_data.items():
                normalized_series = (df['Close'] / df['Close'].iloc[0] - 1) * 100
                fig_market.add_trace(go.Scatter(x=df.index, y=normalized_series, name=name))
            fig_market.update_yaxes(title_text="Cumulative Growth (%)")
        else:
            fig_market.add_trace(go.Scatter(x=df_selected.index, y=df_selected['Close'], name=f"{selected_index} Close"))
            if show_sma:
                df_selected['SMA_50'] = df_selected['Close'].rolling(window=50).mean()
                df_selected['SMA_200'] = df_selected['Close'].rolling(window=200).mean()
                fig_market.add_trace(go.Scatter(x=df_selected.index, y=df_selected['SMA_50'], name="50-Day SMA", line=dict(color='orange', width=1.5)))
                fig_market.add_trace(go.Scatter(x=df_selected.index, y=df_selected['SMA_200'], name="200-Day SMA", line=dict(color='red', width=1.5)))
            fig_market.update_yaxes(title_text="Index Value")

        fig_market.update_layout(
            template="plotly_dark", 
            height=600,
            dragmode='pan', # Forces click-and-drag to pan the chart like TradingView
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(count=5, label="5y", step="year", stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(visible=False), # Turned off to prioritize mouse-wheel zooming
                type="date"
            )
        )
        # Apply the TradingView config here
        st.plotly_chart(fig_market, use_container_width=True, config=tv_config)

    # === TAB 2: MACRO & RATIOS ===
    with tab_macro:
        st.subheader("The 'Buffett Indicator' Proxy Trend")
        st.markdown("*Note: This calculates (S&P 500 Index Price / US GDP) * 100. Because we are using the Index Price rather than Total Market Capitalization, the absolute percentage is a proxy, but the historical trend lines up perfectly with broader market valuations.*")
        
        df_sp = market_data['S&P 500'].copy()
        df_ratio = df_sp.join(df_gdp, how='outer')
        df_ratio['GDP'] = df_ratio['GDP'].ffill()
        df_ratio = df_ratio.dropna()
        
        # MATH FIX: Multiply by 100 to show as a readable percentage format
        df_ratio['Index_to_GDP'] = (df_ratio['Close'] / df_ratio['GDP']) * 100
        
        fig_ratio = px.line(df_ratio, x=df_ratio.index, y='Index_to_GDP')
        fig_ratio.update_layout(template="plotly_dark", height=400, dragmode='pan')
        fig_ratio.update_yaxes(title_text="Proxy Ratio (%)")
        st.plotly_chart(fig_ratio, use_container_width=True, config=tv_config)
        
        st.markdown("---")
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.subheader("Federal Funds Rate (%)")
            fig_fed = px.line(df_fed, x=df_fed.index, y='Value')
            fig_fed.update_layout(template="plotly_dark", dragmode='pan')
            st.plotly_chart(fig_fed, use_container_width=True, config=tv_config)
        with col_m2:
            st.subheader("Inflation Rate (YoY %)")
            fig_inf = px.line(df_cpi, x=df_cpi.index, y='Inflation_Rate')
            fig_inf.update_layout(template="plotly_dark", dragmode='pan')
            st.plotly_chart(fig_inf, use_container_width=True, config=tv_config)