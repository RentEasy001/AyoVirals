from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
import os
import logging
import subprocess
import tempfile
import uuid
import re
import json
from pathlib import Path
from typing import List, Dict, Any
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="AyoVirals API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
try:
    client = MongoClient(os.environ.get('MONGO_URL'))
    db = client.ayovirals_db
    videos_collection = db.videos
    logger.info("Connected to MongoDB successfully")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    db = None

# Pydantic models
class VideoRequest(BaseModel):
    video_url: str
    persona: str

class VideoResponse(BaseModel):
    id: str
    summary: str
    hooks: List[str]
    keywords: List[str]
    platform: str
    persona: str

# Persona configurations
PERSONAS = {
    "nyc-drama": {
        "name": "NYC Drama",
        "hook_templates": [
            "If you live in NYC, you NEED to see this...",
            "NYC rent is crazy, but THIS is next level...",
            "I can't believe what I found in NYC today...",
            "NYC apartments are getting ridiculous...",
            "Living in NYC taught me this harsh truth..."
        ],
        "keywords": ["#nyc", "#newyork", "#manhattan", "#brooklyn", "#apartments", "#rent", "#city", "#urban"]
    },
    "luxury-rentals": {
        "name": "Luxury Rentals",
        "hook_templates": [
            "This luxury property will blow your mind...",
            "I toured a $10M property and here's what I found...",
            "Luxury living redefined in this incredible space...",
            "The most expensive rental I've ever seen...",
            "Rich people really live like this..."
        ],
        "keywords": ["#luxury", "#penthouse", "#mansion", "#expensive", "#rich", "#wealthy", "#property", "#realestate"]
    },
    "fitness-guru": {
        "name": "Fitness Guru",
        "hook_templates": [
            "This workout changed my life in 30 days...",
            "I tried this fitness trend so you don't have to...",
            "The fitness industry doesn't want you to know this...",
            "This simple exercise will transform your body...",
            "I wish I knew this fitness secret 10 years ago..."
        ],
        "keywords": ["#fitness", "#workout", "#gym", "#health", "#muscle", "#bodybuilding", "#transformation", "#exercise"]
    },
    "conspiracy-mode": {
        "name": "Conspiracy Mode",
        "hook_templates": [
            "They don't want you to know this truth...",
            "I discovered something they're hiding from us...",
            "The real story behind this will shock you...",
            "What they're not telling you about this...",
            "I went down a rabbit hole and found this..."
        ],
        "keywords": ["#truth", "#exposed", "#conspiracy", "#hidden", "#secret", "#revealed", "#investigation", "#facts"]
    },
    "lifestyle-flex": {
        "name": "Lifestyle Flex",
        "hook_templates": [
            "My morning routine that changed everything...",
            "Living my best life and here's how...",
            "This lifestyle hack will upgrade your life...",
            "The daily habits that made me successful...",
            "How I built the life of my dreams..."
        ],
        "keywords": ["#lifestyle", "#success", "#motivation", "#luxury", "#goals", "#millionaire", "#entrepreneur", "#habits"]
    },
    "storytime": {
        "name": "Storytime",
        "hook_templates": [
            "You won't believe what happened to me today...",
            "This story will give you chills...",
            "The craziest thing just happened...",
            "I have to tell you this wild story...",
            "This experience changed my perspective forever..."
        ],
        "keywords": ["#storytime", "#story", "#experience", "#crazy", "#unbelievable", "#life", "#personal", "#real"]
    },
    "business-tips": {
        "name": "Business Tips",
        "hook_templates": [
            "This business strategy made me $100K...",
            "The business mistake that cost me everything...",
            "I learned this business lesson the hard way...",
            "This entrepreneur secret will change your life...",
            "The business advice I wish I had 5 years ago..."
        ],
        "keywords": ["#business", "#entrepreneur", "#success", "#money", "#startup", "#tips", "#strategy", "#mindset"]
    },
    "viral-trends": {
        "name": "Viral Trends",
        "hook_templates": [
            "This trend is about to blow up everywhere...",
            "I called this trend before it went viral...",
            "The next big trend is already here...",
            "This viral moment changed everything...",
            "I can't believe this is trending now..."
        ],
        "keywords": ["#viral", "#trending", "#trend", "#fyp", "#popular", "#hot", "#new", "#breaking"]
    }
}

# Utility functions
def detect_platform(url: str) -> str:
    """Detect video platform from URL"""
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    elif "tiktok.com" in url:
        return "tiktok"
    elif "instagram.com" in url:
        return "instagram"
    elif "twitter.com" in url or "x.com" in url:
        return "twitter"
    elif "facebook.com" in url:
        return "facebook"
    else:
        return "unknown"

def extract_keywords_from_text(text: str) -> List[str]:
    """Extract keywords using basic NLP techniques"""
    # Simple keyword extraction - can be enhanced with spaCy later
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    
    # Remove common stop words
    stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use'}
    
    keywords = [word for word in words if word not in stop_words and len(word) > 3]
    
    # Count frequency and return top keywords
    word_freq = {}
    for word in keywords:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort by frequency and return top 10
    top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
    return [f"#{word[0]}" for word in top_keywords]

