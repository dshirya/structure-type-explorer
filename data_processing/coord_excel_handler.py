import pandas as pd


def excel_to_dataframe():
    file_name = 'program_data/table_coordinates.xlsx'
    excel_file = pd.ExcelFile(file_name)
    print("Available sheets:")
    for idx, sheet in enumerate(excel_file.sheet_names, 1):
        print(f"{idx}. {sheet}")

    while True:
        try:
            sheet_choice = int(input("Please enter the number of the sheet you want to load: "))
            if 1 <= sheet_choice <= len(excel_file.sheet_names):
                coord_sheet_name = excel_file.sheet_names[sheet_choice - 1]
                break
            else:
                print("Invalid choice. Please enter a number between 1 and", len(excel_file.sheet_names))
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    df = pd.read_excel(file_name, sheet_name=coord_sheet_name, skiprows=0)

    if df.shape[1] != 4:
        raise ValueError("The Excel sheet must contain exactly 4 columns: Symbol, x, y, and Include.")

    if not pd.api.types.is_numeric_dtype(df.iloc[:, 1]) or not pd.api.types.is_numeric_dtype(df.iloc[:, 2]):
        raise ValueError("The second and third columns must be numeric (x and y coordinates).")
    if not pd.api.types.is_string_dtype(df.iloc[:, 0]):
        raise ValueError("The first column must be a string (element symbol).")
    if not pd.api.types.is_numeric_dtype(df.iloc[:, 3]):
        raise ValueError("The fourth column must be numeric (Include).")

    if 'Include' not in df.columns:
        raise KeyError("'Include' column not found in the Excel file. Please check the column name.")

    df_filtered = df[df['Include'] == 1].copy()
    return df_filtered, coord_sheet_name


def create_element_dict(df):
    return {row['Symbol']: (row['x'], row['y']) for _, row in df.iterrows()}
