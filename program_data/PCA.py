import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


file_path = "program_data/elemental-property-list.xlsx"  # Replace with the actual path to your Excel file
data = pd.read_excel(file_path)

print("Available columns in the data:")
for i, col in enumerate(data.columns):
    print(f"{i}: {col}")

# Ask the user which columns to skip by number
skip_columns_input = input("Enter the column numbers you want to skip (comma-separated), or press Enter to skip none: ")
if skip_columns_input:
    skip_indices = [int(index.strip()) for index in skip_columns_input.split(',')]
    skip_columns = [data.columns[i] for i in skip_indices]
else:
    skip_columns = None

# Row indices for specific groups
noble_gases = [1, 9, 17, 35, 42, 53]
halogens = [8, 16, 34, 52]
group_16_and_hydrogen = [0, 7, 33]
all_groups = noble_gases + halogens + group_16_and_hydrogen

print("\nOptions for skipping rows:")
print("1. Skip noble gases")
print("2. Skip halogens")
print("3. Skip group 16 and hydrogen")
print("4. Skip all the above")

skip_group_option = input("Enter the number of the option you want to use (or press Enter to skip none): ").strip()

if skip_group_option == '1':
    data = data.drop(index=noble_gases, errors='ignore').reset_index(drop=True)
elif skip_group_option == '2':
    data = data.drop(index=halogens, errors='ignore').reset_index(drop=True)
elif skip_group_option == '3':
    data = data.drop(index=group_16_and_hydrogen, errors='ignore').reset_index(drop=True)
elif skip_group_option == '4':
    data = data.drop(index=all_groups, errors='ignore').reset_index(drop=True)

# Ask the user which rows to skip by index
print("\nList of elements:")
print(data)
skip_rows_input = input("\nEnter the row indices you want to skip (comma-separated), or press Enter to skip none: ")
if skip_rows_input:
    skip_rows = [int(index.strip()) for index in skip_rows_input.split(',')]
    data = data.drop(index=skip_rows).reset_index(drop=True)
else:
    skip_rows = None

# Ask if the user wants to skip columns with NaN values
auto_skip_nan_input = input("Do you want to automatically skip columns with NaN values? (yes/no): ").strip().lower()
auto_skip_nan = auto_skip_nan_input == 'yes'


if auto_skip_nan:
    data = data.dropna(axis=1)
if skip_columns:
    data = data.drop(columns=skip_columns, errors='ignore')


numeric_data = data.select_dtypes(include=['float64', 'int64']).copy()
numeric_data.dropna(inplace=True)

# Ensure 'Symbol' column matches the filtered numeric data index
symbol_data = data.loc[numeric_data.index, 'Symbol'] if 'Symbol' in data.columns else None

print("\nColumns used for PCA analysis:")
print(numeric_data.columns.tolist())

scaler = StandardScaler()
scaled_data = scaler.fit_transform(numeric_data)

# Perform PCA to reduce to two dimensions
pca = PCA(n_components=2)
principal_components = pca.fit_transform(scaled_data)


pca_df = pd.DataFrame(data=principal_components, columns=['x', 'y'])
if symbol_data is not None:
    pca_df['Symbol'] = symbol_data.reset_index(drop=True)  # Reset index to align correctly

pca_df = pca_df[['Symbol', 'x', 'y']] if 'Symbol' in pca_df.columns else pca_df[['x', 'y']]

output_file = "elements_pca_coordinates.xlsx"  # Specify your preferred file name and path
pca_df.to_excel(output_file, index=False)
print(f"PCA coordinates saved to {output_file}")