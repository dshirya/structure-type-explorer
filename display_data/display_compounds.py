import os
from data_processing.verify_elements import verify_elements
from data_processing.calculate_compound_coord import calculate_coordinates
import data_processing.appearance as props  # Import as a namespace
from matplotlib import pyplot as plt

def save_plot(structure, coord_sheet_name, ax, folder=props.plot_folder):
    os.makedirs(folder, exist_ok=True)

    structure_clean = structure.replace(" ", "_")
    coord_sheet_clean = coord_sheet_name.replace(" ", "_")

    base_filename = f"{structure_clean}_{coord_sheet_clean}{props.file_extension}"
    file_path = os.path.join(folder, base_filename)

    counter = 1
    while os.path.exists(file_path):
        file_path = os.path.join(
            folder,
            f"{structure_clean}_{coord_sheet_clean}_{counter}{props.file_extension}"
        )
        counter += 1

    plt.savefig(file_path, dpi=props.dpi, bbox_inches=props.bbox_inches)
    print(f"Plot saved as {file_path}")

def display_data(ax, compounds, element_dict, coord_sheet_name):
    structures = sorted(set(compound.structure for compound in compounds))
    structure_colors = {structure: props.colors[i % len(props.colors)] for i, structure in enumerate(structures)}
    added_labels = set()

    rectangle_counts = {}
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
            structure_markers[structure] = props.marker_types[marker_index]
            marker_index += 1
        marker = structure_markers[structure]

        #ax.plot(coords_x, coords_y, color=color, linestyle='-', zorder=2, alpha=0.1)

        if structure not in added_labels:
            ax.scatter(center_x, center_y, edgecolors=color, facecolors='None', label=f'{structure}',
                       zorder=4, s=props.marker_size, marker=marker, alpha=1, linewidths=4)
            added_labels.add(structure)
        else:
            ax.scatter(center_x, center_y, edgecolors=color, facecolors='None',
                       zorder=4, s=props.marker_size, marker=marker, alpha=1, linewidths=4)

        for x, y in original_coordinates:
            ax.plot([center_x, x], [center_y, y], color=color, linestyle='-', zorder=2, alpha=0.1)
            if (x, y) not in rectangle_counts:
                rectangle_counts[(x, y)] = 0
            if (x, y) not in applied_colors:
                applied_colors[(x, y)] = set()

            if color in applied_colors[(x, y)]:
                continue

            count = rectangle_counts[(x, y)]

            if "table" in coord_sheet_name.lower():
                shrink_factor = props.shrink_factor_rect * count
                size = props.initial_rect_size - shrink_factor
                offset = props.initial_rect_offset - shrink_factor / 2
                ax.add_patch(plt.Rectangle((x - offset, y - offset), size, size, fill=False,
                                           edgecolor=color, zorder=4, linewidth=5, alpha=0.8))
            else:
                shrink_factor = props.shrink_factor_circle * count
                size = props.circle_size - shrink_factor
                ax.add_patch(plt.Circle((x, y), size, fill=False, edgecolor=color,
                                        zorder=4, linewidth=4, alpha=0.8))

            applied_colors[(x, y)].add(color)
            rectangle_counts[(x, y)] += 1

    plt.legend(**props.legend_props)
    save_plot(structure, coord_sheet_name, ax)