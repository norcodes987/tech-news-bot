# =============================================================================
# main.py — Bot Orchestrator
# =============================================================================
#   1. Scrape posts from all configured subreddits (no login needed)
#   2. Categorize each post
#   3. Deduplicate against previous runs
#   4. Export to a date-stamped CSV
#
# Usage:
#   python main.py
# =============================================================================

import logging
import sys
from scraper import fetch_posts
from categorizer import categorize_posts
from exporter import export_to_csv

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
    # STEP 3 + 4: Deduplicate and export to CSV
    # ------------------------------------------------------------------
    output_path = export_to_csv(categorized_posts)
    # ------------------------------------------------------------------
    # DONE
    # ------------------------------------------------------------------
    if output_path:
        logger.info("=" * 60)
        logger.info(f"Run complete. CSV saved to: {output_path}")
        logger.info("=" * 60)
    else:
        logger.info("Run complete. No new posts to export today.")
 
    return output_path
 
 
if __name__ == "__main__":
    run()
