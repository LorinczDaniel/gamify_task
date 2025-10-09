// Quest Master RPG - Frontend JavaScript

const API_BASE = '/api';

// State
let currentCharacter = null;
let currentUsername = null;
let currentTab = 'quests';
let questFilter = 'active';
let currentTemplateCategory = 'all';
let previousLevel = 0;
let currentTimeframe = 'all';

// Initialize app on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
});

// Initialize application
async function initializeApp() {
    await loadCharacter();
    await loadTemplates();
    await loadQuests();
    await loadShopItems();
    await loadInventory();
    await loadAchievements();
    await loadBattleHistory();
    
    // Load leaderboard if tab is visible
    if (currentTab === 'leaderboard') {
        await loadLeaderboard();
        await loadYourRank();
    }
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
    
    // Logout button
    document.getElementById('logout-btn').addEventListener('click', logout);
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
        
        if (response.status === 401) {
            window.location.href = '/login';
            return;
        }
        
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

    // Check for level up
    if (previousLevel > 0 && currentCharacter.level > previousLevel) {
        showLevelUpCelebration(previousLevel, currentCharacter.level);
    }
    previousLevel = currentCharacter.level;

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

// Template functions
async function loadTemplates() {
    try {
        // Load categories
        const categoryResponse = await fetch(`${API_BASE}/templates/categories`);
        const categories = await categoryResponse.json();
        
        // Create category tabs
        const categoryTabs = document.getElementById('category-tabs');
        categoryTabs.innerHTML = `
            <div class="category-tab active" data-category="all">⭐ Popular</div>
            ${categories.map(cat => `
                <div class="category-tab" data-category="${cat}">${getCategoryIcon(cat)} ${capitalizeFirst(cat)}</div>
            `).join('')}
        `;
        
        // Add category tab listeners
        document.querySelectorAll('.category-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                currentTemplateCategory = e.target.dataset.category;
                document.querySelectorAll('.category-tab').forEach(t => t.classList.remove('active'));
                e.target.classList.add('active');
                loadTemplatesByCategory();
            });
        });
        
        // Load popular templates initially
        await loadTemplatesByCategory();
    } catch (error) {
        console.error('Error loading templates:', error);
    }
}

async function loadTemplatesByCategory() {
    try {
        let url = `${API_BASE}/templates`;
        if (currentTemplateCategory === 'all') {
            url += '?popular=true';
        } else {
            url += `?category=${currentTemplateCategory}`;
        }
        
        const response = await fetch(url);
        const templates = await response.json();
        
        const templateGrid = document.getElementById('template-grid');
        templateGrid.innerHTML = templates.map(template => `
            <div class="template-btn" data-template-id="${template.id}">
                <span class="template-icon">${template.icon}</span>
                <div class="template-info">
                    <div class="template-title">${template.title}</div>
                    <div class="template-difficulty ${template.difficulty}">${template.difficulty}</div>
                </div>
            </div>
        `).join('');
        
        // Add click listeners
        document.querySelectorAll('.template-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const templateId = e.currentTarget.dataset.templateId;
                createQuestFromTemplate(templateId);
            });
        });
    } catch (error) {
        console.error('Error loading templates:', error);
    }
}

async function createQuestFromTemplate(templateId) {
    try {
        const response = await fetch(`${API_BASE}/templates/${templateId}/create`, {
            method: 'POST',
        });
        
        if (response.ok) {
            showNotification('Quest added! Complete it to earn rewards! 🎯', 'success');
            await loadQuests();
        }
    } catch (error) {
        console.error('Error creating quest from template:', error);
        showNotification('Failed to create quest', 'error');
    }
}

function getCategoryIcon(category) {
    const icons = {
        'household': '🏠',
        'work': '💼',
        'health': '💪',
        'self-care': '✨',
        'social': '👥',
        'financial': '💰'
    };
    return icons[category] || '📝';
}

function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
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
            
            // Show enhanced reward popup
            showRewardPopup(result);
            
            // Show combo badge if applicable
            if (result.bonus && result.bonus.is_combo) {
                showComboBadge(result.bonus.combo_count);
            }

            // Show achievement unlocks
            if (result.newly_unlocked_achievements && result.newly_unlocked_achievements.length > 0) {
                setTimeout(() => {
                    showAchievementUnlock(result.newly_unlocked_achievements);
                }, 3000);
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
        // Make API call first to get battle result
        const response = await fetch(`${API_BASE}/battle`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                monster_name: monsterName, 
                monster_level: monsterLevel 
            })
        });

        const result = await response.json();
        
        // Show animated battle
        await showAnimatedBattle(result, monsterName, monsterLevel);

        // Show achievement unlocks
        if (result.newly_unlocked_achievements && result.newly_unlocked_achievements.length > 0) {
            setTimeout(() => {
                showAchievementUnlock(result.newly_unlocked_achievements);
            }, 1000);
        }

        await loadCharacter();
        await loadBattleHistory();
    } catch (error) {
        console.error('Error in battle:', error);
        showNotification('Error during battle', 'error');
    }
}

