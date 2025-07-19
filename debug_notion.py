#!/usr/bin/env python3
"""
Notion API Debug Script
Help identify and fix Notion API issues.
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_notion_credentials():
    """Check if Notion credentials are properly set."""
    print("🔑 Checking Notion credentials...")
    
    notion_token = os.getenv("NOTION_API_KEY")
    notion_page_id = os.getenv("NOTION_PAGE_ID")
    
    if not notion_token:
        print("❌ NOTION_API_KEY not found in .env file")
        return False
    
    if not notion_page_id:
        print("❌ NOTION_PAGE_ID not found in .env file")
        return False
    
    print(f"✅ NOTION_API_KEY found: {notion_token[:10]}...")
    print(f"✅ NOTION_PAGE_ID found: {notion_page_id}")
    return True

def test_notion_api_connection():
    """Test basic Notion API connectivity."""
    print("\n🔗 Testing Notion API connection...")
    
    notion_token = os.getenv("NOTION_API_KEY")
    
    try:
        # Test with a simple API call
        url = "https://api.notion.com/v1/users/me"
        headers = {
            "Authorization": f"Bearer {notion_token}",
            "Notion-Version": "2022-06-28"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Notion API connection successful")
            print(f"   User: {user_data.get('name', 'Unknown')}")
            return True
        elif response.status_code == 401:
            print("❌ Notion API unauthorized")
            print("   Check your NOTION_API_KEY - it might be invalid")
            return False
        else:
            print(f"❌ Notion API error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def detect_notion_type(notion_id):
    """Detect if the Notion ID is a page or database."""
    notion_token = os.getenv("NOTION_API_KEY")
    
    try:
        # Try to get as page first
        url = f"https://api.notion.com/v1/pages/{notion_id}"
        headers = {
            "Authorization": f"Bearer {notion_token}",
            "Notion-Version": "2022-06-28"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        print(f"   Page API response: {response.status_code}")
        
        if response.status_code == 200:
            return "page"
        elif response.status_code == 400 and "database" in response.text.lower():
            return "database"
        else:
            # Try as database
            url = f"https://api.notion.com/v1/databases/{notion_id}"
            response = requests.get(url, headers=headers, timeout=10)
            print(f"   Database API response: {response.status_code}")
            
            if response.status_code == 200:
                return "database"
            else:
                return None
            
    except Exception as e:
        print(f"   Detection error: {e}")
        return None

def test_notion_page_access():
    """Test if we can access the specified page."""
    print("\n📄 Testing Notion page/database access...")
    
    notion_token = os.getenv("NOTION_API_KEY")
    notion_id = os.getenv("NOTION_PAGE_ID")
    
    # Try to format the ID with dashes if it doesn't have them
    if notion_id and len(notion_id) == 32 and '-' not in notion_id:
        formatted_id = f"{notion_id[:8]}-{notion_id[8:12]}-{notion_id[12:16]}-{notion_id[16:20]}-{notion_id[20:]}"
        print(f"   Trying formatted ID: {formatted_id}")
        notion_id = formatted_id
    
    # Detect type first
    notion_type = detect_notion_type(notion_id)
    print(f"🔍 Detection result: {notion_type}")
    
    if notion_type == "database":
        print("📊 Detected: Database")
        return test_notion_database_access(notion_id)
    elif notion_type == "page":
        print("📄 Detected: Page")
        return test_notion_page_access_internal(notion_id)
    else:
        print("❌ Could not determine if it's a page or database")
        return False

def test_notion_page_access_internal(page_id):
    """Test if we can access the specified page."""
    notion_token = os.getenv("NOTION_API_KEY")
    
    try:
        url = f"https://api.notion.com/v1/pages/{page_id}"
        headers = {
            "Authorization": f"Bearer {notion_token}",
            "Notion-Version": "2022-06-28"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            page_data = response.json()
            print("✅ Page access successful")
            
            # Check page properties
            properties = page_data.get("properties", {})
            if "title" in properties:
                title = properties["title"].get("title", [])
                if title:
                    print(f"   Page title: {title[0].get('text', {}).get('content', 'Untitled')}")
            
            return True
        elif response.status_code == 404:
            print("❌ Page not found")
            print("   Possible issues:")
            print("   1. Page ID is incorrect")
            print("   2. Page doesn't exist")
            print("   3. Your integration doesn't have access to this page")
            return False
        elif response.status_code == 403:
            print("❌ Access forbidden")
            print("   Your integration doesn't have permission to access this page")
            print("   Make sure to:")
            print("   1. Share the page with your integration")
            print("   2. Give the integration 'Can edit' permissions")
            return False
        else:
            print(f"❌ Page access error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Page access error: {e}")
        return False

def test_notion_database_access(database_id):
    """Test if we can access the specified database."""
    notion_token = os.getenv("NOTION_API_KEY")
    
    try:
        url = f"https://api.notion.com/v1/databases/{database_id}"
        headers = {
            "Authorization": f"Bearer {notion_token}",
            "Notion-Version": "2022-06-28"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            db_data = response.json()
            print("✅ Database access successful")
            
            # Check database properties
            properties = db_data.get("properties", {})
            print(f"   Database properties: {list(properties.keys())}")
            
            # Check if required properties exist
            required_props = ["Title", "Summary", "Source Type", "Date"]
            missing_props = []
            for prop in required_props:
                if prop not in properties:
                    missing_props.append(prop)
            
            if missing_props:
                print(f"   ⚠️  Missing properties: {missing_props}")
                print("   You may need to add these properties to your database")
            
            return True
        elif response.status_code == 404:
            print("❌ Database not found")
            print("   Possible issues:")
            print("   1. Database ID is incorrect")
            print("   2. Database doesn't exist")
            print("   3. Your integration doesn't have access to this database")
            return False
        elif response.status_code == 403:
            print("❌ Access forbidden")
            print("   Your integration doesn't have permission to access this database")
            print("   Make sure to:")
            print("   1. Share the database with your integration")
            print("   2. Give the integration 'Can edit' permissions")
            return False
        else:
            print(f"❌ Database access error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Database access error: {e}")
        return False

def test_notion_page_creation():
    """Test if we can create content in the page/database."""
    print("\n✏️  Testing Notion content creation...")
    
    notion_token = os.getenv("NOTION_API_KEY")
    notion_id = os.getenv("NOTION_PAGE_ID")
    
    # Try to format the ID with dashes if it doesn't have them
    if notion_id and len(notion_id) == 32 and '-' not in notion_id:
        formatted_id = f"{notion_id[:8]}-{notion_id[8:12]}-{notion_id[12:16]}-{notion_id[16:20]}-{notion_id[20:]}"
        print(f"   Trying formatted ID: {formatted_id}")
        notion_id = formatted_id
    
    # Detect type first
    notion_type = detect_notion_type(notion_id)
    
    if notion_type == "database":
        return test_notion_database_creation(notion_id)
    elif notion_type == "page":
        return test_notion_page_creation_internal(notion_id)
    else:
        print("❌ Could not determine type for creation test")
        return False

def test_notion_page_creation_internal(page_id):
    """Test if we can create content in the page."""
    notion_token = os.getenv("NOTION_API_KEY")
    
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
                                "content": "🧪 Test Message"
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
                                    "content": "This is a test message from Competitor Tracker"
                                }
                            }
                        ]
                    }
                }
            ]
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        if response.status_code == 200:
            print("✅ Page creation successful")
            return True
        elif response.status_code == 404:
            print("❌ Parent page not found")
            print("   The page you're trying to add content to doesn't exist")
            return False
        elif response.status_code == 403:
            print("❌ Permission denied")
            print("   Your integration doesn't have permission to create content")
            return False
        else:
            print(f"❌ Page creation error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Page creation error: {e}")
        return False

def test_notion_database_creation(database_id):
    """Test if we can create content in the database."""
    notion_token = os.getenv("NOTION_API_KEY")
    
    # Format database ID with dashes if needed
    if len(database_id) == 32:
        formatted_id = f"{database_id[:8]}-{database_id[8:12]}-{database_id[12:16]}-{database_id[16:20]}-{database_id[20:]}"
        print(f"   Formatting database ID: {database_id} -> {formatted_id}")
        database_id = formatted_id
    
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
                                "content": "🧪 Test Entry"
                            }
                        }
                    ]
                },
                "Summary": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "This is a test entry from Competitor Tracker"
                            }
                        }
                    ]
                },
                "Source Type": {
                    "select": {
                        "name": "test"
                    }
                },
                "Date": {
                    "date": {
                        "start": "2024-01-01"
                    }
                },
                "Competitor": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Test Competitor"
                            }
                        }
                    ]
                }
            }
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        if response.status_code == 200:
            print("✅ Database entry creation successful")
            return True
        elif response.status_code == 404:
            print("❌ Database not found")
            print(f"   Database ID: {database_id}")
            return False
        elif response.status_code == 400:
            print("❌ Database schema error")
            print(f"   Response: {response.text}")
            print("   Make sure your database has these properties:")
            print("   - Title (title)")
            print("   - Summary (rich_text)")
            print("   - Source Type (select)")
            print("   - Date (date)")
            print("   - Competitor (rich_text)")
            return False
        elif response.status_code == 403:
            print("❌ Permission denied")
            print("   Your integration doesn't have permission to create entries")
            return False
        else:
            print(f"❌ Database creation error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Database creation error: {e}")
        return False

def main():
    """Run all Notion debug tests."""
    print("🔍 Notion API Debug Tool")
    print("=" * 40)
    
    # Check credentials
    if not check_notion_credentials():
        print("\n❌ Please fix your credentials first")
        return
    
    # Test API connection
    if not test_notion_api_connection():
        print("\n❌ API connection failed")
        return
    
    # Test page/database access
    if not test_notion_page_access():
        print("\n❌ Page/database access failed")
        return
    
    # Test content creation
    if not test_notion_page_creation():
        print("\n❌ Content creation failed")
        return
    
    print("\n🎉 All Notion tests passed!")
    print("Your Notion integration should work correctly now.")

if __name__ == "__main__":
    main() 