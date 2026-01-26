import schedule
import time
from main import run_daily

def job_domestic():
    run_daily("国内AI新闻")

def job_international():
    run_daily("国外AI新闻")

# 每天早9点与下午1点运行
schedule.every().day.at("09:00").do(job_domestic)
schedule.every().day.at("13:00").do(job_international)

while True:
    schedule.run_pending()
    time.sleep(60)