def generate_hooks(content: str, persona: str) -> List[str]:
    """Generate viral hooks based on content and persona"""
    if persona not in PERSONAS:
        persona = "viral-trends"
    
    persona_config = PERSONAS[persona]
    hooks = []
    
    # Use persona templates
    for template in persona_config["hook_templates"]:
        hooks.append(template)
    
    # Add content-specific hooks
    if "money" in content.lower() or "expensive" in content.lower():
        hooks.append("The price of this will shock you...")
    
    if "secret" in content.lower() or "hidden" in content.lower():
        hooks.append("I found a secret that changes everything...")
    
    if "mistake" in content.lower() or "wrong" in content.lower():
        hooks.append("I made this mistake so you don't have to...")
    
    if "amazing" in content.lower() or "incredible" in content.lower():
        hooks.append("This is absolutely mind-blowing...")
    
    # Return top 5 hooks
    return hooks[:5]

def generate_summary(text: str) -> str:
    """Generate a simple summary of the video content"""
    # Simple summarization - take first and last sentences
    sentences = text.split('.')
    if len(sentences) > 2:
        return f"{sentences[0].strip()}. {sentences[-2].strip()}."
    return text[:200] + "..." if len(text) > 200 else text

async def download_video(url: str) -> tuple:
    """Download video and extract audio using yt-dlp"""
    try:
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        
        # Download video info first
        cmd_info = [
            "yt-dlp",
            "--print", "title",
            "--print", "duration",
            "--print", "description",
            url
        ]
        
        result = subprocess.run(cmd_info, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            logger.error(f"yt-dlp info failed: {result.stderr}")
            return None, None, None
        
        output_lines = result.stdout.strip().split('\n')
        title = output_lines[0] if len(output_lines) > 0 else "Unknown"
        duration = output_lines[1] if len(output_lines) > 1 else "Unknown"
        description = output_lines[2] if len(output_lines) > 2 else ""
        
        # Download audio only
        audio_file = os.path.join(temp_dir, "audio.%(ext)s")
        cmd_download = [
            "yt-dlp",
            "-x",
            "--audio-format", "wav",
            "--audio-quality", "0",
            "-o", audio_file,
            url
        ]
        
        result = subprocess.run(cmd_download, capture_output=True, text=True, timeout=120)
        
        if result.returncode != 0:
            logger.error(f"yt-dlp download failed: {result.stderr}")
            return None, None, None
        
        # Find the downloaded audio file
        audio_files = list(Path(temp_dir).glob("audio.*"))
        if not audio_files:
            logger.error("No audio file found after download")
            return None, None, None
        
        return str(audio_files[0]), title, description
        
    except subprocess.TimeoutExpired:
        logger.error("yt-dlp timed out")
        return None, None, None
    except Exception as e:
        logger.error(f"Video download error: {str(e)}")
        return None, None, None

async def transcribe_audio(audio_file: str) -> str:
    """Transcribe audio using whisper (placeholder for now)"""
    try:
        # For now, return a mock transcription
        # In production, you would use whisper-cpp or faster-whisper
        return "This is a mock transcription. Video content analysis coming soon with local Whisper integration."
    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        return "Transcription failed"

# API routes
@app.get("/")
async def root():
    return {"message": "AyoVirals API is running! 🔥"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "database": "connected" if db is not None else "disconnected"}

@app.post("/api/process-video")
async def process_video(request: VideoRequest):
    """Main endpoint to process video and generate hooks"""
    try:
        # Validate URL
        if not request.video_url.strip():
            raise HTTPException(status_code=400, detail="Video URL is required")
        
        # Detect platform
        platform = detect_platform(request.video_url)
        
        # Generate unique ID
        video_id = str(uuid.uuid4())
        
        # For now, create a mock response until we implement full video processing
        # In production, this would download, transcribe, and analyze the video
        
        # Mock content analysis
        mock_content = f"Video analysis for {platform} content. This is a placeholder until full integration is complete."
        
        # Generate hooks based on persona
        hooks = generate_hooks(mock_content, request.persona)
        
        # Generate keywords
        persona_keywords = PERSONAS.get(request.persona, PERSONAS["viral-trends"])["keywords"]
        content_keywords = extract_keywords_from_text(mock_content)
        all_keywords = persona_keywords + content_keywords
        
        # Generate summary
        summary = f"Video from {platform} platform analyzed with {request.persona} persona. Content processing and hook generation complete."
        
        # Create response
        response = {
            "id": video_id,
            "summary": summary,
            "hooks": hooks,
            "keywords": list(set(all_keywords)),  # Remove duplicates
            "platform": platform,
            "persona": request.persona
        }
        
        # Save to database if available
        if db is not None:
            try:
                videos_collection.insert_one({
                    "id": video_id,
                    "url": request.video_url,
                    "platform": platform,
                    "persona": request.persona,
                    "summary": summary,
                    "hooks": hooks,
                    "keywords": all_keywords,
                    "created_at": "2024-01-01T00:00:00Z"  # Would use datetime in production
                })
            except Exception as e:
                logger.error(f"Database save error: {str(e)}")
        
        return response
        
    except Exception as e:
        logger.error(f"Process video error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process video: {str(e)}")

@app.get("/api/personas")
async def get_personas():
    """Get available personas"""
    return {
        "personas": [
            {"id": key, "name": value["name"]}
            for key, value in PERSONAS.items()
        ]
    }

@app.get("/api/videos/{video_id}")
async def get_video(video_id: str):
    """Get video analysis by ID"""
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        video = videos_collection.find_one({"id": video_id})
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        
        # Remove MongoDB _id field
        video.pop("_id", None)
        return video
        
    except Exception as e:
        logger.error(f"Get video error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve video")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)