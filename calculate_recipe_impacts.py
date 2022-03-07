'''
Foodsteps take home test
Data processing task
Robbie Perrott March 2022
Calculate the impacts of various recipes
'''

import sys
from typing import SupportsRound
from csv_utils import get_valid_food_classes, get_valid_recipes
from errors import FoodClassMatchNotFound, ImpactNotFound, InvalidFoodClassTree, InvalidRecipes
from ingredient_impact import find_ingredient_impact
from print_feedback import (print_invalid_food_class_tree, print_invalid_recipes,
    print_recipe_error, print_recipe_success)

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

    # Fetch and validate CSV data. Exit if data is invalid.
    try:
        if sys.argv[1:] and sys.argv[1] == 'test':
            food_classes = get_valid_food_classes(TEST_FOOD_CLASSES_FILE_PATH)
            recipes = get_valid_recipes(TEST_RECIPES_FILE_PATH)
        else:
            food_classes = get_valid_food_classes(FOOD_CLASSES_FILE_PATH)
            recipes = get_valid_recipes(RECIPES_FILE_PATH)
    except InvalidFoodClassTree as exception:
        print_invalid_food_class_tree(exception.args[0])
        sys.exit()
    except InvalidRecipes as exception:
        print_invalid_recipes(exception.args[0])
        sys.exit()

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
