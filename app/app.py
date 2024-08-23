from flask import Flask, request, jsonify
from app.utils.notion_integration import add_to_notion_table, create_daily_read_page
from app.utils.gmail_integration import get_todays_emails
from app.utils.groq_llama3 import generate_social_post
import os

app = Flask(__name__)

@app.route('/add_to_notion', methods=['POST'])
def add_to_notion():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    result = add_to_notion_table(data)
    return jsonify({"message": result})

@app.route('/load_emails_to_notion', methods=['POST'])
def load_emails_to_notion():
    emails = get_todays_emails()
    if not emails:
        return jsonify({"error": "No emails found"}), 400
    
    # Create 'daily read' page if it doesn't exist
    create_daily_read_page()
    
    for email in emails:
        data = {
            "Name": {"title": [{"text": {"content": email['subject']}}]},
            "Description": {"rich_text": [{"text": {"content": email['body']}}]},
            "Status": {"select": {"name": "To Do"}}
        }
        add_to_notion_table(data)
    
    return jsonify({"message": "Emails loaded to Notion successfully"})

@app.route('/create_social_post', methods=['POST'])
def create_social_post():
    content = request.json.get('content')
    if not content:
        return jsonify({"error": "No content provided"}), 400
    
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        return jsonify({"error": "GROQ_API_KEY not found"}), 500
    
    social_post = generate_social_post(content, api_key)
    return jsonify({"social_post": social_post})

if __name__ == '__main__':
    app.run(debug=True)
