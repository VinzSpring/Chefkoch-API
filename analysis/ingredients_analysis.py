
class IngredientsAnalyzer:
    @staticmethod
    def analyze(recipes):
        statistics = {}
        for recipe in recipes:
            for ingredient in recipe.ingredients:
                if ingredient.name in statistics:
                    statistics[ingredient.name] += 1
                else:
                    statistics[ingredient.name] = 1
        return statistics