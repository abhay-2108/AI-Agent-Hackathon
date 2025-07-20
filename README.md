# 🚀 Competitor Feature Tracker

An AI-powered tool for Product Managers to automatically monitor and summarize product updates from competitors (changelogs, blogs, release notes, pricing, and GitHub), and deliver weekly digests via Slack and Notion.

## ✨ Features

-   **🔍 Multi-Source Monitoring**: Track changelogs, blogs, pricing pages, and GitHub releases
-   **🤖 AI Summarization**: Use Google Gemini to automatically summarize and tag updates
-   **📊 Change Detection**: Smart detection of new content using database comparison
-   **📢 Multi-Channel Notifications**: Send updates to Slack, Notion, and Email with rich formatting
-   **⏰ Automated Scheduling**: Run weekly or on-demand tracking
-   **💾 Data Storage**: SQLite database for historical tracking and deduplication
-   **🎨 Enhanced Formatting**: Platform-specific message formatting with emojis, HTML, and rich content

## 🛠️ Tech Stack

-   **Python 3.8+**
-   **Web Scraping**: BeautifulSoup, requests, feedparser
-   **AI Summarization**: Google Gemini API
-   **Database**: SQLite
-   **Notifications**: Slack Webhooks, Notion API
-   **Scheduling**: Python schedule library

## 📦 Installation

1. **Clone the repository**:

    ```bash
    git clone <repository-url>
    cd competitor-tracker
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
    ```bash
    cp env_example.txt .env
    # Edit .env with your API keys
    ```

## 🔑 API Keys Required

You'll need the following API keys (add them to your `.env` file):

### **Required APIs**

-   **GEMINI_API_KEY**: Google Gemini API key for summarization
-   **SLACK_WEBHOOK_URL**: Slack webhook URL for notifications
-   **NOTION_API_KEY**: Notion API key for database integration
-   **NOTION_PAGE_ID**: Notion page ID where updates will be posted

### **Optional APIs**

-   **GITHUB_TOKEN**: GitHub personal access token (for higher rate limits)

## 🚀 Quick Start

### **Automatic Setup (Recommended)**

```bash
python setup.py
```

This will:

-   Check and install dependencies
-   Create a `.env` file with placeholder values
-   Test the system
-   Show next steps

### **Manual Setup**

1. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

2. **Set up environment variables**:

    ```bash
    cp env_example.txt .env
    # Edit .env with your API keys
    ```

3. **Test your setup**:
    ```bash
    python test_tracker.py
    ```

### **Running the Tracker**

**Manual run**:

```bash
python main.py
```

**Weekly digest**:

```bash
python main.py digest
```

**Start automated scheduler**:

```bash
# Using Python directly
python scheduler/job_scheduler.py

# Using the startup script (Windows)
start_scheduler.bat

# Using the startup script (Python)
python start_scheduler.py
```

**Scheduler options**:

```bash
python scheduler/job_scheduler.py once     # Run tracking once
python scheduler/job_scheduler.py digest   # Run digest once
python scheduler/job_scheduler.py help     # Show help
```

## 🧪 Testing

### **Comprehensive Test**

```bash
python test_tracker.py
```

### **Individual API Tests**

```bash
# Test Notion integration
python test_notion.py
```

### **Test Results**

-   ✅ **Working**: API is properly configured and functional
-   ⚠️ **Not configured**: API key missing but not required
-   ❌ **Failed**: API key present but not working

## 📋 Usage Examples

### Basic Tracking

```bash
# Track all competitors once
python main.py

# Generate weekly digest
python main.py digest
```

### Scheduler

```bash
# Start automated scheduler (runs Mon/Wed/Fri at 9 AM)
python scheduler/job_scheduler.py

