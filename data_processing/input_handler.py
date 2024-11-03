import pandas as pd
import sys
import os
import click

def list_excel_files():
    """
    Lists Excel files in the current directory and prompts the user to select one.
    
    Returns:
        str: The file path of the selected Excel file, or None if no valid file is chosen.
    """
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
