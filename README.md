# 🌿 EcoPulse Kerala — Regional Climate & Eco-Hydrology Monitor

**Live Interactive App:** [Launch EcoPulse Kerala](https://ecopulse-kerala-cazzam9b3iwavypk4pe3fj.streamlit.app/)

## 📌 Overview
Built for the **NASA Space Apps Challenge**, **EcoPulse Kerala** is an interactive Earth observation analytics dashboard that tracks 20-year hydro-climatic shifts and micro-climate thermal stress across two contrasting ecological zones in Kerala, India:
* **Idukki Highlands (Western Ghats):** Elevation ~1,500m (`10.08°N, 77.05°E`)
* **Alappuzha Coast (Arabian Sea):** Sea Level ~1m (`9.49°N, 76.33°E`)

## 🛰️ NASA Data & Methodology
* **Data Source:** Live satellite telemetry fetched via the **NASA Langley Research Center (LaRC) POWER API v2.0** (`0.5° × 0.625°` spatial resolution).
* **Parameters Analyzed (2005–2025):**
  * `PRECTOTCORR` — Corrected Precipitation (mm/day)
  * `GWETROOT` — Root Zone Soil Moisture (0–1)
  * `T2M` — Mean Air Temperature at 2 Meters (°C)
  * `T2M_MAX` & `RH2M` — Daily Thermal & Humidity Stress Index (`Tmax ≥ 31°C` and `RH ≥ 70%`, 2015–2025)
* **Statistical Engine:** Applies the non-parametric **Mann-Kendall monotonic trend test** alongside the **Theil-Sen robust slope estimator** to separate statistically significant climate trends from natural inter-annual variability.

## 🛠️ Tech Stack
* **Frontend & Hosting:** Streamlit & Streamlit Community Cloud
* **Data & Statistics:** Python, Pandas, NumPy, `pymannkendall`
* **Visualizations:** Plotly Interactive Charts & Carto Darkmatter Geospatial Mapping
