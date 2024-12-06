import re
import click

class Compound:
    def __init__(self, formula, structure):
        self.formula = formula
        self.elements = self.parse_formula(formula)
        self.structure = structure

    def parse_formula(self, formula):
        pattern = r'([A-Z][a-z]*)(\d*\.?\d*)'
        matches = re.findall(pattern, formula)
        elements = {}
        for element, count in matches:
            elements[element] = float(count) if count else 1
        return elements

    def separate_by_element(self, target_elements):
        """
        Separates formulas based on the presence of specific elements and modifies the structure name.
        For binary compounds, it checks one element.
        For ternary compounds, it checks multiple elements.
        """
        if isinstance(target_elements, (list, set)) and len(target_elements) == 2:
            element1, element2 = target_elements
            if element1 in self.elements and element2 in self.elements:
                self.structure += f" (with {element1} and {element2})"
        elif isinstance(target_elements, str):
            if target_elements in self.elements:
                self.structure += f" (with {target_elements})"

def pick_what_separate(compounds):
    """
    Asks the user to pick elements for separating formulas.
    - For binary compounds (len(elements) == 2), prompts for one element.
    - For ternary compounds (len(elements) == 3), prompts for two elements.
    """
    if not compounds:
        click.echo("No compounds found in the dataset.")
        return None

    compound_type = "binary" if len(compounds[0].elements) == 2 else "ternary"

    if compound_type == "binary":
        if click.confirm("Do you want to fix a certain element for binary compounds?", default=True):
            target_element = click.prompt("Which element?", type=str).strip()
            return target_element
        else:
            return None

    elif compound_type == "ternary":
        if click.confirm("Do you want to fix certain elements for ternary compounds?", default=True):
            element1 = click.prompt("Enter the first element", type=str).strip()
            element2 = click.prompt("Enter the second element", type=str).strip()
            return [element1, element2]  # Return as a list
        else:
            return None