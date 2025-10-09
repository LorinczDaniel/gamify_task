# 🚀 Quest Master - Deployment Guide

## Quick Deploy to Render (FREE) ⭐

### Prerequisites
- GitHub account
- GitHub Desktop or Git CLI

---

## Step 1: Push Your Code to GitHub

### Using GitHub Desktop (Easiest):
1. **Download GitHub Desktop**: https://desktop.github.com/
2. **Open GitHub Desktop** → File → Add Local Repository
3. **Select** your `gamify_task` folder
4. **Create a new repository** on GitHub.com:
   - Go to https://github.com/new
   - Name: `quest-master` (or any name)
   - Make it **Public** or **Private** (both work)
   - Click "Create repository"
5. **Back in GitHub Desktop**:
   - Click "Publish repository"
   - Sign in to GitHub if needed
   - Uncheck "Keep this code private" (or keep checked)
   - Click "Publish repository"

### Using Command Line (Alternative):
```bash
# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Quest Master"

# Create repo on GitHub.com first, then:
git remote add origin https://github.com/YOUR_USERNAME/quest-master.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy to Render

### 2.1 Sign Up
1. Go to **https://render.com**
2. Click "Get Started for Free"
3. Sign up with **GitHub** (easiest)

### 2.2 Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Click **"Connect a repository"**
3. Select your **quest-master** repository
4. If not listed, click "Configure account" to grant access

### 2.3 Configure Service
Fill in these settings:

| Field | Value |
|-------|-------|
| **Name** | `quest-master` (or any name) |
| **Region** | Select closest to you |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |
| **Instance Type** | `Free` |

### 2.4 Environment Variables
Click **"Advanced"** → **Add Environment Variable**:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11.0` |
| `SECRET_KEY` | Click "Generate" |
| `FLASK_ENV` | `production` |

### 2.5 Deploy!
1. Click **"Create Web Service"**
2. Wait 2-5 minutes for deployment
3. Your app will be live at: `https://quest-master-XXXX.onrender.com`

---

## Step 3: Test Your Deployment

1. Visit your Render URL
2. Register a new account
3. Create a character
4. Add a quest and complete it
5. Test all features!

---

## ⚠️ Important Notes

### Database Persistence
- **SQLite on Render's free tier**: Database resets on each deploy/restart
- **For production**: Upgrade to persistent storage or use PostgreSQL

### To Add Persistent Storage:
1. In Render dashboard → Your service
2. Click **"Disks"** tab
3. Add disk: `/opt/render/project/src/data`
4. Update `database.py` to use: `DATABASE_NAME = 'data/quest_master.db'`

### Free Tier Limitations:
- App "sleeps" after 15 minutes of inactivity
- First request after sleep takes ~30 seconds
- Database may reset on redeploy
- 750 hours/month (enough for one app)

---

## 🎯 Alternative: Railway ($5/month)

Railway is simpler and better for serious projects:

### Deploy to Railway:
1. Go to **https://railway.app**
2. Sign up with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your **quest-master** repo
5. Railway auto-detects Python and deploys
6. Done! No configuration needed.

**Railway Advantages:**
- ✅ No sleep time
- ✅ Persistent disk by default
- ✅ Better performance
- ✅ $5 free credit, then $5/month

---

## 🐍 Alternative: PythonAnywhere (Python-Specific)

### Deploy to PythonAnywhere:
1. Go to **https://www.pythonanywhere.com**
2. Sign up for free account
3. Click **"Web"** tab → **"Add a new web app"**
4. Choose **Flask**
5. Upload your code via **Files** tab
6. Configure **WSGI file** to point to `app.py`
7. Click **"Reload"** and visit your site

**Free tier**: `yourusername.pythonanywhere.com`

---

## 💪 Advanced: DigitalOcean (Self-Hosted)

For full control and scalability:

### Cost: $6-12/month

