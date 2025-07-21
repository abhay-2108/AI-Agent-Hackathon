# 🚀 Competitor Feature Tracker

An AI-powered tool for Product Managers to automatically monitor and summarize product updates from TechCrunch, and deliver concise digests via Slack, Notion, and Email. Features a beautiful, modern dashboard with real-time polling, animations, and a deploy-ready Flask UI.

## ✨ Features

- **🌐 Single-Source Monitoring**: Scrapes TechCrunch for the latest news and updates
- **🤖 AI Summarization**: Uses Google Gemini to generate concise, 50-word summaries for each update
- **📊 Change Detection**: Smart detection of new content using database comparison
- **📢 Multi-Channel Notifications**: Sends updates to Slack, Notion, and Email with rich formatting
- **⏰ Automated Scheduling**: Run weekly or on-demand tracking
- **💾 Data Storage**: SQLite database for historical tracking and deduplication
- **🎨 Modern UI/UX**: Animated, responsive dashboard with beautiful cards, hover effects, and smooth transitions
- **🔄 Real-Time Polling**: UI polls for new updates and displays them as soon as scraping is complete

## 🖥️ Live Demo

- Start the dashboard: `python flask_dashboard.py`
- The About page describes the project and features animated cards
- The Tracker page shows the latest TechCrunch updates, with a top-right button to trigger scraping and notifications
- Enter your email to receive updates; the UI shows a loading spinner and displays new content as soon as it's ready

## 🏗️ Project Structure

```
AI-Agent-Hackathon/
├── agent/                # Python virtual environment (optional)
├── db/                   # Database models
├── notifier/             # Notification modules (Slack, Notion, Email)
├── scheduler/            # Job scheduling
├── scrapers/             # Scraping logic
├── summarizer/           # Gemini summarization
├── flask_dashboard.py    # Flask web dashboard (main UI)
├── main.py               # Main scraping and notification logic
├── requirements.txt      # Python dependencies
├── tracker.db            # SQLite database
└── README.md             # This file
```

## 📦 Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/abhay-2108/AI-Agent-Hackathon.git
    cd AI-Agent-Hackathon
    ```
2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4. **Set up environment variables**:
    - Create a `.env` file with your API keys (see below)

## 🔑 API Keys Required

- **GEMINI_API_KEY**: Google Gemini API key for summarization
- **SLACK_WEBHOOK_URL**: Slack webhook URL for notifications
- **NOTION_API_KEY**: Notion API key for database integration
- **NOTION_PAGE_ID**: Notion page ID where updates will be posted
- **EMAIL_FROM, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS**: For email notifications

## 🚀 Usage

### **Start the Dashboard**

```bash
python flask_dashboard.py
```
- The About page describes the project with animated, modern UI
- Click "Go to Competitor Tracker" to view the dashboard
- On the Tracker page, click "Run Competitor Tracker" (top right), enter your email, and the system will scrape TechCrunch, summarize, and send updates to Notion, Slack, and your email
- The UI shows a loading spinner and polls for new updates, displaying them as soon as they're available

### **Manual Run (CLI)**

```bash
python main.py
```

### **Automated Scheduler**

```bash
python scheduler/job_scheduler.py
```

## 🧪 Testing

- The UI and backend are tightly integrated; test by running the dashboard and triggering a scrape
- Ensure your API keys and webhooks are set up in `.env`

## 🛠️ Customization

- **Change Scraping Source**: By default, only TechCrunch is scraped. To change, edit the `self.competitors` dictionary in `main.py`.
- **UI/UX**: All styling and animation is in `flask_dashboard.py` using Bootstrap and Animate.css. Tweak as desired for your brand.

## 🛡️ Security & Troubleshooting

- **Push Issues**: If you see a "Secrets detected" or push rejection, ensure you have not committed any API keys or secrets. Remove them and try again.
- **API Key Errors**: Ensure all required API keys are set in `.env`
- **Scraping Failures**: If TechCrunch changes its structure, update the scraping logic in `scrapers/changelog.py`
- **Database Issues**: If you want to reset, delete `tracker.db` or run:
    ```bash
    python -c "import sqlite3; db=sqlite3.connect('tracker.db'); db.execute('DELETE FROM competitor_updates'); db.commit(); db.close()"
    ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🌐 Repository

- [GitHub: abhay-2108/AI-Agent-Hackathon](https://github.com/abhay-2108/AI-Agent-Hackathon)

---

**Happy competitor tracking! 🎯**
