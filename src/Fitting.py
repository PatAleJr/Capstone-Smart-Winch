from scipy.optimize import least_squares
import numpy as np
import CordRecords
import SimulateJump03 as SimulateJump

### Training / Fitting
# K, C, D, O => spring constant, damping constant, air resistance coeff, constant force
def get_errors(fitting_params, jump_data, cord):
    res = []
    #print("fitting_params for this iteration: " + str(fitting_params))
    for jump in jump_data:
        res.append(SimulateJump.simulate_jump(fitting_params, jump, cord) - jump.measured_water_height)
    return np.array(res)

def fit_cord(cord: CordRecords.Cord, jumps):
    # bounds for k_num_uses enforces: |k_num_uses * max_jumps| < k to not get diverging results
    # similarly, bounds for k_had_break enforces: 0 <= k_had_break * break_occured < k. Breaking this shouldnt cause divergence, but the results wouldnt make sense
    bounds = ([0, 0, 0, 0, 0, -1/cord.number_of_jumps], [np.inf, np.inf, np.inf, np.inf, 1, 0])
    x = cord.get_initial_fitting_params_guess().to_array()
    return least_squares(get_errors, x0=x, jac='3-point', method='trf', diff_step=1e-3, args=(jumps, cord), bounds=bounds)

### Validation
def validate_cord(cord: CordRecords.Cord, fitting_params, jumps, num_worst_jumps_to_print: int = 0):
    # print("Validating cord " + str(cord.serial_number) + " using " + str(num_jumps) + " random jumps.")
    sum_of_squared_errors = get_errors(fitting_params, jumps, cord) ** 2
    sum_of_absolute_errors = np.abs(get_errors(fitting_params, jumps, cord))
    MAE = np.mean(sum_of_absolute_errors)
    MSE = np.mean(sum_of_squared_errors)
    if num_worst_jumps_to_print > 0:
        worst_indices = np.argsort(sum_of_absolute_errors)[-num_worst_jumps_to_print:][::-1]
        print("Jumps with highest errors:")
        for idx in worst_indices:
            print(f"Jump: {jumps[idx]}, Error: {sum_of_absolute_errors[idx]}")
    return MAE, MSE

def fit_and_validate_cord(cord: CordRecords.Cord, num_training_jumps: int, num_validation_jumps: int):
    print("Fitting cord " + str(cord.serial_number) + " using " + str(num_training_jumps) + " random jumps, and validating on " + str(num_validation_jumps) + " random jumps.")

    randomly_shuffled_jumps = np.random.permutation(cord.jump_data)
    training_jumps = randomly_shuffled_jumps[:num_training_jumps]
    validation_jumps = randomly_shuffled_jumps[num_training_jumps:num_training_jumps + num_validation_jumps]

    fit_result = fit_cord(cord, training_jumps)
    MAE, MSE = validate_cord(cord, fit_result.x, validation_jumps)
    fit_and_validate_result = CordRecords.FittingAndValidatingResult(
        cord_serial_number=cord.serial_number,
        fitting_params=CordRecords.FittingParams(fit_result.x),
        num_jumps_trained_on=num_training_jumps,
        MAE_from_random_validation=MAE,
        MSE_from_random_validation=MSE,
        num_jumps_validated_on=num_validation_jumps
    )
    print("MAE: " + str(MAE) + ", MSE: " + str(MSE))
    cord.add_fit_and_validate_result(fit_and_validate_result)

def simulate_and_plot(cord: CordRecords.Cord, fitting_params, jump: CordRecords.JumpDataPoint):
    print("Simulating and plotting jump " + str(jump) + "for cord " + str(cord.serial_number))
    min_y = SimulateJump.simulate_jump(fitting_params, jump, cord, plotting=True)
    print("Lowest height reached: " + str(min_y))

