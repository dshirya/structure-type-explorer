# Structure Type Explorer (STEx)

A powerful Python-based tool for visualizing binary compounds on periodic tables and recommending elements for novel compound discovery.

## **How it works?**
<div align="center">
<img src="https://github.com/user-attachments/assets/a057f327-d124-404f-aff3-7e7cbca19b6f" alt="plot_PCA" width="600">
</div>


1. **Run the program**
```
python main.py
```
2. **Select the file**  
The program will prompt you to choose an Excel file from the same directory as the main.py file. You’ll see a list of available files, and you can select the desired file by entering its corresponding number.
3. **Select table type**  
  Select from one of the four predefined periodic table layouts:  
	1.	Classical Periodic Table  
	2.	Long Periodic Table (f-block elements are not separated)  
	3.	Separated Periodic Table (p-block, d-block, and f-block elements are visually separated)  
	4.	PCA Table (customizable layout based on PCA values)
<div align="center">
  <img src="https://github.com/user-attachments/assets/0638f8bd-0bda-4240-b672-69cdfd4d5b7c" alt="plot_PCA" width="800"/>
	</div>
 
5. **Select whether you want to fix a specific element from other compounds**  
The program offers the option to focus on compounds containing a specific element. This feature separates compounds with the chosen element and prepares data for compound recommendations.
6. **Processing and visualization:**  
The program processes the data, calculates the compound positions based on stoichiometric ratios, and generates plots according to the selected table format.
6. **Output**  
Visualizations are saved as high-resolution image files in the plots directory. Each file is uniquely named to prevent overwriting previous plots.


## **Features**

### Visualize Compounds  

STEx supports binary compounds visualization with user-customizable layouts  


### Customizable Plots  

* Modify the program_data/element_coordinates.xlsx file to update or create entirely new table layouts
* Table styles adjust dynamically based on the sheet name:  
  * Rectangle markers for the sheets with **name_table**
  * Circle markers for the sheets with  **name_plot**
* Edit data_processing/appearance.py to customize plot, markers and colors  

### Recommendation Engine

* Suggests elements for creating novel compounds based on structural similarities
* Uses PCA plots to calculate meaningful x and y axes, scoring potential new elements based on proximity to known compounds
### Input Data

The input file must be an Excel file (.xlsx) containing columns:
* Formula: The chemical formula of the compound (e.g., Fe<sub>2</sub>O<sub>3</sub>)  
* Entry Prototype: A classification or structural label for the compound  

Ensure the file is preprocessed (you can use [stex-data-preprocessor](https://github.com/dshirya/stex-data-preprocessor)) for binary structures with elements present in the periodic table.

### Calculations and Output

* The program calculates the atomic ratio of elements in the formula.
* The average coordinate of the compound on the selected periodic table format is determined based on the elements’ positions and their stoichiometric ratios.

## **How Recommendations Work**  
1. The user specifies a “fixed” element (e.g., Ir).
2. The program identifies all unique binary compounds with the fixed element (e.g., TbIr, GaIr).
3. It finds the nearest neighbors of these related elements (Tb, Ga) that do not include the fixed element.
4. Scores are calculated for each recommended element based on distance, with shorter distances receiving higher scores.
5. Results are saved in an output spreadsheet for further analysis.


## **Prerequisites**  
Install the required Python libraries:

  ```
  pip install pandas matplotlib numpy openpyxl click
  ```



