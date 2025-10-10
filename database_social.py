"""
Social features for Quest Master
Leaderboards, public profiles, and sharing functionality
"""

import sqlite3
from typing import List, Dict, Any, Optional
from database import get_db

def get_leaderboard(timeframe: str = 'all', limit: int = 100) -> List[Dict[str, Any]]:
    """Get leaderboard of top players
    
    Args:
        timeframe: 'daily', 'weekly', 'monthly', or 'all'
        limit: Number of players to return
    """
    conn = get_db()
    cursor = conn.cursor()
    
    # Build query based on timeframe
    query = '''
        SELECT 
            c.id,
            c.name,
            c.level,
            c.xp,
            c.gold,
            c.character_class,
            c.avatar_id,
            c.color_theme,
            c.total_quests_completed,
            c.total_monsters_defeated,
            u.username,
            u.created_at
        FROM character c
        JOIN user u ON c.user_id = u.id
        WHERE c.public_profile = 1
    '''
    
    # Filter by timeframe based on character creation date or activity
    # For now, we'll just order by level and XP
    # TODO: Add last_active timestamp for better timeframe filtering
    
    query += '''
        ORDER BY c.level DESC, c.xp DESC
        LIMIT ?
    '''
    
    cursor.execute(query, (limit,))
    rows = cursor.fetchall()
    conn.close()
    
    leaderboard = []
    for idx, row in enumerate(rows, 1):
        leaderboard.append({
            'rank': idx,
            'character_id': row[0],
            'name': row[1],
            'level': row[2],
            'xp': row[3],
            'gold': row[4],
            'character_class': row[5] or 'Warrior',
            'avatar_id': row[6] or 1,
            'color_theme': row[7] or 'orange',
            'total_quests': row[8] or 0,
            'total_monsters': row[9] or 0,
            'username': row[10],
            'created_at': row[11]
        })
    
    return leaderboard

