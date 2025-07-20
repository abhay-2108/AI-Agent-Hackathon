#!/usr/bin/env python3
"""
Setup script for Competitor Feature Tracker
Helps users configure environment variables and test the system.
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """Create a .env file with placeholder values."""
    env_content = """# API Keys - Replace with your actual keys
GEMINI_API_KEY=your_gemini_api_key_here
SLACK_WEBHOOK_URL=your_slack_webhook_url_here
NOTION_API_KEY=your_notion_api_key_here
NOTION_PAGE_ID=your_notion_page_id_here

# GitHub API (Optional - for higher rate limits)
GITHUB_TOKEN=your_github_token_here

# Competitor URLs to track
LINEAR_CHANGELOG=https://linear.app/changelog
NOTION_BLOG=https://www.notion.so/blog
INTERCOM_CHANGELOG=https://www.intercom.com/changelog
FIGMA_CHANGELOG=https://www.figma.com/changelog

# GitHub Repos to track
GITHUB_OWNER=linear
GITHUB_REPO=linear
"""
    
    env_path = Path(".env")
    if env_path.exists():
        print("⚠️  .env file already exists. Skipping creation.")
        return False
    
    try:
        with open(env_path, "w") as f:
            f.write(env_content)
        print("✅ Created .env file with placeholder values")
        print("📝 Please edit .env file with your actual API keys")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def check_dependencies():
    """Check if all required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        "requests", "beautifulsoup4", "feedparser", 
        "google-generativeai", "slack_sdk", "python-dotenv", "schedule"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
            print("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            return False
    
    return True

def test_system():
    """Run a quick test of the system."""
    print("\n🧪 Testing system...")
    
    try:
        # Test imports
        from scrapers.changelog import fetch_changelog
        from scrapers.blog import fetch_blog_html
        from scrapers.pricing import fetch_pricing
        from db.models import init_db
        from summarizer.summarize import summarize_update
        print("✅ All modules imported successfully")
        
        # Test database
        init_db()
        print("✅ Database initialized successfully")
        
        # Test basic scraping
        test_url = "https://linear.app/changelog"
        result = fetch_changelog(test_url)
        if result:
            print("✅ Web scraping working")
        else:
            print("⚠️  Web scraping returned no results (this might be normal)")
        
        return True
        
    except Exception as e:
        print(f"❌ System test failed: {e}")
        return False

def show_next_steps():
    """Show next steps for the user."""
    print("\n🎯 Next Steps:")
    print("1. Edit .env file with your API keys:")
    print("   - GEMINI_API_KEY: Get from https://makersuite.google.com/app/apikey")
    print("   - SLACK_WEBHOOK_URL: Create webhook in your Slack workspace")
    print("   - NOTION_API_KEY: Get from https://www.notion.so/my-integrations")
    print("   - NOTION_PAGE_ID: Copy from your Notion page URL")
    print("   - GITHUB_TOKEN: Optional, for higher rate limits")
    print("   - DISABLE_GEMINI_API: Set to 'true' to use fallback summarization only")
    
    print("\n💡 Rate Limiting Tips:")
    print("   - Free Gemini API has strict rate limits (60 requests/minute)")
    print("   - The system automatically waits 30 seconds between requests")
    print("   - Set DISABLE_GEMINI_API=true in .env to avoid rate limits entirely")
    print("   - Set SKIP_RATE_LIMIT_WAIT=true in .env to skip waiting on rate limits")
    print("   - Press Ctrl+C during rate limit waits to skip them")
    print("   - Fallback summarization works without API keys")
    
    print("\n2. Test the system:")
    print("   python test_tracker.py")
    
    print("\n3. Run the tracker:")
    print("   python main.py")
    
    print("\n4. Start the scheduler:")
    print("   python scheduler/job_scheduler.py")
    
    print("\n5. For help:")
    print("   python scheduler/job_scheduler.py help")

def main():
    """Main setup function."""
    print("🚀 Competitor Feature Tracker Setup")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Setup failed due to dependency issues")
        return False
    
    # Create .env file
    env_created = create_env_file()
    
    # Test system
    if not test_system():
        print("❌ Setup failed due to system test issues")
        return False
    
    # Show next steps
    show_next_steps()
    
    print("\n✅ Setup completed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 