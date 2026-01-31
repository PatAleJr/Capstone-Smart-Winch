import pandas as pd
from pathlib import Path

# Read the CSV file
df = pd.read_csv('JumpData/Cleaned/BlueCord.csv')

# Group by serial number and save each group to a separate file
for serial_number, group in df.groupby('Cord Serial Number'):
    filename = Path("JumpData/PerCordData") / f'{serial_number}.csv'
    group.to_csv(filename, index=False)
    print(f'Created {filename}')

print('Done!')