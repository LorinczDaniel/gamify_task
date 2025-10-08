import sqlite3
import random
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

DATABASE_NAME = 'quest_master.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with all required tables"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Character table (linked to user)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS character (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            name TEXT NOT NULL,
            level INTEGER DEFAULT 1,
            xp INTEGER DEFAULT 0,
            gold INTEGER DEFAULT 0,
            health INTEGER DEFAULT 100,
            max_health INTEGER DEFAULT 100,
            attack INTEGER DEFAULT 10,
            defense INTEGER DEFAULT 5,
            combo_count INTEGER DEFAULT 0,
            last_quest_completed TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user(id)
        )
    ''')
    
    # Quests/Tasks table (linked to user)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quest (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            difficulty TEXT DEFAULT 'medium',
            xp_reward INTEGER NOT NULL,
            gold_reward INTEGER NOT NULL,
            completed BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user(id)
        )
    ''')
    
    # Equipment/Items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS item (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL,
            attack_bonus INTEGER DEFAULT 0,
            defense_bonus INTEGER DEFAULT 0,
            health_bonus INTEGER DEFAULT 0,
            rarity TEXT DEFAULT 'common'
        )
    ''')
    
    # Character inventory
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            character_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            equipped BOOLEAN DEFAULT 0,
            FOREIGN KEY (character_id) REFERENCES character(id),
            FOREIGN KEY (item_id) REFERENCES item(id)
        )
    ''')
    
    # Achievements table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS achievement (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            icon TEXT,
            requirement_type TEXT NOT NULL,
            requirement_value INTEGER NOT NULL,
            unlocked BOOLEAN DEFAULT 0,
            unlocked_at TIMESTAMP
        )
    ''')
    
    # Monster battles log
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS battle (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            character_id INTEGER NOT NULL,
            monster_name TEXT NOT NULL,
            monster_level INTEGER NOT NULL,
            won BOOLEAN NOT NULL,
            xp_gained INTEGER,
            gold_gained INTEGER,
            battled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (character_id) REFERENCES character(id)
        )
    ''')
    
    # Task templates for quick-add
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS task_template (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            difficulty TEXT DEFAULT 'medium',
            icon TEXT,
            category TEXT,
            popular BOOLEAN DEFAULT 0
        )
    ''')
    
    conn.commit()
    
    # Populate initial items if shop is empty
    cursor.execute('SELECT COUNT(*) FROM item')
    if cursor.fetchone()[0] == 0:
        populate_initial_items(conn)
    
    # Populate initial achievements if empty
    cursor.execute('SELECT COUNT(*) FROM achievement')
    if cursor.fetchone()[0] == 0:
        populate_initial_achievements(conn)
    
    # Populate task templates if empty
    cursor.execute('SELECT COUNT(*) FROM task_template')
    if cursor.fetchone()[0] == 0:
        populate_task_templates(conn)
    
    # Add new columns to existing character table if they don't exist
    try:
        cursor.execute('ALTER TABLE character ADD COLUMN combo_count INTEGER DEFAULT 0')
        cursor.execute('ALTER TABLE character ADD COLUMN last_quest_completed TIMESTAMP')
        conn.commit()
    except sqlite3.OperationalError:
        # Columns already exist
        pass
    
    # Try to add user_id column to existing character table
    try:
        cursor.execute('ALTER TABLE character ADD COLUMN user_id INTEGER')
        conn.commit()
    except sqlite3.OperationalError:
        # Column already exists
        pass
    
    # Try to add user_id column to existing quest table
    try:
        cursor.execute('ALTER TABLE quest ADD COLUMN user_id INTEGER')
        conn.commit()
    except sqlite3.OperationalError:
        # Column already exists
        pass
    
    # Create default demo user if no users exist
    cursor.execute('SELECT COUNT(*) FROM user')
    if cursor.fetchone()[0] == 0:
        create_demo_user(conn)
    
    conn.close()

def create_demo_user(conn):
    """Create a default demo user for easy testing"""
    from werkzeug.security import generate_password_hash
    
    cursor = conn.cursor()
    
    # Create demo user: username "user", password "user"
    password_hash = generate_password_hash("user")
    cursor.execute('''
        INSERT INTO user (username, password_hash)
        VALUES (?, ?)
    ''', ("user", password_hash))
    
    user_id = cursor.lastrowid
    
    # Create character for demo user
    cursor.execute('''
        INSERT INTO character (user_id, name, level, xp, gold)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, "Hero", 1, 0, 0))
    
    conn.commit()
    
    print("✨ Demo account created!")
    print("   Username: user")
    print("   Password: user")

