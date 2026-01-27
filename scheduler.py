import schedule
import time
from main import run_daily,run_community_daily_report

def job_domestic():
    run_daily("国内AI新闻")

def job_international():
    run_daily("国外AI新闻")

def job_community():
    run_community_daily_report()

# 每天早9点与下午1点运行
schedule.every().monday.at("10:00").do(job_domestic)
schedule.every().monday.at("14:00").do(job_international)

schedule.every().thursday.at("10:00").do(job_domestic)
schedule.every().thursday.at("14:00").do(job_international)

schedule.every().tuesday.at("10:00").do(job_community)
schedule.every().friday.at("10:00").do(job_community)

while True:
    schedule.run_pending()
    time.sleep(60)
