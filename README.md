# Structure Type Explorer (STEx)

A powerful Python-based tool for visualizing binary compounds on periodic tables and recommending elements for novel compound discovery.

## **How it works?**

<img src="https://github.com/user-attachments/assets/ea766332-292a-4ab6-bad6-49bc1aa0fd57" alt="plot_PCA" width="600"/>

1. **Run the program**
```
python main.py
```
2. **Select the file:**
* The program will prompt you to choose an Excel file from the same directory as the main.py file. You’ll see a list of available files, and you can select the desired file by entering its corresponding number.
3. **Select table type**
  Select from one of the four predefined periodic table layouts:
	1.	Classical Periodic Table
	2.	Long Periodic Table (f-block elements are not separated)
	3.	Separated Periodic Table (p-block, d-block, and f-block elements are visually separated)
	4.	PCA Table (customizable layout based on PCA values).
4. **Select whether you want to fix a specific element from other compounds**
The program offers the option to focus on compounds containing a specific element. This feature separates compounds with the chosen element and prepares data for compound recommendations.
6. **Processing and visualization:**
* The program processes the data, calculates the compound positions based on stoichiometric ratios, and generates plots according to the selected table format.
6. **Output**
* Visualizations are saved as high-resolution image files in the plots directory. Each file is uniquely named to prevent overwriting previous plots.

## **Prerequisites**
  ```
  pip install pandas matplotlib numpy openpyxl click
  ```

## **Features**
Visualizes binary and ternary compounds based on their formulas
* Supports different periodic table formats:
1. Classical periodic table
2. Long periodic table (f-block elements are not separated from the rest)
3. Separated periodic table (p-block, d-block, and f-block elements are visually separated)
4. PCA table

<img src="https://github.com/user-attachments/assets/f13044ad-3027-428c-93bb-81f95685ee9b" alt="plot_PCA" width="1200"/>



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


## **Prerequisites**
This tool requires the following Python libraries:

* pandas
* click
* matplotlib
* numpy
* openpyxl (to handle Excel files)

  ```
  pip install pandas matplotlib numpy openpyxl click
  ```


