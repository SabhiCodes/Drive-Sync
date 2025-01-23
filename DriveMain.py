import schedule
import time
import signal
from DriveOprtn import DriveManag
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler("DriveMain.log"),  # Log to a file named 'scheduler.log'
        logging.StreamHandler(sys.stdout)      # Also log to the console
    ]
)

schedule.every().tuesday.at("09:30").do(DriveManag.ManageFiles)
schedule.every().tuesday.at("12:00").do(DriveManag.ManageFiles)
schedule.every().tuesday.at("15:00").do(DriveManag.ManageFiles)
schedule.every().tuesday.at("18:00").do(DriveManag.ManageFiles)
schedule.every().tuesday.at("20:30").do(DriveManag.ManageFiles)

schedule.every().thursday.at("09:30").do(DriveManag.ManageFiles)
schedule.every().thursday.at("12:00").do(DriveManag.ManageFiles)
schedule.every().thursday.at("15:00").do(DriveManag.ManageFiles)
schedule.every().thursday.at("18:00").do(DriveManag.ManageFiles)
schedule.every().thursday.at("20:30").do(DriveManag.ManageFiles)

schedule.every().saturday.at("09:30").do(DriveManag.ManageFiles)
schedule.every().saturday.at("12:00").do(DriveManag.ManageFiles)
schedule.every().saturday.at("15:00").do(DriveManag.ManageFiles)
schedule.every().saturday.at("18:00").do(DriveManag.ManageFiles)
schedule.every().saturday.at("20:30").do(DriveManag.ManageFiles)


def signal_handler(sig, frame):
    logging.info("Exiting...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


if __name__ == "__main__":
    logging.info("Starting DriveMain File...")
    while True:
        schedule.run_pending() 
        time.sleep(1)  # Wait for 1 hour before the next check (3600 seconds) but for now it is 1 seconds
    
# The issue here is that the schedule.run_pending() function checks and runs jobs that are scheduled to run at the current time.
#  If no jobs are scheduled to run at the exact moment run_pending() is called, it will not execute any jobs. 
# Since we didn't specify a time for the jobs, they won't run unless it is exactly at midnight (00:00). 
# 