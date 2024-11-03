import numpy as np


def calculate_coordinates(compound, element_dict, fixed_number=None):
    counts = []
    coordinates = []
    for index, (element, count) in enumerate(compound.elements.items(), start=1):
        if index == fixed_number and len(compound.elements) == 3:
            continue
        if element in element_dict:
            x, y = element_dict[element]
            counts.append(count)
            coordinates.append((x, y))

    weight = np.array(counts)
    coord_array = np.array(coordinates)
    weighted_average = np.average(coord_array, weights=weight, axis=0)
    return weighted_average, coord_array
