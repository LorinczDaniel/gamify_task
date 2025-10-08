# Quick Start Guide 🚀

## Starting the App

```bash
python app.py
```

Then open your browser to: **http://localhost:5000**

## Try the New Features!

### 1. Quick-Add a Task (10 seconds)
- Go to the **Quests** tab
- See the "⚡ Quick Add Common Tasks" section at the top
- Click **"Make bed"** or any other template
- **BOOM!** Quest is added instantly

### 2. Complete a Quest and See the Magic ✨
- Click the **"✓ Complete"** button on any quest
- Watch the **animated reward popup** appear
- See your XP and gold with multipliers
- **15% chance** you'll see "💥 CRITICAL HIT! 💥" with confetti!

### 3. Build a Combo 🔥
- Complete another quest **within 10 minutes**
- See the **combo badge** appear in the top-right
- Each combo gives you **+10% more rewards**
- Try to build a streak!

### 4. Level Up 🎊
- Complete enough quests to gain a level
- Experience the **full-screen celebration**
- Watch confetti rain down
- See your new stats with staggered animations

## What Makes Tasks Fun Now?

### Before:
"Do the dishes" → Click complete → "+20 XP" notification → Done

### After:
"Do the dishes" → Click complete → **Spinning reward popup** → "💥 CRITICAL HIT! 💥 2.5x Multiplier!" → **+50 XP +25 Gold** → **Confetti explosion** → 🔥 "3X COMBO!" badge appears → **You feel awesome!**

## Tips for Maximum Fun

1. **Use Quick-Add**: Don't waste time typing - just click templates
2. **Chase Combos**: Complete tasks in bursts for multipliers
3. **Hope for Crits**: 15% base chance + your level = excitement!
4. **Complete Epic Quests**: Higher difficulty = better rewards + bonus drops
5. **Level Up Often**: The celebration is worth it!

## Technical Notes

- **Combo Window**: 10 minutes between quest completions
- **Critical Chance**: 15% base + 1% per level (max 50% at level 35)
- **Critical Multiplier**: 2.5x on both XP and gold
- **Combo Multiplier**: Stacks with critical! (Can get 5x rewards!)
- **Rare Drops**: 15% chance on epic quests or critical hits

## Database Migration

The first time you run the app after this update, it will automatically:
- Add `combo_count` and `last_quest_completed` columns to your character
- Create the `task_template` table
- Populate 28 pre-made task templates
- No data loss - all your existing quests and progress are safe!

## Troubleshooting

**Templates not showing?**
- Refresh the page
- Check browser console for errors

**Animations not working?**
- Clear browser cache (Ctrl+Shift+R)
- Make sure JavaScript is enabled

**Server won't start?**
- Check if port 5000 is available
- Ensure Flask and dependencies are installed: `pip install -r requirements.txt`

---

**Now go make those boring tasks fun!** 🎮✨

