import os
from dataclasses import dataclass, asdict
import pandas as pd
import scipy.optimize
import body
import json
from JumpSimulation import SimulateJump03 as SimulateJump
DIRNAME = os.path.dirname(__file__)

# The parameters used to generate a recommendation
@dataclass
class PreRecommendationJumpSettings:
    weight: int
    height: float # in feet
    harness: str
    desired_water_height: float
    planned_horizontal_distance: float

@dataclass
class JumpDataPoint:
    mass: float  # in slugs
    anchor_offset: float  # in ft
    measured_water_height: float  # in ft
    harness_type: str = "AF"  # default harness type
    horizontal_distance: float = 0 # in ft
    break_occurred: int = 0  # 1 if a break occured before this jump
    num_uses: int = 0  # number of times the cord has been used prior to this jump

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

class Cord:
    def __init__(self, serial_number, color, unstretched_length, force_at_300_elongation):
        self.serial_number = serial_number
        self.color = color
        self.weight = {"Yellow": 33, "Blue": 45, "Red": 50, "Purple": 60, "Black": 70}.get(color, 50)  # in lbs
        self.mass = self.weight / 32.174  # in slugs
        self.unstretched_length = unstretched_length  # in ft
        self.force_at_300_elongation = force_at_300_elongation  # in lbs
        self.initialize_jump_data()
        self.number_of_jumps = max(self.jump_data, key = lambda jump: jump.num_uses).num_uses + 1 if self.jump_data else 0
        self.fit_and_validate_results = [] # An array of FittingAndValidatingResult

    def get_initial_fitting_params_guess(self):
        initial_force = 100 # lb. Estimate provided by Matt Lawrence
        k_guess = (self.force_at_300_elongation - initial_force) / (self.unstretched_length * 2) # lb / ft
        return FittingParams([k_guess, 0.1, body.person_drag_K, initial_force, 0, 0])

    def get_cord_weight_for_length(self, length):
        return self.weight * length / self.unstretched_length  # lbs for given length

    # Sets jump_data to an array of JumpDataPoint generated from the CSV file associated with its serial number
    def initialize_jump_data(self):
        self.jump_data = []
        jump_data_csv_path = os.path.join(DIRNAME, "JumpData", "PerCordData", self.color, f"{self.serial_number}.csv")
        df = pd.read_csv(jump_data_csv_path)
        grouped = df.groupby('Cord Serial Number')
        if self.serial_number in grouped.groups:
            cord_data = grouped.get_group(self.serial_number)
            for _, row in cord_data.iterrows():
                mass = row['Weight'] / 32.174  # Convert weight in lbs to mass in slugs
                anchor_offset = row['Anchor Offset']
                measured_water_height = row['Water Height']
                harness_type = row['Harness']
                horizontal_distance = row['Horizontal Distance'] if 'Horizontal Distance' in row else 0
                had_break = 1 if row['Brk'] not in ['B', 'B/2', "F"] else 0
                num_uses = row['Cord Usage Count'] if 'Cord Usage Count' in row else 0
                self.jump_data.append(JumpDataPoint(mass, anchor_offset, measured_water_height, harness_type, horizontal_distance, had_break, num_uses))
        #print("First 3 jump data points for cord " + str(self.serial_number) + ":")
        #print(self.jump_data[:3])  # Print first 5 jump data points

    def add_fit_and_validate_result(self, fit_and_validate_result: FittingAndValidatingResult):
        self.update_from_json()
        self.fit_and_validate_results.append(fit_and_validate_result)
        self.write_json()
        print("Cord " + str(self.serial_number) + " fit and validate results updated. Total fit results stored: " + str(len(self.fit_and_validate_results)))

    def write_json(self):
        cord_records_for_color_path = os.path.join(DIRNAME, "CordRecordsJson", self.color)
        os.makedirs(cord_records_for_color_path, exist_ok=True)
        with open(os.path.join(cord_records_for_color_path, f"{self.serial_number}.json"), 'w') as f:
            f.write(json.dumps({
            "serial_number": self.serial_number,
            "color": self.color,
            "weight": self.weight,
            "mass": self.mass,
            "unstretched_length": self.unstretched_length,
            "force_at_300_elongation": self.force_at_300_elongation,
            "number_of_jumps": self.number_of_jumps,
            "fit_and_validate_results": [fit_result.to_dict() for fit_result in self.fit_and_validate_results]
        }, indent=4))
    
    def update_from_json(self):
        try:
            with open(os.path.join(DIRNAME, "CordRecordsJson", self.color, f"{self.serial_number}.json"), 'r') as f:
                data = json.load(f)
                self.color = data.get("color", self.color)
                self.weight = {"Yellow": 33, "Blue": 45, "Red": 50, "Purple": 60, "Black": 70}.get(self.color, 50)
                self.mass = self.weight / 32.174
                self.unstretched_length = data.get("unstretched_length", self.unstretched_length)
                self.force_at_300_elongation = data.get("force_at_300_elongation", self.force_at_300_elongation)
                self.number_of_jumps = data.get("number_of_jumps", self.number_of_jumps)
                self.fit_and_validate_results = [FittingAndValidatingResult(
                    cord_serial_number=fit_result["cord_serial_number"],
                    fitting_params=FittingParams([fit_result["fitting_params"]["spring_constant"], fit_result["fitting_params"]["damping_constant"], fit_result["fitting_params"]["air_resistance_coefficient"], fit_result["fitting_params"]["constant_force"], fit_result["fitting_params"]["k_had_break"], fit_result["fitting_params"]["k_num_uses"]]),
                    num_jumps_trained_on=fit_result["num_jumps_trained_on"],
                    MAE_from_random_validation=fit_result["MAE_from_random_validation"],
                    MSE_from_random_validation=fit_result["MSE_from_random_validation"],
                    num_jumps_validated_on=fit_result["num_jumps_validated_on"]
                ) for fit_result in data.get("fit_and_validate_results", [])]
        except FileNotFoundError:
            print("File not found for cord " + str(self.serial_number) + ". Will start a new record for this cord.")
        except json.JSONDecodeError:
            print("JSON decode error for cord " + str(self.serial_number) + ". Will start a new record for this cord.")

    def get_best_fitting_and_validating_params(self):
        if not self.fit_and_validate_results:
            return None
        best_result = min(self.fit_and_validate_results, key=lambda result: result.MAE_from_random_validation)
        return best_result

    def get_recommended_anchor_offset(self, pre_recommendation_jump_settings: PreRecommendationJumpSettings):
        # Fitting parameters as an array
        best_fitting_and_validating_params = self.get_best_fitting_and_validating_params()
        if best_fitting_and_validating_params is None:
            print("No fitting and validating results found for cord " + str(self.serial_number) + ". Cannot provide recommendation.")
            return None
        best_fitting_params_arr = best_fitting_and_validating_params.fitting_params.to_array()

        # Create a dummy jump data point
        dummy_jump = JumpDataPoint(
            mass = pre_recommendation_jump_settings.weight / 32.174,
            anchor_offset = 0,
            measured_water_height = 0,
            harness_type = pre_recommendation_jump_settings.harness,
            horizontal_distance = pre_recommendation_jump_settings.planned_horizontal_distance,
            break_occurred = 0,
            num_uses = self.number_of_jumps)
        
        # Use water_height when anchor_offset is 0 as an initial guess
        # This is not the final recommended anchor offset because this is a non-linear system: 10ft water height != 10 ft anchor offset
        water_height_with_zero_anchor_offset = SimulateJump.simulate_jump(best_fitting_params_arr, dummy_jump, self)
        required_anchor_offset_guess = water_height_with_zero_anchor_offset - pre_recommendation_jump_settings.desired_water_height

        # Iterate to find the anchor offset that results in the desired water height within a certain tolerance
        def difference_between_actual_and_desired_water_height(anchor_offset):
            dummy_jump.anchor_offset = anchor_offset[0]
            simulated_water_height = SimulateJump.simulate_jump(best_fitting_params_arr, dummy_jump, self)
            return abs(simulated_water_height - pre_recommendation_jump_settings.desired_water_height)
        result = scipy.optimize.minimize(difference_between_actual_and_desired_water_height, x0=[required_anchor_offset_guess], bounds=[(0, 50)])
        recommended_anchor_offset = result.x[0]

        return recommended_anchor_offset
    
    def simulate_and_plot_jump(self, pre_recommendation_jump_settings: PreRecommendationJumpSettings, anchor_offset, figure):
        best_fitting_and_validating_params = self.get_best_fitting_and_validating_params()
        if best_fitting_and_validating_params is None:
            print("No fitting and validating results found for cord " + str(self.serial_number) + ". Cannot simulate jump.")
            return None
        best_fitting_params = best_fitting_and_validating_params.fitting_params
        dummy_jump = JumpDataPoint(
            mass = pre_recommendation_jump_settings.weight / 32.174,
            anchor_offset = anchor_offset,
            measured_water_height = 0,
            harness_type = pre_recommendation_jump_settings.harness,
            horizontal_distance = pre_recommendation_jump_settings.planned_horizontal_distance,
            break_occurred = 0,
            num_uses = self.number_of_jumps)
        SimulateJump.simulate_jump(best_fitting_params.to_array(), dummy_jump, self, plotting=True, figure=figure)

