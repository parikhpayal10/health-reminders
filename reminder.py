import os
import requests
from datetime import datetime
import pytz

# ── Config from GitHub Secrets ───────────────────────────────
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID   = os.environ["TELEGRAM_CHAT_ID"]

# ── Get current time in Eastern Time (Payal's timezone) ─────
eastern    = pytz.timezone("America/New_York")
now        = datetime.now(eastern)
hour       = now.hour
weekday    = now.weekday()   # 0=Monday, 6=Sunday

# ── Only send between 5 AM and 10 PM ────────────────────────
if hour < 5 or hour > 22:
    print(f"Quiet hours ({hour}:00 ET) — no message sent.")
    exit(0)

# ── Weekly Grocery List — every Sunday at 9 AM ───────────────
GROCERY_LIST = """🛒 *Weekly Grocery List — Payal's Health Plan*

_Shop today so you're set for the whole week!_

🥚 *PROTEINS*
• Eggs (1 dozen)
• Greek yogurt — plain, full fat, GF (2 large tubs)
• Moong dal / Masoor dal (1 lb each)
• Rajma / Kidney beans (1 can or dry)
• Chickpeas / Chana (1 can or dry)
• Plant-based protein powder (GF, unsweetened)

🌾 *GLUTEN-FREE GRAINS*
• Certified GF rolled oats (1 bag)
• Quinoa (1 lb)
• Jowar flour / Bajra flour (for rotis)
• Brown rice (small bag — limit portions)
• GF rice cakes (1 pack)

🥬 *VEGETABLES — Fresh*
• Spinach (2 large bags — iron + folate)
• Broccoli (1 head)
• Zucchini (2)
• Bell peppers — red/yellow/green (3)
• Cucumber (3)
• Carrots (1 bag)
• Tomatoes (4-5)
• Garlic (1 bulb)
• Beets (2-3 fresh or 1 can)

🍎 *FRUITS*
• Blueberries / Strawberries (1 pint)
• Apples (4-5)
• Lemons (3-4)
• Pomegranate (1) or pomegranate seeds (1 pack)
• Bananas (3-4 — for post-workout)

🥜 *NUTS & SEEDS*
• Walnuts (1 bag — Omega-3 for triglycerides!)
• Almonds (1 bag)
• Chia seeds (1 bag)
• Ground flaxseed (1 bag)
• Pumpkin seeds (1 bag — magnesium + zinc)

🧴 *DAIRY*
• Whole milk or almond milk (fortified with D & B12)
• Buttermilk / Chaas (plain, no salt)
• Ghee (small jar)

🌿 *SPICES & PANTRY (check stock)*
• Turmeric powder
• Ginger (fresh or powder)
• Olive oil (for cooking)
• Almond butter (GF, no added sugar)
• Green tea bags

💊 *SUPPLEMENTS — check if running low*
• Vitamin B12 (methylcobalamin 1000mcg)
• Vitamin D3 5000 IU + K2 100mcg
• Omega-3 algae-based 1000mg EPA+DHA
• Magnesium Glycinate 300mg
• Methylfolate 400mcg
• Vitamin C 500mg

❌ *DO NOT BUY*
• Any wheat/gluten products
• White bread, pasta, naan, regular rotis
• Sugary drinks, juice boxes
• Packaged GF cookies/snacks (high sugar)
• Soy milk in large amounts (worsens adenomyosis)

_Estimated budget: $80-100/week for all fresh items_ 🛒"""

# Send grocery list every Sunday at 9 AM
if weekday == 6 and hour == 9:
    url  = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": GROCERY_LIST, "parse_mode": "Markdown", "disable_web_page_preview": True}
    requests.post(url, data=data)
    print("Weekly grocery list sent!")
    exit(0)

