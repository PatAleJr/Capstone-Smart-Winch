import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


fit = True

blue_cord_weight_kg = 45 * 0.45359237  # pounds to kg

csv_path = "BlueCord.csv"
cord_weight_kg = blue_cord_weight_kg
gravity = 9.80636  # m/s^2 (https://www.sensorsone.com/local-gravity-calculator/) -> gravity in Ottawa
platform_height_m = 194 * 0.3048 + 3 * 0.0254 # ft * m/ft + 3 in * m/in
unstretched_cord_length = 48  # ft

def main():
    # Load data
    if not os.path.exists(csv_path):
        print(f"File not found: {csv_path}", file=sys.stderr)
        sys.exit(1)
    df = pd.read_csv(csv_path)
    keep_cols = ["Weight", "Anchor Offset", "Water Height", "Harness", "Horizontal Distance"]
    df = df[keep_cols].copy()

    weights = pd.to_numeric(df["Weight"], errors="coerce")
    anchor_offsets = pd.to_numeric(df["Anchor Offset"], errors="coerce")
    water_heights = pd.to_numeric(df["Water Height"], errors="coerce")
    harnesses = df["Harness"].astype(str)
    horizontal_distances = pd.to_numeric(df["Horizontal Distance"], errors="coerce")

    # Filter data
    first_filter_mask = (
        (weights.notna() & (weights < 450)) &
        (anchor_offsets.notna() & (anchor_offsets < 37)) &
        (water_heights.notna()) &
        (harnesses.notna()) &
        (horizontal_distances.notna() & (horizontal_distances == 0))
    )
    df_filtered = df.loc[first_filter_mask].copy()

    # Print excluded rows due weight and anchor offset filters
    obvious_outlier_indices = []
    for n in range(len(df)):
        if weights[n] > 450 or anchor_offsets[n] > 36: obvious_outlier_indices.append(n+2)  # +2 for header and 0-based index
    print("Excluded rows due to initial filtering (1-based index):", obvious_outlier_indices)

    weights = pd.to_numeric(df_filtered["Weight"], errors="coerce")
    anchor_offsets = pd.to_numeric(df_filtered["Anchor Offset"], errors="coerce")   
    water_heights = pd.to_numeric(df_filtered["Water Height"], errors="coerce")
    harnesses = df_filtered["Harness"].astype(str)
    horizontal_distances = pd.to_numeric(df_filtered["Horizontal Distance"], errors="coerce")

    avg_BMI = 27.2  # average BMI for adults in Canada (https://en.wikipedia.org/wiki/List_of_countries_by_body_mass_index)
    heights = np.sqrt(703 * weights / avg_BMI)  # Takes weight in pounds and returns height in inches

    # The distance from the person's harness attachment point to the part of their body that touches the water
    # Ancle harness is height of the person - ancle height
    # Body harness is between the chest and waist, and the person is in a seated position
    person_harness_to_bottom = np.where(harnesses.isin(["AF", "AB"]), 0.92 * heights,
                               np.where(harnesses.isin(["BF", "BB"]), 0.4 * heights, 0.5 * heights))
    
    # Convert to metric
    water_height_m = water_heights * 0.3048  # positive means above water, negative means below water
    person_harness_to_bottom_m = person_harness_to_bottom * 0.0254
    unstretched_cord_length_m = unstretched_cord_length * 0.3048 # ft to m
    anchor_offsets_m = anchor_offsets * 0.3048
    weights_kg = weights * 0.45359237

    # Calculate the stretch length and the force
    delta_x = platform_height_m - anchor_offsets_m - unstretched_cord_length_m - person_harness_to_bottom_m - water_height_m
    total_weight = weights_kg + cord_weight_kg/2
    F = total_weight * gravity

    x = delta_x
    y = F
    plt.figure(figsize=(8,6))
    plt.scatter(x, y, color="tab:blue", alpha=0.8, edgecolor="k", linewidth=0.3)
    plt.xlabel("Stretch Length delta_x (m)")
    plt.ylabel("Force (N)")
    plt.title(f"Force vs Stretched Length for Blue Cord (n={len(x)})")
    plt.grid(True, linestyle="--", alpha=0.5)

    if fit:
        # prepare numeric arrays
        x_arr = np.asarray(x).astype(float)
        y_arr = np.asarray(y).astype(float)

        # linear fit
        coeffs = np.polyfit(x_arr, y_arr, 1)
        line_x = np.linspace(x_arr.min(), x_arr.max(), 100)
        line_y = np.polyval(coeffs, line_x)
        plt.plot(line_x, line_y, color="red", linewidth=1.5, label=f"fit: y={coeffs[0]:.4g}x+{coeffs[1]:.4g}")

        # residuals and simple outlier detection (threshold = 2 * std)
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
        
        # TODO: use AND to combine masks if more filters are added instead of this complicated indexing

        outlier_indices_in_all_data = all_data_indices[first_filter_mask.values][outlier_indices_in_filtered_data]
        if outlier_indices_in_all_data.size:
            print("Outliers (index, weight, anchor offset, water level, dX, F, predicted_F, residual):")
            for idx in outlier_indices_in_all_data:
                weight = df.loc[idx, "Weight"]
                anchor_offset = df.loc[idx, "Anchor Offset"]
                water_level = df.loc[idx, "Water Height"]
                idx_in_filtered_data = np.sum(first_filter_mask.values[:idx+1]) - 1
                xi = x_arr[idx_in_filtered_data]; yi = y_arr[idx_in_filtered_data]
                ri = yi - (coeffs[0] * xi + coeffs[1])
                predicted_F = coeffs[0] * xi + coeffs[1]
                print(f"{idx+2}, {weight}, {anchor_offset}, {water_level}, {xi:.4g}, {yi:.4g}, {predicted_F:.4g}, {ri:.4g}")
        else: print()("No outliers detected.")

        plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()