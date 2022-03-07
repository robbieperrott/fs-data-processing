'''
Error classes
'''


class ImpactNotFound(Exception):
    '''
    Throw if an impact score cannot be found for an ingredient
    I.e. if we traverse up the n-ary tree and reach a root node (a node with no parent_id)
    that does not have an impact_per_kg score.
    '''

class FoodClassMatchNotFound(Exception):
    '''
    Throw if no food class name matched the ingredient's name
    '''

class InvalidFoodClassTree(Exception):
    '''
    Throw if the food class tree constructed from the CSV is invalid.
    I.e. if there is a loop in the tree,
    or if a parent ID is found that does not point to an existing food class.
    '''
