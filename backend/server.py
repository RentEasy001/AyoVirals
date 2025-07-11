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
import spacy
from collections import Counter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="AyoVirals API 2.0", version="2.0.0")

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

# Initialize spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
    logger.info("spaCy model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load spaCy model: {e}")
    nlp = None

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

# Enhanced persona configurations with viral patterns
PERSONAS = {
    "nyc-drama": {
        "name": "NYC Drama",
        "hook_templates": [
            "If you live in NYC, you NEED to see this...",
            "NYC rent is crazy, but THIS is next level...",
            "I can't believe what I found in NYC today...",
            "NYC apartments are getting ridiculous...",
            "Living in NYC taught me this harsh truth...",
            "This NYC apartment costs HOW MUCH?!",
            "NYC life hits different when you see this...",
            "Every NYC person needs to watch this NOW..."
        ],
        "keywords": ["#nyc", "#newyork", "#manhattan", "#brooklyn", "#apartments", "#rent", "#city", "#urban"],
        "viral_triggers": ["shocking", "unbelievable", "crazy", "insane", "need to see"],
        "emotion_focus": "surprise"
    },
    "luxury-rentals": {
        "name": "Luxury Rentals",
        "hook_templates": [
            "This luxury property will blow your mind...",
            "I toured a $10M property and here's what I found...",
            "Luxury living redefined in this incredible space...",
            "The most expensive rental I've ever seen...",
            "Rich people really live like this...",
            "This property costs more than your house...",
            "Millionaire lifestyle exposed in this tour...",
            "You won't believe what $50K/month gets you..."
        ],
        "keywords": ["#luxury", "#penthouse", "#mansion", "#expensive", "#rich", "#wealthy", "#property", "#realestate"],
        "viral_triggers": ["blow your mind", "incredible", "expensive", "rich people"],
        "emotion_focus": "aspiration"
    },
    "fitness-guru": {
        "name": "Fitness Guru",
        "hook_templates": [
            "This workout changed my life in 30 days...",
            "I tried this fitness trend so you don't have to...",
            "The fitness industry doesn't want you to know this...",
            "This simple exercise will transform your body...",
            "I wish I knew this fitness secret 10 years ago...",
            "Stop doing this exercise - it's ruining your gains...",
            "This 5-minute routine burns more fat than cardio...",
            "Personal trainers HATE this one simple trick..."
        ],
        "keywords": ["#fitness", "#workout", "#gym", "#health", "#muscle", "#bodybuilding", "#transformation", "#exercise"],
        "viral_triggers": ["changed my life", "secret", "transform", "hate this trick"],
        "emotion_focus": "motivation"
    },
    "conspiracy-mode": {
        "name": "Conspiracy Mode",
        "hook_templates": [
            "They don't want you to know this truth...",
            "I discovered something they're hiding from us...",
            "The real story behind this will shock you...",
            "What they're not telling you about this...",
            "I went down a rabbit hole and found this...",
            "This conspiracy theory just became reality...",
            "The evidence they tried to hide is here...",
            "Connect the dots - this changes everything..."
        ],
        "keywords": ["#truth", "#exposed", "#conspiracy", "#hidden", "#secret", "#revealed", "#investigation", "#facts"],
        "viral_triggers": ["don't want you to know", "hiding", "shock you", "rabbit hole"],
        "emotion_focus": "curiosity"
    },
    "lifestyle-flex": {
        "name": "Lifestyle Flex",
        "hook_templates": [
            "My morning routine that changed everything...",
            "Living my best life and here's how...",
            "This lifestyle hack will upgrade your life...",
            "The daily habits that made me successful...",
            "How I built the life of my dreams...",
            "From broke to millionaire - my story...",
            "This is what success really looks like...",
            "My life before vs after this mindset shift..."
        ],
        "keywords": ["#lifestyle", "#success", "#motivation", "#luxury", "#goals", "#millionaire", "#entrepreneur", "#habits"],
        "viral_triggers": ["changed everything", "life hack", "successful", "dreams"],
        "emotion_focus": "aspiration"
    },
    "storytime": {
        "name": "Storytime",
        "hook_templates": [
            "You won't believe what happened to me today...",
            "This story will give you chills...",
            "The craziest thing just happened...",
            "I have to tell you this wild story...",
            "This experience changed my perspective forever...",
            "I never thought this would happen to me...",
            "The plot twist in this story is insane...",
            "This real-life story sounds fake but it's true..."
        ],
        "keywords": ["#storytime", "#story", "#experience", "#crazy", "#unbelievable", "#life", "#personal", "#real"],
        "viral_triggers": ["won't believe", "give you chills", "crazy", "wild"],
        "emotion_focus": "suspense"
    },
    "business-tips": {
        "name": "Business Tips",
        "hook_templates": [
            "This business strategy made me $100K...",
            "The business mistake that cost me everything...",
            "I learned this business lesson the hard way...",
            "This entrepreneur secret will change your life...",
            "The business advice I wish I had 5 years ago...",
            "How I scaled from $0 to $1M in 12 months...",
            "This business hack saved me thousands...",
            "The #1 mistake new entrepreneurs make..."
        ],
        "keywords": ["#business", "#entrepreneur", "#success", "#money", "#startup", "#tips", "#strategy", "#mindset"],
        "viral_triggers": ["made me $100K", "cost me everything", "secret", "hard way"],
        "emotion_focus": "education"
    },
    "viral-trends": {
        "name": "Viral Trends",
        "hook_templates": [
            "This trend is about to blow up everywhere...",
            "I called this trend before it went viral...",
            "The next big trend is already here...",
            "This viral moment changed everything...",
            "I can't believe this is trending now...",
            "Everyone's doing this trend wrong...",
            "This trend started here and now it's everywhere...",
            "POV: You're witnessing the birth of a trend..."
        ],
        "keywords": ["#viral", "#trending", "#trend", "#fyp", "#popular", "#hot", "#new", "#breaking"],
        "viral_triggers": ["blow up", "went viral", "trending", "everywhere"],
        "emotion_focus": "excitement"
    }
}

