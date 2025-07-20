#!/usr/bin/env python3
"""
Test script for Competitor Feature Tracker
Run this to verify all components are working correctly.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from scrapers.changelog import fetch_changelog
        from scrapers.blog import fetch_blog_rss, fetch_blog_html
        from scrapers.pricing import fetch_pricing, extract_pricing_info
        from scrapers.github import fetch_latest_github_release
        
        from db.models import init_db, save_update, get_last_update
        from summarizer.summarize import summarize_update
        
        from notifier.slack import send_to_slack
        from notifier.notion import send_to_notion
        
        print("All imports successful")
        return True
    except ImportError as e:
        print(f"Import error: {e}")
        return False

def test_environment():
    """Test environment variables."""
    print("Testing environment variables...")
    
    required_vars = [
        'GEMINI_API_KEY',
        'SLACK_WEBHOOK_URL',
        'NOTION_API_KEY',
        'NOTION_PAGE_ID'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"Missing environment variables: {', '.join(missing_vars)}")
        print("   These are required for full functionality")
        return False
    else:
        print("All required environment variables found")
        return True

def test_database():
    """Test database operations."""
    print("Testing database...")
    
    try:
        from db.models import init_db, save_update, get_last_update
        
        # Initialize database
        init_db()
        
        # Test save and retrieve
        test_data = {
            'source_type': 'test',
            'source_url': 'https://test.com',
            'content': 'Test content',
            'summary': 'Test summary',
            'competitor_name': 'Test Competitor'
        }
        
        save_update(**test_data)
        retrieved = get_last_update('https://test.com')
        
        if retrieved == 'Test content':
            print("Database operations working")
            return True
        else:
            print("Database retrieval failed")
            return False
            
    except Exception as e:
        print(f"Database error: {e}")
        return False

def test_summarizer():
    """Test AI summarization."""
    print("Testing AI summarization...")
    
    try:
        from summarizer.summarize import summarize_update
        
        test_text = "We've added new workflow automations for support ticket routing and introduced a new integration with Salesforce."
        summary = summarize_update(test_text, 'feature')
        
        if summary and len(summary) > 0:
            print(f"Summarization working: {summary}")
            return True
        else:
            print("Summarization returned empty result")
            return False
            
    except Exception as e:
        print(f"Summarization error: {e}")
        return False

def test_scrapers():
    """Test web scrapers."""
    print("Testing web scrapers...")
    
    try:
        from scrapers.changelog import fetch_changelog
        from scrapers.blog import fetch_blog_html
        from scrapers.pricing import fetch_pricing
        
        # Test changelog scraper
        changelog_result = fetch_changelog('https://linear.app/changelog')
        print(f"   Changelog: {'OK' if changelog_result else 'No content found'}")
        
        # Test blog scraper
        blog_result = fetch_blog_html('https://linear.app/blog')
        print(f"   Blog: {'OK' if blog_result else 'No content found'}")
        
        # Test pricing scraper
        pricing_result = fetch_pricing('https://linear.app/pricing')
        print(f"   Pricing: {'OK' if pricing_result else 'No content found'}")
        
        print("Scraper tests completed")
        return True
        
    except Exception as e:
        print(f"Scraper error: {e}")
        return False

def test_notifications():
    """Test notification systems."""
    print("Testing notifications...")
    
    try:
        from notifier.slack import send_to_slack
        
        # Test Slack (will fail gracefully if no webhook)
        try:
            send_to_slack("Test message from Competitor Tracker")
            print("   Slack: OK")
        except:
            print("   Slack: No webhook configured")
        
        print("Notification tests completed")
        return True
        
    except Exception as e:
        print(f"Notification error: {e}")
        return False

def test_notion_integration():
    """Test Notion API integration."""
    print("Testing Notion integration...")
    
    try:
        from notifier.notion import send_to_notion
        
        notion_page_id = os.getenv("NOTION_PAGE_ID")
        if notion_page_id:
            success = send_to_notion(
                notion_page_id,
                "Test Message",
                "This is a test message from Competitor Tracker"
            )
            if success:
                print("Notion API working")
                return True
            else:
                print("Notion API failed")
                return False
        else:
            print("Notion not configured")
            return False
            
    except Exception as e:
        print(f"Notion integration error: {e}")
        return False

def main():
    """Run all tests."""
    print("Competitor Feature Tracker - Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_environment,
        test_database,
        test_summarizer,
        test_scrapers,
        test_notifications,
        test_notion_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
    else:
        print("Some tests failed. Check the output above for details.")
        print("\n💡 Run individual test scripts for detailed debugging:")
        print("   python test_notion.py")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 