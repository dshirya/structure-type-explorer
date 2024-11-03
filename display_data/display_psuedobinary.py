from data_processing.verify_elements import verify_elements
from data_processing.calculate_compound_coord import calculate_coordinates
from data_processing.markers import marker_types, colors
import numpy as np
import matplotlib.patches as patches
from matplotlib import pyplot as plt


def display_pseudobinary_data_type(ax, compounds, fixed_number, element_dict, coord_sheet_name):
    added_labels = set()
    structure_marker_map = {}  # To keep track of structures used
    color_map = {}  # To keep track of colors used for fixed element
    structure_marker_counter = 0
    color_counter = 0

    for compound in compounds:
        verify_elements(compound, element_dict)
        jitter = np.random.uniform(0, 0)
        jitter = np.random.uniform(-0.10, 0.10)

        structure = compound.structure
        if structure not in structure_marker_map:
            structure_marker_map[structure] = marker_types[structure_marker_counter]
            structure_marker_counter += 1
        marker = structure_marker_map[structure]
        center, original_coordinates = calculate_coordinates(compound, element_dict, fixed_number)
        center_x, center_y = center + jitter  # Jitter to prevent overlap
        coords_x, coords_y = zip(*original_coordinates)

        # Logic for jittering the lines drawn
        coords_x = [x + jitter for x in coords_x]
        coords_y = [y + jitter for y in coords_y]

        if len(compound.elements) == 2:
            is_binary = True
        else:
            is_binary = False

        if is_binary:
            if structure not in added_labels:
                ax.scatter(center_x, center_y, edgecolors='black', facecolors='None', label=f'{structure}',
                           zorder=4, s=200, marker=marker, alpha=0.5, linewidths=4)
                added_labels.add(structure)
            else:
                ax.scatter(center_x, center_y, edgecolors='black', facecolors='None', zorder=4, s=200, marker=marker,
                           alpha=0.5, linewidths=4)


                ax.plot(coords_x, coords_y, color='black', zorder=3, linestyle='-', alpha=0.5)

                #ax.plot(coords_x, coords_y, color='black', zorder=3, linestyle='-', alpha=0.5)

        if not is_binary:
            elements = compound.elements
            fixed_number = fixed_number - 1
            fixed_element = list(elements.keys())[fixed_number]

            if fixed_element not in color_map:
                color_map[fixed_element] = colors[color_counter % len(colors)]
                color_counter += 1
            color = color_map[fixed_element]
            x, y = element_dict[fixed_element]
            if "table" in coord_sheet_name.lower():
                rectangle = patches.Rectangle((x - 0.5, y - 0.5), 1, 1, facecolor=color)
            else:
                rectangle = patches.Circle((x, y), 0.29, facecolor=color)
            ax.add_patch(rectangle)
            ax.scatter(center_x, center_y, edgecolors=color, facecolors='None', zorder=4, s=50, marker=marker,
                       alpha=0.5)
            ax.plot(coords_x, coords_y, color=color, zorder=3, linestyle='-', alpha=0.1)

    plt.legend(
        loc='upper center',  # Change legend position
        fontsize=24,  # Increase font size for labels
        frameon=False,  # Show legend frame
        framealpha=1,  # Set transparency of the frame
        edgecolor='black',  # Set edge color of the frame
        markerscale=1,  # Increases the size of markers in the legend
        ncol=3
    )

    plt.savefig("pseudobinary.png", dpi=600, bbox_inches='tight')
    plt.show()