# Enhanced viral patterns and triggers
VIRAL_PATTERNS = {
    "power_words": ["shocking", "unbelievable", "secret", "truth", "exposed", "crazy", "insane", "viral", "trending", "exclusive"],
    "urgency_words": ["now", "today", "immediately", "must", "need", "can't", "don't", "stop", "wait"],
    "emotional_triggers": ["amazing", "incredible", "shocking", "mind-blowing", "life-changing", "game-changer", "revolutionary"],
    "curiosity_gaps": ["you won't believe", "what happened next", "the truth about", "what they don't want", "hidden secret"],
    "social_proof": ["everyone", "millions", "viral", "trending", "popular", "celebrities", "influencers"],
    "numbers": ["#1", "5 ways", "10 secrets", "100%", "$1M", "24 hours", "30 days", "one trick"]
}

# Utility functions
def detect_platform(url: str) -> str:
    """Detect video platform from URL"""
    url_lower = url.lower()
    if "youtube.com" in url_lower or "youtu.be" in url_lower:
        return "youtube"
    elif "tiktok.com" in url_lower:
        return "tiktok"
    elif "instagram.com" in url_lower:
        return "instagram"
    elif "twitter.com" in url_lower or "x.com" in url_lower:
        return "twitter"
    elif "facebook.com" in url_lower or "fb.com" in url_lower:
        return "facebook"
    else:
        return "unknown"

def enhanced_keyword_extraction(text: str) -> List[str]:
    """Enhanced keyword extraction using spaCy NLP"""
    if not nlp:
        return basic_keyword_extraction(text)
    
    try:
        doc = nlp(text)
        keywords = []
        
        # Extract named entities
        entities = [ent.text.lower() for ent in doc.ents if ent.label_ in ["PERSON", "ORG", "GPE", "PRODUCT"]]
        
        # Extract important nouns and adjectives
        important_words = []
        for token in doc:
            if (token.pos_ in ["NOUN", "ADJ"] and 
                len(token.text) > 3 and 
                not token.is_stop and 
                not token.is_punct and
                token.text.isalpha()):
                important_words.append(token.text.lower())
        
        # Count frequency and get top words
        word_freq = Counter(important_words)
        top_words = [word for word, count in word_freq.most_common(10) if count > 1]
        
        # Combine all keywords
        all_keywords = entities + top_words
        
        # Add hashtags
        hashtag_keywords = [f"#{word}" for word in all_keywords[:8]]
        
        return hashtag_keywords
    
    except Exception as e:
        logger.error(f"spaCy keyword extraction error: {str(e)}")
        return basic_keyword_extraction(text)

