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

def load_seen_urls() -> set:
    """
    Loads the set of Reddit URLs we've already exported in previous runs.
    If the log file doesn't exist yet (first run), returns an empty set.

    Returns:
        A set of URL strings we've previously exported.
    """
    if not os.path.exists(DEDUPE_LOG_FILE):
        logger.info("No dedupe log found - this looks like the fist run.")
        return set()
    
    with open(DEDUPE_LOG_FILE, "r") as f:
        urls = set(line.strip() for line in f if line.strip())
    
    logger.info(f"Loaded {len(urls)} previously seen URLs from dedupe log.")
    return urls

def save_seen_urls(urls: set) -> None:
    """
    Saves the updated set of seen URLs back to the log file.
    Appends new URLs to the existing log (doesn't overwrite).
 
    Args:
        urls: Set of new URL strings to add to the log.
    """
    with open(DEDUPE_LOG_FILE, "a") as f:
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


# =============================================================================
# CSV EXPORT
# =============================================================================

def get_output_filepath() -> str:
    """
    Generates a date-stamped file path for today's CSV.
 
    Example output: "output/tech_news_2026-03-11.csv"
 
    Returns:
        Full relative file path as a string.
    """
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    filename = f"{OUTPUT_PREFIX}_{today}.csv"
    return os.path.join(OUTPUT_DIR, filename)

 
def export_to_csv(posts: list[dict]) -> str:
    """
    Main export function. Handles deduplication and writes a sorted CSV.
 
    The CSV is sorted by category first, then by score (highest first)
    so it reads like a clean report when you open it.
 
    Args:
        posts: List of categorized post dicts from categorizer.
 
    Returns:
        The file path of the written CSV, or empty string if nothing to export.
    """
    if not posts:
        logger.warning("No posts to export.")
        return ""
    
    # load seen URLs and deduplicate
    seen_urls = load_seen_urls()
    fresh_posts, new_urls = deduplicate_posts(posts, seen_urls)

    if not fresh_posts:
        logger.info("All posts were duplicates from previous runs. Nothing new to export.")
        return ""
    
    # sort posts - by category alphabetically, then by score descending
    fresh_posts.sort(key=lambda p: (p["category"], -p["score"]))

    # create output directory if it dosen't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # write to csv
    filepath = get_output_filepath()

    with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(fresh_posts)
    logger.info(f"CSV exported: {filepath} ({len(fresh_posts)} posts)")

    # save seen urls to dedupe log so tomorrow's run skios them
    save_seen_urls(new_urls)
    return filepath


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
 
    output_path = export_to_csv(test_posts)
    print(f"\nTest CSV written to: {output_path}")