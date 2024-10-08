import os
from notion_client import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the Notion client
notion = Client(auth=os.environ["NOTION_API_KEY"])

def check_template_exists(database_id):
    """Check if the template database exists."""
    try:
        notion.databases.retrieve(database_id)
        return True
    except:
        return False

def create_template(database_id, properties):
    """Create a new template database."""
    notion.databases.create(
        parent={"page_id": os.environ["NOTION_PAGE_ID"]},
        title=[{"type": "text", "text": {"content": "My Template Database"}}],
        properties=properties
    )

def add_data_to_table(database_id, data):
    """Add data to the Notion table."""
    notion.pages.create(
        parent={"database_id": database_id},
        properties=data
    )

def add_to_notion_table(data):
    """
    Add data to Notion table. If the table doesn't exist, create a new one.
    
    :param data: Dictionary containing the data to be added
    :return: String indicating success or failure
    """
    database_id = os.environ["NOTION_DATABASE_ID"]
    
    if not check_template_exists(database_id):
        # Define the properties for your template
        properties = {
            "Name": {"title": {}},
            "Description": {"rich_text": {}},
            "Status": {
                "select": {
                    "options": [
                        {"name": "To Do", "color": "red"},
                        {"name": "In Progress", "color": "yellow"},
                        {"name": "Done", "color": "green"}
                    ]
                }
            }
        }
        create_template(database_id, properties)
    
    try:
        add_data_to_table(database_id, data)
        return "Data added successfully"
    except Exception as e:
        return f"Error adding data: {str(e)}"

def create_daily_read_page():
    """
    Create a 'daily read' page if it doesn't exist.
    
    :return: String indicating success or failure
    """
    page_title = "daily read"
    database_id = os.environ["NOTION_DATABASE_ID"]
    
    # Check if the 'daily read' page already exists
    try:
        response = notion.databases.query(
            **{
                "database_id": database_id,
                "filter": {
                    "property": "Name",
                    "title": {
                        "equals": page_title
                    }
                }
            }
        )
        if response["results"]:
            return "Page already exists"
    except Exception as e:
        return f"Error checking page existence: {str(e)}"
    
    # Create the 'daily read' page
    try:
        notion.pages.create(
            parent={"database_id": database_id},
            properties={
                "Name": {"title": [{"text": {"content": page_title}}]}
            }
        )
        return "Page created successfully"
    except Exception as e:
        return f"Error creating page: {str(e)}"
