import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
import numpy as np
import openmeteo_requests
import requests_cache
from retry_requests import retry
from datetime import datetime

# --- 1. IGC PARSER ---
def parse_igc(file_path):
    data = []
    b_pattern = re.compile(r'^B(\d{6})(\d{7})([NS])(\d{8})([EW])A(\d{5})(\d{5})')
    date_pattern = re.compile(r'^HFDTE(\d{2})(\d{2})(\d{2})')
    flight_date = "2024-06-01" 

    with open(file_path, 'r') as f:
        for line in f:
            d_m = date_pattern.match(line)
            if d_m: flight_date = f"20{d_m.group(3)}-{d_m.group(2)}-{d_m.group(1)}"
            match = b_pattern.match(line)
            if match:
                hhmmss, lat_raw, lat_dir, lon_raw, lon_dir, _, alt_gps = match.groups()
                lat = (int(lat_raw[:2]) + int(lat_raw[2:]) / 60000.0) * (-1 if lat_dir == 'S' else 1)
                lon = (int(lon_raw[:3]) + int(lon_raw[3:]) / 60000.0) * (-1 if lon_dir == 'W' else 1)
                dt = datetime.strptime(f"{flight_date} {hhmmss}", "%Y-%m-%d %H%M%S")
                data.append({'dt': dt, 'lat': lat, 'lon': lon, 'alt': int(alt_gps)})
    return pd.DataFrame(data)

# --- 2. WIND LOOKUP ---
def get_wind(lat, lon, dt, alt):
    cache = requests_cache.CachedSession('.cache', expire_after=-1)
    openmeteo = openmeteo_requests.Client(session=retry(cache, retries=5))
    p_levels = {540: "950hPa", 1450: "850hPa", 3000: "700hPa"}
    var = p_levels[min(p_levels.keys(), key=lambda x: abs(x - alt))]
    params = {"latitude": lat, "longitude": lon, "start_date": dt.date().isoformat(), 
              "end_date": dt.date().isoformat(), "hourly": [f"wind_speed_{var}", f"wind_direction_{var}"], "wind_speed_unit": "ms"}
    try:
        res = openmeteo.weather_api("https://historical-forecast-api.open-meteo.com/v1/forecast", params=params)[0].Hourly()
        return res.Variables(0).ValuesAsNumpy()[dt.hour], res.Variables(1).ValuesAsNumpy()[dt.hour]
    except: return None, None

# --- 3. EXECUTION ---
filename = "test.igc"
try:
    df_full = parse_igc(filename)
    df_wind = df_full.iloc[::600, :].copy() # Every 10 mins
    
    fig = px.scatter_mapbox(df_full, lat="lat", lon="lon", color="alt", color_continuous_scale="Turbo", zoom=12)

    for _, row in df_wind.iterrows():
        ws, wd = get_wind(row['lat'], row['lon'], row['dt'], row['alt'])
        if ws is None: continue

        # Manually construct an arrow using 3 points: Head -> Base -> Wings
        # angle is where wind goes (wd + 180)
        angle = np.deg2rad(90 - (wd + 180))
        scale = 0.006 # Length of arrow
        
        # Tip of the arrow
        tip_lat, tip_lon = row['lat'] + np.sin(angle)*scale, row['lon'] + np.cos(angle)*scale
        
        # Arrow "Wings" logic
        wing_angle = 0.5 # radians
        left_lat = row['lat'] + np.sin(angle - wing_angle)*(scale*0.6)
        left_lon = row['lon'] + np.cos(angle - wing_angle)*(scale*0.6)
        right_lat = row['lat'] + np.sin(angle + wing_angle)*(scale*0.6)
        right_lon = row['lon'] + np.cos(angle + wing_angle)*(scale*0.6)

        # Draw the arrow as a single path: LeftWing -> Tip -> RightWing
        fig.add_trace(go.Scattermapbox(
            lat=[left_lat, tip_lat, right_lat],
            lon=[left_lon, tip_lon, right_lon],
            mode="lines",
            line=dict(width=4, color="white"),
            hoverinfo="text",
            text=f"Wind: {ws:.1f}m/s @ {wd}°",
            showlegend=False
        ))

    fig.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()
except Exception as e: print(f"Error: {e}")