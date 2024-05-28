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