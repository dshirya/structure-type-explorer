import os
from data_processing.verify_elements import verify_elements
from data_processing.calculate_compound_coord import calculate_coordinates
from data_processing.markers import marker_types, colors
from matplotlib import pyplot as plt

def save_plot(structure, coord_sheet_name, ax, folder="plots"):
    # Ensure the folder exists
    os.makedirs(folder, exist_ok=True)

    # Sanitize the file name components
    structure_clean = structure.replace(" ", "_")
    coord_sheet_clean = coord_sheet_name.replace(" ", "_")

    # Initial filename template
    base_filename = f"{structure_clean}_{coord_sheet_clean}.png"
    file_path = os.path.join(folder, base_filename)

    # Check if a file with this name exists, and increment if necessary
    counter = 1
    while os.path.exists(file_path):
        file_path = os.path.join(folder, f"{structure_clean}_{coord_sheet_clean}_{counter}.png")
        counter += 1

    # Save the plot with the unique file path
    plt.savefig(file_path, dpi=600, bbox_inches='tight')
    print(f"Plot saved as {file_path}")

def display_binary_data_type(ax, compounds, element_dict, coord_sheet_name):
    # Danila's code here (Edited a bit to work properly).
    structures = sorted(set(compound.structure for compound in compounds))
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
        coords_x, coords_y = zip(*original_coordinates)
        color = structure_colors.get(structure)

        if structure not in structure_markers:
            structure_markers[structure] = marker_types[marker_index]
            marker_index += 1
        marker = structure_markers[structure]

        ax.plot(coords_x, coords_y, color=color, linestyle='-', zorder=2, alpha=0.1)

        # Plot the center point for the compound using the marker
        if structure not in added_labels:
            ax.scatter(center_x, center_y, edgecolors=color, facecolors='None', label=f'{structure}', zorder=4, s=200,
                       marker=marker, alpha=1, linewidths=4)
            added_labels.add(structure)
        else:
            ax.scatter(center_x, center_y, edgecolors=color, facecolors='None', zorder=4, s=200, marker=marker, alpha=1,
                       linewidths=4)

        # Loop through each element in the compound
        for x, y in original_coordinates:
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
                shrink_factor = 0.054 * count  # Smaller shrink for each additional color
                size = 0.26 - shrink_factor  # Start with 0.92 and decrease with each rectangle
                ax.add_patch(plt.Circle((x, y), size, fill=False, edgecolor=color, zorder=4,
                                        linewidth=4, alpha=0.8))
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

    # Use the helper function to save the plot with a unique name
    save_plot(structure, coord_sheet_name, ax)