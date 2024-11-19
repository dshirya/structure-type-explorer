import pandas as pd
from data_processing.compound_object import Compound
import sys


def make_binary_data(excel_file, user_input_sheet_numbers):
    compounds = []
    excel_file = pd.ExcelFile(excel_file)
    sheet_names = excel_file.sheet_names
    
    for sheet_number in user_input_sheet_numbers:
        df = pd.read_excel(excel_file, sheet_name=sheet_names[sheet_number])
        # Standardize column names to lowercase for easier access
        df.columns = [col.lower() for col in df.columns]
        
        # Check if the required columns exist in the DataFrame
        if 'formula' in df.columns and 'entry prototype' in df.columns:
            df = df.drop_duplicates(subset=['formula', 'entry prototype'])
            for _, row in df.iterrows():
                formula = row['formula']
                structure = row['entry prototype']
                structure = structure.split(',')[0].strip()
                compound = Compound(formula, structure)
                
                if len(compound.elements) != 2:
                    print(f'Non-binary data detected ({compound.formula}).')
                    sys.exit()
                else:
                    compounds.append(compound)
        else:
            print("Required columns 'Formula'/'formula' and 'Entry prototype'/'entry prototype' are not found.")
            sys.exit()
            
    return compounds
