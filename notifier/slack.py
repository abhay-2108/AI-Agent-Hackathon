import os
import requests
from .formatters import MessageFormatter

def send_to_slack(message, update_data=None):
    """
    Send a message to Slack.
    
    Args:
        message: Simple text message or formatted message
        update_data: Dictionary containing update information for formatting
    """
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        print("No SLACK_WEBHOOK_URL set.")
        return False
    
    # If update_data is provided, format the message
    if update_data:
        formatter = MessageFormatter()
        message = formatter.format_slack_message(update_data)
    
    payload = {"text": message}
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code == 200:
            try:
                print(f"✅ Slack message sent successfully")
            except UnicodeEncodeError:
                print("Slack message sent successfully")
            return True
        else:
            try:
                print(f"❌ Failed to send Slack message: {response.status_code}")
            except UnicodeEncodeError:
                print(f"Failed to send Slack message: {response.status_code}")
            return False
    except Exception as e:
        try:
            print(f"❌ Error sending Slack message: {e}")
        except UnicodeEncodeError:
            print(f"Error sending Slack message: {e}")
        return False

def send_slack_digest(updates):
    """
    Send a digest of multiple updates to Slack.
    
    Args:
        updates: List of update dictionaries
    """
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        print("No SLACK_WEBHOOK_URL set.")
        return False
    
    formatter = MessageFormatter()
    message = formatter.format_slack_digest(updates)
    
    payload = {"text": message}
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code == 200:
            try:
                print(f"✅ Slack digest sent successfully")
            except UnicodeEncodeError:
                print("Slack digest sent successfully")
            return True
        else:
            try:
                print(f"❌ Failed to send Slack digest: {response.status_code}")
            except UnicodeEncodeError:
                print(f"Failed to send Slack digest: {response.status_code}")
            return False
    except Exception as e:
        try:
            print(f"❌ Error sending Slack digest: {e}")
        except UnicodeEncodeError:
            print(f"Error sending Slack digest: {e}")
        return False 