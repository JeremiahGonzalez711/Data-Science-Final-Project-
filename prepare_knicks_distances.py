import pandas as pd
import numpy as np

# Haversine distance between two points
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.cos(dlon/2)**2
    return R * (2 * np.arcsin(np.sqrt(a)))

# load data
df = pd.read_csv("mta_knicks_merged.csv", low_memory=False)

# MSG coordinates
msg_lat = 40.7505
msg_lon = -73.9934

# distance calculation
df["distance_km"] = haversine(df["latitude"], df["longitude"], msg_lat, msg_lon)

df.to_csv("mta_knicks_distance.csv", index=False)
print("✔️ Saved mta_knicks_distance.csv with distance_km column")
