'''
Some helper functions to extract data from the CSVs
and to convert this data into FoodClass and RecipeEntry objects
'''
import csv
from classes import FoodClass, RecipeEntry


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

def get_food_classes(food_classes_file_path) -> list[FoodClass]:
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
    return food_classes

def get_recipe_entries(recipes_file_path) -> list[RecipeEntry]:
    '''
    Get data from recipes.csv
    and convert this data into RecipeEntry objects
    '''
    recipes_rows = get_rows_from_csv(recipes_file_path)
    recipe_entries: list[RecipeEntry] = []
    for row in recipes_rows:
        recipe_entry = RecipeEntry(int(row[0]), row[1], row[2], float(row[3]))
        recipe_entries.append(recipe_entry)
    return recipe_entries
