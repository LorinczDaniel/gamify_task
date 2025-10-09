# 🔧 Production Configuration Guide

## Database Persistence Options

### Problem
SQLite on free hosting (Render, Railway) may reset on redeploy or restart.

### Solutions

---

## Option 1: Persistent Disk (Render)

### Enable on Render:
1. Dashboard → Your service → "Disks" tab
2. Click "Add Disk"
3. **Name**: `database`
4. **Mount Path**: `/opt/render/project/src/data`
5. **Size**: 1GB (free)
6. Save

### Update database.py:
```python
import os

# At the top of database.py
# Check if we're on Render with persistent disk
if os.path.exists('/opt/render/project/src/data'):
    DATABASE_NAME = '/opt/render/project/src/data/quest_master.db'
else:
    DATABASE_NAME = 'quest_master.db'  # Local development
```

---

## Option 2: Railway Volumes (Automatic)

Railway automatically provides persistent storage:

1. Deploy to Railway (it auto-detects persistence)
2. Database persists across deploys
3. No configuration needed!

---

## Option 3: PostgreSQL (Production-Ready)

For serious production deployments, use PostgreSQL:

### Why PostgreSQL?
- ✅ Better concurrency (multiple users)
- ✅ Better data integrity
- ✅ Scales better
- ✅ Industry standard
- ✅ Free tier on most platforms

### Setup on Render:
1. Dashboard → New → PostgreSQL
2. **Name**: `quest-master-db`
3. **Database**: `quest_master`
4. **User**: Auto-generated
5. **Region**: Same as your app
6. **Plan**: Free
7. Click "Create Database"

### Update requirements.txt:
```txt
Flask==3.0.0
Flask-CORS==4.0.0
python-dotenv==1.0.0
gunicorn==21.2.0
psycopg2-binary==2.9.9
```

### Update database.py:
```python
import os
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db():
    """Get database connection"""
    if DATABASE_URL:
        # PostgreSQL in production
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    else:
        # SQLite in development
        conn = sqlite3.connect('quest_master.db')
        conn.row_factory = sqlite3.Row
    return conn
```

### Add Environment Variable:
In Render → Your service → Environment:
- **Key**: `DATABASE_URL`
- **Value**: (Copy from PostgreSQL database dashboard)

---

## Option 4: Supabase (Firebase Alternative)

Free PostgreSQL with extra features:

1. Go to https://supabase.com
2. Create new project
3. Get connection string
4. Add to environment variables
5. Use with psycopg2 (same as above)

**Benefits:**
- Free tier: 500MB database
- Built-in authentication
- Real-time features
- REST API
- Dashboard for data management

---

## Security Enhancements

### 1. Environment Variables

Create `.env` file locally (never commit):
```bash
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=postgresql://user:pass@host/db
FLASK_ENV=production
```

### 2. HTTPS Only

Add to `app.py`:
```python
from flask_talisman import Talisman

# Force HTTPS in production
if os.environ.get('FLASK_ENV') == 'production':
    Talisman(app, content_security_policy=None)
```

Add to `requirements.txt`:
```txt
flask-talisman==1.1.0
```

### 3. Rate Limiting

Prevent abuse with Flask-Limiter:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/register', methods=['POST'])
@limiter.limit("5 per hour")  # Limit registrations
def register():
    # ... existing code
```

Add to `requirements.txt`:
```txt
Flask-Limiter==3.5.0
```

### 4. CORS Configuration

Update CORS for production:
```python
# In app.py
if os.environ.get('FLASK_ENV') == 'production':
    CORS(app, origins=['https://your-domain.com'])
else:
    CORS(app)  # Allow all in development
```

---

## Performance Optimizations

### 1. Database Connection Pooling

For PostgreSQL:
```python
from psycopg2 import pool

db_pool = pool.SimpleConnectionPool(1, 20, DATABASE_URL)

def get_db():
    return db_pool.getconn()

def close_db(conn):
    db_pool.putconn(conn)
```

### 2. Caching

Add Redis for caching:
```python
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.environ.get('REDIS_URL', 'redis://localhost:6379')
})

