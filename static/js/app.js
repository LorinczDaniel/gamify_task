// Quest Master RPG - Frontend JavaScript

const API_BASE = '/api';

// State
let currentCharacter = null;
let currentTab = 'quests';
let questFilter = 'active';

// Initialize app on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
});

// Initialize application
async function initializeApp() {
    await loadCharacter();
    await loadQuests();
    await loadShopItems();
    await loadInventory();
    await loadAchievements();
    await loadBattleHistory();
}

// Setup event listeners
function setupEventListeners() {
    // Tab navigation
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            switchTab(e.target.dataset.tab);
        });
    });

    // Quest form
    document.getElementById('new-quest-btn').addEventListener('click', toggleQuestForm);
    document.getElementById('cancel-quest-btn').addEventListener('click', toggleQuestForm);
    document.getElementById('create-quest-btn').addEventListener('click', createQuest);

    // Quest filter
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            questFilter = e.target.dataset.filter;
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            loadQuests();
        });
    });

    // Monster cards
    document.querySelectorAll('.monster-card').forEach(card => {
        card.addEventListener('click', (e) => {
            const monster = e.currentTarget.dataset.monster;
            const level = parseInt(e.currentTarget.dataset.level);
            battleMonster(monster, level);
        });
    });

    // Achievement modal
    document.getElementById('achievement-modal-close').addEventListener('click', closeAchievementModal);
}

// Tab switching
function switchTab(tabName) {
    currentTab = tabName;
    
    // Update buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.tab === tabName) {
            btn.classList.add('active');
        }
    });

    // Update content
    document.querySelectorAll('.tab-pane').forEach(pane => {
        pane.classList.remove('active');
    });
    document.getElementById(`${tabName}-tab`).classList.add('active');

    // Load data if needed
    if (tabName === 'quests') loadQuests();
    if (tabName === 'shop') loadShopItems();
    if (tabName === 'inventory') loadInventory();
    if (tabName === 'battle') loadBattleHistory();
    if (tabName === 'achievements') loadAchievements();
}

// Load character data
async function loadCharacter() {
    try {
        const response = await fetch(`${API_BASE}/character`);
        currentCharacter = await response.json();
        updateCharacterUI();
    } catch (error) {
        console.error('Error loading character:', error);
        showNotification('Error loading character data', 'error');
    }
}

// Update character UI
function updateCharacterUI() {
    if (!currentCharacter) return;

    document.getElementById('character-name').textContent = currentCharacter.name;
    document.getElementById('character-level').textContent = currentCharacter.level;
    document.getElementById('character-attack').textContent = currentCharacter.attack;
    document.getElementById('character-defense').textContent = currentCharacter.defense;
    document.getElementById('character-gold').textContent = currentCharacter.gold;

    // Health bar
    const healthPercent = (currentCharacter.health / currentCharacter.max_health) * 100;
    document.getElementById('health-bar-fill').style.width = `${healthPercent}%`;
    document.getElementById('character-health-text').textContent = 
        `${currentCharacter.health}/${currentCharacter.max_health}`;

    // XP bar
    const xpPercent = (currentCharacter.xp / currentCharacter.xp_to_next_level) * 100;
    document.getElementById('xp-bar-fill').style.width = `${xpPercent}%`;
    document.getElementById('character-xp-text').textContent = 
        `${currentCharacter.xp}/${currentCharacter.xp_to_next_level}`;
}

// Quest functions
function toggleQuestForm() {
    const form = document.getElementById('quest-form');
    form.classList.toggle('hidden');
    
    if (!form.classList.contains('hidden')) {
        document.getElementById('quest-title').focus();
    } else {
        document.getElementById('quest-title').value = '';
        document.getElementById('quest-description').value = '';
        document.getElementById('quest-difficulty').value = 'medium';
    }
}

