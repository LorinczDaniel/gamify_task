from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_cors import CORS
from functools import wraps
import database as db
import secrets
import os

app = Flask(__name__)
# Use environment variable in production, generate random for local dev
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
CORS(app)

# Initialize database on startup
db.init_db()

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Not authenticated'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Serve the main application page (requires login)"""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('index.html')

@app.route('/login')
def login_page():
    """Serve the login page"""
    return render_template('login.html')

@app.route('/register')
def register_page():
    """Serve the register page"""
    return render_template('register.html')

# Auth API endpoints
@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '')
    character_name = data.get('character_name', username)
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    if len(username) < 3:
        return jsonify({'error': 'Username must be at least 3 characters'}), 400
    
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    # Create user
    user = db.create_user(username, password)
    if not user:
        return jsonify({'error': 'Username already exists'}), 400
    
    # Create character for user
    character = db.create_character_for_user(user['id'], character_name)
    
    # Log them in
    session['user_id'] = user['id']
    session['username'] = user['username']
    
    return jsonify({'success': True, 'user': user, 'character': character}), 201

@app.route('/api/login', methods=['POST'])
def login():
    """Login user"""
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    user_id = db.verify_password(username, password)
    if not user_id:
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # Set session
    session['user_id'] = user_id
    session['username'] = username
    
    return jsonify({'success': True, 'message': 'Logged in successfully'})

@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

# Character endpoints
@app.route('/api/character', methods=['GET'])
@login_required
def get_character():
    """Get the logged-in user's character"""
    user_id = session['user_id']
    char = db.get_character_by_user_id(user_id)
    
    if not char:
        # Create default character if doesn't exist
        char = db.create_character_for_user(user_id, session.get('username', 'Hero'))
    
    return jsonify(char)

@app.route('/api/character/stats', methods=['GET'])
@login_required
def get_character_with_stats():
    """Get character with full statistics"""
    user_id = session['user_id']
    char = db.get_character_by_user_id(user_id)
    
    if not char:
        char = db.create_character_for_user(user_id, session.get('username', 'Hero'))
    
    stats = db.get_statistics(char['id'])
    inventory = db.get_inventory(char['id'])
    
    return jsonify({
        'character': char,
        'stats': stats,
        'inventory': inventory
    })

# Quest endpoints
@app.route('/api/quests', methods=['GET'])
@login_required
def get_quests():
    """Get all quests for logged-in user"""
    user_id = session['user_id']
    completed = request.args.get('completed')
    if completed is not None:
        completed = completed.lower() == 'true'
    
    quests = db.get_all_quests(user_id, completed)
    return jsonify(quests)

@app.route('/api/quests', methods=['POST'])
@login_required
def create_quest():
    """Create a new quest"""
    user_id = session['user_id']
    data = request.json
    title = data.get('title')
    description = data.get('description', '')
    difficulty = data.get('difficulty', 'medium')
    
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    
    quest = db.create_quest(user_id, title, description, difficulty)
    return jsonify(quest), 201

@app.route('/api/quests/<int:quest_id>/complete', methods=['POST'])
@login_required
def complete_quest(quest_id):
    """Complete a quest"""
    user_id = session['user_id']
    char = db.get_character_by_user_id(user_id)
    
    if not char:
        return jsonify({'error': 'Character not found'}), 404
    
    result = db.complete_quest(quest_id, char['id'])
    
    if not result:
        return jsonify({'error': 'Quest not found or already completed'}), 404
    
    # Check for newly unlocked achievements
    newly_unlocked = db.check_and_unlock_achievements(char['id'])
    result['newly_unlocked_achievements'] = newly_unlocked
    
    return jsonify(result)

@app.route('/api/quests/<int:quest_id>', methods=['DELETE'])
@login_required
def delete_quest(quest_id):
    """Delete a quest"""
    success = db.delete_quest(quest_id)
    if success:
        return jsonify({'success': True})
    return jsonify({'error': 'Quest not found'}), 404

# Shop endpoints
@app.route('/api/shop/items', methods=['GET'])
@login_required
def get_shop_items():
    """Get all shop items"""
    items = db.get_all_items()
    return jsonify(items)

