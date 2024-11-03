from data_processing.verify_elements import verify_elements
from data_processing.calculate_compound_coord import calculate_coordinates
from data_processing.markers import marker_types, colors
from matplotlib import pyplot as plt


def display_ternary_data_type(ax, compounds, element_dict, coord_sheet_name):
    structures = set(compound.structure for compound in compounds)
    structure_colors = {structure: colors[i % len(colors)] for i, structure in enumerate(structures)}
    added_labels = set()

    # Dictionary to track how many rectangles are drawn for each (x, y)
    rectangle_counts = {}
    # Dictionary to track which colors have already been applied to each (x, y)
    applied_colors = {}
    structure_markers = {}
    marker_index = 0

    for compound in compounds:
        verify_elements(compound, element_dict)
        structure = compound.structure

        center, original_coordinates = calculate_coordinates(compound, element_dict)
        center_x, center_y = center
        color = structure_colors.get(structure)

        if structure not in structure_markers:
            structure_markers[structure] = marker_types[marker_index]
            marker_index += 1
        marker = structure_markers[structure]

        # Plot the center point for the compound using the marker
        if structure not in added_labels:
            ax.scatter(center_x, center_y, edgecolors=color, facecolors='None', label=f'{structure}', zorder=4, s=200,
                       marker=marker, alpha=0.5, linewidths=4)
            added_labels.add(structure)
        else:
            ax.scatter(center_x, center_y, edgecolors=color, facecolors='None', zorder=4, s=200, marker=marker,
                       alpha=0.5, linewidths=4)

        # Loop through each element in the compound
        for x, y in original_coordinates:
            ax.plot([center_x, x], [center_y, y], color=color, linestyle='-', zorder=2, alpha=0.1)
            # For other elements, draw rectangles and connecting lines as usual
            if (x, y) not in rectangle_counts:
                rectangle_counts[(x, y)] = 0
            if (x, y) not in applied_colors:
                applied_colors[(x, y)] = set()

            # Skip if this color has already been applied to this (x, y)
            if color in applied_colors[(x, y)]:
                continue

            # Get the current count for this element (how many rectangles drawn)
            count = rectangle_counts[(x, y)]

            # Draw the rectangle with the current size and offset
            if "table" in coord_sheet_name.lower():
                # Calculate size and offset for the new rectangle (progressively smaller)
                shrink_factor = 0.15 * count  # Smaller shrink for each additional color
                size = 0.92 - shrink_factor  # Start with 0.92 and decrease with each rectangle
                offset = 0.46 - shrink_factor / 2  # Adjust the offset to keep it centered
                ax.add_patch(plt.Rectangle((x - offset, y - offset), size, size, fill=False, edgecolor=color, zorder=4,
                                           linewidth=5, alpha=0.8))
            else:
                shrink_factor = 0.05 * count  # Smaller shrink for each additional color
                size = 0.25 - shrink_factor  # Start with 0.92 and decrease with each rectangle
                ax.add_patch(plt.Circle((x, y), size, fill=False, edgecolor=color, zorder=4,
                                        linewidth=5, alpha=0.8))

            # Mark this color as applied to this (x, y)
            applied_colors[(x, y)].add(color)

            # Increment the count for this element
            rectangle_counts[(x, y)] += 1

    plt.legend(
        loc='upper center',  # Change legend position
        fontsize=24,  # Increase font size for labels
        frameon=False,  # Show legend frame
        framealpha=1,  # Set transparency of the frame
        edgecolor='black',  # Set edge color of the frame
        markerscale=1,  # Increases the size of markers in the legend
        ncol=3
    )
    plt.savefig("ternary.png", dpi=600, bbox_inches='tight')
    plt.show()
