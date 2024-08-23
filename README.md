# GMAIL and Notion Integration

This project integrates GMAIL and Notion to search for today's emails and load them into a Notion table.

## Setup

### GMAIL API Credentials

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing project.
3. Enable the GMAIL API for the project.
4. Create OAuth 2.0 credentials.
5. Download the `credentials.json` file and place it in the root directory of the project.

### Notion API Credentials

1. Go to the [Notion Integrations](https://www.notion.so/my-integrations) page.
2. Create a new integration.
3. Copy the integration token.
4. Share the database with the integration.

### Environment Variables

Create a `.env` file in the root directory of the project and add the following environment variables:

```
NOTION_TOKEN=your_notion_integration_token
NOTION_DATABASE_ID=your_notion_database_id
NOTION_PAGE_ID=your_notion_page_id
GROQ_API_KEY=your_groq_api_key
```

## Running the Application

1. Install the required dependencies:

```
pip install -r requirements.txt
```

2. Run the FastAPI application:

```
uvicorn app.main:app --reload
```

3. Use the `/load_emails_to_notion` endpoint to load today's emails into Notion.

4. Use the `/create_social_post` endpoint to create a social media post using GROQ LLaMA3 70B. Send a POST request with JSON data containing the `content` field to this endpoint. The response will contain the generated social media post.
