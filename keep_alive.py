#!/usr/bin/env python3
"""
Keep Alive Service for Replit
Prevents the repl from sleeping after 30 minutes of inactivity
"""

import time
import requests
import threading
import logging
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KeepAliveService:
    def __init__(self):
        self.repl_url = self.get_repl_url()
        self.running = False
        self.ping_interval = 25 * 60  # 25 minutes (5 min before sleep)
        
    def get_repl_url(self):
        """Get the Replit URL for this repl"""
        repl_slug = os.environ.get('REPL_SLUG', 'ayovirals')
        repl_owner = os.environ.get('REPL_OWNER', 'user')
        
        # Try different URL formats
        urls = [
            f"https://{repl_slug}.{repl_owner}.repl.co",
            f"https://{repl_slug}--{repl_owner}.repl.co",
            "http://localhost:3000"  # Local fallback
        ]
        
        return urls[0]  # Default to first format
    
    def ping_health(self):
        """Ping the health endpoint to keep the repl alive"""
        try:
            response = requests.get(f"{self.repl_url}/api/health", timeout=10)
            if response.status_code == 200:
                logger.info(f"✅ Keep-alive ping successful at {datetime.now()}")
                return True
            else:
                logger.warning(f"⚠️ Keep-alive ping failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Keep-alive ping error: {e}")
            return False
    
    def ping_frontend(self):
        """Ping the frontend to keep it alive"""
        try:
            response = requests.get(self.repl_url, timeout=10)
            if response.status_code == 200:
                logger.info(f"✅ Frontend ping successful at {datetime.now()}")
                return True
            else:
                logger.warning(f"⚠️ Frontend ping failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Frontend ping error: {e}")
            return False
    
    def keep_alive_loop(self):
        """Main keep-alive loop"""
        logger.info(f"🔄 Keep-alive service started for {self.repl_url}")
        logger.info(f"⏰ Pinging every {self.ping_interval // 60} minutes")
        
        while self.running:
            # Ping both frontend and backend
            self.ping_frontend()
            time.sleep(2)  # Small delay between pings
            self.ping_health()
            
            # Wait for next ping
            time.sleep(self.ping_interval)
    
    def start(self):
        """Start the keep-alive service in a separate thread"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.keep_alive_loop, daemon=True)
            self.thread.start()
            logger.info("🚀 Keep-alive service started")
    
    def stop(self):
        """Stop the keep-alive service"""
        if self.running:
            self.running = False
            logger.info("🛑 Keep-alive service stopped")

# Global instance
keep_alive_service = KeepAliveService()

def start_keep_alive():
    """Start the keep-alive service"""
    keep_alive_service.start()

def stop_keep_alive():
    """Stop the keep-alive service"""
    keep_alive_service.stop()

if __name__ == "__main__":
    # Run standalone
    try:
        keep_alive_service.start()
        
        # Keep the main thread alive
        while True:
            time.sleep(60)
            
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
        keep_alive_service.stop()