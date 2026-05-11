# ============================================================
# Morning Affirmation Email Agent
# Sends a personalized uplifting email every morning at 6:00 AM
# Uses Claude AI to generate unique affirmations daily
# ============================================================
# SETUP:
# pip install anthropic schedule python-dotenv
#
# Create a .env file with:
# ANTHROPIC_API_KEY=your_key_here
# EMAIL_SENDER=your_gmail@gmail.com
# EMAIL_PASSWORD=your_gmail_app_password
# EMAIL_RECEIVER=your_email@gmail.com
#
# Gmail App Password setup:
# Google Account > Security > 2-Step Verification > App Passwords
# ============================================================

import anthropic
import smtplib
import schedule
import time
import os
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

# ── Configuration ────────────────────────────────────────────

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "your-api-key-here")
EMAIL_SENDER      = os.getenv("EMAIL_SENDER",   "your_gmail@gmail.com")
EMAIL_PASSWORD    = os.getenv("EMAIL_PASSWORD", "your_app_password")
EMAIL_RECEIVER    = os.getenv("EMAIL_RECEIVER", "recipient@gmail.com")

# ── Personalisation Profile ───────────────────────────────────
# Edit this to match the person receiving the emails

PROFILE = {
    "name"          : "Rajesh",
    "situation"     : "currently between jobs after a company layoff in March 2026",
    "strengths"     : [
        "deep analytical mind — finds what others miss in data",
        "4+ years of stable professional experience in Learning & Development",
        "strong SQL and data analytics skills",
        "emotionally resilient — survived multiple setbacks and kept going",
        "naturally intuitive — Revati nakshatra gives wisdom and completeness",
        "honest, reliable, and deeply committed to quality work",
    ],
    "field"         : "Data Analytics / Learning & Development",
    "goal"          : "landing the right data analyst or L&D analytics role",
    "affirmation_themes": [
        "the right opportunity is already on its way",
        "the silence is temporary — the breakthrough is near",
        "every day of preparation brings you closer",
        "you are not unlucky — you are being redirected to something better",
        "your skills are real and your value is undeniable",
        "rest is part of the journey — you are allowed to breathe",
        "late May 2026 is a turning point — keep going until then",
    ]
}

# ── Claude Prompt ─────────────────────────────────────────────

def build_prompt() -> str:
    today     = datetime.now().strftime("%A, %B %d, %Y")
    day_of_week = datetime.now().strftime("%A")
    strengths = "\n".join(f"  - {s}" for s in PROFILE["strengths"])
    themes    = "\n".join(f"  - {t}" for t in PROFILE["affirmation_themes"])

    return f"""
You are a warm, wise, deeply encouraging life coach writing a personal morning email.

Today is {today}.

You are writing to {PROFILE["name"]}, who is {PROFILE["situation"]}.

Their genuine strengths are:
{strengths}

Their goal is: {PROFILE["goal"]}

Themes to weave in naturally (do not list them — weave them):
{themes}

Write a personal, uplifting morning email that:
1. Opens with a warm good morning greeting for {day_of_week}
2. Includes 3 to 5 powerful personalised affirmations (numbered, bold the key phrase)
3. Reminds them of 2 specific strengths they may be forgetting right now
4. Gives one gentle, practical encouragement for today (not generic — make it specific to their situation)
5. Closes with a warm reassurance that the right opportunity is already moving toward them
6. Signs off as "Your Morning Coach"

Rules:
- Write as if you genuinely know and care about this person
- Do NOT use generic motivational clichés like "believe in yourself" or "you got this"
- Be specific, warm, and human — not corporate
- Keep it under 350 words
- Use plain text — no markdown symbols, no asterisks, no hashtags
- Make each email feel fresh and different from yesterday
- Vary the opening each day so it never feels like a template
"""

# ── Generate Email with Claude ────────────────────────────────

def generate_email_content() -> dict:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Generating email with Claude...")

    client   = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    response = client.messages.create(
        model      = "claude-sonnet-4-20250514",
        max_tokens = 1000,
        messages   = [{"role": "user", "content": build_prompt()}]
    )

    body    = response.content[0].text
    today   = datetime.now().strftime("%B %d")
    subject = f"Good morning {PROFILE['name']} — Your {today} morning message"

    return {"subject": subject, "body": body}

# ── Build HTML Email ──────────────────────────────────────────

