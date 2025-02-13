import pandas as pd
import ipywidgets as widgets
from IPython.display import display

def select_sheets(file_path):
    """
    Function to interactively select sheets from an Excel file using ipywidgets.
    Returns a list of selected sheet names.
    """
    # Load the sheet names
    xls = pd.ExcelFile(file_path)
    sheet_names = xls.sheet_names
    
    # Create a selection widget
    sheet_selector = widgets.SelectMultiple(
        options=sheet_names,
        description='Sheets:',
        disabled=False
    )
    
    # Display widget
    display(sheet_selector)
    
    # Button to confirm selection
    output = widgets.Output()
    def on_confirm(change):
        with output:
            output.clear_output()
            selected_sheets = list(sheet_selector.value)
            print(f"Selected sheet names: {selected_sheets}")
    
    confirm_button = widgets.Button(description="Confirm Selection")
    confirm_button.on_click(on_confirm)
    display(confirm_button, output)
    
    return sheet_selector
