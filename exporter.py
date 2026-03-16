# =============================================================================
# exporter.py — CSV Exporter + Deduplication
# =============================================================================
# take categorized posts, remove duplicates,
# and write the results to a date-stamped CSV file.
# =============================================================================

import os
import csv
import logging
from datetime import datetime
from datetime import datetime, timezone
from config import OUTPUT_DIR, OUTPUT_PREFIX, DEDUPE_LOG_FILE

logger = logging.getLogger(__name__)

CSV_COLUMNS = [
    "category",
    "title",
    "score",
    "num_comments",
    "subreddit",
    "author",
    "created_at",
    "reddit_url",
    "external_url",
]

# =============================================================================
# DEDUPLICATION
# =============================================================================

def load_seen_urls(dedupe_file: str = None) -> set:
    """
    Loads the set of Reddit URLs we've already exported in previous runs.
    If the log file doesn't exist yet (first run), returns an empty set.

    Returns:
        A set of URL strings we've previously exported.
    """
    filepath = dedupe_file if dedupe_file else DEDUPE_LOG_FILE
    if not os.path.exists(filepath):
        logger.info("No dedupe log found - this looks like the fist run.")
        return set()
    
    with open(DEDUPE_LOG_FILE, "r") as f:
        urls = set(line.strip() for line in f if line.strip())
    
    logger.info(f"Loaded {len(urls)} previously seen URLs from dedupe log.")
    return urls

def save_seen_urls(urls: set, dedupe_file: str = None) -> None:
    """
    Saves the updated set of seen URLs back to the log file.
    Appends new URLs to the existing log (doesn't overwrite).
 
    Args:
        urls: Set of new URL strings to add to the log.
    """
    filepath = dedupe_file if dedupe_file else DEDUPE_LOG_FILE
    with open(filepath, "a") as f:
        for url in urls:
            f.write(url + "\n")
    logger.info(f"Saved {len(urls)} new URLs to dedupe log")

def deduplicate_posts(posts: list[dict], seen_urls: set) -> tuple[list[dict], set]:
    """
    Filters out posts whose Reddit URLs have already been exported.
 
    Args:
        posts:      Full list of categorized posts from this run.
        seen_urls:  Set of URLs from previous runs (loaded from log file).
 
    Returns:
        A tuple of:
            - filtered_posts: Only posts we haven't seen before
            - new_urls:       The set of NEW urls from this run (to save to log)
    """
    filtered_posts = []
    new_urls = set()

    for post in posts:
        url = post["reddit_url"]
        if url not in seen_urls:
            filtered_posts.append(post)
            new_urls.add(url)
        # else: silently skip - it's a duplicate
    duplicates_removed = len(posts) - len(filtered_posts)
    logger.info(
        f"Deduplication: {len(filtered_posts)} new posts kept, "
        f"{duplicates_removed} duplicates removed"
    )
    return filtered_posts, new_urls


if __name__ == "__main__":
    # Usage: python exporter.py
    test_posts = [
        {
            "category": "AI / ML",
            "title": "OpenAI releases GPT-5",
            "score": 1500,
            "num_comments": 340,
            "subreddit": "artificial",
            "author": "techuser1",
            "created_at": "2026-03-11 07:00 UTC",
            "reddit_url": "https://www.reddit.com/r/artificial/comments/abc123",
            "external_url": "https://openai.com/blog/gpt-5",
        },
        {
            "category": "Coding",
            "title": "Why Rust is replacing C++ in systems programming",
            "score": 800,
            "num_comments": 210,
            "subreddit": "programming",
            "author": "devguru",
            "created_at": "2026-03-11 06:30 UTC",
            "reddit_url": "https://www.reddit.com/r/programming/comments/def456",
            "external_url": "https://blog.example.com/rust-vs-cpp",
        },
    ]
 