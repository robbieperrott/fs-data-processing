# Foodsteps Data Processing Task

## Running the code

Open a terminal window, go to the fs-data-processing folder and run the following command:

`python calculate_recipe_impacts.py`

You should then see a list of recipes, with impact scores for recipes where impacts were successfully calculated, and error messages for recipes whose impacts could not be calculated.

## Testing

I have included some small test CSV files that I used to check the correctness of my code. To use these files rather than the given CSVs run:

`python calculate_recipe_impacts.py test`

The test files are located in `fs-data-processing/files/test/`. You can play around with the CSV data and check the results.

## Mypy

I used mypy for type checking. If you run `mypy .` you should see something like `Success: no issues found in 5 source files`.





