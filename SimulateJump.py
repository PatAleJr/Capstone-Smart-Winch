from dataclasses import dataclass
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares
import numpy as np
import CordRecords

# General parameters
g = 32.1731  # ft/s^2 (https://www.sensorsone.com/local-gravity-calculator/) -> gravity in Ottawa
platform_height = 194 + 3 * 1/12 # ft

# Jump is modelled like mx'' = mg - Fbungee(x, x') - Fair(x')
# We need to fit parameters for Fbungee and Fair
# Fbungee = kx + cv + o = (linear spring) + (damping) + (constant force)
# Fair = d*|v|*v = some constant times velocity squared

def simulate_jump(fitting_params, jump_data, cord):
    k, c, d, o = fitting_params
    starting_stretch_height = platform_height - jump_data.anchor_offset - cord.unstretched_length
    def ode(t, y):
        x, v = y
        F_bungee = k*x + c*v + o if x < starting_stretch_height else 0
        F_air = d*abs(v)*v
        a = (F_bungee + F_air)/jump_data.mass - g
        return [v, a]

    y0 = [platform_height, 0.0]
    sol = solve_ivp(ode, [0, 20], y0, max_step=0.1)

    x = sol.y[0]
    print("Min for attempt with params " + str(fitting_params) + " is " + str(np.min(x)))
    return np.min(x)

def residuals(fitting_params, jump_data, cord):
    res = []
    for data_point in jump_data:
        pred = simulate_jump(fitting_params, data_point, cord)
        res.append(pred - data_point.measured_water_height)
    return np.array(res)

# Manually taken from BCI Cord Manufacturing Log
example_cord = CordRecords.Cord(65524822, "Blue", 56 + 5/12, 530, "JumpData/PerCordData")
print(example_cord)
print(example_cord.jump_data)
result = least_squares(residuals, x0=[100, 10, 1, 0], diff_step=1e-2, args=(example_cord.jump_data, example_cord))
print("Final result is:")
print(result)