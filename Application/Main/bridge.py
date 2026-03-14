import sys
import os

import matplotlib.pyplot as plt
import math
import body

# Add parent Application directory to path so Icons_rc can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

import PySide6.QtAsyncio as QtAsyncio
import asyncio

from Main.UI.main_window_ui import Ui_mw_Main

import ArduinoInterface
import CordRecords
import JumpSimulation.SimulateJump03 as SimulateJump
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib

g = 32.1731

current_cords_dict = CordRecords.get_currently_used_cords()
yellow_cord = current_cords_dict.get("Yellow")

original_cord_length = yellow_cord.unstretched_length
simulation_cord_length = 6
simulation_cord_weight = simulation_cord_length / original_cord_length * yellow_cord.weight
simulation_cord_mass = simulation_cord_weight / 32.174  # convert lbs to slugs for mass

simulation_cord = CordRecords.Cord(yellow_cord.serial_number, yellow_cord.batch, yellow_cord.color, simulation_cord_length, 380)

potential_anchor_offset = 10.9
bridge_height = 20
bottle_weight = 44.0925  # 20 kg * 2.20462 = 44.0925 lbs

fitting_params = simulation_cord.get_initial_fitting_params_guess().to_array()
dummy_jump = CordRecords.JumpDataPoint(
    mass=bottle_weight / 32.174,  # convert weight in lbs to mass in slugs
    anchor_offset=potential_anchor_offset,
    measured_water_height=0,
    harness_type="AF",
    horizontal_distance=0,
    break_occurred=0,
    num_uses=simulation_cord.number_of_jumps,
    date = "N/A")

def simulate_jump(fitting_params, jump_data, cord): # Takes fitting params as an array
    person_height_estimate = 1.5 # Remember this is a 20kg bottle
    harness_to_lowest_point = 1

    k_spring, c, d, o, k_had_break, k_num_uses = fitting_params
    k_effective = k_spring * (1 + k_had_break * jump_data.break_occurred + k_num_uses * jump_data.num_uses)
    dt = 0.02
    t_max = 15.0
    t, vx, vy, ay, ax = 0, 0, 0, 0, 0
    y, previous_y, min_y = bridge_height, bridge_height, bridge_height
    x = jump_data.horizontal_distance

    # Modify initial velocities based on horizontal distance, with some reasonable assumptions about how people jump to achieve that horizontal distance
    height_gained_from_jump = 0
    if jump_data.horizontal_distance != 0:
        time_to_return_to_platform_height = 0.4 # Reasonable guess
        vx = jump_data.horizontal_distance / time_to_return_to_platform_height
        height_gained_from_jump = 0.8 * vx # Rough guess of how much higher people jump to achieve that horizontal distance
        vy = -height_gained_from_jump / time_to_return_to_platform_height

    plot_points_x, plot_points_y, plot_times = [], [], []

    while t < t_max:
        distance_to_anchor_point = ((bridge_height - y) ** 2 + x ** 2) ** 0.5
        bungee_length = distance_to_anchor_point - jump_data.anchor_offset

        F_air_y = -abs(vy) * vy * c # neglect horizontal air resistance

        if bungee_length <= cord.unstretched_length: 
            F_bungee_x = 0
            F_bungee_y = 0
        else:
            angle_of_depression = math.atan2(bridge_height - y, x)
            F_bungee = k_effective * (bungee_length - cord.unstretched_length) + o
            F_bungee_x = F_bungee * -math.cos(angle_of_depression) - vx * d
            F_bungee_y = F_bungee * math.sin(angle_of_depression) - vy * d

        ay = (F_bungee_y + F_air_y) / (jump_data.mass + cord.mass /2) - g
        ax = F_bungee_x / (jump_data.mass + cord.mass /2)
        vx += ax * dt
        vy += ay * dt
        previous_y = y
        y += vy * dt
        x += vx * dt
        if y < min_y: min_y = y
        if previous_y < y: return previous_y + harness_to_lowest_point
        t += dt

    return min_y

print(simulate_jump(fitting_params, dummy_jump, simulation_cord))