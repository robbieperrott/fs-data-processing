'''
Some functions to calculate the impact of an ingredient,
with error handling.
'''
import string
from classes import FoodClass, Ingredient


class ImpactNotFoundError(Exception):
    '''
    Throw if an impact score cannot be found for an ingredient
    I.e. if we traverse up the n-ary tree and reach a root node (a node with no parent_id)
    that does not have an impact_per_kg score.
    '''

class FoodClassNotFoundError(Exception):
    '''
    Throw if a food class cannot be found for an ingredient
    I.e. no food class name matched the ingredient's name
    '''


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
    food_class = next((fc for fc in food_classes if names_match(ingredient.name, fc.name)), None)
    if food_class is None:
        raise FoodClassNotFoundError

    # Traverse up the n-ary tree until a node with an impact_per_kg score is found
    while food_class.impact_per_kg is None and food_class.parent_id:
        food_class = next(fc for fc in food_classes if fc.food_class_id == food_class.parent_id)

    if food_class.impact_per_kg is None:
        # We have reached a root node with no impact_per_kg score, so throw error.
        raise ImpactNotFoundError

    impact = food_class.impact_per_kg * ingredient.weight_per_kg

    return impact
