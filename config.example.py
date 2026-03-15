import os


# -----------------------------------------------------------------------------
# SUBREDDITS TO SCRAPE
# -----------------------------------------------------------------------------
# The bot will scrape the top posts from each of these every morning.

SUBREDDITS = [
    # AI & Machine Learning
    "MachineLearning",
   
]


# -----------------------------------------------------------------------------
# SCRAPING SETTINGS
# -----------------------------------------------------------------------------

POSTS_PER_SUBREDDIT = 1   # Pull top 10 posts per subreddit
POST_SORT_BY        = "hot"  # Options: "hot", "new", "top", "rising"
TIME_FILTER         = "day"  # Only relevant for sort_by="top". Options: "day", "week"
MIN_SCORE           = 1     # Skip posts with fewer upvotes than this

# -----------------------------------------------------------------------------
# CATEGORY KEYWORD MAP
# -----------------------------------------------------------------------------
# Each key is a category name. Each value is a list of keywords.
# The categorizer checks if ANY keyword appears in the post title (case-insensitive).
# Posts that don't match any category are labelled "General".
#
# Order matters: categories are checked top-to-bottom.
# The FIRST matching category wins.

CATEGORIES = {
    "AI / ML": [
        "ai"
    ],
    
}


# -----------------------------------------------------------------------------
# OUTPUT SETTINGS
# -----------------------------------------------------------------------------
# Where the daily CSV file will be saved locally.
# The filename will include today's date, e.g. "tech_news_2026-03-11.csv"

OUTPUT_DIR      = "output"           # Folder to save CSVs into (created automatically)
OUTPUT_PREFIX   = "tech_news"        # Prefix for the CSV filename
DEDUPE_LOG_FILE = "seen_urls.txt"    # Tracks URLs already seen to avoid duplicates across days

# -----------------------------------------------------------------------------
# EMAIL SETTINGS
# -----------------------------------------------------------------------------

#
GMAIL_SENDER    = "your_email@gmail.com"
GMAIL_APP_PASS  = "xxxx xxxx xxxx xxxx"
EMAIL_RECIPIENT = "your_email@gmail.com"