def basic_keyword_extraction(text: str) -> List[str]:
    """Basic keyword extraction fallback"""
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    
    # Remove common stop words
    stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use'}
    
    keywords = [word for word in words if word not in stop_words and len(word) > 3]
    
    # Count frequency and return top keywords
    word_freq = Counter(keywords)
    top_keywords = [word for word, count in word_freq.most_common(10)]
    
    return [f"#{word}" for word in top_keywords]

def extract_keywords_from_text(text: str) -> List[str]:
    """Main keyword extraction function"""
    return enhanced_keyword_extraction(text)

def generate_enhanced_hooks(content: str, persona: str) -> List[str]:
    """Enhanced hook generation with viral patterns"""
    if persona not in PERSONAS:
        persona = "viral-trends"
    
    persona_config = PERSONAS[persona]
    hooks = []
    
    # Use persona templates
    for template in persona_config["hook_templates"]:
        hooks.append(template)
    
    # Add content-specific hooks with viral patterns
    content_lower = content.lower()
    
    # Money/value hooks
    if any(word in content_lower for word in ["money", "expensive", "cost", "price", "dollar"]):
        hooks.append("The price of this will shock you...")
        hooks.append("I spent HOW MUCH on this?!")
    
    # Secret/hidden hooks
    if any(word in content_lower for word in ["secret", "hidden", "private", "exclusive"]):
        hooks.append("I found a secret that changes everything...")
        hooks.append("They don't want you to know this...")
    
    # Mistake/failure hooks
    if any(word in content_lower for word in ["mistake", "wrong", "failed", "error"]):
        hooks.append("I made this mistake so you don't have to...")
        hooks.append("This common mistake is costing you money...")
    
    # Amazing/incredible hooks
    if any(word in content_lower for word in ["amazing", "incredible", "awesome", "fantastic"]):
        hooks.append("This is absolutely mind-blowing...")
        hooks.append("You have to see this to believe it...")
    
    # Transform/change hooks
    if any(word in content_lower for word in ["change", "transform", "different", "new"]):
        hooks.append("This completely changed my perspective...")
        hooks.append("My life before vs after this...")
    
    # Time-based hooks
    if any(word in content_lower for word in ["day", "week", "month", "year", "time"]):
        hooks.append("What I learned in 30 days...")
        hooks.append("This happened in just 24 hours...")
    
    # Return top hooks with variety
    return hooks[:8]

def generate_hooks(content: str, persona: str) -> List[str]:
    """Generate viral hooks based on content and persona"""
    return generate_enhanced_hooks(content, persona)

def generate_enhanced_summary(text: str) -> str:
    """Enhanced summary generation"""
    if not text or len(text) < 50:
        return "Video content analysis in progress..."
    
    # Split into sentences
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    
    if len(sentences) < 3:
        return text[:300] + "..." if len(text) > 300 else text
    
    # Try to create a meaningful summary
    if len(sentences) >= 3:
        # Take first sentence, a middle one, and last one
        middle_idx = len(sentences) // 2
        summary_parts = [sentences[0], sentences[middle_idx], sentences[-1]]
        summary = ". ".join(summary_parts) + "."
    else:
        summary = ". ".join(sentences) + "."
    
    # Ensure summary is reasonable length
    if len(summary) > 400:
        summary = summary[:400] + "..."
    
    return summary

def generate_summary(text: str) -> str:
    """Generate a summary of the video content"""
    return generate_enhanced_summary(text)

