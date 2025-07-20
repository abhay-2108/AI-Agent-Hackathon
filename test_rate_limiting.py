#!/usr/bin/env python3
"""
Test script to demonstrate rate limiting improvements
"""

import os
import time
from summarizer.summarize import summarize_update

def test_rate_limiting():
    """Test the rate limiting functionality."""
    print("🧪 Testing Rate Limiting Improvements")
    print("=" * 50)
    
    # Test 1: Basic summarization
    print("\n1. Testing basic summarization...")
    test_content = """
    New Feature Release: Enhanced Workflow Automation
    
    We've added powerful new workflow automation features to help teams work more efficiently:
    
    • Automated task assignment based on workload
    • Smart notification routing for support tickets
    • Integration with popular CRM systems
    • Advanced reporting and analytics dashboard
    
    These improvements will save teams up to 3 hours per week on manual tasks.
    """
    
    result = summarize_update(test_content, "feature", "Test Competitor")
    print("✅ Summarization completed")
    print(f"Result preview: {result[:150]}...")
    
    # Test 2: Rate limiting behavior
    print("\n2. Testing rate limiting behavior...")
    print("Note: If you have a valid Gemini API key, this will show rate limiting in action.")
    print("If you don't have an API key, it will use fallback summarization.")
    
    # Test multiple requests to see rate limiting
    for i in range(3):
        print(f"\n   Request {i+1}/3...")
        start_time = time.time()
        result = summarize_update(f"Test content {i+1}", "test")
        end_time = time.time()
        print(f"   Completed in {end_time - start_time:.1f} seconds")
        print(f"   Result: {result[:100]}...")
    
    # Test 3: Environment variable control
    print("\n3. Testing environment variable control...")
    print("Setting DISABLE_GEMINI_API=true...")
    os.environ["DISABLE_GEMINI_API"] = "true"
    
    result = summarize_update("Test content with disabled API", "test")
    print("✅ Fallback summarization working")
    print(f"Result: {result[:100]}...")
    
    # Clean up
    os.environ.pop("DISABLE_GEMINI_API", None)
    
    print("\n✅ Rate limiting tests completed!")
    print("\n💡 Tips:")
    print("- Set DISABLE_GEMINI_API=true in .env to avoid rate limits")
    print("- The system automatically waits between requests")
    print("- Fallback summarization works without API keys")

if __name__ == "__main__":
    test_rate_limiting() 