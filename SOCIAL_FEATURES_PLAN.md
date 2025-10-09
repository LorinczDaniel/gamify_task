# 🌐 Social Features Implementation Plan

**Status**: In Progress  
**Expected Completion**: This session

---

## ✅ What's Been Added So Far:

### 1. Database Updates
- ✅ Added `public_profile` column (BOOLEAN, default TRUE)
- ✅ Added `total_quests_completed` column (INTEGER)
- ✅ Added `total_monsters_defeated` column (INTEGER)
- ✅ Created `database_social.py` with social functions

### 2. Social Functions Created
- ✅ `get_leaderboard()` - Get top players
- ✅ `get_public_profile()` - Fetch public profile by user_id
- ✅ `get_public_profile_by_username()` - Fetch by username
- ✅ `toggle_public_profile()` - Privacy toggle
- ✅ `increment_quest_counter()` - Track total quests
- ✅ `increment_monster_counter()` - Track monsters defeated
- ✅ `get_user_rank()` - Get player's rank

---

## 🔨 Still To Build:

### 3. Backend Routes (app.py)
- [ ] `/api/leaderboard` - GET leaderboard data
- [ ] `/profile/<username>` - Public profile page
- [ ] `/api/profile/toggle` - Toggle profile visibility
- [ ] `/api/profile/stats` - Get user stats for sharing

### 4. Frontend - Leaderboard Tab
- [ ] Add "Leaderboard" to navigation tabs
- [ ] Create leaderboard UI with:
  - Daily/Weekly/All-Time tabs
  - Rank, Avatar, Name, Level, Quests, Monsters
  - Highlight current user
  - Responsive design

### 5. Frontend - Public Profile Page
- [ ] Create `/templates/profile.html`
- [ ] Show character info, stats, achievements
- [ ] "Challenge this hero" button (future feature)
- [ ] Social share buttons

### 6. Social Share Buttons
- [ ] Tweet achievement unlocks
- [ ] Share to Discord
- [ ] Copy profile link
- [ ] Share quest completion milestones

### 7. Privacy Settings
- [ ] Add toggle in customize/settings page
- [ ] "Make my profile public/private"
- [ ] Update UI to reflect setting

---

## 🎯 User Flows:

### Leaderboard Flow:
```
User clicks "Leaderboard" tab
→ Sees top 100 players
→ Can filter by Daily/Weekly/All-Time
→ Sees own rank highlighted
→ Can click any player to view profile
```

### Profile Sharing Flow:
```
User completes achievement
→ "Share" button appears
→ Clicks to tweet/discord
→ Generates message: "Just unlocked [Achievement] in Quest Master! 🎮"
→ Includes link to public profile
```

### Privacy Flow:
```
User goes to Settings
→ Toggles "Public Profile" OFF
→ Profile hidden from leaderboards
→ Profile page shows "This profile is private"
```

---

## 📊 Leaderboard Design:

```
╔═══════════════════════════════════════════╗
║        🏆 LEADERBOARD                     ║
║  [All Time] [Weekly] [Daily]              ║
╠═══════════════════════════════════════════╣
║ Rank | Hero        | Lvl | Quests | Mons  ║
║  1   | 👤 DragonSlayer | 25  | 500 | 150  ║
║  2   | 🧙 Gandalf  | 23  | 480 | 140       ║
║  3   | 🥷 Ninja    | 22  | 450 | 130       ║
║  ... |             |     |     |           ║
║  42  | 🤴 YOU      | 15  | 150 | 50  ← YOU ║
║  ... |             |     |     |           ║
╚═══════════════════════════════════════════╝
```

---

## 🎨 Public Profile Design:

```
╔═══════════════════════════════════════════╗
║      👤 Hero's Profile                    ║
║                                           ║
║       [Large Avatar]                      ║
║       DragonSlayer                        ║
║       Level 25 Warrior                    ║
║                                           ║
║  ⚔️ 75  🛡️ 40  💰 5000                   ║
║                                           ║
║  📊 Stats                                 ║
║  • 500 Quests Completed                   ║
║  • 150 Monsters Defeated                  ║
║  • 25 Achievements Unlocked               ║
║  • Member since: Jan 2025                 ║
║                                           ║
║  📜 Bio:                                  ║
║  "Slaying tasks by day, monsters by      ║
║   night. Productivity warrior!"          ║
║                                           ║
║  [Share Profile] [Challenge]              ║
╚═══════════════════════════════════════════╝
```

---

## 🔗 Share Messages:

### Achievement Unlock:
```
"Just unlocked [Achievement Name] in Quest Master! 🎮🏆
Level [X] [Class] | [Y] quests completed

Join me: https://rpgtask.up.railway.app
#productivity #gamification"
```

### Level Up:
```
"Level UP! Just hit Level [X] in Quest Master! ⚔️✨
[Y] quests conquered, [Z] monsters defeated

Turn your tasks into quests: https://rpgtask.up.railway.app"
```

### Quest Milestone:
```
"100 quests completed in Quest Master! 🎯🔥
Productivity has never been this fun!

Start your adventure: https://rpgtask.up.railway.app"
```

---

## 🔒 Privacy Options:

Users can toggle:
- ✅ **Public Profile** (ON/OFF)
  - ON: Appears in leaderboards, profile viewable
  - OFF: Hidden from leaderboards, profile page shows "private"

Future options:
- Show/hide specific stats
- Friends-only visibility
- Anonymous leaderboard entry

---

## 📈 Analytics Tracking:

Track these events:
- `profile_viewed` - When someone views a profile
- `leaderboard_viewed` - When leaderboard is opened
- `achievement_shared` - When achievement is shared
- `profile_link_copied` - When profile link is copied
- `challenge_clicked` - When challenge button clicked (future)

---

## 🚀 Implementation Order:

1. ✅ Database structure
2. ✅ Social functions
3. Next: Backend routes
4. Next: Leaderboard UI
5. Next: Public profile page
6. Next: Share buttons
7. Next: Privacy settings
8. Final: Testing & deployment

---

## 💡 Future Enhancements:

- **Friends System**: Add/follow other players
- **Direct Challenges**: Challenge friends to quest races
- **Team Leaderboards**: Guild/team rankings
- **Social Feed**: See friends' recent achievements
- **Badges/Flair**: Customizable profile badges
- **Profile Comments**: Let users leave messages
- **Compare Stats**: Side-by-side stat comparison

---

**This will be a game-changer for virality and user engagement!** 🎉

