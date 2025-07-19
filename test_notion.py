#!/usr/bin/env python3
"""
Notion API Test Script
Test Notion API integration for Competitor Feature Tracker.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_notion_credentials():
    """Test if Notion credentials are properly configured."""
    print("🔑 Testing Notion credentials...")
    
    notion_token = os.getenv("NOTION_API_KEY")
    notion_page_id = os.getenv("NOTION_PAGE_ID")
    
    if notion_token:
        print("✅ NOTION_API_KEY found")
    else:
        print("❌ NOTION_API_KEY not found")
        return False
    
    if notion_page_id:
        print("✅ NOTION_PAGE_ID found")
    else:
        print("❌ NOTION_PAGE_ID not found")
        return False
    
    return True

def test_notion_api_connection():
    """Test Notion API connectivity."""
    print("🔗 Testing Notion API connection...")
    
    try:
        from notifier.notion import send_to_notion
        
        # Test sending a simple message
        success = send_to_notion(
            page_id=os.getenv("NOTION_PAGE_ID"),
            title="🧪 Test Message",
            summary="This is a test message from Competitor Feature Tracker"
        )
        
        if success:
            print("✅ Notion API connection successful")
            return True
        else:
            print("❌ Notion API connection failed")
            return False
            
    except Exception as e:
        print(f"❌ Notion API error: {e}")
        return False

def test_notion_database():
    """Test Notion database functionality."""
    print("📊 Testing Notion database...")
    
    try:
        from notifier.notion import send_to_notion_database
        
        # Test sending to database (if database ID is configured)
        database_id = os.getenv("NOTION_DATABASE_ID")
        if database_id:
            success = send_to_notion_database(
                database_id=database_id,
                title="🧪 Test Database Entry",
                summary="This is a test database entry",
                source_type="test"
            )
            
            if success:
                print("✅ Notion database integration working")
                return True
            else:
                print("❌ Notion database integration failed")
                return False
        else:
            print("⚠️  NOTION_DATABASE_ID not configured - skipping database test")
            return True
            
    except Exception as e:
        print(f"❌ Notion database error: {e}")
        return False

def test_notion_page_structure():
    """Test if the Notion page has the correct structure."""
    print("📄 Testing Notion page structure...")
    
    try:
        import requests
        
        notion_token = os.getenv("NOTION_API_KEY")
        page_id = os.getenv("NOTION_PAGE_ID")
        
        url = f"https://api.notion.com/v1/pages/{page_id}"
        headers = {
            "Authorization": f"Bearer {notion_token}",
            "Notion-Version": "2022-06-28"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            page_data = response.json()
            page_title = page_data.get("properties", {}).get("title", {}).get("title", [])
            
            if page_title:
                print(f"✅ Notion page accessible: {page_title[0].get('text', {}).get('content', 'Untitled')}")
            else:
                print("✅ Notion page accessible (no title)")
            
            return True
        else:
            print(f"❌ Notion page access failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Notion page structure error: {e}")
        return False

def main():
    """Run all Notion tests."""
    print("🧪 Notion API Test Suite")
    print("=" * 40)
    
    # Test credentials first
    if not test_notion_credentials():
        print("\n❌ Notion credentials not configured. Please check your .env file.")
        return False
    
    print()
    
    # Test API connection
    api_success = test_notion_api_connection()
    print()
    
    # Test page structure
    page_success = test_notion_page_structure()
    print()
    
    # Test database (optional)
    db_success = test_notion_database()
    print()
    
    # Summary
    print("=" * 40)
    print("📊 Notion Test Results:")
    print(f"   API Connection: {'✅ Working' if api_success else '❌ Failed'}")
    print(f"   Page Access: {'✅ Working' if page_success else '❌ Failed'}")
    print(f"   Database: {'✅ Working' if db_success else '⚠️  Not configured'}")
    
    if api_success and page_success:
        print("\n🎉 Notion integration ready!")
        return True
    else:
        print("\n⚠️  Notion integration needs configuration")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 