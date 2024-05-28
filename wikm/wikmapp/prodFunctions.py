import requests
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
        "Emmer", "Matzo ", "Udon noodles", "Pasta", 
        "Bread ", "Crackers", "Cookies", 
        "Cakes", "Pastries", "Pizza crust", 
        "Beer", "Some soy sauces", "Some processed foods"
    ],
    "eggs": [
        "Eggs", "Egg powder", "Eggnog", "Mayonnaise", "Aioli", "Meringue", 
        "Custard", "Pudding", "Quiche", "Frittata", "Omelet", "Scrambled eggs", 
        "Deviled eggs", "Egg noodles", "Pasta", "Egg wash", 
        "Baked goods (many types of bread, cakes, muffins, cookies, pastries)", "French toast", 
        "Pancakes", "Waffles", 
        "Meatloaf", "Meatballs", 
        "Breaded or battered food", "Ice cream", 
        "Marshmallows", "Marzipan", "Some candies"
    ],
    "soy": [
        "Soybeans", "Soy sauce", "Tamari", "Miso", "Tempeh", "Tofu", "Edamame", "Soy milk", 
        "Soy yogurt", "Soy cheese", "Soy protein isolate", "Soy protein concentrate", "Soy lecithin", 
        "Textured vegetable protein (TVP)", "Natto", "Soy flour", "Soybean oil", 
        "Soy nuts", "Soy nut butter", "Shoyu", "Teriyaki sauce", 
        "Vegetable broth", "Hydrolyzed soy protein", "Soy crisps", 
        "Meat substitutes"
    ],
    "fish_and_seafood": [
        "Fish", "Salmon", "Tuna", "Cod", "Haddock", "Halibut", "Mackerel", "Sardines", 
        "Anchovies", "Tilapia", "Trout", "Bass", "Shellfish", "Shrimp", "Crab", "Lobster", 
        "Clams", "Mussels", "Oysters", "Scallops", "Squid (calamari)", "Fish sauce", "Oyster sauce", 
        "Worcestershire sauce", "Caviar", "Roe", "Imitation crab (surimi)", 
        "Fish stock", "Fish broth", "Bouillabaisse", "Pâté", 
        "Seafood soup", "Sushi and sashimi", "Seafood salad", 
        "Seafood-based dips", "Fish sticks","fish fingers", "Breaded seafood","battered seafood", 
        "Canned fish", "Dried fish", "Pickled fish", 
        "Smoked fish"
    ]
}

import requests
import re

def GetProdData(barcode):
    headers = {
        "Authorization": 'Token a769dd89b0a61ab6ec841ef69b790557'  # API token
    }
    
    response = requests.get(f'https://www.foodrepo.org/api/v3/products?excludes=images%2Cnutrients&barcodes={barcode}', headers=headers)
    data = response.json()
    
    all_ingredients = []  # List to store all ingredient lists
    
    if data and 'data' in data and data['data']:
        for item in data['data']:
            ingredients_translation = item.get('ingredients_translations', {}).get('en', None)
            if ingredients_translation:
                # Use regular expressions to remove all non-letter characters except comma
                cleaned_ingredients = re.sub(r'[^a-zA-Z,\s]', '', ingredients_translation)
                cleaned_ingredients = cleaned_ingredients.replace('\r\n', '')
                cleaned_ingredients = cleaned_ingredients.replace('May contain traces of', ', ')
                cleaned_ingredients = cleaned_ingredients.replace('contains  or less of ', ', ')
                # Fix spaces: Replace consecutive spaces with a single space
                cleaned_ingredients = re.sub(r'\s+', ' ', cleaned_ingredients)
                # Fix spaces: Remove leading and trailing spaces
                cleaned_ingredients = cleaned_ingredients.strip()
                # Remove empty strings
                cleaned_ingredients = cleaned_ingredients.replace(',,', ',')
                # Split cleaned ingredients by comma
                split_ingredients = [ingredient.strip().lower() for ingredient in cleaned_ingredients.split(',')]
                # Filter out lists with only empty strings
                split_ingredients = [ingredient_list for ingredient_list in split_ingredients if ingredient_list]
                # Append cleaned ingredients to the list if non-empty
                if split_ingredients:
                    all_ingredients.append(split_ingredients)
    
    return all_ingredients


#NOTE: IDE ÚJ FUNCTION

def _compute_lps_array(pattern):
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def _kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)

    lps = _compute_lps_array(pattern)
    
    i = 0 
    j = 0 
    
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        
        if j == m:
            return True
        
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return False

def check_for_allergens(ing_list, user_allergy):
    allergictto = set()

    for ingredient_list in ing_list:
        for ingredient in ingredient_list:
            ingredient = str(ingredient)
            for allergen, items in ingredients.items():
                for item in items:
                    if _kmp_search(item.lower(), ingredient.lower()):
                        allergictto.add(allergen)
    
    return list(allergictto.intersection(user_allergy))
