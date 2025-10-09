/**
 * Google Analytics Event Tracking
 * 
 * Usage: Add these event tracking calls throughout your app
 * Make sure Google Analytics is loaded first (analytics.html)
 */

// Track user registration
function trackRegistration() {
    if (window.trackEvent) {
        window.trackEvent('sign_up', {
            method: 'Email'
        });
    }
}

// Track login
function trackLogin() {
    if (window.trackEvent) {
        window.trackEvent('login', {
            method: 'Email'
        });
    }
}

// Track quest creation
function trackQuestCreated(difficulty) {
    if (window.trackEvent) {
        window.trackEvent('quest_created', {
            difficulty: difficulty
        });
    }
}

// Track quest completion
function trackQuestCompleted(difficulty, xpEarned, goldEarned, criticalHit, comboCount) {
    if (window.trackEvent) {
        window.trackEvent('quest_completed', {
            difficulty: difficulty,
            xp_earned: xpEarned,
            gold_earned: goldEarned,
            critical_hit: criticalHit,
            combo_count: comboCount
        });
    }
}

// Track level up
function trackLevelUp(newLevel, attack, defense) {
    if (window.trackEvent) {
        window.trackEvent('level_up', {
            character_level: newLevel,
            attack: attack,
            defense: defense
        });
    }
}

// Track shop purchase
function trackShopPurchase(itemName, itemType, goldSpent, rarity) {
    if (window.trackEvent) {
        window.trackEvent('shop_purchase', {
            item_name: itemName,
            item_type: itemType,
            gold_spent: goldSpent,
            rarity: rarity
        });
    }
}

// Track equipment equip
function trackEquipItem(itemName, itemType) {
    if (window.trackEvent) {
        window.trackEvent('equip_item', {
            item_name: itemName,
            item_type: itemType
        });
    }
}

// Track battle
function trackBattle(monsterName, monsterLevel, victory, goldEarned) {
    if (window.trackEvent) {
        window.trackEvent('battle', {
            monster_name: monsterName,
            monster_level: monsterLevel,
            victory: victory,
            gold_earned: goldEarned
        });
    }
}

// Track achievement unlock
function trackAchievementUnlocked(achievementName) {
    if (window.trackEvent) {
        window.trackEvent('achievement_unlocked', {
            achievement_name: achievementName
        });
    }
}

// Track character customization
function trackCharacterCustomization(characterClass, avatarId, colorTheme) {
    if (window.trackEvent) {
        window.trackEvent('customize_character', {
            character_class: characterClass,
            avatar_id: avatarId,
            color_theme: colorTheme
        });
    }
}

// Track template usage
function trackTemplateUsed(templateName, templateCategory) {
    if (window.trackEvent) {
        window.trackEvent('template_used', {
            template_name: templateName,
            template_category: templateCategory
        });
    }
}

// Track premium upgrade (when implemented)
function trackPremiumUpgrade(plan, price) {
    if (window.trackEvent) {
        window.trackEvent('purchase', {
            transaction_id: 'premium_' + Date.now(),
            value: price,
            currency: 'USD',
            items: [{
                item_name: 'Premium Subscription',
                item_id: plan,
                price: price,
                quantity: 1
            }]
        });
    }
}

// Track page views manually (if needed)
function trackPageView(pageName) {
    if (window.trackEvent) {
        window.trackEvent('page_view', {
            page_title: pageName
        });
    }
}

// Track time spent on page
let pageStartTime = Date.now();
window.addEventListener('beforeunload', function() {
    const timeSpent = Math.round((Date.now() - pageStartTime) / 1000);
    if (window.trackEvent && timeSpent > 5) { // Only track if more than 5 seconds
        window.trackEvent('time_on_page', {
            duration_seconds: timeSpent,
            page_title: document.title
        });
    }
});

// Export functions for use in other scripts
window.AnalyticsEvents = {
    trackRegistration,
    trackLogin,
    trackQuestCreated,
    trackQuestCompleted,
    trackLevelUp,
    trackShopPurchase,
    trackEquipItem,
    trackBattle,
    trackAchievementUnlocked,
    trackCharacterCustomization,
    trackTemplateUsed,
    trackPremiumUpgrade,
    trackPageView
};

