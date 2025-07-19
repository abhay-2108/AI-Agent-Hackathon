# notifier/notion.py

import os
import requests

def detect_notion_type(notion_id):
    """
    Detect if the Notion ID is a page or database.
    """
    notion_token = os.getenv("NOTION_API_KEY")
    if not notion_token:
        return None
    
    try:
        # Try to get as page first
        url = f"https://api.notion.com/v1/pages/{notion_id}"
        headers = {
            "Authorization": f"Bearer {notion_token}",
            "Notion-Version": "2022-06-28"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return "page"
        elif response.status_code == 400 and "database" in response.text.lower():
            return "database"
        else:
            # Try as database
            url = f"https://api.notion.com/v1/databases/{notion_id}"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return "database"
            else:
                return None
            
    except Exception:
        return None

def send_to_notion(notion_id, title, summary, competitor_name=None, source_type="changelog"):
    """
    Send a competitor update to Notion (automatically detects page or database).
    """
    notion_token = os.getenv("NOTION_API_KEY")
    if not notion_token:
        print("No NOTION_API_KEY set.")
        return False
    
    # Extract competitor name from title if not provided
    if not competitor_name and "Competitor Update:" in title:
        competitor_name = title.split("Competitor Update:")[1].split()[0]
    elif not competitor_name:
        competitor_name = "Unknown"
    
    # Detect if it's a page or database
    notion_type = detect_notion_type(notion_id)
    
    if notion_type == "database":
        return send_to_notion_database(notion_id, title, summary, source_type, competitor_name)
    elif notion_type == "page":
        return send_to_notion_page(notion_id, title, summary)
    else:
        print(f"Could not determine if {notion_id} is a page or database")
        print("Trying as page first...")
        return send_to_notion_page(notion_id, title, summary)

def send_to_notion_page(page_id, title, summary):
    """
    Send a competitor update to Notion as a new page.
    """
    notion_token = os.getenv("NOTION_API_KEY")
    if not notion_token:
        print("No NOTION_API_KEY set.")
        return False
    
    try:
        url = "https://api.notion.com/v1/pages"
        headers = {
            "Authorization": f"Bearer {notion_token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        
        data = {
            "parent": {"page_id": page_id},
            "properties": {
                "title": {
                    "title": [
                        {
                            "text": {
                                "content": title
                            }
                        }
                    ]
                }
            },
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": summary
                                }
                            }
                        ]
                    }
                }
            ]
        }
        
        resp = requests.post(url, headers=headers, json=data, timeout=10)
        
        if resp.status_code == 200:
            print(f"Successfully sent to Notion page: {title}")
            return True
        elif resp.status_code == 404:
            print(f"Notion page not found. Check your NOTION_PAGE_ID: {page_id}")
            print("Make sure the page exists and your integration has access to it.")
            return False
        elif resp.status_code == 401:
            print("Notion API unauthorized. Check your NOTION_API_KEY.")
            return False
        elif resp.status_code == 403:
            print("Notion API forbidden. Check your integration permissions.")
            return False
        else:
            print(f"Failed to send to Notion page: {resp.status_code} - {resp.text}")
            return False
        
    except Exception as e:
        print(f"Failed to send to Notion page: {e}")
        return False

def send_to_notion_database(database_id, title, summary, source_type="changelog", competitor_name="Unknown"):
    """
    Send a competitor update to Notion as a new database entry.
    """
    notion_token = os.getenv("NOTION_API_KEY")
    if not notion_token:
        print("No NOTION_API_KEY set.")
        return False
    
    try:
        url = "https://api.notion.com/v1/pages"
        headers = {
            "Authorization": f"Bearer {notion_token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        
        data = {
            "parent": {"database_id": database_id},
            "properties": {
                "Title": {
                    "title": [
                        {
                            "text": {
                                "content": title
                            }
                        }
                    ]
                },
                "Summary": {
                    "rich_text": [
                        {
                            "text": {
                                "content": summary
                            }
                        }
                    ]
                },
                "Source Type": {
                    "select": {
                        "name": source_type
                    }
                },
                "Date": {
                    "date": {
                        "start": "2024-01-01"  # You might want to get current date
                    }
                },
                "Competitor": {
                    "rich_text": [
                        {
                            "text": {
                                "content": competitor_name
                            }
                        }
                    ]
                }
            }
        }
        
        resp = requests.post(url, headers=headers, json=data, timeout=10)
        
        if resp.status_code == 200:
            print(f"Successfully sent to Notion database: {title}")
            return True
        elif resp.status_code == 404:
            print(f"Notion database not found. Check your NOTION_PAGE_ID: {database_id}")
            return False
        elif resp.status_code == 400:
            print(f"Database schema error. Make sure your database has these properties:")
            print("  - Title (title)")
            print("  - Summary (rich_text)")
            print("  - Source Type (select)")
            print("  - Date (date)")
            return False
        else:
            print(f"Failed to send to Notion database: {resp.status_code} - {resp.text}")
            return False
        
    except Exception as e:
        print(f"Failed to send to Notion database: {e}")
        return False 