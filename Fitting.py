from dataclasses import dataclass
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares
import numpy as np
import CordRecords
import SimulateJump01 as SimulateJump


### Training / Fitting
# K, C, D, O => spring constant, damping constant, air resistance coeff, constant force
def residuals(fitting_params, jump_data, cord):
    res = []
    for jump in jump_data:
        pred = SimulateJump.simulate_jump(fitting_params, jump, cord)
        res.append((pred - jump.measured_water_height) ** 2)
    return np.array(res)

def fit_cord(cord: CordRecords.Cord, num_jumps: int):
    print("Fitting cord " + str(cord.serial_number) + " using " + str(num_jumps) + " random jumps.")
    training_set_of_jumps = np.random.choice(cord.jump_data, size=num_jumps, replace=False)
    result = least_squares(residuals, x0=cord.fitting_params_as_array, diff_step=1e-2, args=(training_set_of_jumps, cord))
    print("Result of fitting: " + str(result.x))
    return result

### Validation
def validate_cord(cord: CordRecords.Cord, fitting_params, num_jumps: int):
    print("Validating cord " + str(cord.serial_number) + " using " + str(num_jumps) + " random jumps.")
    validation_set_of_jumps = np.random.choice(cord.jump_data, size=num_jumps, replace=False)
    residuals_list = residuals(fitting_params, validation_set_of_jumps, cord)
    MSE = np.mean(residuals_list)
    print("MSE is: " + str(MSE))

def simulate_and_plot(cord: CordRecords.Cord, fitting_params, jump: CordRecords.JumpDataPoint):
    print("Simulating and plotting jump " + str(jump))
    min_y = SimulateJump.simulate_jump(fitting_params, jump, cord, plotting=True)
    print("Lowest height reached: " + str(min_y))

NUM_TRAINING_JUMPS = 100
NUM_VALIDATION_JUMPS = 50
example_cord = CordRecords.Cord(65524822, "Blue", 56 + 5/12, 530, "JumpData/PerCordData")
fit_result = fit_cord(example_cord, NUM_TRAINING_JUMPS)
validate_cord(example_cord, fit_result.x, NUM_VALIDATION_JUMPS)

simulate_and_plot(example_cord, fit_result.x, example_cord.jump_data[0])