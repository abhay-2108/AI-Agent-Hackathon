#!/usr/bin/env python3
"""
Competitor Feature Tracker - Main Workflow
Automatically monitors and summarizes competitor updates from multiple sources.
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Import scrapers
from scrapers.changelog import fetch_changelog
from scrapers.blog import fetch_blog_rss, fetch_blog_html
from scrapers.pricing import fetch_pricing, extract_pricing_info
from scrapers.github import fetch_latest_github_release, fetch_github_commits

# Import core modules
from db.models import init_db, save_update, get_last_update, get_weekly_updates
from summarizer.summarize import summarize_update

# Import notifiers
from notifier.slack import send_to_slack
from notifier.notion import send_to_notion, send_to_notion_database

# Load environment variables
load_dotenv()

class CompetitorTracker:
    def __init__(self):
        """Initialize the competitor tracker."""
        self.updates_found = []
        self.competitors = {
            'linear': {
                'name': 'Linear',
                'changelog': 'https://linear.app/changelog',
                'blog': 'https://linear.app/blog',
                'pricing': 'https://linear.app/pricing',
                'github': {'owner': 'linear', 'repo': 'linear'}
            },
            'notion': {
                'name': 'Notion',
                'blog': 'https://www.notion.so/blog',
                'pricing': 'https://www.notion.so/pricing'
            },
            'figma': {
                'name': 'Figma',
                'changelog': 'https://www.figma.com/changelog',
                'blog': 'https://www.figma.com/blog',
                'pricing': 'https://www.figma.com/pricing'
            }
        }
    
    def track_changelogs(self):
        """Track changelog updates from competitors."""
        print("Tracking changelogs...")
        
        for competitor_id, competitor in self.competitors.items():
            if 'changelog' in competitor:
                try:
                    latest_entry = fetch_changelog(competitor['changelog'])
                    if latest_entry:
                        last_entry = get_last_update(competitor['changelog'])
                        
                        if latest_entry != last_entry:
                            summary = summarize_update(latest_entry, 'changelog')
                            save_update(
                                source_type='changelog',
                                source_url=competitor['changelog'],
                                content=latest_entry,
                                summary=summary,
                                competitor_name=competitor['name']
                            )
                            self.updates_found.append({
                                'source': f"{competitor['name']} Changelog",
                                'summary': summary,
                                'content': latest_entry,
                                'previous_content': last_entry,
                                'source_url': competitor['changelog']
                            })
                            
                            print(f"New changelog update from {competitor['name']}")
                        else:
                            print(f"No new changelog updates from {competitor['name']}")
                            
                except Exception as e:
                    print(f"Error tracking {competitor['name']} changelog: {e}")
    
    def track_blogs(self):
        """Track blog updates from competitors."""
        print("Tracking blogs...")
        
        for competitor_id, competitor in self.competitors.items():
            if 'blog' in competitor:
                try:
                    # Try RSS first, then HTML
                    latest_post = fetch_blog_rss(competitor['blog'])
                    if not latest_post:
                        latest_post = fetch_blog_html(competitor['blog'])
                    
                    if latest_post:
                        last_post = get_last_update(competitor['blog'])
                        
                        if latest_post != last_post:
                            summary = summarize_update(latest_post, 'blog')
                            save_update(
                                source_type='blog',
                                source_url=competitor['blog'],
                                content=latest_post,
                                summary=summary,
                                competitor_name=competitor['name']
                            )
                            self.updates_found.append({
                                'source': f"{competitor['name']} Blog",
                                'summary': summary,
                                'content': latest_post,
                                'previous_content': last_post,
                                'source_url': competitor['blog']
                            })
                            
                            print(f"New blog post from {competitor['name']}")
                        else:
                            print(f"No new blog posts from {competitor['name']}")
                            
                except Exception as e:
                    print(f"Error tracking {competitor['name']} blog: {e}")
    
    def track_pricing(self):
        """Track pricing page changes."""
        print("Tracking pricing changes...")
        
        for competitor_id, competitor in self.competitors.items():
            if 'pricing' in competitor:
                try:
                    pricing_content = fetch_pricing(competitor['pricing'])
                    if pricing_content:
                        pricing_info = extract_pricing_info(pricing_content)
                        last_pricing = get_last_update(competitor['pricing'])
                        
                        if pricing_info != last_pricing:
                            summary = summarize_update(pricing_info, 'pricing')
                            save_update(
                                source_type='pricing',
                                source_url=competitor['pricing'],
                                content=pricing_content,
                                summary=summary,
                                competitor_name=competitor['name']
                            )
                            self.updates_found.append({
                                'source': f"{competitor['name']} Pricing",
                                'summary': summary,
                                'content': pricing_info,
                                'previous_content': last_pricing,
                                'source_url': competitor['pricing']
                            })
                            
                            print(f"New pricing update from {competitor['name']}")
                        else:
                            print(f"No pricing changes from {competitor['name']}")
                            
                except Exception as e:
                    print(f"Error tracking {competitor['name']} pricing: {e}")
    
    def track_github(self):
        """Track GitHub releases and commits."""
        print("Tracking GitHub updates...")
        
        for competitor_id, competitor in self.competitors.items():
            if 'github' in competitor:
                try:
                    github_info = competitor['github']
                    latest_release = fetch_latest_github_release(
                        github_info['owner'], 
                        github_info['repo']
                    )
                    
                    if latest_release:
                        last_release = get_last_update(f"github://{github_info['owner']}/{github_info['repo']}")
                        
                        if latest_release != last_release:
                            summary = summarize_update(latest_release, 'github')
                            save_update(
                                source_type='github',
                                source_url=f"github://{github_info['owner']}/{github_info['repo']}",
                                content=latest_release,
                                summary=summary,
                                competitor_name=competitor['name']
                            )
                            self.updates_found.append({
                                'source': f"{competitor['name']} GitHub",
                                'summary': summary,
                                'content': latest_release,
                                'previous_content': last_release,
                                'source_url': f"https://github.com/{github_info['owner']}/{github_info['repo']}/releases"
                            })
                            
                            print(f"New GitHub release from {competitor['name']}")
                        else:
                            print(f"No new GitHub releases from {competitor['name']}")
                            
                except Exception as e:
                    print(f"Error tracking {competitor['name']} GitHub: {e}")
    
    def send_notifications(self):
        """Send notifications for all found updates."""
        if not self.updates_found:
            print("No updates to notify about")
            return
        
        print(f"Sending notifications for {len(self.updates_found)} updates...")
        
        # Send to Slack
        from notifier.slack import send_to_slack
        for update in self.updates_found:
            # Create enhanced update data
            update_data = {
                'competitor_name': update['source'].split()[0],  # Extract competitor name
                'source_type': update['source'].split()[-1].lower(),  # Extract source type
                'summary': update['summary'],
                'content': update['content'],
                'previous_content': update.get('previous_content', ''),
                'source_url': update.get('source_url', '')
            }
            send_to_slack(None, update_data)
        
        # Send to Notion
        notion_page_id = os.getenv("NOTION_PAGE_ID")
        if notion_page_id:
            from notifier.notion import send_to_notion
            for update in self.updates_found:
                update_data = {
                    'competitor_name': update['source'].split()[0],
                    'source_type': update['source'].split()[-1].lower(),
                    'summary': update['summary'],
                    'content': update['content'],
                    'previous_content': update.get('previous_content', ''),
                    'source_url': update.get('source_url', '')
                }
                send_to_notion(
                    notion_page_id,
                    f"Competitor Update: {update['source']}",
                    update['summary'],
                    update_data=update_data
                )
        
        # Send to Email
        email_recipient = os.getenv("EMAIL_TO", os.getenv("EMAIL_FROM"))
        if email_recipient:
            from notifier.email import send_email
            for update in self.updates_found:
                update_data = {
                    'competitor_name': update['source'].split()[0],
                    'source_type': update['source'].split()[-1].lower(),
                    'summary': update['summary'],
                    'content': update['content'],
                    'previous_content': update.get('previous_content', ''),
                    'source_url': update.get('source_url', '')
                }
                send_email(
                    recipient=email_recipient,
                    subject=f"Competitor Update: {update['source']}",
                    message=update['summary'],
                    update_data=update_data
                )
    
    def run_weekly_digest(self):
        """Generate weekly digest of all updates."""
        print("Generating weekly digest...")
        
        weekly_updates = get_weekly_updates()
        if weekly_updates:
            print(f"Found {len(weekly_updates)} updates in the last week")
            
            # Convert database format to notification format
            formatted_updates = []
            for update in weekly_updates:
                formatted_updates.append({
                    'competitor_name': update['competitor_name'],
                    'source_type': update['source_type'],
                    'summary': update['summary'],
                    'content': update.get('content', ''),
                    'previous_content': update.get('previous_content', ''),
                    'source_url': update.get('source_url', '')
                })
            
            # Send digest to Slack
            from notifier.slack import send_slack_digest
            send_slack_digest(formatted_updates)
            
            # Send digest to Notion
            notion_page_id = os.getenv("NOTION_PAGE_ID")
            if notion_page_id:
                from notifier.notion import send_notion_digest
                send_notion_digest(notion_page_id, formatted_updates)
            
            # Send digest to Email
            email_recipient = os.getenv("EMAIL_TO", os.getenv("EMAIL_FROM"))
            if email_recipient:
                from notifier.email import send_email_digest
                send_email_digest(email_recipient, formatted_updates)
        else:
            print("No updates in the last week for digest")
    
    def run(self, digest_only=False):
        """Run the complete competitor tracking workflow."""
        print(f"Starting Competitor Feature Tracker at {datetime.now()}")
        
        # Initialize database
        init_db()
        
        if digest_only:
            self.run_weekly_digest()
            return
        
        # Track all sources
        self.track_changelogs()
        self.track_blogs()
        self.track_pricing()
        self.track_github()
        
        # Send notifications
        self.send_notifications()
        
        print(f"Competitor tracking completed. Found {len(self.updates_found)} updates.")

def run_tracker(email=None):
    """Run the competitor tracker, optionally overriding the email recipient."""
    if email:
        os.environ["EMAIL_TO"] = email
    tracker = CompetitorTracker()
    tracker.run()

def main():
    """Main entry point."""
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "digest":
            tracker = CompetitorTracker()
            tracker.run(digest_only=True)
        elif sys.argv[1] == "test":
            print("Running in test mode...")
            # Add test functionality here
        elif sys.argv[1] == "--email" and len(sys.argv) > 2:
            run_tracker(email=sys.argv[2])
        else:
            print("Usage: python main.py [digest|test|--email you@example.com]")
    else:
        run_tracker()

if __name__ == "__main__":
    main() 