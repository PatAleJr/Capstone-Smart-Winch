import pandas as pd
from pathlib import Path

colors = ["Black", "Blue", "Red", "Purple", "Yellow"]

for color in colors:
    # Read the CSV file
    df = pd.read_csv(f'JumpData/Cleaned/{color}Cord.csv')

    # Group by serial number and save each group to a separate file
    for serial_number, group in df.groupby('Cord Serial Number'):
        filename = Path(f"JumpData/PerCordData/{color}") / f'{serial_number}.csv'
        group.to_csv(filename, index=False)
        print(f'Created {filename}')

print('Done!')