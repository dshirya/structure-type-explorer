# Structure Type Explorer (STEx)
<div align="center">
<img src="https://github.com/user-attachments/assets/bf2091d0-17a4-46c2-aa00-1ef6519e2d2f" alt="plot_PCA" >
</div>

## Purpose
STEx is a powerful tool for visualizing compounds on periodic tables and recommending elements for novel compound discovery. 

## **Getting started**
1. **Download all required libraries:**

Install packages listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

Or you may install all packages at once:

```bash
pip install pandas matplotlib numpy openpyxl click
```

2. **Run the program**
```
python main.py
```
3. **Select the file**  
The program will prompt you to choose an Excel file from the same directory as the `main.py` file. A list of available files will be displayed, and you can select the desired file by entering its corresponding number. The input file must be an `.xlsx` file with two columns:
	* **Formula**: The chemical formula of the compound (e.g., Fe2O3)
	* **Entry Prototype**: A classification or structural label for the compound

The input file must be preprocessed to include only compounds containing elements present in the periodic table. You can use the [stex-data-preprocessor](https://github.com/dshirya/stex-data-preprocessor) to prepare the data


4. **Select table type**  
  Users can select from one of four predefined periodic table layouts:  
	1.	**Classical Periodic Table**  
	2.	**Long Periodic Table** (f-block elements are not separated)  
	3.	**Separated Periodic Table** (p-block, d-block, and f-block elements are visually separated)  
	4.	**PCA Table** (customizable layout based on PCA values)
<div align="center">
  <img src="https://github.com/user-attachments/assets/0638f8bd-0bda-4240-b672-69cdfd4d5b7c" alt="plot_PCA" width="800"/>
	</div>
 
5. **Optional: Fix a Specific Element**  
Users can choose to focus on compounds containing a specific element. The program separates compounds that include the selected element, preparing data for compound recommendations
6. **Processing and visualization:**  
The program processes the data, calculates the atomic ratios of elements in the formulas, and maps compounds onto the selected periodic table format.
	* Geometric markers represent element locations

	* Connections between elements in a formula are shown as lines

	* Colors and markers can be customized in `data_processing/appearance.py`
7. **Output**  
Visualizations are saved as high-resolution image files in the `plots` directory. Each file is uniquely named to prevent overwriting previous plots.


## **Features**


### Customizable Plots  

* Modify the `program_data/element_coordinates.xlsx` file to update or create entirely new table layouts
* Table styles adjust dynamically based on the sheet name:  
  * Rectangle markers for the sheets with `*_table`
  * Circle markers for the sheets with  `*_plot`
* You can make new PCA plot based on your element properties, by using `PCA_plotting/PCA.py` code
  1. Put the file with you element properties in the `PCA_plotting` folder (elements should be in the first column)
  2. Run the `PCA.py`
     * PCA plot will be produced based on the element properties with skipping N/A and not-numerical values
* Edit ***data_processing/appearance.py*** to customize plot, markers and colors

### Recommendation Engine

* Suggests elements for novel compound formation based on structural similarities.

* Uses PCA plots to determine meaningful x and y axes.

* Scores potential new elements based on their proximity to known compounds.

 **How Recommendations Work**  
1. The user specifies a “fixed” element (e.g., Ir)
2. The program identifies all unique binary compounds containing the fixed element (e.g., TbIr, GaIr)

3. It locates the nearest neighbors of these related elements (Tb, Ga), excluding those that already contain the fixed element

4. A score is assigned to each recommended element based on distance:

	* Shorter distances receive higher scores

	* Scores are calculated as `100% * (min_distance / element_distance)`

5. Results are saved in an output spreadsheet for further analysis




