from flask import Flask, render_template_string, jsonify
from db.models import get_weekly_updates
import os
import markdown as md

app = Flask(__name__)

NOTION_URL = os.getenv("NOTION_DASHBOARD_URL", "https://www.notion.so/2354567f104e8047b931ea6037251f80")
SLACK_URL = os.getenv("SLACK_DASHBOARD_URL", "https://slack.com/app_redirect?channel=C0978AU90TS")

DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Competitor Feature Tracker Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #f8fafc 0%, #e0e7ef 100%); }
        .card { transition: box-shadow 0.2s; }
        .card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.08); }
        .icon-badge { width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; border-radius: 8px; font-weight: 600; font-size: 1.1rem; }
        .icon-figma { background: #ede9fe; color: #7c3aed; }
        .icon-notion { background: #f3f4f6; color: #374151; }
        .icon-linear { background: #dbeafe; color: #2563eb; }
        .badge-pricing { background: #fef3c7; color: #b45309; }
        .badge-changelog { background: #d1fae5; color: #047857; }
        .badge-blog { background: #f3e8ff; color: #7c3aed; }
        .badge-default { background: #e5e7eb; color: #374151; }
        .sentto-badge { font-size: 0.85em; margin-right: 0.3em; }
    </style>
</head>
<body>
<div class="container py-4">
    <div class="text-center mb-4">
        <h1 class="fw-bold mb-2">Competitor Feature Tracker</h1>
        <p class="lead text-secondary mb-3">Stay ahead with real-time competitor insights and feature updates</p>
        <div class="d-flex justify-content-center gap-2 mb-2">
            <a href="{{ notion_url }}" target="_blank" class="btn btn-primary btn-lg">
                View in Notion
            </a>
            <a href="{{ slack_url }}" target="_blank" class="btn btn-success btn-lg">
                View in Slack
            </a>
        </div>
    </div>
    <hr class="mb-4">
    <div class="row mb-4">
        <div class="col-md-4 mb-3">
            <div class="card shadow-sm">
                <div class="card-body d-flex align-items-center gap-3">
                    <div class="p-2 bg-primary bg-opacity-10 rounded">
                        <svg width="24" height="24" fill="none"><path d="M12 4v16m8-8H4" stroke="#2563eb" stroke-width="2" stroke-linecap="round"/></svg>
                    </div>
                    <div>
                        <div class="text-secondary small">Total Updates</div>
                        <div class="h4 mb-0">{{ updates|length }}</div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-4 mb-3">
            <div class="card shadow-sm">
                <div class="card-body d-flex align-items-center gap-3">
                    <div class="p-2 bg-success bg-opacity-10 rounded">
                        <svg width="24" height="24" fill="none"><circle cx="12" cy="12" r="10" stroke="#16a34a" stroke-width="2"/></svg>
                    </div>
                    <div>
                        <div class="text-secondary small">Competitors Tracked</div>
                        <div class="h4 mb-0">{{ updates|map(attribute='competitor_name')|unique|list|length }}</div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-4 mb-3">
            <div class="card shadow-sm">
                <div class="card-body d-flex align-items-center gap-3">
                    <div class="p-2 bg-warning bg-opacity-10 rounded">
                        <svg width="24" height="24" fill="none"><rect x="4" y="4" width="16" height="16" rx="4" stroke="#f59e42" stroke-width="2"/></svg>
                    </div>
                    <div>
                        <div class="text-secondary small">This Week</div>
                        <div class="h4 mb-0">{{ updates|length }}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <h3 class="mb-3">Latest Scraped Updates</h3>
    <div id="updates-list">
        {% if updates %}
            <div class="row g-4">
            {% for update in updates %}
                <div class="col-md-6">
                    <div class="card mb-3 hover:shadow-lg">
                        <div class="card-header d-flex align-items-center gap-3 pb-2">
                            <div class="icon-badge 
                                {% if update.competitor_name == 'Figma' %}icon-figma
                                {% elif update.competitor_name == 'Notion' %}icon-notion
                                {% elif update.competitor_name == 'Linear' %}icon-linear
                                {% else %}icon-notion{% endif %}">
                                {{ update.competitor_name[0] }}
                            </div>
                            <div>
                                <div class="fw-semibold">{{ update.competitor_name }} {{ update.source_type.title() }} Update</div>
                                <div class="text-muted small">{{ update.timestamp }}</div>
                            </div>
                            <span class="ms-auto badge 
                                {% if update.source_type == 'pricing' %}badge-pricing
                                {% elif update.source_type == 'changelog' %}badge-changelog
                                {% elif update.source_type == 'blog' %}badge-blog
                                {% else %}badge-default{% endif %}">
                                {{ update.source_type.upper() }}
                            </span>
                        </div>
                        <div class="card-body pt-2">
                            <div class="mb-3" style="white-space: pre-line; cursor:pointer;" data-bs-toggle="collapse" data-bs-target="#{{ update.collapse_id }}" aria-expanded="false" aria-controls="{{ update.collapse_id }}">{{ update.summary_html|safe }}</div>
                            <div class="collapse" id="{{ update.collapse_id }}"><div class="card card-body mt-2">{{ update.content_html|safe }}</div></div>
                            <div class="d-flex flex-wrap align-items-center gap-2 mb-2">
                                <span class="text-secondary small">Sent to:</span>
                                <span class="badge sentto-badge bg-secondary text-white">Notion</span>
                                <span class="badge sentto-badge bg-success text-white">Slack</span>
                                <span class="badge sentto-badge bg-primary text-white">Email</span>
                            </div>
                            <a href="{{ update.source_url }}" target="_blank" class="btn btn-outline-primary btn-sm">
                                Read More
                            </a>
                        </div>
                    </div>
                </div>
            {% endfor %}
            </div>
        {% else %}
            <div class="alert alert-info">No updates found.</div>
        {% endif %}
    </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

@app.route('/')
def dashboard():
    updates = get_weekly_updates()
    # Sort and limit to top 10 most recent
    updates = sorted(updates, key=lambda u: u['timestamp'], reverse=True)[:10]
    for idx, update in enumerate(updates):
        summary = update.get('summary', '')
        content = update.get('content', '')
        # Preview: summary (markdown), full content for expanded
        update['summary_html'] = md.markdown(summary)
        update['content_html'] = md.markdown(content)
        update['collapse_id'] = f"collapseContent{idx}"
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