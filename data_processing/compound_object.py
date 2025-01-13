import re
import click

class Compound:
    def __init__(self, formula, structure):
        self.formula = formula
        self.elements = self.parse_formula(formula)
        self.structure = structure
        self.separated_elements = None  # To track elements used for separation

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
        Updates the separated_elements attribute to track used elements.
        """
        if isinstance(target_elements, (list, set)) and len(target_elements) > 0:
            target_set = set(target_elements)
            compound_set = set(self.elements.keys())

            if len(target_set) > 1 and target_set.issubset(compound_set):
                self.structure += f" (with {' and '.join(target_elements)})"
                self.separated_elements = list(target_set)

            elif len(target_set) == 1:
                single_target = next(iter(target_set))
                if single_target in compound_set:
                    self.structure += f" (with {single_target})"
                    self.separated_elements = [single_target]

        elif isinstance(target_elements, str) and target_elements in self.elements:
            self.structure += f" (with {target_elements})"
            self.separated_elements = [target_elements]

def pick_what_separate(compounds):
    """
    Prompts the user to select elements for separating formulas:
    Handles both binary and ternary compounds in the same flow.
    """
    if not compounds:
        click.echo("No compounds found in the dataset.")
        return None

  
    all_elements = {element for compound in compounds for element in compound.elements}

    click.echo("You can specify elements to separate for both binary and ternary compounds.")

    fixed_elements = {}

  
    if click.confirm("Do you want to fix an element for binary compounds?", default=True):
        target_binary = click.prompt("Enter the element to separate for binary compounds", type=str).strip()
        if target_binary not in all_elements:
            click.echo(f"Error: The element '{target_binary}' is not found in the dataset.")
        else:
            fixed_elements['binary'] = target_binary

    if click.confirm("Do you want to fix elements for ternary compounds?", default=True):
        target_ternary = click.prompt("Enter one or more elements separated by spaces for ternary compounds", type=str)
        target_ternary = [e.strip() for e in target_ternary.split() if e.strip()]
        invalid_elements = [e for e in target_ternary if e not in all_elements]
        if invalid_elements:
            click.echo(f"Error: The following elements are not found in the dataset: {', '.join(invalid_elements)}")
        else:
            fixed_elements['ternary'] = target_ternary

    return fixed_elements

