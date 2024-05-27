import cv2
import pyzbar.pyzbar as pyzbar
from pyzbar.wrapper import ZBarSymbol
from matplotlib import pyplot as plt
import requests

img = null



def set_img(path):
    img=cv2.imread(path)

def run():
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    barcodes = pyzbar.decode(gray, [ZBarSymbol.EAN13, ZBarSymbol.EAN5])
    for barcode in barcodes:
        print('{}: {}'.format(barcode.type, barcode.data))

    barcode_ = barcode.data.decode('utf-8')
    product_code = barcode_        # ide a termék kódot!!                  Pombär: '4000522108440'
    url_base = 'https://big-product-data.p.rapidapi.com/gtin/'
    base_url = "https://api.example.com"
    url = f"{url_base}{product_code}"

    headers = {
        "X-RapidAPI-Key": '59499afdc9msh2cfe3f889acb5f7p1e162ajsn06de5ce8230e'  # RapidAPI kulcs
    }
    response = requests.get(url, headers=headers)
    data = response.json()
def get_data():
    return data



from GetProdData import check_for_allergens
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_user_allergies(request):
    user = request.user
    data_json = request.data.get('data_json', '{}')
    try:
        data = json.loads(data_json)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    allergens = check_for_allergens(user, data_json)
    
    return JsonResponse({"allergens": allergens})

