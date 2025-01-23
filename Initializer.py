import subprocess
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler("Lcation of file log file save"),
        logging.StreamHandler()                
    ]
)

def DeviceMainFunc():
    logging.info("Running DeviceMainFunc")
    subprocess.run(["python","DeviceMain.py"])

def DriveMainFunc():
    logging.info("Running DriveMainFunc")
    subprocess.run(["python","DriveMain.py"])

job_schedule = {
    0: DeviceMainFunc,  # Monday
    1: DriveMainFunc,   # Tuesday
    2: DeviceMainFunc,  # Wednesday
    3: DriveMainFunc,   # Thursday
    4: DeviceMainFunc,  # Friday
    5: DriveMainFunc    # Saturday
}

def run_scheduled_job():
    today = datetime.now().weekday()
    if today in job_schedule:
        try:
            job_schedule[today]()
        except Exception as e:
            logging.info(f'{e}')
        return True
    return False

if __name__ == "__main__":
    logging.info("Starting scheduler...")
    try:
        job_executed = run_scheduled_job()
    except Exception as e:
        logging.info(f'{e}')
    if job_executed:
        logging.info("Job executed, exiting.")
    else:
        logging.info("No job scheduled for today, exiting.")