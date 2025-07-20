from flask import Flask, render_template_string, jsonify
from db.models import get_weekly_updates
import os

app = Flask(__name__)

# Replace with your actual Notion and Slack URLs
NOTION_URL = os.getenv("NOTION_DASHBOARD_URL", "https://www.notion.so/your-notion-page-id")
SLACK_URL = os.getenv("SLACK_DASHBOARD_URL", "https://slack.com/app_redirect?channel=your-channel-id")

DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Competitor Feature Tracker Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<div class="container py-4">
    <h1 class="mb-4 text-center">Competitor Feature Tracker Dashboard</h1>
    <div class="mb-3 d-flex justify-content-center gap-3">
        <a href="{{ notion_url }}" target="_blank" class="btn btn-primary">View in Notion</a>
        <a href="{{ slack_url }}" target="_blank" class="btn btn-success">View in Slack</a>
    </div>
    <h3 class="mb-3">Latest Scraped Updates</h3>
    <div id="updates-list">
        {% if updates %}
            {% for update in updates %}
                <div class="card mb-3">
                    <div class="card-body">
                        <h5 class="card-title">{{ update.competitor_name }} {{ update.source_type.title() }} Update</h5>
                        <p class="card-text">{{ update.summary }}</p>
                        <a href="{{ update.source_url }}" target="_blank" class="card-link">Read more</a>
                        <div class="text-muted small mt-2">Sent to: Notion, Slack, Email | {{ update.timestamp }}</div>
                    </div>
                </div>
            {% endfor %}
        {% else %}
            <p>No updates found.</p>
        {% endif %}
    </div>
</div>
</body>
</html>
'''

@app.route('/')
def dashboard():
    updates = get_weekly_updates()
    return render_template_string(DASHBOARD_TEMPLATE, updates=updates, notion_url=NOTION_URL, slack_url=SLACK_URL)

@app.route('/api/updates')
def api_updates():
    updates = get_weekly_updates()
    for u in updates:
        u['title'] = f"{u['competitor_name']} {u['source_type'].title()} Update"
        u['sentTo'] = ['notion', 'slack', 'email']
    return jsonify(updates)

if __name__ == '__main__':
    app.run(debug=True) 