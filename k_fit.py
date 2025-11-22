import argparse
import sys
import os
import pandas as pd
import numpy as np

# k_fit.py
# Usage: python k_fit.py [path/to/BlueCord.csv]
# Defaults to "BlueCord.csv" in the current working directory.
import matplotlib.pyplot as plt

def main():
    p = argparse.ArgumentParser(description="Plot 'Anchor Offset' vs 'Weight' from a CSV file.")
    p.add_argument("csv", nargs="?", default="BlueCord.csv", help="Path to CSV file (default: BlueCord.csv)")
    p.add_argument("--save", default="anchor_offset_vs_weight.png", help="Output image filename (default: %(default)s)")
    p.add_argument("--fit", action="store_true", help="Overlay linear fit")
    args = p.parse_args()

    if not os.path.exists(args.csv):
        print(f"File not found: {args.csv}", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(args.csv)

    x_col = "Anchor Offset"
    y_col = "Weight"
    if x_col not in df.columns or y_col not in df.columns:
        print("Required columns not found. Available columns:", file=sys.stderr)
        for c in df.columns:
            print(" -", c, file=sys.stderr)
        sys.exit(1)

    x = pd.to_numeric(df[x_col], errors="coerce")
    y = pd.to_numeric(df[y_col], errors="coerce")
    mask = x.notna() & y.notna()
    if mask.sum() == 0:
        print("No valid numeric data in the selected columns.", file=sys.stderr)
        sys.exit(1)

    x = x[mask]
    y = y[mask]

    plt.figure(figsize=(8,6))
    plt.scatter(x, y, color="tab:blue", alpha=0.8, edgecolor="k", linewidth=0.3)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(f"{y_col} vs {x_col}")
    plt.grid(True, linestyle="--", alpha=0.5)

    if args.fit:
        coeffs = np.polyfit(x, y, 1)
        line_x = np.linspace(x.min(), x.max(), 100)
        line_y = np.polyval(coeffs, line_x)
        plt.plot(line_x, line_y, color="red", linewidth=1.5, label=f"fit: y={coeffs[0]:.4g}x+{coeffs[1]:.4g}")
        plt.legend()

    plt.tight_layout()
    plt.savefig(args.save, dpi=150)
    print(f"Saved plot to {args.save}")
    plt.show()

if __name__ == "__main__":
    main()