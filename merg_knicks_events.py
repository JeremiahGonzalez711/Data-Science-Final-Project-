import pandas as pd

# Load MTA ridership data
mta = pd.read_csv("MTA_Subway_Hourly_Ridership__Beginning_2025.csv")

# Prepare date column
mta["transit_timestamp"] = pd.to_datetime(mta["transit_timestamp"])
mta["date"] = mta["transit_timestamp"].dt.date

# Load Knicks event dates
events = pd.read_csv("knicks_events.csv")
events["event_date"] = pd.to_datetime(events["event_date"]).dt.date

# merge event info
mta["event_day"] = mta["date"].isin(events["event_date"]).astype(int)

mta.to_csv("mta_knicks_merged.csv", index=False)

print("✅ mta_knicks_merged.csv created successfully!")
print(mta.head())
