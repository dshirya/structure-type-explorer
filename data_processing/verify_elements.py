import sys


def verify_elements(molecule, element_dict):
    for element in molecule.elements.keys():
        if element not in element_dict:
            print(f'Please check the following formula in the sheet: {molecule.formula}.'
                  f' It may contain a bad element: {element}.')
            sys.exit()
