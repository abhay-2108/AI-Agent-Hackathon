# scheduler/job_scheduler.py

import schedule
import time
import subprocess
import os
import sys
from datetime import datetime

def job():
    """
    Main job function that runs the competitor tracking workflow.
    """
    print(f"Starting Competitor Feature Tracker at {datetime.now()}")
    try:
        # Run the main tracking script using the current Python interpreter
        result = subprocess.run([sys.executable, "main.py"], 
                              capture_output=True, text=True, timeout=600)  # Increased timeout to 10 minutes
        
        if result.returncode == 0:
            print("Competitor tracking job completed successfully")
            if result.stdout:
                print("Output:", result.stdout)
        else:
            print("Competitor tracking job failed")
            if result.stderr:
                print("Error:", result.stderr)
                
    except subprocess.TimeoutExpired:
        print("Competitor tracking job timed out after 10 minutes")
    except Exception as e:
        print(f"Error running competitor tracking job: {e}")

def digest_job():
    """
    Job function that runs the weekly digest.
    """
    print(f"Starting Weekly Digest at {datetime.now()}")
    try:
        # Run the digest script
        result = subprocess.run([sys.executable, "main.py", "digest"], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("Weekly digest completed successfully")
            if result.stdout:
                print("Output:", result.stdout)
        else:
            print("Weekly digest failed")
            if result.stderr:
                print("Error:", result.stderr)
                
    except subprocess.TimeoutExpired:
        print("Weekly digest timed out after 5 minutes")
    except Exception as e:
        print(f"Error running weekly digest: {e}")

def start_scheduler():
    """
    Start the scheduler with various job schedules.
    """
    # Schedule job for Sunday at 17:08 (5:08 PM)
    schedule.every().sunday.at("17:26").do(job)
    print("Scheduler started. Jobs scheduled:")
    print("- Sunday at 17:15 (Test run)")
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

def run_digest_once():
    """
    Run the digest job once immediately (for testing).
    """
    print("Running weekly digest once...")
    digest_job()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "once":
            run_once()
        elif sys.argv[1] == "digest":
            run_digest_once()
        elif sys.argv[1] == "help":
            print("Usage:")
            print("  python scheduler/job_scheduler.py          # Start scheduler")
            print("  python scheduler/job_scheduler.py once     # Run tracking once")
            print("  python scheduler/job_scheduler.py digest   # Run digest once")
            print("  python scheduler/job_scheduler.py help     # Show this help")
        else:
            print(f"Unknown argument: {sys.argv[1]}")
            print("Use 'help' to see available options")
    else:
        start_scheduler() 