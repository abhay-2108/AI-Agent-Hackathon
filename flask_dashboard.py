from flask import Flask, render_template_string, jsonify, request, redirect, url_for
import subprocess
import threading
import os
import markdown as md
from db.models import get_weekly_updates

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
        .dashboard-fadein { animation: fadeIn 1.2s cubic-bezier(.4,0,.2,1); }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(40px); }
            to { opacity: 1; transform: none; }
        }
        .card { transition: box-shadow 0.3s, transform 0.2s; border-radius: 1.25rem; box-shadow: 0 2px 12px rgba(99,102,241,0.07); }
        .card:hover { box-shadow: 0 8px 32px rgba(99,102,241,0.16); transform: translateY(-4px) scale(1.03); }
        .icon-badge { width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; border-radius: 8px; font-weight: 600; font-size: 1.1rem; box-shadow: 0 2px 8px rgba(99,102,241,0.08); transition: background 0.2s, color 0.2s; }
        .icon-figma { background: #ede9fe; color: #7c3aed; }
        .icon-notion { background: #f3f4f6; color: #374151; }
        .icon-linear { background: #dbeafe; color: #2563eb; }
        .badge-pricing { background: #fef3c7; color: #b45309; }
        .badge-changelog { background: #d1fae5; color: #047857; }
        .badge-blog { background: #f3e8ff; color: #7c3aed; }
        .badge-default { background: #e5e7eb; color: #374151; }
        .sentto-badge { font-size: 0.85em; margin-right: 0.3em; }
        .card-header { background: none; border-bottom: none; }
        .card-body { transition: background 0.2s; }
        .card:hover .card-body { background: #f8fafc; }
        .btn-outline-primary { transition: box-shadow 0.2s, background 0.2s; }
        .btn-outline-primary:hover { box-shadow: 0 2px 8px #2563eb33; background: #2563eb; color: #fff; }
        .spinner-border { animation: spinner-grow 1s linear infinite; }
        @keyframes spinner-grow { 0% { transform: scale(1); } 50% { transform: scale(1.2); } 100% { transform: scale(1); } }
    </style>
</head>
<body>
<div class="container py-4 dashboard-fadein">
    <div class="text-center mb-4">
        <h1 class="fw-bold mb-2">Competitor Feature Tracker</h1>
        <p class="lead text-secondary mb-3">Stay ahead with real-time competitor insights and feature updates</p>
        <div class="d-flex justify-content-center gap-2 mb-2">
            <a href="{{ notion_url }}" target="_blank" class="btn btn-primary btn-lg shadow-sm animate__animated animate__pulse animate__delay-1s animate__infinite">View in Notion</a>
            <a href="{{ slack_url }}" target="_blank" class="btn btn-success btn-lg shadow-sm animate__animated animate__pulse animate__delay-2s animate__infinite">View in Slack</a>
        </div>
    </div>
    <hr class="mb-4">
    <div class="row mb-4">
        <div class="col-md-4 mb-3">
            <div class="card shadow-sm animate__animated animate__fadeInUp animate__delay-1s">
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
            <div class="card shadow-sm animate__animated animate__fadeInUp animate__delay-2s">
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
            <div class="card shadow-sm animate__animated animate__fadeInUp animate__delay-3s">
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
    <h3 class="mb-3 animate__animated animate__fadeInDown">Latest Scraped Updates</h3>
    <div id="updates-list">
        {% if updates %}
            <div class="row g-4">
            {% for update in updates %}
                <div class="col-md-6">
                    <div class="card mb-3 hover:shadow-lg animate__animated animate__fadeInUp animate__faster" style="transition-delay: {{ loop.index0 * 0.1 }}s;">
                        <div class="card-header d-flex align-items-center gap-3 pb-2">
                            <div class="icon-badge icon-notion">{{ update.competitor_name[0] }}</div>
                            <div>
                                <div class="fw-semibold">{{ update.competitor_name }} {{ update.source_type.title() }} Update</div>
                                <div class="text-muted small">{{ update.timestamp }}</div>
                            </div>
                            <span class="ms-auto badge badge-changelog">{{ update.source_type.upper() }}</span>
                        </div>
                        <div class="card-body pt-2">
                            <div class="mb-3" style="white-space: pre-line; cursor:pointer; transition: color 0.2s;" data-bs-toggle="collapse" data-bs-target="#{{ update.collapse_id }}" aria-expanded="false" aria-controls="{{ update.collapse_id }}">{{ update.summary_html|safe }}</div>
                            <div class="collapse" id="{{ update.collapse_id }}"><div class="card card-body mt-2 animate__animated animate__fadeIn">{{ update.content_html|safe }}</div></div>
                            <div class="d-flex flex-wrap align-items-center gap-2 mb-2">
                                <span class="text-secondary small">Sent to:</span>
                                <span class="badge sentto-badge bg-secondary text-white">Notion</span>
                                <span class="badge sentto-badge bg-success text-white">Slack</span>
                                <span class="badge sentto-badge bg-primary text-white">Email</span>
                            </div>
                            <a href="{{ update.source_url }}" target="_blank" class="btn btn-outline-primary btn-sm">Read More</a>
                        </div>
                    </div>
                </div>
            {% endfor %}
            </div>
        {% else %}
            <div class="alert alert-info animate__animated animate__fadeIn">No updates found.</div>
        {% endif %}
    </div>
</div>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

ABOUT_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About - Competitor Feature Tracker</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>
    <style>
        body { background: linear-gradient(135deg, #f8fafc 0%, #e0e7ef 100%); font-family: 'Inter', sans-serif; }
        .hero { padding: 4rem 0 2rem 0; }
        .feature-card { border: none; border-radius: 1.25rem; box-shadow: 0 4px 24px rgba(99,102,241,0.07); transition: transform 0.3s, box-shadow 0.3s; background: #fff; }
        .feature-card:hover { transform: translateY(-8px) scale(1.04); box-shadow: 0 12px 36px rgba(99,102,241,0.18); }
        .feature-icon { font-size: 2.5rem; margin-bottom: 0.5rem; transition: color 0.2s, transform 0.2s; }
        .feature-card:hover .feature-icon { color: #2563eb; transform: scale(1.2) rotate(-8deg); }
        .btn-main { background: linear-gradient(90deg, #2563eb 0%, #6366f1 100%); color: #fff; border-radius: 8px; font-weight: 600; box-shadow: 0 2px 8px rgba(99,102,241,0.08); transition: background 0.2s, box-shadow 0.2s; }
        .btn-main:hover { background: linear-gradient(90deg, #1d4ed8 0%, #6366f1 100%); box-shadow: 0 4px 16px rgba(99,102,241,0.16); }
        .section-title { font-weight: 800; letter-spacing: -1px; }
        .feature-title { font-weight: 600; font-size: 1.2rem; }
        .feature-desc { color: #64748b; font-size: 1rem; }
        .github-link { color: #6366f1; text-decoration: none; font-weight: 600; }
        .github-link:hover { text-decoration: underline; color: #2563eb; }
    </style>
    <script src="https://unpkg.com/feather-icons"></script>
</head>
<body>
<div class="container hero text-center animate__animated animate__fadeInDown animate__faster">
    <h1 class="display-4 fw-bold mb-3 section-title animate__animated animate__fadeInDown">Competitor Feature Tracker</h1>
    <p class="lead mb-4 animate__animated animate__fadeIn animate__delay-1s">AI-powered tool for Product Managers to monitor, summarize, and get notified about competitor product updates &mdash; all in one place.</p>
    <div class="row justify-content-center g-4 mb-4">
        <div class="col-md-4">
            <div class="card feature-card p-4 h-100 animate__animated animate__zoomIn animate__delay-1s">
                <div class="feature-icon text-primary"><i data-feather="search"></i></div>
                <div class="feature-title">Multi-Source Monitoring</div>
                <div class="feature-desc">Automatically tracks changelogs, blogs, pricing pages, and GitHub releases from your competitors, so you never miss an update.</div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card feature-card p-4 h-100 animate__animated animate__zoomIn animate__delay-2s">
                <div class="feature-icon text-info"><i data-feather="cpu"></i></div>
                <div class="feature-title">AI Summarization</div>
                <div class="feature-desc">Uses Google Gemini to generate concise, insightful summaries and tags for every update, saving you hours of manual review.</div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card feature-card p-4 h-100 animate__animated animate__zoomIn animate__delay-3s">
                <div class="feature-icon text-success"><i data-feather="bell"></i></div>
                <div class="feature-title">Multi-Channel Notifications</div>
                <div class="feature-desc">Delivers updates to Slack, Notion, and Email with rich, platform-optimized formatting for maximum clarity and impact.</div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card feature-card p-4 h-100 animate__animated animate__zoomIn animate__delay-4s">
                <div class="feature-icon text-warning"><i data-feather="clock"></i></div>
                <div class="feature-title">Automated Scheduling</div>
                <div class="feature-desc">Runs on a schedule (e.g., weekly digests) or on-demand, so you always get updates at the right time without manual effort.</div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card feature-card p-4 h-100 animate__animated animate__zoomIn animate__delay-5s">
                <div class="feature-icon text-secondary"><i data-feather="database"></i></div>
                <div class="feature-title">Data Storage & Change Detection</div>
                <div class="feature-desc">Uses SQLite to store historical updates and smartly detects new changes, ensuring you only see what’s new and relevant.</div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card feature-card p-4 h-100 animate__animated animate__zoomIn animate__delay-6s">
                <div class="feature-icon text-danger"><i data-feather="layout"></i></div>
                <div class="feature-title">Enhanced Formatting</div>
                <div class="feature-desc">Messages are beautifully formatted for each platform: emojis, HTML emails, Notion markdown, and grouped digests for easy reading.</div>
            </div>
        </div>
    </div>
    <a href="{{ url_for('tracker') }}" class="btn btn-main btn-lg mt-3 shadow animate__animated animate__pulse animate__infinite">Go to Competitor Tracker</a>
    <div class="mt-5 text-muted animate__animated animate__fadeInUp animate__delay-2s">Deploy-ready Flask UI &mdash; <a href="https://github.com/your-repo" class="github-link" target="_blank">View on GitHub</a></div>
</div>
<script>feather.replace()</script>
</body>
</html>
'''

@app.route('/')
def about():
    return render_template_string(ABOUT_TEMPLATE)

@app.route('/tracker', methods=['GET'])
def tracker():
    updates = get_weekly_updates()
    updates = sorted(updates, key=lambda u: u['timestamp'], reverse=True)[:10]
    for idx, update in enumerate(updates):
        summary = update.get('summary', '')
        content = update.get('content', '')
        update['summary_html'] = md.markdown(summary)
        update['content_html'] = md.markdown(content)
        update['collapse_id'] = f"collapseContent{idx}"
    run_status = request.args.get('run_status')
    email = request.args.get('email', '')
    return render_template_string('''
    <style>
    .topbar-action { position: absolute; top: 2rem; right: 2rem; z-index: 10; }
    .topbar-back { position: absolute; top: 2rem; left: 2rem; z-index: 10; }
    .btn-back {
      background: linear-gradient(90deg, #6366f1 0%, #2563eb 100%);
      color: #fff;
      border-radius: 8px;
      font-weight: 600;
      box-shadow: 0 2px 8px rgba(99,102,241,0.08);
      border: none;
      padding: 0.5rem 1.25rem;
      transition: background 0.2s, box-shadow 0.2s;
    }
    .btn-back:hover {
      background: linear-gradient(90deg, #2563eb 0%, #6366f1 100%);
      color: #fff;
      box-shadow: 0 4px 16px rgba(99,102,241,0.16);
      text-decoration: none;
    }
    </style>
    <div class="topbar-back">
      <a href="/" class="btn btn-back"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor" style="vertical-align:middle;margin-right:6px;"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>Back</a>
    </div>
    <div class="topbar-action">
        <button class="btn btn-lg btn-warning" onclick="showEmailModal()">Run Competitor Tracker</button>
    </div>
    <!-- Email Modal -->
    <div class="modal fade" id="emailModal" tabindex="-1" aria-labelledby="emailModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <form id="runForm" method="post" action="/run_tracker" onsubmit="return submitRunForm(event)">
            <div class="modal-header">
              <h5 class="modal-title" id="emailModalLabel">Enter your email for notifications</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <input type="email" name="email" class="form-control" placeholder="Email address" required autofocus>
            </div>
            <div class="modal-footer">
              <button type="submit" class="btn btn-primary">Run Tracker</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    <div id="loadingSpinner" class="d-none text-center my-5">
      <div class="spinner-border text-primary" style="width: 4rem; height: 4rem;" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <div class="mt-3">Running tracker, scraping and sending notifications...</div>
    </div>
    <div id="trackerContent">
    ''' + DASHBOARD_TEMPLATE + '''
    <div class="text-center mt-4">
        {% if run_status %}
        <div class="alert alert-info mt-3">{{ run_status }}</div>
        {% endif %}
    </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
    let lastUpdateTimestamp = null;
    let pollStartTime = null;
    function showEmailModal() {
      var modal = new bootstrap.Modal(document.getElementById('emailModal'));
      modal.show();
    }
    function submitRunForm(e) {
      e.preventDefault();
      document.getElementById('trackerContent').classList.add('d-none');
      document.getElementById('loadingSpinner').classList.remove('d-none');
      var form = document.getElementById('runForm');
      var formData = new FormData(form);
      sessionStorage.setItem('showSpinner', 'true');
      fetch('/api/updates').then(r => r.json()).then(updates => {
        if (updates.length > 0) {
          lastUpdateTimestamp = updates[0].timestamp;
        } else {
          lastUpdateTimestamp = null;
        }
        fetch('/run_tracker', {
          method: 'POST',
          body: formData
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            pollStartTime = Date.now();
            pollForUpdates();
          } else {
            alert('Error: ' + (data.message || 'Failed to run tracker.'));
            document.getElementById('loadingSpinner').classList.add('d-none');
            document.getElementById('trackerContent').classList.remove('d-none');
            sessionStorage.removeItem('showSpinner');
          }
        })
        .catch(() => {
          alert('Error running tracker.');
          document.getElementById('loadingSpinner').classList.add('d-none');
          document.getElementById('trackerContent').classList.remove('d-none');
          sessionStorage.removeItem('showSpinner');
        });
      });
      var modal = bootstrap.Modal.getInstance(document.getElementById('emailModal'));
      modal.hide();
      return false;
    }
    function pollForUpdates() {
      if (!pollStartTime) pollStartTime = Date.now();
      fetch('/api/updates')
        .then(r => r.json())
        .then(updates => {
          let newUpdate = false;
          if (updates.length > 0) {
            if (!lastUpdateTimestamp || updates[0].timestamp !== lastUpdateTimestamp) {
              newUpdate = true;
            }
          }
          if (newUpdate) {
            sessionStorage.removeItem('showSpinner');
            window.location.reload();
          } else if (Date.now() - pollStartTime > 60000) { // 60 seconds timeout
            sessionStorage.removeItem('showSpinner');
            document.getElementById('loadingSpinner').classList.add('d-none');
            document.getElementById('trackerContent').classList.remove('d-none');
            alert('No new updates found. Please try again later.');
          } else {
            setTimeout(pollForUpdates, 5000);
          }
        })
        .catch(() => {
          setTimeout(pollForUpdates, 5000);
        });
    }
    window.addEventListener('DOMContentLoaded', function() {
      if (sessionStorage.getItem('showSpinner') === 'true') {
        document.getElementById('trackerContent').classList.add('d-none');
        document.getElementById('loadingSpinner').classList.remove('d-none');
        pollStartTime = Date.now();
        pollForUpdates();
      }
    });
    window.addEventListener('load', function() {
      sessionStorage.removeItem('showSpinner');
    });
    </script>
    ''', updates=updates, notion_url=NOTION_URL, slack_url=SLACK_URL, run_status=run_status, email=email)

# Run scraping, summarization, and email in background, return JSON
import threading
from notifier.email import send_email
from main import CompetitorTracker
from db.models import get_weekly_updates

@app.route('/run_tracker', methods=['POST'])
def run_tracker_api():
    email = request.form.get('email', '')
    def run_job():
        tracker = CompetitorTracker()
        tracker.run()
        # After run, send digest email
        updates = get_weekly_updates()
        from notifier.email import send_email_digest
        send_email_digest(email, updates)
    thread = threading.Thread(target=run_job)
    thread.start()
    return jsonify({'success': True, 'message': 'Tracker started. You will be notified at your email.'})

@app.route('/api/updates')
def api_updates():
    updates = get_weekly_updates()
    for u in updates:
        u['title'] = f"{u['competitor_name']} {u['source_type'].title()} Update"
        u['sentTo'] = ['notion', 'slack', 'email']
    return jsonify(updates)

if __name__ == '__main__':
    app.run(debug=True) 