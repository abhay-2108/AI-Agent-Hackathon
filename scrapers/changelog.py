# scrapers/changelog.py

import requests
from bs4 import BeautifulSoup

def fetch_changelog(url):
    """
    Fetch the latest changelog entry from a competitor's website.
    """
    try:
        resp = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Multiple selectors for different changelog structures
        selectors = [
            "article h2",                    # Linear style
            ".changelog-entry h2",           # Generic changelog
            ".release-note h2",              # Release notes
            ".update-title",                 # Update titles
            "h2",                           # Any h2
            ".changelog h1",                 # Changelog headers
            ".release h1",                   # Release headers
            "h1",                           # Any h1
            ".entry-title",                  # Entry titles
            ".post-title"                    # Post titles
        ]
        
        for selector in selectors:
            entry = soup.select_one(selector)
            if entry and entry.text.strip():
                return entry.text.strip()
        
        # If no specific selectors work, try to find any meaningful content
        main_content = soup.find("main") or soup.find("body")
        if main_content:
            # Look for the first meaningful text block
            for element in main_content.find_all(['p', 'div', 'span'], limit=10):
                text = element.get_text(strip=True)
                if len(text) > 20 and len(text) < 500:  # Reasonable length
                    return text
        
        return None
    except Exception as e:
        print(f"Error fetching changelog from {url}: {e}")
        return None