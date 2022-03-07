'''Error classes'''


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

class ParentNotFound(Exception):
    '''
    Throw if a food class has a parent ID that does not
    match the ID of any food class
    '''

class LoopInFoodClassTree(Exception):
    '''
    Throw if it is discovered that the parent_id of a food class
    is the id of the food class's children,
    or if the parent_id of a food class is equal to its own id.
    This is to prevent an infinite loop while moving up the tree.
    '''