async def download_video(url: str) -> tuple:
    """Download video and extract audio using yt-dlp"""
    try:
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        
        # Download video info first
        cmd_info = [
            "/root/.venv/bin/yt-dlp",
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
            "/root/.venv/bin/yt-dlp",
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
    """Transcribe audio using faster-whisper"""
    try:
        from faster_whisper import WhisperModel
        
        # Initialize model (using base model for speed)
        model = WhisperModel("base", device="cpu", compute_type="int8")
        
        # Transcribe the audio file
        segments, info = model.transcribe(audio_file, beam_size=5)
        
        # Extract text from segments
        transcription = ""
        for segment in segments:
            transcription += segment.text + " "
        
        return transcription.strip()
        
    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        # Fallback to mock transcription if Whisper fails
        return "Mock transcription: Video content analysis. The speaker discusses various topics that can be used for hook generation."

# API routes
@app.get("/")
async def root():
    return {"message": "AyoVirals API 2.0 is running! 🔥", "version": "2.0.0"}

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy", 
        "database": "connected" if db is not None else "disconnected",
        "nlp": "enabled" if nlp is not None else "disabled",
        "version": "2.0.0"
    }

@app.post("/api/process-video")
async def process_video(request: VideoRequest):
    """Enhanced video processing with AI-powered analysis"""
    try:
        # Validate URL
        if not request.video_url.strip():
            raise HTTPException(status_code=400, detail="Video URL is required")
        
        # Detect platform
        platform = detect_platform(request.video_url)
        
        # Generate unique ID
        video_id = str(uuid.uuid4())
        
        # Try to download and process video
        try:
            logger.info(f"Processing video: {request.video_url}")
            
            # Download video and extract audio
            audio_file, title, description = await download_video(request.video_url)
            
            if audio_file:
                # Transcribe audio
                transcription = await transcribe_audio(audio_file)
                
                # Use real transcription for content analysis
                content_for_analysis = f"{title}. {description}. {transcription}"
                
                # Clean up audio file
                try:
                    import os
                    os.remove(audio_file)
                    # Also remove parent directory if it's a temp directory
                    parent_dir = os.path.dirname(audio_file)
                    if "tmp" in parent_dir:
                        import shutil
                        shutil.rmtree(parent_dir, ignore_errors=True)
                except Exception as e:
                    logger.warning(f"Cleanup error: {str(e)}")
                
                logger.info(f"Video processed successfully: {title}")
                
            else:
                # Fallback to mock content if download fails
                logger.warning("Video download failed, using enhanced mock content")
                content_for_analysis = f"Video analysis for {platform} content. Enhanced mock content for {request.persona} persona hook generation with viral patterns."
                
        except Exception as e:
            logger.error(f"Video processing error: {str(e)}")
            # Fallback to mock content if processing fails
            content_for_analysis = f"Video analysis for {platform} content. Enhanced mock content for {request.persona} persona hook generation with viral patterns."
        
        # Generate enhanced hooks
        hooks = generate_hooks(content_for_analysis, request.persona)
        
        # Generate enhanced keywords
        persona_keywords = PERSONAS.get(request.persona, PERSONAS["viral-trends"])["keywords"]
        content_keywords = extract_keywords_from_text(content_for_analysis)
        all_keywords = persona_keywords + content_keywords
        
        # Remove duplicates while preserving order
        unique_keywords = []
        seen = set()
        for keyword in all_keywords:
            if keyword not in seen:
                unique_keywords.append(keyword)
                seen.add(keyword)
        
        # Generate enhanced summary
        summary = generate_summary(content_for_analysis)
        
        # Create response
        response = {
            "id": video_id,
            "summary": summary,
            "hooks": hooks,
            "keywords": unique_keywords,
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
                    "keywords": unique_keywords,
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
    """Get enhanced personas with viral patterns"""
    return {
        "personas": [
            {
                "id": key, 
                "name": value["name"],
                "description": f"{len(value['hook_templates'])} hook templates",
                "emotion_focus": value.get("emotion_focus", "general")
            }
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

@app.get("/api/viral-patterns")
async def get_viral_patterns():
    """Get viral patterns for analysis"""
    return {
        "patterns": VIRAL_PATTERNS,
        "personas": {key: value["viral_triggers"] for key, value in PERSONAS.items()}
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)