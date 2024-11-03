import pandas as pd
import sys


def input_handler(file_path):
    excel_file = pd.ExcelFile(file_path)
    sheet_names = excel_file.sheet_names
    print(f'Sheets currently in {file_path}: ')
    for index, sheet in enumerate(sheet_names, start=1):
        print(f'{index}. {sheet}')

    user_response = input('\nEnter the numbers of the sheets you want to visualize, separated by commas (e.g. "1,2,'
                          '3") or type "exit" to quit: ').strip()

    if user_response.lower() == 'exit':
        print('\nExiting Program...')
        sys.exit()
    else:
        user_input_sheet_numbers = [int(s.strip()) - 1 for s in user_response.split(',')]
    return user_input_sheet_numbers
