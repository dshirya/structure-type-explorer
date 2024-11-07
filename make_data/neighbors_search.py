import os
import pandas as pd
import numpy as np


def separate_compounds(compounds, target_element):
    elements_with_target = set()
    elements_without_target = set()
    for compound in compounds:
        elements = set(compound.elements.keys())
        if target_element in elements:
            for element in elements:
                if element != target_element:
                    elements_with_target.add(element)
        else:
            elements_without_target.update(elements)
    elements_without_target = elements_without_target - elements_with_target
    # This part makes sure there's no weird duplicates between both sets
    return elements_with_target, elements_without_target


def get_distance(coord1, coord2):
    return np.linalg.norm(np.array(coord1) - np.array(coord2))


def recommender(set_with_target, set_without_target, element_dict, top_n=None):
    distances = []
    target_coords = [element_dict[element] for element in set_with_target]

    for element in set_without_target:
        element_coord = element_dict[element]
        min_distance = min([get_distance(element_coord, target_coord) for target_coord in target_coords])
        distances.append((min_distance, element))

    # Sort distances by the minimum distance
    distances.sort(key=lambda x: x[0])
    ratings = []
    for distance, element in distances:
        rating = (distances[0][0] / distance) * 100  # Calculate the rating based on the shortest distance
        ratings.append((element, rating))

    # Return top_n results if specified, otherwise return all
    if top_n:
        ratings = ratings[:top_n]

    return [f"{element}, {rating:.2f}" for element, rating in ratings]


def recommendation_system(compounds, target_element, element_dict, top_n):
    set_a, set_b = separate_compounds(compounds, target_element)
    results = recommender(set_a, set_b, element_dict, top_n)
    return results


def save_recommendations_to_excel(recommendations, structure, folder="recommendation"):
    os.makedirs(folder, exist_ok=True)
    structure_clean = structure.replace(" ", "_")

    base_filename = f"{structure_clean}_recommendations.xlsx"
    file_path = os.path.join(folder, base_filename)

    # Check if a file with this name exists, and increment if necessary
    counter = 1
    while os.path.exists(file_path):
        file_path = os.path.join(folder, f"{structure_clean}_recommendations_{counter}.xlsx")
        counter += 1

    df = pd.DataFrame([rec.split(", ") for rec in recommendations], columns=["Element", "Value"])
    df.to_excel(file_path, index=False)
    print(f"Recommendations saved as {file_path}")
