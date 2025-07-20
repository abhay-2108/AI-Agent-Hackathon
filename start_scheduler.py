#!/usr/bin/env python3
"""
Startup script for Competitor Feature Tracker Scheduler
This script can be used to run the scheduler as a service with proper error handling.
"""

import os
import sys
import time
import logging
from datetime import datetime
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)

def check_environment():
    """Check if the environment is properly set up."""
    logging.info("Checking environment...")
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        logging.error("main.py not found. Please run this script from the project root directory.")
        return False
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        logging.warning("Virtual environment not detected. Consider activating it for better dependency management.")
    
    # Check if .env file exists
    if not Path(".env").exists():
        logging.warning(".env file not found. Some features may not work without API keys.")
        logging.info("Run 'python setup.py' to create a .env file with placeholder values.")
    
    return True

def start_scheduler():
    """Start the scheduler with error handling."""
    try:
        logging.info("Starting Competitor Feature Tracker Scheduler...")
        
        # Import and start the scheduler
        from scheduler.job_scheduler import start_scheduler as run_scheduler
        
        logging.info("Scheduler started successfully")
        run_scheduler()
        
    except KeyboardInterrupt:
        logging.info("Scheduler stopped by user")
    except Exception as e:
        logging.error(f"Error starting scheduler: {e}")
        return False
    
    return True

def main():
    """Main function."""
    print("🚀 Competitor Feature Tracker Scheduler")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        print("❌ Environment check failed. Please fix the issues above.")
        return False
    
    # Start scheduler
    if not start_scheduler():
        print("❌ Failed to start scheduler.")
        return False
    
    print("✅ Scheduler stopped gracefully.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 