import re

class Compound:
    def __init__(self, formula, structure):
        self.formula = formula
        self.elements = self.parse_formula(formula)
        self.structure = structure
        self.structure_elements = self.parse_formula(structure)  # Parse structure elements
        self.separated_elements = None  # 

    def parse_formula(self, formula):
        pattern = r'([A-Z][a-z]*)(\d*\.?\d*)'
        matches = re.findall(pattern, formula)
        elements = {}
        for element, count in matches:
            elements[element] = float(count) if count else 1
        return elements

    def compare_elements_with_structure(self):
        """
        Compares the number of unique elements in the compound formula
        with the number of unique elements in the structure.
        Returns True if the formula has more elements than the structure.
        """
        compound_elements_set = set(self.elements.keys())
        structure_elements_set = set(self.structure_elements.keys())
        return compound_elements_set > structure_elements_set  # True if co

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

def pick_what_separate(compounds, binary_element=None, ternary_elements=None):
    """
    Selects elements for separating formulas based on predefined parameters.
    :param compounds: List of Compound objects.
    :param binary_element: String specifying the element for binary compounds.
    :param ternary_elements: List of strings specifying elements for ternary compounds.
    :return: Dictionary with fixed elements for binary and ternary compounds.
    """
    if not compounds:
        raise ValueError("No compounds found in the dataset.")

    all_elements = {element for compound in compounds for element in compound.elements}
    fixed_elements = {}

    has_binary = any(len(compound.elements) == 2 for compound in compounds)
    has_ternary = any(len(compound.elements) == 3 for compound in compounds)

    # Handling binary compounds
    if has_binary and binary_element:
        if binary_element not in all_elements:
            raise ValueError(f"Error: The element '{binary_element}' is not found in the dataset.")
        fixed_elements['binary'] = binary_element
        [compound.separate_by_element(fixed_elements.get('binary')) for compound in compounds if len(compound.elements) == 2]
        compounds.sort(key=lambda x: x.structure)
    
    # Handling ternary compounds
    if has_ternary and ternary_elements:
        if isinstance(ternary_elements, str):
            ternary_elements = [ternary_elements]  # Convert single element to list
        invalid_elements = [e for e in ternary_elements if e not in all_elements]
        if invalid_elements:
            raise ValueError(f"Error: The following elements are not found in the dataset: {', '.join(invalid_elements)}")
        fixed_elements['ternary'] = ternary_elements
        [compound.separate_by_element(fixed_elements.get('ternary')) for compound in compounds if len(compound.elements) == 3]
        compounds.sort(key=lambda x: x.structure)
    

    return fixed_elements