# ── Hourly messages ──────────────────────────────────────────
reminders = {
    5: """💪 *WORKOUT TIME!* — 5:00 AM (45 min)

*Today's Focus + Follow Along Videos:*

🏋️ *Mon/Wed* → Strength Training
  Search YouTube: "Caroline Girvan beginner upper body"
  OR: "Sydney Cummings 30 min strength no jumping"
  _(#1 fix for insulin resistance)_

🧘 *Tue/Thu* → Yoga for Pelvic Health
  Search YouTube: "Yoga With Adriene gentle morning yoga"
  OR: "yoga for adenomyosis pain relief"
  _(reduces adenomyosis pain + inflammation)_

🚴 *Fri* → Low-Impact Cardio
  Search YouTube: "Leslie Sansone 30 minute walk at home"
  OR: "low impact cardio no jumping Sydney Cummings"
  _(raises HDL cholesterol — yours is borderline at 51)_

🚶 *Sat* → Outdoor Walk 45-60 min
  No video needed — go outside for Vitamin D bonus! ☀️

🛌 *Sun* → Rest + Light Stretch
  Search YouTube: "Yoga With Adriene Sunday reset"

You're doing this for your health — let's go! 💥""",

    6: """🌅 *Good Morning, Payal!* — 6:00 AM

Great job finishing your workout! Now:
▶ Drink 1 large glass of *warm water* right now
☀️ Get *15 min sunlight* outside (critical for Vitamin D deficiency!)
🚿 Fresh up and get ready for breakfast

_Triglycerides goal: <150 | Your current: 190 — you're working on it!_""",

    7: """🥤 *Post-Workout Nutrition!* — 7:00 AM

Eat within 30 min of finishing workout:

✅ Plant-based protein shake (GF, unsweetened)
   OR
✅ 2 boiled eggs + 1 small banana

This window is critical for:
• Muscle recovery
• Blood sugar stabilization

💧 Drink 2 glasses of water — you lost fluids during workout!""",

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

    9: """💧☕ *Hydration + Chai Time!* — 9:00 AM

✅ Drink 1 full glass of water first 🥤
✅ Now you can have your *Masala Chai!* ☕
   _(1 hour after supplements = safe to drink now)_

*Your health chai recipe:*
• 1 cup water + ½ cup milk (dairy or almond)
• Fresh ginger slices → anti-inflammatory, adenomyosis pain
• Cinnamon stick → improves *insulin sensitivity* directly!
• Cardamom + cloves → antioxidants, anti-platelet
• *NO sugar, NO jaggery, NO honey* ❌

⚠️ Max 1-2 cups per day. No chai after 2 PM.

Target water today: *3 liters total*""",

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

    16: """⏰ *Tomorrow's Workout Prep!* — 4:00 PM

Workout is at *5:00 AM tomorrow!*

💧 Drink 2 glasses of water now
👟 Set out your workout clothes tonight
🎵 Prepare your workout playlist
⏰ Set alarm for *4:45 AM*
🛏️ Aim to sleep by 9:30 PM (7 hrs before 5 AM!)

Tomorrow's workout:
• Mon → Upper body strength (dumbbells/bands)
• Wed → Lower body (squats, lunges, glute bridges)
• Fri → Low-impact cardio (cycling/elliptical)
• Tue/Thu → Yoga""",

    17: """🍽️ *Dinner Time!* — 5:00 PM (~450 cal)

✅ 2 small jowar OR bajra rotis (GF millets — NOT wheat!)
✅ ¾ cup rajma / chickpea curry
✅ 1 cup mixed veggies: broccoli + bell pepper + zucchini
✅ ½ cup beet + pomegranate salad (iron + antioxidants)
✅ 1 tsp ghee on roti (helps absorb Vitamin D)

⚠️ *KEEP CARBS LOW* — critical rule for you!
Eating early dinner helps lower triglycerides and insulin.
No rice. No dessert. No fruit juice.""",

    18: """💧 *Evening Hydration!* — 6:00 PM

Drink 1 glass of water 🥤
Alarm set for 4:45 AM tomorrow for your 5 AM workout? ⏰

    19: """� *Prep for Tomorrow's 5 AM Workout!* — 7:00 PM

✅ Workout clothes laid out?
✅ Water bottle filled and ready?
✅ Alarm set for 4:45 AM?
✅ Supplements organized for breakfast?

💧 Drink 1 glass of water
📵 Reduce screen time — sleep by 9:30 PM
   so you get 7 hrs rest before your 5 AM workout!

_Early morning workout = better insulin control all day!_""",

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