async function showAnimatedBattle(result, monsterName, monsterLevel) {
    const arena = document.getElementById('battle-arena');
    const battleLog = document.getElementById('battle-log');
    
    // Get monster emoji
    const monsterEmojis = {
        'Goblin': '👺',
        'Orc': '👹',
        'Troll': '🧌',
        'Dragon': '🐉',
        'Demon': '😈',
        'Ancient Dragon': '🐲'
    };
    
    // Set up battle field
    document.getElementById('hero-name').textContent = currentCharacter.name;
    document.getElementById('hero-attack').textContent = currentCharacter.attack;
    document.getElementById('hero-defense').textContent = currentCharacter.defense;
    document.getElementById('monster-name').textContent = monsterName;
    document.getElementById('monster-attack').textContent = result.monster.attack;
    document.getElementById('monster-defense').textContent = result.monster.defense;
    document.getElementById('monster-sprite').textContent = monsterEmojis[monsterName] || '👹';
    
    // Calculate actual health values for animation
    const heroMaxHP = currentCharacter.max_health;
    const monsterMaxHP = result.monster.health;
    let heroHP = heroMaxHP;
    let monsterHP = monsterMaxHP;
    
    // Update health bars
    updateBattleHealth('hero', heroHP, heroMaxHP);
    updateBattleHealth('monster', monsterHP, monsterMaxHP);
    
    // Show arena
    arena.style.display = 'flex';
    battleLog.innerHTML = '';
    
    // Wait for entrance animation
    await sleep(800);
    
    // Simulate turn-based combat
    const heroSprite = document.getElementById('hero-sprite');
    const monsterSprite = document.getElementById('monster-sprite');
    
    addBattleLog(`${currentCharacter.name} encounters ${monsterName}!`);
    await sleep(1000);
    
    // Determine winner and simulate combat
    const heroPower = currentCharacter.attack - result.monster.defense;
    const monsterPower = result.monster.attack - currentCharacter.defense;
    const heroDamage = Math.max(heroPower, 1);
    const monsterDamage = Math.max(monsterPower, 1);
    
    // Combat rounds
    let round = 1;
    while (heroHP > 0 && monsterHP > 0 && round <= 5) {
        // Hero attacks
        addBattleLog(`${currentCharacter.name} attacks! 💥`);
        heroSprite.classList.add('attacking');
        await sleep(300);
        
        createSlashEffect(monsterSprite);
        monsterSprite.classList.add('taking-damage');
        monsterHP = Math.max(0, monsterHP - heroDamage * 15);
        showDamageNumber(monsterSprite, heroDamage * 15, false);
        updateBattleHealth('monster', monsterHP, monsterMaxHP);
        
        await sleep(600);
        heroSprite.classList.remove('attacking');
        monsterSprite.classList.remove('taking-damage');
        
        if (monsterHP <= 0) break;
        
        await sleep(500);
        
        // Monster attacks
        addBattleLog(`${monsterName} counter-attacks! 🔥`);
        monsterSprite.classList.add('attacking');
        await sleep(300);
        
        createSlashEffect(heroSprite);
        heroSprite.classList.add('taking-damage');
        heroHP = Math.max(0, heroHP - monsterDamage * 8);
        showDamageNumber(heroSprite, monsterDamage * 8, false);
        updateBattleHealth('hero', heroHP, heroMaxHP);
        
        await sleep(600);
        monsterSprite.classList.remove('attacking');
        heroSprite.classList.remove('taking-damage');
        
        await sleep(800);
        round++;
    }
    
    // Determine actual result based on API response
    await sleep(500);
    
    if (result.won) {
        addBattleLog(`${currentCharacter.name} emerges victorious! 🎉`);
        monsterSprite.style.opacity = '0.3';
        createConfetti(20);
    } else {
        addBattleLog(`${monsterName} proves too powerful... 💀`);
        heroSprite.style.opacity = '0.7';
    }
    
    await sleep(1500);
    
    // Show result screen
    showBattleResultScreen(result);
}

function updateBattleHealth(combatant, current, max) {
    const healthBar = document.getElementById(`${combatant}-health-bar`);
    const healthText = document.getElementById(`${combatant}-health-text`);
    const percent = (current / max) * 100;
    
    healthBar.style.width = percent + '%';
    healthText.textContent = `${Math.round(current)}/${max}`;
    
    if (percent <= 25) {
        healthBar.classList.add('low');
    } else {
        healthBar.classList.remove('low');
    }
}

