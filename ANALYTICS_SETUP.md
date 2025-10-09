# 📊 Google Analytics Setup Guide

**Goal**: Track user behavior, page views, and conversions in Quest Master

---

## 🚀 Quick Setup (10 minutes)

### Step 1: Create Google Analytics Account

1. **Go to**: https://analytics.google.com
2. **Sign in** with your Google account
3. **Click "Start measuring"**
4. **Account Setup**:
   - Account name: `Quest Master`
   - Check all data sharing settings (recommended)
   - Click "Next"

5. **Property Setup**:
   - Property name: `Quest Master App`
   - Reporting time zone: Your timezone
   - Currency: USD (or your currency)
   - Click "Next"

6. **Business Information**:
   - Industry: Software/Technology
   - Business size: Small (1-10)
   - How you intend to use Analytics: Check all that apply
   - Click "Create"

7. **Accept Terms of Service**

### Step 2: Set Up Data Stream

1. **Choose platform**: Web
2. **Website URL**: `https://your-app.railway.app` (or your domain)
3. **Stream name**: `Quest Master Production`
4. **Click "Create stream"**

### Step 3: Get Your Measurement ID

You'll see a **Measurement ID** like: `G-XXXXXXXXXX`

**Copy this!** You'll need it.

---

## 💻 Implementation

### Option 1: Google Tag (gtag.js) - Recommended

Add this to your HTML `<head>` section:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

### Option 2: Google Tag Manager (GTM) - Advanced

If you want more control:
1. Go to https://tagmanager.google.com
2. Create account and container
3. Add GTM code to your site
4. Configure GA4 tag in GTM

---

## 🎯 Custom Events to Track

### User Actions
```javascript
// Registration
gtag('event', 'sign_up', {
  method: 'Email'
});

// Quest Completion
gtag('event', 'quest_completed', {
  difficulty: 'medium',
  xp_earned: 50
});

// Level Up
gtag('event', 'level_up', {
  character_level: 5
});

// Purchase (Premium)
gtag('event', 'purchase', {
  transaction_id: 'T12345',
  value: 4.99,
  currency: 'USD',
  items: [{
    item_name: 'Premium Subscription',
    price: 4.99
  }]
});

// Shop Purchase
gtag('event', 'shop_purchase', {
  item_name: 'Iron Sword',
  gold_spent: 200
});

// Character Customization
gtag('event', 'customize_character', {
  character_class: 'Warrior',
  avatar_id: 3
});
```

---

## 📈 Key Metrics to Monitor

### User Acquisition
- **New Users**: How many people sign up
- **Traffic Sources**: Where users come from (Reddit, ProductHunt, etc.)
- **User Demographics**: Age, location, interests

### Engagement
- **Active Users**: Daily/Weekly/Monthly
- **Session Duration**: How long users stay
- **Pages per Session**: How many pages they view
- **Events**: Custom actions (quests completed, etc.)

### Retention
- **Returning Users**: How many come back
- **User Retention**: Day 1, 7, 30 retention rates
- **Churn Rate**: When users stop using the app

### Conversions (After Adding Payments)
- **Conversion Rate**: Free → Paid users
- **Revenue**: Total from subscriptions
- **ARPU**: Average Revenue Per User
- **LTV**: Customer Lifetime Value

---

## 🎨 Custom Dimensions (Advanced)

Track extra data about users:

1. **Character Level**: Track user's character level
2. **Premium Status**: Free vs. Premium user
3. **Character Class**: Warrior, Mage, Rogue, Ranger
4. **Days Active**: How many days they've used the app
5. **Quests Completed**: Total quest count

---

## 🔒 Privacy & GDPR Compliance

### Required for EU Users

1. **Cookie Consent Banner**:
```javascript
// Only load analytics after consent
if (getCookieConsent()) {
  // Load gtag.js
}
```

2. **Privacy Policy**: Update to mention Google Analytics
3. **Data Retention**: Set in GA4 settings (14 months recommended)
4. **IP Anonymization**: Automatic in GA4
5. **User Opt-Out**: Provide option to disable tracking