def build_html_email(body: str) -> str:
    paragraphs = body.strip().split("\n")
    html_body  = ""
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        # Number lines get styled as affirmations
        if para and para[0].isdigit() and "." in para[:3]:
            html_body += f'<p style="margin:0 0 12px; padding:12px 16px; background:#f0f9ff; border-left:3px solid #00BCEB; border-radius:4px; color:#1a1a1a; font-size:15px;">{para}</p>'
        else:
            html_body += f'<p style="margin:0 0 14px; color:#333; font-size:15px; line-height:1.7;">{para}</p>'

    today_str = datetime.now().strftime("%A, %B %d, %Y")

    return f"""
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0; padding:0; background:#f5f5f0; font-family: Georgia, serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f5f0; padding:40px 20px;">
    <tr><td align="center">
      <table width="580" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 2px 20px rgba(0,0,0,0.08);">

        <!-- Header -->
        <tr>
          <td style="background:linear-gradient(135deg,#001f3f,#003d7a); padding:32px 40px; text-align:center;">
            <p style="margin:0; color:#00BCEB; font-size:12px; letter-spacing:3px; text-transform:uppercase; font-family:Arial,sans-serif;">Your Morning Message</p>
            <h1 style="margin:8px 0 4px; color:#ffffff; font-size:26px; font-weight:normal; font-family:Georgia,serif;">Good Morning, {PROFILE['name']}</h1>
            <p style="margin:0; color:#7fb3d3; font-size:13px; font-family:Arial,sans-serif;">{today_str}</p>
          </td>
        </tr>

        <!-- Sun icon row -->
        <tr>
          <td style="background:#fffdf5; padding:20px; text-align:center; border-bottom:1px solid #f0ede0;">
            <span style="font-size:28px;">☀️</span>
            <p style="margin:8px 0 0; color:#888; font-size:12px; font-family:Arial,sans-serif; letter-spacing:1px; text-transform:uppercase;">A new day — a new beginning</p>
          </td>
        </tr>

        <!-- Body -->
        <tr>
          <td style="padding:36px 40px;">
            {html_body}
          </td>
        </tr>

        <!-- Footer -->
        <tr>
          <td style="background:#f9f9f7; padding:20px 40px; border-top:1px solid #eeebe0; text-align:center;">
            <p style="margin:0; color:#aaa; font-size:12px; font-family:Arial,sans-serif;">
              Sent with care every morning at 6:00 AM<br>
              Your personal AI Morning Coach
            </p>
          </td>
        </tr>

      </table>
    </td></tr>
  </table>
</body>
</html>
"""

# ── Send Email via Gmail SMTP ─────────────────────────────────

def send_email(subject: str, body: str, html: str):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Sending email to {EMAIL_RECEIVER}...")

    msg                    = MIMEMultipart("alternative")
    msg["Subject"]         = subject
    msg["From"]            = f"Morning Coach <{EMAIL_SENDER}>"
    msg["To"]              = EMAIL_RECEIVER

    msg.attach(MIMEText(body, "plain"))
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Email sent successfully!")
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Failed to send email: {e}")

# ── Main Job ──────────────────────────────────────────────────

def send_morning_email():
    print(f"\n{'='*50}")
    print(f"Morning Email Agent — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")

    try:
        content = generate_email_content()
        html    = build_html_email(content["body"])
        send_email(content["subject"], content["body"], html)
    except Exception as e:
        print(f"Agent error: {e}")

# ── Preview Mode — test without sending ──────────────────────

def preview_email():
    print("\nPREVIEW MODE — generating email content...\n")
    content = generate_email_content()
    print(f"SUBJECT: {content['subject']}")
    print("-" * 50)
    print(content["body"])
    print("-" * 50)
    print("(Email not sent — preview only)")

# ── Scheduler ─────────────────────────────────────────────────

def run_agent():
    print(f"\n{'='*50}")
    print("Morning Affirmation Email Agent")
    print(f"Scheduled: 6:00 AM daily to {EMAIL_RECEIVER}")
    print(f"{'='*50}\n")

    # Schedule daily at 6:00 AM
    schedule.every().day.at("06:00").do(send_morning_email)

    print("Agent running... Press Ctrl+C to stop.")
    print("Waiting for 6:00 AM...\n")

    while True:
        schedule.run_pending()
        time.sleep(30)     # check every 30 seconds


# ── Entry Point ───────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        # python morning_affirmation_agent.py preview
        preview_email()
    elif len(sys.argv) > 1 and sys.argv[1] == "now":
        # python morning_affirmation_agent.py now
        send_morning_email()
    else:
        # python morning_affirmation_agent.py
        run_agent()
