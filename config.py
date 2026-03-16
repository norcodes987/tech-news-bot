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
    "ChatGPT",
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

# =============================================================================
# TECH BOT
# =============================================================================
 
TECH_SUBREDDITS = [
    # AI & Machine Learning
    "MachineLearning",
    "artificial",
    "LocalLLaMA",
    "singularity",
 
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
 
TECH_CATEGORIES = {
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
 
TECH_DEDUPE_FILE   = "seen_urls_tech.txt"
TECH_EMAIL_SUBJECT = "🖥️ Your Daily Tech Digest"
 
# =============================================================================
# FINANCE BOT
# =============================================================================
 
FINANCE_SUBREDDITS = [
    # General Finance & Personal Finance
    "personalfinance",
    "financialindependence",
    "frugal",
    "povertyfinance",
 
    # Investing & Stock Market
    "investing",
    "stocks",
    "Bogleheads"
 
    # Singapore-Specific
    "singaporefi",
    "SgHENRY",
 
    # Crypto
    "CryptoCurrency",
]
 
FINANCE_CATEGORIES = {
    "Personal Finance": [
        "budget", "budgeting", "debt", "savings", "emergency fund",
        "credit card", "credit score", "mortgage", "rent", "insurance",
        "frugal", "saving money", "expense", "income", "salary",
        "cpf", "srs", "medisave", "singpass",
    ],
    "Investing": [
        "invest", "investing", "portfolio", "stock", "equity", "shares",
        "index fund", "etf", "mutual fund", "bogle", "vanguard",
        "asset allocation", "rebalance", "dollar cost", "dca",
        "passive investing", "long term", "compound",
    ],
    "Stock Market": [
        "earnings", "ipo", "nyse", "nasdaq", "s&p", "sp500", "dow",
        "bull", "bear", "market crash", "rally", "correction",
        "valuation", "pe ratio", "dividend", "buyback", "analyst",
        "quarterly results", "guidance", "revenue",
    ],
    "FIRE": [
        "fire", "financial independence", "retire early", "lean fire",
        "fat fire", "coast fire", "barista fire", "4% rule",
        "safe withdrawal", "passive income", "financial freedom",
    ],
    "Singapore Finance": [
        "cpf", "srs", "singapore", "sgd", "mas", "dbs", "ocbc", "uob",
        "syfe", "endowus", "stashaway", "tiger", "moomoo", "ibkr",
        "hdb", "bto", "condo", "sgx", "reits", "t-bills", "ssb",
        "singapore savings bond", "sgs", "gst",
    ],
    "Crypto": [
        "bitcoin", "btc", "ethereum", "eth", "crypto", "cryptocurrency",
        "defi", "nft", "blockchain", "altcoin", "stablecoin",
        "binance", "coinbase", "web3", "solana", "polygon",
    ],
    "Macro & Economy": [
        "fed", "federal reserve", "interest rate", "inflation", "cpi",
        "gdp", "recession", "economy", "unemployment", "central bank",
        "monetary policy", "fiscal", "bond yield", "treasury",
        "dollar", "forex", "currency",
    ],
}
 
FINANCE_DEDUPE_FILE   = "seen_urls_finance.txt"
FINANCE_EMAIL_SUBJECT = "💰 Your Daily Finance Digest"
# -----------------------------------------------------------------------------
# OUTPUT SETTINGS
# -----------------------------------------------------------------------------
# Legacy fields (kept for compatibility)
OUTPUT_DIR      = "output"
OUTPUT_PREFIX   = "tech_news"
DEDUPE_LOG_FILE = "seen_urls_tech.txt"
CATEGORIES      = TECH_CATEGORIES
SUBREDDITS      = TECH_SUBREDDITS
EMAIL_SUBJECT   = TECH_EMAIL_SUBJECT
# -----------------------------------------------------------------------------
# EMAIL SETTINGS
# -----------------------------------------------------------------------------
# The bot sends a daily HTML digest email via Gmail's SMTP server.
#
# How to get a Gmail App Password (required — Google blocks regular passwords):
# 1. Go to https://myaccount.google.com/security
# 2. Make sure 2-Step Verification is turned ON
# 3. Search "App passwords" in the search bar at the top
# 4. Click App passwords → create one named "reddit-bot"
# 5. Google will show you a 16-character password — paste it below
#
# IMPORTANT: Never commit this file to a public GitHub repo with real credentials.
# Use environment variables for GitHub Actions (instructions in README.md)
GMAIL_SENDER    = "automationupdates396@gmail.com"
GMAIL_APP_PASS  = "usqh hicu prvc oksq"
EMAIL_RECIPIENT = "automationupdates396@gmail.com"