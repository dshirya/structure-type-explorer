import pandas as pd
import numpy as np


def excel_to_dataframe(sheet_name):
    file_name = 'program_data/table_coordinates.xlsx'
    df = pd.read_excel(file_name, sheet_name, skiprows=0)

    df_filtered = df[df['Include'] == 1].copy()
    return df_filtered, sheet_name

def create_element_dict(df):
    return {row['Symbol']: (row['x'], row['y']) for _, row in df.iterrows()}

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
