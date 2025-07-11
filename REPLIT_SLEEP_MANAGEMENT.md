# 🛡️ Replit Sleep Management Guide

## 🚨 The 30-Minute Sleep Problem

**Free Replit accounts** put repls to sleep after **30 minutes of inactivity**. This means:
- ❌ Your app becomes inaccessible
- ❌ All processes stop running
- ❌ Users get errors when trying to access your app

## 🔧 Solutions Available

### 1. **Replit Hacker/Pro Plan** (Best Solution) ⭐
- **Cost**: $7/month (Hacker) or $20/month (Pro)
- **Features**: 
  - ✅ Always On repls (never sleep)
  - ✅ Private repls
  - ✅ More CPU/RAM
  - ✅ Custom domains
  - ✅ Faster boot times

**How to enable:**
1. Upgrade to Hacker/Pro plan
2. Go to your repl settings
3. Enable "Always On" feature
4. Your repl will run 24/7

### 2. **Keep-Alive Service** (Free Solution) 🔄
I've created a keep-alive service that automatically pings your app every 25 minutes.

**Files created:**
- `keep_alive.py` - Keep-alive service
- `replit_config.py` - Replit configuration

**How it works:**
- Pings your app every 25 minutes (5 minutes before sleep)
- Keeps both frontend and backend alive
- Runs automatically when you start your app

**To use:**
```python
# Already integrated in main.py
from replit_config import setup_replit
setup_replit()  # Automatically enables keep-alive on Replit
```

### 3. **External Monitoring** (Free Alternative) 📡
Use external services to ping your repl:

**UptimeRobot (Free):**
1. Sign up at [uptimerobot.com](https://uptimerobot.com)
2. Add your repl URL for monitoring
3. Set check interval to 25 minutes
4. It will ping your app automatically

**Pingdom, StatusCake, etc.:**
- Similar services that can ping your repl
- Set up HTTP monitoring
- Use 25-minute intervals

### 4. **GitHub Actions** (Free Developer Solution) 🤖
Create a GitHub Action that pings your repl:

```yaml
# .github/workflows/keep-alive.yml
name: Keep Repl Alive
on:
  schedule:
    - cron: '*/25 * * * *'  # Every 25 minutes
  workflow_dispatch:

jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - name: Ping Repl
        run: |
          curl -f https://your-repl-name.your-username.repl.co/api/health
```

### 5. **Replit Database Solution** (Advanced) 🗄️
Use Replit's database to trigger activity:

```python
# In your main.py
import threading
import time
from replit import db

def database_heartbeat():
    while True:
        db['heartbeat'] = int(time.time())
        time.sleep(1500)  # 25 minutes

# Start in background
threading.Thread(target=database_heartbeat, daemon=True).start()
```

## 🎯 **Recommended Approach**

### For Development/Testing:
1. **Use the built-in keep-alive service** (already integrated)
2. **Set up UptimeRobot** as backup
3. **Pin your repl** to favorites for easy access

### For Production:
1. **Upgrade to Replit Hacker plan** ($7/month)
2. **Enable "Always On"** feature
3. **Use custom domain** for professional appearance

## 🔧 **Implementation in Your App**

The keep-alive service is **already integrated** in your AyoVirals app:

```python
# In main.py
from replit_config import setup_replit

class AyoViralsApp:
    def setup_environment(self):
        # ... existing code ...
        
        # Setup Replit configuration and keep-alive
        setup_replit()  # This automatically enables keep-alive
```

## 📊 **Keep-Alive Service Features**

✅ **Automatic Detection**: Detects if running on Replit
✅ **Smart Pinging**: Pings every 25 minutes (before sleep)
✅ **Dual Endpoints**: Pings both frontend and backend
✅ **Error Handling**: Continues working even if pings fail
✅ **Logging**: Shows ping status in console
✅ **Background Operation**: Runs as daemon thread

## 🚨 **Important Notes**

### Limitations:
- **Keep-alive only works while repl is running**
- **If repl crashes, keep-alive stops**
- **Replit may detect and limit excessive keep-alive attempts**

### Best Practices:
1. **Don't ping too frequently** (causes rate limiting)
2. **Use multiple methods** (keep-alive + external monitoring)
3. **Monitor your repl** regularly
4. **Consider upgrading** for serious projects

## 🎉 **Your Setup Status**

✅ **Keep-alive service integrated** in your AyoVirals app
✅ **Automatic Replit detection** enabled
✅ **Background pinging** configured
✅ **Error handling** implemented
✅ **Logging** for monitoring

**Your app will automatically:**
1. Detect if running on Replit
2. Start keep-alive service
3. Ping every 25 minutes
4. Log ping status
5. Continue running indefinitely

## 🔄 **Monitoring Your App**

Check if keep-alive is working:

```bash
# Look for these logs in console:
# "🔄 Keep-alive service started"
# "✅ Keep-alive ping successful"
# "⏰ Pinging every 25 minutes"
```

## 💡 **Pro Tips**

1. **Pin your repl** to prevent accidental deletion
2. **Use meaningful repl names** for easier management
3. **Set up external monitoring** as backup
4. **Consider upgrading** for production use
5. **Monitor resource usage** to avoid limits

---

## 🎯 **Quick Setup Checklist**

- ✅ Keep-alive service integrated in your app
- ✅ Replit configuration ready
- ✅ Automatic detection enabled
- ✅ Background pinging configured
- ☐ Set up external monitoring (UptimeRobot)
- ☐ Consider upgrading to Hacker plan
- ☐ Pin your repl to favorites

**Your AyoVirals app is ready to stay awake on Replit!** 🚀