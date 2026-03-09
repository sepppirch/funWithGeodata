import openmeteo_requests
import requests_cache
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from retry_requests import retry

# 1. Setup API client
cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

def get_high_altitude_wind(lat, lon, start_date, end_date):
    url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
    
    # We now have 8 distinct pressure levels
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
    surface_elevation = response.Elevation()

    hourly = response.Hourly()
    dates = pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )
    
    data = {"date": dates}
    
    # Mapping index to approximate ASL heights
    p_levels = {
        0: 540, 1: 990, 2: 1450, 3: 1950, 
        4: 2500, 5: 3000, 6: 3500, 7: 4000
    }
    
    num_vars = len(p_levels)
    for idx, h_asl in p_levels.items():
        data[f"speed_{h_asl}m"] = hourly.Variables(idx).ValuesAsNumpy()
        data[f"dir_{h_asl}m"] = hourly.Variables(idx + num_vars).ValuesAsNumpy()
        
    return pd.DataFrame(data), surface_elevation

# --- EXECUTION ---
LAT, LON = 47.37, 8.54 # Example: Zurich
START, END = "2024-06-01", "2024-06-02"

df, ground_alt = get_high_altitude_wind(LAT, LON, START, END)

# --- VISUALIZATION ---
fig, ax = plt.subplots(figsize=(15, 10))

# Sorting columns by altitude to ensure correct plotting order
speed_cols = sorted([c for c in df.columns if "speed" in c], key=lambda x: int(x.split('_')[1][:-1]))
last_q = None

for s_col in speed_cols:
    h = int(s_col.split('_')[1][:-1])
    d_col = s_col.replace("speed", "dir")
    
    mask = ~df[s_col].isna()
    if not mask.any(): continue
    
    # Vector math: 0 deg North -> Points Up (90 deg math)
    rads = np.deg2rad(90 - df.loc[mask, d_col])
    u = df.loc[mask, s_col] * np.cos(rads)
    v = df.loc[mask, s_col] * np.sin(rads)
    
    # quiver: X, Y, U, V, Color
    last_q = ax.quiver(df.loc[mask, 'date'], [h] * mask.sum(), u, v, df.loc[mask, s_col], 
                       cmap='viridis', pivot='middle', scale=70, alpha=0.9, width=0.002)

# Legend and Colorbar
if last_q:
    cbar = fig.colorbar(last_q, ax=ax, pad=0.02)
    cbar.set_label('Wind Speed (m/s)', fontsize=12, fontweight='bold')

# Ground Reference
ax.axhline(y=ground_alt, color='black', linewidth=1.5, linestyle='--', label=f'Ground ({ground_alt}m)')
ax.fill_between(df['date'], 0, ground_alt, color='gray', alpha=0.15)

ax.set_ylabel("Altitude Above Sea Level (m)", fontsize=12)
ax.set_xlabel("Time (UTC)", fontsize=12)
ax.set_title(f"High Altitude Wind Profile (540m - 4000m ASL)\nLocation: {LAT}, {LON}", fontsize=14, pad=20)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M\n%d %b'))
ax.set_yticks(np.arange(0, 4501, 500))
ax.grid(True, alpha=0.2)
ax.legend(loc='upper left')

plt.tight_layout()
plt.show()

print(df.tail())