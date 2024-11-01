import requests
import json

#open Json file return dict
def openJson(nameJson):
    
    with open(nameJson, 'r', encoding='utf-8') as file:
        
        data_json = json.load(file)
        
    return data_json

#request which return answer Api
def loginRequest(urlRequest = 'https://api-seller.rozetka.com.ua/sites', data_login = {}):
    
    response = requests.post(urlRequest, json=data_login)
    
    response.raise_for_status()
    
    responseData = json.loads(response.text)
    
    return responseData

#request which return 20 orders in page we indicated
def requestListOrders(urlRequest = 'https://api-seller.rozetka.com.ua/orders/search', headerData = {}, params = {}):
    
    response = requests.get(urlRequest, headers=headerData, params=params)
    
    response.raise_for_status()
    
    responseData = json.loads(response.text)
    
    return responseData


#function which take orders and return dict
def startBot(nameSeller, page_number):
    seller = {
        'Party Zoo': 'seller_PartyZoo.json',
        'Rock Dog': 'seller_RockDog.json'
    }
    
    data = openJson(seller[nameSeller])

    responseDataLogin = loginRequest('https://api-seller.rozetka.com.ua/sites', data)

    token = responseDataLogin['content']['access_token']

    requestHeaderListOrder = {
        'Authorization': f"Bearer {token}",
        'Accept-Validate-Exception': '1',
        'Content-Language': 'uk',
    }
    
    params = {
        "page": page_number,
        "types": 1
    }

    responseDataListOrder =  requestListOrders('https://api-seller.rozetka.com.ua/orders/search', requestHeaderListOrder, params)

    listOrder = responseDataListOrder['content']['orders']
    return listOrder

if __name__ == "__main__":
    result = startBot('Party Zoo', 53)
    print(result)

