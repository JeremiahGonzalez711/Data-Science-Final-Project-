import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Coordinates for msg
MSG_LAT, MSG_LON = 40.750504, -73.993439

# Load
df = pd.read_csv("mta_knicks_distance.csv", low_memory=False)

# this function calculates haversine distance
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)
    a = np.sin(dphi/2)**2 + np.cos(phi1)*np.cos(phi2)*np.sin(dlambda/2)**2
    return 2 * R * np.arcsin(np.sqrt(a))

df["distance_km"] = haversine(df["latitude"], df["longitude"], MSG_LAT, MSG_LON)

# Keep relevant columns and drop NaNs
df = df[["distance_km", "ridership", "event_day"]].dropna()

# Bin distances 0–10 km
bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
labels = ["0–1 km", "1–2 km", "2–3 km", "3–4 km", "4–5 km",
          "5–6 km", "6–7 km", "7–8 km", "8–9 km", "9–10 km"]

df["distance_band"] = pd.cut(df["distance_km"], bins=bins, labels=labels, include_lowest=True)

# Group by distance band and event day
summary = df.groupby(["distance_band", "event_day"])["ridership"].mean().reset_index()
event = summary[summary["event_day"] == 1]
baseline = summary[summary["event_day"] == 0]

# Plot two lines next to each other
plt.figure(figsize=(12,6))
plt.plot(event["distance_band"], event["ridership"], marker="o", color="red", label="Knicks Game Days")
plt.plot(baseline["distance_band"], baseline["ridership"], marker="o", color="blue", label="Non-Game Days")

plt.title("Subway Ridership vs Distance from MSG (Knicks Games)")
plt.xlabel("Distance from Madison Square Garden (km)")
plt.ylabel("Average Ridership")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("knicks_ridership_vs_distance_fixed.png")
plt.show()

print("✅ Saved knicks_ridership_vs_distance_fixed.png")
