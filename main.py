#!/usr/bin/env python3
"""
AyoVirals - Main entry point for Replit deployment
This file starts both the backend API and frontend development server
"""

import os
import sys
import time
import signal
import subprocess
import threading
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class AyoViralsApp:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.mongodb_process = None
        self.processes = []
        
    def setup_environment(self):
        """Setup environment variables for Replit"""
        # Set environment variables
        os.environ['PYTHONPATH'] = '/app'
        os.environ['NODE_ENV'] = 'production'
        os.environ['PORT'] = '3000'
        os.environ['BACKEND_PORT'] = '8001'
        
        # Set backend URL for Replit
        repl_slug = os.environ.get('REPL_SLUG', 'ayovirals')
        repl_owner = os.environ.get('REPL_OWNER', 'user')
        backend_url = f"https://{repl_slug}.{repl_owner}.repl.co"
        os.environ['REACT_APP_BACKEND_URL'] = backend_url
        
        # MongoDB setup
        os.environ['MONGO_URL'] = 'mongodb://localhost:27017'
        os.environ['DB_NAME'] = 'ayovirals_db'
        
        logger.info(f"Environment setup complete")
        logger.info(f"Backend URL: {backend_url}")
        
    def start_mongodb(self):
        """Start MongoDB server"""
        try:
            # Create MongoDB data directory
            data_dir = Path('/tmp/mongodb_data')
            data_dir.mkdir(exist_ok=True)
            
            # Start MongoDB
            cmd = [
                'mongod',
                '--dbpath', str(data_dir),
                '--port', '27017',
                '--bind_ip', '127.0.0.1',
                '--nojournal',
                '--noprealloc',
                '--smallfiles',
                '--quiet'
            ]
            
            logger.info("Starting MongoDB...")
            self.mongodb_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd='/app'
            )
            self.processes.append(self.mongodb_process)
            
            # Wait for MongoDB to start
            time.sleep(3)
            logger.info("MongoDB started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start MongoDB: {e}")
            # Continue without MongoDB for now
            
    def install_dependencies(self):
        """Install Python and Node.js dependencies"""
        try:
            # Install Python dependencies
            logger.info("Installing Python dependencies...")
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', '-r', 'backend/requirements.txt'
            ], cwd='/app', check=True)
            
            # Install Node.js dependencies
            logger.info("Installing Node.js dependencies...")
            subprocess.run(['yarn', 'install'], cwd='/app/frontend', check=True)
            
            logger.info("Dependencies installed successfully")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install dependencies: {e}")
            # Continue anyway, some dependencies might already be installed
            
    def build_frontend(self):
        """Build the React frontend"""
        try:
            logger.info("Building React frontend...")
            subprocess.run(['yarn', 'build'], cwd='/app/frontend', check=True)
            logger.info("Frontend build completed successfully")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to build frontend: {e}")
            # Continue anyway, we can serve in development mode
            
    def start_backend(self):
        """Start the FastAPI backend server"""
        try:
            logger.info("Starting FastAPI backend...")
            
            # Change to backend directory
            backend_dir = '/app/backend'
            
            # Start backend with uvicorn
            cmd = [
                sys.executable, '-m', 'uvicorn',
                'server:app',
                '--host', '0.0.0.0',
                '--port', '8001',
                '--reload',
                '--log-level', 'info'
            ]
            
            self.backend_process = subprocess.Popen(
                cmd,
                cwd=backend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            self.processes.append(self.backend_process)
            
            logger.info("Backend server started on port 8001")
            
        except Exception as e:
            logger.error(f"Failed to start backend: {e}")
            return False
            
        return True
        
    def start_frontend(self):
        """Start the React frontend development server"""
        try:
            logger.info("Starting React frontend...")
            
            # Change to frontend directory
            frontend_dir = '/app/frontend'
            
            # Start frontend with yarn
            cmd = ['yarn', 'start']
            
            # Set environment variables for frontend
            env = os.environ.copy()
            env['PORT'] = '3000'
            env['BROWSER'] = 'none'  # Don't open browser
            env['CI'] = 'true'  # Prevent interactive prompts
            
            self.frontend_process = subprocess.Popen(
                cmd,
                cwd=frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                env=env
            )
            self.processes.append(self.frontend_process)
            
            logger.info("Frontend server started on port 3000")
            
        except Exception as e:
            logger.error(f"Failed to start frontend: {e}")
            return False
            
        return True
        
    def monitor_processes(self):
        """Monitor running processes"""
        def log_output(process, name):
            """Log output from a process"""
            try:
                for line in iter(process.stdout.readline, ''):
                    if line.strip():
                        logger.info(f"[{name}] {line.strip()}")
            except Exception as e:
                logger.error(f"Error monitoring {name}: {e}")
                
        # Start monitoring threads
        if self.backend_process:
            threading.Thread(
                target=log_output,
                args=(self.backend_process, "Backend"),
                daemon=True
            ).start()
            
        if self.frontend_process:
            threading.Thread(
                target=log_output,
                args=(self.frontend_process, "Frontend"),
                daemon=True
            ).start()
            
    def cleanup(self):
        """Clean up processes"""
        logger.info("Shutting down services...")
        
        for process in self.processes:
            if process and process.poll() is None:
                try:
                    process.terminate()
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                except Exception as e:
                    logger.error(f"Error cleaning up process: {e}")
                    
        logger.info("Cleanup complete")
        
    def run(self):
        """Main run method"""
        try:
            # Setup
            self.setup_environment()
            
            # Install dependencies
            self.install_dependencies()
            
            # Start MongoDB
            self.start_mongodb()
            
            # Build frontend
            self.build_frontend()
            
            # Start backend
            if not self.start_backend():
                logger.error("Failed to start backend server")
                return
                
            # Wait a bit for backend to start
            time.sleep(2)
            
            # Start frontend
            if not self.start_frontend():
                logger.error("Failed to start frontend server")
                return
                
            # Monitor processes
            self.monitor_processes()
            
            # Keep the main process running
            logger.info("🔥 AyoVirals is running!")
            logger.info("Frontend: http://localhost:3000")
            logger.info("Backend: http://localhost:8001")
            logger.info("Press Ctrl+C to stop")
            
            # Wait for processes
            while True:
                time.sleep(1)
                
                # Check if processes are still running
                if self.backend_process and self.backend_process.poll() is not None:
                    logger.error("Backend process died, restarting...")
                    self.start_backend()
                    
                if self.frontend_process and self.frontend_process.poll() is not None:
                    logger.error("Frontend process died, restarting...")
                    self.start_frontend()
                    
        except KeyboardInterrupt:
            logger.info("Received interrupt signal")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        finally:
            self.cleanup()

def signal_handler(signum, frame):
    """Handle interrupt signals"""
    logger.info(f"Received signal {signum}")
    sys.exit(0)

if __name__ == "__main__":
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create and run the app
    app = AyoViralsApp()
    app.run()