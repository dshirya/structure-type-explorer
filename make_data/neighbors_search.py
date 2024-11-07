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


def recommender(set_with_target, set_without_target, element_dict, top_n):
    distances = []
    target_coords = [element_dict[element] for element in set_with_target]

    for element in set_without_target:
        element_coord = element_dict[element]
        min_distance = min([get_distance(element_coord, target_coord) for target_coord in target_coords])
        distances.append((min_distance, element))

    distances.sort(key=lambda x: x[0])
    ratings = []
    for i in range(min(top_n, len(distances))):
        distance = distances[i][0]
        rating = (distances[0][0] / distance) * 100
        ratings.append((distances[i][1], rating))

    return [f"{element}, {rating: .2f}" for element, rating in ratings]


def recommendation_system(compounds, target_element, element_dict, top_n):
    set_a, set_b = separate_compounds(compounds, target_element)
    results = recommender(set_a, set_b, element_dict, top_n)
    return results

# print(recommendation_system(compounds,target_element,element_dict,10))
# Paste this ^^^ in main() to see the data format
# It might be slow so only run it once with the larger number first
# i.e. if you want both top 50 and top 3, set top_n to 50 and then use that data rather than
# running recommendation_system twice
