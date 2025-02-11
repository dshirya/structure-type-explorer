import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

ELEMENTAL_PROPERTIES_FILE = "program_data/elemental-property-list.xlsx"  # Predefined property file

def generate_coordinates(compounds, use_full_element_list=False):
    """
    Generates PCA-based coordinates dynamically for the elements in the dataset
    or the full periodic table list.

    Args:
        compounds (list): List of compound objects containing element information.
        use_full_element_list (bool): If True, uses all elements from the predefined property file.

    Returns:
        DataFrame: A DataFrame containing PCA-based coordinates for elements.
    """
    if use_full_element_list:
        data = pd.read_excel(ELEMENTAL_PROPERTIES_FILE)
    else:
        # Extract unique elements from the dataset
        elements_to_include = {element for compound in compounds for element in compound.elements}
        data = pd.read_excel(ELEMENTAL_PROPERTIES_FILE)
        data = data[data['Symbol'].isin(elements_to_include)]  # Filter elements based on dataset

    # Automatically drop columns with NaN values
    data = data.dropna(axis=1)

    # Select only numeric columns for PCA
    numeric_data = data.select_dtypes(include=['float64', 'int64']).copy()
    numeric_data.dropna(inplace=True)

    # Ensure 'Symbol' column matches the filtered numeric data index
    symbol_data = data.loc[numeric_data.index, 'Symbol'] if 'Symbol' in data.columns else None

    # Standardize the data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(numeric_data)

    # Perform PCA to reduce to two dimensions
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(scaled_data)

    # Create a DataFrame for PCA results
    pca_df = pd.DataFrame(data=principal_components, columns=['x', 'y'])
    if symbol_data is not None:
        pca_df['Symbol'] = symbol_data.reset_index(drop=True)  # Reset index to align correctly

    pca_df['Include'] = 1  # Mark all elements as included

    return pca_df[['Symbol', 'x', 'y', 'Include']] if 'Symbol' in pca_df.columns else pca_df[['x', 'y', 'Include']]

def create_element_dict(df):
    """
    Creates a dictionary mapping element symbols to their PCA-generated coordinates.

    Args:
        df (DataFrame): DataFrame containing element coordinates.

    Returns:
        dict: Dictionary with element symbols as keys and (x, y) tuples as values.
    """
    return {row['Symbol']: (row['x'], row['y']) for _, row in df.iterrows()}

def calculate_coordinates(compound, element_dict, fixed_number=None):
    """
    Computes the weighted average position of elements in a compound.

    Args:
        compound: Compound object containing element counts.
        element_dict (dict): Dictionary mapping elements to coordinates.
        fixed_number (int, optional): If provided, fixes a specific element's contribution.

    Returns:
        tuple: Weighted average coordinates and the array of individual element coordinates.
    """
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