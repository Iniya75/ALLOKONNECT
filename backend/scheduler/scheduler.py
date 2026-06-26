"""
APScheduler configuration — fires at 06:00, 10:00, 14:00, 18:00 IST daily.
Category rotation is managed internally by PlannerAgent via category_state.json.
"""

from apscheduler.schedulers.background import BackgroundScheduler
from zoneinfo import ZoneInfo
from .jobs import update_news

IST = ZoneInfo("Asia/Kolkata")

scheduler = BackgroundScheduler(timezone=IST)

# Four daily triggers — 4-hour intervals
for trigger_hour in (6, 10, 14, 18):
    scheduler.add_job(update_news, "cron", hour=trigger_hour, minute=0)


def start_scheduler():
    scheduler.start()
    print("[Scheduler] Started - runs at 06:00, 10:00, 14:00, 18:00 IST")
