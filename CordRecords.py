from dataclasses import dataclass
import pandas as pd
import body

# We dont have weights per individual cords, but we have rough weights per color
yellow_cord_weight = 33
blue_cord_weight = 45
blue_num_loops = 11
red_cord_weight = 50
purple_cord_weight = 60
black_cord_weight = 70

# Estimate provided by Matt Lawrence
initial_force = 100 # lb

@dataclass
class FittingParams:
    spring_constant: float = 0  # spring constant (lb/ft)
    damping_constant: float = 0    # damping coefficient (lb/(ft/s))
    air_resistance_coefficient: float = 0  # air resistance coefficient
    constant_force: float = 0     # constant offset force (lb)
    k_had_break: float = 0   # k_had_break is added to the spring constant if a break occurred. is positive
    k_num_uses: float = 0    # number of prior uses * k_num_uses is added from spring constant. is negative

@dataclass
class JumpDataPoint:
    mass: float  # in slugs
    anchor_offset: float  # in ft
    measured_water_height: float  # in ft
    harness_type: str = "AF"  # default harness type
    break_occurred: int = 0  # 1 if a break occured before this jump
    num_uses: int = 0  # number of times the cord has been used prior to this jump

class Cord:
    def __init__(self, serial_number, color, unstretched_length, force_at_300_elongation, jump_data_directory):
        self.serial_number = serial_number
        self.color = color

        if color == "Yellow":
            self.weight = yellow_cord_weight  # in lbs
        elif color == "Blue":
            self.weight = blue_cord_weight  # in lbs
        elif color == "Red":
            self.weight = red_cord_weight  # in lbs
        elif color == "Purple":
            self.weight = purple_cord_weight  # in lbs
        elif color == "Black":
            self.weight = black_cord_weight  # in lbs
        else:
            print()("Warning: Unknown cord color, defaulting weight to 50 lbs")
            self.weight = 50  # in lbs
        self.mass = self.weight / 32.174  # in slugs
        self.unstretched_length = unstretched_length  # in ft
        self.force_at_300_elongation = force_at_300_elongation  # in lbs
        self.wasFitted = False
        self.jump_data_directory = jump_data_directory  # Directory where per-cord jump data CSVs are stored
        self.initialize_jump_data()

        k_guess = (self.force_at_300_elongation - initial_force) / (self.unstretched_length * 2) # lb / ft
        self.fitting_params = FittingParams(k_guess, 0.1, body.person_drag_K, initial_force)
        self.fitting_params_as_array = [self.fitting_params.spring_constant,
                self.fitting_params.damping_constant,
                self.fitting_params.air_resistance_coefficient,
                self.fitting_params.constant_force,
                self.fitting_params.k_had_break,
                self.fitting_params.k_num_uses]

    def get_weight_for_length(self, length):
        return self.weight * length / self.unstretched_length  # lbs for given length

    # Sets jump_data to an array of JumpDataPoint generated from the CSV file associated with its serial number
    def initialize_jump_data(self):
        self.jump_data = []
        df = pd.read_csv(f"{self.jump_data_directory}/{self.serial_number}.csv")
        grouped = df.groupby('Cord Serial Number')
        if self.serial_number in grouped.groups:
            cord_data = grouped.get_group(self.serial_number)
            for _, row in cord_data.iterrows():
                mass = row['Weight'] / 32.174  # Convert weight in lbs to mass in slugs
                anchor_offset = row['Anchor Offset']
                measured_water_height = row['Water Height']
                harness_type = row['Harness']
                had_break = 1 if 'Brk' in row else 0
                num_uses = row['Cord Usage Count'] if 'Cord Usage Count' in row else 0
                self.jump_data.append(JumpDataPoint(mass, anchor_offset, measured_water_height, harness_type, had_break, num_uses))
        #print("First 3 jump data points for cord " + str(self.serial_number) + ":")
        #print(self.jump_data[:3])  # Print first 5 jump data points