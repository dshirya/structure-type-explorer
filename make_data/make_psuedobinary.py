import pandas as pd
from data_processing.compound_object import Compound


def make_psuedobinary_data(excel_file, user_input_sheet_numbers):
    ternary_detected = False
    fixed_number = None
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
            if ternary_detected is False and len(compound.elements) == 3:
                fixed_number = int(input(f'Ternary compound detected, {formula}. Please input a number corresponding '
                                         'to the fixed element: e.g. 1, 2, or 3: '))
                ternary_detected = True
                compounds.append(compound)
            else:
                compounds.append(compound)
    return compounds, fixed_number
