import numpy as np
import CordRecords
import SimulateJump02 as SimulateJump
import Fitting

def simulate_and_plot(cord: CordRecords.Cord, fitting_params, jump: CordRecords.JumpDataPoint):
    print("Simulating and plotting jump " + str(jump) + "for cord " + str(cord.serial_number))
    min_y = SimulateJump.simulate_jump(fitting_params, jump, cord, plotting=True)
    print("Lowest height reached: " + str(min_y))


example_cord = CordRecords.Cord(65524822, "Blue", 56 + 5/12, 530)
#example_cord = CordRecords.Cord(66094822, "Blue", 56, 520, "JumpData/PerCordData")
Fitting.fit_and_validate_cord(example_cord, num_training_jumps=50, num_validation_jumps=50)