from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import database as db

app = Flask(__name__)
CORS(app)

# Initialize database on startup
db.init_db()

@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')

# Character endpoints
@app.route('/api/character', methods=['GET'])
def get_character():
    """Get the main character"""
    char = db.get_or_create_character()
    return jsonify(char)

@app.route('/api/character', methods=['POST'])
def create_character():
    """Create or reset character"""
    data = request.json
    name = data.get('name', 'Hero')
    char = db.create_character(name)
    return jsonify(char)

@app.route('/api/character/stats', methods=['GET'])
def get_character_with_stats():
    """Get character with full statistics"""
    char = db.get_or_create_character()
    stats = db.get_statistics(char['id'])
    inventory = db.get_inventory(char['id'])
    
    return jsonify({
        'character': char,
        'stats': stats,
        'inventory': inventory
    })

# Quest endpoints
@app.route('/api/quests', methods=['GET'])
def get_quests():
    """Get all quests"""
    completed = request.args.get('completed')
    if completed is not None:
        completed = completed.lower() == 'true'
    
    quests = db.get_all_quests(completed)
    return jsonify(quests)

@app.route('/api/quests', methods=['POST'])
def create_quest():
    """Create a new quest"""
    data = request.json
    title = data.get('title')
    description = data.get('description', '')
    difficulty = data.get('difficulty', 'medium')
    
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    
    quest = db.create_quest(title, description, difficulty)
    return jsonify(quest), 201

@app.route('/api/quests/<int:quest_id>/complete', methods=['POST'])
def complete_quest(quest_id):
    """Complete a quest"""
    result = db.complete_quest(quest_id)
    
    if not result:
        return jsonify({'error': 'Quest not found or already completed'}), 404
    
    # Check for newly unlocked achievements
    newly_unlocked = db.check_and_unlock_achievements(result['character']['id'])
    result['newly_unlocked_achievements'] = newly_unlocked
    
    return jsonify(result)

@app.route('/api/quests/<int:quest_id>', methods=['DELETE'])
def delete_quest(quest_id):
    """Delete a quest"""
    success = db.delete_quest(quest_id)
    if success:
        return jsonify({'success': True})
    return jsonify({'error': 'Quest not found'}), 404

# Shop endpoints
@app.route('/api/shop/items', methods=['GET'])
def get_shop_items():
    """Get all shop items"""
    items = db.get_all_items()
    return jsonify(items)

@app.route('/api/shop/purchase', methods=['POST'])
def purchase_item():
    """Purchase an item"""
    data = request.json
    item_id = data.get('item_id')
    
    char = db.get_or_create_character()
    result = db.purchase_item(char['id'], item_id)
    
    if 'error' in result:
        return jsonify(result), 400
    
    # Check for achievements
    newly_unlocked = db.check_and_unlock_achievements(char['id'])
    result['newly_unlocked_achievements'] = newly_unlocked
    
    return jsonify(result)

# Inventory endpoints
@app.route('/api/inventory', methods=['GET'])
def get_inventory():
    """Get character inventory"""
    char = db.get_or_create_character()
    inventory = db.get_inventory(char['id'])
    return jsonify(inventory)

@app.route('/api/inventory/<int:inventory_id>/equip', methods=['POST'])
def equip_item(inventory_id):
    """Equip an item"""
    char = db.get_or_create_character()
    result = db.equip_item(inventory_id, char['id'])
    
    if 'error' in result:
        return jsonify(result), 400
    
    return jsonify(result)

# Battle endpoints
@app.route('/api/battle', methods=['POST'])
def battle_monster():
    """Battle a monster"""
    data = request.json
    monster_name = data.get('monster_name', 'Goblin')
    monster_level = data.get('monster_level', 1)
    
    char = db.get_or_create_character()
    result = db.battle_monster(char['id'], monster_name, monster_level)
    
    # Check for achievements
    newly_unlocked = db.check_and_unlock_achievements(char['id'])
    result['newly_unlocked_achievements'] = newly_unlocked
    
    return jsonify(result)

@app.route('/api/battle/history', methods=['GET'])
def get_battle_history():
    """Get battle history"""
    char = db.get_or_create_character()
    limit = request.args.get('limit', 10, type=int)
    history = db.get_battle_history(char['id'], limit)
    return jsonify(history)

# Achievement endpoints
@app.route('/api/achievements', methods=['GET'])
def get_achievements():
    """Get all achievements"""
    achievements = db.get_all_achievements()
    return jsonify(achievements)

@app.route('/api/achievements/check', methods=['POST'])
def check_achievements():
    """Manually check for unlocked achievements"""
    char = db.get_or_create_character()
    newly_unlocked = db.check_and_unlock_achievements(char['id'])
    return jsonify({
        'newly_unlocked': newly_unlocked,
        'all_achievements': db.get_all_achievements()
    })

# Statistics endpoint
@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get comprehensive statistics"""
    char = db.get_or_create_character()
    stats = db.get_statistics(char['id'])
    return jsonify(stats)

if __name__ == '__main__':
    print("🎮 Quest Master RPG Server Starting...")
    print("📍 Navigate to http://localhost:5000 to play!")
    app.run(debug=True, host='0.0.0.0', port=5000)

