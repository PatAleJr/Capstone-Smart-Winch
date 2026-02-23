# Body proportions
avg_ape_index = 1.0  # average ape index (arm span / height)
avg_shoulder_span = 0.25  # proportion of height (I used myself as reference)
avg_ancle_height = 0.08 # proportion of height (I used myself as reference)
avg_head_height = 1/7.5  # proportion of height
ancle_strap_to_hands_multiplier = 1 - avg_ancle_height - avg_head_height +  (avg_ape_index - avg_shoulder_span) / 2
body_strap_to_feet_multiplier = 0.4 # proportion of height. rough guess

# Drag estimate
air_density = 0.00237  # slugs/ft^3 -> function of altitude and temperature
person_drag_coefficient = 1.0  # dimensionless
person_cross_sectional_area = 7  # ft^2
person_drag_K = 0.5 * air_density * person_drag_coefficient * person_cross_sectional_area

# The distance from the person's harness attachment point to the part of their body that touches the water
# Ancle harness is height of the person + arms reaching - ancle height
# Body harness is between the chest and waist, and the person is in a seated position
def harness_to_lowest_point(harness, height):
    if harness in ["AF", "AB"]:
         return ancle_strap_to_hands_multiplier * height + 8 / 12
    elif harness in ["BF", "BB"]:
        return body_strap_to_feet_multiplier * height
    print("Warning: Unknown harness type " + str(harness) + ". Using 0 for HTLP.")
    return 0

def estimate_height_from_weight(weight_lbs: float) -> float:
    avg_BMI = 27.2  # average BMI for adults in Canada (https://en.wikipedia.org/wiki/List_of_countries_by_body_mass_index)
    height_inches = (703 * weight_lbs / avg_BMI) ** 0.5  # Height in inches
    height_feet = height_inches / 12  # Convert to feet
    return height_feet

## The below was used for np arrays

# The distance from the person's harness attachment point to the part of their body that touches the water
# Ancle harness is height of the person + arms reaching - ancle height
# Body harness is between the chest and waist, and the person is in a seated position
# def harness_to_lowest_point(harness, height):
#     h_series = pd.Series(harness).astype(str).str.strip().str.upper()
#     hgt = pd.Series(height).astype(float)

#     result = pd.Series(index=h_series.index, dtype=float)

#     mask_ankle = h_series.isin(["AF", "AB"])
#     mask_body = h_series.isin(["BF", "BB"])

#     result[mask_ankle] = ancle_strap_to_hands_multiplier * hgt[mask_ankle] + 8 / 12
#     result[mask_body] = body_strap_to_feet_multiplier * hgt[mask_body]

#     unknown = ~(mask_ankle | mask_body)
#     if unknown.any():
#         unknown_vals = h_series[unknown].unique().tolist()
#         print(f"Unknown harness type(s) {unknown_vals}. Using half the body for those.")
#         result[unknown] = 0.5 * hgt[unknown]

#     # Preserve original index if input was a Series/DataFrame column
#     return result

# def estimate_height_from_weight(weight_lbs: float) -> float:
#     avg_BMI = 27.2  # average BMI for adults in Canada (https://en.wikipedia.org/wiki/List_of_countries_by_body_mass_index)
#     height_inches = (703 * weight_lbs / avg_BMI) ** 0.5  # Height in inches
#     height_feet = height_inches / 12  # Convert to feet
#     return height_feet