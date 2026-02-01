from dataclasses import dataclass
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares
import numpy as np
import CordRecords
import body

# General parameters
g = 32.1731  # ft/s^2 (https://www.sensorsone.com/local-gravity-calculator/) -> gravity in Ottawa
platform_height = 194 + 3 * 1/12 # ft

# Jump is modelled like mx'' = mg - Fbungee(x, x') - Fair(x')
# We need to fit parameters for Fbungee and Fair
# Fbungee = kx + cv + o = (linear spring) + (damping) + (constant force)
# Fair = d*|v|*v = some constant times velocity squared

def simulate_jump(fitting_params, jump_data, cord, plotting=False):
    if plotting:
        print("Jump data is: " + str(jump_data))
        print("Params are  : " + str(fitting_params))
    
    person_height_estimate = body.estimate_height_from_weight(jump_data.mass * 32.174 / 32.174)  # convert slugs to lbs for weight
    harness_to_lowest_point = body.harness_to_lowest_point(jump_data.harness_type, person_height_estimate)

    k, c, d, o = fitting_params
    dt = 0.1
    t_max = 20.0
    t, v, a = 0, 0, 0
    y, previous_y = platform_height, platform_height
    while t < t_max:
        cord_length = platform_height - jump_data.anchor_offset - y
        if cord_length < cord.unstretched_length: F_bungee = 0
        else: F_bungee = k * (cord_length - cord.unstretched_length) + v * d + o
        F_air = -abs(v) * v * c
        a = (F_bungee + F_air) / jump_data.mass - g
        v += a * dt
        previous_y = y
        y += v * dt
        if not plotting and previous_y < y: return previous_y + harness_to_lowest_point
        t += dt
        if plotting and t % 0.2 < dt: plt.scatter(t, y + harness_to_lowest_point, color='blue')

    if plotting:
        plt.title("Jump Simulation: Height vs Time")
        plt.xlabel("Time (s)")
        plt.ylabel("Height (ft)")
        plt.grid()
        plt.show()
    else:
        print("Warning: Simulation reached t_max without rebound")
    return 999