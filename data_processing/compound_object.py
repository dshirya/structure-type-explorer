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

    def separate_by_element(self, target_element):
        """Separates formulas by the presence of a specific element and modifies the structure name."""
        if target_element in self.elements:
            # Modify the structure name if the element is present
            self.structure += f" (with {target_element})"

def pick_what_separate():
    """Asks the user if they want to separate formulas by a specific element and proceeds if yes."""
    if click.confirm("Do you want to separate formulas with a certain element?", default=True):
        # Ask which element to filter by
        target_element = click.prompt("Which element?", type=str).strip()
        return target_element
    else:
        target_element = None
        return target_element