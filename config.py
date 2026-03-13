import os


# -----------------------------------------------------------------------------
# SUBREDDITS TO SCRAPE
# -----------------------------------------------------------------------------
# The bot will scrape the top posts from each of these every morning.

SUBREDDITS = [
    # AI & Machine Learning
    "MachineLearning",
    "artificial",
    "LocalLLaMA",
    "singularity",
    "ChatGPT"
    "ClaudeAI"

    # General Programming & Coding
    "programming",
    "learnprogramming",
    "coding",

    # Web Development
    "webdev",
    "frontend",
    "javascript",

    # Dev Tools & Open Source
    "devops",
    "opensource",

    # Tech Industry & News
    "technology",
    "technews",
    "startups",

    # Security
    "netsec",
    "cybersecurity",
]


# -----------------------------------------------------------------------------
# SCRAPING SETTINGS
# -----------------------------------------------------------------------------

POSTS_PER_SUBREDDIT = 10   # Pull top 10 posts per subreddit
POST_SORT_BY        = "hot"  # Options: "hot", "new", "top", "rising"
TIME_FILTER         = "day"  # Only relevant for sort_by="top". Options: "day", "week"
MIN_SCORE           = 10     # Skip posts with fewer upvotes than this

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
        "ai", "artificial intelligence", "machine learning", "ml", "llm",
        "gpt", "chatgpt", "claude", "gemini", "openai", "anthropic",
        "deep learning", "neural", "transformer", "diffusion", "stable diffusion",
        "ollama", "fine-tun", "rag", "vector", "embedding", "llama",
        "mistral", "copilot", "midjourney", "dall-e", "hugging face",
    ],
    "Coding": [
        "python", "javascript", "typescript", "rust", "golang", "java",
        "c++", "kotlin", "swift", "algorithm", "data structure",
        "leetcode", "interview", "compiler", "interpreter", "syntax",
        "programming language", "backend", "api", "rest", "graphql",
    ],
    "Web Dev": [
        "react", "nextjs", "next.js", "vue", "angular", "svelte",
        "css", "html", "tailwind", "frontend", "web development",
        "vercel", "netlify", "cloudflare", "browser", "dom",
        "fullstack", "full-stack", "full stack",
    ],
    "Dev Tools": [
        "vscode", "vs code", "github", "gitlab", "git", "docker",
        "kubernetes", "k8s", "ci/cd", "devops", "linux", "terminal",
        "cli", "bash", "shell", "homebrew", "package manager",
        "debugging", "profiling", "testing", "jest", "pytest",
    ],
    "Open Source": [
        "open source", "opensource", "open-source", "self-hosted",
        "self host", "foss", "free software", "mit license", "apache",
        "github release", "new release", "v1.0", "launch",
    ],
    "Startups": [
        "startup", "founder", "funding", "seed", "series a", "series b",
        "vc", "venture capital", "yc", "y combinator", "product hunt",
        "saas", "b2b", "bootstrapped", "mrr", "arr", "pivot",
    ],
    "Security": [
        "security", "vulnerability", "exploit", "hack", "breach",
        "malware", "ransomware", "phishing", "zero-day", "cve",
        "encryption", "privacy", "vpn", "firewall", "penetration",
        "cybersecurity", "infosec",
    ],
    "Hardware": [
        "gpu", "cpu", "chip", "nvidia", "amd", "intel", "apple silicon",
        "m1", "m2", "m3", "raspberry pi", "arduino", "fpga",
        "quantum", "semiconductor", "transistor",
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
