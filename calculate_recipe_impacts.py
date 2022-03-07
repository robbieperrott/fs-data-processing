'''
Foodsteps take home test
Data processing task
Robbie Perrott March 2022
Calculate the impacts of various recipes
'''

import sys
from typing import SupportsRound
from checks import validate_food_class_tree
from classes import Recipe, Ingredient
from csv_utils import get_food_classes, get_recipe_entries
from errors import FoodClassMatchNotFound, ImpactNotFound, InvalidFoodClassTree
from ingredient_impact import find_ingredient_impact
from print_feedback import print_food_class_tree_error, print_recipe_error, print_recipe_success

FOOD_CLASSES_FILE_PATH = './files/food_classes.csv'
RECIPES_FILE_PATH = './files/recipes.csv'
TEST_FOOD_CLASSES_FILE_PATH = './files/test/food_classes_test.csv'
TEST_RECIPES_FILE_PATH = './files/test/recipes_test.csv'


def main() -> None:
    '''
    Reads data from food_classes.csv and recipes.csv,
    calculates the impact of each recipe (if all ingredient impacts are available),
    and prints the results.
    '''

    # Get data from CSVs
    if sys.argv[1:] and sys.argv[1] == 'test':
        food_classes = get_food_classes(TEST_FOOD_CLASSES_FILE_PATH)
        recipe_entries = get_recipe_entries(TEST_RECIPES_FILE_PATH)
    else:
        food_classes = get_food_classes(FOOD_CLASSES_FILE_PATH)
        recipe_entries = get_recipe_entries(RECIPES_FILE_PATH)

    # Validate the food classes
    try:
        validate_food_class_tree(food_classes)
    except InvalidFoodClassTree as exception:
        print_food_class_tree_error(exception.args[0])
        exit()

    # Create Recipe objects
    recipe_ids = list(set([recipe_entry.recipe_id for recipe_entry in recipe_entries]))
    recipes: list[Recipe] = []
    for recipe_id in recipe_ids:
        ingredients = [Ingredient(entry.ingredient_name, entry.ingredient_weight_per_kg) \
            for entry in recipe_entries if entry.recipe_id == recipe_id]
        recipe_name = next(r.recipe_name for r in recipe_entries if r.recipe_id == recipe_id)
        recipe = Recipe(recipe_id, recipe_name, ingredients)
        recipes.append(recipe)

    # Calculate and print impacts for each recipe (if they can be calculated)
    for recipe in recipes:
        ingredient_impacts: list[float] = []
        recipe_errors: list[str] = []
        for ingredient in recipe.ingredients:
            try:
                ingredient_impact = find_ingredient_impact(ingredient, food_classes)
                ingredient_impacts.append(ingredient_impact)
            except (
                FoodClassMatchNotFound,
                ImpactNotFound
            ) as exception:
                recipe_errors.append(f'\033[1m{ingredient.name}\033[0m: ' + exception.args[0])
        if recipe_errors:
            print_recipe_error(recipe.name, recipe_errors)
        else:
            impact: SupportsRound[float] = sum(i for i in ingredient_impacts if i)
            print_recipe_success(recipe.name, impact)


if __name__ == "__main__":
    main()
