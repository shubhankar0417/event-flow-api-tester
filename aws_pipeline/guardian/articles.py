import requests
from utils.config import get_config

def get_guardian_articles(category):
    config = get_config()
    url = config['GUARDIAN_API_URL']
    key = config['GUARDIAN_API_KEY']
    params = {
        'q': category,
        'api-key': key
    }
    # Pass the url and params to get the query response
    response = requests.get(url, params)
    
    # print('Response :', response.json())
    # print('Status :', response.status_code)
    return response

    
