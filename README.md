# Binary system exploration tool

## **How it works?**
1. **Run the program**
```
python main.py
```

2. **Select the file:**
* The program will prompt you to choose an Excel file from the same directory as the main.py file. You’ll see a list of available files, and you can select the desired file by entering its corresponding number.
3. **Select table type**
4. **Select whether you want to separate compounds with a specific element from other compounds**
5. **Data processing and visualization:**
* The program processes the selected Excel file, extracts relevant data, and generates a visualization based on binary compound information.
6. **Output**
* Each generated visualization file is saved in the plots directory with a unique name to prevent overwriting previous images.

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


