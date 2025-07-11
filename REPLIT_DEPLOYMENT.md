# 🚀 Replit Deployment Guide for AyoVirals

This guide will help you deploy AyoVirals on Replit in just a few steps!

## 📋 Prerequisites

- A Replit account (free tier works perfectly!)
- Basic understanding of web applications (optional)

## 🎯 One-Click Deployment

### Method 1: Fork from GitHub (Recommended)

1. **Go to Replit**: Visit [replit.com](https://replit.com)
2. **Create New Repl**: Click "Create Repl"
3. **Import from GitHub**: Choose "Import from GitHub"
4. **Enter Repository**: Paste your GitHub repository URL
5. **Click "Import"**: Replit will automatically detect the configuration
6. **Click "Run"**: Everything will be set up automatically!

### Method 2: Manual Upload

1. **Create New Repl**: Choose "Python" as the language
2. **Upload Files**: Use the file explorer to upload all project files
3. **Ensure Structure**: Make sure the file structure matches:
   ```
   /
   ├── .replit
   ├── replit.nix
   ├── main.py
   ├── requirements.txt
   ├── backend/
   │   ├── server.py
   │   ├── requirements.txt
   │   └── .env
   ├── frontend/
   │   ├── package.json
   │   ├── src/
   │   └── .env
   └── README.md
   ```
4. **Click "Run"**: The application will start automatically

## ⚙️ Configuration

### Automatic Configuration

The `.replit` file automatically configures:
- Python 3.11 environment
- Node.js 18 for React frontend
- MongoDB for local database
- Environment variables
- Port settings (3000 for frontend, 8001 for backend)

### Manual Configuration (if needed)

If you need to customize settings:

1. **Edit `.replit`**: Modify the run command or environment variables
2. **Update `replit.nix`**: Add or remove system dependencies
3. **Modify `main.py`**: Adjust startup behavior

## 🔧 Environment Variables

The following environment variables are automatically set:

```bash
# Required for Replit
REACT_APP_BACKEND_URL=https://your-repl-name.your-username.repl.co
MONGO_URL=mongodb://localhost:27017
DB_NAME=ayovirals_db
PORT=3000
BACKEND_PORT=8001

# Optional (already set)
NODE_ENV=production
PYTHONPATH=/app
```

## 🚀 Startup Process

When you click "Run", the application:

1. **Installs Dependencies**: Python packages and Node.js modules
2. **Starts MongoDB**: Local database server
3. **Builds Frontend**: React production build
4. **Starts Backend**: FastAPI server on port 8001
5. **Starts Frontend**: React development server on port 3000
6. **Opens Web Preview**: Your app is ready to use!

## 🌐 Accessing Your App

### Web Preview
- **Frontend**: Available in the Replit web preview
- **Backend API**: Access via `https://your-repl-name.your-username.repl.co/api/`
- **Health Check**: `https://your-repl-name.your-username.repl.co/api/health`

### Custom Domain (Replit Hacker Plan)
If you have a Replit Hacker plan, you can use a custom domain:
1. Go to your Repl settings
2. Add your custom domain
3. Update the `REACT_APP_BACKEND_URL` environment variable

## 📊 Monitoring & Debugging

### Logs
Monitor your application with:
- **Console**: Real-time logs in the Replit console
- **Backend Logs**: `/tmp/logs/backend.log`
- **Frontend Logs**: `/tmp/logs/frontend.log`

### Debug Mode
To run in debug mode:
1. Stop the current run
2. Open Shell
3. Run: `python main.py` manually
4. Monitor output for detailed debugging

## 🔒 Security & Privacy

### Data Security
- **Local Processing**: All data stays in your Replit environment
- **No External APIs**: No data sent to third-party services
- **Temporary Storage**: Video files are automatically cleaned up

### Environment Security
- **Private Variables**: Use Replit's Secrets for sensitive data
- **HTTPS**: All Replit apps use HTTPS by default
- **Access Control**: Configure who can view your Repl

## 🛠️ Customization

### Adding Features
1. **Backend**: Modify `backend/server.py` to add new API endpoints
2. **Frontend**: Update `frontend/src/App.js` for UI changes
3. **Database**: Add new collections or modify existing ones

### Styling
- **TailwindCSS**: Pre-configured for easy styling
- **Custom CSS**: Add styles to `frontend/src/App.css`
- **Responsive Design**: Mobile-first approach already implemented

## 🚨 Troubleshooting

### Common Issues

#### "Module not found" Error
```bash
# Solution: Install missing dependencies
pip install -r requirements.txt
cd frontend && yarn install
```

#### MongoDB Connection Failed
```bash
# Solution: Restart MongoDB
pkill mongod
mongod --dbpath /tmp/mongodb_data --port 27017 --bind_ip 127.0.0.1 &
```

#### Frontend Not Loading
```bash
# Solution: Check port availability
lsof -i :3000
# Kill process if needed
kill -9 [PID]
```

#### Backend API Error
```bash
# Solution: Check backend logs
tail -f /tmp/logs/backend.log
# Or restart backend
cd backend && python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

### Performance Tips

1. **Keep Repl Active**: Pin your Repl to prevent sleeping
2. **Optimize Build**: Use production builds for better performance
3. **Monitor Resources**: Check CPU/memory usage in Replit

## 📈 Scaling

### Replit Limitations
- **Always-On**: Requires Replit Hacker plan for 24/7 availability
- **CPU/Memory**: Limited by Replit's resource constraints
- **Database**: Local MongoDB has storage limits

### Production Deployment
For production use, consider:
- **MongoDB Atlas**: For persistent, scalable database
- **Dedicated Hosting**: For higher resource requirements
- **CDN**: For faster global access

## 🎉 Success!

Once deployed, you'll have:
- ✅ Full-stack AyoVirals application
- ✅ AI-powered hook and keyword generation
- ✅ Multi-platform video processing
- ✅ Beautiful, responsive UI
- ✅ Local database storage
- ✅ HTTPS-enabled public URL

## 🆘 Getting Help

### Support Channels
- **GitHub Issues**: Report bugs and request features
- **Replit Community**: Ask questions in the Replit Discord
- **Documentation**: Check the README for detailed information

### Quick Help Commands
```bash
# Check if services are running
ps aux | grep -E "(mongod|uvicorn|node)"

# View all logs
tail -f /tmp/logs/*.log

# Restart everything
python main.py
```

---

**🎊 Congratulations! Your AyoVirals app is now live on Replit!**

Visit your web preview and start generating viral content! 🔥