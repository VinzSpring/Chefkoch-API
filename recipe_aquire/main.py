from chefkoch import ChefKochAPI, DataParser

if __name__ == '__main__':
    categories = ChefKochAPI.get_categories()

    category = categories[0]

    recipes = ChefKochAPI.parse_recipes(category, 5)

    DataParser.write_recipes_to_json(category.title, recipes)
