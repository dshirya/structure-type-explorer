import pandas as pd
from data_processing.compound_object import Compound
import sys
import click

def make_compound_data(excel_file, user_input_sheet_numbers):
    """
    Reads the Excel file and categorizes compounds into binary or ternary lists
    based on the number of elements in the formula.
    """
    compounds_binary = []
    compounds_ternary = []
    excel_file = pd.ExcelFile(excel_file)
    sheet_names = excel_file.sheet_names

    for sheet_number in user_input_sheet_numbers:
        df = pd.read_excel(excel_file, sheet_name=sheet_names[sheet_number])
        # Standardize column names
        df.columns = [col.lower() for col in df.columns]

        if 'formula' in df.columns and 'entry prototype' in df.columns:
            df = df.drop_duplicates(subset=['formula', 'entry prototype'])
            for _, row in df.iterrows():
                formula = row['formula']
                structure = row['entry prototype']
                structure = structure.split(',')[0].strip()
                compound = Compound(formula, structure)

                # Categorize the compound based on the number of elements
                if len(compound.elements) == 2:
                    compounds_binary.append(compound)
                elif len(compound.elements) == 3:
                    compounds_ternary.append(compound)
                else:
                    click.echo(f"Unsupported number of elements in formula: {compound.formula}")
                    sys.exit()
        else:
            click.echo("Required columns 'Formula'/'formula' and 'Entry prototype'/'entry prototype' are not found.")
            sys.exit()

    return compounds_binary, compounds_ternary