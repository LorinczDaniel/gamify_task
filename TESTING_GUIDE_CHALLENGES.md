# Testing Guide - Daily Challenges & Weekly Summary

## Quick Start

1. **Start the application**:
   ```bash
   python app.py
   ```

2. **Navigate to**: http://localhost:5000

3. **Login** with existing account or create a new one

## Testing Daily Challenges

### Test 1: View Daily Challenges
**Expected Result**: See 3 challenge cards displayed below the character panel

**What to Look For**:
- Each challenge shows an icon, description, progress bar, and rewards
- Progress bar shows "0/X" initially
- All challenges show "In Progress" button (disabled)

### Test 2: Complete a Quest Challenge
**Steps**:
1. Look for a challenge like "Complete 3 quests today"
2. Go to the Quests tab
3. Create and complete 3 quests

**Expected Result**:
- After each quest completion, challenge progress bar updates (1/3, 2/3, 3/3)
- When complete, button changes to "🎁 Claim Rewards"
- Challenge card gets a green border

### Test 3: Claim Challenge Rewards
**Steps**:
1. Complete a challenge (see Test 2)
2. Click the "🎁 Claim Rewards" button

**Expected Result**:
- Notification appears: "Challenge completed! +X XP, +Y Gold"
- Character XP and Gold increase
- Challenge card shows "✓ Claimed"
- Card becomes semi-transparent
- Button is no longer clickable

### Test 4: Battle Challenge
**Steps**:
1. Look for "Defeat 2 monsters today" challenge
2. Go to Battle tab
3. Battle and win against 2 monsters

**Expected Result**:
- Progress updates after each victory (1/2, 2/2)
- XP and Gold earned from battles also count toward XP/Gold challenges
- Can claim rewards when complete

### Test 5: XP Challenge
**Steps**:
1. Look for "Earn 150 XP today" challenge
2. Complete quests or battles to earn XP

**Expected Result**:
- Progress bar updates with total XP earned
- Completing quests contributes to this challenge
- Winning battles contributes to this challenge

### Test 6: Combo Challenge
**Steps**:
1. Look for "Complete a 3x combo" challenge
2. Complete 3 quests within 10 minutes of each other

**Expected Result**:
- Challenge completes when you achieve a 3x combo
- This is the rarest challenge to complete

### Test 7: Hard Quest Challenge
**Steps**:
1. Look for "Complete 1 hard quest" challenge
2. Create a quest with "Hard" difficulty
3. Complete it

**Expected Result**:
- Challenge completes immediately
- Can claim rewards

### Test 8: Next Day Challenges
**Steps**:
1. Complete and claim all today's challenges
2. Wait until tomorrow OR change your system date to tomorrow
3. Refresh the page

**Expected Result**:
- 3 new challenges appear
- Different mix of challenge types
- Previous day's challenges are gone

## Testing Weekly Summary

### Test 9: View Weekly Summary
**Steps**:
1. Click the "📊 Weekly Report" button (next to Daily Challenges title)

**Expected Result**:
- Modal opens with weekly statistics
- Shows current week dates (Monday - Sunday)
- Displays 4 stat cards: Quests Completed, XP Earned, Gold Earned, Monsters Defeated
- Shows "Active Days" count
- Displays motivational message

### Test 10: Week Comparison
**Steps**:
1. Complete some quests/battles this week
2. Open Weekly Report

**Expected Result**:
- If you have data from last week, comparison arrows appear:
  - Green ↑ +X% for improvements
  - Red ↓ -X% for decreases
  - Gray — for no change
- If no last week data, shows baseline stats

### Test 11: Active Days Tracking
**Steps**:
1. Complete quests on different days this week
2. Check Weekly Report

**Expected Result**:
- "Active Days" count shows how many days you completed quests
- Maximum is 7/7 (every day of the week)

### Test 12: Most Productive Day
**Steps**:
1. Complete different amounts of quests on different days
2. Check Weekly Report

**Expected Result**:
- Shows the date when you completed the most quests
- Only appears if you've completed quests this week

