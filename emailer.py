# =============================================================================
# emailer.py — HTML Email Generator + Gmail Sender
# =============================================================================
# Single responsibility: take categorized posts, build a formatted HTML email,
# and send it via Gmail SMTP.
# =============================================================================

import smtplib
import logging
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from collections import defaultdict
from config import (
    GMAIL_SENDER,
    GMAIL_APP_PASS,
    EMAIL_RECIPIENT,
    EMAIL_SUBJECT,
)

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# CATEGORY EMOJI MAP
# -----------------------------------------------------------------------------
CATEGORY_EMOJI = {
    "AI / ML":      "🤖",
    "Coding":       "💻",
    "Web Dev":      "🌐",
    "Dev Tools":    "🛠️",
    "Open Source":  "📖",
    "Startups":     "🚀",
    "Security":     "🔒",
    "Hardware":     "⚙️",
    "General":      "📌",
}


# =============================================================================
# HTML BUILDER
# =============================================================================

def build_email_html(posts: list[dict]) -> str:
    """
    Builds a clean HTML email from categorized posts.

    Layout:
    - Header with date
    - One section per category, sorted alphabetically
    - Each post shows: title (clickable link), subreddit, score, comment count
    - Footer with total post count

    Args:
        posts: List of categorized post dicts from categorizer.py

    Returns:
        A complete HTML string ready to be sent as an email body.
    """
    today = datetime.now(timezone.utc).strftime("%A, %d %B %Y")
    total = len(posts)

    # Group posts by category, sorted by score descending within each group
    grouped = defaultdict(list)
    for post in posts:
        grouped[post["category"]].append(post)

    for category in grouped:
        grouped[category].sort(key=lambda p: -p["score"])

    # Build category sections HTML
    sections_html = ""
    for category in sorted(grouped.keys()):
        emoji = CATEGORY_EMOJI.get(category, "📌")
        category_posts = grouped[category]
        count = len(category_posts)

        # Build individual post rows
        posts_html = ""
        for i, post in enumerate(category_posts):
            # Alternate row background for readability
            row_bg = "#ffffff" if i % 2 == 0 else "#f9f9f9"

            # Show external link if available, otherwise Reddit thread
            link = post["external_url"] if post["external_url"] else post["reddit_url"]

            posts_html += f"""
            <tr style="background-color: {row_bg};">
                <td style="padding: 10px 14px;">
                    <a href="{link}"
                       style="color: #1a1a2e; font-weight: 600; text-decoration: none;
                              font-size: 14px; line-height: 1.4;">
                        {post["title"]}
                    </a>
                    <div style="margin-top: 4px; font-size: 12px; color: #888;">
                        r/{post["subreddit"]}
                        &nbsp;·&nbsp;
                        <a href="{post["reddit_url"]}"
                           style="color: #888; text-decoration: none;">
                            💬 {post["num_comments"]} comments
                        </a>
                        &nbsp;·&nbsp;
                        ⬆️ {post["score"]}
                    </div>
                </td>
            </tr>"""

        sections_html += f"""
        <!-- {category} SECTION -->
        <tr>
            <td style="padding: 24px 0 8px 0;">
                <table width="100%" cellpadding="0" cellspacing="0" border="0"
                       style="border-radius: 8px; overflow: hidden;
                              border: 1px solid #e8e8e8;">
                    <!-- Section Header -->
                    <tr>
                        <td style="background-color: #1a1a2e; padding: 10px 14px;">
                            <span style="color: #ffffff; font-size: 15px; font-weight: 700;">
                                {emoji} {category}
                            </span>
                            <span style="color: #aaaacc; font-size: 12px;
                                         margin-left: 8px;">
                                {count} post{"s" if count != 1 else ""}
                            </span>
                        </td>
                    </tr>
                    <!-- Posts -->
                    {posts_html}
                </table>
            </td>
        </tr>"""

    # Assemble the full email
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; background-color: #f4f4f4;
             font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI',
             Roboto, Helvetica, Arial, sans-serif;">

    <table width="100%" cellpadding="0" cellspacing="0" border="0"
           style="background-color: #f4f4f4; padding: 24px 0;">
        <tr>
            <td align="center">
                <table width="620" cellpadding="0" cellspacing="0" border="0"
                       style="max-width: 620px; width: 100%;">

                    <!-- HEADER -->
                    <tr>
                        <td style="background-color: #1a1a2e; border-radius: 10px 10px 0 0;
                                   padding: 28px 24px;">
                            <div style="color: #ffffff; font-size: 22px; font-weight: 700;">
                                🗞️ Daily Tech Digest
                            </div>
                            <div style="color: #aaaacc; font-size: 13px; margin-top: 4px;">
                                {today} &nbsp;·&nbsp; {total} posts across {len(grouped)} categories
                            </div>
                        </td>
                    </tr>

                    <!-- BODY -->
                    <tr>
                        <td style="background-color: #ffffff; padding: 8px 24px 24px 24px;
                                   border-radius: 0 0 10px 10px;">
                            <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                {sections_html}
                            </table>
                        </td>
                    </tr>

                    <!-- FOOTER -->
                    <tr>
                        <td style="padding: 16px 0; text-align: center;
                                   color: #aaaaaa; font-size: 11px;">
                            Sent by your Reddit Tech News Bot &nbsp;·&nbsp;
                            Powered by Reddit public feeds
                        </td>
                    </tr>

                </table>
            </td>
        </tr>
    </table>