function addBattleLog(message) {
    const battleLog = document.getElementById('battle-log');
    const entry = document.createElement('div');
    entry.className = 'battle-log-entry';
    entry.textContent = message;
    battleLog.appendChild(entry);
    battleLog.scrollTop = battleLog.scrollHeight;
}

function showDamageNumber(target, damage, isCrit) {
    const rect = target.getBoundingClientRect();
    const damageEl = document.createElement('div');
    damageEl.className = 'damage-number' + (isCrit ? ' critical' : '');
    damageEl.textContent = `-${Math.round(damage)}`;
    damageEl.style.left = rect.left + rect.width / 2 + 'px';
    damageEl.style.top = rect.top + 'px';
    document.body.appendChild(damageEl);
    
    setTimeout(() => damageEl.remove(), 1000);
}

function createSlashEffect(target) {
    const rect = target.getBoundingClientRect();
    const slash = document.createElement('div');
    slash.className = 'slash-effect';
    slash.textContent = '⚔️';
    slash.style.left = rect.left + rect.width / 2 - 50 + 'px';
    slash.style.top = rect.top + rect.height / 2 - 50 + 'px';
    document.body.appendChild(slash);
    
    setTimeout(() => slash.remove(), 500);
}

function showBattleResultScreen(result) {
    const arena = document.getElementById('battle-arena');
    const resultDiv = document.createElement('div');
    resultDiv.className = 'battle-result ' + (result.won ? 'victory' : 'defeat');
    
    resultDiv.innerHTML = `
        <h2>${result.won ? '🏆 VICTORY! 🏆' : '💀 DEFEAT 💀'}</h2>
        <p style="font-size: 1.3rem; margin: 20px 0;">
            ${result.won ? 
                `You have defeated ${result.monster.name}!` : 
                `${result.monster.name} has bested you in combat.`}
        </p>
        <div class="battle-rewards">
            <div class="reward-item">✨ +${result.rewards.xp} XP</div>
            <div class="reward-item">💰 +${result.rewards.gold} Gold</div>
        </div>
        <p style="color: var(--text-secondary); margin: 20px 0;">
            ${result.won ? 
                'Your strength grows with each victory!' : 
                'Learn from this defeat and grow stronger!'}
        </p>
        <button class="btn btn-primary" onclick="closeBattleArena()" style="font-size: 1.2rem; padding: 15px 30px;">
            Continue
        </button>
    `;
    
    arena.appendChild(resultDiv);
}

