import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pymannkendall as mk
import requests

# 1. Page Configuration
st.set_page_config(
    page_title="EcoPulse Kerala | Ecological Trend Analytics",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Custom Dark Botanical Lab Theme CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Fira+Code:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
        color: #f1f5f9;
    }
    .stApp {
        background-color: #0d1117;
    }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1280px;
    }

    /* Custom Header Bar */
    .eco-nav {
        background: rgba(22, 27, 34, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 16px 26px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 22px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(10px);
    }
    .eco-brand-title {
        font-weight: 800;
        font-size: 1.35rem;
        color: #34d399;
        letter-spacing: -0.02em;
    }
    .eco-brand-title span {
        color: #fbbf24;
    }
    .eco-brand-sub {
        font-size: 0.76rem;
        color: #10b981;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
    .eco-badge {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 6px 14px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 700;
    }

    /* Analytical Cards */
    .bot-card {
        background: rgba(22, 27, 34, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        height: 100%;
        backdrop-filter: blur(10px);
    }
    .bot-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    .region-heading {
        font-size: 1.1rem;
        font-weight: 700;
        color: #e2e8f0;
    }
    .region-info {
        font-size: 0.8rem;
        color: #94a3b8;
        margin-bottom: 14px;
    }
    .pill-warning {
        background: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.3);
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 700;
    }
    .pill-success {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 700;
    }
    .stat-box-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        background: rgba(13, 17, 23, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 12px;
        margin-top: 10px;
    }
    .stat-lbl {
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        color: #94a3b8;
    }
    .stat-val {
        font-family: 'Fira Code', monospace;
        font-size: 0.95rem;
        font-weight: 600;
        color: #f8fafc;
        margin-top: 2px;
    }

    /* Info Callout */
    .info-box {
        background: rgba(22, 27, 34, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-left: 4px solid #10b981;
        border-radius: 12px;
        padding: 18px 22px;
        font-size: 0.88rem;
        color: #cbd5e1;
    }
    .code-pill {
        font-family: 'Fira Code', monospace;
        background: rgba(255, 255, 255, 0.08);
        padding: 2px 6px;
        border-radius: 5px;
        font-size: 0.8rem;
        color: #34d399;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Header
st.markdown("""
    <div class="eco-nav">
        <div>
            <div class="eco-brand-sub">NASA Space Apps Challenge • Ecological Analytics</div>
            <div class="eco-brand-title">EcoPulse <span>Kerala</span> — Regional Climate & Eco-Hydrology Monitor</div>
        </div>
        <div class="eco-badge">🌱 NASA POWER API v2.0 • Botanical Analytics Engine</div>
    </div>
""", unsafe_allow_html=True)

# 4. Data Fetcher (JSON Endpoint)
@st.cache_data
def fetch_monthly_nasa(lat, lon):
    url = (
        f"https://power.larc.nasa.gov/api/temporal/monthly/point?"
        f"parameters=PRECTOTCORR,GWETROOT,T2M&community=AG&longitude={lon}&latitude={lat}"
        f"&start=2005&end=2025&format=JSON"
    )
    data = requests.get(url).json()["properties"]["parameter"]
    rows = []
    for param, yearly_dict in data.items():
        for ym, val in yearly_dict.items():
            if ym.endswith("13"):
                rows.append({"PARAMETER": param, "YEAR": int(ym[:4]), "ANN": val})
    return pd.DataFrame(rows)

@st.cache_data
def fetch_daily_stress(lat, lon):
    url = (
        f"https://power.larc.nasa.gov/api/temporal/daily/point?"
        f"parameters=T2M_MAX,RH2M&community=AG&longitude={lon}&latitude={lat}"
        f"&start=20150101&end=20251231&format=JSON"
    )
    data = requests.get(url).json()["properties"]["parameter"]
    tmax = data["T2M_MAX"]
    rh = data["RH2M"]
    rows = []
    for date_str, t_val in tmax.items():
        if t_val > -900 and date_str in rh and rh[date_str] > -900:
            yr = int(date_str[:4])
            is_stress = 1 if (t_val >= 31.0 and rh[date_str] >= 70.0) else 0
            rows.append({"YEAR": yr, "STRESS": is_stress})
    df = pd.DataFrame(rows)
    return df.groupby("YEAR")["STRESS"].sum().reset_index()

with st.spinner("Retrieving satellite telemetry from NASA Langley Research Center..."):
    try:
        idukki_m = fetch_monthly_nasa(10.0889, 77.0595)
        alappuzha_m = fetch_monthly_nasa(9.4981, 76.3388)
    except Exception as e:
        st.error(f"NASA POWER Connection Error: {e}")
        st.stop()

# 5. Statistical Engine
def compute_metrics(years, values):
    clean = pd.DataFrame({"y": years, "v": values}).dropna()
    clean = clean[clean["v"] > -900]
    res = mk.original_test(clean["v"])
    x_idx = np.arange(len(clean))
    trend_line = res.intercept + res.slope * x_idx
    return {
        "years": clean["y"].values,
        "values": clean["v"].values,
        "trend_line": trend_line,
        "direction": res.trend.upper(),
        "slope": round(res.slope, 5),
        "p_value": round(res.p, 4),
        "tau": round(res.Tau, 3),
        "is_sig": res.p < 0.05,
        "coverage": f"{len(clean)} yrs (100%)"
    }

# 6. Tabs
tab1, tab2, tab3 = st.tabs([
    "🌿 Regional Eco-Trend Comparison",
    "☀️ Micro-Climate Thermal Stress",
    "📊 Provenance & Data Audit"
])

# ==================== TAB 1 ====================
with tab1:
    c_ctrl1, c_ctrl2, c_ctrl3 = st.columns([2, 2, 1])
    with c_ctrl1:
        var_choice = st.selectbox(
            "Ecological Variable",
            [
                "PRECTOTCORR — Precipitation (mm/day)",
                "GWETROOT — Root Zone Soil Moisture (0–1)",
                "T2M — Mean Temperature (°C)"
            ]
        )
    param_code = var_choice.split(" — ")[0]
    unit_str = var_choice.split("(")[1].replace(")", "")

    with c_ctrl2:
        yr_range = st.slider("Timeframe", 2005, 2025, (2005, 2025))
    with c_ctrl3:
        show_trend = st.toggle("Theil-Sen Fit", value=True)

    def get_sub(df):
        s = df[(df["PARAMETER"] == param_code) & (df["YEAR"] >= yr_range[0]) & (df["YEAR"] <= yr_range[1])]
        return s.sort_values("YEAR")

    sub_h = get_sub(idukki_m)
    sub_c = get_sub(alappuzha_m)

    ev_h = compute_metrics(sub_h["YEAR"], sub_h["ANN"])
    ev_c = compute_metrics(sub_c["YEAR"], sub_c["ANN"])

    colA, colB = st.columns(2, gap="medium")

    with colA:
        badge = f'<span class="pill-success">Significant (p = {ev_h["p_value"]})</span>' if ev_h["is_sig"] else f'<span class="pill-warning">Natural Variation (p = {ev_h["p_value"]})</span>'
        st.markdown(f"""
            <div class="bot-card">
                <div class="bot-header">
                    <div class="region-heading">🌲 Idukki Highlands (Western Ghats)</div>
                    {badge}
                </div>
                <div class="region-info">Elevation ~1,500m • 10.08°N, 77.05°E • Data Coverage: {ev_h['coverage']}</div>
                <div class="stat-box-grid">
                    <div>
                        <div class="stat-lbl">Theil-Sen Slope</div>
                        <div class="stat-val">{ev_h['slope']:+} /yr</div>
                    </div>
                    <div>
                        <div class="stat-lbl">Mann-Kendall p</div>
                        <div class="stat-val">{ev_h['p_value']}</div>
                    </div>
                    <div>
                        <div class="stat-lbl">Trend State</div>
                        <div class="stat-val">{ev_h['direction']}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with colB:
        badge = f'<span class="pill-success">Significant (p = {ev_c["p_value"]})</span>' if ev_c["is_sig"] else f'<span class="pill-warning">Natural Variation (p = {ev_c["p_value"]})</span>'
        st.markdown(f"""
            <div class="bot-card">
                <div class="bot-header">
                    <div class="region-heading">🌊 Alappuzha Coast (Arabian Sea)</div>
                    {badge}
                </div>
                <div class="region-info">Sea Level (~1m) • 9.49°N, 76.33°E • Data Coverage: {ev_c['coverage']}</div>
                <div class="stat-box-grid">
                    <div>
                        <div class="stat-lbl">Theil-Sen Slope</div>
                        <div class="stat-val">{ev_c['slope']:+} /yr</div>
                    </div>
                    <div>
                        <div class="stat-lbl">Mann-Kendall p</div>
                        <div class="stat-val">{ev_c['p_value']}</div>
                    </div>
                    <div>
                        <div class="stat-lbl">Trend State</div>
                        <div class="stat-val">{ev_c['direction']}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    viz_left, viz_right = st.columns([2.3, 1], gap="medium")

    with viz_left:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=ev_h["years"], y=ev_h["values"],
            name="Idukki Observed", mode="lines+markers",
            line=dict(color="#10b981", width=2.5),
            marker=dict(size=6, color="#10b981")
        ))
        fig.add_trace(go.Scatter(
            x=ev_c["years"], y=ev_c["values"],
            name="Alappuzha Observed", mode="lines+markers",
            line=dict(color="#fbbf24", width=2.5),
            marker=dict(size=6, color="#fbbf24")
        ))

        if show_trend:
            fig.add_trace(go.Scatter(
                x=ev_h["years"], y=ev_h["trend_line"],
                name="Idukki Trendline", mode="lines",
                line=dict(color="#10b981", width=2, dash="dash")
            ))
            fig.add_trace(go.Scatter(
                x=ev_c["years"], y=ev_c["trend_line"],
                name="Alappuzha Trendline", mode="lines",
                line=dict(color="#fbbf24", width=2, dash="dash")
            ))

        fig.update_layout(
            title=dict(text=f"Time Series Analysis ({yr_range[0]}–{yr_range[1]})", font=dict(size=15, color="#f8fafc")),
            template="plotly_dark",
            plot_bgcolor="rgba(22, 27, 34, 0.6)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=390,
            hovermode="x unified",
            margin=dict(l=20, r=20, t=55, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
            xaxis=dict(title="Year", gridcolor="rgba(255,255,255,0.06)", dtick=2),
            yaxis=dict(title=unit_str, gridcolor="rgba(255,255,255,0.06)")
        )
        st.plotly_chart(fig, use_container_width=True)

    with viz_right:
        fig_map = go.Figure(go.Scattermap(
            lat=[10.0889, 9.4981],
            lon=[77.0595, 76.3388],
            mode="markers+text",
            marker=go.scattermap.Marker(size=14, color=["#10b981", "#fbbf24"]),
            text=["Idukki (Highlands)", "Alappuzha (Coast)"],
            textposition="top center",
            textfont=dict(color="#f8fafc", size=12)
        ))
        fig_map.update_layout(
            map_style="carto-darkmatter",
            map=dict(center=dict(lat=9.8, lon=76.7), zoom=7.1),
            margin=dict(l=0, r=0, t=0, b=0),
            height=390,
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_map, use_container_width=True)

# ==================== TAB 2 ====================
with tab2:
    st.markdown("""
        <div class="info-box">
            <strong>Micro-Climate Indicator (Thermal & Humidity Stress):</strong><br>
            Tracking annual days where <span class="code-pill">T2M_MAX ≥ 31.0°C</span> AND <span class="code-pill">RH2M ≥ 70.0%</span> to evaluate coastal versus highland ecological resilience.
        </div><br>
    """, unsafe_allow_html=True)

    with st.spinner("Computing daily thermal stress indicators (2015–2025)..."):
        stress_h = fetch_daily_stress(10.0889, 77.0595)
        stress_c = fetch_daily_stress(9.4981, 76.3388)

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=stress_c["YEAR"], y=stress_c["STRESS"],
        name="Alappuzha Coast", marker_color="#fbbf24"
    ))
    fig_bar.add_trace(go.Bar(
        x=stress_h["YEAR"], y=stress_h["STRESS"],
        name="Idukki Highlands", marker_color="#10b981"
    ))
    fig_bar.update_layout(
        barmode="group",
        template="plotly_dark",
        plot_bgcolor="rgba(22, 27, 34, 0.6)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=380,
        title="Annual High Stress Days (Tmax ≥ 31°C & RH ≥ 70%)",
        xaxis=dict(title="Year", dtick=1),
        yaxis=dict(title="Cumulative Days", gridcolor="rgba(255,255,255,0.06)")
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ==================== TAB 3 ====================
with tab3:
    st.markdown("""
        <div class="info-box">
            <h4>🧾 Data Provenance & Reproducibility</h4>
            <ul>
                <li><strong>Data Source:</strong> NASA Langley Research Center (LaRC) POWER Project API v2.0</li>
                <li><strong>Spatial Resolution:</strong> <span class="code-pill">0.5° × 0.625°</span> grid cells</li>
                <li><strong>Statistical Model:</strong> Mann-Kendall monotonic trend test with Theil-Sen robust slope estimator</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>**JSON Audit Output**")
    st.json({
        "project": "EcoPulse Kerala",
        "window": f"{yr_range[0]}-{yr_range[1]}",
        "parameter": param_code,
        "highlands": {
            "slope": ev_h["slope"],
            "p_value": ev_h["p_value"],
            "verdict": ev_h["direction"]
        },
        "coast": {
            "slope": ev_c["slope"],
            "p_value": ev_c["p_value"],
            "verdict": ev_c["direction"]
        }
    })