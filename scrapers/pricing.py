# scrapers/pricing.py

import requests
from bs4 import BeautifulSoup
import re

def fetch_pricing(url):
    """
    Fetch pricing page content to detect pricing changes.
    """
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get main content area
        main_content = soup.find("main") or soup.find("body")
        if not main_content:
            return None
        
        # Extract text content
        text_content = main_content.get_text(separator="\n", strip=True)
        
        # Clean up whitespace
        text_content = re.sub(r'\n\s*\n', '\n', text_content)
        text_content = re.sub(r'\s+', ' ', text_content)
        
        # Limit content length to avoid token limits
        if len(text_content) > 2000:
            text_content = text_content[:2000] + "..."
        
        return text_content
    except Exception as e:
        print(f"Error fetching pricing from {url}: {e}")
        return None

def extract_pricing_info(content):
    """
    Extract key pricing information from content.
    """
    if not content:
        return None
    
    # Look for common pricing patterns
    pricing_patterns = [
        r'\$\d+(?:\.\d{2})?',  # $10, $10.99
        r'\d+\s*(?:USD|dollars?|per\s+month|per\s+year)',  # 10 USD, 10 dollars
        r'(?:free|trial|pro|enterprise|basic|premium)',  # Plan names
    ]
    
    found_pricing = []
    for pattern in pricing_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        found_pricing.extend(matches)
    
    if found_pricing:
        return f"Pricing info: {', '.join(set(found_pricing[:5]))}"
    
    return content[:500] + "..." if len(content) > 500 else content 