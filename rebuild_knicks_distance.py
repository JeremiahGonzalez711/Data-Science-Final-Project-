import pandas as pd
import numpy as np

MSG_LAT = 40.7505
MSG_LON = -73.9934

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    return 2 * R * np.arcsin(np.sqrt(a))

df = pd.read_csv("mta_knicks_distance.csv", low_memory=False)

# Ensure latitude and longitude are numeric
df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

df = df.dropna(subset=["latitude", "longitude"])

# Recalculate distance
df["distance_km"] = haversine(
    df["latitude"], df["longitude"], MSG_LAT, MSG_LON
)

df.to_csv("mta_knicks_distance_fixed.csv", index=False)

print("✅ Rebuilt distances correctly")
print(df["distance_km"].describe())
