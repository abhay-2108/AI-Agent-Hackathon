#!/usr/bin/env python3
"""
Test script to demonstrate improved rate limiting features
"""

import os
import time
from summarizer.summarize import summarize_update, should_skip_rate_limit_wait

def test_rate_limiting_improvements():
    """Test the improved rate limiting functionality."""
    print("🧪 Testing Improved Rate Limiting")
    print("=" * 50)
    
    # Test 1: Check environment variable function
    print("\n1. Testing environment variable detection:")
    print(f"   SKIP_RATE_LIMIT_WAIT: {should_skip_rate_limit_wait()}")
    print(f"   DISABLE_GEMINI_API: {os.getenv('DISABLE_GEMINI_API', 'false')}")
    
    # Test 2: Demonstrate rate limiting behavior
    print("\n2. Rate limiting behavior:")
    print("   - Global rate limiting: 30 seconds between requests")
    print("   - Rate limit detection: Automatic retry delay extraction")
    print("   - Skip options: Environment variable or Ctrl+C")
    
    # Test 3: Test summarization with fallback
    print("\n3. Testing summarization (will use fallback if no API key):")
    test_content = """
    New Feature Release: Enhanced Workflow Automation
    
    We've added powerful new workflow automation features to help teams work more efficiently:
    
    • Automated task assignment based on workload
    • Smart notification routing for support tickets
    • Integration with popular CRM systems
    • Advanced reporting and analytics dashboard
    
    These improvements will save teams up to 3 hours per week on manual tasks.
    """
    
    try:
        result = summarize_update(test_content, 'feature', 'Test Competitor')
        print("✅ Summarization completed successfully")
        print(f"Result preview: {result[:200]}...")
    except Exception as e:
        print(f"❌ Summarization failed: {e}")
    
    # Test 4: Show configuration options
    print("\n4. Configuration options:")
    print("   To disable Gemini API entirely:")
    print("   export DISABLE_GEMINI_API=true")
    print("   ")
    print("   To skip rate limit waiting:")
    print("   export SKIP_RATE_LIMIT_WAIT=true")
    print("   ")
    print("   To use both (fallback only, no waiting):")
    print("   export DISABLE_GEMINI_API=true")
    print("   export SKIP_RATE_LIMIT_WAIT=true")
    
    print("\n✅ Rate limiting improvements test completed!")
    print("\n💡 Tips:")
    print("- The system now waits only 30 seconds between requests (reduced from 60)")
    print("- You can press Ctrl+C during rate limit waits to skip them")
    print("- Set environment variables to control behavior without interruption")
    print("- Fallback summarization works without any API keys")

if __name__ == "__main__":
    test_rate_limiting_improvements() 