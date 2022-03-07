'''
Check that data is valid
'''

from classes import FoodClass, Recipe
from errors import InvalidFoodClassTree, InvalidRecipes


def validate_food_class_tree(food_classes: list[FoodClass]) -> None:
    '''
    Ensure that there are no loops in the food class tree,
    and that all parent IDs point to an existing food class.
    '''
    errors: list[str] = []
    food_class_ids_in_loops: set[int] = set()

    for food_class in food_classes:
        # Check non-negative impact per kg
        if food_class.impact_per_kg is not None and food_class.impact_per_kg < 0:
            errors.append(
              f'Negative impact score found for food class {food_class.name} ' + \
              f'(ID = {food_class.food_class_id})'
            )

        # If this food class has already been identified as part of a loop, skip it.
        if food_class.food_class_id in food_class_ids_in_loops:
            continue

        food_class_children_ids: list[int] = []

        while food_class.parent_id is not None:
            # If there is a loop create an error message and go to the next food class
            if food_class.parent_id in food_class_children_ids + [food_class.food_class_id]:
                loop_path_list = food_class_children_ids + \
                    [food_class.food_class_id, food_class.parent_id]
                loop_path_string = ' -> '.join([str(fc_id) for fc_id in loop_path_list])
                errors.append(f'Loop found in food class tree: {loop_path_string}')
                food_class_ids_in_loops = food_class_ids_in_loops.union(set(loop_path_list))
                break

            # Find the parent food class if it exists
            parent_food_class = \
                next((fc for fc in food_classes if fc.food_class_id == food_class.parent_id), None)

            # If the parent food class could not be found,
            # create an error message and go to the next food class
            if parent_food_class is None:
                errors.append(
                    f'Parent (ID = {food_class.parent_id}) not found ' + \
                    f'for food class {food_class.name}'
                )
                break

            # Traverse up the tree
            food_class_children_ids.append(food_class.food_class_id)
            food_class = parent_food_class

    if errors:
        raise InvalidFoodClassTree(errors)

def validate_recipes(recipes: list[Recipe]) -> None:
    '''
    Ensure that there are no negative ingredient weights per kg in any recipes
    '''
    errors: list[str] = []
    for recipe in recipes:
        invalid_ingredient_names: list[str] = []
        for ingredient in recipe.ingredients:
            if ingredient.weight_per_kg < 0:
                invalid_ingredient_names.append(ingredient.name)
        if invalid_ingredient_names:
            errors.append(
                f'\033[1m{recipe.name}\033[0m: Negative weight / kg ' + \
                f'found for the following ingredients: {", ".join(invalid_ingredient_names)}')
    if errors:
        raise InvalidRecipes(errors)
