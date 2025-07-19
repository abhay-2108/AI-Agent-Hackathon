import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
EMAIL_FROM = os.getenv("EMAIL_FROM")


def send_email(recipient, subject, message):
    """
    Send an email using SMTP with both HTML and plain text content.
    """
    if not all([SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, EMAIL_FROM]):
        print("❌ SMTP configuration missing in .env file.")
        return False

    # Prepare message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = recipient

    # Plain text fallback (strip markdown)
    plain = message.replace("**", "").replace("*", "").replace("__", "").replace("`", "")
    plain = plain.replace("\n\n", "\n").replace("•", "- ")

    # HTML version (convert markdown basics)
    html = message
    html = html.replace("**", "<b>").replace("*", "<i>")
    html = html.replace("\n\n", "<br><br>").replace("\n", "<br>")
    html = html.replace("•", "<li>")
    html = html.replace("<li>", "<br>&bull; ")

    part1 = MIMEText(plain, "plain")
    part2 = MIMEText(html, "html")
    msg.attach(part1)
    msg.attach(part2)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(EMAIL_FROM, recipient, msg.as_string())
        print(f"✅ Email sent to {recipient}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False 