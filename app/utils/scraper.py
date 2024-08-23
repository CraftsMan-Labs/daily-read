import requests

def scrape_website_data(url):
    BASE_URL = "https://r.jina.ai/"
    response = requests.get(BASE_URL + url)
    return response.text
