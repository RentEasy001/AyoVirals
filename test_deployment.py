#!/usr/bin/env python3
"""
Test script to verify AyoVirals deployment on Replit
"""

import requests
import time
import json
import sys
import os

def test_backend_health():
    """Test backend health endpoint"""
    try:
        print("🔍 Testing backend health...")
        response = requests.get("http://localhost:8001/api/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend health: {data.get('status', 'unknown')}")
            print(f"   Database: {data.get('database', 'unknown')}")
            print(f"   NLP: {data.get('nlp', 'unknown')}")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend health check error: {e}")
        return False

def test_personas_endpoint():
    """Test personas endpoint"""
    try:
        print("🔍 Testing personas endpoint...")
        response = requests.get("http://localhost:8001/api/personas", timeout=10)
        if response.status_code == 200:
            data = response.json()
            personas = data.get('personas', [])
            print(f"✅ Found {len(personas)} personas")
            for persona in personas[:3]:  # Show first 3
                print(f"   - {persona.get('name', 'Unknown')}")
            return True
        else:
            print(f"❌ Personas endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Personas endpoint error: {e}")
        return False

def test_video_processing():
    """Test video processing endpoint"""
    try:
        print("🔍 Testing video processing...")
        test_data = {
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "persona": "viral-trends"
        }
        
        response = requests.post(
            "http://localhost:8001/api/process-video",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Video processing successful")
            print(f"   Platform: {data.get('platform', 'unknown')}")
            print(f"   Hooks: {len(data.get('hooks', []))}")
            print(f"   Keywords: {len(data.get('keywords', []))}")
            
            # Show first hook
            hooks = data.get('hooks', [])
            if hooks:
                print(f"   Sample hook: {hooks[0][:50]}...")
            return True
        else:
            print(f"❌ Video processing failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Video processing error: {e}")
        return False

def test_frontend():
    """Test frontend accessibility"""
    try:
        print("🔍 Testing frontend...")
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
            return True
        else:
            print(f"❌ Frontend failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend error: {e}")
        return False

def main():
    """Main test runner"""
    print("🚀 AyoVirals Replit Deployment Test")
    print("=" * 50)
    
    # Wait for services to start
    print("⏳ Waiting for services to start...")
    time.sleep(10)
    
    tests = [
        ("Backend Health", test_backend_health),
        ("Personas Endpoint", test_personas_endpoint),
        ("Video Processing", test_video_processing),
        ("Frontend Access", test_frontend)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📝 Running: {test_name}")
        try:
            if test_func():
                passed += 1
            else:
                print(f"   ⚠️  {test_name} failed")
        except Exception as e:
            print(f"   ❌ {test_name} error: {e}")
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! AyoVirals is ready to use!")
        print("🌐 Open your web preview to start generating viral content!")
    else:
        print("⚠️  Some tests failed. Check the logs for more details.")
        print("💡 Try restarting the application or checking the troubleshooting guide.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)