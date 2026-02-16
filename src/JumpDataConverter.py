# This code converts jump data into a csv file containing only what is needed for analysis

# Required data per jump:
# water offset
# jump type
# person weight
# time since last jump
# breaks
# harness type
# number of previous jumps on the cord
# anchor offset

import csv
import os
import sys
import pandas as pd

csv_input_path = "JumpData/BlueCord.csv"
csv_output_path = "JumpDataProcessed.csv"

def main():
    # Load data
    if not os.path.exists(csv_input_path):
        print(f"File not found: {csv_input_path}", file=sys.stderr)
        sys.exit(1)
    df = pd.read_csv(csv_input_path)
    keep_cols = ["Brk", "Weight", "Anchor Offset", "Water Height", "Harness", "Horizontal Distance"]
    df = df[keep_cols].copy()