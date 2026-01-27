import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
from datetime import datetime

# --- 1. PAGE CONFIG & THEME VARIABLES ---
st.set_page_config(layout="wide", page_title="Smart Air Quality Dashboard")

# Theme colors
is_dark = True 
bg_color = "#000000"
text_color = "#ffffff"
card_bg = "#1e1e1e"
card_shadow = "rgba(79,112,255,0.4)"
alert_bg = "rgba(230, 57, 70, 0.1)"

# --- 2. GLOBAL STYLES & LOADER ANIMATIONS ---
st.markdown(f"""
<style>
    /* Dashboard Layout Tweaks */
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    
    header[data-testid="stHeader"] {{
        background-color: #000000 !important;
    }}

    [data-testid="stSidebar"] {{ background-color: #111111 !important; border-right: 1px solid #333; }}
    [data-testid="column"] {{ background-color: {card_bg} !important; padding: 25px !important; border-radius: 12px !important; border: 1px solid #333 !important; }}
    h1, h3, .stMarkdown p {{ color: {text_color} !important; }}

    /* EARTH LOADER CSS */
    .earth-wrapper {{
        display: flex; flex-direction: column; align-items: center; justify-content: center; height: 80vh;
    }}
    .earth-loader {{
      --watercolor: #3f51d9; --landcolor: #9be24f;
      width: 10em; height: 10em; position: relative; overflow: hidden; border-radius: 50%;
      border: 2px solid rgba(255,255,255,0.9);
      background: radial-gradient(circle at 30% 30%, #6a78ff, var(--watercolor));
      box-shadow: inset 0.45em 0.45em rgba(255,255,255,0.22), inset -0.6em -0.6em rgba(0,0,0,0.42), 0 0 30px rgba(79,112,255,0.4);
    }}
    .earth-loader svg {{ position: absolute; width: 10.2em; opacity: 0.9; filter: drop-shadow(0 0 4px rgba(155,226,79,0.65)); }}
    .earth-loader svg:nth-child(1) {{ top: -2.6em; animation: round1 4s infinite linear; }}
    .earth-loader svg:nth-child(2) {{ bottom: -2.8em; animation: round2 4s infinite linear 0.9s; }}
    .earth-loader svg:nth-child(3) {{ top: -1.8em; animation: round1 4s infinite linear 1.8s; }}

    @keyframes round1 {{
      0%   {{ left: -3.5em; transform: rotate(0deg); opacity: 1; }}
      45%  {{ left: -8em; transform: rotate(20deg); }}
      46%  {{ opacity: 0; }}
      55%  {{ left: 9em; transform: rotate(-20deg); }}
      65%  {{ opacity: 1; }}
      100% {{ left: -3.5em; transform: rotate(0deg); }}
    }}
    @keyframes round2 {{
      0%   {{ left: 5.5em; transform: rotate(0deg); opacity: 1; }}
      65%  {{ left: -9em; transform: rotate(-20deg); }}
      66%  {{ opacity: 0; }}
      75%  {{ left: 10em; transform: rotate(20deg); }}
      85%  {{ opacity: 1; }}
      100% {{ left: 5.5em; transform: rotate(0deg); }}
    }}

    /* DASHBOARD ANIMATIONS */
    .float-title {{ animation: float 3s ease-in-out infinite; }}
    @keyframes float {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-6px); }} }}
</style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR & ADMIN LOGIC ---
if 'main_data' not in st.session_state:
    st.session_state.main_data = pd.DataFrame()

with st.sidebar:
    st.markdown("### ⚙️ Controls")
    st.selectbox("Monitoring Station", ["Downtown", "East Industrial"])
    
    # ADDED SELECTORS
    st.selectbox("Time Range", ["Last 24 Hours", "Last 7 Days", "Last 30 Days"])
    st.selectbox("Pollutant", ["PM2.5", "PM10", "NO2", "O3", "SO2"])
    st.selectbox("Forecast Horizon", ["12 Hours", "24 Hours", "48 Hours", "72 Hours"])
    
    st.write("")
    st.button("🔄 Update Dashboard")
    
    admin_mode = st.toggle("Admin Mode")
    
    if admin_mode:
        st.markdown("---")
        st.markdown("### 📂 Upload Data for Dashboard")
        uploaded_file = st.file_uploader("Upload Air Quality CSV", type=["csv"])
        if uploaded_file:
            st.session_state.main_data = pd.read_csv(uploaded_file)
            st.success("Data Loaded Successfully!")

# --- 4. SCREEN LOGIC (LOADER -> DASHBOARD) ---
if st.session_state.main_data.empty:
    st.markdown(f"""
    <div class="earth-wrapper">
      <div class="earth-loader">
        <svg viewBox="0 0 200 200"><path fill="#9be24f" d="M100 35 C138 38, 162 68, 158 105 C154 142, 120 160, 100 156 C62 152, 38 125, 42 100 C46 70, 70 40, 100 35Z"/></svg>
        <svg viewBox="0 0 200 200"><path fill="#9be24f" d="M100 45 C132 48, 152 78, 148 108 C144 138, 118 148, 100 145 C68 142, 48 120, 52 100 C56 78, 72 50, 100 45Z"/></svg>
        <svg viewBox="0 0 200 200"><path fill="#9be24f" d="M100 40 C130 44, 150 72, 146 104 C142 136, 118 148, 100 144 C70 140, 50 118, 54 100 C58 74, 74 46, 100 40Z"/></svg>
      </div>
      <h2 style="color:white; margin-top:20px; font-family: 'Segoe UI';">Connecting to Smart Aware System...</h2>
      <p style="color:#aaa;">Please enable Admin Mode and upload a CSV in the sidebar to enter dashboard</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # DASHBOARD SCREEN
    main_data_df = st.session_state.main_data
    st.markdown(f"<h1 class='float-title' style='text-align:center; margin-bottom: 40px;'>🌍 Smart Air Quality Dashboard</h1>", unsafe_allow_html=True)

    current_aqi = main_data_df['AQI'].iloc[-1] if 'AQI' in main_data_df.columns else 164.6
    
    if current_aqi > 150:
        status_text, status_color, alert_msg = "Unhealthy", "#e63946", "🚨 Unhealthy air quality today!"
    elif current_aqi > 100:
        status_text, status_color, alert_msg = "Moderate", "#f1c40f", "⚠️ Moderate air quality detected."
    else:
        status_text, status_color, alert_msg = "Good", "#2ecc71", "✅ Air quality is currently Good."

    # TOP ROW
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Current Air Quality")
        fig_gauge = go.Figure(go.Pie(values=[15, 15, 15, 15, 40], hole=0.75,
            marker_colors=['#a32cc4', '#e63946', '#f1c40f', '#2ecc71', '#333333'],
            textinfo='none', sort=False))
        fig_gauge.add_annotation(text=f"<b>{current_aqi}</b>", x=0.5, y=0.6, font_size=50, showarrow=False, font_color="white")
        fig_gauge.add_annotation(text=f"AQI<br><span style='color:{status_color}'>{status_text}</span>", x=0.5, y=0.35, font_size=16, showarrow=False)
        fig_gauge.update_layout(height=350, margin=dict(t=0,b=0,l=0,r=0), showlegend=False, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col2:
        st.subheader("PM2.5 Forecast")
        fig_forecast = go.Figure()
        fig_forecast.add_trace(go.Scatter(x=["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"], y=[42, 38, 45, 52, 48, 44], name='Historical', line=dict(color='#5c7cfa', width=3)))
        fig_forecast.add_trace(go.Scatter(x=["00:00", "04:00", "08:00", "12:00"], y=[40, 40, 43, 48], name='Forecast', line=dict(color='#ff8787', width=3, dash='dash')))
        fig_forecast.update_layout(height=350, margin=dict(t=20,b=20,l=20,r=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), legend=dict(orientation="h", x=0.3, y=-0.2))
        st.plotly_chart(fig_forecast, use_container_width=True)

    # BOTTOM ROW
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Pollutant Concentrations (μg/m³)")
        times = ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00", "24:00"]
        fig_conc = go.Figure()
        fig_conc.add_trace(go.Scatter(x=times, y=[15, 18, 20, 25, 22, 19, 17], name="PM2.5", line=dict(color='#f9a825', width=2)))
        fig_conc.add_trace(go.Scatter(x=times, y=[30, 32, 35, 40, 38, 32, 30], name="PM10", line=dict(color='#1976d2', width=2)))
        fig_conc.add_trace(go.Scatter(x=times, y=[20, 22, 28, 35, 30, 25, 22], name="O3", line=dict(color='#43a047', width=2)))
        fig_conc.add_shape(type="line", x0=times[0], y0=42, x1=times[-1], y1=42, line=dict(color="Red", width=2, dash="dot"))
        fig_conc.add_annotation(x=times[-1], y=42, text="WHO Limit", showarrow=False, yshift=10, font=dict(color="white"), bgcolor="Red")
        fig_conc.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), legend=dict(orientation="h", x=0.2, y=-0.3))
        st.plotly_chart(fig_conc, use_container_width=True)

    with col4:
        st.subheader("Alert Notifications")
        st.markdown(f"""
            <div style="background-color: {alert_bg}; padding: 15px; border-radius: 8px; margin-bottom: 12px; border-left: 5px solid {status_color};">
                <span style="color: {status_color}; font-weight: bold;">{alert_msg}</span><br>
                <span style="color: #ccc; font-size: 0.85rem;">Current AQI: {current_aqi}. Take necessary precautions.</span>
            </div>
            <div style="background-color: rgba(253, 126, 20, 0.1); padding: 15px; border-radius: 8px; margin-bottom: 12px; border-left: 5px solid #fd7e14;">
                <span style="color: #fd7e14; font-weight: bold;">⚠️ Trend Warning</span><br>
                <span style="color: #ccc; font-size: 0.85rem;">Levels have increased by {round(current_aqi * 0.05, 1)}% in the last 4 hours.</span>
            </div>
        """, unsafe_allow_html=True)
      
