# AyoVirals - Hook & Keyword Generator 🔥

**Transform any video into viral content with AI-powered hooks and keywords!**

AyoVirals is a powerful tool that processes video links from YouTube, TikTok, Instagram, Facebook, and Twitter/X to generate viral hooks and keywords based on selected personas.

## ✨ Features

- **Multi-Platform Support**: YouTube, TikTok, Instagram, Facebook, Twitter/X
- **8 Viral Personas**: NYC Drama, Luxury Rentals, Fitness Guru, Conspiracy Mode, Lifestyle Flex, Storytime, Business Tips, Viral Trends
- **AI-Powered Analysis**: Hook scoring with viral potential indicators
- **Real-time Processing**: Video downloading, transcription, and analysis
- **Beautiful UI**: Modern, mobile-first design with glass morphism effects
- **Copy to Clipboard**: Easy sharing of generated content
- **Recent Videos**: History tracking for quick access

## 🚀 Quick Start on Replit

1. **Fork this Repl** or upload the files to your Replit environment
2. **Click the "Run" button** - everything will be set up automatically!
3. **Wait for startup** - The app will install dependencies and start both frontend and backend
4. **Access your app** - Open the web preview to use AyoVirals

## 📋 Manual Setup (if needed)

If you need to set up manually:

```bash
# Install Python dependencies
pip install -r backend/requirements.txt

# Install Node.js dependencies
cd frontend && yarn install

# Build frontend
yarn build

# Start the application
python main.py
```

## 🔧 Configuration

### Environment Variables

The app uses these environment variables (automatically set in Replit):

```bash
REACT_APP_BACKEND_URL=https://your-repl-name.your-username.repl.co
MONGO_URL=mongodb://localhost:27017
DB_NAME=ayovirals_db
PORT=3000
BACKEND_PORT=8001
```

### Database

- **MongoDB**: Runs locally in Replit for development
- **Data**: Stored in `/tmp/mongodb_data`
- **Persistence**: Data persists during your session

## 📱 How to Use

1. **Paste Video URL**: Support for YouTube, TikTok, Instagram, Facebook, Twitter/X
2. **Choose Persona**: Select from 8 viral personas
3. **Generate Content**: Click "Generate Viral Content"
4. **Copy & Share**: Use the generated hooks and keywords

## 🎭 Available Personas

- **🏙️ NYC Drama**: Urban lifestyle & apartment hunts
- **🏨 Luxury Rentals**: High-end property showcases
- **💪 Fitness Guru**: Motivational workout content
- **🔍 Conspiracy Mode**: Deep dive investigations
- **✨ Lifestyle Flex**: Aspirational daily routines
- **📖 Storytime**: Narrative-driven content
- **💼 Business Tips**: Entrepreneurial insights
- **🔥 Viral Trends**: Trending topic analysis

## 🛠️ Tech Stack

- **Frontend**: React 19, TailwindCSS, Modern UI Components
- **Backend**: FastAPI, Python 3.11
- **Database**: MongoDB
- **AI/ML**: spaCy NLP, faster-whisper
- **Video Processing**: yt-dlp
- **Deployment**: Replit-optimized with Nix

## 📊 Features Overview

### Hook Generation
- AI-powered viral hook templates
- Persona-specific content adaptation
- Viral score calculation (0-100)
- Character count optimization for each platform

### Keyword Extraction
- spaCy NLP for intelligent keyword extraction
- Platform-specific hashtag generation
- Persona-based keyword enhancement
- Frequency analysis and relevance scoring

### Video Processing
- Multi-platform video downloading
- Audio extraction and transcription
- Content analysis and summarization
- Real-time progress tracking

## 🔒 Privacy & Security

- **100% Self-Hosted**: No data leaves your Replit environment
- **No External API Keys**: Works completely offline
- **Temporary Storage**: Downloaded videos are automatically cleaned up
- **Local Processing**: All AI processing happens locally

## 🚨 Troubleshooting

### Common Issues

1. **MongoDB Connection Error**
   - MongoDB starts automatically, wait a few seconds
   - Check logs: `tail -f /tmp/logs/backend.log`

2. **Frontend Not Loading**
   - Ensure port 3000 is available
   - Check logs: `tail -f /tmp/logs/frontend.log`

3. **Video Processing Failed**
   - Some videos may be geo-blocked or private
   - Try a different video URL
   - Check backend logs for specific errors

### Development Mode

To run in development mode:

```bash
# Terminal 1 - Backend
cd backend
python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload

# Terminal 2 - Frontend  
cd frontend
yarn start

# Terminal 3 - MongoDB
mongod --dbpath /tmp/mongodb_data --port 27017
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

- **Issues**: Report bugs via GitHub Issues
- **Questions**: Check the documentation or create a discussion
- **Feature Requests**: We welcome new ideas!

---

**Made with ❤️ for viral content creators everywhere!**

> Transform your videos into viral sensations with AyoVirals - the ultimate hook and keyword generator!
