import cv2
import pyzbar.pyzbar as pyzbar
from pyzbar.wrapper import ZBarSymbol
from matplotlib import pyplot as plt
import requests

def set_img(img):
    img=cv2.imread(img)
    return img

def barcode_scan(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    barcodes = pyzbar.decode(gray, [ZBarSymbol.EAN13, ZBarSymbol.EAN5])
    for barcode in barcodes:
         print('{}: {}'.format(barcode.type, barcode.data))

    barcode_ = barcode.data.decode('utf-8')
    return barcode_

#Example:

#img = "20240421_144402.jpg"
#barcode_scan(barcode_scan(set_img(img)))

def get_product_data(barcode):
    # API endpoint
    url = f'https://www.foodrepo.org/api/v3/products?gtin={barcode}'
    api_key= '34dcd2cee6a9f6a556a54bd1576fe36b'

    # Headers
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json'
    }

    response = requests.get(url, headers=headers)
    # Check if the request was successful
    if response.status_code == 200:
        product_data = response.json()
    else:
        print(f'Error: {response.status_code}')
        return None

    # Extracting ingredients (if available)
    if 'products' in product_data and len(product_data['products']) > 0:
        ingredients = product_data['products'][0].get('ingredients_translations', {})
    else:
        ingredients = {}

    data = product_data.get('data')

    # Filter the data based on the provided barcode
    filtered_data = [item for item in data if item.get('barcode') == barcode]

    # Extract English ingredients
    english_ingredients = [item['ingredients_translations'].get('en', '') for item in filtered_data]

    # Format into desired JSON structure
    filtered_data_english = [{"data": [{"ingredients_translations": {"en": ingredient}}]} for ingredient in english_ingredients]

    result = filtered_data_english[0]
    
    return result



# Example:

#barcode_ = '7610848493136' 
#result = get_product_data(barcode_)
#print(result)


# OR --> result = get_product_data((barcode_scan(set_img(img)))