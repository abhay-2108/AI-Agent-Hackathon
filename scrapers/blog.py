# scrapers/blog.py

import feedparser
import requests
from bs4 import BeautifulSoup
import os

def fetch_blog_rss(rss_url):
    """
    Fetch the latest blog post from an RSS feed.
    """
    try:
        feed = feedparser.parse(rss_url)
        if feed.entries:
            # Return the latest blog post title and summary
            entry = feed.entries[0]
            return f"{entry.title}: {entry.summary}"
        return None
    except Exception as e:
        print(f"Error fetching RSS from {rss_url}: {e}")
        return None

def fetch_blog_html(url):
    """
    Fetch the latest blog post from an HTML page.
    """
    try:
        resp = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Common selectors for blog posts
        selectors = [
            "article h1", ".post-title", ".blog-title", 
            ".entry-title", "h1.post-title", ".article-title",
            "h1", ".title", ".headline", ".post-header h1"
        ]
        
        for selector in selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                title = title_elem.text.strip()
                
                # Try to get summary/excerpt
                summary_selectors = [
                    ".post-excerpt", ".post-summary", ".entry-summary",
                    ".article-excerpt", "p.lead", ".post-content p",
                    ".excerpt", ".summary", ".description"
                ]
                
                summary = ""
                for summary_selector in summary_selectors:
                    summary_elem = soup.select_one(summary_selector)
                    if summary_elem:
                        summary = summary_elem.text.strip()
                        break
                
                # If no summary found, try to get first paragraph
                if not summary:
                    first_p = soup.select_one("p")
                    if first_p:
                        summary = first_p.text.strip()
                
                return f"{title}: {summary}" if summary else title
        
        # Fallback: try to find any meaningful content
        main_content = soup.find("main") or soup.find("body")
        if main_content:
            for element in main_content.find_all(['p', 'div'], limit=5):
                text = element.get_text(strip=True)
                if len(text) > 30 and len(text) < 300:
                    return text
        
        return None
    except Exception as e:
        print(f"Error fetching blog from {url}: {e}")
        return None 