/**
 * Leaderboard and Social Features JavaScript
 */

let currentTimeframe = 'all';

// Avatar mapping
const avatarMapping = {
    1: '👤', 2: '🧙', 3: '🥷', 4: '🦸',
    5: '🤴', 6: '👸', 7: '🧝', 8: '🧛'
};

// Load leaderboard
async function loadLeaderboard(timeframe = 'all') {
    currentTimeframe = timeframe;
    
    try {
        const response = await fetch(`/api/leaderboard?timeframe=${timeframe}&limit=100`);
        if (!response.ok) throw new Error('Failed to load leaderboard');
        
        const leaderboard = await response.json();
        displayLeaderboard(leaderboard);
        
        // Track analytics
        if (window.trackEvent) {
            window.trackEvent('leaderboard_viewed', {
                timeframe: timeframe
            });
        }
    } catch (error) {
        console.error('Error loading leaderboard:', error);
        document.getElementById('leaderboard-body').innerHTML = `
            <tr>
                <td colspan="6" style="text-align: center; color: var(--danger-color);">
                    Failed to load leaderboard. Please try again.
                </td>
            </tr>
        `;
    }
}

// Display leaderboard
function displayLeaderboard(leaderboard) {
    const tbody = document.getElementById('leaderboard-body');
    
    if (!leaderboard || leaderboard.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" style="text-align: center; color: var(--text-secondary);">
                    No players yet. Be the first hero!
                </td>
            </tr>
        `;
        return;
    }
    
    // Get current user's data
    const currentCharacter = window.currentCharacter || {};
    
    tbody.innerHTML = leaderboard.map(player => {
        const isCurrentUser = player.username === (window.currentUsername || '');
        const rankBadgeClass = player.rank === 1 ? 'gold' : 
                               player.rank === 2 ? 'silver' : 
                               player.rank === 3 ? 'bronze' : 'normal';
        
        const avatar = avatarMapping[player.avatar_id] || '👤';
        const classIcon = player.character_class === 'Warrior' ? '⚔️' :
                         player.character_class === 'Mage' ? '🔮' :
                         player.character_class === 'Rogue' ? '🗡️' :
                         player.character_class === 'Ranger' ? '🏹' : '⚔️';
        
        return `
            <tr class="${isCurrentUser ? 'current-user' : ''}">
                <td style="text-align: center;">
                    <div class="rank-badge ${rankBadgeClass}">
                        ${player.rank <= 3 ? (player.rank === 1 ? '🥇' : player.rank === 2 ? '🥈' : '🥉') : player.rank}
                    </div>
                </td>
                <td>
                    <div class="player-info">
                        <div class="player-avatar">${avatar}</div>
                        <div class="player-details">
                            <span class="player-name">${escapeHtml(player.name)}</span>
                            <span class="player-class">${classIcon} ${player.character_class || 'Warrior'}</span>
                        </div>
                    </div>
                </td>
                <td><strong>Lvl ${player.level}</strong></td>
                <td>${player.total_quests || 0}</td>
                <td>${player.total_monsters || 0}</td>
                <td>
                    <button class="view-profile-btn" onclick="viewProfile('${player.username}')">
                        View Profile
                    </button>
                </td>
            </tr>
        `;
    }).join('');
}

// Load your rank
async function loadYourRank() {
    try {
        const response = await fetch('/api/my-rank');
        if (!response.ok) throw new Error('Failed to load rank');
        
        const data = await response.json();
        const rank = data.rank;
        
        // Get character data
        const charResponse = await fetch('/api/character');
        const char = await charResponse.json();
        
        document.getElementById('your-rank-content').innerHTML = `
            <div class="your-rank-display">
                <div class="rank-stat">
                    <span class="rank-stat-value">#${rank}</span>
                    <span class="rank-stat-label">Global Rank</span>
                </div>
                <div class="rank-stat">
                    <span class="rank-stat-value">Lvl ${char.level}</span>
                    <span class="rank-stat-label">Level</span>
                </div>
                <div class="rank-stat">
                    <span class="rank-stat-value">${char.total_quests_completed || 0}</span>
                    <span class="rank-stat-label">Quests</span>
                </div>
                <div class="rank-stat">
                    <span class="rank-stat-value">${char.total_monsters_defeated || 0}</span>
                    <span class="rank-stat-label">Monsters</span>
                </div>
            </div>
        `;
    } catch (error) {
        console.error('Error loading rank:', error);
        document.getElementById('your-rank-content').innerHTML = `
            <p style="color: var(--text-secondary);">Complete quests to appear on the leaderboard!</p>
        `;
    }
}

// Timeframe button handlers
document.addEventListener('DOMContentLoaded', () => {
    const timeframeBtns = document.querySelectorAll('.timeframe-btn');
    
    timeframeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            timeframeBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            loadLeaderboard(btn.dataset.timeframe);
        });
    });
    
    // Public profile toggle
    const profileToggle = document.getElementById('public-profile-toggle');
    if (profileToggle) {
        // Load current setting
        fetch('/api/character')
            .then(res => res.json())
            .then(char => {
                profileToggle.checked = char.public_profile !== 0;
            });
        
        profileToggle.addEventListener('change', async () => {
            try {
                const response = await fetch('/api/profile/toggle', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ public: profileToggle.checked })
                });
                
                if (response.ok) {
                    showNotification(
                        profileToggle.checked ? 
                        'Profile is now public! 🌐' : 
                        'Profile is now private 🔒',
                        'success'
                    );
                    // Reload leaderboard if now hidden
                    if (!profileToggle.checked) {
                        loadLeaderboard(currentTimeframe);
                    }
                } else {
                    showNotification('Failed to update profile visibility', 'error');
                    profileToggle.checked = !profileToggle.checked; // Revert
                }
            } catch (error) {
                console.error('Error toggling profile:', error);
                showNotification('Network error', 'error');
                profileToggle.checked = !profileToggle.checked; // Revert
            }
        });
    }
});

// View profile function
function viewProfile(username) {
    window.open(`/profile/${username}`, '_blank');
    
    if (window.trackEvent) {
        window.trackEvent('profile_viewed', {
            username: username
        });
    }
}

// Share achievement to Twitter
function shareAchievement(achievementName) {
    const text = `Just unlocked "${achievementName}" in Quest Master! 🎮🏆\n\nJoin me: https://rpgtask.up.railway.app\n#productivity #gamification`;
    const url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}`;
    window.open(url, '_blank', 'width=550,height=420');
    
    if (window.trackEvent) {
        window.trackEvent('achievement_shared', {
            achievement_name: achievementName,
            platform: 'twitter'
        });
    }
}

// Share quest completion
function shareQuestMilestone(questCount) {
    const text = `${questCount} quests completed in Quest Master! 🎯🔥\nProductivity has never been this fun!\n\nStart your adventure: https://rpgtask.up.railway.app`;
    const url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}`;
    window.open(url, '_blank', 'width=550,height=420');
    
    if (window.trackEvent) {
        window.trackEvent('quest_milestone_shared', {
            quest_count: questCount,
            platform: 'twitter'
        });
    }
}

// Share level up
function shareLevelUp(level, characterClass) {
    const text = `Level UP! Just hit Level ${level} ${characterClass} in Quest Master! ⚔️✨\n\nTurn your tasks into quests: https://rpgtask.up.railway.app`;
    const url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}`;
    window.open(url, '_blank', 'width=550,height=420');
    
    if (window.trackEvent) {
        window.trackEvent('level_up_shared', {
            level: level,
            character_class: characterClass,
            platform: 'twitter'
        });
    }
}

// Copy profile link
function copyProfileLink(username) {
    const link = `https://rpgtask.up.railway.app/profile/${username}`;
    navigator.clipboard.writeText(link).then(() => {
        showNotification('Profile link copied! 📋', 'success');
        
        if (window.trackEvent) {
            window.trackEvent('profile_link_copied', {
                username: username
            });
        }
    });
}

// Helper function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Export functions
window.LeaderboardFunctions = {
    loadLeaderboard,
    loadYourRank,
    viewProfile,
    shareAchievement,
    shareQuestMilestone,
    shareLevelUp,
    copyProfileLink
};

