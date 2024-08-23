from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.utils.notion_integration import add_to_notion_table, create_daily_read_page
from app.utils.gmail_integration import get_todays_emails
from app.utils.groq_llama3 import generate_social_post
import os

app = FastAPI()

class NotionData(BaseModel):
    Name: dict
    Description: dict
    Status: dict

class SocialPostContent(BaseModel):
    content: str

@app.post("/add_to_notion")
async def add_to_notion(data: NotionData):
    result = add_to_notion_table(data.dict())
    return {"message": result}

@app.post("/load_emails_to_notion")
async def load_emails_to_notion():
    emails = get_todays_emails()
    if not emails:
        raise HTTPException(status_code=400, detail="No emails found")
    
    create_daily_read_page()
    
    for email in emails:
        data = {
            "Name": {"title": [{"text": {"content": email['subject']}}]},
            "Description": {"rich_text": [{"text": {"content": email['body']}}]},
            "Status": {"select": {"name": "To Do"}}
        }
        add_to_notion_table(data)
    
    return {"message": "Emails loaded to Notion successfully"}

@app.post("/create_social_post")
async def create_social_post(content: SocialPostContent):
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not found")
    
    social_post = generate_social_post(content.content, api_key)
    return {"social_post": social_post}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
