#%%
from matplotlib.pyplot import title
import requests

api_key = '352414cea46e40089e7970226495d8dd'
api_call = f"https://api.spoonacular.com/recipes/findByIngredients?apiKey={api_key}&ingredients=apples,+oranges"

api_response = requests.get(api_call).json()


#%%
for recipe in api_response:
    print(recipe["title"])
    print(recipe["image"])
    recipe_name = recipe["title"].replace(' ', '-') + '-'
    link_start = "https://spoonacular.com/recipes/"
    recipe_id = recipe["image"][-18: -12]
    recipe_link = ''.join((link_start, recipe_name, recipe_id))
    print("link to recipe: " + recipe_link)

 
    for missed_ingredient in recipe["missedIngredients"]:
        print(missed_ingredient["name"], end="     ")
        print()
    print()
# %%
