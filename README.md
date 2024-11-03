# System exploration tool


## **Overview**
This repository contains a Python-based tool for visualizing binary and ternary compounds based on their chemical formulas. The tool uses Excel data to plot compounds on various periodic table formats and calculates the average coordinates of each compound based on its molar ratios.

## **Features**
Visualizes binary and ternary compounds based on their formulas
* Supports different periodic table formats:
1. Classical periodic table
<img src="https://github.com/user-attachments/assets/a20bea8e-77ce-4259-8541-96e8979170e6" alt="table_short" width="400"/>

2. Long periodic table (f-block elements are not separated from the rest)
<img src="https://github.com/user-attachments/assets/55d93e36-e531-4a54-a8e0-68cbeda8b01d" alt="table_long" width="400"/>

3. Separated periodic table (p-block, d-block, and f-block elements are visually separated)
<img src="https://github.com/user-attachments/assets/cadba324-a60e-4356-93c1-815c51705c38" alt="table_separated" width="400"/>

4. PCA table
<img src="https://github.com/user-attachments/assets/49d1e9b1-eab8-46f3-9d03-442d918428e5" alt="plot_PCA" width="400"/>

* Dynamic loading of Excel sheets with user-selected data visualization
* Customizable plot shapes (rectangles or circles) depending on the data sheet name

## **How it works**

### Input Data

The input file is an Excel file (.xlsx) containing:

1. Formula: The chemical formula of the compound (e.g., Fe2O3).
2. Entry Prototype: A classification or structural label for the compound.

### Calculations and Output

* The program calculates the molar ratio of elements in the formula.
* The average coordinate of the compound on the selected periodic table format is determined based on the elements’ positions and their stoichiometric ratios.
* Users can specify binary or ternary data for visualization.


## **Prerequisites**
This tool requires the following Python libraries:

* pandas
* argparse
* matplotlib
* numpy
* openpyxl (to handle Excel files)

  `pip install pandas matplotlib numpy openpyxl`