def get_all_cord_records_from_jsons():
    cord_records = []
    cord_records_path = os.path.join(DIRNAME, "CordRecordsJson")
    for color_dir in os.listdir(cord_records_path):
        color_dir_path = os.path.join(cord_records_path, color_dir)
        if os.path.isdir(color_dir_path):
            for json_file in os.listdir(color_dir_path):
                if json_file.endswith(".json"):
                    serial_number = int(json_file[:-5])  # Remove .json extension
                    try:
                        with open(os.path.join(color_dir_path, json_file), 'r') as f:
                            data = json.load(f)
                            cord = Cord(serial_number, data.get("color", "Unknown"), data.get("unstretched_length", 0), data.get("force_at_300_elongation", 0))
                            cord.update_from_json()  # Update cord with all details from JSON
                            cord_records.append(cord)
                    except (FileNotFoundError, json.JSONDecodeError) as e:
                        print(f"Error loading cord record from {json_file}: {e}")
    return cord_records

# Returns a dictionary mapping cord colors to a cord of that color that has been fit and validated at least once
def get_currently_used_cords():
    all_cords = get_all_cord_records_from_jsons()
    color_to_cord = {"Yellow": None, "Blue": None, "Red": None, "Purple": None, "Black": None}
    for cord in all_cords:
        if cord.fit_and_validate_results.__len__() == 0: continue  # Only consider cords that have been fit and validated at least once
        if cord.color in color_to_cord and color_to_cord[cord.color] is None:
            color_to_cord[cord.color] = cord
    print(color_to_cord)
    return color_to_cord