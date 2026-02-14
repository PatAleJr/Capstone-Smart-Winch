import sys
import os
import pandas as pd
import numpy as np

# Removes jumps missing cord serial numbers
# Converts cord serial numbers to integers. removes rows without serial numbers
# Adds forward fill for Date columns
# Removes useless columns
# Add a new column for how many times the cord was used (based on serial number)
# Removes rows missing weight, anchor offset, water height, or horizontal distance
# Removes rows where harness is not either AF, BF, AB or BB
# Convert D0 and W0 to 0 as an integer for water height and removes all other non-integer entries

cord_colors = ["Yellow", "Blue", "Red", "Purple", "Black"]

for color in cord_colors:
    csv_path = f"JumpData/Raw/{color}Cord.csv"
    output_path = f"JumpData/Cleaned/{color}Cord.csv"
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
    df["Cord Usage Count"] = df.groupby("Cord Serial Number").cumcount() + 1

    # Removing rows with missing critical data *** after adding usage count to avoid losing data
    df = df[df["Weight"].notna() & df["Anchor Offset"].notna() & df["Water Height"].notna() & df["Horizontal Distance"].notna()]
    df = df[df["Harness"].isin(["AF", "BF", "AB", "BB"])]

    # Water heights D0 and W0 are considered 0. Remove any other non-integer entries
    df = df[df["Water Height"].astype(str).str.match(r"^-?\d+$|^D0$|^W0$")]
    df["Water Height"] = df["Water Height"].replace({"D0": 0, "W0": 0}).astype(int)
    df = df[abs(df["Water Height"]) <= 5]

    print(df.head())

    # Save cleaned data
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to: {output_path}")