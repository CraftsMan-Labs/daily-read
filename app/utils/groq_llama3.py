import requests
import os

def generate_social_post(content, api_key):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": [{"role": "user", "content": content}],
        "model": "llama3-8b-8192"
    }
    response = requests.post(url, headers=headers, json(data))
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}
