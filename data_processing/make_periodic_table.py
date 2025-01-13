import matplotlib.pyplot as plt
import data_processing.appearance as props

def periodic_table(coord_df, coord_sheet_name):
    # Calculate the range of x and y values
    x_range = coord_df['x'].max() - coord_df['x'].min() + 1
    y_range = coord_df['y'].max() - coord_df['y'].min() + 1

    # Scale factor for adjusting the figure size
    figsize_x = x_range * props.scale_factor
    figsize_y = y_range * props.scale_factor

    # Create figure and axis with dynamic figsize
    fig, ax = plt.subplots(figsize=(figsize_x, figsize_y))

    # Determine whether to plot rectangles or circles based on the sheet name
    if "table" in coord_sheet_name.lower():
        ax = periodic_table_rectangle(ax, coord_df)
    elif "plot" in coord_sheet_name.lower():
        ax = periodic_table_circle(ax, coord_df)
    else:
        raise ValueError("Sheet name must contain 'table' or 'plot' to specify shape type.")

    # Set axis limits, margins, and visibility
    ax.set_xlim(coord_df['x'].min() - props.x_margin, coord_df['x'].max() + props.x_margin)
    ax.set_ylim(coord_df['y'].min() - props.y_margin, coord_df['y'].max() + props.y_margin)
    ax.set_xticks([])
    ax.set_yticks([])
    if not props.axis_visibility:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
    ax.set_aspect(props.aspect_ratio)

    return ax


def periodic_table_circle(ax, df):
    for idx, row in df.iterrows():
        include = row['Include']
        if include == 0:
            continue

        x = row['x']  # Use the x-coordinate from the DataFrame
        y = row['y']  # Use the y-coordinate from the DataFrame
        symbol = row['Symbol']  # Use the element symbol from the DataFrame

        # Plot the element as a circle
        ax.add_patch(plt.Circle(
            (x, y),
            props.circle_radius,
            fill=None,
            edgecolor='black',
            lw=props.shape_linewidth
        ))
        ax.text(
            x, y, symbol,
            ha='center',
            va='center',
            fontsize=props.text_fontsize_circle,
            zorder=5,
        )

    return ax


def periodic_table_rectangle(ax, df):
    for idx, row in df.iterrows():
        include = row['Include']
        if include == 0:
            continue

        x = row['x']  # Use the x-coordinate from the DataFrame
        y = row['y']  # Use the y-coordinate from the DataFrame
        symbol = row['Symbol']  # Use the element symbol from the DataFrame

        # Plot the element as a rectangle
        ax.add_patch(plt.Rectangle(
            (x - 0.5, y - 0.5),
            props.rectangle_size,
            props.rectangle_size,
            fill=None,
            edgecolor='black',
            lw=props.shape_linewidth
        ))
        ax.text(
            x, y, symbol,
            ha='center',
            va='center',
            fontsize=props.text_fontsize_rectangle,
            weight=props.text_weight_rectangle,
            zorder=5
        )

    return ax