### Quick Setup:
1. Create **DigitalOcean** account
2. Deploy **App Platform** (like Render but paid)
3. Or use **Droplet** (VPS) for more control

### Using App Platform:
1. Connect GitHub repo
2. DigitalOcean auto-detects Python
3. Configure and deploy
4. Get custom domain support

---

## 🌐 Custom Domain Setup (Optional)

### After deploying to Render/Railway:

1. **Buy a domain**: Namecheap, Google Domains ($10-15/year)
2. **In your hosting dashboard**:
   - Go to Settings → Custom Domains
   - Add your domain: `questmaster.com`
3. **In your domain registrar**:
   - Add CNAME record:
     - Name: `www`
     - Value: `your-app.onrender.com`
   - Add A record for root domain (Render provides IP)
4. Wait 5-60 minutes for DNS propagation
5. Enable **HTTPS** (automatic on Render/Railway)

---

## 📊 Monitoring Your App

### Render Dashboard:
- View logs: Click "Logs" tab
- Monitor usage: Check "Metrics"
- Restart service: Click "Manual Deploy"

### Add Application Monitoring:
```bash
# Add to requirements.txt
sentry-sdk==1.40.0

# In app.py add:
import sentry_sdk
sentry_sdk.init(dsn="YOUR_SENTRY_DSN")
```

Get free monitoring at: https://sentry.io

---

## 🔧 Troubleshooting

### "Application failed to start"
- Check Render logs
- Verify `gunicorn` is in requirements.txt
- Ensure `app.py` has `app` variable

### Database resets
- Enable persistent disk in Render
- Or migrate to PostgreSQL

### App is slow
- Free tier sleeps after inactivity (first load slow)
- Upgrade to paid tier ($7/month)
- Or use Railway instead

### Can't register users
- Check logs for errors
- Verify SECRET_KEY is set
- Test locally first

---

## 🎉 Your App is Live!

Share your link:
- 📱 On social media
- 👥 With friends and family
- 🌐 On ProductHunt (for feedback)
- 💼 On Reddit (r/productivity, r/SideProject)

---

## 🚀 Next Steps

1. **Add analytics**: Google Analytics, Plausible
2. **Set up monitoring**: Sentry for error tracking
3. **Enable backups**: Export database regularly
4. **Add email**: SendGrid for notifications
5. **Upgrade database**: PostgreSQL for production
6. **Add caching**: Redis for performance
7. **CDN**: Cloudflare for speed
8. **SEO**: Add meta tags, sitemap

---

## 💡 Pro Tips

### Update Your App:
```bash
# Make changes locally
git add .
git commit -m "Update features"
git push origin main

# Render auto-deploys from GitHub!
```

### View Logs:
- Render: Dashboard → Logs tab
- Railway: Dashboard → Deployments → View logs
- PythonAnywhere: Web tab → Log files

### Environment Variables:
- Never commit `.env` file
- Use Render's environment variables
- Generate secure SECRET_KEY

### Database Backups:
```python
# Add this endpoint to app.py
@app.route('/api/admin/backup')
def backup_db():
    # Download database backup
    pass
```

---

## 📚 Resources

- **Render Docs**: https://render.com/docs
- **Railway Docs**: https://docs.railway.app
- **Flask Production**: https://flask.palletsprojects.com/en/3.0.x/deploying/
- **Gunicorn Config**: https://docs.gunicorn.org/

---

**Need help? Open an issue on GitHub or check the deployment logs!** 🎮

---

## Quick Reference Commands

```bash
# Local testing
python app.py

# Install production dependencies
pip install -r requirements.txt

# Test with gunicorn locally
gunicorn app:app

# Push to GitHub
git add .
git commit -m "Your message"
git push origin main

# View Render logs (CLI)
render logs -s quest-master
```

---

**Deployment Time: ~5 minutes** ⚡
**Cost: FREE (with limitations)** 💰
**Difficulty: Easy** 😊

