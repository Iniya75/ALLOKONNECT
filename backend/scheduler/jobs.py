"""
Scheduler jobs — called by APScheduler every 4 hours.
"""

from workflows.news_workflow import run_news_workflow


def update_news():
    """Triggered every 4 hours to generate one new article."""
    print("\n[Scheduler] Scheduled job triggered")

    try:
        result = run_news_workflow()

        if result:
            print(
                f"[Scheduler] Completed - "
                f"Article: [{result.get('category')}] {result.get('title', '')[:60]}"
            )
        else:
            print("[Scheduler] No new article published this run")

    except Exception as e:
        print(f"[Scheduler] Job failed: {e}")