# 🔐 Authentication System Documentation

## Overview

Quest Master now supports **multiple user accounts**! Each user gets their own:
- ✅ Character with unique progress
- ✅ Personal quest list
- ✅ Individual inventory and equipment
- ✅ Separate battle history
- ✅ Independent achievements

---

## Features

### 👤 User Registration
- Create account with username + password
- Choose your character name (or use username)
- Secure password hashing (werkzeug)
- Automatic character creation
- Instant login after registration

### 🔐 Login System
- Session-based authentication
- Secure password verification
- "Remember me" via session cookies
- Auto-redirect if not logged in

### 🚪 Logout
- Logout button in top-right of game
- Clears session data
- Redirects to login page

---

## Security Features

### Password Protection
- **Hashed passwords** using werkzeug.security
- Never stored in plain text
- Industry-standard bcrypt hashing

### Session Management
- Secure session cookies
- Random secret key generated on startup
- Session expires when browser closes

### Input Validation
- Username: minimum 3 characters
- Password: minimum 6 characters
- Prevents duplicate usernames
- SQL injection protection (parameterized queries)

---

## Database Schema Changes

### New Tables

**user**
```sql
id              INTEGER PRIMARY KEY
username        TEXT UNIQUE NOT NULL
password_hash   TEXT NOT NULL
created_at      TIMESTAMP
```

### Modified Tables

**character**
- Added `user_id` foreign key
- Each user gets ONE character
- Character tied to user account

**quest**
- Added `user_id` foreign key
- Quests are user-specific
- Users only see their own quests

---

## API Changes

### New Endpoints

**POST /api/register**
```json
Request:
{
  "username": "string",
  "password": "string",
  "character_name": "string" (optional)
}

Response (201):
{
  "success": true,
  "user": { "id": 1, "username": "..." },
  "character": { ... }
}
```

**POST /api/login**
```json
Request:
{
  "username": "string",
  "password": "string"
}

Response (200):
{
  "success": true,
  "message": "Logged in successfully"
}
```

**POST /api/logout**
```json
Response (200):
{
  "success": true,
  "message": "Logged out successfully"
}
```

### Updated Endpoints

**All API endpoints now:**
- ✅ Require authentication (@login_required decorator)
- ✅ Return 401 if not logged in
- ✅ Use session['user_id'] to get current user
- ✅ Filter data by user (quests, stats, etc.)

---

## User Flow

### First Time User

1. Visit http://localhost:5000
2. Redirected to `/login`
3. Click "Create One" → `/register`
4. Fill in username, password, character name
5. Click "Begin Your Adventure"
6. Auto-logged in → redirected to game
7. Character automatically created
8. Start playing!

### Returning User

1. Visit http://localhost:5000
2. Redirected to `/login`
3. Enter username + password
4. Click "Start Quest"
5. Logged in → see your character and progress!

### During Gameplay

- **Logout**: Click 🚪 Logout button (top-right)
- **Session persists**: Stay logged in until you close browser
- **Auto-redirect**: If session expires, redirected to login

---

## Migration Notes

### Existing Data

⚠️ **Important**: If you have existing character data:

The old database had ONE character (id=1) with no user association. After this update:

**Option 1: Fresh Start** (Recommended)
```bash
# Delete old database
del quest_master.db

# Start server (creates new database)
python app.py
```

**Option 2: Manual Migration** (Advanced)
You can manually create a user and link the existing character, but Option 1 is cleaner.

### New Installation

Fresh installs automatically create proper schema with user support!

---

## Code Architecture

### Backend (app.py)

**Authentication Decorator**
```python
@login_required
def protected_endpoint():
    user_id = session['user_id']
    # ... endpoint logic
```

**Session Data**
```python
session['user_id']     # Current user's ID
session['username']    # Current user's username
```

### Database (database.py)

**User Functions**
- `create_user(username, password)` - Register new user
- `verify_password(username, password)` - Validate login
- `get_user(user_id)` - Get user info
- `get_user_by_username(username)` - Lookup by username

**Character Functions**
- `get_character_by_user_id(user_id)` - Get user's character
- `create_character_for_user(user_id, name)` - Create character

**Updated Functions**
- `create_quest(user_id, ...)` - Now requires user_id
- `get_all_quests(user_id, ...)` - Filters by user
- `get_statistics(character_id)` - Filters stats by user

---

## Testing

### Test User Accounts

Create test accounts:
```
Username: hero1
Password: password123
Character: Sir Lancelot

Username: hero2  
Password: password123
Character: Merlin
```

### Verify Isolation

1. Login as hero1
2. Create quest "Test Quest 1"
3. Logout
4. Login as hero2
5. Verify you DON'T see "Test Quest 1"
6. ✅ Data is properly isolated!

---

## Security Considerations

### For Development ✅
- Session-based auth is fine
- Random secret key works
- Password hashing is secure

### For Production ⚠️
If deploying publicly, consider:
- Use persistent secret key (environment variable)
- Add HTTPS/SSL
- Rate limiting on login attempts
- Password strength requirements
- Email verification
- Password reset functionality
- CSRF protection (Flask-WTF)

---

## Future Enhancements

Possible additions:
- 📧 Email-based registration
- 🔑 Password reset via email
- 👥 Friend system
- 🏆 Global leaderboards
- 🎭 Multiple characters per user
- 🔒 Two-factor authentication
- 📱 Mobile app support
- 🌐 OAuth (Google, Discord login)

---

## Troubleshooting

**Can't login?**
- Check username/password are correct
- Try registering a new account
- Check browser console for errors

**Session expired?**
- Sessions clear on browser close
- Just login again

**Lost password?**
- Currently no password reset
- Create new account with different username

**Database errors?**
- If migrating from old version, delete `quest_master.db`
- Restart server to create fresh database

---

## Summary

✅ **Multi-user support** - Each person gets their own hero
✅ **Secure authentication** - Hashed passwords, session management
✅ **Data isolation** - Users only see their own data
✅ **Beautiful UI** - RPG-themed login/register pages
✅ **Easy to use** - Simple registration flow

**Your adventure is now personal!** 🎮✨

