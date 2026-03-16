# =============================================================================
# scraper.py — Reddit Post Fetcher (no API key required)
# =============================================================================
# Uses Reddit's public JSON endpoints instead of the official API.
# Any Reddit URL can be turned into a JSON feed by appending ".json" to it.
# Example: https://www.reddit.com/r/MachineLearning/hot.json
# =============================================================================

import requests
import logging
import time
from datetime import datetime, timezone
from config import (
    POSTS_PER_SUBREDDIT,
    POST_SORT_BY,
    TIME_FILTER,
    MIN_SCORE,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# Reddit blocks requests with no User-Agent header.
# This is a polite identifier string — no credentials needed.
HEADERS = {"User-Agent": "tech-news-bot/1.0 (personal project)"}

# Be polite to Reddit's servers — wait between each subreddit request
REQUEST_DELAY_SECONDS = 2


def build_url(subreddit: str) -> str:
    """
    Builds the public JSON URL for a subreddit feed.

    Args:
        subreddit: Subreddit name without the r/ prefix, e.g. "MachineLearning"

    Returns:
        Full JSON endpoint URL, e.g.
        "https://www.reddit.com/r/MachineLearning/hot.json?limit=10"
    """
    base = f"https://www.reddit.com/r/{subreddit}/{POST_SORT_BY}.json"
    params = f"?limit={POSTS_PER_SUBREDDIT}"

    # "top" sort supports a time filter (day/week/month etc.)
    if POST_SORT_BY == "top":
        params += f"&t={TIME_FILTER}"

    return base + params


def fetch_posts(subreddits: list[str] = None) -> list[dict]:
    """
    Fetches posts from all subreddits defined in config.SUBREDDITS.

    Hits each subreddit's public JSON endpoint, parses the response,
    and returns a flat list of post dicts.

    Returns:
        A list of dicts, one per post:
            - title:        Post title
            - reddit_url:   Link to the Reddit thread
            - external_url: External link (if link post), else empty string
            - score:        Upvote count
            - num_comments: Comment count
            - subreddit:    Subreddit name
            - author:       Reddit username
            - created_at:   Human-readable UTC timestamp
    """
    all_posts = []

    active_subreddits = subreddits if subreddits is not None else SUBREDDITS
    for subreddit in active_subreddits:
        url = build_url(subreddit)

        try:
            logger.info(f"Scraping r/{subreddit}...")
            response = requests.get(url, headers=HEADERS, timeout=10)

            # Raise an exception for HTTP errors (404, 429 rate limit, etc.)
            response.raise_for_status()

            data = response.json()
            posts_data = data.get("data", {}).get("children", [])

            count = 0
            for item in posts_data:
                post = item.get("data", {})

                # Skip stickied mod posts
                if post.get("stickied"):
                    continue

                # Filter low-engagement posts
                score = post.get("score", 0)
                if score < MIN_SCORE:
                    continue

                # Convert Unix timestamp to readable string
                created_utc = post.get("created_utc", 0)
                created_at = datetime.fromtimestamp(created_utc, timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

                reddit_url = f"https://www.reddit.com{post.get('permalink', '')}"

                # is_self=True means it's a text post (no external link)
                is_self = post.get("is_self", True)
                external_url = "" if is_self else post.get("url", "")

                all_posts.append({
                    "title":        post.get("title", ""),
                    "reddit_url":   reddit_url,
                    "external_url": external_url,
                    "score":        score,
                    "num_comments": post.get("num_comments", 0),
                    "subreddit":    subreddit,
                    "author":       post.get("author", "[deleted]"),
                    "created_at":   created_at,
                })
                count += 1

            logger.info(f"  → {count} posts fetched from r/{subreddit}")

        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                logger.warning(f"Rate limited on r/{subreddit}. Waiting 30s before continuing...")
                time.sleep(30)
            else:
                logger.error(f"HTTP error scraping r/{subreddit}: {e}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error scraping r/{subreddit}: {e}")

        except Exception as e:
            logger.error(f"Unexpected error scraping r/{subreddit}: {e}")

        finally:
            # Always wait between requests, even if this one failed
            time.sleep(REQUEST_DELAY_SECONDS)

    logger.info(f"Total posts fetched: {len(all_posts)}")
    return all_posts


if __name__ == "__main__":
    posts = fetch_posts()
