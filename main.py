import math

# Cord parameters
K_spring = 50.0  # N/m
anchor_offset = 10.0  # m
rope_length = 48 * 0.3048  # ft * m/ft m
rope_mass = 5.0  # kg

# Person parameters
person_mass = 70.0  # kg
person_height = 1.75  # m
person_drag_coefficient = 1.0  # dimensionless
person_cross_sectional_area = 0.7  # m^2

# General parameters
air_density = 1.225  # kg/m^3 -> function of altitude and temperature
gravity = 9.80636  # m/s^2 (https://www.sensorsone.com/local-gravity-calculator/) -> gravity in Ottawa
platform_height = 194 * 0.3048 + 3 * 0.0254 # ft * m/ft + 3 in * m/in

def simulate(m=80.0, Cd=1.0, A=0.7, rho=1.225, g=-9.80665,
             y0=100.0, v0=0.0,
             dt=0.01, t_max=60.0, print_dt=0.05):
    k = 0.5 * rho * Cd * A  # drag coefficient in F = k * v^2
    t = 0.0
    y = y0
    v = v0
    next_print = 0.0

    print("t(s)\ty(m)\tv(m/s)\ta(m/s^2)")
    while t <= t_max and y > 0:
        a = g + (k / m) * v * abs(v)
        if t >= next_print - 1e-12:
            print(f"{t:6.2f}\t{y:7.3f}\t{v:7.3f}\t{a:7.3f}")
            next_print += print_dt

        #TODO: RK4 integration
        y += dt * v
        v += dt * a
        t += dt

simulate()