</body>
</html>"""

    return html


# =============================================================================
# EMAIL SENDER
# =============================================================================

def send_email(posts: list[dict]) -> bool:
    """
    Builds and sends the HTML digest email via Gmail SMTP.

    Gmail SMTP settings used:
        Host: smtp.gmail.com
        Port: 587 (TLS)

    Args:
        posts: List of categorized post dicts

    Returns:
        True if email was sent successfully, False otherwise.
    """
    if not posts:
        logger.warning("No posts to email.")
        return False

    logger.info(f"Building email with {len(posts)} posts...")

    # Build the HTML body
    html_body = build_email_html(posts)

    # Set up the email message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = EMAIL_SUBJECT
    msg["From"]    = GMAIL_SENDER
    msg["To"]      = EMAIL_RECIPIENT

    # Attach HTML part — "alternative" means fallback to plain text if HTML fails
    # We only provide HTML here since all modern email clients support it
    msg.attach(MIMEText(html_body, "html"))

    # Send via Gmail SMTP
    try:
        logger.info(f"Connecting to Gmail SMTP...")
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()           # Identify ourselves to the server
            server.starttls()       # Upgrade connection to TLS (encrypted)
            server.ehlo()           # Re-identify after TLS upgrade
            server.login(GMAIL_SENDER, GMAIL_APP_PASS)
            server.sendmail(GMAIL_SENDER, EMAIL_RECIPIENT, msg.as_string())

        logger.info(f"Email sent successfully to {EMAIL_RECIPIENT}")
        return True

    except smtplib.SMTPAuthenticationError:
        logger.error(
            "Gmail authentication failed. "
            "Make sure you're using an App Password, not your regular Gmail password. "
            "See config.py for instructions."
        )
        return False

    except smtplib.SMTPException as e:
        logger.error(f"SMTP error while sending email: {e}")
        return False

    except Exception as e:
        logger.error(f"Unexpected error sending email: {e}")
        return False


if __name__ == "__main__":
    # Quick test with dummy data — no Reddit connection needed
    # Usage: python emailer.py
    test_posts = [
        {
            "category": "AI / ML",
            "title": "OpenAI releases GPT-5 with improved reasoning",
            "score": 1500,
            "num_comments": 340,
            "subreddit": "artificial",
            "reddit_url": "https://www.reddit.com/r/artificial/comments/abc123",
            "external_url": "https://openai.com/blog/gpt-5",
        },
        {
            "category": "AI / ML",
            "title": "Local LLMs are now fast enough for real-time use",
            "score": 900,
            "num_comments": 210,
            "subreddit": "LocalLLaMA",
            "reddit_url": "https://www.reddit.com/r/LocalLLaMA/comments/xyz789",
            "external_url": "",
        },
        {
            "category": "Coding",
            "title": "Why Rust is replacing C++ in systems programming",
            "score": 800,
            "num_comments": 180,
            "subreddit": "programming",
            "reddit_url": "https://www.reddit.com/r/programming/comments/def456",
            "external_url": "https://blog.example.com/rust-vs-cpp",
        },
        {
            "category": "Security",
            "title": "Critical zero-day vulnerability found in OpenSSL",
            "score": 950,
            "num_comments": 220,
            "subreddit": "netsec",
            "reddit_url": "https://www.reddit.com/r/netsec/comments/ghi012",
            "external_url": "",
        },
    ]

    success = send_email(test_posts)
    if success:
        print("✅ Test email sent! Check your inbox.")
    else:
        print("❌ Failed to send. Check your Gmail credentials in config.py.")