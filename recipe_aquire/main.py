from chefkoch import ChefKochAPI, DataParser
from datetime import date

if __name__ == '__main__':
    categories = ChefKochAPI.get_categories()

    # recipe_amount = 200
    # recipes = []
    #category = categories[0]
    for category in categories:
        category_recipes = ChefKochAPI.parse_recipes(category)
        DataParser.write_recipes_to_json(str(date.today()) + "-category-" + category.title, category_recipes)
        """ for category_recipe in category_recipes:
            recipes.append(category_recipe) """