def get_public_profile(user_id: int) -> Optional[Dict[str, Any]]:
    """Get public profile for a user"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            c.*,
            u.username,
            u.created_at as user_created_at,
            (SELECT COUNT(*) FROM quest WHERE user_id = u.id AND completed = 1) as completed_quests,
            (SELECT COUNT(*) FROM battle_history WHERE character_id = c.id AND victory = 1) as battles_won,
            (SELECT COUNT(*) FROM character_achievement WHERE character_id = c.id) as achievements_count
        FROM character c
        JOIN user u ON c.user_id = u.id
        WHERE u.id = ? AND c.public_profile = 1
    ''', (user_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
    
    return dict(row)

def get_public_profile_by_username(username: str) -> Optional[Dict[str, Any]]:
    """Get enhanced public profile with all stats, achievements, equipment, and activity"""
    from datetime import datetime
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Get basic character and user info
    cursor.execute('''
        SELECT 
            c.*,
            u.username,
            u.created_at as user_created_at
        FROM character c
        JOIN user u ON c.user_id = u.id
        WHERE u.username = ? AND c.public_profile = 1
    ''', (username,))
    
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return None
    
    profile = dict(row)
    user_id = profile['user_id']
    character_id = profile['id']
    
    # Get quest stats
    cursor.execute('SELECT COUNT(*) FROM quest WHERE user_id = ? AND completed = 1', (user_id,))
    profile['completed_quests'] = cursor.fetchone()[0]
    
    # Get battle stats
    cursor.execute('SELECT COUNT(*) FROM battle WHERE character_id = ? AND won = 1', (character_id,))
    profile['battles_won'] = cursor.fetchone()[0]
    
    # Get achievements count
    cursor.execute('SELECT COUNT(*) FROM achievement WHERE unlocked = 1')
    profile['achievements_count'] = cursor.fetchone()[0]
    
    # Get unlocked achievements list
    cursor.execute('SELECT * FROM achievement WHERE unlocked = 1 ORDER BY unlocked_at DESC LIMIT 12')
    profile['achievements'] = [dict(row) for row in cursor.fetchall()]
    
    # Get equipped items
    cursor.execute('''
        SELECT i.name, i.type, i.rarity, i.attack_bonus, i.defense_bonus, i.health_bonus
        FROM inventory inv
        JOIN item i ON inv.item_id = i.id
        WHERE inv.character_id = ? AND inv.equipped = 1
    ''', (character_id,))
    profile['equipped_items'] = [dict(row) for row in cursor.fetchall()]
    
    # Get recent activity (last 10 completed quests)
    cursor.execute('''
        SELECT title, difficulty, xp_reward, gold_reward, completed_at
        FROM quest
        WHERE user_id = ? AND completed = 1
        ORDER BY completed_at DESC
        LIMIT 10
    ''', (user_id,))
    profile['recent_quests'] = [dict(row) for row in cursor.fetchall()]
    
    # Get recent battles (last 5)
    cursor.execute('''
        SELECT monster_name, monster_level, won, xp_gained, gold_gained, battled_at
        FROM battle
        WHERE character_id = ?
        ORDER BY battled_at DESC
        LIMIT 5
    ''', (character_id,))
    profile['recent_battles'] = [dict(row) for row in cursor.fetchall()]
    
    # Get daily challenge stats
    cursor.execute('''
        SELECT COUNT(*) as total_completed
        FROM user_daily_challenge
        WHERE user_id = ? AND completed = 1
    ''', (user_id,))
    profile['daily_challenges_completed'] = cursor.fetchone()[0]
    
    # Get today's challenge progress
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('''
        SELECT COUNT(*) as today_completed
        FROM user_daily_challenge udc
        JOIN daily_challenge dc ON udc.challenge_id = dc.id
        WHERE udc.user_id = ? AND udc.completed = 1 AND dc.challenge_date = ?
    ''', (user_id, today))
    profile['daily_challenges_today'] = cursor.fetchone()[0]
    
    # Get their rank
    profile['rank'] = get_user_rank(character_id)
    
    # Get activity streak (consecutive days with completed quests)
    profile['current_streak'] = calculate_streak(user_id)
    
    # Get weekly stats for graph
    profile['weekly_activity'] = get_weekly_activity_graph(user_id)
    
    conn.close()
    return profile

def toggle_public_profile(character_id: int, public: bool) -> bool:
    """Toggle public profile visibility"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            UPDATE character
            SET public_profile = ?
            WHERE id = ?
        ''', (1 if public else 0, character_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error toggling public profile: {e}")
        conn.close()
        return False

def increment_quest_counter(character_id: int):
    """Increment total quests completed counter"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            UPDATE character
            SET total_quests_completed = total_quests_completed + 1
            WHERE id = ?
        ''', (character_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error incrementing quest counter: {e}")
        conn.close()

def increment_monster_counter(character_id: int):
    """Increment total monsters defeated counter"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            UPDATE character
            SET total_monsters_defeated = total_monsters_defeated + 1
            WHERE id = ?
        ''', (character_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error incrementing monster counter: {e}")
        conn.close()

def get_user_rank(character_id: int) -> int:
    """Get user's current rank on leaderboard"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get character's level and XP
    cursor.execute('SELECT level, xp FROM character WHERE id = ?', (character_id,))
    char = cursor.fetchone()
    
    if not char:
        conn.close()
        return 0
    
    level, xp = char[0], char[1]
    
    # Count how many characters are ahead
    cursor.execute('''
        SELECT COUNT(*) + 1 as rank
        FROM character
        WHERE public_profile = 1
        AND (level > ? OR (level = ? AND xp > ?))
    ''', (level, level, xp))
    
    rank = cursor.fetchone()[0]
    conn.close()
    
    return rank

def calculate_streak(user_id: int) -> int:
    """Calculate consecutive days with completed quests"""
    from datetime import datetime, timedelta
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Get all distinct dates with completed quests, ordered by date descending
    cursor.execute('''
        SELECT DISTINCT DATE(completed_at) as quest_date
        FROM quest
        WHERE user_id = ? AND completed = 1
        ORDER BY quest_date DESC
    ''', (user_id,))
    
    dates = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    if not dates:
        return 0
    
    # Check if there's activity today or yesterday
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    # Convert string dates to date objects
    activity_dates = [datetime.strptime(d, '%Y-%m-%d').date() for d in dates]
    
    # Streak is broken if no activity today or yesterday
    if activity_dates[0] not in [today, yesterday]:
        return 0
    
    # Count consecutive days
    streak = 1
    current_date = activity_dates[0]
    
    for date in activity_dates[1:]:
        expected_previous = current_date - timedelta(days=1)
        if date == expected_previous:
            streak += 1
            current_date = date
        else:
            break
    
    return streak

def get_weekly_activity_graph(user_id: int, weeks: int = 4) -> List[Dict[str, Any]]:
    """Get quest completion activity for the last N weeks"""
    from datetime import datetime, timedelta
    
    conn = get_db()
    cursor = conn.cursor()
    
    activity = []
    
    # Get last N weeks
    for week_offset in range(weeks):
        week_start_dt = datetime.now() - timedelta(weeks=week_offset, days=datetime.now().weekday())
        week_start = week_start_dt.strftime('%Y-%m-%d')
        week_end = (week_start_dt + timedelta(days=7)).strftime('%Y-%m-%d')
        
        # Get quest count for this week
        cursor.execute('''
            SELECT COUNT(*) as count
            FROM quest
            WHERE user_id = ? AND completed = 1 
            AND completed_at >= ? AND completed_at < ?
        ''', (user_id, week_start, week_end))
        
        count = cursor.fetchone()[0]
        
        activity.append({
            'week_start': week_start,
            'week_label': week_start_dt.strftime('%b %d'),
            'quests_completed': count
        })
    
    conn.close()
    
    # Reverse to show oldest to newest
    return list(reversed(activity))

