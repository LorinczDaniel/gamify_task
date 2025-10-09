# 🚀 Deploy Quest Master in 5 Minutes

## Fastest Path: Railway (Recommended)

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Ready to deploy"
   git branch -M main
   # Create repo on github.com/new, then:
   git remote add origin https://github.com/YOUR_USERNAME/quest-master.git
   git push -u origin main
   ```

2. **Deploy:**
   - Go to https://railway.app
   - Sign up with GitHub (1 click)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your quest-master repo
   - **Done!** Railway auto-deploys in ~2 minutes

3. **Get your URL:**
   - Click on your deployment
   - Go to Settings → Generate Domain
   - Visit: `https://quest-master-production-XXXX.up.railway.app`

**Total time: 5 minutes** ⚡

---

## Alternative: Render (Free)

1. Push to GitHub (same as above)
2. Go to https://render.com → Sign up with GitHub
3. New Web Service → Connect repository
4. Settings:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`
   - Add env var: `SECRET_KEY` (click Generate)
5. Create Web Service
6. Wait 3 minutes → Live!

---

## Files I Created:

✅ `render.yaml` - Render config
✅ `Procfile` - Railway/Heroku config  
✅ `runtime.txt` - Python version
✅ `.gitignore` - Protect sensitive files
✅ Updated `requirements.txt` - Added gunicorn
✅ Updated `app.py` - Production-ready secret key

## You're ready to deploy! 🎉

Pick Railway or Render, follow steps above, and you're live in 5 minutes!