def populate_initial_items(conn):
    """Add initial shop items"""
    items = [
        # Weapons
        ('Wooden Sword', 'weapon', 'A simple training sword', 50, 5, 0, 0, 'common'),
        ('Iron Sword', 'weapon', 'A sturdy iron blade', 200, 15, 0, 0, 'common'),
        ('Steel Sword', 'weapon', 'A well-crafted steel weapon', 500, 30, 0, 0, 'uncommon'),
        ('Legendary Blade', 'weapon', 'Forged by ancient smiths', 2000, 75, 0, 0, 'legendary'),
        
        # Armor
        ('Leather Armor', 'armor', 'Basic leather protection', 75, 0, 8, 0, 'common'),
        ('Iron Armor', 'armor', 'Heavy iron plating', 300, 0, 20, 0, 'common'),
        ('Steel Armor', 'armor', 'Masterwork steel armor', 750, 0, 40, 0, 'uncommon'),
        ('Dragon Scale Armor', 'armor', 'Armor made from dragon scales', 2500, 0, 100, 0, 'legendary'),
        
        # Accessories
        ('Health Potion', 'consumable', 'Restores 50 HP', 30, 0, 0, 50, 'common'),
        ('Ring of Power', 'accessory', 'Increases attack power', 400, 20, 0, 0, 'rare'),
        ('Amulet of Defense', 'accessory', 'Enhances defensive abilities', 400, 0, 25, 0, 'rare'),
        ('Crown of Vitality', 'accessory', 'Increases maximum health', 600, 0, 0, 100, 'rare'),
    ]
    
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO item (name, type, description, price, attack_bonus, defense_bonus, health_bonus, rarity)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', items)
    conn.commit()

