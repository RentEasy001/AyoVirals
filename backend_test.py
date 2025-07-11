#!/usr/bin/env python3
"""
Backend API Testing Suite for AyoVirals
Tests all backend endpoints and functionality
"""

import requests
import json
import time
import sys
from typing import Dict, Any, List

# Backend URL from environment
BACKEND_URL = "https://132813f0-e3e6-4e5e-a27b-0a2569f3a330.preview.emergentagent.com/api"

class BackendTester:
    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def log_result(self, test_name: str, passed: bool, details: str = ""):
        """Log test result"""
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            self.failed_tests += 1
            status = "❌ FAIL"
            
        result = f"{status} - {test_name}"
        if details:
            result += f" | {details}"
            
        self.results.append(result)
        print(result)
        
    def test_health_endpoint(self):
        """Test /api/health endpoint"""
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "status" in data and data["status"] == "healthy":
                    self.log_result("Health Endpoint", True, f"Status: {data.get('status')}, DB: {data.get('database')}")
                else:
                    self.log_result("Health Endpoint", False, f"Unexpected response: {data}")
            else:
                self.log_result("Health Endpoint", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("Health Endpoint", False, f"Exception: {str(e)}")
    
    def test_personas_endpoint(self):
        """Test /api/personas endpoint"""
        try:
            response = requests.get(f"{BACKEND_URL}/personas", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "personas" in data and isinstance(data["personas"], list):
                    personas = data["personas"]
                    expected_personas = ["nyc-drama", "luxury-rentals", "fitness-guru", "conspiracy-mode", 
                                       "lifestyle-flex", "storytime", "business-tips", "viral-trends"]
                    
                    persona_ids = [p["id"] for p in personas]
                    missing_personas = [p for p in expected_personas if p not in persona_ids]
                    
                    if len(personas) >= 8 and not missing_personas:
                        self.log_result("Personas Endpoint", True, f"Found {len(personas)} personas")
                    else:
                        self.log_result("Personas Endpoint", False, f"Missing personas: {missing_personas}")
                else:
                    self.log_result("Personas Endpoint", False, f"Invalid response format: {data}")
            else:
                self.log_result("Personas Endpoint", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("Personas Endpoint", False, f"Exception: {str(e)}")
    
    def test_process_video_endpoint(self):
        """Test /api/process-video endpoint with various scenarios"""
        
        # Test 1: Valid YouTube URL
        self.test_process_video_with_url(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ", 
            "nyc-drama", 
            "YouTube URL Processing"
        )
        
        # Test 2: Valid TikTok URL
        self.test_process_video_with_url(
            "https://www.tiktok.com/@user/video/1234567890", 
            "fitness-guru", 
            "TikTok URL Processing"
        )
        
        # Test 3: Valid Instagram URL
        self.test_process_video_with_url(
            "https://www.instagram.com/p/ABC123/", 
            "luxury-rentals", 
            "Instagram URL Processing"
        )
        
        # Test 4: Valid Twitter/X URL
        self.test_process_video_with_url(
            "https://x.com/user/status/1234567890", 
            "conspiracy-mode", 
            "Twitter/X URL Processing"
        )
        
        # Test 5: Valid Facebook URL
        self.test_process_video_with_url(
            "https://www.facebook.com/watch/?v=1234567890", 
            "storytime", 
            "Facebook URL Processing"
        )
        
        # Test 6: Invalid URL
        self.test_process_video_invalid_url()
        
        # Test 7: Missing parameters
        self.test_process_video_missing_params()
        
    def test_process_video_with_url(self, url: str, persona: str, test_name: str):
        """Test process video with specific URL and persona"""
        try:
            payload = {
                "video_url": url,
                "persona": persona
            }
            
            response = requests.post(
                f"{BACKEND_URL}/process-video", 
                json=payload, 
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ["id", "summary", "hooks", "keywords", "platform", "persona"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    # Validate data types and content
                    if (isinstance(data["hooks"], list) and len(data["hooks"]) > 0 and
                        isinstance(data["keywords"], list) and len(data["keywords"]) > 0 and
                        data["persona"] == persona):
                        
                        platform = data["platform"]
                        hooks_count = len(data["hooks"])
                        keywords_count = len(data["keywords"])
                        
                        self.log_result(test_name, True, 
                                      f"Platform: {platform}, Hooks: {hooks_count}, Keywords: {keywords_count}")
                    else:
                        self.log_result(test_name, False, "Invalid data types or empty arrays")
                else:
                    self.log_result(test_name, False, f"Missing fields: {missing_fields}")
            else:
                self.log_result(test_name, False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result(test_name, False, f"Exception: {str(e)}")
    
    def test_process_video_invalid_url(self):
        """Test process video with invalid URL"""
        try:
            payload = {
                "video_url": "not-a-valid-url",
                "persona": "nyc-drama"
            }
            
            response = requests.post(
                f"{BACKEND_URL}/process-video", 
                json=payload, 
                timeout=10
            )
            
            # Should still work but detect platform as "unknown"
            if response.status_code == 200:
                data = response.json()
                if data.get("platform") == "unknown":
                    self.log_result("Invalid URL Handling", True, "Platform detected as unknown")
                else:
                    self.log_result("Invalid URL Handling", False, f"Unexpected platform: {data.get('platform')}")
            else:
                self.log_result("Invalid URL Handling", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("Invalid URL Handling", False, f"Exception: {str(e)}")
    
    def test_process_video_missing_params(self):
        """Test process video with missing parameters"""
        try:
            # Test missing video_url
            payload = {"persona": "nyc-drama"}
            
            response = requests.post(
                f"{BACKEND_URL}/process-video", 
                json=payload, 
                timeout=10
            )
            
            if response.status_code == 422:  # Validation error expected
                self.log_result("Missing URL Parameter", True, "Validation error returned as expected")
            else:
                self.log_result("Missing URL Parameter", False, f"Expected 422, got {response.status_code}")
                
        except Exception as e:
            self.log_result("Missing URL Parameter", False, f"Exception: {str(e)}")
        
        try:
            # Test missing persona
            payload = {"video_url": "https://www.youtube.com/watch?v=test"}
            
            response = requests.post(
                f"{BACKEND_URL}/process-video", 
                json=payload, 
                timeout=10
            )
            
            if response.status_code == 422:  # Validation error expected
                self.log_result("Missing Persona Parameter", True, "Validation error returned as expected")
            else:
                self.log_result("Missing Persona Parameter", False, f"Expected 422, got {response.status_code}")
                
        except Exception as e:
            self.log_result("Missing Persona Parameter", False, f"Exception: {str(e)}")
    
    def test_platform_detection(self):
        """Test platform detection functionality"""
        test_cases = [
            ("https://www.youtube.com/watch?v=test", "youtube"),
            ("https://youtu.be/test", "youtube"),
            ("https://www.tiktok.com/@user/video/123", "tiktok"),
            ("https://www.instagram.com/p/ABC/", "instagram"),
            ("https://twitter.com/user/status/123", "twitter"),
            ("https://x.com/user/status/123", "twitter"),
            ("https://www.facebook.com/watch/?v=123", "facebook"),
            ("https://unknown-platform.com/video", "unknown")
        ]
        
        for url, expected_platform in test_cases:
            try:
                payload = {
                    "video_url": url,
                    "persona": "viral-trends"
                }
                
                response = requests.post(
                    f"{BACKEND_URL}/process-video", 
                    json=payload, 
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    actual_platform = data.get("platform")
                    
                    if actual_platform == expected_platform:
                        self.log_result(f"Platform Detection - {expected_platform}", True, f"URL: {url}")
                    else:
                        self.log_result(f"Platform Detection - {expected_platform}", False, 
                                      f"Expected {expected_platform}, got {actual_platform}")
                else:
                    self.log_result(f"Platform Detection - {expected_platform}", False, 
                                  f"HTTP {response.status_code}")
                    
            except Exception as e:
                self.log_result(f"Platform Detection - {expected_platform}", False, f"Exception: {str(e)}")
    
    def test_persona_hook_generation(self):
        """Test hook generation for different personas"""
        personas = ["nyc-drama", "luxury-rentals", "fitness-guru", "conspiracy-mode", 
                   "lifestyle-flex", "storytime", "business-tips", "viral-trends"]
        
        for persona in personas:
            try:
                payload = {
                    "video_url": "https://www.youtube.com/watch?v=test",
                    "persona": persona
                }
                
                response = requests.post(
                    f"{BACKEND_URL}/process-video", 
                    json=payload, 
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    hooks = data.get("hooks", [])
                    keywords = data.get("keywords", [])
                    
                    if len(hooks) > 0 and len(keywords) > 0:
                        self.log_result(f"Persona Hook Generation - {persona}", True, 
                                      f"Generated {len(hooks)} hooks, {len(keywords)} keywords")
                    else:
                        self.log_result(f"Persona Hook Generation - {persona}", False, 
                                      "No hooks or keywords generated")
                else:
                    self.log_result(f"Persona Hook Generation - {persona}", False, 
                                  f"HTTP {response.status_code}")
                    
            except Exception as e:
                self.log_result(f"Persona Hook Generation - {persona}", False, f"Exception: {str(e)}")
    
    def test_video_retrieval(self):
        """Test video retrieval by ID"""
        # First create a video
        try:
            payload = {
                "video_url": "https://www.youtube.com/watch?v=test",
                "persona": "nyc-drama"
            }
            
            response = requests.post(
                f"{BACKEND_URL}/process-video", 
                json=payload, 
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                video_id = data.get("id")
                
                if video_id:
                    # Now try to retrieve it
                    get_response = requests.get(f"{BACKEND_URL}/videos/{video_id}", timeout=10)
                    
                    if get_response.status_code == 200:
                        retrieved_data = get_response.json()
                        if retrieved_data.get("id") == video_id:
                            self.log_result("Video Retrieval", True, f"Retrieved video ID: {video_id}")
                        else:
                            self.log_result("Video Retrieval", False, "ID mismatch in retrieved data")
                    else:
                        self.log_result("Video Retrieval", False, f"HTTP {get_response.status_code}")
                else:
                    self.log_result("Video Retrieval", False, "No video ID returned from creation")
            else:
                self.log_result("Video Retrieval", False, "Failed to create video for retrieval test")
                
        except Exception as e:
            self.log_result("Video Retrieval", False, f"Exception: {str(e)}")
    
    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting AyoVirals Backend API Tests")
        print(f"🔗 Testing against: {BACKEND_URL}")
        print("=" * 60)
        
        # Basic API tests
        self.test_health_endpoint()
        self.test_personas_endpoint()
        
        # Video processing tests
        self.test_process_video_endpoint()
        
        # Platform detection tests
        self.test_platform_detection()
        
        # Persona and hook generation tests
        self.test_persona_hook_generation()
        
        # Video retrieval tests
        self.test_video_retrieval()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.total_tests}")
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%")
        
        if self.failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.results:
                if "❌ FAIL" in result:
                    print(f"  {result}")
        
        return self.failed_tests == 0

if __name__ == "__main__":
    tester = BackendTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)