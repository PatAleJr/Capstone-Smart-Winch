import CordRecords
import Fitting

### Automatic fitting for all available cords
import os
from pathlib import Path
import pandas as pd

def parse_feet_inches(value):
    """Parse a length string like '56\\'5\"' to feet (56 + 5/12)"""
    if isinstance(value, float) or isinstance(value, int):
        return float(value)
    if pd.isna(value):
        return 0.0
    value = str(value).strip()
    # Handle quotes
    value = value.replace('"', '').replace("'", "'")
    if "'" in value:
        parts = value.split("'")
        try:
            feet = float(parts[0])
            if len(parts) > 1 and parts[1]:
                inches = float(parts[1])
                return feet + inches / 12
            return feet
        except ValueError:
            return 0.0
    try:
        return float(value)
    except ValueError:
        return 0.0

# Read BCI Cord Manufacturing Log and create lookup dictionary
print("Reading BCI Cord Manufacturing Log...")
    
bci_df = pd.read_csv(os.path.join(os.path.dirname(__file__), "BCI Cord Manufacturing Log.csv"), skiprows=1)  # Skip first header row
bci_dict = {}
for _, row in bci_df.iterrows():
    try:
        serial_num = str(int(row.iloc[1]))  # SERIAL # column (index 1, 0-indexed)
        wraps = str(int(row.iloc[2]))       # WRAPS column (index 2, 0-indexed)
        force = float(row.iloc[10])         # END LOAD column (index 10, 0-indexed)
        length_str = row.iloc[13]           # FINAL LENGTH column (index 13, 0-indexed)
        length = parse_feet_inches(length_str)
        combined_serial = serial_num + wraps
        bci_dict[combined_serial] = (length, force)
    except (ValueError, IndexError):
        continue

print(f"Loaded {len(bci_dict)} cord specifications from BCI database")

# Iterate through all cord data directories
jump_data_path = Path(os.path.join(os.path.dirname(__file__), "JumpData", "PerCordData"))
cords_processed = 0
cords_skipped = 0

for color_dir in sorted(jump_data_path.iterdir()):
    if color_dir.is_dir():
        color = color_dir.name
        for csv_file in sorted(color_dir.glob("*.csv")):
            serial_str = csv_file.stem  # Filename without extension
            if serial_str in bci_dict:
                try:
                    unstretched_length, force_at_300 = bci_dict[serial_str]
                    cord = CordRecords.Cord(int(serial_str), color, unstretched_length, force_at_300)
                    num_training = int(cord.number_of_jumps * 0.8)
                    num_validation = int(cord.number_of_jumps * 0.2)
                    if num_training > 0 and num_validation > 0:
                        print(f"\nProcessing cord {serial_str} ({color}): {cord.number_of_jumps} jumps total")
                        Fitting.fit_and_validate_cord(cord, num_training, num_validation)
                        cords_processed += 1
                    else:
                        print(f"Skipping cord {serial_str} ({color}): insufficient data ({cord.number_of_jumps} jumps)")
                        cords_skipped += 1
                except Exception as e:
                    print(f"Error processing cord {serial_str} ({color}): {e}")
                    cords_skipped += 1
            else:
                print(f"Warning: Cord {serial_str} ({color}) not found in BCI database")
                cords_skipped += 1

print(f"\n\nSummary: Successfully processed {cords_processed} cords, skipped {cords_skipped}")