def populate_initial_achievements(conn):
    """Add initial achievements"""
    achievements = [
        ('First Steps', 'Complete your first quest', '🎯', 'quests_completed', 1),
        ('Quest Warrior', 'Complete 10 quests', '⚔️', 'quests_completed', 10),
        ('Quest Master', 'Complete 50 quests', '👑', 'quests_completed', 50),
        ('Level Up!', 'Reach level 5', '⬆️', 'level', 5),
        ('Veteran', 'Reach level 10', '🌟', 'level', 10),
        ('Legendary Hero', 'Reach level 20', '💫', 'level', 20),
        ('Wealthy', 'Accumulate 1000 gold', '💰', 'gold_earned', 1000),
        ('Monster Slayer', 'Defeat 5 monsters', '🐉', 'monsters_defeated', 5),
        ('Shopping Spree', 'Purchase 5 items', '🛍️', 'items_purchased', 5),
    ]
    
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO achievement (name, description, icon, requirement_type, requirement_value)
        VALUES (?, ?, ?, ?, ?)
    ''', achievements)
    conn.commit()

def populate_task_templates(conn):
    """Add common task templates for quick-add"""
    templates = [
        # Household Chores
        ('Do the dishes', 'Wash and put away all dishes', 'easy', '🍽️', 'household', 1),
        ('Laundry', 'Wash, dry, and fold laundry', 'medium', '👕', 'household', 1),
        ('Clean room', 'Tidy up and organize bedroom', 'medium', '🧹', 'household', 1),
        ('Vacuum house', 'Vacuum all carpets and floors', 'medium', '🏠', 'household', 1),
        ('Take out trash', 'Empty all trash bins', 'easy', '🗑️', 'household', 1),
        ('Make bed', 'Make your bed neatly', 'easy', '🛏️', 'household', 1),
        ('Cook meal', 'Prepare a home-cooked meal', 'medium', '🍳', 'household', 1),
        ('Grocery shopping', 'Buy groceries for the week', 'medium', '🛒', 'household', 1),
        
        # Work/Study
        ('Study for 1 hour', 'Focused study session', 'hard', '📚', 'work', 1),
        ('Study for 30 min', 'Quick study session', 'medium', '📖', 'work', 1),
        ('Finish homework', 'Complete all pending homework', 'hard', '✏️', 'work', 1),
        ('Read 20 pages', 'Read educational material', 'medium', '📕', 'work', 1),
        ('Work on project', 'Make progress on main project', 'hard', '💼', 'work', 1),
        ('Answer emails', 'Clear email inbox', 'easy', '📧', 'work', 1),
        ('Attend meeting', 'Participate in scheduled meeting', 'medium', '👥', 'work', 1),
        
        # Health/Fitness
        ('Exercise 30 min', 'Workout or cardio session', 'hard', '💪', 'health', 1),
        ('Go for a walk', 'Take a 20-minute walk', 'easy', '🚶', 'health', 1),
        ('Drink 8 glasses water', 'Stay hydrated throughout day', 'easy', '💧', 'health', 1),
        ('Meditate 10 min', 'Mindfulness meditation', 'medium', '🧘', 'health', 1),
        ('Prepare healthy meal', 'Cook a nutritious meal', 'medium', '🥗', 'health', 1),
        
        # Self-care
        ('Shower/bath', 'Take a refreshing shower', 'easy', '🚿', 'self-care', 0),
        ('Brush teeth', 'Morning and evening dental care', 'easy', '🦷', 'self-care', 0),
        ('Skincare routine', 'Complete skincare regimen', 'easy', '✨', 'self-care', 0),
        ('Get 8 hours sleep', 'Maintain healthy sleep schedule', 'medium', '😴', 'self-care', 1),
        
        # Social
        ('Call family/friend', 'Catch up with loved ones', 'easy', '📞', 'social', 0),
        ('Plan social activity', 'Organize time with friends', 'medium', '🎉', 'social', 0),
        
        # Financial
        ('Pay bills', 'Handle monthly bill payments', 'easy', '💳', 'financial', 0),
        ('Budget review', 'Review spending and budget', 'medium', '💰', 'financial', 0),
    ]
    
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO task_template (title, description, difficulty, icon, category, popular)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', templates)
    conn.commit()

def calculate_xp_for_next_level(level: int) -> int:
    """Calculate XP needed for next level"""
    return int(100 * (1.5 ** (level - 1)))

def calculate_quest_rewards(difficulty: str) -> tuple:
    """Calculate XP and gold rewards based on difficulty"""
    rewards = {
        'easy': (20, 10),
        'medium': (50, 25),
        'hard': (100, 50),
        'epic': (200, 100)
    }
    return rewards.get(difficulty, rewards['medium'])

# Character operations
def create_character(name: str) -> Dict[str, Any]:
    """Create a new character"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO character (name) VALUES (?)
    ''', (name,))
    
    conn.commit()
    character_id = cursor.lastrowid
    conn.close()
    
    return get_character(character_id)

def get_character(character_id: int = 1) -> Optional[Dict[str, Any]]:
    """Get character by ID"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM character WHERE id = ?', (character_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        char = dict(row)
        char['xp_to_next_level'] = calculate_xp_for_next_level(char['level'])
        return char
    return None

def get_or_create_character() -> Dict[str, Any]:
    """Get the main character or create if doesn't exist"""
    char = get_character(1)
    if not char:
        char = create_character("Hero")
    return char

