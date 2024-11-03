import click
import os
from data_processing.input_handler import input_handler
from data_processing.coord_excel_handler import *
from data_processing.make_periodic_table import periodic_table
from make_data import *
from display_data import *
from data_processing.compound_object import pick_what_separate  

def list_excel_files():
    # List all Excel files in the current directory
    excel_files = [f for f in os.listdir() if f.endswith('.xlsx') or f.endswith('.xls')]
    if not excel_files:
        click.echo("No Excel files found in the current directory.")
        return None

    # Display the files with an index
    click.echo("Select an Excel file by number:")
    for i, file in enumerate(excel_files, start=1):
        click.echo(f"{i}. {file}")

    # Prompt the user to select a file by index
    choice = click.prompt("Enter the number of the file", type=int)
    if 1 <= choice <= len(excel_files):
        return excel_files[choice - 1]
    else:
        click.echo("Invalid choice. Exiting.")
        return None

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
    target_element = pick_what_separate()
    if target_element:
        for compound in compounds:
            compound.separate_by_element(target_element)
        # Sort compounds to move modified structures with "(with {element})" to the end
        compounds.sort(key=lambda x: f"(with {target_element})" in x.structure)
    display_binary_data_type(periodic_table_ax, compounds, element_dict, coord_sheet_name)

    return 0


if __name__ == '__main__':
    main()