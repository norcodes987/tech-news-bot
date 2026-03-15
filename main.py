# =============================================================================
# main.py — Bot Orchestrator
# =============================================================================
#   1. Fetch posts from Reddit (no login needed)
#   2. Categorize each post by keyword
#   3. Deduplicate against previous runs
#   4. Send a formatted HTML digest email via Gmail
#
# Usage:
#   python main.py
# =============================================================================

import logging
import sys
from emailer import send_email
from scraper import fetch_posts
from categorizer import categorize_posts
from exporter import deduplicate_posts, load_seen_urls, save_seen_urls

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
        str: Path to the exported CSV file, or empty string if nothing exported.
    """
    logger.info("=" * 60)
    logger.info("Reddit Tech News Bot — Starting run")
    logger.info("=" * 60)
 
    # ------------------------------------------------------------------
    # STEP 1: Fetch raw posts from all subreddits
    # No credentials needed — uses public JSON endpoints
    # ------------------------------------------------------------------
    try:
        raw_posts = fetch_posts()
    except Exception as e:
        logger.error(f"Failed to fetch posts: {e}")
        sys.exit(1)
 
    if not raw_posts:
        logger.warning("No posts were fetched. Check subreddit names in config.py.")
        return ""
    # ------------------------------------------------------------------
    # STEP 2: Categorize each post
    # ------------------------------------------------------------------
    categorized_posts = categorize_posts(raw_posts)
    # ------------------------------------------------------------------
    # STEP 3: Deduplicate
    # ------------------------------------------------------------------
     # load seen URLs and deduplicate
    seen_urls = load_seen_urls()
    fresh_posts, new_urls = deduplicate_posts(categorized_posts, seen_urls)
    if not fresh_posts:
        logger.info("All posts were duplicates from previous runs. Nothing new to export.")
        return ""
    
    # ------------------------------------------------------------------
    # Step 4: Send email
    # ------------------------------------------------------------------
    success = send_email(fresh_posts)
    # Only save seen URLs if email sent successfully
    # This way if the email fails, we'll retry those posts tomorrow
    if success:
        save_seen_urls(new_urls)
        logger.info("=" * 60)
        logger.info(f"Done. Email sent with {len(fresh_posts)} posts.")
        logger.info("=" * 60)
    else:
        logger.info("Email failed - seen_urls not updated. Will retry tomorrow")
 
 
 
if __name__ == "__main__":
    run()
