import os
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# List available Excel files in the current directory
excel_files = [f for f in os.listdir() if f.endswith('.xlsx')]
print("Available Excel files for PCA analysis:")
for i, file in enumerate(excel_files, start=1):
    print(f"{i}. {file}")

# Ask user to pick the file
file_choice = int(input("\nEnter the number corresponding to the Excel file you want to use: ").strip())
file_path = excel_files[file_choice]

# Load the chosen Excel file
data = pd.read_excel(file_path)

# Automatically drop columns with NaN values
data = data.dropna(axis=1)

# Select only numeric columns for PCA
numeric_data = data.select_dtypes(include=['float64', 'int64']).copy()
numeric_data.dropna(inplace=True)

# Ensure 'Symbol' column matches the filtered numeric data index
symbol_data = data.loc[numeric_data.index, 'Symbol'] if 'Symbol' in data.columns else None

print("\nColumns used for PCA analysis:")
print(numeric_data.columns.tolist())

# Standardize the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(numeric_data)

# Perform PCA to reduce to two dimensions
pca = PCA(n_components=2)
principal_components = pca.fit_transform(scaled_data)

# Create a DataFrame for PCA results
pca_df = pd.DataFrame(data=principal_components, columns=['x', 'y'])
if symbol_data is not None:
    pca_df['Symbol'] = symbol_data.reset_index(drop=True)  # Reset index to align correctly

pca_df['Include'] = 1  # Add the "Include" column and fill it with "1"

pca_df = pca_df[['Symbol', 'x', 'y', 'Include']] if 'Symbol' in pca_df.columns else pca_df[['x', 'y', 'Include']]

# Save the PCA coordinates to an Excel file
output_file = "elements_pca_coordinates.xlsx"
pca_df.to_excel(output_file, index=False)
print(f"PCA coordinates saved to {output_file}")

# Create a DataFrame for the contribution of each property to the PCA components in the desired format
pca_contribution = pd.DataFrame(pca.components_, columns=numeric_data.columns, index=['PC1', 'PC2']).T
pca_contribution.reset_index(inplace=True)
pca_contribution.columns = ['Property', 'PC1', 'PC2']

# Save the PCA contributions to an Excel file
contribution_file = "pca_properties_contributions.xlsx"
pca_contribution.to_excel(contribution_file, index=False)
print(f"PCA contributions saved to {contribution_file}")