function closeBattleArena() {
    const arena = document.getElementById('battle-arena');
    arena.style.animation = 'battleArenaAppear 0.3s ease-out reverse';
    setTimeout(() => {
        arena.style.display = 'none';
        arena.style.animation = 'battleArenaAppear 0.5s ease-out';
        // Clean up result screen
        const resultScreen = arena.querySelector('.battle-result');
        if (resultScreen) resultScreen.remove();
        // Reset sprites
        document.getElementById('hero-sprite').style.opacity = '1';
        document.getElementById('monster-sprite').style.opacity = '1';
    }, 300);
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Logout function
async function logout() {
    if (!confirm('Are you sure you want to logout?')) return;
    
    try {
        await fetch('/api/logout', { method: 'POST' });
        window.location.href = '/login';
    } catch (error) {
        console.error('Error logging out:', error);
        window.location.href = '/login';
    }
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
            <button class="share-btn" onclick="shareAchievement('${escapeHtml(ach.name)}')" style="margin-top: 15px;">
                🐦 Share on Twitter
            </button>
        </div>
    `).join('');
    
    modal.classList.remove('hidden');
    
    // Reload achievements list
    loadAchievements();
    
    // Track achievement unlock
    if (window.trackEvent && window.AnalyticsEvents) {
        achievements.forEach(ach => {
            window.AnalyticsEvents.trackAchievementUnlocked(ach.name);
        });
    }
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

// Enhanced reward animations
function showRewardPopup(result) {
    const popup = document.getElementById('reward-popup');
    const content = document.getElementById('reward-content');
    
    const bonus = result.bonus || {};
    const isCritical = bonus.is_critical;
    const isCombo = bonus.is_combo;
    const multiplier = bonus.total_multiplier || 1;
    const rareDrop = bonus.rare_drop;
    
    let bonusHTML = '';
    if (isCritical) {
        bonusHTML += `<div class="reward-bonus-text">💥 CRITICAL HIT! 💥</div>`;
        bonusHTML += `<div class="reward-multiplier">${bonus.crit_multiplier}x Multiplier!</div>`;
    }
    if (isCombo) {
        bonusHTML += `<div class="reward-bonus-text">🔥 ${bonus.combo_count}x COMBO! 🔥</div>`;
        bonusHTML += `<div class="reward-multiplier">${bonus.combo_multiplier.toFixed(1)}x Multiplier!</div>`;
    }
    if (rareDrop) {
        bonusHTML += `<div class="reward-bonus-text">🎁 BONUS DROP! +${rareDrop.amount} Gold! 🎁</div>`;
    }
    
    content.innerHTML = `
        <h2>Quest Complete!</h2>
        ${bonusHTML}
        <div class="reward-content">
            <div>
                <span class="reward-amount" ${isCritical ? 'class="critical-hit"' : ''}>
                    +${result.rewards.xp} XP
                </span>
                ${result.rewards.base_xp !== result.rewards.xp ? 
                    `<small>(Base: ${result.rewards.base_xp})</small>` : ''}
            </div>
            <div>
                <span class="reward-amount" ${isCritical ? 'class="critical-hit"' : ''}>
                    +${result.rewards.gold} Gold
                </span>
                ${result.rewards.base_gold !== result.rewards.gold ? 
                    `<small>(Base: ${result.rewards.base_gold})</small>` : ''}
            </div>
        </div>
        ${multiplier > 1 ? `<p style="margin-top: 20px; font-size: 1.2rem;">Total Multiplier: <strong>${multiplier.toFixed(2)}x</strong></p>` : ''}
        <button class="btn btn-primary" onclick="closeRewardPopup()" style="margin-top: 20px;">Awesome!</button>
    `;
    
    popup.style.display = 'block';
    popup.style.animation = 'rewardPopIn 0.5s ease-out forwards';
    
    // Create confetti
    if (isCritical || isCombo) {
        createConfetti();
    }
    
    // Auto-close after 5 seconds
    setTimeout(() => {
        closeRewardPopup();
    }, 5000);
}

function closeRewardPopup() {
    const popup = document.getElementById('reward-popup');
    popup.style.animation = 'rewardPopIn 0.3s ease-out reverse';
    setTimeout(() => {
        popup.style.display = 'none';
    }, 300);
}

function showComboBadge(comboCount) {
    const badge = document.getElementById('combo-badge');
    const numberEl = document.getElementById('combo-number');
    
    numberEl.textContent = comboCount;
    badge.style.display = 'block';
    
    // Reset animation
    badge.style.animation = 'none';
    setTimeout(() => {
        badge.style.animation = 'comboAppear 0.3s ease-out, comboPulse 1s ease-in-out infinite';
    }, 10);
    
    // Hide after 10 minutes (matches combo timeout)
    setTimeout(() => {
        badge.style.display = 'none';
    }, 10 * 60 * 1000);
}

function showLevelUpCelebration(oldLevel, newLevel) {
    const overlay = document.getElementById('level-up-overlay');
    const content = document.getElementById('level-up-content');
    
    // Calculate stat increases (based on backend logic)
    const healthIncrease = 10;
    const attackIncrease = 3;
    const defenseIncrease = 2;
    
    content.innerHTML = `
        <h1>🎊 LEVEL UP! 🎊</h1>
        <p style="font-size: 2rem; margin: 20px 0;">Level ${oldLevel} → Level ${newLevel}</p>
        <div class="level-up-stats">
            <div class="stat-increase">
                <span>❤️ Max Health</span>
                <span class="increase">+${healthIncrease}</span>
            </div>
            <div class="stat-increase">
                <span>⚔️ Attack</span>
                <span class="increase">+${attackIncrease}</span>
            </div>
            <div class="stat-increase">
                <span>🛡️ Defense</span>
                <span class="increase">+${defenseIncrease}</span>
            </div>
        </div>
        <button class="btn btn-primary" onclick="closeLevelUpOverlay()" style="margin-top: 30px; font-size: 1.2rem; padding: 15px 40px;">
            Continue Your Journey!
        </button>
    `;
    
    overlay.style.display = 'flex';
    createConfetti(50); // More confetti for level ups!
}

function closeLevelUpOverlay() {
    const overlay = document.getElementById('level-up-overlay');
    overlay.style.animation = 'overlayFadeIn 0.3s ease-out reverse';
    setTimeout(() => {
        overlay.style.display = 'none';
        overlay.style.animation = 'overlayFadeIn 0.3s ease-out';
    }, 300);
}

function createConfetti(count = 30) {
    const colors = ['#fbbf24', '#f59e0b', '#d97706', '#ef4444', '#10b981', '#3b82f6', '#a78bfa'];
    
    for (let i = 0; i < count; i++) {
        setTimeout(() => {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            confetti.style.left = Math.random() * 100 + '%';
            confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            confetti.style.animationDelay = Math.random() * 0.5 + 's';
            confetti.style.animationDuration = (Math.random() * 2 + 2) + 's';
            
            document.body.appendChild(confetti);
            
            setTimeout(() => confetti.remove(), 3500);
        }, i * 30);
    }
}

