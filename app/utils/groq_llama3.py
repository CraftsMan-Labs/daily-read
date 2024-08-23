import requests
import os

def generate_social_post(content, api_key):
    url = "https://api.groq.com/llama3/70b/generate"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": content,
        "max_tokens": 100
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("text")
    else:
        return None
