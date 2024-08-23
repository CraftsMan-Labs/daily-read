from flask import Flask, request, jsonify
from app.utils.notion_integration import add_to_notion_table, create_daily_read_page
from app.utils.gmail_integration import get_todays_emails

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

if __name__ == '__main__':
    app.run(debug=True)
