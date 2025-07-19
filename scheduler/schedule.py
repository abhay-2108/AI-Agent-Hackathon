# scheduler/schedule.py

import schedule
import time
import subprocess
import os
from datetime import datetime

def job():
    """
    Main job function that runs the competitor tracking workflow.
    """
    print(f"Starting Competitor Feature Tracker at {datetime.now()}")
    try:
        # Run the main tracking script
        result = subprocess.run(["python", "main.py"], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("Competitor tracking job completed successfully")
            if result.stdout:
                print("Output:", result.stdout)
        else:
            print("Competitor tracking job failed")
            if result.stderr:
                print("Error:", result.stderr)
                
    except subprocess.TimeoutExpired:
        print("Competitor tracking job timed out after 5 minutes")
    except Exception as e:
        print(f"Error running competitor tracking job: {e}")

def start_scheduler():
    """
    Start the scheduler with various job schedules.
    """
    # Schedule jobs
    schedule.every().monday.at("09:00").do(job)  # Weekly on Monday at 9 AM
    schedule.every().wednesday.at("09:00").do(job)  # Weekly on Wednesday at 9 AM
    schedule.every().friday.at("09:00").do(job)  # Weekly on Friday at 9 AM
    
    # For testing, you can also run every hour
    # schedule.every().hour.do(job)
    
    print("Scheduler started. Jobs scheduled:")
    print("- Monday at 09:00")
    print("- Wednesday at 09:00") 
    print("- Friday at 09:00")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\nScheduler stopped by user")

def run_once():
    """
    Run the job once immediately (for testing).
    """
    print("Running competitor tracking job once...")
    job()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "once":
        run_once()
    else:
        start_scheduler() 