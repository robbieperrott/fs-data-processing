'''
Check that data is valid
'''

from classes import FoodClass
from errors import InvalidFoodClassTree


def validate_food_class_tree(food_classes: list[FoodClass]) -> None:
    '''
    Ensure that there are no loops in the food class tree,
    and that all parent IDs point to an existing food class.
    '''
    errors: list[str] = []
    food_class_ids_in_loops: set[int] = set()

    for food_class in food_classes:
        # If this food class has already been identified as part of a loop, skip it.
        if food_class.food_class_id in food_class_ids_in_loops:
            continue

        food_class_children_ids: list[int] = []

        while food_class.parent_id:
            # If there is a loop create an error message and go to the next food class
            if food_class.parent_id in food_class_children_ids + [food_class.food_class_id]:
                loop_path_list = food_class_children_ids + \
                    [food_class.food_class_id, food_class.parent_id]
                loop_path_string = ' -> '.join([str(fc_id) for fc_id in loop_path_list])
                errors.append(f'There is a loop in the food class tree: {loop_path_string}')
                food_class_ids_in_loops = food_class_ids_in_loops.union(set(loop_path_list))
                break

            # Find the parent food class if it exists
            parent_food_class = \
                next((fc for fc in food_classes if fc.food_class_id == food_class.parent_id), None)

            # If the parent food class could not be found,
            # create an error message and go to the next food class
            if parent_food_class is None:
                errors.append(
                    f'Could not find parent food class (ID = {food_class.parent_id}) ' + \
                    f'for food class {food_class.name}'
                )
                break

            # Traverse up the tree
            food_class_children_ids.append(food_class.food_class_id)
            food_class = parent_food_class

    if errors:
        raise InvalidFoodClassTree(errors)
