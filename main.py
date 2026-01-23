import math
import matplotlib.pyplot as plt
import body
import k_fit_rope_data as rope_data

# General physical parameters
air_density = 0.00237  # slugs/ft^3 -> function of altitude and temperature
g = 32.1731  # ft/s^2 (https://www.sensorsone.com/local-gravity-calculator/) -> gravity in Ottawa
platform_height = 194 + 3 * 1/12 # ft
person_drag_coefficient = 1.0  # dimensionless
person_cross_sectional_area = 7  # ft^2

#unstretched_rope_length = 48  # ft
unstretched_rope_length = 56 + 5/12  # ft -> end length from spreadsheet for cord 6552


yellow_cord_weight = 33
blue_cord_weight = 45
blue_num_loops = 11
red_cord_weight = 50
purple_cord_weight = 60
black_cord_weight = 70

damping_constant = 0.1 * 0.737  # damping constant N/m/s to lb/(ft/s)

# Simulation parameters
t_max = 10
consider_damping = True
consider_air_resistance = True

# Jump parameters
person_weight = 137.0  # Lbs
anchor_offset = 30.0  # ft

# Derived parameters
person_mass = person_weight/g # Slugs
person_height = body.estimate_height_from_weight(person_weight)
blue_cord_mass = 45 / g # slugs

t_list = []
y_list = []

# Things left to fit:
# - damping constant
# - number of loops
# - k constant

def simulate():
    t = 0.0
    dt = 0.05
    y = platform_height
    v = 0
    next_print = 0.0
    print_dt = 1

    lowest_height = platform_height

    print(f"   t(s)         y(ft)         v(ft/s)         a(ft/s^2)         fcord(lb)         dx(ft)         fdrag")
    while t <= t_max and y > -50:
        delta_x = (platform_height - anchor_offset - y) - unstretched_rope_length
        
        #F_cord = rope_data.get_undamped_force(unstretched_rope_length + delta_x, unstretched_rope_length, blue_num_loops)
        # This math is for cord 6552
        percent_elongation = 100 * delta_x / unstretched_rope_length
        F_elastic = 1.433 * percent_elongation + 120

        F_damping = damping_constant * v
        if not consider_damping: F_damping = 0.0

        F_drag = 0.5 * air_density * person_drag_coefficient * person_cross_sectional_area * abs(v)*-v
        if not consider_air_resistance: F_drag = 0.0
        
        a = (F_elastic + F_drag + F_damping - person_weight - blue_cord_weight/2) / (person_mass + blue_cord_mass)

        if t >= next_print - 1e-12:
            print(f"{t:6.2f}\t{y:9.2f}\t{v:9.2f}\t{a:9.2f}\t{F_elastic:9.2f}\t{delta_x:9.2f}\t{F_drag:9.2f}")
            next_print += print_dt

        #TODO: RK4 integration
        y += dt * v
        v += dt * a
        t += dt

        t_list.append(t)
        y_list.append(y)
        if y < lowest_height:
            lowest_height = y
    print(f"Lowest height reached: {lowest_height:.2f} ft")

simulate()

plt.figure(figsize=(8,6))
plt.scatter(t_list, y_list, alpha=0.8, edgecolor="k", linewidth=0.3)
plt.xlabel("Time (s)")
plt.ylabel("Height (ft)")
plt.title(f"Jump")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()