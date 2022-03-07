'''
Some functions to calculate the impact of an ingredient,
with error handling.
'''
import string
from classes import FoodClass, Ingredient
from errors import ImpactNotFound, FoodClassMatchNotFound, LoopInFoodClassTree, ParentNotFound


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
        raise FoodClassMatchNotFound('Could not find a food class with a matching name')

    # Traverse up the n-ary tree until a node with an impact score is found,
    # or until a root node is reached.
    food_class_children_ids: list[int] = []
    while food_class.impact_per_kg is None and food_class.parent_id:

        # Check that the parent_id of this food_class does not cause a loop in the tree
        if food_class.parent_id in food_class_children_ids + [food_class.food_class_id]:
            loop_path_list = food_class_children_ids + \
                [food_class.food_class_id, food_class.parent_id]
            loop_path_string = ' -> '.join([str(fc_id) for fc_id in loop_path_list])
            raise LoopInFoodClassTree(f'There is a loop in the food class tree: {loop_path_string}')

        # Find the parent food class if it exists
        parent_food_class = \
            next((fc for fc in food_classes if fc.food_class_id == food_class.parent_id), None)

        # If the parent food class could not be found, throw an error
        if parent_food_class is None:
            raise ParentNotFound(
                f'Could not find parent food class (ID {food_class.parent_id}) ' + \
                f'for food class {food_class.name}'
            )

        # Traverse up the tree
        food_class_children_ids.append(food_class.food_class_id)
        food_class = parent_food_class

    # If there is still no impact score at the root node, throw an error
    if food_class.impact_per_kg is None:
        raise ImpactNotFound(
          f'A root node (ID {food_class.food_class_id}) with no impact score was reached'
        )

    # Calculate impact
    impact = food_class.impact_per_kg * ingredient.weight_per_kg

    return impact
