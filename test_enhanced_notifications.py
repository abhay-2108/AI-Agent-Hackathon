#!/usr/bin/env python3
"""
Test script to demonstrate enhanced notification formatting
"""

import os
from notifier.formatters import MessageFormatter

def test_enhanced_formatting():
    """Test the enhanced notification formatting."""
    print("🧪 Testing Enhanced Notification Formatting")
    print("=" * 60)
    
    # Create sample update data
    sample_update = {
        'competitor_name': 'Linear',
        'source_type': 'changelog',
        'summary': '🚀 **New Feature: Enhanced Workflow Automation**\n\nWe\'ve added powerful new workflow automation features to help teams work more efficiently:\n\n• **Automated task assignment** based on workload and expertise\n• **Smart notification routing** for support tickets\n• **Integration with popular CRM systems** including Salesforce and HubSpot\n• **Advanced reporting and analytics dashboard** with real-time insights\n\nThese improvements will save teams up to 3 hours per week on manual tasks and improve overall productivity.',
        'content': 'We\'ve added powerful new workflow automation features to help teams work more efficiently. The new system includes automated task assignment based on workload and expertise, smart notification routing for support tickets, integration with popular CRM systems including Salesforce and HubSpot, and an advanced reporting and analytics dashboard with real-time insights. These improvements will save teams up to 3 hours per week on manual tasks and improve overall productivity.',
        'source_url': 'https://linear.app/changelog'
    }
    
    sample_updates = [
        {
            'competitor_name': 'Linear',
            'source_type': 'changelog',
            'summary': '🚀 **New Feature: Enhanced Workflow Automation**\n\nWe\'ve added powerful new workflow automation features to help teams work more efficiently.',
            'content': 'We\'ve added powerful new workflow automation features to help teams work more efficiently.',
            'source_url': 'https://linear.app/changelog'
        },
        {
            'competitor_name': 'Notion',
            'source_type': 'blog',
            'summary': '📝 **New Blog Post: The Future of Team Collaboration**\n\nExploring how AI and automation are transforming the way teams work together.',
            'content': 'Exploring how AI and automation are transforming the way teams work together.',
            'source_url': 'https://www.notion.so/blog'
        },
        {
            'competitor_name': 'Figma',
            'source_type': 'pricing',
            'summary': '💰 **Pricing Update: New Enterprise Features**\n\nIntroducing advanced collaboration tools and enhanced security features for enterprise customers.',
            'content': 'Introducing advanced collaboration tools and enhanced security features for enterprise customers.',
            'source_url': 'https://www.figma.com/pricing'
        }
    ]
    
    formatter = MessageFormatter()
    
    # Test 1: Slack formatting
    print("\n1. 📱 Slack Message Formatting")
    print("-" * 40)
    slack_message = formatter.format_slack_message(sample_update)
    print(slack_message)
    
    # Test 2: Slack digest formatting
    print("\n2. 📱 Slack Digest Formatting")
    print("-" * 40)
    slack_digest = formatter.format_slack_digest(sample_updates)
    print(slack_digest)
    
    # Test 3: Notion formatting
    print("\n3. 📄 Notion Page Formatting")
    print("-" * 40)
    notion_content = formatter.format_notion_page(sample_update)
    print(notion_content)
    
    # Test 4: Notion digest formatting
    print("\n4. 📄 Notion Digest Formatting")
    print("-" * 40)
    notion_digest = formatter.format_notion_digest(sample_updates)
    print(notion_digest)
    
    # Test 5: Email formatting (HTML preview)
    print("\n5. 📧 Email HTML Formatting (Preview)")
    print("-" * 40)
    email_html = formatter.format_email_message(sample_update)
    print("HTML content generated (showing first 500 chars):")
    print(email_html[:500] + "..." if len(email_html) > 500 else email_html)
    
    # Test 6: Email digest formatting (HTML preview)
    print("\n6. 📧 Email Digest Formatting (Preview)")
    print("-" * 40)
    email_digest_html = formatter.format_email_digest(sample_updates)
    print("HTML digest content generated (showing first 500 chars):")
    print(email_digest_html[:500] + "..." if len(email_digest_html) > 500 else email_digest_html)
    
    # Test 7: Platform-specific titles
    print("\n7. 🏷️ Platform-Specific Titles")
    print("-" * 40)
    for platform in ['slack', 'notion', 'email']:
        title = formatter.get_platform_specific_title(sample_update, platform)
        print(f"{platform.title()}: {title}")
    
    print("\n✅ Enhanced formatting tests completed!")
    print("\n💡 Features demonstrated:")
    print("- Rich formatting with emojis and markdown")
    print("- Platform-specific optimizations")
    print("- HTML email templates with styling")
    print("- Digest formatting with grouping by competitor")
    print("- Source URL integration")
    print("- Timestamp and metadata inclusion")

if __name__ == "__main__":
    test_enhanced_formatting() 