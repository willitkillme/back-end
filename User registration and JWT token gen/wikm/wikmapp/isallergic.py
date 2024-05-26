import json

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
        "Eggs (whole, whites, yolks)", "Egg powder", "Eggnog", "Mayonnaise", "Aioli", "Meringue", 
        "Custard", "Pudding", "Quiche", "Frittata", "Omelet", "Scrambled eggs", 
        "Deviled eggs", "Egg noodles", "Pasta", "Egg wash (used in baking)", 
        "Baked goods (many types of bread, cakes, muffins, cookies, pastries)", "French toast", 
        "Pancakes", "Waffles", 
        "Meatloaf", "Meatballs", 
        "Breaded or battered foods (the coating often contains egg)", "Ice cream", 
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

data_json = None

def process_ingredient_list(data): #pass extracted info from barcode.
    ingredients_str = data['data'][0]['ingredients_translations']['en']
    ingredients_list = [ingredient.strip() for ingredient in ingredients_str.split(',')]
    for i in range(len(ingredients_list)):
        ingredients_list[i] = ingredients_list[i].replace('.', '')
    return ingredients_list

def check_for_allergens(data_json): #pass what the user is allergic to
    #could optimize further because its ->
    # -> unnecessary to check those key value pairs where the user isn't allergic but will do for now
    allergictto=[]
    data = json.loads(data_json)
    ing_list=process_ingredient_list(data)
    
    for ingredient in ing_list:
        for allergen, items in ingredients.items():
            for item in items:
                if ingredient.lower() == item.lower():
                    allergictto.append(allergen)
    return allergictto
