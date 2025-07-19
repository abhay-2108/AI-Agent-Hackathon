# summarizer/summarize.py

import os
import time
import google.generativeai as genai
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def simple_summarize(content, source_type="update"):
    """
    Simple fallback summarization when Gemini API is unavailable.
    """
    # Extract key information without AI
    lines = content.split('\n')
    title = lines[0][:100] if lines else "Update"
    
    # Create a basic summary
    summary = f"**{source_type.title()} Update**\n\n"
    summary += f"**Title:** {title}\n\n"
    
    # Add first few lines as summary
    content_preview = content[:500] + "..." if len(content) > 500 else content
    summary += f"**Content:**\n{content_preview}\n\n"
    
    return summary

def summarize_with_gemini(content, source_type="update"):
    """
    Summarize competitor update content using Google Gemini API.
    """
    if not os.getenv("GEMINI_API_KEY"):
        print("No GEMINI_API_KEY set. Using fallback summarization.")
        return simple_summarize(content, source_type)
    
    try:
        # Add rate limiting - wait between requests
        time.sleep(2)  # Wait 2 seconds between requests
        
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        prompt = f"""
        Summarize this {source_type} update from a competitor in a clear, concise way.
        Focus on:
        - What new feature or change was announced
        - Key benefits or improvements
        - Impact on users or market
        
        Keep it under 200 words and use bullet points for clarity.
        
        Content:
        {content}
        """
        
        response = model.generate_content(prompt)
        
        if response.text:
            return response.text
        else:
            print("Empty response from Gemini. Using fallback.")
            return simple_summarize(content, source_type)
            
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            print(f"Gemini API rate limit exceeded. Using fallback summarization.")
            print(f"Error: {error_msg}")
            return simple_summarize(content, source_type)
        else:
            print(f"Error summarizing with Gemini: {e}")
            print("Using fallback summarization.")
            return simple_summarize(content, source_type)

def format_for_slack_and_notion(summary, competitor=None, update_type=None):
    """
    Post-process Gemini summary for Slack and Notion readability.
    """
    heading = ""
    if competitor and update_type:
        heading = f"🚨 **{competitor} {update_type.title()} Update**\n"
    elif competitor:
        heading = f"🚨 **{competitor} Update**\n"
    elif update_type:
        heading = f"🚨 **{update_type.title()} Update**\n"

    # Ensure bullet points start with • or -
    summary = re.sub(r"^[-*]\s+", "• ", summary, flags=re.MULTILINE)
    # Bold any lines that look like headings
    summary = re.sub(r"^(.*:)\s*$", r"**\1**", summary, flags=re.MULTILINE)
    # Remove excessive blank lines
    summary = re.sub(r"\n{3,}", "\n\n", summary)
    # Ensure each bullet point is on its own line
    summary = re.sub(r"•", "\n•", summary)
    # Clean up leading/trailing whitespace
    summary = summary.strip()

    return f"{heading}{summary}"

def summarize_update(content, source_type="update", competitor=None):
    """
    Main summarization function with formatting for Slack/Notion.
    """
    summary = summarize_with_gemini(content, source_type)
    return format_for_slack_and_notion(summary, competitor=competitor, update_type=source_type) 