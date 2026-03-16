# Reddit Daily Digest Bot

A Python bot that scrapes Reddit every morning and sends a formatted HTML email digest, organised by category. Supports two separate digests — **Tech** and **Finance** — each with their own subreddit list, categories, and schedule.

---

## How It Works

```
Task Scheduler (7 AM / 8 AM SGT)
        ↓
  Scrape Reddit public JSON feeds
        ↓
  Categorize posts by keyword
        ↓
  Deduplicate against previous runs
        ↓
  Send HTML digest email via Gmail
```

No API keys required for scraping — uses Reddit's public `.json` endpoints.

---

## Project Structure

```
reddit-bot/
├── config.py              # ⚙️  All settings — edit this to customise the bot
├── scraper.py             # Fetches posts from Reddit
├── categorizer.py         # Assigns each post a category by keyword matching
├── exporter.py            # Deduplication logic (tracks seen posts)
├── emailer.py             # Builds and sends the HTML email
├── main.py                # Tech bot entrypoint (run this for tech digest)
├── main_finance.py        # Finance bot entrypoint (run this for finance digest)
├── requirements.txt       # Python dependencies
├── .gitignore             # Excludes secrets and runtime files from git
└── output/                # Auto-created — stores CSV files if needed
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://gitlab.com/your-username/reddit-bot.git
cd reddit-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create your config file

`config.py` is gitignored so your credentials are never committed. Create it by copying the example:

```bash
cp config.example.py config.py
```

Then open `config.py` and fill in your Gmail credentials:

```python
GMAIL_SENDER    = "your_email@gmail.com"
GMAIL_APP_PASS  = "xxxx xxxx xxxx xxxx"   # Gmail App Password (see below)
EMAIL_RECIPIENT = "your_email@gmail.com"
```

### 4. Get a Gmail App Password

Google blocks regular passwords for scripts. You need an App Password:

1. Go to [myaccount.google.com/security](https://myaccount.google.com/security)
2. Make sure **2-Step Verification** is turned ON
3. Search **"App passwords"** in the search bar
4. Create one named `reddit-bot`
5. Copy the 16-character password into `config.py`

---

## Running Locally

```bash
# Tech digest
python main.py

# Finance digest
python main_finance.py
```

Check your inbox — the email should arrive within ~2 minutes.

---

## Scheduling with Windows Task Scheduler

The bot runs on your local machine via Windows Task Scheduler. Two tasks are set up — one for each digest.

### Tech Digest (7:00 AM SGT)

1. Open **Task Scheduler** → **Create Task**
2. **General tab:**
   - Name: `Reddit Tech News Bot`
   - Select: `Run only when user is logged on`
3. **Triggers tab** → New:
   - Daily at `7:00:00 AM`
4. **Actions tab** → New:
   - Program: `C:\Users\xxx\AppData\Local\Programs\Python\Python313\python.exe`
   - Arguments: `main.py`
   - Start in: `C:\path\to\reddit-bot`
5. **Conditions tab:**
   - Uncheck `Start only if on AC power`
6. **Settings tab:**
   - Check `Run task as soon as possible after a scheduled start is missed`

### Finance Digest (8:00 AM SGT)

Repeat the steps above with:

- Name: `Reddit Finance News Bot`
- Time: `8:00:00 AM`
- Arguments: `main_finance.py`

### Find your Python path

If you're unsure of your Python path, run this in a command prompt:

```bash
where python
```

---

## Customisation

All customisation is done in `config.py` — you never need to edit the other files.

### Add or remove subreddits

```python
TECH_SUBREDDITS = [
    "MachineLearning",
    "programming",
    # Add more here...
]

FINANCE_SUBREDDITS = [
    "investing",
    "singaporefi",
    # Add more here...
]
```

### Add or remove categories

```python
TECH_CATEGORIES = {
    "AI / ML": ["ai", "llm", "openai", ...],
    "Coding":  ["python", "typescript", ...],
    # Add a new category:
    "Cloud":   ["aws", "azure", "gcp", "serverless", ...],
}
```

Category order matters — the **first matching category wins**. Put more specific categories above more general ones.

### Change how many posts are fetched

```python
POSTS_PER_SUBREDDIT = 10   # Posts per subreddit per run
MIN_SCORE           = 10   # Minimum upvotes (filters out low-quality posts)
POST_SORT_BY        = "hot"  # Options: "hot", "new", "top", "rising"
```

---

## Email Categories & Emojis

### Tech Digest

| Emoji | Category    |
| ----- | ----------- |
| 🤖    | AI / ML     |
| 💻    | Coding      |
| 🌐    | Web Dev     |
| 🛠️    | Dev Tools   |
| 📖    | Open Source |
| 🚀    | Startups    |
| 🔒    | Security    |
| ⚙️    | Hardware    |
| 📌    | General     |

### Finance Digest

| Emoji | Category          |
| ----- | ----------------- |
| 💳    | Personal Finance  |
| 📈    | Investing         |
| 📊    | Stock Market      |
| 🔥    | FIRE              |
| 🇸🇬    | Singapore Finance |
| ₿     | Crypto            |
| 🌍    | Macro & Economy   |

---

## Deduplication

The bot tracks every post it has already emailed so repeat posts don't appear across multiple days.

- Tech posts → tracked in `seen_urls_tech.txt`
- Finance posts → tracked in `seen_urls_finance.txt`

These files are auto-created on first run and grow over time. They are gitignored and local to your machine.

> **Note:** If you set up the bot on a new machine, these files won't exist and the first run will include older posts that are still in the hot feed. This is normal — deduplication kicks in from the second run onwards.

To reset deduplication (e.g. after a long break):

```bash
del seen_urls_tech.txt
del seen_urls_finance.txt
```

---

## Troubleshooting

**Bot runs but no email arrives**

- Check your Gmail App Password is correct in `config.py`
- Make sure 2-Step Verification is enabled on your Google account
- Check your spam folder

**403 errors when scraping**

- Reddit blocks requests from cloud/datacenter IPs (e.g. GitHub Actions)
- Running locally via Task Scheduler avoids this — your home IP is not blocked
- If it happens locally, Reddit may be temporarily rate-limiting — try again later

**Duplicate posts appearing**

- Delete `seen_urls_tech.txt` or `seen_urls_finance.txt` and restart
- The dedup log may have been corrupted

**Task Scheduler doesn't run the bot**

- Right click the task → **Run** to test it manually
- Check **History** tab for error codes
- Make sure the Python path and Start In folder are both correct

**No posts fetched**

- A subreddit may have been renamed or made private
- Check the subreddit names in `config.py` are correct (case-sensitive)

---

## Dependencies

| Package    | Version | Purpose                                  |
| ---------- | ------- | ---------------------------------------- |
| `requests` | 2.31.0  | HTTP requests to Reddit's JSON endpoints |
| `pandas`   | 3.0.1   | Data handling                            |

Python 3.13+ required.
