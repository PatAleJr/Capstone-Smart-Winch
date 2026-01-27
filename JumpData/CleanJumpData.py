import sys
import os
import pandas as pd
import numpy as np

# Removes jumps missing cord serial numbers
# Converts cord serial numbers to integers
# Adds forward fill for Date columns
# Removes useless columns

csv_path = "JumpData/Raw/YellowCord.csv"
output_path = "JumpData/Cleaned/YellowCord.csv"

if not os.path.exists(csv_path):
    print(f"File not found: {csv_path}", file=sys.stderr)
    sys.exit(1)

df = pd.read_csv(csv_path)
keep_cols = ["Date", "Brk", "Weight", "Anchor Offset", "Water Height", 
                "Harness", "Horizontal Distance", "Cord Serial Number"]
df = df[keep_cols].copy()
df = df[df["Cord Serial Number"].notna()]
df["Cord Serial Number"] = df["Cord Serial Number"].str.replace(" ", "").astype(int)
df["Date"] = df["Date"].fillna(method="ffill")
print(df.head())

# Save cleaned data
df.to_csv(output_path, index=False)
print(f"Cleaned data saved to: {output_path}")