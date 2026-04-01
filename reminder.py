import os
import requests
from datetime import datetime
import pytz

# ── Config from GitHub Secrets ───────────────────────────────
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID   = os.environ["TELEGRAM_CHAT_ID"]

# ── Get current hour in Eastern Time (Payal's timezone) ─────
eastern = pytz.timezone("America/New_York")
hour    = datetime.now(eastern).hour

# ── Only send between 6 AM and 10 PM ────────────────────────
if hour < 6 or hour > 22:
    print(f"Quiet hours ({hour}:00 ET) — no message sent.")
    exit(0)

# ── Hourly messages ──────────────────────────────────────────
reminders = {
    6: """🌅 *Good Morning, Payal!* — 6:00 AM

▶ Drink 1 glass of *warm water* right now
☀️ Get *15 min sunlight* outside (critical for Vitamin D deficiency!)
💊 Get your supplements ready for breakfast
🧘 Light stretching before exercise

_Triglycerides goal: <150 | Your current: 190 — you're working on it!_""",

    7: """🏃 *Morning Exercise Time!* — 7:00 AM

Today's plan:
• *Mon/Wed/Fri* → 30 min brisk walk
• *Tue/Thu* → Yoga or stretching
• *Sat* → Long 45 min outdoor walk (bonus Vitamin D!)
• *Sun* → Rest day 🛌

💡 Exercise is your #1 tool against insulin resistance (Hyperinsulinemia)""",

    8: """🍳 *Breakfast Time!* — 8:00 AM (~350 cal)

✅ 2 boiled/scrambled eggs (B12 + Vitamin D)
✅ ½ cup GF oats with 1 tbsp flaxseed + 1 tsp chia seeds
✅ ½ cup blueberries or strawberries
✅ 1 cup green tea (no sugar!)

💊 *TAKE SUPPLEMENTS NOW:*
• Vitamin B12 — 1000mcg sublingual (under tongue)
• Vitamin D3 5000 IU + K2 100mcg
• Methylfolate 400mcg

_(Helps fix your high MCV 100.5 — macrocytosis)_""",

    9: """💧 *Hydration Check!* — 9:00 AM

Drink 1 full glass of water RIGHT NOW 🥤
Target for today: *3 liters total*

⚠️ Staying hydrated is critical for your:
• Elevated platelet count (516 — needs to come down)
• Kidney health (eGFR 85 — keep it healthy)
• Constipation (doctor's advice: more water + fiber)""",

    10: """🥜 *Mid-Morning Snack!* — 10:00 AM (~150 cal)

✅ 8 almonds + 4 walnuts
✅ 1 medium apple (with skin)
✅ 1 glass water

💡 *Walnuts are your secret weapon:*
Omega-3 in walnuts directly lowers triglycerides
4 walnuts daily → can reduce triglycerides by 10-15%
Your target: 190 → below 150 mg/dL""",

    11: """🧍 *Stand Up & Stretch!* — 11:00 AM

⏰ You've been sitting — get up for 5 minutes!
• Roll your shoulders, stretch your neck
• Walk to the kitchen and back
• Drink 1 glass of water 🥤

💡 Continuous sitting spikes blood sugar even in active people.
Small movement breaks help your *hyperinsulinemia* significantly.""",

    12: """🥗 *Lunch Time!* — 12:30 PM (~500 cal)

✅ ¾ cup cooked *quinoa* (NOT white rice — raises insulin!)
✅ 1 cup moong dal / masoor dal curry (iron + folate)
✅ 1 cup sautéed *spinach* with garlic + lemon
   _(spinach = folate + iron → fixes your high MCV)_
✅ 1 cup cucumber + carrot + tomato salad
✅ 1 glass plain buttermilk (probiotics + calcium)

❌ No bread, no maida, no gluten anything!""",

    13: """🚶 *POST-LUNCH WALK — Do it NOW!* — 1:00 PM

🔴 This is the MOST important habit for you!

Walk for *10-15 minutes* right after eating.
This single habit:
• Lowers blood sugar spike by up to 30%
• Directly fights your *Hyperinsulinemia*
• Helps lower *Triglycerides* over time

💧 Also drink 1 glass of water before your walk.""",

    14: """💧 *Afternoon Hydration!* — 2:00 PM

Drink 1 glass of water 🥤

How many glasses so far today?
• 2 or fewer → drink 2 glasses now
• 3-4 → you're on track, keep going
• 5+ → great work!

☕ Avoid tea/coffee after 2 PM — caffeine blocks *Vitamin D absorption*
and can worsen *adenomyosis* inflammation.""",

    15: """🥣 *Afternoon Snack!* — 3:00 PM (~150 cal)

✅ ¾ cup plain Greek yogurt (GF) + 1 tbsp pumpkin seeds
   OR
✅ 1 GF rice cake + 1 tbsp almond butter

💊 *TAKE SUPPLEMENT NOW:*
• Omega-3 (algae-based) 1000mg EPA+DHA with food
   → *Most proven supplement for lowering triglycerides*
   → Also anti-inflammatory for adenomyosis pain

❌ No packaged snacks — even "GF" ones are full of sugar!""",

    16: """⚡ *Pre-Workout Prep!* — 4:00 PM

Workout is in 1.5 hours — prepare now:

💧 Drink 2 glasses of water
🍌 If feeling low energy: 5 extra walnuts or ½ banana
👟 Lay out your workout clothes
🎵 Prepare your workout playlist

Today's workout:
• Mon → Upper body strength (dumbbells/bands)
• Wed → Lower body (squats, lunges, glute bridges)
• Fri → Low-impact cardio (cycling/elliptical)
• Tue/Thu → Yoga""",

    17: """💪 *WORKOUT TIME!* — 5:30 PM (45 min)

*Today's Focus:*
• 🏋️ *Mon/Wed* → Strength Training
  _(#1 fix for insulin resistance — builds metabolic muscle)_
• 🧘 *Tue/Thu* → Yoga/Stretching
  _(reduces adenomyosis pain + inflammation)_
• 🚴 *Fri* → Low-impact cardio
  _(raises HDL cholesterol — yours is borderline at 51)_
• 🚶 *Sat* → 45-60 min outdoor walk
  _(sunlight = Vitamin D bonus!)_

You're doing this for your health — let's go! 💥""",

    18: """🥤 *Post-Workout Nutrition!* — 6:30 PM

Eat within *30 minutes* of finishing workout:

✅ Plant-based protein shake (GF, unsweetened)
   OR
✅ 2 boiled eggs + 1 small banana

This window is critical for:
• Muscle recovery
• Blood sugar stabilization
• Preventing evening hunger

💧 Also drink 2 glasses of water — you lost fluids!""",

    19: """🍽️ *Dinner Time!* — 7:00 PM (~450 cal)

✅ 2 small jowar OR bajra rotis (GF millets — NOT wheat!)
✅ ¾ cup rajma / chickpea curry
✅ 1 cup mixed veggies: broccoli + bell pepper + zucchini
✅ ½ cup beet + pomegranate salad (iron + antioxidants)
✅ 1 tsp ghee on roti (helps absorb Vitamin D)

⚠️ *KEEP CARBS LOW AT NIGHT* — critical rule for you!
High carbs at dinner → spikes triglycerides while you sleep.
No rice at dinner. No dessert. No fruit juice.""",

    20: """📊 *Evening Check-In!* — 8:00 PM

Quick daily review:

💧 Water today: Did you reach 3 liters?
☀️ Sunlight: 15 min this morning?
🏃 Exercise: Done today?
🥗 Gluten: Avoided completely?
🍬 Sugar: No sweets or fruit juice?
💊 Supplements: B12 + D3 + Omega-3 + Folate taken?

_Every green check = progress toward lower triglycerides,_
_better insulin levels, and reduced platelet count._""",

    21: """🌙 *Wind-Down Time!* — 9:00 PM

🥛 Drink warm *turmeric + ginger milk* now
   → Curcumin in turmeric is anti-inflammatory
   → Helps with *adenomyosis* pain
   → Reduces platelet aggregation naturally

💊 *TAKE BEFORE BED:*
• Magnesium Glycinate 300mg
  → Reduces adenomyosis cramps
  → Improves sleep quality
  → Boosts insulin sensitivity overnight

📵 Put phone down in 30 minutes — sleep is medicine!""",

    22: """😴 *Bedtime!* — 10:00 PM

Time to sleep, Payal! 🌙

7-8 hours of sleep tonight will:
• Lower cortisol → reduces blood sugar spikes
• Help normalize *triglycerides*
• Support hormonal balance (important for *adenomyosis*)
• Reduce inflammation → helps platelet count

*Tomorrow's first reminder: 6 AM* ☀️

_You're doing great — every healthy choice today_
_is moving you toward better lab results!_ 💪""",
}

default_message = f"""💧 *Hydration Reminder*

Drink 1 glass of water right now! 🥤
Daily target: 3 liters

Quick check:
• Staying gluten-free? ✅
• Avoiding sugar and refined carbs? ✅
• Moving every hour? ✅

_Small consistent habits = big improvements in your next blood report!_"""

# ── Send message ─────────────────────────────────────────────
message = reminders.get(hour, default_message)

url  = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
data = {
    "chat_id":    CHAT_ID,
    "text":       message,
    "parse_mode": "Markdown",
    "disable_web_page_preview": True,
}

response = requests.post(url, data=data)

if response.status_code == 200:
    print(f"Message sent successfully for hour {hour}:00 ET")
else:
    print(f"ERROR: {response.status_code} — {response.text}")
    exit(1)
