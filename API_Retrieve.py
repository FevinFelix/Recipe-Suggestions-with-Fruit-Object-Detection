
import requests

class Recipe():
     def __init__(self, picture, link, name, missed_ingredients):
         self.picture = picture
         self.link = link
         self.name = name
         self.missed_ingredients = missed_ingredients


def get_recipes(ingredients): #takes list of strings for ingredients (assumes at least one in it) and returns list of recipe objects
    recipes = []
    ingredient_string = ""
    if len(ingredients) == 1:
        ingredient_string = f"{ingredients[0]}"
    else:
        ingredient_string += f"{ingredients[0]}"
        for ingredient in ingredients[1:]:          # every other ingredient after the first
            ingredient_string += f",+{ingredient}"

    api_key = '352414cea46e40089e7970226495d8dd'
    api_call = f"https://api.spoonacular.com/recipes/findByIngredients?apiKey={api_key}&ingredients={ingredient_string}&ranking=2"

    api_response = requests.get(api_call).json()

    for recipe in api_response:
        missed = []
        recipe_name = recipe["title"].replace(' ', '-') + '-'
        link_start = "https://spoonacular.com/recipes/"
        recipe_id = recipe["image"][-18: -12]
        recipe_link = ''.join((link_start, recipe_name, recipe_id))

        for missed_ingredient in recipe["missedIngredients"]:
            missed.append(missed_ingredient["name"])

        recipes.append(Recipe(recipe["image"], recipe_link, recipe["title"], missed))
    
        
    return recipes

stuff = get_recipes(["strawberries, bananas"])
for item in stuff:
    print (item.name + '\n', item.link + '\n', item.picture + '\n', item.missed_ingredients)
    print()
    print("---------------------------------------------------------")