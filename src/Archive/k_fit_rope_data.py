import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import body

csv_path = "2025RopeData.csv"
numWraps = 2

# Notes from 2024RopeData.csv:
# 21C, cloudy, Lot 180432 box 002

# Notes from 2025 RopeData.csv:
#All measurements taken using 2 loops 10' (total 160 strands - 80 each side) wrapped around delrin spools and stretched horizontally

coeffs = None

def fit_data(plot):
    # Load data
    if not os.path.exists(csv_path):
        print(f"File not found: {csv_path}", file=sys.stderr)
        sys.exit(1)
    df = pd.read_csv(csv_path)
    keep_cols = ["% Elongation", "Sample 1"]
    df = df[keep_cols].copy()

    elongation = pd.to_numeric(df["% Elongation"], errors="coerce")
    sample1 = pd.to_numeric(df["Sample 1"], errors="coerce")

    # Remove rows with NaN values
    mask = elongation.notna() & sample1.notna()
    x = elongation[mask]
    y = sample1[mask]

    x_arr = np.asarray(x).astype(float)
    y_arr = np.asarray(y).astype(float)

    # polynomial fit
    global coeffs
    coeffs = np.polyfit(x_arr, y_arr, 6)
    line_x = np.linspace(x_arr.min(), x_arr.max(), 100)
    line_y = np.polyval(coeffs, line_x)

    if plot:
        plt.figure(figsize=(8,6))
        plt.scatter(x, y, color="blue", s=30, label="data points")
        plt.xlabel("% Elongation")
        plt.ylabel("Force (Lb)")
        plt.title(f"Force / % Elongation")
        plt.grid(True, linestyle="--", alpha=0.5)        
        plt.plot(line_x, line_y, color="black", linewidth=1.5, label=f"fit: y={coeffs[0]:.4g}x+{coeffs[1]:.4g}")
        plt.tight_layout()
        plt.show()

# Get the force from the undamped stress-strain curve
def get_undamped_force(stretched_length, unstretched_length, num_loops):
    global coeffs
    if coeffs is None:
        fit_data(False)
    if stretched_length < unstretched_length:
        return 0.0
    percent_elongation = 100 * (stretched_length - unstretched_length) / unstretched_length
    force = np.polyval(coeffs, percent_elongation)
    force_per_loop = force / 2 # 2 loops in the test setup
    return force_per_loop * num_loops