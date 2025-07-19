import os
import requests

def send_to_slack(message):
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        print("No SLACK_WEBHOOK_URL set.")
        return
    payload = {"text": message}
    requests.post(webhook_url, json=payload) 