def update_character(character_id: int, **kwargs) -> Dict[str, Any]:
    """Update character attributes"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Build dynamic update query
    fields = []
    values = []
    for key, value in kwargs.items():
        fields.append(f"{key} = ?")
        values.append(value)
    
    values.append(character_id)
    query = f"UPDATE character SET {', '.join(fields)} WHERE id = ?"
    
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    
    return get_character(character_id)

def add_xp_and_gold(character_id: int, xp: int, gold: int) -> Dict[str, Any]:
    """Add XP and gold to character, handle level ups"""
    char = get_character(character_id)
    if not char:
        return None
    
    new_xp = char['xp'] + xp
    new_gold = char['gold'] + gold
    new_level = char['level']
    
    # Check for level ups
    while new_xp >= calculate_xp_for_next_level(new_level):
        new_xp -= calculate_xp_for_next_level(new_level)
        new_level += 1
        
        # Increase stats on level up
        new_health = char['max_health'] + 10
        new_attack = char['attack'] + 3
        new_defense = char['defense'] + 2
        
        char = update_character(
            character_id,
            level=new_level,
            max_health=new_health,
            health=new_health,
            attack=new_attack,
            defense=new_defense
        )
    
    return update_character(character_id, xp=new_xp, gold=new_gold)

# Quest operations
def create_quest(user_id: int, title: str, description: str = "", difficulty: str = "medium") -> Dict[str, Any]:
    """Create a new quest"""
    xp_reward, gold_reward = calculate_quest_rewards(difficulty)
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO quest (user_id, title, description, difficulty, xp_reward, gold_reward)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, title, description, difficulty, xp_reward, gold_reward))
    
    conn.commit()
    quest_id = cursor.lastrowid
    conn.close()
    
    return get_quest(quest_id)

def get_quest(quest_id: int) -> Optional[Dict[str, Any]]:
    """Get quest by ID"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM quest WHERE id = ?', (quest_id,))
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else None

