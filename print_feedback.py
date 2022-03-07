'''
Functions used to print results to console
'''

from typing import SupportsRound


def print_recipe_success(recipe_name: str, impact: SupportsRound[float]) -> None:
    '''Print successful recipe calculation to console'''
    print(f'\033[92m\033[1m{recipe_name}\033[0m')
    print(f'Impact: {round(impact, 8)}')
    print()

def print_recipe_error(recipe_name: str, recipe_errors: list[str]) -> None:
    '''Print erroneous recipe calculation to console with ingredient errors'''
    print(f'\033[91m\033[1m{recipe_name}\033[0m')
    print('Could not calculate impacts for the following ingredients')
    for error in recipe_errors:
        print(f'    {error}')
    print()

def print_food_class_tree_error(error_messages: list[str]) -> None:
    '''Print food class tree error message to console'''
    print('\033[91m\033[1mInvalid food class tree\033[0m')
    for error in error_messages:
        print(f'    {error}')
    print()
