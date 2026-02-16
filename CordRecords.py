from dataclasses import dataclass, asdict
import pandas as pd
import body
import json

class FittingParams:
    spring_constant: float = 0  # spring constant (lb/ft)
    damping_constant: float = 0    # damping coefficient (lb/(ft/s))
    air_resistance_coefficient: float = 0  # air resistance coefficient
    constant_force: float = 0     # constant offset force (lb)
    k_had_break: float = 0   # k_had_break is added to the spring constant if a break occurred. is a positive fraction of k
    k_num_uses: float = 0    # number of prior uses * k_num_uses is added from spring constant. is a negative fraction of k
    # k_had_break and k_num_uses must be fractions of K to prevent the spring constant from going negative -> diverging result

    def __init__(self, array):
        self.spring_constant = array[0]
        self.damping_constant = array[1]
        self.air_resistance_coefficient = array[2]
        self.constant_force = array[3]
        self.k_had_break = array[4]
        self.k_num_uses = array[5]

    def to_array(self):
        return [self.spring_constant, self.damping_constant, self.air_resistance_coefficient, self.constant_force, self.k_had_break, self.k_num_uses]

    def to_dict(self):
        return {
            "spring_constant": float(self.spring_constant),
            "damping_constant": float(self.damping_constant),
            "air_resistance_coefficient": float(self.air_resistance_coefficient),
            "constant_force": float(self.constant_force),
            "k_had_break": float(self.k_had_break),
            "k_num_uses": float(self.k_num_uses)
        }

@dataclass
class FittingAndValidatingResult:
    cord_serial_number: int
    fitting_params: FittingParams
    num_jumps_trained_on: int
    MAE_from_random_validation: float
    MSE_from_random_validation: float
    num_jumps_validated_on: int

    def to_dict(self):
        d = asdict(self)
        d['fitting_params'] = self.fitting_params.to_dict()
        return d

@dataclass
class JumpDataPoint:
    mass: float  # in slugs
    anchor_offset: float  # in ft
    measured_water_height: float  # in ft
    harness_type: str = "AF"  # default harness type
    break_occurred: int = 0  # 1 if a break occured before this jump
    num_uses: int = 0  # number of times the cord has been used prior to this jump

class Cord:
    jump_data_folder = "JumpData/PerCordData"
    cord_records_json_folder = "CordRecordsJson/"
    def __init__(self, serial_number, color, unstretched_length, force_at_300_elongation):
        self.serial_number = serial_number
        self.color = color
        self.weight = {"Yellow": 33, "Blue": 45, "Red": 50, "Purple": 60, "Black": 70}.get(color, 50)  # in lbs
        self.mass = self.weight / 32.174  # in slugs
        self.unstretched_length = unstretched_length  # in ft
        self.force_at_300_elongation = force_at_300_elongation  # in lbs
        self.initialize_jump_data()
        self.number_of_jumps = max(self.jump_data, key=lambda jump: jump.num_uses).num_uses
        self.fit_and_validate_results = []

    def get_initial_fitting_params_guess(self):
        initial_force = 100 # lb. Estimate provided by Matt Lawrence
        k_guess = (self.force_at_300_elongation - initial_force) / (self.unstretched_length * 2) # lb / ft
        return FittingParams([k_guess, 0.1, body.person_drag_K, initial_force, 0, 0])

    def get_cord_weight_for_length(self, length):
        return self.weight * length / self.unstretched_length  # lbs for given length

    # Sets jump_data to an array of JumpDataPoint generated from the CSV file associated with its serial number
    def initialize_jump_data(self):
        self.jump_data = []
        df = pd.read_csv(f"{self.jump_data_folder}/{self.color}/{self.serial_number}.csv")
        grouped = df.groupby('Cord Serial Number')
        if self.serial_number in grouped.groups:
            cord_data = grouped.get_group(self.serial_number)
            for _, row in cord_data.iterrows():
                mass = row['Weight'] / 32.174  # Convert weight in lbs to mass in slugs
                anchor_offset = row['Anchor Offset']
                measured_water_height = row['Water Height']
                harness_type = row['Harness']
                had_break = 1 if row['Brk'] not in ['B', 'B/2', "F"] else 0
                num_uses = row['Cord Usage Count'] if 'Cord Usage Count' in row else 0
                self.jump_data.append(JumpDataPoint(mass, anchor_offset, measured_water_height, harness_type, had_break, num_uses))
        #print("First 3 jump data points for cord " + str(self.serial_number) + ":")
        #print(self.jump_data[:3])  # Print first 5 jump data points

    def add_fit_and_validate_result(self, fit_and_validate_result: FittingAndValidatingResult):
        self.update_from_json()
        self.fit_and_validate_results.append(fit_and_validate_result)
        self.write_json()
        print("Cord " + str(self.serial_number) + " fit and validate results updated. Total fit results stored: " + str(len(self.fit_and_validate_results)))

    def write_json(self):
        with open(f"{self.cord_records_json_folder}{self.serial_number}.json", 'w') as f:
            f.write(json.dumps({
            "serial_number": self.serial_number,
            "color": self.color,
            "weight": self.weight,
            "mass": self.mass,
            "unstretched_length": self.unstretched_length,
            "force_at_300_elongation": self.force_at_300_elongation,
            "fit_and_validate_results": [fit_result.to_dict() for fit_result in self.fit_and_validate_results]
        }, indent=4))
    
    def update_from_json(self):
        try:
            with open(f"{self.cord_records_json_folder}{self.serial_number}.json", 'r') as f:
                data = json.load(f)
                self.color = data.get("color", self.color)
                self.weight = {"Yellow": 33, "Blue": 45, "Red": 50, "Purple": 60, "Black": 70}.get(self.color, 50)
                self.mass = self.weight / 32.174
                self.unstretched_length = data.get("unstretched_length", self.unstretched_length)
                self.force_at_300_elongation = data.get("force_at_300_elongation", self.force_at_300_elongation)

                self.fit_and_validate_results = [FittingAndValidatingResult(
                    cord_serial_number=fit_result["cord_serial_number"],
                    fitting_params=FittingParams([fit_result["fitting_params"]["spring_constant"], fit_result["fitting_params"]["damping_constant"], fit_result["fitting_params"]["air_resistance_coefficient"], fit_result["fitting_params"]["constant_force"], fit_result["fitting_params"]["k_had_break"], fit_result["fitting_params"]["k_num_uses"]]),
                    num_jumps_trained_on=fit_result["num_jumps_trained_on"],
                    MAE_from_random_validation=fit_result["MAE_from_random_validation"],
                    MSE_from_random_validation=fit_result["MSE_from_random_validation"],
                    num_jumps_validated_on=fit_result["num_jumps_validated_on"]
                ) for fit_result in data.get("fit_and_validate_results", [])]
                print("hi")
        except FileNotFoundError:
            print("File not found for cord " + str(self.serial_number) + ". Will start a new recoerd for this cord.")
        except json.JSONDecodeError:
            print("JSON decode error for cord " + str(self.serial_number) + ". Will start a new recoerd for this cord.")