def get_all_quests(user_id: int, completed: Optional[bool] = None) -> List[Dict[str, Any]]:
    """Get all quests for a user, optionally filtered by completion status"""
    conn = get_db()
    cursor = conn.cursor()
    
    if completed is None:
        cursor.execute('SELECT * FROM quest WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
    else:
        cursor.execute('SELECT * FROM quest WHERE user_id = ? AND completed = ? ORDER BY created_at DESC', (user_id, completed))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def complete_quest(quest_id: int, character_id: int = 1) -> Dict[str, Any]:
    """Mark quest as completed and reward character with enhanced rewards"""
    quest = get_quest(quest_id)
    if not quest or quest['completed']:
        return None
    
    char = get_character(character_id)
    
    # Check for combo (completed quest within last 10 minutes)
    combo_count = 0
    combo_multiplier = 1.0
    is_combo = False
    
    if char.get('last_quest_completed'):
        try:
            last_completed = datetime.fromisoformat(char['last_quest_completed'])
            time_since_last = datetime.now() - last_completed
            
            # If within 10 minutes, increment combo
            if time_since_last < timedelta(minutes=10):
                combo_count = char.get('combo_count', 0) + 1
                is_combo = True
                # Combo multiplier: +10% per combo, max 200% (10 combos)
                combo_multiplier = min(1.0 + (combo_count * 0.1), 2.0)
            else:
                combo_count = 1  # Reset combo
                combo_multiplier = 1.0
        except (ValueError, TypeError):
            combo_count = 1
    else:
        combo_count = 1
    
    # Critical hit chance: 15% base + 1% per level
    crit_chance = min(0.15 + (char['level'] * 0.01), 0.5)  # Max 50%
    is_critical = random.random() < crit_chance
    crit_multiplier = 2.5 if is_critical else 1.0
    
    # Calculate total rewards with multipliers
    base_xp = quest['xp_reward']
    base_gold = quest['gold_reward']
    
    total_multiplier = combo_multiplier * crit_multiplier
    
    final_xp = int(base_xp * total_multiplier)
    final_gold = int(base_gold * total_multiplier)
    
    # Rare item drop chance on epic quests or critical hits
    rare_drop = None
    if (quest['difficulty'] == 'epic' or is_critical) and random.random() < 0.15:
        # 15% chance for bonus gold
        bonus_gold = random.randint(20, 100)
        final_gold += bonus_gold
        rare_drop = {'type': 'gold', 'amount': bonus_gold}
    
    # Mark quest as completed
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE quest SET completed = 1, completed_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (quest_id,))
    
    # Update character combo info
    cursor.execute('''
        UPDATE character SET combo_count = ?, last_quest_completed = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (combo_count, character_id))
    
    conn.commit()
    conn.close()
    
    # Reward character
    char = add_xp_and_gold(character_id, final_xp, final_gold)
    
    return {
        'quest': get_quest(quest_id),
        'character': char,
        'rewards': {
            'xp': final_xp,
            'gold': final_gold,
            'base_xp': base_xp,
            'base_gold': base_gold
        },
        'bonus': {
            'is_critical': is_critical,
            'crit_multiplier': crit_multiplier if is_critical else None,
            'is_combo': is_combo,
            'combo_count': combo_count if is_combo else None,
            'combo_multiplier': combo_multiplier if is_combo else None,
            'total_multiplier': total_multiplier,
            'rare_drop': rare_drop
        }
    }

def delete_quest(quest_id: int) -> bool:
    """Delete a quest"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM quest WHERE id = ?', (quest_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted

# Shop operations
def get_all_items() -> List[Dict[str, Any]]:
    """Get all shop items"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM item ORDER BY price ASC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def purchase_item(character_id: int, item_id: int) -> Dict[str, Any]:
    """Purchase an item from the shop"""
    char = get_character(character_id)
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM item WHERE id = ?', (item_id,))
    item = cursor.fetchone()
    
    if not item:
        conn.close()
        return {'error': 'Item not found'}
    
    item = dict(item)
    
    if char['gold'] < item['price']:
        conn.close()
        return {'error': 'Not enough gold'}
    
    # Deduct gold
    new_gold = char['gold'] - item['price']
    update_character(character_id, gold=new_gold)
    
    # Add to inventory
    cursor.execute('''
        INSERT INTO inventory (character_id, item_id)
        VALUES (?, ?)
    ''', (character_id, item_id))
    conn.commit()
    inventory_id = cursor.lastrowid
    conn.close()
    
    return {
        'success': True,
        'item': item,
        'inventory_id': inventory_id,
        'character': get_character(character_id)
    }

def get_inventory(character_id: int) -> List[Dict[str, Any]]:
    """Get character's inventory"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT inv.id as inventory_id, inv.equipped, item.*
        FROM inventory inv
        JOIN item ON inv.item_id = item.id
        WHERE inv.character_id = ?
    ''', (character_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def equip_item(inventory_id: int, character_id: int) -> Dict[str, Any]:
    """Equip an item from inventory"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get the item
    cursor.execute('''
        SELECT inv.*, item.type, item.attack_bonus, item.defense_bonus, item.health_bonus
        FROM inventory inv
        JOIN item ON inv.item_id = item.id
        WHERE inv.id = ? AND inv.character_id = ?
    ''', (inventory_id, character_id))
    
    inv_item = cursor.fetchone()
    if not inv_item:
        conn.close()
        return {'error': 'Item not found in inventory'}
    
    inv_item = dict(inv_item)
    
    # Unequip other items of same type
    cursor.execute('''
        UPDATE inventory SET equipped = 0
        WHERE character_id = ? AND id IN (
            SELECT inv.id FROM inventory inv
            JOIN item ON inv.item_id = item.id
            WHERE item.type = ? AND inv.character_id = ?
        )
    ''', (character_id, inv_item['type'], character_id))
    
    # Equip this item
    cursor.execute('UPDATE inventory SET equipped = 1 WHERE id = ?', (inventory_id,))
    conn.commit()
    conn.close()
    
    # Recalculate character stats
    recalculate_character_stats(character_id)
    
    return {'success': True, 'character': get_character(character_id)}

def recalculate_character_stats(character_id: int):
    """Recalculate character stats based on equipped items"""
    char = get_character(character_id)
    conn = get_db()
    cursor = conn.cursor()
    
    # Get base stats (from level)
    base_attack = 10 + (char['level'] - 1) * 3
    base_defense = 5 + (char['level'] - 1) * 2
    base_max_health = 100 + (char['level'] - 1) * 10
    
    # Add equipped item bonuses
    cursor.execute('''
        SELECT SUM(item.attack_bonus) as total_attack,
               SUM(item.defense_bonus) as total_defense,
               SUM(item.health_bonus) as total_health
        FROM inventory inv
        JOIN item ON inv.item_id = item.id
        WHERE inv.character_id = ? AND inv.equipped = 1
    ''', (character_id,))
    
    bonuses = cursor.fetchone()
    conn.close()
    
    total_attack = base_attack + (bonuses['total_attack'] or 0)
    total_defense = base_defense + (bonuses['total_defense'] or 0)
    total_max_health = base_max_health + (bonuses['total_health'] or 0)
    
    update_character(
        character_id,
        attack=total_attack,
        defense=total_defense,
        max_health=total_max_health,
        health=min(char['health'], total_max_health)
    )

# Battle system
def battle_monster(character_id: int, monster_name: str, monster_level: int) -> Dict[str, Any]:
    """Simulate a battle with a monster"""
    char = get_character(character_id)
    
    # Calculate monster stats
    monster_health = 50 + monster_level * 20
    monster_attack = 5 + monster_level * 3
    monster_defense = 3 + monster_level * 2
    
    # Simple battle calculation
    char_power = char['attack'] - monster_defense
    monster_power = monster_attack - char['defense']
    
    char_power = max(char_power, 1)
    monster_power = max(monster_power, 1)
    
    # Determine winner (simplified)
    won = char_power > monster_power or (char_power == monster_power and char['level'] >= monster_level)
    
    # Calculate rewards
    if won:
        xp_gained = 30 * monster_level
        gold_gained = 20 * monster_level
        add_xp_and_gold(character_id, xp_gained, gold_gained)
    else:
        xp_gained = 5 * monster_level
        gold_gained = 0
        add_xp_and_gold(character_id, xp_gained, 0)
    
    # Log battle
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO battle (character_id, monster_name, monster_level, won, xp_gained, gold_gained)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (character_id, monster_name, monster_level, won, xp_gained, gold_gained))
    conn.commit()
    conn.close()
    
    return {
        'won': won,
        'monster': {
            'name': monster_name,
            'level': monster_level,
            'health': monster_health,
            'attack': monster_attack,
            'defense': monster_defense
        },
        'rewards': {
            'xp': xp_gained,
            'gold': gold_gained
        },
        'character': get_character(character_id)
    }

def get_battle_history(character_id: int, limit: int = 10) -> List[Dict[str, Any]]:
    """Get recent battle history"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM battle
        WHERE character_id = ?
        ORDER BY battled_at DESC
        LIMIT ?
    ''', (character_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Achievement system
def get_all_achievements() -> List[Dict[str, Any]]:
    """Get all achievements"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM achievement ORDER BY requirement_value ASC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def check_and_unlock_achievements(character_id: int) -> List[Dict[str, Any]]:
    """Check and unlock any earned achievements"""
    char = get_character(character_id)
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Get user_id from character
    cursor.execute('SELECT user_id FROM character WHERE id = ?', (character_id,))
    char_row = cursor.fetchone()
    if not char_row:
        conn.close()
        return []
    
    user_id = char_row['user_id']
    
    # Get stats (filtered by user)
    cursor.execute('SELECT COUNT(*) as count FROM quest WHERE user_id = ? AND completed = 1', (user_id,))
    quests_completed = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM battle WHERE character_id = ? AND won = 1', (character_id,))
    monsters_defeated = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM inventory WHERE character_id = ?', (character_id,))
    items_purchased = cursor.fetchone()['count']
    
    cursor.execute('SELECT SUM(gold_reward) as total FROM quest WHERE user_id = ? AND completed = 1', (user_id,))
    gold_earned = cursor.fetchone()['total'] or 0
    
    stats = {
        'quests_completed': quests_completed,
        'level': char['level'],
        'gold_earned': gold_earned,
        'monsters_defeated': monsters_defeated,
        'items_purchased': items_purchased
    }
    
    # Check unlockable achievements
    cursor.execute('SELECT * FROM achievement WHERE unlocked = 0')
    achievements = cursor.fetchall()
    
    newly_unlocked = []
    for achievement in achievements:
        ach = dict(achievement)
        req_type = ach['requirement_type']
        req_value = ach['requirement_value']
        
        if req_type in stats and stats[req_type] >= req_value:
            cursor.execute('''
                UPDATE achievement SET unlocked = 1, unlocked_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (ach['id'],))
            newly_unlocked.append(ach)
    
    conn.commit()
    conn.close()
    
    return newly_unlocked

# Statistics
def get_statistics(character_id: int) -> Dict[str, Any]:
    """Get comprehensive statistics for a character"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get user_id from character
    cursor.execute('SELECT user_id FROM character WHERE id = ?', (character_id,))
    char_row = cursor.fetchone()
    if not char_row:
        conn.close()
        return {}
    
    user_id = char_row['user_id']
    
    cursor.execute('SELECT COUNT(*) as count FROM quest WHERE user_id = ? AND completed = 1', (user_id,))
    quests_completed = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM quest WHERE user_id = ? AND completed = 0', (user_id,))
    quests_pending = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM battle WHERE character_id = ? AND won = 1', (character_id,))
    battles_won = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM battle WHERE character_id = ? AND won = 0', (character_id,))
    battles_lost = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM achievement WHERE unlocked = 1')
    achievements_unlocked = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM achievement')
    total_achievements = cursor.fetchone()['count']
    
    cursor.execute('SELECT SUM(gold_reward) as total FROM quest WHERE user_id = ? AND completed = 1', (user_id,))
    total_gold_earned = cursor.fetchone()['total'] or 0
    
    cursor.execute('SELECT SUM(xp_reward) as total FROM quest WHERE user_id = ? AND completed = 1', (user_id,))
    total_xp_earned = cursor.fetchone()['total'] or 0
    
    conn.close()
    
    return {
        'quests_completed': quests_completed,
        'quests_pending': quests_pending,
        'battles_won': battles_won,
        'battles_lost': battles_lost,
        'achievements_unlocked': achievements_unlocked,
        'total_achievements': total_achievements,
        'total_gold_earned': total_gold_earned,
        'total_xp_earned': total_xp_earned
    }

# Task Templates
def get_all_templates(category: Optional[str] = None, popular_only: bool = False) -> List[Dict[str, Any]]:
    """Get all task templates, optionally filtered"""
    conn = get_db()
    cursor = conn.cursor()
    
    if category:
        cursor.execute('SELECT * FROM task_template WHERE category = ? ORDER BY popular DESC, title ASC', (category,))
    elif popular_only:
        cursor.execute('SELECT * FROM task_template WHERE popular = 1 ORDER BY title ASC')
    else:
        cursor.execute('SELECT * FROM task_template ORDER BY category ASC, popular DESC, title ASC')
    
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_template_categories() -> List[str]:
    """Get all unique template categories"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT category FROM task_template ORDER BY category ASC')
    rows = cursor.fetchall()
    conn.close()
    return [row['category'] for row in rows]

def create_quest_from_template(template_id: int, user_id: int) -> Dict[str, Any]:
    """Create a quest from a template"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM task_template WHERE id = ?', (template_id,))
    template = cursor.fetchone()
    conn.close()
    
    if not template:
        return None
    
    template = dict(template)
    return create_quest(
        user_id=user_id,
        title=template['title'],
        description=template['description'] or '',
        difficulty=template['difficulty']
    )

# User Authentication
def create_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """Create a new user with hashed password"""
    from werkzeug.security import generate_password_hash
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        password_hash = generate_password_hash(password)
        cursor.execute('''
            INSERT INTO user (username, password_hash)
            VALUES (?, ?)
        ''', (username, password_hash))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        return get_user(user_id)
    except sqlite3.IntegrityError:
        conn.close()
        return None  # Username already exists

def get_user(user_id: int) -> Optional[Dict[str, Any]]:
    """Get user by ID"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, created_at FROM user WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    """Get user by username (including password hash for auth)"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user WHERE username = ?', (username,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def verify_password(username: str, password: str) -> Optional[int]:
    """Verify password and return user_id if correct"""
    from werkzeug.security import check_password_hash
    
    user = get_user_by_username(username)
    if not user:
        return None
    
    if check_password_hash(user['password_hash'], password):
        return user['id']
    return None

def get_character_by_user_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Get character for a specific user"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM character WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        char = dict(row)
        char['xp_to_next_level'] = calculate_xp_for_next_level(char['level'])
        return char
    return None

def create_character_for_user(user_id: int, name: str) -> Dict[str, Any]:
    """Create a character for a user"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO character (user_id, name) VALUES (?, ?)
    ''', (user_id, name))
    
    conn.commit()
    conn.close()
    
    return get_character_by_user_id(user_id)
