import pandas as pd
import ipywidgets as widgets
from IPython.display import display

def select_sheets(file_path):
    """
    Function to interactively select sheets from an Excel file using ipywidgets.
    Ensures the output prints only once.
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

    output = widgets.Output()
    selected_sheets = []  # Store the selected sheet names

    def on_confirm(change):
        """Handles button click to store and display selected sheets."""
        output.clear_output()
        with output:
            selected_sheets[:] = list(sheet_selector.value)  # Update list in-place

    # Ensure only one event binding happens
    confirm_button = widgets.Button(description="Confirm Selection")
    confirm_button.on_click(on_confirm)

    # Display widgets
    display(sheet_selector, confirm_button, output)
    
    return selected_sheets  # Return the list of selected sheets
