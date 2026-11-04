import openmeteo_requests
import requests_cache
import pandas as pd
import numpy as np
import plotly.express as px
from retry_requests import retry

# 1. Setup API client
cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

def get_wind_rose_data(lat, lon, start_date, end_date):
    url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
    
    # Altitudes: 540m, 990m, 1450m, 1950m, 2500m, 3000m, 3500m, 4000m
    params = {
        "latitude": lat, "longitude": lon,
        "start_date": start_date, "end_date": end_date,
        "hourly": [
            "wind_speed_950hPa", "wind_speed_900hPa", "wind_speed_850hPa", "wind_speed_800hPa",
            "wind_speed_750hPa", "wind_speed_700hPa", "wind_speed_650hPa", "wind_speed_600hPa",
            "wind_direction_950hPa", "wind_direction_900hPa", "wind_direction_850hPa", "wind_direction_800hPa",
            "wind_direction_750hPa", "wind_direction_700hPa", "wind_direction_650hPa", "wind_direction_600hPa"
        ],
        "wind_speed_unit": "ms"
    }
    
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    hourly = response.Hourly()

    dates = pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )
    
    p_levels = {0: 540, 1: 990, 2: 1450, 3: 1950, 4: 2500, 5: 3000, 6: 3500, 7: 4000}
    num_vars = len(p_levels)
    
    records = []
    for t_idx, time in enumerate(dates):
        for var_idx, h_asl in p_levels.items():
            speed = hourly.Variables(var_idx).ValuesAsNumpy()[t_idx]
            direction = hourly.Variables(var_idx + num_vars).ValuesAsNumpy()[t_idx]
            
            if not np.isnan(speed):
                records.append({
                    "Time": time.strftime("%Y-%m-%d %H:%M"),
                    "Altitude": f"{h_asl}m ASL",
                    "Speed": speed,
                    "Direction": direction
                })
                
    return pd.DataFrame(records)

# --- EXECUTION ---
LAT, LON = 48.20, 16.37
START, END = "2024-06-01", "2024-06-02"
df = get_wind_rose_data(LAT, LON, START, END)

# --- PLOTLY WIND ROSE ANIMATION ---
fig = px.bar_polar(
    df, 
    r="Speed", 
    theta="Direction", 
    color="Altitude",
    animation_frame="Time",
    template="plotly_dark",
    color_discrete_sequence=px.colors.sequential.Plasma_r,
    labels={"Speed": "Wind Speed (m/s)", "Direction": "Bearing (°)"},
    title=f"Animated Wind Rose Profile (Lat: {LAT}, Lon: {LON})"
)

# Customizing the Polar Chart
fig.update_polars(
    angularaxis=dict(
        rotation=90,      # Puts North at the top
        direction="clockwise",
        tickvals=[0, 45, 90, 135, 180, 225, 270, 315],
        ticktext=['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    ),
    radialaxis=dict(
        ticksuffix=" m/s",
        angle=45          # Angle of the speed labels
    )
)

fig.update_layout(
    polar=dict(bgcolor="rgba(0,0,0,0)"),
    margin=dict(t=80, b=20, l=20, r=20)
)

fig.show()