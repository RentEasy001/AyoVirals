#!/usr/bin/env python3
"""
Replit Configuration and Management
Handles Replit-specific settings and keep-alive functionality
"""

import os
import json
import logging
from pathlib import Path
from keep_alive import start_keep_alive

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReplitConfig:
    def __init__(self):
        self.is_replit = self.detect_replit()
        self.repl_info = self.get_repl_info()
        
    def detect_replit(self):
        """Detect if running on Replit"""
        indicators = [
            'REPL_SLUG' in os.environ,
            'REPL_OWNER' in os.environ,
            'REPLIT_DB_URL' in os.environ,
            Path('/home/runner').exists()
        ]
        return any(indicators)
    
    def get_repl_info(self):
        """Get Replit information"""
        if not self.is_replit:
            return {}
            
        return {
            'slug': os.environ.get('REPL_SLUG', 'ayovirals'),
            'owner': os.environ.get('REPL_OWNER', 'user'),
            'id': os.environ.get('REPL_ID', 'unknown'),
            'language': os.environ.get('REPL_LANGUAGE', 'python'),
            'db_url': os.environ.get('REPLIT_DB_URL', ''),
            'public_url': self.get_public_url()
        }
    
    def get_public_url(self):
        """Get the public URL for this repl"""
        if not self.is_replit:
            return 'http://localhost:3000'
            
        slug = os.environ.get('REPL_SLUG', 'ayovirals')
        owner = os.environ.get('REPL_OWNER', 'user')
        
        # Try different URL formats that Replit uses
        possible_urls = [
            f"https://{slug}.{owner}.repl.co",
            f"https://{slug}--{owner}.repl.co",
            f"https://{owner}.repl.co/{slug}"
        ]
        
        return possible_urls[0]  # Default to first format
    
    def setup_environment(self):
        """Setup environment variables for Replit"""
        if not self.is_replit:
            logger.info("Not running on Replit, skipping Replit-specific setup")
            return
            
        logger.info("🔧 Setting up Replit environment")
        
        # Set backend URL
        public_url = self.get_public_url()
        os.environ['REACT_APP_BACKEND_URL'] = public_url
        
        # Set other environment variables
        os.environ.setdefault('PORT', '3000')
        os.environ.setdefault('BACKEND_PORT', '8001')
        os.environ.setdefault('MONGO_URL', 'mongodb://localhost:27017')
        os.environ.setdefault('DB_NAME', 'ayovirals_db')
        os.environ.setdefault('NODE_ENV', 'production')
        
        logger.info(f"✅ Replit environment configured")
        logger.info(f"   Public URL: {public_url}")
        logger.info(f"   Backend URL: {os.environ.get('REACT_APP_BACKEND_URL')}")
        
    def enable_keep_alive(self):
        """Enable keep-alive functionality to prevent sleep"""
        if not self.is_replit:
            logger.info("Not on Replit, keep-alive not needed")
            return
            
        logger.info("🔄 Enabling keep-alive service")
        start_keep_alive()
        
    def print_info(self):
        """Print Replit information"""
        logger.info("🔍 Replit Environment Information:")
        logger.info(f"   Running on Replit: {self.is_replit}")
        
        if self.is_replit:
            for key, value in self.repl_info.items():
                logger.info(f"   {key.title()}: {value}")
        
        logger.info("🌐 URLs:")
        logger.info(f"   Frontend: {self.get_public_url()}")
        logger.info(f"   Backend: {self.get_public_url()}/api/")
        logger.info(f"   Health: {self.get_public_url()}/api/health")

# Global instance
replit_config = ReplitConfig()

def setup_replit():
    """Setup Replit configuration"""
    replit_config.setup_environment()
    replit_config.print_info()
    
    # Enable keep-alive if on Replit
    if replit_config.is_replit:
        replit_config.enable_keep_alive()

if __name__ == "__main__":
    setup_replit()