### Test 13: Motivational Messages
**Steps**:
Complete different amounts of quests and check messages:
- 0 quests: "💡 New week, new opportunities! Start your first quest!"
- 1-4 quests: "🌟 Good start! Every quest counts!"
- 5-9 quests: "💪 Nice progress! You're doing great!"
- 10-19 quests: "⭐ Great work! Keep up the momentum!"
- 20+ quests: "🔥 Amazing week! You're on fire!"

**Expected Result**:
- Message changes based on performance
- Provides appropriate encouragement

### Test 14: Close Weekly Summary
**Steps**:
1. Open Weekly Report
2. Click the "✕" button in top right

**Expected Result**:
- Modal closes smoothly
- Returns to main app view

## Visual Testing

### Test 15: Challenge Card States
**Visual Checks**:
- **In Progress**: Gray background, progress bar partially filled
- **Completed**: Green border, full progress bar
- **Claimed**: Faded appearance, checkmark shown

### Test 16: Progress Bar Animation
**Steps**:
1. Watch challenge progress bars as you complete actions

**Expected Result**:
- Progress bar fills smoothly with animation
- Numbers update (e.g., "2/3")
- Percentage shown in the bar

### Test 17: Hover Effects
**Steps**:
1. Hover over challenge cards
2. Hover over stat cards in weekly summary

**Expected Result**:
- Cards lift slightly (translateY)
- Border color changes to orange/gold
- Smooth transition animation

### Test 18: Mobile Responsiveness
**Steps**:
1. Resize browser window to mobile size (< 768px)
2. Check challenges panel
3. Check weekly summary modal

**Expected Result**:
- Challenge cards stack vertically
- Text remains readable
- Buttons remain clickable
- Modal scrolls if needed

## API Testing (Optional - For Developers)

### Test 19: API Endpoints
```bash
# Get daily challenges (requires authentication)
curl http://localhost:5000/api/challenges/daily

# Get weekly summary
curl http://localhost:5000/api/stats/weekly

# Claim challenge (POST with challenge ID)
curl -X POST http://localhost:5000/api/challenges/daily/1/claim
```

## Common Issues & Solutions

### Issue 1: Challenges Not Loading
**Solution**: 
- Check browser console for errors
- Verify database was initialized: `python -c "import database; database.init_db()"`
- Refresh the page

### Issue 2: Progress Not Updating
**Solution**:
- Complete an action (quest or battle)
- Refresh the page if progress doesn't auto-update
- Check browser console for API errors

### Issue 3: Can't Claim Rewards
**Solution**:
- Ensure challenge progress shows 100%
- Check that you're logged in
- Verify character exists in database

### Issue 4: Weekly Summary Empty
**Solution**:
- Complete at least one quest first
- Weekly summary only shows data for completed actions
- Previous week comparison only works if you had activity last week

## Database Verification

### Verify Tables Exist
```python
import sqlite3
conn = sqlite3.connect('quest_master.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%challenge%'")
print(cursor.fetchall())
# Should show: [('daily_challenge',), ('user_daily_challenge',)]
```

### View Today's Challenges
```python
import database
challenges = database.generate_daily_challenges()
print(challenges)
```

### Check User Progress
```python
import database
user_id = 1  # Your user ID
progress = database.get_daily_challenges(user_id)
print(progress)
```

## Success Criteria

✅ All 3 daily challenges display correctly  
✅ Challenge progress updates in real-time  
✅ Rewards can be claimed successfully  
✅ Character XP/Gold increases after claiming  
✅ Weekly summary shows accurate statistics  
✅ Week-over-week comparison displays correctly  
✅ UI is responsive and visually appealing  
✅ No console errors  
✅ Smooth animations and transitions  
✅ Motivational messages are appropriate  

## Performance Checklist

- [ ] Page loads in < 2 seconds
- [ ] Challenge updates feel instant
- [ ] Modal opens/closes smoothly
- [ ] No lag when claiming rewards
- [ ] Progress bars animate smoothly

## Browser Compatibility

Test in:
- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari (if available)
- [ ] Mobile browsers

---

**Ready for Production**: If all tests pass, the feature is ready to deploy! 🚀

