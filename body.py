# Body proportions
avg_ape_index = 1.0  # average ape index (arm span / height)
avg_shoulder_span = 0.25  # proportion of height (I used myself as reference)
avg_ancle_height = 0.08 # proportion of height (I used myself as reference)
avg_head_height = 1/7.5  # proportion of height
ancle_strap_to_hands_multiplier = 1 - avg_ancle_height - avg_head_height +  (avg_ape_index - avg_shoulder_span) / 2
body_strap_to_feet_multiplier = 0.4 # proportion of height. rough guess

# The distance from the person's harness attachment point to the part of their body that touches the water
# Ancle harness is height of the person + arms reaching - ancle height
# Body harness is between the chest and waist, and the person is in a seated position
def harness_to_lowest_point(harness: list, height: list) -> list:
    lowest_points = []
    for h, hgt in zip(harness, height):
        if h in ("AF", "AB"):
            lowest_points.append(ancle_strap_to_hands_multiplier * hgt + 8 / 12)  # 8 inches for the thing that connects to the harness
        elif h in ("BF", "BB"):
            lowest_points.append(body_strap_to_feet_multiplier * hgt)
        else:
            print("Unknown harness type. Using half the body", h)
            lowest_points.append(0.5 * hgt)
    return lowest_points

def estimate_height_from_weight(weight_lbs: float) -> float:
    avg_BMI = 27.2  # average BMI for adults in Canada (https://en.wikipedia.org/wiki/List_of_countries_by_body_mass_index)
    height_inches = (703 * weight_lbs / avg_BMI) ** 0.5  # Height in inches
    height_feet = height_inches / 12  # Convert to feet
    return height_feet