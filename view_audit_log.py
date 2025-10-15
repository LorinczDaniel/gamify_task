"""
View Character Audit Log
Shows all character changes to detect any unexpected resets
"""
import sqlite3
from datetime import datetime

conn = sqlite3.connect('quest_master.db')
cursor = conn.cursor()

print("=" * 80)
print("CHARACTER AUDIT LOG")
print("=" * 80)

cursor.execute('''
    SELECT 
        id, user_id, character_id, event_type, 
        old_level, new_level, old_xp, new_xp, old_gold, new_gold,
        triggered_by, timestamp
    FROM character_audit_log
    ORDER BY timestamp DESC
    LIMIT 50
''')

rows = cursor.fetchall()

if not rows:
    print("\nNo audit log entries found.")
else:
    print(f"\nShowing {len(rows)} most recent events:\n")
    print(f"{'Time':<20} {'Event':<20} {'User':<6} {'Char':<6} {'Level':<12} {'XP':<15} {'Gold':<15}")
    print("-" * 110)
    
    for row in rows:
        event_id, user_id, char_id, event_type, old_lvl, new_lvl, old_xp, new_xp, old_gold, new_gold, triggered_by, timestamp = row
        
        # Format timestamp
        try:
            dt = datetime.fromisoformat(timestamp)
            time_str = dt.strftime("%m/%d %H:%M:%S")
        except:
            time_str = timestamp[:19] if timestamp else "N/A"
        
        # Format level change
        if event_type == 'LEVEL_UP':
            level_str = f"{old_lvl} → {new_lvl}"
            xp_str = f"{old_xp} → {new_xp}"
            gold_str = f"{old_gold} → {new_gold}"
        elif event_type == 'CHARACTER_CREATED':
            level_str = f"1 (new)"
            xp_str = "0 (new)"
            gold_str = "0 (new)"
        else:
            level_str = f"{new_lvl}"
            xp_str = f"{new_xp}"
            gold_str = f"{new_gold}"
        
        print(f"{time_str:<20} {event_type:<20} {user_id:<6} {char_id:<6} {level_str:<12} {xp_str:<15} {gold_str:<15}")

# Check for suspicious events
print("\n" + "=" * 80)
print("SUSPICIOUS EVENTS CHECK")
print("=" * 80)

# Check for multiple character creations for same user
cursor.execute('''
    SELECT user_id, COUNT(*) as creation_count
    FROM character_audit_log
    WHERE event_type = 'CHARACTER_CREATED'
    GROUP BY user_id
    HAVING creation_count > 1
''')

suspicious = cursor.fetchall()
if suspicious:
    print("\n⚠️  ALERT: Multiple character creations detected!")
    for user_id, count in suspicious:
        print(f"   User {user_id}: {count} characters created")
else:
    print("\n✓ No multiple character creations detected")

# Check for level decreases (shouldn't happen!)
cursor.execute('''
    SELECT user_id, character_id, old_level, new_level, timestamp
    FROM character_audit_log
    WHERE event_type = 'LEVEL_UP' AND new_level < old_level
''')

level_drops = cursor.fetchall()
if level_drops:
    print("\n🚨 CRITICAL: Level DECREASE detected!")
    for user_id, char_id, old_lvl, new_lvl, timestamp in level_drops:
        print(f"   User {user_id}, Char {char_id}: Level {old_lvl} → {new_lvl} at {timestamp}")
else:
    print("✓ No level decreases detected")

conn.close()
print("\n" + "=" * 80)