@app.route('/api/shop/items')
@cache.cached(timeout=300)  # Cache for 5 minutes
def get_shop_items():
    # ... existing code
```

### 3. Gzip Compression

```python
from flask_compress import Compress

Compress(app)
```

Add to requirements.txt:
```txt
Flask-Compress==1.14
```

---

## Monitoring & Logging

### 1. Sentry (Error Tracking)

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

if os.environ.get('SENTRY_DSN'):
    sentry_sdk.init(
        dsn=os.environ.get('SENTRY_DSN'),
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0
    )
```

Free at https://sentry.io

### 2. Application Logs

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

logger = logging.getLogger(__name__)

@app.route('/api/login', methods=['POST'])
def login():
    logger.info(f"Login attempt for user: {username}")
    # ... existing code
```

---

## Backup Strategy

### Automatic Daily Backups

Create `backup.py`:
```python
import sqlite3
import boto3
from datetime import datetime
import os

def backup_database():
    """Backup database to S3 or local storage"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f'backup_{timestamp}.db'
    
    # Copy database
    conn = sqlite3.connect('quest_master.db')
    backup_conn = sqlite3.connect(backup_file)
    conn.backup(backup_conn)
    backup_conn.close()
    conn.close()
    
    # Upload to S3 (optional)
    if os.environ.get('AWS_ACCESS_KEY'):
        s3 = boto3.client('s3')
        s3.upload_file(backup_file, 'my-bucket', f'backups/{backup_file}')
    
    print(f"Backup created: {backup_file}")

if __name__ == '__main__':
    backup_database()
```

Run daily with cron or Render cron jobs.

---

## Scaling Checklist

When you have 100+ users:

- [ ] Migrate to PostgreSQL
- [ ] Add Redis caching
- [ ] Enable CDN (Cloudflare)
- [ ] Add rate limiting
- [ ] Set up monitoring (Sentry)
- [ ] Enable database backups
- [ ] Add load balancer (if needed)
- [ ] Optimize database queries
- [ ] Add database indexes
- [ ] Consider microservices architecture

---

## Cost Breakdown (Monthly)

### Free Tier (0-100 users):
- Hosting: $0 (Render/Railway free tier)
- Database: $0 (SQLite or PostgreSQL free tier)
- Monitoring: $0 (Sentry free tier)
- **Total: $0**

### Starter (100-1000 users):
- Hosting: $7 (Render/Railway paid)
- Database: $7 (PostgreSQL)
- Redis: $5 (optional)
- Monitoring: $0-26 (Sentry)
- **Total: $14-45**

### Growth (1000-10,000 users):
- Hosting: $25 (multiple instances)
- Database: $15-50 (larger PostgreSQL)
- Redis: $15
- CDN: $5 (Cloudflare paid)
- Monitoring: $26+ (Sentry)
- **Total: $86-131**

### Scale (10,000+ users):
- AWS/GCP/Azure: $200-1000+
- Load balancer: $20+
- Multiple databases: $100+
- Full monitoring: $100+
- **Total: $420-1200+**

---

## Quick Production Setup

For immediate production deployment:

```bash
# 1. Update requirements.txt
echo "flask-talisman==1.1.0" >> requirements.txt
echo "Flask-Limiter==3.5.0" >> requirements.txt
echo "sentry-sdk==1.40.0" >> requirements.txt

# 2. Set environment variables in Render/Railway
SECRET_KEY=<generate-secure-key>
FLASK_ENV=production
DATABASE_URL=<your-postgres-url>  # optional
SENTRY_DSN=<your-sentry-dsn>  # optional

# 3. Deploy!
git add .
git commit -m "Production ready"
git push origin main
```

---

## Summary

**Minimum for launch:**
- ✅ Deploy to Render/Railway
- ✅ Set SECRET_KEY
- ✅ Enable HTTPS (automatic)

**Recommended for production:**
- ✅ PostgreSQL database
- ✅ Error monitoring (Sentry)
- ✅ Rate limiting
- ✅ Regular backups

**Optional but great:**
- Redis caching
- CDN (Cloudflare)
- Load balancer
- Microservices

---

**Start simple, scale as you grow!** 🚀

