import math
import matplotlib.pyplot as plt
import body

# General physical parameters
air_density = 0.00237  # slugs/ft^3 -> function of altitude and temperature
g = 32.1731  # ft/s^2 (https://www.sensorsone.com/local-gravity-calculator/) -> gravity in Ottawa
platform_height = 194 + 3 * 1/12 # ft
person_drag_coefficient = 1.0  # dimensionless
person_cross_sectional_area = 7  # ft^2

unstretched_rope_length = 48  # ft
yellow_cord_weight = 33
blue_cord_weight = 45
red_cord_weight = 50
purple_cord_weight = 60
black_cord_weight = 70

blue_K = 1.3527 # computed from end point
blue_offset = -17.24 # lb. the constant term in equation for F = kx + b

blue_K = 3.417 # Computed from energy. mean. I overwrite this later using weight
blue_offset = 0

# Simulation parameters
t_max = 30

# Jump parameters
person_weight = 148.0  # Lbs
anchor_offset = 25.0  # ft

# Derived parameters
person_mass = person_weight/g # Slugs
person_height = body.estimate_height_from_weight(person_weight)
blue_cord_mass = 45 / g # slugs

blue_K = 0.01991 * person_weight + 0.5778

t_list = []
y_list = []

def simulate():
    t = 0.0
    dt = 0.05
    y = platform_height
    v = 0
    next_print = 0.0
    print_dt = 0.5

    print(f"   t(s)         y(ft)         v(ft/s)         a(ft/s^2)         fcord(lb)         dx(ft)         fdrag")
    while t <= t_max and y > -50:
        delta_x = (platform_height - anchor_offset - y) - unstretched_rope_length
        if (delta_x <= 0): 
            delta_x = 0
            F_cord = 0
        else: F_cord = delta_x * blue_K + blue_offset

        F_drag = 0.5 * air_density * person_drag_coefficient * person_cross_sectional_area * abs(v)*-v

        a = (F_cord + F_drag - person_weight - blue_cord_weight/2) / (person_mass + blue_cord_mass)

        if t >= next_print - 1e-12:
            print(f"{t:6.2f}\t{y:9.2f}\t{v:9.2f}\t{a:9.2f}\t{F_cord:9.2f}\t{delta_x:9.2f}\t{F_drag:9.2f}")
            next_print += print_dt

        #TODO: RK4 integration
        y += dt * v
        v += dt * a
        t += dt

        t_list.append(t)
        y_list.append(y)

simulate()

plt.figure(figsize=(8,6))
plt.scatter(t_list, y_list, alpha=0.8, edgecolor="k", linewidth=0.3)
plt.xlabel("Time (s)")
plt.ylabel("Height (ft)")
plt.title(f"Jump")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()