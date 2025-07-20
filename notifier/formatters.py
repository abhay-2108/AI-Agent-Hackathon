# notifier/formatters.py

import os
from datetime import datetime
from typing import Dict, List, Optional

class MessageFormatter:
    """Formats competitor updates for different notification platforms."""
    
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def format_slack_message(self, update: Dict) -> str:
        """Format a single update for Slack with rich formatting."""
        competitor = update.get('competitor_name', 'Unknown')
        source_type = update.get('source_type', 'update')
        summary = update.get('summary', '')
        content = update.get('content', '')
        previous_content = update.get('previous_content', '')
        source_url = update.get('source_url', '')
        
        # Determine emoji based on source type
        emoji_map = {
            'changelog': '🆕',
            'blog': '📝',
            'pricing': '💰',
            'github': '🐙',
            'social': '📱',
            'update': '📢'
        }
        emoji = emoji_map.get(source_type.lower(), '📢')
        
        # Format the message
        message = f"{emoji} *{competitor} {source_type.title()} Update*\n"
        message += f"*Posted:* {self.timestamp}\n"
        message += f"*Source:* {source_type.title()}\n"
        
        if source_url:
            message += f"*Link:* <{source_url}|View Original>\n"
        
        message += "\n*Summary:*\n"
        message += summary
        
        # Add before/after comparison if previous_content is available
        if previous_content and previous_content != content:
            message += f"\n\n*Before:*\n{previous_content[:500]}"
            message += f"\n*After:*\n{content[:500]}"
        # Add content preview if available and different from summary
        elif content and content != summary and len(content) > 50:
            content_preview = content[:300] + "..." if len(content) > 300 else content
            message += f"\n\n*Content Preview:*\n{content_preview}"
        
        return message
    
    def format_slack_digest(self, updates: List[Dict]) -> str:
        """Format multiple updates as a digest for Slack."""
        if not updates:
            return "No updates found for this period."
        
        message = f"📊 *Weekly Competitor Update Digest*\n"
        message += f"*Period:* {self.timestamp}\n"
        message += f"*Total Updates:* {len(updates)}\n\n"
        
        # Group by competitor
        competitors = {}
        for update in updates:
            competitor = update.get('competitor_name', 'Unknown')
            if competitor not in competitors:
                competitors[competitor] = []
            competitors[competitor].append(update)
        
        for competitor, competitor_updates in competitors.items():
            message += f"*{competitor}* ({len(competitor_updates)} updates):\n"
            
            for i, update in enumerate(competitor_updates, 1):
                source_type = update.get('source_type', 'update')
                summary = update.get('summary', '')
                content = update.get('content', '')
                previous_content = update.get('previous_content', '')
                
                # Truncate summary for digest
                summary_preview = summary[:150] + "..." if len(summary) > 150 else summary
                message += f"  {i}. *{source_type.title()}:* {summary_preview}\n"
                
                # Add before/after comparison if previous_content is available
                if previous_content and previous_content != content:
                    message += f"    *Before:*\n{previous_content[:100]}\n"
                    message += f"    *After:*\n{content[:100]}\n"
                
                message += "\n"
        
        return message
    
    def format_notion_page(self, update: Dict) -> str:
        """Format an update for Notion page with rich formatting."""
        competitor = update.get('competitor_name', 'Unknown')
        source_type = update.get('source_type', 'update')
        summary = update.get('summary', '')
        content = update.get('content', '')
        previous_content = update.get('previous_content', '')
        source_url = update.get('source_url', '')
        
        # Create rich Notion content
        notion_content = f"# {competitor} {source_type.title()} Update\n\n"
        notion_content += f"**Posted:** {self.timestamp}\n"
        notion_content += f"**Source Type:** {source_type.title()}\n"
        
        if source_url:
            notion_content += f"**Source URL:** {source_url}\n"
        
        notion_content += "\n## Summary\n\n"
        notion_content += summary
        
        # Add before/after comparison if previous_content is available
        if previous_content and previous_content != content:
            notion_content += f"\n\n## Before\n\n{previous_content[:1000]}"
            notion_content += f"\n\n## After\n\n{content[:1000]}"
        elif content and content != summary:
            notion_content += f"\n\n## Full Content\n\n"
            notion_content += content
        
        return notion_content
    
    def format_notion_digest(self, updates: List[Dict]) -> str:
        """Format multiple updates as a digest for Notion."""
        if not updates:
            return "No updates found for this period."
        
        notion_content = f"# Weekly Competitor Update Digest\n\n"
        notion_content += f"**Period:** {self.timestamp}\n"
        notion_content += f"**Total Updates:** {len(updates)}\n\n"
        
        # Group by competitor
        competitors = {}
        for update in updates:
            competitor = update.get('competitor_name', 'Unknown')
            if competitor not in competitors:
                competitors[competitor] = []
            competitors[competitor].append(update)
        
        for competitor, competitor_updates in competitors.items():
            notion_content += f"## {competitor} ({len(competitor_updates)} updates)\n\n"
            
            for i, update in enumerate(competitor_updates, 1):
                source_type = update.get('source_type', 'update')
                summary = update.get('summary', '')
                content = update.get('content', '')
                previous_content = update.get('previous_content', '')
                source_url = update.get('source_url', '')
                
                notion_content += f"### {i}. {source_type.title()} Update\n\n"
                notion_content += summary
                
                if source_url:
                    notion_content += f"\n\n**Source:** {source_url}\n"
                
                # Add before/after comparison if previous_content is available
                if previous_content and previous_content != content:
                    notion_content += f"\n\n## Before\n\n{previous_content[:1000]}"
                    notion_content += f"\n\n## After\n\n{content[:1000]}"
                
                notion_content += "\n---\n\n"
        
        return notion_content
    
    def format_email_message(self, update: Dict) -> str:
        """Format an update for email with HTML and plain text support."""
        competitor = update.get('competitor_name', 'Unknown')
        source_type = update.get('source_type', 'update')
        summary = update.get('summary', '')
        content = update.get('content', '')
        previous_content = update.get('previous_content', '')
        source_url = update.get('source_url', '')
        
        # HTML version
        html_message = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px 8px 0 0;">
                <h1 style="margin: 0; font-size: 24px;">{competitor} {source_type.title()} Update</h1>
                <p style="margin: 5px 0 0 0; opacity: 0.9;">Posted on {self.timestamp}</p>
            </div>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 0 0 8px 8px; border: 1px solid #e9ecef;">
                <div style="background: white; padding: 20px; border-radius: 6px; margin-bottom: 20px;">
                    <h2 style="color: #495057; margin-top: 0;">Summary</h2>
                    <div style="line-height: 1.6; color: #212529;">
                        {summary.replace(chr(10), '<br>')}
                    </div>
                </div>
        """
        
        if source_url:
            html_message += f"""
                <div style="text-align: center; margin: 20px 0;">
                    <a href="{source_url}" style="background: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                        View Original Source
                    </a>
                </div>
            """
        
        # Add before/after comparison if previous_content is available
        if previous_content and previous_content != content:
            html_message += f"""
                <div style="background: white; padding: 20px; border-radius: 6px;">
                    <h2 style="color: #495057; margin-top: 0;">Before</h2>
                    <div style="line-height: 1.6; color: #212529; white-space: pre-wrap;">{previous_content[:1000].replace(chr(10), '<br>')}</div>
                </div>
                <div style="background: white; padding: 20px; border-radius: 6px;">
                    <h2 style="color: #495057; margin-top: 0;">After</h2>
                    <div style="line-height: 1.6; color: #212529; white-space: pre-wrap;">{content[:1000].replace(chr(10), '<br>')}</div>
                </div>
            """
        elif content and content != summary:
            html_message += f"""
                <div style="background: white; padding: 20px; border-radius: 6px;">
                    <h2 style="color: #495057; margin-top: 0;">Full Content</h2>
                    <div style="line-height: 1.6; color: #212529; white-space: pre-wrap;">{content.replace(chr(10), '<br>')}</div>
                </div>
            """
        
        html_message += """
            </div>
            
            <div style="text-align: center; margin-top: 20px; color: #6c757d; font-size: 12px;">
                <p>This update was automatically generated by the Competitor Feature Tracker.</p>
            </div>
        </div>
        """
        
        return html_message
    
    def format_email_digest(self, updates: List[Dict]) -> str:
        """Format multiple updates as a digest for email."""
        if not updates:
            return "No updates found for this period."
        
        # HTML version
        html_message = f"""
        <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 8px 8px 0 0;">
                <h1 style="margin: 0; font-size: 28px;">Weekly Competitor Update Digest</h1>
                <p style="margin: 10px 0 0 0; opacity: 0.9;">Period: {self.timestamp}</p>
                <p style="margin: 5px 0 0 0; opacity: 0.9;">Total Updates: {len(updates)}</p>
            </div>
            
            <div style="background: #f8f9fa; padding: 30px; border-radius: 0 0 8px 8px; border: 1px solid #e9ecef;">
        """
        
        # Group by competitor
        competitors = {}
        for update in updates:
            competitor = update.get('competitor_name', 'Unknown')
            if competitor not in competitors:
                competitors[competitor] = []
            competitors[competitor].append(update)
        
        for competitor, competitor_updates in competitors.items():
            html_message += f"""
                <div style="background: white; padding: 20px; border-radius: 6px; margin-bottom: 20px;">
                    <h2 style="color: #495057; margin-top: 0; border-bottom: 2px solid #007bff; padding-bottom: 10px;">
                        {competitor} ({len(competitor_updates)} updates)
                    </h2>
            """
            
            for i, update in enumerate(competitor_updates, 1):
                source_type = update.get('source_type', 'update')
                summary = update.get('summary', '')
                content = update.get('content', '')
                previous_content = update.get('previous_content', '')
                source_url = update.get('source_url', '')
                
                html_message += f"""
                    <div style="margin-bottom: 20px; padding: 15px; background: #f8f9fa; border-radius: 4px;">
                        <h3 style="color: #495057; margin-top: 0; font-size: 16px;">
                            {i}. {source_type.title()} Update
                        </h3>
                        <div style="line-height: 1.6; color: #212529; margin-bottom: 10px;">
                            {summary.replace(chr(10), '<br>')}
                        </div>
                """
                
                # Add before/after comparison if previous_content is available
                if previous_content and previous_content != content:
                    html_message += f"""
                        <div style="margin-top: 10px; padding: 10px; background: #e9ecef; border-radius: 4px;">
                            <h4 style="color: #6c757d; margin-top: 0; font-size: 14px;">Before</h4>
                            <div style="line-height: 1.6; color: #212529; white-space: pre-wrap;">{previous_content[:1000].replace(chr(10), '<br>')}</div>
                        </div>
                        <div style="margin-top: 10px; padding: 10px; background: #e9ecef; border-radius: 4px;">
                            <h4 style="color: #6c757d; margin-top: 0; font-size: 14px;">After</h4>
                            <div style="line-height: 1.6; color: #212529; white-space: pre-wrap;">{content[:1000].replace(chr(10), '<br>')}</div>
                        </div>
                    """
                
                if source_url:
                    html_message += f"""
                        <a href="{source_url}" style="color: #007bff; text-decoration: none; font-size: 14px;">
                            View Original Source →
                        </a>
                    """
                
                html_message += "</div>"
            
            html_message += "</div>"
        
        html_message += """
            </div>
            
            <div style="text-align: center; margin-top: 20px; color: #6c757d; font-size: 12px;">
                <p>This digest was automatically generated by the Competitor Feature Tracker.</p>
            </div>
        </div>
        """
        
        return html_message
    
    def get_platform_specific_title(self, update: Dict, platform: str) -> str:
        """Get platform-specific title for the update."""
        competitor = update.get('competitor_name', 'Unknown')
        source_type = update.get('source_type', 'update')
        
        if platform == 'slack':
            return f"{competitor} {source_type.title()} Update"
        elif platform == 'notion':
            return f"{competitor} {source_type.title()} Update - {self.timestamp}"
        elif platform == 'email':
            return f"Competitor Update: {competitor} {source_type.title()}"
        else:
            return f"Competitor Update: {competitor} {source_type.title()}"
    
    def get_digest_title(self, platform: str) -> str:
        """Get platform-specific title for digest."""
        if platform == 'slack':
            return "Weekly Competitor Update Digest"
        elif platform == 'notion':
            return f"Weekly Digest - {self.timestamp}"
        elif platform == 'email':
            return f"Weekly Competitor Digest - {self.timestamp}"
        else:
            return f"Weekly Competitor Digest - {self.timestamp}" 