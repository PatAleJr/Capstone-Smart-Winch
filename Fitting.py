from dataclasses import dataclass
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares
import numpy as np
import CordRecords
import SimulateJump02 as SimulateJump


### Training / Fitting
# K, C, D, O => spring constant, damping constant, air resistance coeff, constant force
def loss_MSE(fitting_params, jump_data, cord):
    res = []
    for jump in jump_data:
        pred = SimulateJump.simulate_jump(fitting_params, jump, cord)
        res.append((pred - jump.measured_water_height) ** 2)
    return np.array(res)

def loss_MAE(fitting_params, jump_data, cord):
    res = []
    for jump in jump_data:
        pred = SimulateJump.simulate_jump(fitting_params, jump, cord)
        res.append(abs(pred - jump.measured_water_height))
    return np.array(res)

def fit_cord(cord: CordRecords.Cord, num_jumps: int):
    print("Fitting cord " + str(cord.serial_number) + " using " + str(num_jumps) + " random jumps with loss function " + loss_function.__name__ )
    training_set_of_jumps = np.random.choice(cord.jump_data, size=num_jumps, replace=False)
    # bounds for k_num_uses enforces: |k_num_uses * max_jumps| < k to not get diverging results
    # similarly, bounds for k_had_break enforces: 0 <= k_had_break * break_occured < k. Breaking this shouldnt cause divergence, but the results wouldnt make sense
    bounds = ([0, 0, 0, 0, 0, -1/cord.number_of_jumps], [np.inf, np.inf, np.inf, np.inf, 1, 0])
    result = least_squares(loss_function, x0=cord.fitting_params_as_array, diff_step=1e-2, args=(training_set_of_jumps, cord), bounds=bounds)
    print("Result of fitting: " + str(result.x))
    return result

### Validation
def validate_cord(cord: CordRecords.Cord, fitting_params, num_jumps: int):
    print("Validating cord " + str(cord.serial_number) + " using " + str(num_jumps) + " random jumps.")
    validation_set_of_jumps = np.random.choice(cord.jump_data, size=num_jumps, replace=False)

    sum_of_squared_errors = loss_MSE(fitting_params, validation_set_of_jumps, cord)
    sum_of_absolute_errors = loss_MAE(fitting_params, validation_set_of_jumps, cord)
    MAE = np.mean(np.abs(sum_of_absolute_errors))
    print("MAE is: " + str(MAE))
    MSE = np.mean(sum_of_squared_errors)
    RMSE = np.sqrt(MSE)
    print("MSE is: " + str(MSE))
    print("RMSE is: " + str(RMSE))

    worst_indices = np.argsort(sum_of_absolute_errors)[-5:][::-1]
    print("Jumps with highest errors:")
    for idx in worst_indices:
        print(f"Jump: {validation_set_of_jumps[idx]}, Error: {sum_of_absolute_errors[idx]}")

def simulate_and_plot(cord: CordRecords.Cord, fitting_params, jump: CordRecords.JumpDataPoint):
    print("Simulating and plotting jump " + str(jump))
    min_y = SimulateJump.simulate_jump(fitting_params, jump, cord, plotting=True)
    print("Lowest height reached: " + str(min_y))

loss_function = loss_MAE
NUM_TRAINING_JUMPS = 100
NUM_VALIDATION_JUMPS = 50
example_cord = CordRecords.Cord(65524822, "Blue", 56 + 5/12, 530, "JumpData/PerCordData")
#example_cord = CordRecords.Cord(66094822, "Blue", 56, 520, "JumpData/PerCordData")
fit_result = fit_cord(example_cord, NUM_TRAINING_JUMPS)
validate_cord(example_cord, fit_result.x, NUM_VALIDATION_JUMPS)
simulate_and_plot(example_cord, fit_result.x, example_cord.jump_data[10])