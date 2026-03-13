# =============================================================================
# categorizer.py — Post Category Classifier
# =============================================================================
# take a list of raw posts and assign each one
# a category based on keyword matching against the post title.
# =============================================================================

import logging
from config import CATEGORIES

logger = logging.getLogger(__name__)

def categorize_post(title: str) -> str:
    """
    Assigns a category to a single post based on its title.

    How it works:
    - Converts the title to lowercase for case-insensitive matching
    - Checks each category's keyword list in order (order defined in config.py)
    - Returns the FIRST category whose keywords appear in the title
    - If no keywords match, returns "General"

    Args:
        title: The Reddit post title string

    Returns:
        A category string, e.g. "AI / ML", "Coding", "General"

    Example:
        categorize_post("OpenAI releases GPT-5 with reasoning capabilities")
        → "AI / ML"

        categorize_post("How I set up my home server with Docker")
        → "Dev Tools"
    """
    title_lower = title.lower()

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword.lower() in title_lower:
                return category

    return "General"

def categorize_posts(posts: list[dict]) -> list[dict]:
    """
        Runs categorize_post() on every post in the list and adds
        a "category" field to each post dict.

        Args:
            posts: List of post dicts from scraper.fetch_posts()

        Returns:
            Same list with a "category" key added to each post dict.
    """
    logger.info("Categorizing posts...")

    category_counts = {}
    
    for post in posts:
        category = categorize_post(post["title"])
        post["category"] = category

        category_counts[category] = category_counts.get(category, 0) + 1
    
    logger.info("Category breakdown:")
    for category, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        logger.info(f"  {category}: {count} posts")
    return posts

# if __name__ == "__main__":
#     test_posts = [
#         {"title": "OpenAI releases GPT-5 with improved reasoning", "score": 1500},
#         {"title": "Why I switched from Python to Rust for backend services", "score": 800},
#         {"title": "Next.js 15 is out — what's new?", "score": 600},
#         {"title": "Critical zero-day vulnerability found in OpenSSL", "score": 950},
#         {"title": "My journey bootstrapping a SaaS to $10k MRR", "score": 400},
#         {"title": "Weekend project: built a chess engine from scratch", "score": 300},
#     ]
#     result = categorize_posts(test_posts)
#     print("\n--- Categorization Test Results ---")
#     for post in result:
#         print(f"[{post['category']}] {post['title']}")
