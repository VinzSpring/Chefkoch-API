import requests as rq
from bs4 import BeautifulSoup
import re
import json


class Category:
    id_pattern = re.compile("(/rs/s0)(g\d*)")

    def __init__(self, title, url=None, id=None):
        self.title = title.replace("&", "")
        if url is not None:
            self.id = Category.id_pattern.search(url).group(2)
        if id is not None:
            self.id = id

    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)


class Ingredient:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)


class Recipe:
    def __init__(self, name, id, category, ingredients):
        self.name = name
        self.id = id
        self.category = category
        self.ingredients = ingredients

    @staticmethod
    def from_json(json_obj):
        name = json_obj['name']
        id = json_obj['id']
        category = Category(json_obj['category']['title'], id=json_obj['category']['id'])
        ingredients = [Ingredient(ingredient['name'], ingredient['amount']) for ingredient in json_obj['ingredients']]
        return Recipe(name, id, category, ingredients)

    def __str__(self):
        return json.dumps({
            "name": self.name,
            "id": self.id,
            "category": self.category.__dict__,
            "ingredients": [ingredient.__dict__ for ingredient in self.ingredients]
        }, ensure_ascii=False)


class ChefKochAPI:
    base_url = "https://www.chefkoch.de/"

    @staticmethod
    def get_categories():
        response = rq.get(ChefKochAPI.base_url + "rezepte/kategorien/")
        soup = BeautifulSoup(response.text, "html5lib")

        categories = []
        for category_column in soup.findAll("div", {"class": "category-column"}):
            for category_container in category_column.findChildren():
                category = category_container.find('a', href=True)
                try:
                    title = category.string
                    url = category["href"]
                except Exception:
                    continue
                categories.append(Category(title, url=url))

        return categories

    @staticmethod
    def parse_recipes(category, end_index=0, start_index=0):

        # max_dish_count = int(soup.)
        index = start_index
        while True:
            response = rq.get(ChefKochAPI.base_url + 'rs/' + 's' + str(index) + category.id + '/')
            if response.status_code == 404:
                return
            soup = BeautifulSoup(response.text, "html5lib")

            for recipe_list_item in soup.find_all("li", {"class": "search-list-item"}):

                index += 1

                recipe_id = recipe_list_item['id'].replace("recipe-", "")
                recipe_url = ChefKochAPI.base_url + "rezepte/" + recipe_id + "/"
                recipe_response = rq.get(recipe_url)

                if recipe_response.status_code != 200:
                    continue

                recipe_soup = BeautifulSoup(recipe_response.text, "html5lib")
                recipe_name = recipe_soup.find("h1", {"class": "page-title"}).text
                ingredients_table = recipe_soup.find("table", {"class": "incredients"})
                ingredients_table_body = ingredients_table.find("tbody")

                recipe_ingredients = []
                for row in ingredients_table_body.find_all('tr'):
                    cols = row.find_all('td')
                    recipe_ingredients.append(Ingredient(cols[1].text.strip().replace(u"\u00A0", " "),
                                                         cols[0].text.strip().replace(u"\u00A0", " ")))

                yield Recipe(recipe_name.replace(u"\u00A0", " "), recipe_id.replace(u"\u00A0", " "),
                       category, recipe_ingredients)

                if 0 < end_index < index:
                    return


class DataParser:

    @staticmethod
    def write_recipes_to_json(file_path, recipes,):
        with open(file_path + ".json", "w") as txt_file:
            txt_file.write("[")
            for recipe in recipes:
                try:
                    txt_file.write(str(recipe))
                    txt_file.write(",")
                except Exception:
                    pass
            txt_file.write("{}]")

    @staticmethod
    def load_recipes_from_json(file_path):
        raw_text = ""
        with open(file_path) as file:
            raw_text = file.read()

        recipes = []
        for obj in json.loads(raw_text):
            if len(obj.keys()) > 0:
                recipes.append(Recipe.from_json(obj))
        return recipes
