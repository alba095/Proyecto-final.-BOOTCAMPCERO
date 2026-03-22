from config import api_url,api_key
import requests

def get_conversion(moneda_from, moneda_to, cantidad):
    
    headers = {
        "X-CMC_PRO_API_KEY" : api_key
    }
    params = {
        "symbol" : moneda_from,
        "convert" : moneda_to ,
        "amount" : cantidad
    }
    response = requests.get(api_url, params = params, headers = headers)
    data = response.json()
    precio = data["data"][0]["quote"][moneda_to]["price"]
    return precio