---

## 🧪 Testing Your Setup

### Verify Installation

1. **Real-Time Reports**:
   - GA4 Dashboard → Reports → Realtime
   - Visit your site
   - Should see 1 active user (you!)

2. **DebugView** (Recommended):
   - Add `?debug_mode=true` to URL
   - Or use GA Debugger Chrome extension
   - See events in real-time

3. **Chrome DevTools**:
   - Open DevTools → Network tab
   - Filter: `google-analytics` or `gtag`
   - Should see requests being sent

### Test Events

```javascript
// Test custom event
gtag('event', 'test_event', {
  test_parameter: 'test_value'
});
```

Check in GA4 → Realtime → Events

---

## 📊 Useful Reports to Create

### User Behavior Flow
Shows how users navigate through your app

### Conversion Funnels
Track signup → first quest → level up → premium purchase

### Cohort Analysis
See retention by signup date

### Custom Dashboards
Create dashboard with your key metrics

---

## 🔧 Troubleshooting

### Analytics Not Working?

1. **Check Measurement ID**: Correct format `G-XXXXXXXXXX`
2. **Ad Blockers**: May block Google Analytics (test in incognito)
3. **Browser Console**: Check for errors
4. **Wait 24 hours**: Data may take time to appear in reports

### Events Not Showing?

1. **Check event name**: No spaces, lowercase recommended
2. **Verify gtag loaded**: `console.log(window.gtag)`
3. **Use DebugView**: See events in real-time
4. **Check date range**: Recent events only

---

## 🎯 Goals to Set Up

### Micro Conversions
- Sign up completed
- First quest created
- First quest completed
- Profile customized
- First item purchased

### Macro Conversions
- Premium subscription purchased
- 7-day retention
- 30-day retention
- Referral made

---

## 📱 Mobile App Tracking (Future)

When you create mobile apps:
- **Firebase Analytics** (same as GA4)
- Track app opens, screen views
- In-app purchase events

---

## 🚀 Alternative Analytics Tools

### Free Options
- **Plausible** (privacy-focused, $9/month after trial)
- **Matomo** (self-hosted, free)
- **Mixpanel** (event-based, free tier)
- **PostHog** (open-source, free tier)

### Why GA4?
- ✅ Free forever
- ✅ Most popular (industry standard)
- ✅ Powerful features
- ✅ Integrates with Google Ads
- ❌ Complex interface
- ❌ Privacy concerns (GDPR)

### Privacy-Focused Alternative: Plausible

If you care about privacy:
```html
<script defer data-domain="yourdomain.com" 
  src="https://plausible.io/js/script.js"></script>
```

- Lightweight (< 1KB)
- GDPR compliant
- No cookie banner needed
- Simple dashboard
- $9/month (10K pageviews)

---

## 📋 Implementation Checklist

- [ ] Create Google Analytics account
- [ ] Get Measurement ID (G-XXXXXXXXXX)
- [ ] Add tracking code to all pages
- [ ] Test in Realtime view
- [ ] Set up custom events
- [ ] Add conversion goals
- [ ] Create custom dashboard
- [ ] Test with ad blocker disabled
- [ ] Add privacy policy
- [ ] Set data retention period
- [ ] Monitor daily for first week

---

## 💡 Pro Tips

1. **Set up alerts**: Get notified of traffic spikes/drops
2. **Exclude internal traffic**: Filter out your own visits
3. **Track campaign URLs**: Use UTM parameters
4. **Export to BigQuery**: For advanced analysis (free tier available)
5. **Link to Google Ads**: If you run paid ads later

---

## 🔗 Resources

- **GA4 Documentation**: https://support.google.com/analytics
- **GA4 Training**: https://analytics.google.com/analytics/academy/
- **Measurement Protocol**: https://developers.google.com/analytics/devguides/collection/protocol/ga4
- **gtag.js Reference**: https://developers.google.com/tag-platform/gtagjs

---

**Next**: Let me implement this in your app! 🚀

