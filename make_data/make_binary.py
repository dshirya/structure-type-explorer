import pandas as pd
from data_processing.compound_object import Compound
import sys


def make_binary_data(excel_file, user_input_sheet_numbers):
    compounds = []
    excel_file = pd.ExcelFile(excel_file)
    sheet_names = excel_file.sheet_names
    for sheet_number in user_input_sheet_numbers:
        df = pd.read_excel(excel_file, sheet_name=sheet_names[sheet_number])
        df = df.drop_duplicates(subset=['Formula', 'Entry prototype'])
        for _, row in df.iterrows():
            formula = row['Formula']
            structure = row['Entry prototype']
            structure = structure.split(',')[0].strip()
            compound = Compound(formula, structure)
            if len(compound.elements) != 2:
                print(f'Non-binary data detected ({compound.formula}).')
                sys.exit()
            else:
                compounds.append(compound)
    return compounds
