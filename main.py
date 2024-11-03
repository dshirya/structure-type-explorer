import argparse
from data_processing.input_handler import input_handler
from data_processing.coord_excel_handler import *
from data_processing.make_periodic_table import periodic_table
from make_data import *
from display_data import *
from data_processing.compound_object import pick_what_separate  


def main():
    # Code for obtaining the user's input
    parser = argparse.ArgumentParser(
        prog='Data Visualization Tool',
        usage='py data_visualization.py [options] [file_path] || Use -h option for more information.',
        description='Processes Excel file and visualizes binary and ternary compounds via periodic table.'
                    ' Maintained by Brian Hoang & Danila Shiryaev.',
        epilog='This program is currently being developed for the 2024 Oliynyk Research Group.')
    group = parser.add_mutually_exclusive_group()
    parser.add_argument('file_path', type=str,
                        help='This is the path to the Excel file. The Excel file should contain two columns: '
                             '"Formula", and "Entry prototype". The excel sheet is assumed to contain a header on the '
                             'first row. For ternary compounds, the formulas are expected to be organized to have '
                             'consistent subscripts for pseudo-binary visualization.')

    group.add_argument('-b', '--binary', action='store_true',
                       help='for visualizations of only binary data.')
    group.add_argument('-t', '--ternary', action='store_true',
                       help='for visualizations of only ternary data.')

    args = parser.parse_args()
    file_path = args.file_path
    user_input_sheet_numbers = input_handler(file_path)
    coord_df, coord_sheet_name = excel_to_dataframe()
    element_dict = create_element_dict(coord_df)
    periodic_table_ax = periodic_table(coord_df, coord_sheet_name)

    

    # Generate the compound data based on user's selection
    if args.binary:
        compounds = make_binary_data(file_path, user_input_sheet_numbers)
        target_element = pick_what_separate()
        if target_element:
            for compound in compounds:
                compound.separate_by_element(target_element)
            # Sort compounds to move modified structures with "(with {element})" to the end
            compounds.sort(key=lambda x: f"(with {target_element})" in x.structure)
        display_binary_data_type(periodic_table_ax, compounds, element_dict, coord_sheet_name)
        # Prompt the user to separate compounds by element
        

    elif args.ternary:
        compounds = make_ternary_data(file_path, user_input_sheet_numbers)
        display_ternary_data_type(periodic_table_ax, compounds, element_dict, coord_sheet_name)

    else:
        compounds, fixed_number = make_psuedobinary_data(file_path, user_input_sheet_numbers)
        display_pseudobinary_data_type(periodic_table_ax, compounds, fixed_number, element_dict, coord_sheet_name)

    return 0

if __name__ == '__main__':
    main()