# Run once immediately
python scheduler/job_scheduler.py once
```

## 🏗️ Project Structure

```
competitor-tracker/
├── scrapers/           # Web scraping modules
│   ├── changelog.py    # Changelog scraping
│   ├── blog.py         # Blog/RSS scraping
│   ├── pricing.py      # Pricing page scraping
│   ├── github.py       # GitHub API integration
│   └── social.py       # Social media placeholder
├── summarizer/         # AI summarization
│   └── summarize.py    # Gemini API integration
├── notifier/           # Notification modules
│   ├── slack.py        # Slack webhook integration
│   ├── notion.py       # Notion API integration
│   ├── email.py        # Email SMTP integration
│   └── formatters.py   # Message formatting for all platforms
├── db/                 # Database operations
│   └── models.py       # SQLite database models
├── scheduler/          # Automation
│   └── job_scheduler.py     # Job scheduling
├── main.py             # Main workflow orchestration
├── test_tracker.py     # Comprehensive test suite
├── test_notion.py      # Notion API tests
├── test_enhanced_notifications.py  # Enhanced formatting tests
├── test_rate_limiting_improved.py  # Rate limiting improvements test
├── requirements.txt    # Python dependencies
├── env_example.txt     # Environment variables template
└── README.md           # This file
```

## 🔧 Configuration

### Adding New Competitors

Edit the `competitors` dictionary in `main.py`:

```python
self.competitors = {
    'your_competitor': {
        'name': 'Competitor Name',
        'changelog': 'https://competitor.com/changelog',
        'blog': 'https://competitor.com/blog',
        'pricing': 'https://competitor.com/pricing',
        'github': {'owner': 'owner', 'repo': 'repo'}
    }
}
```

### Customizing Scrapers

Each scraper can be customized for specific websites by modifying the CSS selectors in the respective files.

## 📊 Database Schema

The SQLite database (`tracker.db`) contains:

-   **competitor_updates**: All tracked updates with metadata
    -   `id`: Primary key
    -   `source_type`: Type of update (changelog, blog, pricing, etc.)
    -   `source_url`: Source URL
    -   `content`: Raw content
    -   `summary`: AI-generated summary
    -   `competitor_name`: Competitor name
    -   `timestamp`: When the update was detected

## 🔄 Workflow

1. **Data Collection**: Scrapers fetch latest content from all sources
2. **Change Detection**: Compare with last stored version
3. **AI Summarization**: Use Gemini to summarize and tag updates
4. **Storage**: Save to SQLite database
5. **Notifications**: Send to Slack and Notion
6. **Scheduling**: Automated weekly runs

## 🚨 Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure all required API keys are set in `.env`
2. **Rate Limiting**: Some APIs have rate limits; consider adding delays
3. **Scraping Failures**: Websites may change structure; update selectors
4. **Database Errors**: Check file permissions for `tracker.db`

### **Scheduling Issues (Fixed)**

**Problem**: Scheduler wasn't working automatically due to Python environment issues.

**Solution**:

-   Fixed scheduler to use the correct Python interpreter (`sys.executable`)
-   Added proper virtual environment detection
-   Created startup scripts for easier deployment
-   Added comprehensive error handling and logging

**New Features**:

-   Automatic dependency checking and installation
-   Environment validation
-   Multiple startup options (Python script, batch file)
-   Better error messages and logging
-   Support for both tracking and digest jobs

### **Rate Limiting Improvements (Fixed)**

**Problem**: Gemini API rate limits were causing failures during summarization.

**Solution**:

-   Implemented global rate limiting (60 seconds between requests)
-   Added automatic retry delay extraction from error messages
-   Improved fallback summarization for when API is unavailable
-   Added option to disable Gemini API entirely via environment variable

**New Features**:

-   Smart rate limiting that respects API quotas (reduced to 30 seconds between requests)
-   Better fallback summarization with key point extraction
-   Environment variable `DISABLE_GEMINI_API=true` to use fallback only
-   Environment variable `SKIP_RATE_LIMIT_WAIT=true` to skip rate limit waiting
-   Manual skip option: Press Ctrl+C during rate limit waits
-   Automatic retry delay extraction from error messages
-   Graceful degradation when API is unavailable

### **Enhanced Notification Formatting (New)**

**Problem**: Messages sent to different platforms were basic and lacked visual appeal.

**Solution**:

-   Created a centralized `MessageFormatter` class for all platforms
-   Implemented platform-specific formatting optimizations
-   Added rich HTML email templates with professional styling
-   Enhanced Slack messages with emojis and structured formatting
-   Improved Notion content with proper markdown and organization

**New Features**:

-   **Slack**: Emoji indicators, structured formatting, source links
-   **Email**: Professional HTML templates, responsive design, rich content
-   **Notion**: Proper markdown formatting, organized sections, metadata
-   **Digest Support**: Grouped updates by competitor with summaries
-   **Source URLs**: Direct links to original content
-   **Timestamps**: Automatic timestamp inclusion
-   **Platform Optimization**: Each platform gets optimized formatting

### Debug Mode

Run individual test scripts for specific issues:

```bash
python test_notion.py     # Debug Notion issues
```

### API Setup Guides

-   [Slack Webhook Setup](#slack-webhook-setup)
-   [Notion API Setup](#notion-api-setup)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:

1. Check the troubleshooting section
2. Review the code comments
3. Open an issue on GitHub

---

**Happy competitor tracking! 🎯**
