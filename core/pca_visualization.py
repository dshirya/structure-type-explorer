import os
import matplotlib.pyplot as plt
from utils import appearance as props
from utils import pca_coordinates
from utils.verify_elements import verify_elements

def save_plot(structure, coord_sheet_name, ax, folder=props.plot_folder) -> None:
    """
    Saves the plotted periodic table.

    Args:
        structure (str): Name of the structure.
        coord_sheet_name (str): Name of the coordinate sheet used.
        ax: Matplotlib axis object.
        folder (str): Directory to save the plot.
    """
    os.makedirs(folder, exist_ok=True)

    structure_clean = structure.replace(" ", "_")
    coord_sheet_clean = coord_sheet_name.replace(" ", "_")

    base_filename = f"{structure_clean}_{coord_sheet_clean}{props.file_extension}"
    file_path = os.path.join(folder, base_filename)

    counter = 1
    while os.path.exists(file_path):
        file_path = os.path.join(folder, f"{structure_clean}_{coord_sheet_clean}_{counter}{props.file_extension}")
        counter += 1

    plt.savefig(file_path, dpi=props.dpi, bbox_inches=props.bbox_inches)
    print(f"Plot saved as {file_path}")

def PCA_plot(compounds, use_full_element_list=False) -> plt.Axes:
    """
    Plots a periodic table dynamically based on the elements present in the dataset.

    Args:
        compounds (list): List of compound objects containing element information.
        use_full_element_list (bool): If True, generates coordinates for all elements.

    Returns:
        ax: Matplotlib axis object.
    """
    # Generate PCA-based element coordinates dynamically
    coord_df = pca_coordinates.generate_coordinates(compounds, use_full_element_list)
    element_dict = pca_coordinates.create_element_dict(coord_df)

    # Define figure size dynamically
    x_range = coord_df['x'].max() - coord_df['x'].min() + 1
    y_range = coord_df['y'].max() - coord_df['y'].min() + 1
    figsize_x = x_range * props.scale_factor
    figsize_y = y_range * props.scale_factor

    fig, ax = plt.subplots(figsize=(figsize_x, figsize_y))

    # Plot elements dynamically
    for idx, row in coord_df.iterrows():
        x, y, symbol = row['x'], row['y'], row['Symbol']
        ax.add_patch(plt.Circle((x, y), props.circle_radius, fill=None, edgecolor='black', lw=props.shape_linewidth))
        ax.text(x, y, symbol, ha='center', va='center', fontsize=props.text_fontsize_circle, zorder=5)

    # Remove axis labels and ticks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    
    # Highlight compounds dynamically
    display_data(ax, compounds, element_dict)


    return ax

def display_data(ax, compounds, element_dict) -> None:
    """
    Highlights compounds by marking their elements with different styles.

    Args:
        ax: Matplotlib axis object.
        compounds (list): List of compound objects.
        element_dict (dict): Dictionary of element coordinates.
    """
    structures = sorted(set(compound.structure for compound in compounds))
    structure_colors = {structure: props.colors[i % len(props.colors)] for i, structure in enumerate(structures)}
    added_labels = set()

    rectangle_counts = {}
    applied_colors = {}
    structure_markers = {}
    marker_index = 0

    coordinates_cache = {}
    for compound in compounds:
        verify_elements(compound, element_dict)
        structure = compound.structure

        if compound not in coordinates_cache:
            coordinates_cache[compound] = pca_coordinates.calculate_coordinates(compound, element_dict)
        
        center, original_coordinates = coordinates_cache[compound]
        center_x, center_y = center
        color = structure_colors.get(structure)
        color = structure_colors.get(structure)

        if structure not in structure_markers:
            structure_markers[structure] = props.marker_types[marker_index]
            marker_index += 1
        marker = structure_markers[structure]

        # Apply color to elements
        if structure not in added_labels:
            ax.scatter(center_x, center_y, edgecolors=color, facecolors='None', label=f'{structure}',
                       zorder=4, s=props.marker_size, marker=marker, alpha=1, linewidths=4)
            added_labels.add(structure)
        else:
            ax.scatter(center_x, center_y, edgecolors=color, facecolors='None',
                       zorder=4, s=props.marker_size, marker=marker, alpha=1, linewidths=4)

        for x, y in original_coordinates:
            ax.plot([center_x, x], [center_y, y], color=color, linestyle='-', zorder=2, alpha=0.1)  # Line from element to the marker
            if (x, y) not in rectangle_counts:
                rectangle_counts[(x, y)] = 0
            if (x, y) not in applied_colors:
                applied_colors[(x, y)] = set()

            if color in applied_colors[(x, y)]:
                continue

            count = rectangle_counts[(x, y)]

           
            shrink_factor = props.shrink_factor_circle * count
            size = props.circle_size - shrink_factor
            ax.add_patch(plt.Circle((x, y), size, fill=False, edgecolor=color,
                                        zorder=4, linewidth=props.linewidth_circle, alpha=0.8))  

            applied_colors[(x, y)].add(color)
            rectangle_counts[(x, y)] += 1

    plt.legend(**props.legend_props)
    save_plot(compounds[0].structure, 'PCA_plot', ax)