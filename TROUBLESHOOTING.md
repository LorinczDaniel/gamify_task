# Character Level Reset - Troubleshooting Guide

## Problem
A user's character dropped from a higher level back to level 1.

## Current Status
✅ Your character is currently at **Level 8** (not level 1)
✅ Audit logging system is now in place
✅ Debug warnings added to detect the issue

## Root Cause
The app auto-creates a new level 1 character if it can't find an existing one. This can happen due to:
- Session corruption
- Database connection issues  
- User logging into wrong account
- Database file being replaced

## How to Diagnose

### 1. Check Audit Log
```bash
python view_audit_log.py
```

Look for:
- Multiple `CHARACTER_CREATED` events for the same user (🚨 problem!)
- Level decreases (🚨 should never happen!)

### 2. Check Application Logs
When running the app, watch for:
```
WARNING: No character found for user_id X, creating new character
```

### 3. Verify Database
```bash
python -c "import sqlite3; conn = sqlite3.connect('quest_master.db'); cursor = conn.cursor(); cursor.execute('SELECT id, user_id, name, level, xp, gold FROM character'); [print(f'ID:{r[0]} UserID:{r[1]} Name:{r[2]} Level:{r[3]} XP:{r[4]} Gold:{r[5]}') for r in cursor.fetchall()]; conn.close()"
```

## Prevention

### Daily Backup
Run this before making changes:
```bash
python backup_database.py
```

### Monitor Audit Log
Check weekly for suspicious activity:
```bash
python view_audit_log.py
```

## Recovery (If Level Reset Happens Again)

### Step 1: Check Audit Log
```bash
python view_audit_log.py
```

Look for the last known good level in the `LEVEL_UP` events.

### Step 2: Restore from Backup
```bash
# List available backups
dir backups

# Copy the most recent good backup
copy backups\quest_master_backup_YYYYMMDD_HHMMSS.db quest_master.db
```

### Step 3: Manual Recovery (if no backup)
If you know the correct level, you can manually fix it:

```python
import sqlite3

conn = sqlite3.connect('quest_master.db')
cursor = conn.cursor()

# Update character to correct level
character_id = 1  # Change if needed
correct_level = 8  # Change to actual level

# Recalculate stats based on level
new_attack = 10 + (correct_level - 1) * 3
new_defense = 5 + (correct_level - 1) * 2
new_max_health = 100 + (correct_level - 1) * 10

cursor.execute('''
    UPDATE character 
    SET level = ?, attack = ?, defense = ?, max_health = ?, health = ?
    WHERE id = ?
''', (correct_level, new_attack, new_defense, new_max_health, new_max_health, character_id))

conn.commit()
print(f"✓ Character {character_id} restored to level {correct_level}")
conn.close()
```

## Long-term Solutions

### Option 1: Prevent Auto-Creation
Edit `app.py` to return an error instead of auto-creating:

```python
if not char:
    return jsonify({'error': 'Character not found'}), 404
```

### Option 2: Add User Confirmation
Before creating a new character, check if there's audit history and warn the user.

### Option 3: Use Character History
Query audit log before creating to see if user had a character before.

## Contact Support
If this happens in production:
1. Don't panic - check backups first
2. Review audit log: `python view_audit_log.py`
3. Check which user account you're logged in as
4. Verify database file hasn't been replaced

## Files
- `view_audit_log.py` - View character change history
- `backup_database.py` - Create database backup
- `quest_master.db` - Current database
- `backups/` - Database backups directory



