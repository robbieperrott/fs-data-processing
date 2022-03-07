'''
Some helper functions to extract data from the CSVs
and to convert this data into FoodClass and RecipeEntry objects
'''

import csv
from classes import FoodClass, Ingredient, Recipe, RecipeEntry
from validation import validate_food_class_tree, validate_recipes


def get_rows_from_csv(file_path) -> list[list[str]]:
    '''
    Reads a CSV file and returns its rows.
    '''
    file = open(file_path, encoding='UTF-8')
    csv_reader = csv.reader(file)
    next(csv_reader)
    rows: list[list[str]] = []
    for row in csv_reader:
        rows.append(row)
    return rows

def get_valid_food_classes(food_classes_file_path) -> list[FoodClass]:
    '''
    Get data from food_classes.csv
    and convert this data into FoodClass objects
    '''
    food_class_rows = get_rows_from_csv(food_classes_file_path)
    food_classes: list[FoodClass] = []
    for row in food_class_rows:
        food_class_id = int(row[0])
        food_class_name = row[1]
        impact = float(row[2]) if row[2] else None
        parent_id = int(row[3]) if row[3] else None
        food_class = FoodClass(food_class_id, food_class_name, impact, parent_id)
        food_classes.append(food_class)
    # Validate the food class tree
    validate_food_class_tree(food_classes)
    return food_classes

def get_valid_recipes(recipes_file_path) -> list[Recipe]:
    '''
    Get data from recipes.csv
    and convert this data into Recipe objects
    '''
    # Get RecipeEntry objects from CSV
    recipes_rows = get_rows_from_csv(recipes_file_path)
    recipe_entries: list[RecipeEntry] = []
    for row in recipes_rows:
        recipe_entry = RecipeEntry(int(row[0]), row[1], row[2], float(row[3]))
        recipe_entries.append(recipe_entry)

    # Convert RecipeEntrys into Recipes
    recipe_ids = list(set([recipe_entry.recipe_id for recipe_entry in recipe_entries]))
    recipes: list[Recipe] = []
    for recipe_id in recipe_ids:
        ingredients = [Ingredient(entry.ingredient_name, entry.ingredient_weight_per_kg) \
            for entry in recipe_entries if entry.recipe_id == recipe_id]
        recipe_name = next(r.recipe_name for r in recipe_entries if r.recipe_id == recipe_id)
        recipe = Recipe(recipe_id, recipe_name, ingredients)
        recipes.append(recipe)

    # Validate the recipes
    validate_recipes(recipes)

    return recipes
