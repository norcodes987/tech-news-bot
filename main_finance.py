# =============================================================================
# main_finance.py — Finance Bot Orchestrator
# =============================================================================
# Runs the finance news pipeline:
#   1. Fetch posts from finance subreddits
#   2. Categorize by finance keywords
#   3. Deduplicate against previous runs
#   4. Send HTML digest email
#
# Usage:
#   python main_finance.py
# Task Scheduler: runs daily at 8:00 AM
# =============================================================================

import logging
import sys
from emailer import send_email
from scraper import fetch_posts
from categorizer import categorize_posts
from exporter import deduplicate_posts, load_seen_urls, save_seen_urls
from config import FINANCE_SUBREDDITS, FINANCE_CATEGORIES, FINANCE_DEDUPE_FILE, FINANCE_EMAIL_SUBJECT

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)


logger = logging.getLogger(__name__)

def run():
    """
    Executes the full scrape → categorize → export pipeline.
 
    Returns:
        Send email
    """
    logger.info("=" * 60)
    logger.info("Reddit Finance News Bot — Starting run")
    logger.info("=" * 60)
 
    # ------------------------------------------------------------------
    # STEP 1: Fetch raw posts from all subreddits
    # No credentials needed — uses public JSON endpoints
    # ------------------------------------------------------------------
    try:
        raw_posts = fetch_posts(subreddits=FINANCE_SUBREDDITS)
    except Exception as e:
        logger.error(f"Failed to fetch posts: {e}")
        sys.exit(1)
 
    if not raw_posts:
        logger.warning("No posts were fetched. Check finance_subreddits in config.py.")
        return ""
    # ------------------------------------------------------------------
    # STEP 2: Categorize each post
    # ------------------------------------------------------------------
    categorized_posts = categorize_posts(raw_posts, categories=FINANCE_CATEGORIES)
    # ------------------------------------------------------------------
    # STEP 3: Deduplicate
    # ------------------------------------------------------------------
     # load seen URLs and deduplicate
    seen_urls = load_seen_urls(FINANCE_DEDUPE_FILE)
    fresh_posts, new_urls = deduplicate_posts(categorized_posts, seen_urls)
    if not fresh_posts:
        logger.info("All posts were duplicates from previous runs. Nothing new to export.")
        return ""
    
    # ------------------------------------------------------------------
    # Step 4: Send email
    # ------------------------------------------------------------------
    success = send_email(fresh_posts, subject=FINANCE_EMAIL_SUBJECT)
    # Only save seen URLs if email sent successfully
    # This way if the email fails, we'll retry those posts tomorrow
    if success:
        save_seen_urls(new_urls, FINANCE_DEDUPE_FILE)
        logger.info("=" * 60)
        logger.info(f"Done. Email sent with {len(fresh_posts)} posts.")
        logger.info("=" * 60)
    else:
        logger.info("Email failed - seen_urls not updated. Will retry tomorrow")
 
 
 
if __name__ == "__main__":
    run()

