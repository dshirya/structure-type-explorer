import click
from data_processing.input_handler import input_handler, list_excel_files
from data_processing.coord_excel_handler import *  # noqa: F403
from data_processing.make_periodic_table import periodic_table
from display_data import *  # noqa: F403
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
    coord_df, coord_sheet_name = excel_to_dataframe()  # noqa: F405
    element_dict = create_element_dict(coord_df)  # noqa: F405
    periodic_table_ax = periodic_table(coord_df, coord_sheet_name)

    # Generate the compound data dynamically
    compounds_binary, compounds_ternary = make_compound_data(file_path, user_input_sheet_numbers)

    # Combine binary and ternary compounds
    all_compounds = compounds_binary + compounds_ternary

    if all_compounds:
        # Unified logic for picking fixed elements
        fixed_elements = pick_what_separate(all_compounds)

        if fixed_elements:
            # Update entry prototypes and process compounds
            for compound in all_compounds:
                if len(compound.elements) == 2 and 'binary' in fixed_elements:
                    compound.separate_by_element(fixed_elements['binary'])
                elif len(compound.elements) == 3 and 'ternary' in fixed_elements:
                    compound.separate_by_element(fixed_elements['ternary'])

            # Sort compounds by structure for consistent visualization
            all_compounds.sort(key=lambda x: x.structure)

            # Display and generate visualizations
            display_data(periodic_table_ax, all_compounds, element_dict, coord_sheet_name)  # noqa: F405

            # Recommendations
            top_n = 50  # Specify the number of top recommendations to save
            recommendations_binary = recommendation_system(compounds_binary, fixed_elements.get('binary'), element_dict, top_n)
            recommendations_ternary = recommendation_system(compounds_ternary, fixed_elements.get('ternary'), element_dict, top_n)

            # Save recommendations to Excel
            if 'binary' in fixed_elements:
                save_recommendations_to_excel(recommendations_binary, fixed_elements['binary'])
            if 'ternary' in fixed_elements:
                formatted_target = " and ".join(fixed_elements['ternary'])
                save_recommendations_to_excel(recommendations_ternary, formatted_target)

            click.echo("Compounds processed and visualized.")
        else:
            # Display compounds without separation
            display_binary_data_type(periodic_table_ax, compounds_binary, element_dict, coord_sheet_name)  # noqa: F405
            display_ternary_data_type(periodic_table_ax, compounds_ternary, element_dict, coord_sheet_name)  # noqa: F405
            click.echo("No target elements selected. Visualizations saved to the /plots folder.")
    else:
        click.echo("No compounds found in the dataset.")
    return 0


if __name__ == '__main__':
    main()