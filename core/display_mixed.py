import os
from utils.verify_elements import verify_elements
from utils.table_coordinates import calculate_coordinates
import utils.appearance as props  # Import as a namespace
from utils.mixed_table import periodic_table_mixed
from matplotlib import pyplot as plt


def highlight_and_save(ax, compounds, element_dict, coord_sheet_name, fig, output_folder="output", group_index=None):
    """
    Adds highlights (e.g., rectangles, circles) to an existing periodic table plot and saves the result.
    
    Args:
        ax: Matplotlib axis object with the periodic table plotted.
        compounds (list or tuple): List or tuple of Compound objects to highlight.
        element_dict (dict): Dictionary of element information for coordinate calculations.
        coord_sheet_name (str): Name of the sheet to determine shape type.
        fig: Matplotlib figure object associated with the axis.
        output_folder (str): Directory to save the final plot.
        group_index (int, optional): Unique identifier for the group, used in file naming.
    """

    os.makedirs(output_folder, exist_ok=True)

    structures = sorted(set(compound.structure for compound in compounds))
    structure_colors = {structure: props.mixed_colors[i % len(props.mixed_colors)] for i, structure in enumerate(structures)}
    added_labels = set()

    for compound in compounds:
        verify_elements(compound, element_dict)
        structure = compound.structure

        center, original_coordinates = calculate_coordinates(compound, element_dict)
        center_x, center_y = center
        coords_x, coords_y = zip(*original_coordinates)
        color = structure_colors.get(structure)

        # Highlight the center point
        if structure not in added_labels:
            ax.scatter(center_x, center_y, edgecolors=color, facecolors='None', label=f'{structure}',
                       zorder=4, s=props.mixed_marker_size, marker=props.mixed_marker_types[0], alpha=1, linewidths=4)
            added_labels.add(structure)
        else:
            ax.scatter(center_x, center_y, edgecolors=color, facecolors='None',
                       zorder=4, s=props.mixed_marker_size, marker=props.mixed_marker_types[0], alpha=1, linewidths=4)

        # Add rectangles or circles at original coordinates
        for x, y in original_coordinates:
            ax.plot([center_x, x], [center_y, y], color=color, linestyle='-', zorder=2, alpha=0.1)
            if "table" in coord_sheet_name.lower():
                ax.add_patch(plt.Rectangle((x - 0.5, y - 0.5), props.mixed_rectangle_size, props.mixed_rectangle_size,
                                           fill=False, edgecolor=color, zorder=4, linewidth=props.mixed_shape_linewidth, alpha=0.8))
            else:
                ax.add_patch(plt.Circle((x, y), props.mixed_circle_size, fill=False, edgecolor=color,
                                        zorder=4, linewidth=props.mixed_shape_linewidth, alpha=0.8))

    # Add legend dynamically
    ax.legend(
        loc="upper center",  
        bbox_to_anchor=(0.5, 1.1),  
        **props.mixed_legend_props 
    )

    # Save the final plot
    if group_index is not None:
        file_name = f"Mixed_{group_index}_{coord_sheet_name.replace(' ', '_')}.png"
    else:
        file_name = f"unnamed_group_{coord_sheet_name.replace(' ', '_')}.png"

    output_path = os.path.join(output_folder, file_name)
    fig.savefig(output_path, dpi=props.dpi, bbox_inches=props.bbox_inches)
    plt.close(fig)

    print(f"Plots for compounds with mixing saved in {output_path}")

def process_and_visualize_mixed_compounds(coord_df, mixed_compounds_groups, coord_sheet_name, element_dict):
    """
    Processes and visualizes mixed compounds, generating and saving plots with highlights.

    Args:
        coord_df (pd.DataFrame): DataFrame containing periodic table data.
        mixed_compounds_groups (list of lists): Groups of mixed compounds, each a list of Compound objects.
        coord_sheet_name (str): Sheet name used to determine plot style.
        element_dict (dict): Dictionary containing element data for coordinate calculations.
    """
    output_folder = "plots/mixed-compound-plots"
    os.makedirs(output_folder, exist_ok=True)
    
    print("\nMixed Compounds Detected:")
    for i, group in enumerate(mixed_compounds_groups):
        print(f"Group {i + 1}:")
        group_elements = set()
        for compound in group:
            group_elements.update(compound.elements.keys())
            print(f"  Formula: {compound.formula}, Structure: {compound.structure}")
            
        # Generate the base plot for the mixed compound group
        fig, ax = periodic_table_mixed(coord_df, group_elements, coord_sheet_name)  # Get new figure and axis

        # Add highlights and save the plot with a unique group index
        highlight_and_save(ax, group, element_dict, coord_sheet_name, fig, output_folder, group_index=i + 1)

    print(f"All mixed compound visualizations saved in: {output_folder}")