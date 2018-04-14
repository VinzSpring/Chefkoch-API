# Chefkoch-API
A small API for pulling recipe data from [Chefkoch](www.chefkoch.de)
This project was made for machine learning researcers who'd need to craft a database of different dishes and their
ingredients.

## Example/How to use
```python
#get all available dish categories
categories = ChefKochAPI.get_categories()

#parse all recipes (yields) from the first category
recipes = ChefKochAPI.parse_recipes(categories[0])

#write recipes to json file one at a time
DataParser.write_recipes_to_json(category.title, recipes)

```

# if you are associated with chefkoch.de and want me to take this down, please message me :)
