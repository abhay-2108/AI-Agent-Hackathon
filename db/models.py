import sqlite3
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_PATH = "tracker.db"

def init_db():
    """Initialize the database with tables for all competitor update types."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create table for all competitor updates
    c.execute("""
        CREATE TABLE IF NOT EXISTS competitor_updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_type TEXT NOT NULL,
            source_url TEXT,
            content TEXT,
            summary TEXT,
            competitor_name TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create index for faster lookups
    c.execute("""
        CREATE INDEX IF NOT EXISTS idx_source_url 
        ON competitor_updates(source_url)
    """)
    
    c.execute("""
        CREATE INDEX IF NOT EXISTS idx_timestamp 
        ON competitor_updates(timestamp)
    """)
    
    conn.commit()
    conn.close()

def save_update(source_type, source_url, content, summary, competitor_name=None):
    """Save a competitor update to the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO competitor_updates 
        (source_type, source_url, content, summary, competitor_name) 
        VALUES (?, ?, ?, ?, ?)
    """, (source_type, source_url, content, summary, competitor_name))
    conn.commit()
    conn.close()

def get_last_update(source_url):
    """Get the last update for a specific source URL."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT content FROM competitor_updates 
        WHERE source_url = ? 
        ORDER BY timestamp DESC LIMIT 1
    """, (source_url,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def get_weekly_updates():
    """Get all updates from the last week for digest."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT source_type, source_url, summary, competitor_name, timestamp
        FROM competitor_updates 
        WHERE timestamp >= datetime('now', '-7 days')
        ORDER BY timestamp DESC
    """)
    rows = c.fetchall()
    conn.close()
    
    updates = []
    for row in rows:
        updates.append({
            'source_type': row[0],
            'source_url': row[1],
            'summary': row[2],
            'competitor_name': row[3],
            'timestamp': row[4]
        })
    return updates

def get_competitor_updates(competitor_name, days=7):
    """Get updates for a specific competitor."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT source_type, source_url, summary, timestamp
        FROM competitor_updates 
        WHERE competitor_name = ? AND timestamp >= datetime('now', '-{} days')
        ORDER BY timestamp DESC
    """.format(days), (competitor_name,))
    rows = c.fetchall()
    conn.close()
    
    updates = []
    for row in rows:
        updates.append({
            'source_type': row[0],
            'source_url': row[1],
            'summary': row[2],
            'timestamp': row[3]
        })
    return updates 