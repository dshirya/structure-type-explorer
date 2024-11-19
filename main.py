import click
import os
from data_processing.input_handler import input_handler, list_excel_files
from data_processing.coord_excel_handler import *
from data_processing.make_periodic_table import periodic_table
from make_data import *
from display_data import *
from data_processing.compound_object import pick_what_separate  
from make_data.neighbors_search import recommendation_system, save_recommendations_to_excel

@click.command()
def main():
    """
    Processes Excel file and visualizes binary compounds via periodic table.
    Maintained by Brian Hoang & Danila Shiryaev.
    """

    # Get the file_path from the user's selection
    file_path = list_excel_files()
    if not file_path:
        return  # Exit if no valid file is chosen

    # Process the selected Excel file
    user_input_sheet_numbers = input_handler(file_path)
    coord_df, coord_sheet_name = excel_to_dataframe()
    element_dict = create_element_dict(coord_df)
    periodic_table_ax = periodic_table(coord_df, coord_sheet_name)

    # Generate the compound data
    compounds = make_binary_data(file_path, user_input_sheet_numbers)
    target_element = pick_what_separate()  # This will always prompt the user

    if target_element:
        for compound in compounds:
            compound.separate_by_element(target_element)
        # Sort compounds to move modified structures with "(with {element})" to the end
        compounds.sort(key=lambda x: f"(with {target_element})" in x.structure)

        # Display binary data type on the periodic table visualization
        display_binary_data_type(periodic_table_ax, compounds, element_dict, coord_sheet_name)

        # Generate recommendations and save them to an Excel file
        top_n = 50  # Specify the number of top recommendations to save (you can adjust this)
        recommendations = recommendation_system(compounds, target_element, element_dict, top_n)
        save_recommendations_to_excel(recommendations, target_element)
    else:
        click.echo("Continuing without separating by any element.")
        # Display binary data type on the periodic table visualization
        display_binary_data_type(periodic_table_ax, compounds, element_dict, coord_sheet_name)

    # Program continues to run even if no element is chosen for separation
    click.echo("Program completed successfully.")

    return 0

if __name__ == '__main__':
    main()