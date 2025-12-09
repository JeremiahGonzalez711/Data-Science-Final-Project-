import pandas as pd
import matplotlib.pyplot as plt

# Loading 
mta = pd.read_csv("MTA_Subway_Hourly_Ridership__Beginning_2025.csv", low_memory=False)
knicks = pd.read_csv("nba-2025-new-york-knicks-UTC.csv", low_memory=False)

# Fixing column names to lowercase for consistency
knicks.columns = knicks.columns.str.lower()
mta.columns = mta.columns.str.lower()

# cleaning Knicks date column
date_col = "date"

knicks["game_datetime"] = pd.to_datetime(
    knicks[date_col],
    format="%d/%m/%Y %H:%M",
    errors="coerce"
)

# October 2025 games only
knicks_oct = knicks[
    (knicks["game_datetime"].dt.month == 10) &
    (knicks["game_datetime"].dt.year == 2025)
].copy()

if knicks_oct.empty:
    raise ValueError(" No Knicks games found for October 2025.")

print("=== Knicks October 2025 Games ===")
print(knicks_oct[["game_datetime", "location", "home team", "away team"]])

# cleaning MTA date column
mta["transit_timestamp"] = pd.to_datetime(mta["transit_timestamp"], errors="coerce")

mta_manhattan = mta[mta["borough"] == "Manhattan"].copy()

all_game_windows = []
all_nextday_windows = []

for _, row in knicks_oct.iterrows():
    start = row["game_datetime"]
    end = start + pd.Timedelta(hours=3)

    # during game ridership
    game_window = mta_manhattan[
        (mta_manhattan["transit_timestamp"] >= start) &
        (mta_manhattan["transit_timestamp"] <= end)
    ].copy()
    game_window["game"] = start
    all_game_windows.append(game_window)

    # next day ridership
    nextday_start = end
    nextday_end = end + pd.Timedelta(hours=24)

    nextday_window = mta_manhattan[
        (mta_manhattan["transit_timestamp"] >= nextday_start) &
        (mta_manhattan["transit_timestamp"] <= nextday_end)
    ].copy()
    nextday_window["game"] = start
    all_nextday_windows.append(nextday_window)

games_df = pd.concat(all_game_windows)
nextday_df = pd.concat(all_nextday_windows)

games_grouped = (
    games_df.groupby("transit_timestamp")["ridership"]
    .sum()
    .reset_index()
)

nextday_grouped = (
    nextday_df.groupby("transit_timestamp")["ridership"]
    .sum()
    .reset_index()
)
# game time plot
plt.figure(figsize=(14, 7))
plt.plot(games_grouped["transit_timestamp"], games_grouped["ridership"])
plt.title("Manhattan Subway Ridership During Knicks Games (October 2025)")
plt.xlabel("Time")
plt.ylabel("Ridership")
plt.tight_layout()
plt.savefig("knicks_october_2025_manhattan_games.png")
plt.close()

# next day plot
plt.figure(figsize=(14, 7))
plt.plot(nextday_grouped["transit_timestamp"], nextday_grouped["ridership"])
plt.title("Manhattan Subway Ridership the Day After Knicks Games (October 2025)")
plt.xlabel("Time")
plt.ylabel("Ridership")
plt.tight_layout()
plt.savefig("knicks_october_2025_manhattan_next_day.png")
plt.close()

print("\n🎉 DONE!")
print("Saved:")
print(" - knicks_october_2025_manhattan_games.png")
print(" - knicks_october_2025_manhattan_next_day.png")
