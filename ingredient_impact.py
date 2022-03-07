'''
Functions used to calculate the impact of an ingredient
'''

import string
from classes import FoodClass, Ingredient
from errors import ImpactNotFound, FoodClassMatchNotFound


def names_match(ingredient_name: str, food_class_name: str) -> bool:
    '''
    Check if the name of an ingredient matches the name of a food class.
    '''
    return get_words(ingredient_name) == get_words(food_class_name)

def get_words(input_string: str) -> set[str]:
    '''
    Get a set of the words used in a string,
    ignoring punctuation, upper case, and word order.
    '''
    words_string = input_string.translate(str.maketrans('', '', string.punctuation)).lower()
    words_array = words_string.split()
    words_set = set(words_array)
    return words_set

def find_ingredient_impact(ingredient: Ingredient, food_classes: list[FoodClass]) -> float:
    '''
    Find the impact of an ingredient.
    '''
    # Find the initial matching food class for an ingredient. If none is found, throw an error.
    food_class = next((fc for fc in food_classes if names_match(ingredient.name, fc.name)), None)
    if food_class is None:
        raise FoodClassMatchNotFound('Could not find a food class with a matching name')

    # Traverse up the n-ary tree until a node with an impact score is found,
    # or until a root node is reached.
    while food_class.impact_per_kg is None and food_class.parent_id:
        food_class = next(fc for fc in food_classes if fc.food_class_id == food_class.parent_id)

    # If there is still no impact score at the root node, throw an error
    if food_class.impact_per_kg is None:
        raise ImpactNotFound(
          f'A root node (ID {food_class.food_class_id}) with no impact score was reached'
        )

    # Calculate impact
    impact = food_class.impact_per_kg * ingredient.weight_per_kg

    return impact
