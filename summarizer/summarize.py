# summarizer/summarize.py

import os
import time
import google.generativeai as genai
from dotenv import load_dotenv
import re
from datetime import datetime, timedelta

# Global rate limiting
last_request_time = None
MIN_REQUEST_INTERVAL = 30  # Minimum 30 seconds between requests for free tier (reduced from 60)

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def simple_summarize(content, source_type="update"):
    """
    Simple fallback summarization when Gemini API is unavailable.
    """
    # Extract key information without AI
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    title = lines[0][:100] if lines else "Update"
    
    # Create a basic summary
    summary = f"**{source_type.title()} Update**\n\n"
    summary += f"**Title:** {title}\n\n"
    
    # Try to extract key points from the content
    key_points = []
    for line in lines[:10]:  # Look at first 10 lines
        line = line.strip()
        if len(line) > 20 and len(line) < 200:  # Reasonable length
            # Look for lines that might be key points
            if any(keyword in line.lower() for keyword in ['new', 'feature', 'update', 'improved', 'added', 'enhanced', 'launched', 'released']):
                key_points.append(f"• {line}")
            elif line.startswith(('•', '-', '*', '1.', '2.', '3.')):
                key_points.append(f"• {line.lstrip('•-*1234567890. ')}")
    
    if key_points:
        summary += "**Key Points:**\n"
        summary += "\n".join(key_points[:5]) + "\n\n"  # Limit to 5 points
    
    # Add content preview
    content_preview = content[:300] + "..." if len(content) > 300 else content
    summary += f"**Content Preview:**\n{content_preview}\n\n"
    
    return summary

def summarize_with_gemini(content, source_type="update"):
    """
    Summarize competitor update content using Google Gemini API.
    """
    global last_request_time
    
    if not os.getenv("GEMINI_API_KEY"):
        print("No GEMINI_API_KEY set. Using fallback summarization.")
        return simple_summarize(content, source_type)
    
    # Global rate limiting
    if last_request_time:
        time_since_last = datetime.now() - last_request_time
        if time_since_last.total_seconds() < MIN_REQUEST_INTERVAL:
            wait_time = MIN_REQUEST_INTERVAL - time_since_last.total_seconds()
            print(f"Rate limiting: Waiting {wait_time:.1f} seconds before next Gemini request...")
            time.sleep(wait_time)
    
    try:
        # Update last request time
        last_request_time = datetime.now()
        
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
            # Extract retry delay from error message if available
            if "retry_delay" in error_msg and not should_skip_rate_limit_wait():
                try:
                    import re
                    retry_match = re.search(r'retry_delay\s*{\s*seconds:\s*(\d+)', error_msg)
                    if retry_match:
                        retry_seconds = int(retry_match.group(1))
                        print(f"Rate limit detected. Waiting {retry_seconds} seconds... (Press Ctrl+C to skip)")
                        try:
                            time.sleep(retry_seconds)
                            print("Resume after rate limit wait.")
                        except KeyboardInterrupt:
                            print("Rate limit wait skipped by user.")
                except:
                    pass
            elif should_skip_rate_limit_wait():
                print("Rate limit wait skipped via SKIP_RATE_LIMIT_WAIT environment variable.")
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

def truncate_summary(summary, max_chars=900, max_words=180):
    """
    Truncate the summary to a maximum number of characters or words, ending at the last full sentence or line.
    """
    # Truncate by words first
    words = summary.split()
    if len(words) > max_words:
        summary = ' '.join(words[:max_words])
    # Truncate by characters, but try to end at a sentence or line break
    if len(summary) > max_chars:
        # Find the last period or line break before max_chars
        cut = summary.rfind('.', 0, max_chars)
        cut_nl = summary.rfind('\n', 0, max_chars)
        cut = max(cut, cut_nl)
        if cut > 0:
            summary = summary[:cut+1]
        else:
            summary = summary[:max_chars]
        summary = summary.rstrip() + '\n[Summary truncated due to length limit.]'
    return summary

def summarize_update(content, source_type="update", competitor=None):
    """
    Main summarization function with formatting for Slack/Notion.
    """
    # Check if Gemini API is disabled via environment variable
    if os.getenv("DISABLE_GEMINI_API", "false").lower() == "true":
        print("Gemini API disabled via DISABLE_GEMINI_API environment variable. Using fallback summarization.")
        summary = simple_summarize(content, source_type)
    else:
        summary = summarize_with_gemini(content, source_type)
    formatted = format_for_slack_and_notion(summary, competitor=competitor, update_type=source_type)
    return truncate_summary(formatted)

def should_skip_rate_limit_wait():
    """Check if rate limit waiting should be skipped."""
    return os.getenv("SKIP_RATE_LIMIT_WAIT", "false").lower() == "true" 