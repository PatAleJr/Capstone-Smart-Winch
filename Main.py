import numpy as np
import CordRecords
import SimulateJump03 as SimulateJump
import Fitting

def simulate_and_plot(cord: CordRecords.Cord, jump: CordRecords.JumpDataPoint):
    print("Simulating and plotting jump " + str(jump) + "for cord " + str(cord.serial_number))
    fitting_params_as_array = cord.get_best_fitting_and_validating_params().fitting_params.to_array()
    min_y = SimulateJump.simulate_jump(fitting_params_as_array, jump, cord, plotting=True)
    print("Lowest height reached: " + str(min_y))


example_cord = CordRecords.Cord(65524822, "Blue", 56 + 5/12, 530)
example_cord.update_from_json()
simulate_and_plot(example_cord, example_cord.jump_data[1])