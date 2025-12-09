import pandas as pd
from math import radians, cos, sin, sqrt, atan2

# this function calculates haversine distance in miles
def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    return 2 * R * atan2(sqrt(a), sqrt(1 - a))

# load
df = pd.read_csv("mta_knicks_merged.csv", low_memory=False)

# msg location
MSG_LAT = 40.7505045
MSG_LON = -73.9934387

# compute distance to MSG
df["distance_to_msg"] = df.apply(
    lambda row: haversine(
        row["latitude"],
        row["longitude"],
        MSG_LAT,
        MSG_LON
    ),
    axis=1
)

bins = [0, 0.25, 0.5, 1, 2, 5]
labels = ["0–0.25 mi", "0.25–0.5 mi", "0.5–1 mi", "1–2 mi", "2–5 mi"]

df["distance_band"] = pd.cut(df["distance_to_msg"], bins=bins, labels=labels)

# average ridership by borough, distance band, and event day
grouped = (
    df.groupby(["borough", "distance_band", "event_day"])["ridership"]
    .mean()
    .reset_index()
)

event = grouped[grouped["event_day"] == 1]
non_event = grouped[grouped["event_day"] == 0]

comparison = event.merge(
    non_event,
    on=["borough", "distance_band"],
    suffixes=("_event", "_non_event")
)

# percent increase calculation
comparison["percent_increase"] = (
    (comparison["ridership_event"] - comparison["ridership_non_event"])
    / comparison["ridership_non_event"]
) * 100

final = comparison[
    ["borough", "distance_band", "ridership_event",
     "ridership_non_event", "percent_increase"]
].sort_values("percent_increase", ascending=False)

final.to_csv("knicks_percent_increase_by_distance.csv", index=False)

print("✅ knicks_percent_increase_by_distance.csv created successfully!")
print(final.head(10))
