#!/usr/bin/env python3
"""
Email Debug Script
Test SMTP email functionality.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_email_credentials():
    """Check if email credentials are properly set."""
    print("🔑 Checking email credentials...")
    
    required_vars = [
        'SMTP_HOST',
        'SMTP_PORT', 
        'SMTP_USER',
        'SMTP_PASS',
        'EMAIL_FROM'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing email variables: {', '.join(missing_vars)}")
        return False
    else:
        print("✅ All email credentials found")
        print(f"   SMTP Host: {os.getenv('SMTP_HOST')}")
        print(f"   SMTP Port: {os.getenv('SMTP_PORT')}")
        print(f"   SMTP User: {os.getenv('SMTP_USER')}")
        print(f"   From Email: {os.getenv('EMAIL_FROM')}")
        return True

def test_smtp_connection():
    """Test SMTP connection."""
    print("\n🔗 Testing SMTP connection...")
    
    try:
        import smtplib
        
        smtp_host = os.getenv("SMTP_HOST")
        smtp_port = int(os.getenv("SMTP_PORT", 587))
        smtp_user = os.getenv("SMTP_USER")
        smtp_pass = os.getenv("SMTP_PASS")
        
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            print("✅ SMTP connection successful")
            return True
            
    except Exception as e:
        print(f"❌ SMTP connection failed: {e}")
        return False

def test_email_send():
    """Test sending a test email."""
    print("\n📧 Testing email send...")
    
    try:
        from notifier.email import send_email
        
        # Test with the same formatted content as Slack/Notion
        test_message = """🚨 **Test Competitor Update**

**Key Points:**
• New feature released
• Pricing updated
• UI improvements

**Details:**
This is a test email from the Competitor Tracker to verify that email notifications are working properly.
"""
        
        success = send_email(
            recipient=os.getenv("EMAIL_FROM"),  # Send to yourself for testing
            subject="🧪 Test Email - Competitor Tracker",
            message=test_message
        )
        
        if success:
            print("✅ Test email sent successfully!")
            print("   Check your inbox for the test email")
            return True
        else:
            print("❌ Test email failed")
            return False
            
    except Exception as e:
        print(f"❌ Email test error: {e}")
        return False

def main():
    """Run all email tests."""
    print("📧 Email Debug Tool")
    print("=" * 40)
    
    tests = [
        check_email_credentials,
        test_smtp_connection,
        test_email_send
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 Email is working perfectly!")
    else:
        print("⚠️  Some email tests failed. Check the output above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 