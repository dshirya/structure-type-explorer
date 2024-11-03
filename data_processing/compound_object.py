import re

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

def ask_to_separate(message, default=True):
    """Custom confirmation function with a default Y/n response."""
    default_str = "Y/n" if default else "y/N"
    response = input(f"{message} ({default_str}): ").strip().lower()
    if not response:  # If Enter is pressed with no input
        return default
    return response == 'y'

def pick_what_separate():
    """Asks the user if they want to separate formulas by a specific element and proceeds if yes."""
    if ask_to_separate("Do you want to separate formulas with a certain element?"):
        # Ask which element to filter by
        target_element = input("Which element? ").strip()
        return target_element
    else:
        print("Skipping separation by element.")
        return None