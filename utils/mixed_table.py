import matplotlib.pyplot as plt
import utils.appearance as props

def periodic_table_mixed(coord_df, mixed_compounds_elements, coord_sheet_name):
    """
    Generates a periodic table visualization with only the elements 
    from the mixed compounds list and returns the figure and axis.
    
    Args:
        coord_df (pd.DataFrame): DataFrame containing coordinates and element information.
        mixed_compounds_elements (set): A set of element symbols to include in the visualization.
        coord_sheet_name (str): Name of the sheet to determine shape type.
    
    Returns:
        tuple: Matplotlib figure and axis objects with the periodic table plotted.
    """
    # Filter the DataFrame to include only the required elements
    filtered_df = coord_df[coord_df['Symbol'].isin(mixed_compounds_elements)].copy()

    # Calculate the range of x and y values
    x_range = filtered_df['x'].max() - filtered_df['x'].min() + 2
    y_range = filtered_df['y'].max() - filtered_df['y'].min() + 2

    # Scale factor for adjusting the figure size
    figsize_x = x_range * props.mixed_scale_factor
    figsize_y = y_range * props.mixed_scale_factor

    # Create figure and axis with dynamic figsize
    fig, ax = plt.subplots(figsize=(figsize_x, figsize_y))

    # Determine whether to plot rectangles or circles based on the sheet name
    if "table" in coord_sheet_name.lower():
        ax = periodic_table_rectangle(ax, filtered_df)
    elif "plot" in coord_sheet_name.lower():
        ax = periodic_table_circle(ax, filtered_df)
    else:
        raise ValueError("Sheet name must contain 'table' or 'plot' to specify shape type.")

    # Set axis limits, margins, and visibility
    ax.set_xlim(filtered_df['x'].min() - props.mixed_x_margin, filtered_df['x'].max() + props.mixed_x_margin)
    ax.set_ylim(filtered_df['y'].min() - props.mixed_y_margin, filtered_df['y'].max() + props.mixed_y_margin)
    ax.set_xticks([])
    ax.set_yticks([])
    if not props.mixed_axis_visibility:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
    ax.set_aspect(props.mixed_aspect_ratio)

    return fig, ax

def periodic_table_circle(ax, df):
    """
    Plots periodic table elements as circles using mixed appearance settings.
    """
    for idx, row in df.iterrows():
        x = row['x']  # Use the x-coordinate from the DataFrame
        y = row['y']  # Use the y-coordinate from the DataFrame
        symbol = row['Symbol']  # Use the element symbol from the DataFrame

        # Plot the element as a circle with mixed appearance settings
        ax.add_patch(plt.Circle(
            (x, y),
            props.mixed_circle_radius,
            fill=None,
            edgecolor='black',
            lw=props.mixed_shape_linewidth
        ))
        ax.text(
            x, y, symbol,
            ha='center',
            va='center',
            fontsize=props.mixed_text_fontsize_circle,
            zorder=5,
        )

    return ax


def periodic_table_rectangle(ax, df):
    """
    Plots periodic table elements as rectangles using mixed appearance settings.
    """
    for idx, row in df.iterrows():
        x = row['x']  # Use the x-coordinate from the DataFrame
        y = row['y']  # Use the y-coordinate from the DataFrame
        symbol = row['Symbol']  # Use the element symbol from the DataFrame

        # Plot the element as a rectangle with mixed appearance settings
        ax.add_patch(plt.Rectangle(
            (x - 0.5, y - 0.5),
            props.mixed_rectangle_size,
            props.mixed_rectangle_size,
            fill=None,
            edgecolor='black',
            lw=props.mixed_shape_linewidth
        ))
        ax.text(
            x, y, symbol,
            ha='center',
            va='center',
            fontsize=props.mixed_text_fontsize_rectangle,
            weight=props.mixed_text_weight_rectangle,
            zorder=5
        )

    return ax

def generate_mixed_compound_visualizations(coord_df, mixed_compounds_groups, coord_sheet_name):
    """
    Generates periodic table visualizations for each group of mixed compounds 
    and returns a list of figures and axes for further processing.
    
    Args:
        coord_df (pd.DataFrame): DataFrame containing coordinates and element information.
        mixed_compounds_groups (list of lists): Groups of mixed compounds, where each group is a list of Compound objects.
        coord_sheet_name (str): Name of the sheet to determine shape type (e.g., "table" or "plot").
    
    Returns:
        list: A list of tuples (fig, ax) for each group's visualization.
    """
    figures_and_axes = []

    for group in mixed_compounds_groups:
        # Extract the unique elements for the current group
        group_elements = set()
        for compound in group:
            group_elements.update(compound.elements.keys())

        # Generate the visualization for this group
        fig, ax = periodic_table_mixed(coord_df, group_elements, coord_sheet_name)
        figures_and_axes.append((fig, ax))

    return figures_and_axes