async function createQuest() {
    const title = document.getElementById('quest-title').value.trim();
    const description = document.getElementById('quest-description').value.trim();
    const difficulty = document.getElementById('quest-difficulty').value;

    if (!title) {
        showNotification('Please enter a quest title', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/quests`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, description, difficulty })
        });

        if (response.ok) {
            showNotification('Quest created successfully!', 'success');
            toggleQuestForm();
            await loadQuests();
        }
    } catch (error) {
        console.error('Error creating quest:', error);
        showNotification('Error creating quest', 'error');
    }
}

async function loadQuests() {
    try {
        const completed = questFilter === 'completed';
        const response = await fetch(`${API_BASE}/quests?completed=${completed}`);
        const quests = await response.json();
        
        const questsList = document.getElementById('quests-list');
        
        if (quests.length === 0) {
            questsList.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📜</div>
                    <p>${completed ? 'No completed quests yet' : 'No active quests. Create one to get started!'}</p>
                </div>
            `;
            return;
        }

        questsList.innerHTML = quests.map(quest => `
            <div class="quest-card ${quest.completed ? 'completed' : ''}">
                <div class="quest-header">
                    <h3 class="quest-title">${escapeHtml(quest.title)}</h3>
                    <span class="quest-difficulty ${quest.difficulty}">${quest.difficulty}</span>
                </div>
                ${quest.description ? `<p class="quest-description">${escapeHtml(quest.description)}</p>` : ''}
                <div class="quest-rewards">
                    <span>✨ ${quest.xp_reward} XP</span>
                    <span>💰 ${quest.gold_reward} Gold</span>
                </div>
                <div class="quest-actions">
                    ${!quest.completed ? `
                        <button class="btn btn-success btn-small" onclick="completeQuest(${quest.id})">
                            ✓ Complete
                        </button>
                    ` : ''}
                    <button class="btn btn-danger btn-small" onclick="deleteQuest(${quest.id})">
                        🗑️ Delete
                    </button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading quests:', error);
        showNotification('Error loading quests', 'error');
    }
}

async function completeQuest(questId) {
    try {
        const response = await fetch(`${API_BASE}/quests/${questId}/complete`, {
            method: 'POST'
        });

        if (response.ok) {
            const result = await response.json();
            showNotification(`Quest completed! +${result.rewards.xp} XP, +${result.rewards.gold} Gold`, 'success');
            
            // Check for level up
            if (result.character.level > currentCharacter.level) {
                showNotification(`🎉 Level Up! You are now level ${result.character.level}!`, 'success');
            }

            // Show achievement unlocks
            if (result.newly_unlocked_achievements && result.newly_unlocked_achievements.length > 0) {
                showAchievementUnlock(result.newly_unlocked_achievements);
            }

            await loadCharacter();
            await loadQuests();
        }
    } catch (error) {
        console.error('Error completing quest:', error);
        showNotification('Error completing quest', 'error');
    }
}

async function deleteQuest(questId) {
    if (!confirm('Are you sure you want to delete this quest?')) return;

    try {
        const response = await fetch(`${API_BASE}/quests/${questId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            showNotification('Quest deleted', 'info');
            await loadQuests();
        }
    } catch (error) {
        console.error('Error deleting quest:', error);
        showNotification('Error deleting quest', 'error');
    }
}

// Shop functions
async function loadShopItems() {
    try {
        const response = await fetch(`${API_BASE}/shop/items`);
        const items = await response.json();
        
        const shopItems = document.getElementById('shop-items');
        
        shopItems.innerHTML = items.map(item => `
            <div class="item-card ${item.rarity}">
                ${getItemIcon(item.type)}
                <h3 class="item-name">${escapeHtml(item.name)}</h3>
                <p class="item-type">${item.type}</p>
                <p class="item-description">${escapeHtml(item.description)}</p>
                <div class="item-stats">
                    ${item.attack_bonus > 0 ? `<div class="item-stat">⚔️ +${item.attack_bonus} Attack</div>` : ''}
                    ${item.defense_bonus > 0 ? `<div class="item-stat">🛡️ +${item.defense_bonus} Defense</div>` : ''}
                    ${item.health_bonus > 0 ? `<div class="item-stat">❤️ +${item.health_bonus} Health</div>` : ''}
                </div>
                <div class="item-price">💰 ${item.price}</div>
                <button class="btn btn-primary" onclick="purchaseItem(${item.id})" 
                    ${currentCharacter && currentCharacter.gold < item.price ? 'disabled' : ''}>
                    ${currentCharacter && currentCharacter.gold >= item.price ? 'Purchase' : 'Not Enough Gold'}
                </button>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading shop items:', error);
        showNotification('Error loading shop', 'error');
    }
}

async function purchaseItem(itemId) {
    try {
        const response = await fetch(`${API_BASE}/shop/purchase`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ item_id: itemId })
        });

        const result = await response.json();

        if (result.error) {
            showNotification(result.error, 'error');
            return;
        }

        showNotification(`Purchased ${result.item.name}!`, 'success');

        // Show achievement unlocks
        if (result.newly_unlocked_achievements && result.newly_unlocked_achievements.length > 0) {
            showAchievementUnlock(result.newly_unlocked_achievements);
        }

        await loadCharacter();
        await loadShopItems();
        await loadInventory();
    } catch (error) {
        console.error('Error purchasing item:', error);
        showNotification('Error purchasing item', 'error');
    }
}

// Inventory functions
async function loadInventory() {
    try {
        const response = await fetch(`${API_BASE}/inventory`);
        const items = await response.json();
        
        const inventoryItems = document.getElementById('inventory-items');
        
        if (items.length === 0) {
            inventoryItems.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">🎒</div>
                    <p>Your inventory is empty. Visit the shop to buy items!</p>
                </div>
            `;
            return;
        }

        inventoryItems.innerHTML = items.map(item => `
            <div class="item-card ${item.rarity}">
                ${item.equipped ? '<span class="equipped-badge">⚡ Equipped</span>' : ''}
                ${getItemIcon(item.type)}
                <h3 class="item-name">${escapeHtml(item.name)}</h3>
                <p class="item-type">${item.type}</p>
                <p class="item-description">${escapeHtml(item.description)}</p>
                <div class="item-stats">
                    ${item.attack_bonus > 0 ? `<div class="item-stat">⚔️ +${item.attack_bonus} Attack</div>` : ''}
                    ${item.defense_bonus > 0 ? `<div class="item-stat">🛡️ +${item.defense_bonus} Defense</div>` : ''}
                    ${item.health_bonus > 0 ? `<div class="item-stat">❤️ +${item.health_bonus} Health</div>` : ''}
                </div>
                ${item.type !== 'consumable' ? `
                    <button class="btn ${item.equipped ? 'btn-secondary' : 'btn-success'}" 
                        onclick="equipItem(${item.inventory_id})"
                        ${item.equipped ? 'disabled' : ''}>
                        ${item.equipped ? 'Equipped' : 'Equip'}
                    </button>
                ` : ''}
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading inventory:', error);
        showNotification('Error loading inventory', 'error');
    }
}

async function equipItem(inventoryId) {
    try {
        const response = await fetch(`${API_BASE}/inventory/${inventoryId}/equip`, {
            method: 'POST'
        });

        const result = await response.json();

        if (result.error) {
            showNotification(result.error, 'error');
            return;
        }

        showNotification('Item equipped!', 'success');
        await loadCharacter();
        await loadInventory();
    } catch (error) {
        console.error('Error equipping item:', error);
        showNotification('Error equipping item', 'error');
    }
}

// Battle functions
async function battleMonster(monsterName, monsterLevel) {
    try {
        const response = await fetch(`${API_BASE}/battle`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                monster_name: monsterName, 
                monster_level: monsterLevel 
            })
        });

        const result = await response.json();
        showBattleResult(result);

        // Show achievement unlocks
        if (result.newly_unlocked_achievements && result.newly_unlocked_achievements.length > 0) {
            showAchievementUnlock(result.newly_unlocked_achievements);
        }

        await loadCharacter();
        await loadBattleHistory();
    } catch (error) {
        console.error('Error in battle:', error);
        showNotification('Error during battle', 'error');
    }
}

function showBattleResult(result) {
    const battleResult = document.getElementById('battle-result');
    battleResult.classList.remove('hidden', 'victory', 'defeat');
    battleResult.classList.add(result.won ? 'victory' : 'defeat');

    battleResult.innerHTML = `
        <h3>${result.won ? '🎉 Victory!' : '💀 Defeat!'}</h3>
        <p style="font-size: 1.2rem; margin-bottom: 20px;">
            You ${result.won ? 'defeated' : 'were defeated by'} 
            ${result.monster.name} (Level ${result.monster.level})
        </p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-bottom: 20px;">
            <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px;">
                <div style="color: #94a3b8; margin-bottom: 5px;">Monster Stats</div>
                <div>⚔️ ${result.monster.attack}</div>
                <div>🛡️ ${result.monster.defense}</div>
                <div>❤️ ${result.monster.health}</div>
            </div>
            <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px;">
                <div style="color: #94a3b8; margin-bottom: 5px;">Rewards</div>
                <div>✨ +${result.rewards.xp} XP</div>
                <div>💰 +${result.rewards.gold} Gold</div>
            </div>
        </div>
        <p style="color: #94a3b8; font-size: 0.9rem;">
            ${result.won ? 
                'Your strength has proven superior!' : 
                'Train harder and try again!'}
        </p>
    `;

    // Scroll to result
    battleResult.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

async function loadBattleHistory() {
    try {
        const response = await fetch(`${API_BASE}/battle/history`);
        const battles = await response.json();
        
        const historyList = document.getElementById('battle-history-list');
        
        if (battles.length === 0) {
            historyList.innerHTML = '<p style="color: var(--text-secondary);">No battles yet. Challenge a monster!</p>';
            return;
        }

        historyList.innerHTML = battles.map(battle => `
            <div class="battle-entry ${battle.won ? 'won' : 'lost'}">
                <div>
                    <strong>${battle.monster_name}</strong> (Lvl ${battle.monster_level})
                    <span style="color: var(--text-secondary); font-size: 0.85rem; margin-left: 10px;">
                        ${new Date(battle.battled_at).toLocaleDateString()}
                    </span>
                </div>
                <div style="text-align: right;">
                    <div style="color: ${battle.won ? 'var(--success-color)' : 'var(--danger-color)'}">
                        ${battle.won ? 'Victory' : 'Defeat'}
                    </div>
                    ${battle.won ? `
                        <div style="font-size: 0.85rem; color: var(--text-secondary);">
                            +${battle.xp_gained} XP, +${battle.gold_gained} Gold
                        </div>
                    ` : ''}
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading battle history:', error);
    }
}

// Achievement functions
async function loadAchievements() {
    try {
        const response = await fetch(`${API_BASE}/achievements`);
        const achievements = await response.json();
        
        const achievementsList = document.getElementById('achievements-list');
        
        achievementsList.innerHTML = achievements.map(ach => `
            <div class="achievement-card ${ach.unlocked ? 'unlocked' : 'locked'}">
                <div class="achievement-icon">${ach.icon}</div>
                <h3 class="achievement-name">${escapeHtml(ach.name)}</h3>
                <p class="achievement-description">${escapeHtml(ach.description)}</p>
                ${ach.unlocked ? `
                    <p style="color: var(--gold-color); font-size: 0.85rem; margin-top: 10px;">
                        Unlocked ${new Date(ach.unlocked_at).toLocaleDateString()}
                    </p>
                ` : ''}
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading achievements:', error);
        showNotification('Error loading achievements', 'error');
    }
}

function showAchievementUnlock(achievements) {
    const modal = document.getElementById('achievement-modal');
    const content = document.getElementById('achievement-modal-content');
    
    content.innerHTML = achievements.map(ach => `
        <div style="margin: 20px 0;">
            <div style="font-size: 4rem; margin-bottom: 10px;">${ach.icon}</div>
            <h3 style="color: var(--gold-color); margin-bottom: 10px;">${escapeHtml(ach.name)}</h3>
            <p style="color: var(--text-secondary);">${escapeHtml(ach.description)}</p>
        </div>
    `).join('');
    
    modal.classList.remove('hidden');
    
    // Reload achievements list
    loadAchievements();
}

function closeAchievementModal() {
    document.getElementById('achievement-modal').classList.add('hidden');
}

// Utility functions
function showNotification(message, type = 'info') {
    const container = document.getElementById('notification-container');
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    container.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideInRight 0.3s ease-out reverse';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function getItemIcon(type) {
    const icons = {
        weapon: '⚔️',
        armor: '🛡️',
        accessory: '💍',
        consumable: '🧪'
    };
    return `<div class="item-icon">${icons[type] || '📦'}</div>`;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

