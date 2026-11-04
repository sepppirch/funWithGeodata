import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
import numpy as np
import requests_cache
import openmeteo_requests
from retry_requests import retry
from datetime import datetime

# --- 1. UTILS: COLOR MAPPING ---
def get_speed_color(speed_ms):
    if speed_ms < 2: return "#440154" 
    if speed_ms < 5: return "#3b528b" 
    if speed_ms < 8: return "#21918c" 
    if speed_ms < 11: return "#5ec962" 
    if speed_ms < 14: return "#fde725" 
    return "#ff0000"

# --- 2. IGC PARSER ---
def parse_igc(file_path):
    data = []
    b_pattern = re.compile(r'^B(\d{6})(\d{7})([NS])(\d{8})([EW])A(\d{5})(\d{5})')
    date_pattern = re.compile(r'^HFDTE(\d{2})(\d{2})(\d{2})')
    flight_date = datetime.now().strftime("%Y-%m-%d")

    with open(file_path, 'r') as f:
        content = f.readlines()
        for line in content:
            d_m = date_pattern.match(line)
            if d_m:
                dd, mm, yy = d_m.groups()
                flight_date = f"20{yy}-{mm}-{dd}"
        
        for line in content:
            match = b_pattern.match(line)
            if match:
                hhmmss, lat_raw, lat_dir, lon_raw, lon_dir, _, alt_gps = match.groups()
                lat = (int(lat_raw[:2]) + int(lat_raw[2:]) / 60000.0) * (-1 if lat_dir == 'S' else 1)
                lon = (int(lon_raw[:3]) + int(lon_raw[3:]) / 60000.0) * (-1 if lon_dir == 'W' else 1)
                dt = datetime.strptime(f"{flight_date} {hhmmss}", "%Y-%m-%d %H%M%S")
                data.append({'dt': dt, 'lat': lat, 'lon': lon, 'alt': int(alt_gps)})
    return pd.DataFrame(data)

# --- 3. WIND LOOKUP ---
def get_wind(lat, lon, dt, alt):
    cache = requests_cache.CachedSession('.cache', expire_after=-1)
    openmeteo = openmeteo_requests.Client(session=retry(cache, retries=5))
    p_levels = {540: "950hPa", 1450: "850hPa", 3000: "700hPa"}
    var = p_levels[min(p_levels.keys(), key=lambda x: abs(x - alt))]
    params = {"latitude": lat, "longitude": lon, "start_date": dt.date().isoformat(), 
              "end_date": dt.date().isoformat(), "hourly": [f"wind_speed_{var}", f"wind_direction_{var}"], "wind_speed_unit": "ms"}
    try:
        url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
        res = openmeteo.weather_api(url, params=params)[0].Hourly()
        return res.Variables(0).ValuesAsNumpy()[dt.hour], res.Variables(1).ValuesAsNumpy()[dt.hour]
    except: return None, None

# --- 4. EXECUTION ---
FILENAME = "test.igc" 

try:
    df_full = parse_igc(FILENAME)
    df_wind_points = df_full.iloc[::600, :].copy() 
    
    # 1. Base Track (Altitude)
    fig = px.scatter_mapbox(df_full, lat="lat", lon="lon", color="alt", 
                            color_continuous_scale="Turbo", zoom=11)

    layers = []
    label_lats, label_lons, label_texts, label_colors = [], [], [], []
    
    # 2. Add Wind Arrows as Color-Coded Layers and Collect Labels
    for _, row in df_wind_points.iterrows():
        ws, wd = get_wind(row['lat'], row['lon'], row['dt'], row['alt'])
        if ws is not None:
            # Conversion to km/h
            ws_kmh = round(ws * 3.6)
            
            # Geometry for arrows
            angle_rad = np.deg2rad(90 - (wd + 180))
            length = 0.006 + (ws * 0.0004)
            lat_corr = np.cos(np.deg2rad(row['lat']))
            tip_lat = row['lat'] + np.sin(angle_rad) * length
            tip_lon = row['lon'] + (np.cos(angle_rad) * length) / lat_corr
            
            wing_angle, wing_len = 0.6, length * 0.4
            l_lat, l_lon = tip_lat - np.sin(angle_rad - wing_angle) * wing_len, tip_lon - (np.cos(angle_rad - wing_angle) * wing_len) / lat_corr
            r_lat, r_lon = tip_lat - np.sin(angle_rad + wing_angle) * wing_len, tip_lon - (np.cos(angle_rad + wing_angle) * wing_len) / lat_corr

            # Append arrow layer
            color = get_speed_color(ws)
            layers.append({
                "sourcetype": "geojson",
                "source": {"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[l_lon, l_lat], [tip_lon, tip_lat], [r_lon, r_lat]]}},
                "type": "line", "line": {"width": 4}, "color": color
            })

            # Collect label data (placed at the base of the arrow)
            label_lats.append(row['lat'])
            label_lons.append(row['lon'])
            label_texts.append(f"{ws_kmh}")
            label_colors.append(color)

    # 3. Add Labels to Map
    fig.add_trace(go.Scattermapbox(
        lat=label_lats,
        lon=label_lons,
        mode='text+markers',
        marker=dict(size=5, color='black', opacity=0.8),
        text=label_texts,
        textposition="top right",
        textfont=dict(size=25, color="black"),
        name="Wind Speed (km/h)",
        showlegend=False
    ))

    # 4. Custom Legend for Wind Speed
    legend_steps = [0, 5, 10, 15] # m/s for logic
    for step in legend_steps:
        fig.add_trace(go.Scattermapbox(
            lat=[None], lon=[None], mode='lines',
            line=dict(width=4, color=get_speed_color(step)),
            name=f"{round(step*3.6)} km/h",
            showlegend=True
        ))

    # 5. Final Layout
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_layers=layers,
        margin={"r":0,"t":50,"l":0,"b":0},
        legend=dict(title="Wind Speed", yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(0,0,0,0.5)", font=dict(color="white")),
        title="Flight Track: Altitude & Wind Vectors (km/h labels)"
    )
    fig.show()

except Exception as e:
    print(f"Error: {e}")