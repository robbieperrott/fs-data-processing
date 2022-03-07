'''
Class definitions
'''


class FoodClass:
    '''A food class corresponds to a row in the food_classes.csv file'''
    def __init__(self,
            food_class_id: int,
            name: str,
            impact_per_kg: float | None,
            parent_id: int | None
        ) -> None:
        self.food_class_id = food_class_id
        self.name = name
        self.impact_per_kg = impact_per_kg
        self.parent_id = parent_id

    def __str__(self) -> str:
        return \
            f'Food class: {self.food_class_id}, {self.name}, {self.impact_per_kg}, {self.parent_id}'

class RecipeEntry:
    '''A recipe entry corresponds to a row in the recipes.csv file'''
    def __init__(
            self,
            recipe_id: int,
            recipe_name: str,
            ingredient_name: str,
            ingredient_weight_per_kg: float
        ) -> None:
        self.recipe_id = recipe_id
        self.recipe_name = recipe_name
        self.ingredient_name = ingredient_name
        self.ingredient_weight_per_kg = ingredient_weight_per_kg

    def __str__(self) -> str:
        return f'Recipe entry: {self.recipe_id}, {self.recipe_name}, ' + \
            f'{self.ingredient_name}, {self.ingredient_weight_per_kg}'

class Ingredient:
    '''An ingredient that is part of a recipe'''
    def __init__(self, name: str, weight_per_kg: float) -> None:
        self.name = name
        self.weight_per_kg = weight_per_kg

    def __str__(self) -> str:
        return f'Ingredient: {self.name}, {self.weight_per_kg}'

class Recipe:
    '''A recipe containing ingredients'''
    def __init__(self, recipe_id: int, name: str, ingredients: list[Ingredient]) -> None:
        self.recipe_id = recipe_id
        self.name = name
        self.ingredients = ingredients

    def __str__(self) -> str:
        return f'Recipe: {self.recipe_id}, {self.name}, ' + \
            f'{[ingredient.name for ingredient in self.ingredients]}'
