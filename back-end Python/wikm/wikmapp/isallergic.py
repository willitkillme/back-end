import json
import wikmapp.GetProdData
import wikmapp.GetUserAllergies
import requests
import logging


ingredients = {
    "lactose": [
        "Milk", "Cream", "Butter", "Cheese (most types)", "Yogurt", "Ice cream", "Sour cream", 
        "Condensed milk", "Evaporated milk", "Buttermilk", "Whey", "Milk powder", "Milk solids", 
        "Casein", "Cream cheese", "Cottage cheese", "Ricotta cheese", "Kefir", "Custard", "Pudding","Milk ingredients"
    ],
    "gluten": [
        "Wheat", "Barley", "Rye", "Triticale (a cross between wheat and rye)", "Spelt", "Kamut", 
        "Farro", "Bulgur", "Semolina", "Couscous", "Durum wheat", "Graham flour", "Malt", 
        "Malt extract", "Malt syrup", "Brewer's yeast", "Wheat starch", "Modified wheat starch", 
        "Hydrolyzed wheat protein", "Seitan (wheat gluten)", "Wheat bran", "Wheat germ", "Einkorn", 
        "Emmer", "Matzo (unless specifically gluten-free)", "Udon noodles", "Pasta (unless gluten-free)", 
        "Bread (unless gluten-free)", "Crackers (unless gluten-free)", "Cookies (unless gluten-free)", 
        "Cakes (unless gluten-free)", "Pastries (unless gluten-free)", "Pizza crust (unless gluten-free)", 
        "Beer (unless gluten-free)", "Some soy sauces (unless labeled gluten-free)", "Some processed foods (check labels for hidden gluten)"
    ],
    "eggs": [
        "Eggs (whole, whites, yolks)", "Egg powder", "Eggnog", "Mayonnaise", "Aioli", "Meringue", 
        "Custard", "Pudding (some types)", "Quiche", "Frittata", "Omelet", "Scrambled eggs", 
        "Deviled eggs", "Egg noodles", "Pasta (some types)", "Egg wash (used in baking)", 
        "Baked goods (many types of bread, cakes, muffins, cookies, pastries)", "French toast", 
        "Pancakes", "Waffles", "Some salad dressings (e.g., Caesar dressing)", "Some sauces (e.g., hollandaise, béarnaise)", 
        "Meatloaf (often contains egg as a binder)", "Meatballs (often contains egg as a binder)", 
        "Breaded or battered foods (the coating often contains egg)", "Ice cream (some types)", 
        "Marshmallows (some types)", "Marzipan (some types)", "Some candies (e.g., certain chocolates, nougat)", 
        "Certain processed foods (always check labels)"
    ],
    "soy": [
        "Soybeans", "Soy sauce", "Tamari", "Miso", "Tempeh", "Tofu", "Edamame", "Soy milk", 
        "Soy yogurt", "Soy cheese", "Soy protein isolate", "Soy protein concentrate", "Soy lecithin", 
        "Textured vegetable protein (TVP)", "Natto", "Soy flour", "Soybean oil", 
        "Soy nuts", "Soy nut butter", "Shoyu", "Teriyaki sauce (often contains soy sauce)", 
        "Vegetable broth (sometimes contains soy)", "Hydrolyzed soy protein", "Soy crisps", 
        "Meat substitutes (many vegetarian and vegan products like veggie burgers, sausages, and deli slices)", 
        "Some baked goods (check labels)", "Some cereals (check labels)", "Some snack foods (check labels)", 
        "Some chocolate and candy (check labels)", "Some infant formulas (check labels)"
    ],
    "fish_and_seafood": [
        "Fish (all types)", "Salmon", "Tuna", "Cod", "Haddock", "Halibut", "Mackerel", "Sardines", 
        "Anchovies", "Tilapia", "Trout", "Bass", "Shellfish (all types)", "Shrimp", "Crab", "Lobster", 
        "Clams", "Mussels", "Oysters", "Scallops", "Squid (calamari)", "Fish sauce", "Oyster sauce", 
        "Worcestershire sauce (some brands contain anchovies)", "Caviar", "Roe", "Imitation crab (surimi)", 
        "Fish stock", "Fish broth", "Bouillabaisse (fish stew)", "Pâté (some types)", 
        "Seafood soup (clam chowder, lobster bisque, etc.)", "Sushi and sashimi", "Seafood salad", 
        "Seafood-based dips", "Fish sticks/fish fingers", "Breaded or battered seafood", 
        "Canned fish (tuna, salmon, sardines, etc.)", "Dried fish", "Pickled fish (herring, etc.)", 
        "Smoked fish (salmon, mackerel, etc.)"
    ]
}

#-------------------------------------------------------------------------------------------------------------------------
# 1 : 1 equality (nem jó, mert nem mindig van szó szerint):

# data_json = '{"data": [{"ingredients_translations": {"en": "Milk, Sugar, Wheat Flour, Salt, Mussels"}}]}' #json.null

# def set_data(data):
#     data_json=data
# def process_ingredient_list(data): #pass extracted info from barcode.
#     ingredients_str = data['data'][0]['ingredients_translations']['en']
#     ingredients_list = [ingredient.strip() for ingredient in ingredients_str.split(',')]
#     for i in range(len(ingredients_list)):
#         ingredients_list[i] = ingredients_list[i].replace('.', '')
#     return ingredients_list


# def check_for_allergens(user): #pass what the user is allergic to
#     #could optimize further because its ->
#     # -> unnecessary to check those key value pairs where the user isn't allergic but will do for now
#     allergictto=[]
#     data = json.loads(data_json)
#     ing_list=process_ingredient_list(data)
    
#     for ingredient in ing_list:
#         for allergen, items in ingredients.items():
#             for item in items:
#                 if ingredient.lower() == item.lower():
#                     allergictto.append(allergen)
#     return allergictto

# print(check_for_allergens("asdf"))

#-------------------------------------------------------------------------------------------------------------------------


# similarity:

def process_ingredient_list(data): #pass extracted info from barcode.
    ingredients_str = data['data'][0]['ingredients_translations']['en']
    ingredients_list = [ingredient.strip() for ingredient in ingredients_str.split(',')]
    for i in range(len(ingredients_list)):
        ingredients_list[i] = ingredients_list[i].replace('.', '')
    return ingredients_list

#Example data:
#data_json = '{"data": [{"ingredients_translations": {"en": "Milk, Sugar, Wheat Flour, Salt, Mussels"}}]}'

#data_json = wikmapp.GetProdData.get_product_data(wikmapp.GetProdData.barcode_scan(wikmapp.GetProdData.set_img(img)))     # img = "20240421_144402.jpg"

def check_for_allergens(): 
    allergicto = []
    data = json.loads(data_json)
    ing_list = process_ingredient_list(data)
    
    for ingredient in ing_list:
        for allergen, items in ingredients.items():
            for item in items:
                if item.lower() in ingredient.lower() or ingredient.lower() in item.lower():
                    allergicto.append(allergen)
                    break  # Break out of the inner loop if a match is found
            else:
                continue  # Continue to the next allergen if no match is found
            break  # Break out of the middle loop if a match is found
    return allergicto

#print(check_for_allergens())


#Example:

#print(list(set(wikmapp.GetUserAllergies.get_user_allergies()).intersection(check_for_allergens())))
