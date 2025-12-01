import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import body

fit = True

# In pounds
yellow_cord_weight = 33
blue_cord_weight = 45
red_cord_weight = 50
purple_cord_weight = 60
black_cord_weight = 70

csv_path = "BlueCord.csv"
cord_weight = blue_cord_weight
cord_color = "blue"

gravity = 32.1731  # ft/s^2 (https://www.sensorsone.com/local-gravity-calculator/) -> gravity in Ottawa
platform_height = 194 + 3 * 1/12 # ft
unstretched_cord_length = 48  # ft

def main():
    # Load data
    if not os.path.exists(csv_path):
        print(f"File not found: {csv_path}", file=sys.stderr)
        sys.exit(1)
    df = pd.read_csv(csv_path)
    keep_cols = ["Brk", "Weight", "Anchor Offset", "Water Height", "Harness", "Horizontal Distance"]
    df = df[keep_cols].copy()

    acceptable_harnesses = ("AF", "AB", "BF", "BB")
    water_numeric = pd.to_numeric(df["Water Height"], errors="coerce")
    first_filter_mask = (
        (df["Weight"].notna() & (df["Weight"] < 450)) &
        (df["Anchor Offset"].notna() & (df["Anchor Offset"] < 37)) &
        (water_numeric.notna()) &  # only accept numerical water heights (there are some W0 and D0)
        (df["Harness"].notna() & df["Harness"].astype(str).str.strip().isin(acceptable_harnesses)) &
        (df["Horizontal Distance"].notna() & (df["Horizontal Distance"] == 0))
    )

    #break_indicators = ("B", "B/2", "F")
    #filter_no_break_only = df["Brk"].astype(str).str.strip().str.upper().isin(break_indicators)
    #first_filter_mask &= filter_no_break_only
    df_filtered = df.loc[first_filter_mask].copy()

    weights = pd.to_numeric(df_filtered["Weight"], errors="coerce")
    anchor_offsets = pd.to_numeric(df_filtered["Anchor Offset"], errors="coerce") / 12  # convert to feet
    water_heights = pd.to_numeric(df_filtered["Water Height"], errors="raise")
    harnesses = df_filtered["Harness"].astype(str)
    heights = body.estimate_height_from_weight(weights) # in feet
    person_harness_to_bottom = body.harness_to_lowest_point(harnesses, heights)

    # Calculate the stretch length and the force
    delta_x = platform_height - anchor_offsets - unstretched_cord_length - person_harness_to_bottom - water_heights
    total_weight = weights + cord_weight/2
    F = total_weight * gravity

    x = delta_x
    y = F
    plt.figure(figsize=(8,6))
    plt.scatter(x, y, color=cord_color, alpha=0.8, edgecolor="k", linewidth=0.3)
    plt.xlabel("Stretch Length delta_x (ft)")
    plt.ylabel("Force (Lb)")
    plt.title(f"Force vs Stretched Length for {cord_color} Cord (n={len(x)})")
    plt.grid(True, linestyle="--", alpha=0.5)

    if fit:
        x_arr = np.asarray(x).astype(float)
        y_arr = np.asarray(y).astype(float)

        print(f"x_arr is {x_arr}")

        # linear fit
        coeffs = np.polyfit(x_arr, y_arr, 1)
        line_x = np.linspace(x_arr.min(), x_arr.max(), 100)
        line_y = np.polyval(coeffs, line_x)
        plt.plot(line_x, line_y, color="black", linewidth=1.5, label=f"fit: y={coeffs[0]:.4g}x+{coeffs[1]:.4g}")

        # residuals and simple outlier detection
        y_pred = np.polyval(coeffs, x_arr)
        residuals = y_arr - y_pred
        res_std = residuals.std(ddof=1) if residuals.size > 1 else 0.0
        outlier_mask = np.zeros_like(residuals, dtype=bool) if res_std == 0 else (np.abs(residuals) > 3 * res_std)

        # highlight outliers on the plot
        plt.scatter(x_arr[outlier_mask], y_arr[outlier_mask],
                    facecolors="none", edgecolors="orange", s=80, linewidths=1.5, label="outliers")

        # print outlier info (original indices, x, y, residual)
        # Map back to original dataframe indices
        filtered_data_indices = np.arange(len(df_filtered))
        outlier_indices_in_filtered_data = filtered_data_indices[outlier_mask]
        all_data_indices = np.arange(len(df))

        outlier_indices_in_all_data = all_data_indices[first_filter_mask.values][outlier_indices_in_filtered_data]
        if outlier_indices_in_all_data.size:
            print("Outliers (index, weight, anchor offset, water level, dX, F, predicted_F, residual):")
            for idx in outlier_indices_in_all_data:
                idx_in_filtered_data = np.sum(first_filter_mask.values[:idx+1]) - 1
                xi = x_arr[idx_in_filtered_data]; yi = y_arr[idx_in_filtered_data]
                ri = yi - (coeffs[0] * xi + coeffs[1])
                predicted_F = coeffs[0] * xi + coeffs[1]
                print(f"{idx+2}, {df.loc[idx, "Weight"]}, {df.loc[idx, "Anchor Offset"]}, {df.loc[idx, "Water Height"]}, {xi:.4g}, {yi:.4g}, {predicted_F:.4g}, {ri:.4g}")
        else: print("No outliers detected.")

        plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()