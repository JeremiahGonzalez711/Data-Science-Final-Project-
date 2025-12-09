import pandas as pd

# loading
knicks = pd.read_csv("nba-2025-new-york-knicks-UTC.csv")

# clean date column
knicks["Date"] = pd.to_datetime(knicks["Date"], errors="coerce")

# only home games
knicks_home = knicks[knicks["Home Team"].str.contains("Knicks", case=False, na=False)]

# Extract event date
knicks_home["event_date"] = knicks_home["Date"].dt.date

knicks_home[["event_date"]].drop_duplicates().to_csv("knicks_events.csv", index=False)

print("✅ Created knicks_events.csv with", len(knicks_home), "home games.")
