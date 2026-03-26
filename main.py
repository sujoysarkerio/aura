# main.py - Master Controller (Run this file)
import time
import multiprocessing
import threading
import os
import sys
import subprocess
from datetime import datetime

print("=== Instagram Full Auto System v12.0 Started ===")

def run_instagram_creator():
    """Main Instagram creation task"""
    print(f"[{datetime.now()}] Starting Instagram creator task...")
    try:
        subprocess.run([sys.executable, "instagram_creator.py"], check=True)
    except Exception as e:
        print(f"Instagram creator error: {e}")

def run_scheduler():
    """Background scheduler"""
    while True:
        try:
            # Run every 45 seconds (adjust as needed)
            run_instagram_creator()
            time.sleep(45)
        except Exception as e:
            print(f"Scheduler error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    print("Starting full automation system...")

    # Start scheduler in background
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    print("System is running in background.")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nSystem stopped by user.")
