import pandas as pd
import matplotlib.pyplot as plt
import re
#Read completed trade data
df = pd.read_csv("backtesting/trades.csv")
df["tokenName"] = df["tokenName"].str.strip().str.upper()
df["side"] = df["tokenName"].replace({
    "YES": "UP",
    "NO": "DOWN"
})

#Group markets that have been split into multiple trades
grouped = (
    df.groupby(["marketName", "side"])["tokenAmount"]
    .sum()
    .unstack(fill_value=0)
    .reset_index()
)

#Set UP/DOWN to 0 if no trade completed
if "UP" not in grouped.columns:
    grouped["UP"] = 0
if "DOWN" not in grouped.columns:
    grouped["DOWN"] = 0
grouped["UP"] = grouped["UP"].astype(float)
grouped["DOWN"] = grouped["DOWN"].astype(float)

# Classify succesful hedges against unsuccesful hedges
TOL = 2e-2
diff = (grouped["UP"] - grouped["DOWN"]).abs()

grouped["UP_complete"] = diff < TOL
grouped["DOWN_complete"] = diff < TOL
grouped["hedge_status"] = grouped.apply(
    lambda row: "SUCCESS" if (row["UP_complete"] and row["DOWN_complete"]) else "FAIL",
    axis=1
)

#Calculate outputs
successful = grouped[grouped["hedge_status"] == "SUCCESS"]
failed = grouped[grouped["hedge_status"] == "FAIL"]

#Output data
print("\n=== FAILED HEDGES ===")
print(failed[["marketName", "UP", "DOWN"]])

print("\n=== SUMMARY ===")
print(f"Total markets: {len(grouped)}")
print(f"Successful hedges: {len(successful)}")
print(f"Failed hedges: {len(failed)}")

# Save data to csv
grouped.to_csv("hedge_analysis_full.csv", index=False)

# --- Extract time from marketName (e.g. 08:40) ---
def extract_datetime(market):
    match = re.search(
        r'([A-Za-z]+ \d+), (\d{1,2}:\d{2})(AM|PM)',
        market
    )
    if match:
        date_part = match.group(1)
        time_part = match.group(2) + match.group(3)
        return pd.to_datetime(
            f"{date_part} 2026 {time_part}",
            format="%B %d %Y %I:%M%p"
        )
    return None

grouped["datetime"] = grouped["marketName"].apply(extract_datetime)
grouped = grouped.dropna(subset=["datetime"])
time_stats = grouped.sort_values("datetime").set_index("datetime")

time_stats["fail"] = (time_stats["hedge_status"] == "FAIL").astype(int)
rolling_fail_rate = time_stats["fail"].rolling(20).mean()
plt.figure()

rolling_fail_rate.plot()

plt.title("Smoothed Hedge Failure Rate Over Time")
plt.xlabel("Time")
plt.ylabel("Failure Rate (rolling)")

plt.tight_layout()
plt.show()