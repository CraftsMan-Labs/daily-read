from flask import Flask, request, jsonify
from app.utils.notion_integration import add_to_notion_table

app = Flask(__name__)

@app.route('/add_to_notion', methods=['POST'])
def add_to_notion():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    result = add_to_notion_table(data)
    return jsonify({"message": result})

if __name__ == '__main__':
    app.run(debug=True)
