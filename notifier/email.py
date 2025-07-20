import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from .formatters import MessageFormatter

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
EMAIL_FROM = os.getenv("EMAIL_FROM")


def send_email(recipient, subject, message, update_data=None):
    """
    Send an email using SMTP with both HTML and plain text content.
    
    Args:
        recipient: Email address to send to
        subject: Email subject
        message: Message content (will be overridden if update_data is provided)
        update_data: Dictionary containing update information for formatting
    """
    if not all([SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, EMAIL_FROM]):
        print("❌ SMTP configuration missing in .env file.")
        return False

    # If update_data is provided, format the message
    if update_data:
        formatter = MessageFormatter()
        html_message = formatter.format_email_message(update_data)
        subject = formatter.get_platform_specific_title(update_data, 'email')
        
        # Create plain text version
        plain = html_message
        # Remove HTML tags for plain text
        import re
        plain = re.sub(r'<[^>]+>', '', plain)
        plain = re.sub(r'\s+', ' ', plain).strip()
    else:
        # Use provided message
        html_message = message
        # Plain text fallback (strip markdown)
        plain = message.replace("**", "").replace("*", "").replace("__", "").replace("`", "")
        plain = plain.replace("\n\n", "\n").replace("•", "- ")

    # Prepare message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = recipient

    part1 = MIMEText(plain, "plain")
    part2 = MIMEText(html_message, "html")
    msg.attach(part1)
    msg.attach(part2)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(EMAIL_FROM, recipient, msg.as_string())
        try:
            print(f"✅ Email sent to {recipient}")
        except UnicodeEncodeError:
            print(f"Email sent to {recipient}")
        return True
    except Exception as e:
        try:
            print(f"❌ Failed to send email: {e}")
        except UnicodeEncodeError:
            print(f"Failed to send email: {e}")
        return False

def send_email_digest(recipient, updates):
    """
    Send a digest of multiple updates via email.
    
    Args:
        recipient: Email address to send to
        updates: List of update dictionaries
    """
    if not all([SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, EMAIL_FROM]):
        print("❌ SMTP configuration missing in .env file.")
        return False

    formatter = MessageFormatter()
    html_message = formatter.format_email_digest(updates)
    subject = formatter.get_digest_title('email')
    
    # Create plain text version
    plain = html_message
    import re
    plain = re.sub(r'<[^>]+>', '', plain)
    plain = re.sub(r'\s+', ' ', plain).strip()

    # Prepare message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = recipient

    part1 = MIMEText(plain, "plain")
    part2 = MIMEText(html_message, "html")
    msg.attach(part1)
    msg.attach(part2)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(EMAIL_FROM, recipient, msg.as_string())
        try:
            print(f"✅ Email digest sent to {recipient}")
        except UnicodeEncodeError:
            print(f"Email digest sent to {recipient}")
        return True
    except Exception as e:
        try:
            print(f"❌ Failed to send email digest: {e}")
        except UnicodeEncodeError:
            print(f"Failed to send email digest: {e}")
        return False 