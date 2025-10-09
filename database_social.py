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
    """Get public profile by username"""
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
        WHERE u.username = ? AND c.public_profile = 1
    ''', (username,))
    
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
    
    return dict(row)

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

