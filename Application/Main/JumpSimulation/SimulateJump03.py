import matplotlib.pyplot as plt
import math
import body

# General parameters
g = 32.1731  # ft/s^2 (https://www.sensorsone.com/local-gravity-calculator/) -> gravity in Ottawa
platform_height = 194 + 3 * 1/12 # ft

# Returns predicted water height of a jump, with the option of plotting the trajectory
# Jump is modelled like mx'' = mg - Fbungee(x, x') - Fair(x')
# We need to fit parameters for Fbungee and Fair
# Fbungee = kx + cv + o = (linear spring) + (damping) + (constant force)
# Fair = d*|v|*v = some constant times velocity squared

# Assume k is a function of how many times the cord was used, and whether or not there was a break
# k = spring_constant + k_had_break*spring_constant*had_break + k_num_uses*spring_constant*num_uses

# This model considers horizontal distance

def simulate_jump(fitting_params, jump_data, cord, plotting=False, figure=None): # Takes fitting params as an array
    person_height_estimate = body.estimate_height_from_weight(jump_data.mass * 32.174 / 32.174)  # convert slugs to lbs for weight
    harness_to_lowest_point = body.harness_to_lowest_point(jump_data.harness_type, person_height_estimate)

    k_spring, c, d, o, k_had_break, k_num_uses = fitting_params
    k_effective = k_spring * (1 + k_had_break * jump_data.break_occurred + k_num_uses * jump_data.num_uses)
    dt = 0.02
    t_max = 15.0
    t, vx, vy, ay, ax = 0, 0, 0, 0, 0
    y, previous_y, min_y = platform_height, platform_height, platform_height
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
        distance_to_anchor_point = ((platform_height - y) ** 2 + x ** 2) ** 0.5
        bungee_length = distance_to_anchor_point - jump_data.anchor_offset

        F_air_y = -abs(vy) * vy * c # neglect horizontal air resistance

        if bungee_length <= cord.unstretched_length: 
            F_bungee_x = 0
            F_bungee_y = 0
        else:
            angle_of_depression = math.atan2(platform_height - y, x)
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
        if not plotting and previous_y < y: return previous_y + harness_to_lowest_point
        t += dt
        if plotting and t % 0.2 < dt:
            plot_points_x.append(x)
            plot_points_y.append(y + harness_to_lowest_point)
            plot_times.append(t)

    if plotting:
        # Accept either a Figure or an Axes as 'figure' argument and draw directly into its axes.
        created_fig = False
        if figure is None:
            fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
            created_fig = True
        elif hasattr(figure, "add_subplot") and isinstance(figure, plt.Figure):
            fig = figure
            ax = fig.gca()
        else:
            # fallback
            fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
            created_fig = True

        scatter = ax.scatter(plot_points_x, plot_points_y, c=plot_times, cmap='coolwarm', s=20)
        fig.colorbar(scatter, ax=ax, label='Time (s)')
        ax.set_title("Jump Simulation: Height vs Distance per time")
        ax.set_xlabel("Distance (ft)")
        ax.set_xlim(min(-5, ax.get_xlim()[0]), max(5, ax.get_xlim()[1])) # Don't zoom in ridiculously if the jump is short
        ax.set_ylabel("Height (ft)")
        ax.grid(True)

        # Only show if we created the figure locally; otherwise caller is responsible for embedding/updating the canvas.
        if created_fig:
            plt.show()
        else:
            try:
                fig.canvas.draw_idle()
            except Exception:
                pass
    #else:
        #print("Warning: Simulation reached t_max without rebound. fitting parameters tried were: " + str(fitting_params))
        #print("Jump was : " + str(jump_data))
    return min_y