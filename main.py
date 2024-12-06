import click
import os
from data_processing.input_handler import input_handler, list_excel_files
from data_processing.coord_excel_handler import *
from data_processing.make_periodic_table import periodic_table
from display_data import *
from make_data.neighbors_search import recommendation_system, save_recommendations_to_excel
from make_data import make_compound_data  # Import the consolidated function
from data_processing.compound_object import pick_what_separate

@click.command()
def main():
    """
    Processes Excel file and visualizes binary and ternary compounds via periodic table.
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

    # Generate the compound data dynamically
    compounds_binary, compounds_ternary = make_compound_data(file_path, user_input_sheet_numbers)

    # Process binary compounds if any
    if compounds_binary:
        target_element = pick_what_separate(compounds_binary)  # Pass the binary compounds

        if target_element:
            for compound in compounds_binary:
                compound.separate_by_element(target_element)
            compounds_binary.sort(key=lambda x: f"(with {target_element})" in x.structure)

            display_binary_data_type(periodic_table_ax, compounds_binary, element_dict, coord_sheet_name)
            top_n = 50  # Specify the number of top recommendations to save
            recommendations = recommendation_system(compounds_binary, target_element, element_dict, top_n)
            save_recommendations_to_excel(recommendations, target_element)
            click.echo("Binary compounds processed.")
        else:
            # If no target element is selected, just display the binary data
            display_binary_data_type(periodic_table_ax, compounds_binary, element_dict, coord_sheet_name)
            click.echo("No target element selected. Binary structures visualization saved to the /plots folder.")
    # Process ternary compounds if any
    if compounds_ternary:           
        target_elements = pick_what_separate(compounds_ternary)

        if target_elements:
            for compound in compounds_ternary:
                compound.separate_by_element(target_elements)
            if isinstance(target_elements, list):
                formatted_target = " and ".join(target_elements)
            else:
                formatted_target = target_elements

            compounds_ternary.sort(key=lambda x: f"(with {formatted_target})" in x.structure)

            display_ternary_data_type(periodic_table_ax, compounds_ternary, element_dict, coord_sheet_name)
            top_n = 50
            recommendations = recommendation_system(compounds_ternary, target_elements, element_dict, top_n)
            save_recommendations_to_excel(recommendations, formatted_target)
            click.echo("Ternary compounds processed.")
        else:
            display_ternary_data_type(periodic_table_ax, compounds_ternary, element_dict, coord_sheet_name)
            click.echo("No target element selected. Ternary structures visualization saved to the /plots folder.")
    return 0

if __name__ == '__main__':
    main()