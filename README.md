# Quest Master - Gamified Task Manager RPG

Transform your daily tasks into an epic adventure! Quest Master is a gamified task management app where completing real-life tasks helps you level up your character, earn gold, purchase equipment, and battle monsters.

## Features

### Core Mechanics
- 🎮 **Character System**: Create and level up your hero
- ⚔️ **Task Quests**: Turn your to-dos into rewarding quests
- 💰 **Economy**: Earn gold by completing tasks
- 🛡️ **Equipment Shop**: Buy weapons, armor, and items with your earned gold
- 🐉 **Monster Battles**: Use your stats to defeat creatures
- 🏆 **Achievements**: Unlock achievements for various accomplishments
- 📊 **Stats Tracking**: Monitor your productivity and character growth

### Upcoming Features
- Daily challenges and streak bonuses
- Multiple character classes
- Boss battles
- Party system (multiplayer)
- Pet companions
- Skill trees

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## How to Play

1. **Create Your Character**: Choose a name and start your adventure
2. **Create Quests**: Add your real-life tasks as quests with difficulty levels
3. **Complete Quests**: Mark tasks as complete to earn XP and gold
4. **Level Up**: Gain levels to increase your stats
5. **Visit the Shop**: Spend gold on equipment to boost your character
6. **Battle Monsters**: Test your strength against various creatures
7. **Unlock Achievements**: Complete special goals to earn badges

## Tech Stack

- **Backend**: Python + Flask
- **Frontend**: Vanilla JavaScript + Modern CSS
- **Database**: SQLite
- **Styling**: Custom RPG-themed CSS with animations

## Project Structure

```
quest-master/
├── app.py              # Flask backend
├── database.py         # Database models and operations
├── static/
│   ├── css/
│   │   └── style.css   # Main stylesheet
│   ├── js/
│   │   └── app.js      # Frontend JavaScript
│   └── images/         # Game assets
├── templates/
│   └── index.html      # Main application page
└── requirements.txt    # Python dependencies
```

## Contributing

This is a personal fun project, but feel free to fork and customize it to your liking!

## License

MIT License - Feel free to use and modify as you wish!

