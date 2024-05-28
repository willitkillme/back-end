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

def GetProdData(barcode):
    headers = {
        "Authorization": 'Token a769dd89b0a61ab6ec841ef69b790557'  # API token
    }
    
    response = requests.get(f'https://www.foodrepo.org/api/v3/products?excludes=images%2Cnutrients&barcodes={barcode}', headers=headers)
    data = response.json()
    
    ingredients = []
    if data and 'data' in data and data['data']:
        for item in data['data']:
            ingredients_translation = item.get('ingredients_translations', {}).get('en', None)
            if ingredients_translation:
                ingredients.append(ingredients_translation)

    return ingredients


#NOTE: IDE ÚJ FUNCTION

data_json = None

def _process_ingredient_list(data): #pass extracted info from barcode.
    ingredients_str = data['data'][0]['ingredients_translations']['en']
    ingredients_list = [ingredient.strip() for ingredient in ingredients_str.split(',')]
    for i in range(len(ingredients_list)):
        ingredients_list[i] = ingredients_list[i].replace('.', '')
    return ingredients_list

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

    lps = compute_lps_array(pattern)
    
    i = 0 
    j = 0 
    
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        
        if j == m:
            #print("GAY")
            return True
        
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return False

def check_for_allergens(data_json,user_allergy):
    allergictto=[]
    data = json.loads(data_json)
    ing_list=process_ingredient_list(data)
    
    for ingredient in ing_list:
        for allergen, items in ingredients.items():
            for item in items:
                #if ingredient.lower() == item.lower():
                if _kmp_search(item.lower(),ingredient.lower()): ##comment out if dont work, untested shi
                    allergictto.append(allergen)

    return [item for item in allergictto if item in user_allergy]