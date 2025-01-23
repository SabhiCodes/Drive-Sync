import schedule
import time
import logging
import sys
import signal
from DeviceOprtn import ScanObj

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler("DeviceMain.log"),  # Log to a file named 'scheduler.log'
        logging.StreamHandler(sys.stdout)      # Also log to the console
    ]
)

schedule.every().monday.at("09:30").do(ScanObj.ManageFilesRecord)
schedule.every().monday.at("12:00").do(ScanObj.ManageFilesRecord)
schedule.every().monday.at("15:00").do(ScanObj.ManageFilesRecord)
schedule.every().monday.at("18:00").do(ScanObj.ManageFilesRecord)
schedule.every().monday.at("20:30").do(ScanObj.ManageFilesRecord)

schedule.every().wednesday.at("09:30").do(ScanObj.ManageFilesRecord)
schedule.every().wednesday.at("12:00").do(ScanObj.ManageFilesRecord)
schedule.every().wednesday.at("15:00").do(ScanObj.ManageFilesRecord)
schedule.every().wednesday.at("18:00").do(ScanObj.ManageFilesRecord)
schedule.every().wednesday.at("20:30").do(ScanObj.ManageFilesRecord)

schedule.every().friday.at("09:30").do(ScanObj.ManageFilesRecord)
schedule.every().friday.at("12:00").do(ScanObj.ManageFilesRecord)
schedule.every().friday.at("15:00").do(ScanObj.ManageFilesRecord)
schedule.every().friday.at("18:00").do(ScanObj.ManageFilesRecord)
schedule.every().friday.at("20:30").do(ScanObj.ManageFilesRecord)

# Define signal handler to gracefully exit
def signal_handler(sig, frame):
    logging.info("Exiting...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Main loop
if __name__ == "__main__":
    logging.info("Starting DeviceMain File...")
    while True:
        schedule.run_pending()  # Check for pending jobs and run them
        time.sleep(1)  # Wait for 2 hour before the next check (3600*2 seconds) for now it is 1 second