@app.route('/api/shop/purchase', methods=['POST'])
@login_required
def purchase_item():
    """Purchase an item"""
    user_id = session['user_id']
    char = db.get_character_by_user_id(user_id)
    
    if not char:
        return jsonify({'error': 'Character not found'}), 404
    
    data = request.json
    item_id = data.get('item_id')
    
    result = db.purchase_item(char['id'], item_id)
    
    if 'error' in result:
        return jsonify(result), 400
    
    # Check for achievements
    newly_unlocked = db.check_and_unlock_achievements(char['id'])
    result['newly_unlocked_achievements'] = newly_unlocked
    
    return jsonify(result)

# Inventory endpoints
@app.route('/api/inventory', methods=['GET'])
@login_required
def get_inventory():
    """Get character inventory"""
    user_id = session['user_id']
    char = db.get_character_by_user_id(user_id)
    
    if not char:
        return jsonify({'error': 'Character not found'}), 404
    
    inventory = db.get_inventory(char['id'])
    return jsonify(inventory)

@app.route('/api/inventory/<int:inventory_id>/equip', methods=['POST'])
@login_required
def equip_item(inventory_id):
    """Equip an item"""
    user_id = session['user_id']
    char = db.get_character_by_user_id(user_id)
    
    if not char:
        return jsonify({'error': 'Character not found'}), 404
    
    result = db.equip_item(inventory_id, char['id'])
    
    if 'error' in result:
        return jsonify(result), 400
    
    return jsonify(result)

# Battle endpoints
@app.route('/api/battle', methods=['POST'])
@login_required
def battle_monster():
    """Battle a monster"""
    user_id = session['user_id']
    char = db.get_character_by_user_id(user_id)
    
    if not char:
        return jsonify({'error': 'Character not found'}), 404
    
    data = request.json
    monster_name = data.get('monster_name', 'Goblin')
    monster_level = data.get('monster_level', 1)
    
    result = db.battle_monster(char['id'], monster_name, monster_level)
    
    # Check for achievements
    newly_unlocked = db.check_and_unlock_achievements(char['id'])
    result['newly_unlocked_achievements'] = newly_unlocked
    
    return jsonify(result)

@app.route('/api/battle/history', methods=['GET'])
@login_required
def get_battle_history():
    """Get battle history"""
    user_id = session['user_id']
    char = db.get_character_by_user_id(user_id)
    
    if not char:
        return jsonify([])
    
    limit = request.args.get('limit', 10, type=int)
    history = db.get_battle_history(char['id'], limit)
    return jsonify(history)

# Achievement endpoints
@app.route('/api/achievements', methods=['GET'])
@login_required
def get_achievements():
    """Get all achievements"""
    achievements = db.get_all_achievements()
    return jsonify(achievements)

@app.route('/api/achievements/check', methods=['POST'])
@login_required
def check_achievements():
    """Manually check for unlocked achievements"""
    user_id = session['user_id']
    char = db.get_character_by_user_id(user_id)
    
    if not char:
        return jsonify({'error': 'Character not found'}), 404
    
    newly_unlocked = db.check_and_unlock_achievements(char['id'])
    return jsonify({
        'newly_unlocked': newly_unlocked,
        'all_achievements': db.get_all_achievements()
    })

# Template endpoints
@app.route('/api/templates', methods=['GET'])
@login_required
def get_templates():
    """Get all task templates"""
    category = request.args.get('category')
    popular_only = request.args.get('popular', 'false').lower() == 'true'
    
    templates = db.get_all_templates(category, popular_only)
    return jsonify(templates)

@app.route('/api/templates/categories', methods=['GET'])
@login_required
def get_template_categories():
    """Get all template categories"""
    categories = db.get_template_categories()
    return jsonify(categories)

@app.route('/api/templates/<int:template_id>/create', methods=['POST'])
@login_required
def create_from_template(template_id):
    """Create a quest from a template"""
    user_id = session['user_id']
    quest = db.create_quest_from_template(template_id, user_id)
    
    if not quest:
        return jsonify({'error': 'Template not found'}), 404
    
    return jsonify(quest), 201

# Statistics endpoint
@app.route('/api/stats', methods=['GET'])
@login_required
def get_stats():
    """Get comprehensive statistics"""
    user_id = session['user_id']
    char = db.get_character_by_user_id(user_id)
    
    if not char:
        return jsonify({'error': 'Character not found'}), 404
    
    stats = db.get_statistics(char['id'])
    return jsonify(stats)

if __name__ == '__main__':
    print("🎮 Quest Master RPG Server Starting...")
    print("📍 Navigate to http://localhost:5000 to play!")
    app.run(debug=True, host='0.0.0.0', port=5000)

