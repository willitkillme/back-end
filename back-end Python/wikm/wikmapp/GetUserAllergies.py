import requests

def get_user_allergies():
    url = 'http://127.0.0.1:8000/api/allergies/'
    headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE2NzYzMjkwLCJpYXQiOjE3MTY3NTI0OTAsImp0aSI6ImUyZTg2NTg3ZTQwZDQ3MGZhY2I4NmY0OWE4N2FkMDAxIiwidXNlcl9pZCI6MTEsInVzZXJuYW1lIjoidmFsYWtpMTdUZXN0In0.TkSwLrF0Si4MZoR7kQBSObjMMdXAl4z4cykz8DtOkG4'
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        allergies = response.json()
        return [allergy['name'] for allergy in allergies]
    else:
        return []