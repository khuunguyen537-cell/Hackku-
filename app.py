import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh
from streamlit_js_eval import get_geolocation 
from geopy.geocoders import Nominatim  # NEW
from datetime import datetime
from zoneinfo import ZoneInfo
import math                                      # NEW
import random
import urllib.parse
import base64
from pathlib import Path

st.set_page_config(page_title="Schedulémon", layout="centered")

geolocator = Nominatim(user_agent="schedulemon_app")

# ── Font ──────────────────────────────────────────────────────────────────────
def load_pokemon_font():
    with open("Pokemon Solid.ttf", "rb") as f:
        solid = base64.b64encode(f.read()).decode()
    return f"""
    <style>
    @font-face {{
        font-family: 'PokemonSolid';
        src: url(data:font/ttf;base64,{solid}) format('truetype');
    }}
    h1 {{
        font-family: 'PokemonSolid' !important;
        color: #ffcb05;
        text-shadow:
            -3px -3px 0 #2a75bb,
             3px -3px 0 #2a75bb,
            -3px  3px 0 #2a75bb,
             3px  3px 0 #2a75bb;
    }}
    </style>
    """

st.markdown(load_pokemon_font(), unsafe_allow_html=True)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@700;900&family=Luckiest+Guy&display=swap');

html, body, [class*="css"] {
    font-family: 'Fredoka One', 'Nunito', cursive !important;
    color: #5a7fa8 !important;
}
h2, h3, .stSubheader {
    font-family: 'Luckiest Guy', cursive !important;
    color: #ffcb05 !important;
    text-shadow:
        -3px -3px 0 #2a75bb,
         3px -3px 0 #2a75bb,
        -3px  3px 0 #2a75bb,
         3px  3px 0 #2a75bb,
        -6px -6px 0 #2a75bb,
         6px -6px 0 #2a75bb,
        -6px  6px 0 #2a75bb,
         6px  6px 0 #2a75bb,
         0px  8px 0 #1b4f9c,
         2px  9px 0 #1b4f9c,
        -2px  9px 0 #1b4f9c;
}
header[data-testid="stHeader"] { background: #BED9F4 !important; }
.stToolbar, [data-testid="stToolbar"] { background: #BED9F4 !important; }
[data-testid="stToolbar"] button, [data-testid="stToolbar"] * { color: #5a7fa8 !important; }

/* TEXT INPUT WHOLE BOX */
/* TEXT INPUT WHOLE BOX */
[data-testid="stTextInput"] {
    border-radius: 18px !important;
}

[data-testid="stTextInput"] > div {
    background: transparent !important;
    border: none !important;
    border-radius: 18px !important;
    padding: 3px !important;
    box-shadow: none !important;
}

[data-testid="stTextInput"] > div > div {
    background-color: #FFF8B5 !important;
    background-image: none !important;
    border: 2px solid transparent !important;
    border-radius: 14px !important;
    box-shadow: none !important;
    overflow: hidden !important;
}

/* actual text field */
[data-testid="stTextInput"] input {
    background-color: #FFF8B5 !important;
    background-image: none !important;
    color: #222 !important;
    -webkit-text-fill-color: #222 !important;
    font-family: 'Fredoka One', cursive !important;
    box-shadow: none !important;
}

/* placeholder */
[data-testid="stTextInput"] input::placeholder {
    color: #777 !important;
    -webkit-text-fill-color: #777 !important;
}

/* force typed/autofilled text boxes to stay yellow */
[data-testid="stTextInput"] input:not(:placeholder-shown) {
    background-color: #FFF8B5 !important;
    -webkit-text-fill-color: #222 !important;
    color: #222 !important;
    caret-color: #222 !important;
}

[data-testid="stTextInput"] input:-webkit-autofill,
[data-testid="stTextInput"] input:-webkit-autofill:hover,
[data-testid="stTextInput"] input:-webkit-autofill:focus,
[data-testid="stTextInput"] input:-webkit-autofill:active {
    -webkit-box-shadow: 0 0 0 1000px #FFF8B5 inset !important;
    -webkit-text-fill-color: #222 !important;
    caret-color: #222 !important;
    border-radius: 14px !important;
    transition: background-color 9999s ease-in-out 0s;
}

/* focus state: rounded blue border around the yellow box */
[data-testid="stTextInput"] > div:focus-within {
    border: 2px solid #BED9F4 !important;
    border-radius: 18px !important;
    padding: 3px !important;
    box-shadow: none !important;
}

[data-testid="stTextInput"] > div > div:focus-within {
    border: none !important;
    box-shadow: none !important;
}

/* MULTISELECT */
[data-testid="stMultiSelect"] > div {
    background: transparent !important;
    border: none !important;
    border-radius: 18px !important;
    padding: 3px !important;
    box-shadow: none !important;
}

[data-testid="stMultiSelect"] > div > div,
[data-baseweb="select"] > div {
    background-color: #FFF8B5 !important;
    border: 2px solid transparent !important;
    border-radius: 14px !important;
    box-shadow: none !important;
}

/* rounded blue border only when clicked */
[data-testid="stMultiSelect"] > div:focus-within {
    border: 2px solid #BED9F4 !important;
    border-radius: 18px !important;
    padding: 3px !important;
    box-shadow: none !important;
}

[data-testid="stMultiSelect"] > div > div:focus-within,
[data-baseweb="select"] > div:focus-within {
    border: none !important;
    box-shadow: none !important;
}

/* Placeholder text */
[data-baseweb="select"] input::placeholder {
    color: #2a75bb !important;
    -webkit-text-fill-color: #2a75bb !important;
    font-family: 'Luckiest Guy', cursive !important;
    font-size: 16px !important;
    letter-spacing: 1px !important;
}

/* "Choose options" default text shown before typing */
[data-baseweb="select"] [data-testid="stMarkdownContainer"] p,
[data-baseweb="placeholder"] {
    color: #2a75bb !important;
    font-family: 'Luckiest Guy', cursive !important;
    font-size: 16px !important;
    letter-spacing: 1px !important;
}
            
/* text inside multiselect */
[data-baseweb="select"] span,
[data-baseweb="select"] div {
    color: #2a75bb !important;
    -webkit-text-fill-color: #2a75bb !important;
    font-family: 'Luckiest Guy', cursive !important;
    letter-spacing: 0.5px !important;
}

/* dropdown menu */
ul[role="listbox"] {
    background-color: #FFF8B5 !important;
    background-image: none !important;
    border: 3px solid #ffcb05 !important;
    border-radius: 16px !important;
    padding: 6px !important;
    box-shadow: 0 8px 24px rgba(42,117,187,0.15) !important;
    overflow: hidden !important;
}

/* dropdown options */
li[role="option"] {
    background-color: #FFF8B5 !important;
    color: #2a75bb !important;
    font-family: 'Luckiest Guy', cursive !important;
    font-size: 18px !important;
    letter-spacing: 1px !important;
    padding: 10px 16px !important;
    border-bottom: 1px solid rgba(190,217,244,0.4) !important;
    transition: background 0.15s !important;
}

li[role="option"]:hover {
    background-color: #BED9F4 !important;
    color: #1b4f9c !important;
}

li[role="option"][aria-selected="true"] {
    background-color: #ffcb05 !important;
    color: #1b4f9c !important;
}

/* selected day tags */
[data-baseweb="tag"] {
    background-color: #BED9F4 !important;
    color: #222 !important;
    border-radius: 10px !important;
}

/* labels */
/* FORCE ALL FORM LABELS */
label, 
[data-testid="stTextInput"] label,
[data-testid="stMultiSelect"] label,
[data-testid="stForm"] label,
[data-testid="stTextInput"] p,
[data-testid="stMultiSelect"] p {
    color: #5a7fa8 !important;
    font-family: 'Luckiest Guy', cursive !important;
    font-size: 18px !important;
    letter-spacing: 0px !important;
}
.stButton > button {
    background-color: #FEFDD0 !important;
    color: #222 !important;
    border: 2px solid #BED9F4 !important;
    border-radius: 14px !important;
    font-family: 'Luckiest Guy', cursive !important;
    font-size: 18px !important;
    box-shadow: none !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background-color: #FFF8B5 !important;
    border: 2px solid #ffcb05 !important;
    transform: scale(1.05);
}

.stButton > button:active {
    transform: scale(0.97);
}
/* ADD CLASS BUTTON (inside form) */
[data-testid="stForm"] button,
[data-testid="stForm"] button * {
    background-color: #FEFDD0 !important;
    color: #222 !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: 'Luckiest Guy', cursive !important;
    font-size: 18px !important;
    box-shadow: none !important;
}

[data-testid="stForm"] button:hover {
    background-color: #FFF8B5 !important;
    border: 2px solid #ffcb05 !important;
    transform: scale(1.05);
}

[data-testid="stForm"] button:active {
    transform: scale(0.97);
}
/* ✨ EDIT PANEL ANIMATION */
.edit-panel {
    animation: fadeSlide 0.3s ease-out;
}

@keyframes fadeSlide {
    from {
        opacity: 0;
        transform: translateY(-12px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
            
/* SHARE TEXT BOX */
[data-testid="stCodeBlock"] {
    border-radius: 18px !important;
}

[data-testid="stCodeBlock"] pre {
    background-color: #FEFDD0 !important;
    color: #5a7fa8 !important;
    border: 2px solid #BED9F4 !important;
    border-radius: 16px !important;
    font-family: 'Fredoka One', cursive !important;
    font-size: 15px !important;
    white-space: pre-wrap !important;
    word-break: break-word !important;
    padding: 14px 16px !important;
    box-shadow: none !important;
}

[data-testid="stCodeBlock"] code {
    color: #5a7fa8 !important;
    background: transparent !important;
    font-family: 'Fredoka One', cursive !important;
}

[data-testid="stCodeBlock"] pre:focus,
[data-testid="stCodeBlock"] pre:focus-visible {
    outline: none !important;
    border: 2px solid #BED9F4 !important;
    box-shadow: 0 0 0 3px #FEFDD0 !important;
}

/* in case Streamlit adds inner wrappers */
[data-testid="stCodeBlock"] div {
    color: #5a7fa8 !important;
    font-family: 'Fredoka One', cursive !important;
}
            
/* SHARE EXPANDER */
[data-testid="stExpander"] {
    border: 2px solid #BED9F4 !important;
    border-radius: 18px !important;
    background: #FEFDD0 !important;
    overflow: hidden !important;
}

[data-testid="stExpander"] details {
    background: #FEFDD0 !important;
    border-radius: 18px !important;
}

[data-testid="stExpander"] summary {
    background: #FEFDD0 !important;
    color: #5a7fa8 !important;
    font-family: 'Luckiest Guy', cursive !important;
    font-size: 20px !important;
    border-radius: 18px !important;
    padding: 12px 16px !important;
}

[data-testid="stExpander"] summary p {
    color: #5a7fa8 !important;
    font-family: 'Luckiest Guy', cursive !important;
    font-size: 20px !important;
    margin: 0 !important;
    line-height: 1.2 !important;
}

[data-testid="stExpander"] summary svg {
    color: #5a7fa8 !important;
    fill: #5a7fa8 !important;
    width: 1rem !important;
    height: 1rem !important;
    flex-shrink: 0 !important;
    margin-right: 8px !important;
}

[data-testid="stExpander"] summary > div {
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
}

[data-testid="stExpander"] summary:hover {
    background: #FFF8B5 !important;
}
/* SHARE TEXT DISPLAY */
[data-testid="stCodeBlock"] {
    border-radius: 16px !important;
}

[data-testid="stCodeBlock"] pre {
    background: #FEFDD0 !important;
    color: #5a7fa8 !important;
    border: 2px solid #BED9F4 !important;
    border-radius: 16px !important;
    font-family: 'Fredoka One', cursive !important;
    font-size: 15px !important;
    white-space: pre-wrap !important;
    word-break: break-word !important;
    padding: 14px 16px !important;
    box-shadow: none !important;
}

[data-testid="stCodeBlock"] code {
    color: #5a7fa8 !important;
    background: transparent !important;
    font-family: 'Fredoka One', cursive !important;
}

[data-testid="stCodeBlock"] pre:focus,
[data-testid="stCodeBlock"] pre:focus-visible {
    outline: none !important;
    border: 2px solid #BED9F4 !important;
    box-shadow: none !important;
}

/* LINK BUTTONS + DOWNLOAD BUTTONS */
[data-testid="stLinkButton"] a,
[data-testid="stDownloadButton"] button {
    background: #FEFDD0 !important;
    color: #5a7fa8 !important;
    border: 2px solid #BED9F4 !important;
    border-radius: 14px !important;
    font-family: 'Luckiest Guy', cursive !important;
    font-size: 18px !important;
    box-shadow: none !important;
    text-decoration: none !important;
    transition: all 0.2s ease !important;
}

[data-testid="stLinkButton"] a:hover,
[data-testid="stDownloadButton"] button:hover {
    background: #FFF8B5 !important;
    color: #5a7fa8 !important;
    border: 2px solid #ffcb05 !important;
    transform: scale(1.03);
}

[data-testid="stLinkButton"] a:visited,
[data-testid="stLinkButton"] a:active,
[data-testid="stLinkButton"] a:focus,
[data-testid="stDownloadButton"] button:focus,
[data-testid="stDownloadButton"] button:focus-visible {
    color: #5a7fa8 !important;
    outline: none !important;
    box-shadow: none !important;
}

/* make inner text inherit blue */
[data-testid="stLinkButton"] a *,
[data-testid="stDownloadButton"] button * {
    color: #5a7fa8 !important;
    font-family: 'Luckiest Guy', cursive !important;
}
     /* SIDEBAR RADIO LABELS */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span p,
[data-testid="stSidebar"] .stRadio label {
    font-family: 'Luckiest Guy', cursive !important;
    color: #5a7fa8 !important;
    font-size: 18px !important;
    letter-spacing: 1px !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    font-family: 'Luckiest Guy', cursive !important;
    color: #5a7fa8 !important;
}   
</style>
""", unsafe_allow_html=True)
# ── Session State ─────────────────────────────────────────────────────────────
defaults = {
    "checked_in": False,
    "selected_course": None,
    "cards": [],
    "streaks": {},
    "check_in_time": None,
    "pending_reward": None,
    "gps_verified": False, 
    "editing_index": None,     # NEW — tracks whether GPS passed for this attempt
    "schedule": [
        {"course": "CHEM 135", "day": "Saturday", "start": "00:00", "end": "18:00",
         "location": "Demo Hall",    "lat": 38.9541, "lon": -95.2558, "radius": 80},
        {"course": "MATH 125", "day": "Friday",   "start": "11:00", "end": "12:15",
         "location": "Math Building","lat": 38.9555, "lon": -95.2520, "radius": 80},
        {"course": "BIOL 240", "day": "Friday",   "start": "14:00", "end": "14:50",
         "location": "Bio Room 101", "lat": 38.9530, "lon": -95.2545, "radius": 80},
    ],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

schedule = st.session_state.schedule
for cls in schedule:
    if cls["course"] not in st.session_state.streaks:
        st.session_state.streaks[cls["course"]] = 0

# ── GPS Helpers ───────────────────────────────────────────────────────────────
def haversine_distance(lat1, lon1, lat2, lon2):
    """Returns distance in metres between two GPS coordinates."""
    R = 6_371_000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi    = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.asin(math.sqrt(a))

def get_class_info(course_name):
    for cls in schedule:
        if cls["course"] == course_name:
            return cls
    return None

def is_user_at_hall(user_lat, user_lon, course_name):
    """Returns (bool, distance_in_metres). Skips check if no coords stored."""
    cls = get_class_info(course_name)
    if not cls or "lat" not in cls:
        return True, 0
    dist = haversine_distance(user_lat, user_lon, cls["lat"], cls["lon"])
    return dist <= cls.get("radius", 80), round(dist)

def geocode_location_name(location_name):
    try:
        result = geolocator.geocode(location_name)
    
        if result:
            return result.latitude, result.longitude
        return None, None
    except Exception:
        return None, None
    else:
        st.warning("Couldn't find that location — try being more specific (e.g. include city or university name).")

# ── Schedule / Card Logic ─────────────────────────────────────────────────────
RARITY_CHANCES = {
    "Common": 600, "Uncommon": 250, "Rare": 100,
    "Double Rare": 35, "Illustration Rare": 9,
    "Ultra Rare": 6, "Special Illustration Rare": 3,
}

def pull_random_card():
    rarities = list(RARITY_CHANCES.keys())
    weights  = list(RARITY_CHANCES.values())
    rarity   = random.choices(rarities, weights=weights, k=1)[0]
    name_map = {
        "Common": "Lecture Starter Card", "Uncommon": "Steady Learner Card",
        "Rare": "Focused Scholar Card",   "Double Rare": "Double Grind Card",
        "Ultra Rare": "Ultra Focus Card", "Illustration Rare": "Showcase Scholar Card",
        "Special Illustration Rare": "Master Collector Card",
    }
    return {"name": name_map[rarity], "rarity": rarity}

def is_class_active(course_name):
    now = datetime.now(ZoneInfo("America/Chicago"))
    current_day = now.strftime("%A")
    current_time = now.time()

    for cls in schedule:
        if cls["course"] == course_name:
            try:
                start_time = datetime.strptime(cls["start"].strip(), "%H:%M").time()
                end_time = datetime.strptime(cls["end"].strip(), "%H:%M").time()
            except ValueError:
                return False

            days = cls.get("days") or [cls.get("day", "").strip()]
            days = [d.strip() for d in days if d.strip()]

            if start_time <= end_time:
                return current_day in days and start_time <= current_time <= end_time
            else:
                return current_day in days and (current_time >= start_time or current_time <= end_time)

    return False

CARD_LIBRARY = {
    "Common":                    [f"151/common/c{i}.png"  for i in range(1, 7)],
    "Uncommon":                  [f"151/uncommon/u{i}.png" for i in range(1, 10)],
    "Rare":                      [f"151/rare/r{i}.png"    for i in range(1, 6)],
    "Double Rare":               [f"151/dr/dr{i}.png"     for i in range(1, 7)],
    "Illustration Rare":         [f"151/ir/ir{i}.png"     for i in range(1, 9)],
    "Ultra Rare":                [f"151/ur/ur{i}.png"     for i in range(1, 6)],
    "Special Illustration Rare": [f"151/sir/sir{i}.png"   for i in range(1, 6)],
}
RARITY_LABELS = {
    "Common": "common", "Uncommon": "uncommon", "Rare": "rare",
    "Double Rare": "dr", "Illustration Rare": "ir",
    "Ultra Rare": "ur", "Special Illustration Rare": "sir",
}

def build_streak_share_text():
    if not st.session_state.streaks:
        return "I'm building my class streaks on Schedulémon!"
    
    parts = []
    for course, streak in st.session_state.streaks.items():
        parts.append(f"{course}: {streak}")
    
    streak_text = " | ".join(parts)
    return f"🔥 My Schedulémon streaks: {streak_text} 🎓⚡"

def build_collection_share_text():
    total_cards = len(st.session_state.cards)
    if total_cards == 0:
        return "I just started my Schedulémon collection!"
    
    rarity_counts = {}
    for card in st.session_state.cards:
        rarity = card["rarity"]
        rarity_counts[rarity] = rarity_counts.get(rarity, 0) + 1
    
    rarity_text = ", ".join([f"{k}: {v}" for k, v in rarity_counts.items()])
    return f"🎴 My Schedulémon collection: {total_cards} cards collected! ({rarity_text}) #Schedulémon #StudyGame"

def social_share_links(text):
    encoded = urllib.parse.quote(text)
    return {
        "x": f"https://twitter.com/intent/tweet?text={encoded}",
        "facebook": f"https://www.facebook.com/sharer/sharer.php?u=&quote={encoded}",
        "whatsapp": f"https://wa.me/?text={encoded}",
        "telegram": f"https://t.me/share/url?url=&text={encoded}"
    }

def render_share_buttons(text, key_suffix):
    links = social_share_links(text)

    is_collection = text.startswith("🎴") or "cards collected" in text or "just started" in text

    clean = text
    for prefix in ["🔥 My Schedulémon streaks: ", "🎴 My Schedulémon collection: "]:
        if clean.startswith(prefix):
            clean = clean[len(prefix):]
    for suffix in [" 🎓⚡", " #Schedulémon #StudyGame"]:
        clean = clean.replace(suffix, "")

    if is_collection:
        total = len(st.session_state.cards)
        rarity_counts = {}
        for card in st.session_state.cards:
            r = card["rarity"]
            rarity_counts[r] = rarity_counts.get(r, 0) + 1

        card_rows = "".join(f"""
<div style="display:flex;justify-content:space-between;align-items:center;
            background:rgba(255,255,255,0.55);border-radius:12px;
            padding:10px 16px;border:1.5px solid rgba(255,203,5,0.35);margin-bottom:8px;">
    <span style="font-family:'Fredoka One',cursive;font-size:17px;color:#2a75bb;">{rarity}</span>
    <span style="font-family:'Fredoka One',cursive;font-size:17px;color:#e67e00;">🎴 {count}</span>
</div>""" for rarity, count in rarity_counts.items()) if rarity_counts else """
<div style="background:rgba(255,255,255,0.55);border-radius:12px;padding:14px 16px;
            border:1.5px solid rgba(255,203,5,0.35);text-align:center;
            font-family:'Fredoka One',cursive;font-size:16px;color:#2a75bb;">
    Just getting started! 🎴
</div>"""

        rows_html = f"""
<div style="display:flex;justify-content:space-between;align-items:center;
            background:rgba(255,255,255,0.55);border-radius:12px;
            padding:10px 16px;border:1.5px solid rgba(255,203,5,0.35);margin-bottom:8px;">
    <span style="font-family:'Fredoka One',cursive;font-size:17px;color:#2a75bb;">Total cards</span>
    <span style="font-family:'Fredoka One',cursive;font-size:17px;color:#e67e00;">🎴 {total}</span>
</div>{card_rows}"""
        header_label = "Share my collection"
        subheader = "My Schedulémon Collection"

    else:
        streak_lines = []
        for part in clean.split(" | "):
            part = part.strip()
            if ":" in part:
                course, count = part.split(":", 1)
                streak_lines.append((course.strip(), count.strip()))

        def flame_html(count_str):
            try:
                n = int(count_str.strip())
            except ValueError:
                n = 0
            css_class = "flame-active" if n > 0 else "flame-base"
            return f'<span class="{css_class}">🔥</span>'

        rows_html = "".join(f"""
<div style="display:flex;justify-content:space-between;align-items:center;
            background:rgba(255,255,255,0.55);border-radius:12px;
            padding:10px 16px;border:1.5px solid rgba(255,203,5,0.35);margin-bottom:8px;">
    <span style="font-family:'Fredoka One',cursive;font-size:17px;color:#2a75bb;">{c}</span>
    <span style="font-family:'Fredoka One',cursive;font-size:17px;color:#e67e00;display:flex;align-items:center;gap:6px;">
        {flame_html(n)} {n}
    </span>
</div>""" for c, n in streak_lines)

        header_label = "Share my streaks"
        subheader = "My Schedulémon streaks"

    flame_style = """
<style>
@keyframes flicker {
    0%   { transform: scale(1) rotate(-2deg); opacity: 1; }
    25%  { transform: scale(1.15) rotate(2deg); opacity: 0.9; }
    50%  { transform: scale(0.95) rotate(-1deg); opacity: 1; }
    75%  { transform: scale(1.1) rotate(1deg); opacity: 0.85; }
    100% { transform: scale(1) rotate(-2deg); opacity: 1; }
}
@keyframes flare {
    0%   { transform: scale(1); filter: brightness(1); }
    50%  { transform: scale(1.5); filter: brightness(1.4); }
    100% { transform: scale(1); filter: brightness(1); }
}
.flame-base {
    display:inline-block;
    font-size:20px;
    animation:flicker 1.2s ease-in-out infinite;
    transform-origin:bottom center;
}
.flame-active {
    animation:flicker 1.2s ease-in-out infinite, flare 0.6s ease-out 1;
    transform-origin:bottom center;
}
</style>
"""

    share_box_html = f"""{flame_style}
<div style="background:#FFF8B5;border:3px solid #ffcb05;border-radius:22px;
            padding:22px 24px 18px;font-family:'Fredoka One',cursive;">
    <div style="font-size:12px;letter-spacing:2px;text-transform:uppercase;
                color:#2a75bb;margin-bottom:10px;">{header_label}</div>
    <div style="font-size:13px;color:#b8a000;margin-bottom:12px;">{subheader}</div>
    {rows_html}
</div>
<div style="margin-bottom:14px;"></div>
"""

    st.markdown(share_box_html, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.link_button("Share on X", links["x"], use_container_width=True)
    with col2:
        st.link_button("Facebook", links["facebook"], use_container_width=True)
    with col3:
        st.link_button("WhatsApp", links["whatsapp"], use_container_width=True)
    with col4:
        st.link_button("Telegram", links["telegram"], use_container_width=True)

    st.download_button(
        "⬇ Download share text",
        data=text,
        file_name=f"schedulemon_share_{key_suffix}.txt",
        mime="text/plain",
        use_container_width=True,
        key=f"download_share_{key_suffix}"
    )# ── CSS / JS ──────────────────────────────────────────────────────────────────
CARD_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Nunito:wght@400;700;900&display=swap');

.card-inner { display:flex;justify-content:center;align-items:center;overflow:hidden;padding:0; }
.pokemon-sprite { width:100%;height:100%;object-fit:cover;transition:transform 0.3s;filter:none !important; }
.cards-grid { display:flex;flex-wrap:wrap;gap:2rem;justify-content:center;padding:1rem 0 2rem; }
.card-wrap { perspective:900px;cursor:pointer; }
.card { width:200px;height:300px;border-radius:18px;position:relative;transform-style:preserve-3d;transition:transform 0.15s ease;user-select:none; }
.card-inner { width:100%;height:100%;border-radius:18px;padding:14px;display:flex;flex-direction:column;position:relative;overflow:hidden;border:2px solid transparent; }
.card-inner::before { content:'';position:absolute;inset:0;border-radius:18px;opacity:0;transition:opacity 0.3s;pointer-events:none;z-index:10;mix-blend-mode:screen; }
.card-wrap:hover .card-inner::before { opacity:1;animation:shimmerPink 1.6s linear infinite; }
@keyframes shimmerPink {
    0%   { background:linear-gradient(120deg,rgba(255,255,255,0) 25%,rgba(255,182,222,0.18) 45%,rgba(255,255,255,0.28) 50%,rgba(255,105,180,0.16) 55%,rgba(255,255,255,0) 75%);background-position:0% 0%; }
    100% { background:linear-gradient(120deg,rgba(255,255,255,0) 25%,rgba(255,182,222,0.18) 45%,rgba(255,255,255,0.28) 50%,rgba(255,105,180,0.16) 55%,rgba(255,255,255,0) 75%);background-position:100% 100%; }
}
.pokemon-sprite { width:100%;height:100%;object-fit:cover;border-radius:18px;box-shadow:0 0 12px rgba(255,182,222,0.35),0 0 24px rgba(255,105,180,0.25),0 0 40px rgba(255,105,180,0.15); }
.card-common .card-inner::after {
    content:"";position:absolute;inset:0;border-radius:16px;pointer-events:none;
    background:radial-gradient(circle at 18% 22%,rgba(255,255,255,0.30) 0 1.5px,transparent 2px),radial-gradient(circle at 82% 18%,rgba(255,192,203,0.28) 0 1.5px,transparent 2px),radial-gradient(circle at 74% 74%,rgba(255,255,255,0.22) 0 1.5px,transparent 2px),radial-gradient(circle at 28% 78%,rgba(255,182,193,0.26) 0 1.5px,transparent 2px),linear-gradient(135deg,rgba(255,255,255,0.06),rgba(255,105,180,0.06),rgba(255,255,255,0.02));
    opacity:0.95;animation:pinkFoilTwinkle 2.8s ease-in-out infinite;mix-blend-mode:screen;
}
.card-common .pokemon-sprite { filter:drop-shadow(0 0 2px rgba(255,255,255,0.18)) drop-shadow(0 0 8px rgba(255,105,180,0.14)) !important; }
@keyframes pinkFoilTwinkle { 0%,100%{opacity:0.72;transform:scale(1)} 50%{opacity:1;transform:scale(1.01)} }

.card-uncommon .card-inner { background:linear-gradient(160deg,#1b2e1b,#2f5a2f,#1a3d1a);border-color:#66bb6a;box-shadow:0 0 18px rgba(102,187,106,0.35),0 8px 32px rgba(0,0,0,0.6); }
.card-uncommon .rarity-badge { background:#66bb6a;color:#fff; }
.card-uncommon .pokemon-sprite { filter:drop-shadow(0 0 8px #66bb6a); }

.card-double-rare .card-inner { background:linear-gradient(160deg,#1e123a,#35205f,#180d33);border-color:#9575cd;box-shadow:0 0 24px rgba(149,117,205,0.45),0 8px 32px rgba(0,0,0,0.7); }
.card-double-rare .rarity-badge { background:linear-gradient(90deg,#7e57c2,#9575cd);color:#fff; }
.card-double-rare .pokemon-sprite { filter:drop-shadow(0 0 10px #b39ddb); }

.card-ultra-rare .card-inner { background:linear-gradient(160deg,#3a2a00,#6b4f00,#2b1f00);border-color:#ffca28;box-shadow:0 0 28px rgba(255,202,40,0.5),0 8px 32px rgba(0,0,0,0.75); }
.card-ultra-rare .rarity-badge { background:linear-gradient(90deg,#f9a825,#ffca28);color:#1a1a1a; }
.card-ultra-rare .pokemon-sprite { filter:drop-shadow(0 0 12px #ffd54f); }

.card-illustration-rare .card-inner { background:linear-gradient(160deg,#10243d,#1f4b5f,#3d1f52);border-color:#4dd0e1;box-shadow:0 0 28px rgba(77,208,225,0.35),0 0 40px rgba(244,143,177,0.18),0 8px 32px rgba(0,0,0,0.75); }
.card-illustration-rare .rarity-badge { background:linear-gradient(90deg,#26c6da,#ec407a);color:#fff; }
.card-illustration-rare .pokemon-sprite { filter:drop-shadow(0 0 12px #80deea); }

.card-special-illustration-rare .card-inner { background:linear-gradient(160deg,#24103d,#4a1f5f,#5f2a3d,#1f3f5f);border-color:#ff80ab;box-shadow:0 0 34px rgba(255,128,171,0.45),0 0 60px rgba(255,241,118,0.18),0 8px 32px rgba(0,0,0,0.82); }
.card-special-illustration-rare .card-inner::after { content:'';position:absolute;inset:0;border-radius:16px;background:linear-gradient(135deg,rgba(255,255,255,0.05) 0%,rgba(255,241,118,0.08) 35%,rgba(255,128,171,0.08) 70%,rgba(179,157,219,0.08) 100%);pointer-events:none;animation:epicPulse 3s ease-in-out infinite; }
.card-special-illustration-rare .rarity-badge { background:linear-gradient(90deg,#ff80ab,#fff176,#b39ddb);color:#1a1a1a;font-weight:900; }
.card-special-illustration-rare .pokemon-sprite { filter:drop-shadow(0 0 14px #fff59d) drop-shadow(0 0 8px #f8bbd0); }
@keyframes epicPulse { 0%,100%{opacity:0.85} 50%{opacity:1} }

.card-header { display:flex;justify-content:space-between;align-items:center;padding-bottom:10px;border-bottom:1px solid;margin-bottom:12px; }
.rarity-badge { font-size:9px;font-weight:900;letter-spacing:1.5px;text-transform:uppercase;padding:3px 9px;border-radius:20px; }
.stats { margin-top:auto;display:flex;flex-direction:column;gap:4px; }
.stat-row { display:flex;justify-content:space-between;font-size:10px;color:rgba(255,255,255,0.5);padding:3px 6px;border-radius:6px;background:rgba(0,0,0,0.2); }
.stat-row span:last-child { font-weight:700; }
.bottom-glow { position:absolute;bottom:0;left:0;right:0;height:80px;border-radius:0 0 18px 18px;pointer-events:none; }
.sparkle { display:none;position:absolute;top:0;left:0;right:0;bottom:0;pointer-events:none;z-index:5; }
.sparkle span { position:absolute;width:4px;height:4px;border-radius:50%;background:white;animation:float 2s ease-in-out infinite; }
@keyframes float { 0%,100%{transform:translateY(0) scale(1);opacity:0.8} 50%{transform:translateY(-6px) scale(1.4);opacity:0.3} }
</style>
"""

CARD_JS = """
<script>
document.querySelectorAll('.card-wrap').forEach(wrap => {
    wrap.addEventListener('mousemove', e => {
        const rect = wrap.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;
        wrap.querySelector('.card').style.transform =
            `rotateY(${x * 12}deg) rotateX(${-y * 10}deg) translateY(-8px)`;
    });
    wrap.addEventListener('mouseleave', () => {
        wrap.querySelector('.card').style.transform = 'translateY(0px)';
    });
});
</script>
"""

RUNNING_POKEMON_HTML = """
<style>
.poke-runner { position:fixed;bottom:60px;width:64px;height:64px;image-rendering:pixelated;z-index:0;pointer-events:none;animation:runAcross linear infinite;opacity:0.55; }
@keyframes runAcross {
    0%   { left:-80px;  transform:scaleX(1);  }
    49%  { left:110%;   transform:scaleX(1);  }
    50%  { left:110%;   transform:scaleX(-1); }
    99%  { left:-80px;  transform:scaleX(-1); }
    100% { left:-80px;  transform:scaleX(1);  }
}
.poke-1{bottom:50px; animation-duration:9s;  animation-delay:0s;}
.poke-2{bottom:120px;animation-duration:13s; animation-delay:-4s;}
.poke-3{bottom:200px;animation-duration:17s; animation-delay:-8s;}
.poke-4{bottom:280px;animation-duration:11s; animation-delay:-2s;}
.poke-5{bottom:350px;animation-duration:15s; animation-delay:-6s;}
body,.stApp{
    background:linear-gradient(180deg,#BED9F4 0%,#FEFDD0 100%) !important;
}
.stApp::before{content:'';position:fixed;inset:0;background-image:radial-gradient(circle,rgba(255,255,255,0.03) 1px,transparent 1px);background-size:40px 40px;pointer-events:none;z-index:0;}
</style>
<img class="poke-runner poke-1" src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png"  alt=""/>
<img class="poke-runner poke-2" src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/39.png"  alt=""/>
<img class="poke-runner poke-3" src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/133.png" alt=""/>
<img class="poke-runner poke-4" src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/52.png"  alt=""/>
<img class="poke-runner poke-5" src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/129.png" alt=""/>
"""
st.markdown(RUNNING_POKEMON_HTML, unsafe_allow_html=True)

# ── Image helpers ─────────────────────────────────────────────────────────────
def image_to_base64(image_path):
    path = Path(image_path)
    if not path.exists():
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def get_back_card_base64():
    path = Path("back.png")
    if not path.exists():
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# ── Card builders ─────────────────────────────────────────────────────────────
CSS_CLASS_MAP = {
    "Common":                    ("card-common",                   "#f0a0c0", "rgba(240,160,192,0.4)"),
    "Uncommon":                  ("card-uncommon",                 "#66bb6a", "rgba(102,187,106,0.4)"),
    "Rare":                      ("card-rare",                     "#90caf9", "rgba(144,202,249,0.4)"),
    "Double Rare":               ("card-double-rare",              "#9575cd", "rgba(149,117,205,0.4)"),
    "Ultra Rare":                ("card-ultra-rare",               "#ffca28", "rgba(255,202,40,0.4)"),
    "Illustration Rare":         ("card-illustration-rare",        "#4dd0e1", "rgba(77,208,225,0.4)"),
    "Special Illustration Rare": ("card-special-illustration-rare","#ff80ab", "rgba(255,128,171,0.4)"),
}

def build_card_back_html():
    back_b64 = get_back_card_base64()
    img_tag  = (f'<img src="data:image/webp;base64,{back_b64}" style="width:100%;height:100%;object-fit:cover;border-radius:14px;"/>'
                if back_b64 else '<div style="background:#1a3a6b;width:100%;height:100%;border-radius:14px;"></div>')
    return f"""
    <div class="card-wrap">
      <div class="card" style="border-radius:18px;">
        <div class="card-inner" style="padding:0;">{img_tag}</div>
      </div>
    </div>
    """

def build_card_html_with_image(card):
    """Flip card: starts face-down (back). Click once → flips to front. Click again → modal."""
    css_class, border_color, glow_color = CSS_CLASS_MAP.get(card["rarity"], CSS_CLASS_MAP["Common"])
    image_b64 = image_to_base64(card["image"])
    back_b64  = get_back_card_base64()
    card_id   = f"card_{random.randint(10000, 99999)}"

    front_img = (f'<img src="data:image/png;base64,{image_b64}" style="width:94%;height:94%;object-fit:cover;border-radius:14px;"/>'
                 if image_b64 else '<div style="color:white;padding:20px;">Image not found</div>')
    back_img  = (f'<img src="data:image/webp;base64,{back_b64}" style="width:100%;height:100%;object-fit:cover;border-radius:12px;"/>'
                 if back_b64 else '<div style="background:#1a3a6b;width:100%;height:100%;border-radius:14px;"></div>')

    return f"""
    <style>
    .flip-container-{card_id}{{perspective:1000px;width:200px;height:300px;cursor:pointer;}}
    .flipper-{card_id}{{width:100%;height:100%;position:relative;transform-style:preserve-3d;transform:rotateY(180deg);transition:transform 0.8s ease;}}
    .flipper-{card_id}.flipped{{transform:rotateY(0deg);}}
    .card-face-{card_id}{{position:absolute;width:100%;height:100%;border-radius:18px;backface-visibility:hidden;-webkit-backface-visibility:hidden;}}
    .card-front-{card_id}{{transform:rotateY(0deg);border:6px solid {border_color};box-shadow:0 0 12px {glow_color},0 0 24px {glow_color};border-radius:18px;display:flex;align-items:center;justify-content:center;overflow:hidden;}}
    .card-back-{card_id}{{transform:rotateY(180deg);border-radius:18px;overflow:hidden;}}
    </style>

    <div class="flip-container-{card_id}"
         onclick="var f=document.getElementById('flipper-{card_id}');
                  if(!f.classList.contains('flipped')){{f.classList.add('flipped');}}
                  else{{document.getElementById('modal-{card_id}').style.display='flex';}}">
      <div id="flipper-{card_id}" class="flipper-{card_id}">
        <div class="card-face-{card_id} card-front-{card_id} card {css_class}">{front_img}</div>
        <div class="card-face-{card_id} card-back-{card_id}">{back_img}</div>
      </div>
    </div>

    <div id="modal-{card_id}" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.6);z-index:9999;justify-content:center;align-items:center;" onclick="this.style.display='none'">
      <div style="background:#FEFDD0;border-radius:20px;padding:28px;max-width:320px;width:90%;border:3px solid {border_color};box-shadow:0 0 30px {glow_color};text-align:center;" onclick="event.stopPropagation()">
        <img src="data:image/png;base64,{image_b64}" style="width:180px;border-radius:12px;margin-bottom:16px;"/>
        <div style="font-family:'Luckiest Guy',cursive;font-size:20px;color:#5a7fa8;margin-bottom:8px;">{card['rarity']}</div>
        <div style="font-family:'Fredoka One',cursive;font-size:16px;color:#8ab4d4;">Course: {card['course']}</div>
        <div style="margin-top:16px;font-family:'Fredoka One',cursive;font-size:13px;color:#aac4d8;">Tap outside to close</div>
      </div>
    </div>
    """

def build_card_html_revealed(card):
    """Already-flipped card for collection page. Click = modal."""
    css_class, border_color, glow_color = CSS_CLASS_MAP.get(card["rarity"], CSS_CLASS_MAP["Common"])
    image_b64 = image_to_base64(card["image"])
    card_id   = f"card_{random.randint(10000, 99999)}"
    front_img = (f'<img src="data:image/png;base64,{image_b64}" style="width:94%;height:94%;object-fit:cover;border-radius:14px;"/>'
                 if image_b64 else '<div style="color:white;padding:20px;">Image not found</div>')
    return f"""
    <div class="card-wrap" onclick="document.getElementById('modal-{card_id}').style.display='flex'">
      <div class="card {css_class}" style="border:6px solid {border_color};box-shadow:0 0 12px {glow_color},0 0 24px {glow_color};border-radius:18px;display:flex;align-items:center;justify-content:center;overflow:hidden;">
        {front_img}
      </div>
    </div>
    <div id="modal-{card_id}" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.6);z-index:9999;justify-content:center;align-items:center;" onclick="this.style.display='none'">
      <div style="background:#FEFDD0;border-radius:20px;padding:28px;max-width:320px;width:90%;border:3px solid {border_color};box-shadow:0 0 30px {glow_color};text-align:center;" onclick="event.stopPropagation()">
        <img src="data:image/png;base64,{image_b64}" style="width:180px;border-radius:12px;margin-bottom:16px;"/>
        <div style="font-family:'Luckiest Guy',cursive;font-size:20px;color:#5a7fa8;margin-bottom:8px;">{card['rarity']}</div>
        <div style="font-family:'Fredoka One',cursive;font-size:16px;color:#8ab4d4;">Course: {card['course']}</div>
        <div style="margin-top:16px;font-family:'Fredoka One',cursive;font-size:13px;color:#aac4d8;">Tap outside to close</div>
      </div>
    </div>
    """

# ── GPS status box helper ─────────────────────────────────────────────────────
def gps_box(icon, color, bg, border, title, subtitle=""):
    sub = (f"<div style='font-size:14px;font-family:Fredoka One,cursive;margin-top:4px;opacity:0.85;'>{subtitle}</div>"
           if subtitle else "")
    return f"""
    <div style="background:{bg};border:2px solid {border};border-radius:16px;
                padding:16px 20px;margin-bottom:14px;
                font-family:Luckiest Guy,cursive;font-size:18px;color:{color};">
        {icon} {title}{sub}
    </div>
    """

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<h2 style='color:#5a7fa8;font-family:Luckiest Guy,cursive;'>Menu</h2>", unsafe_allow_html=True)
    page = st.radio("Go to", ["Check In", "My Schedule", "My Collection"], label_visibility="collapsed")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: CHECK IN
# ══════════════════════════════════════════════════════════════════════════════
if page == "Check In":

    # Only auto-refresh while countdown is active
    if st.session_state.checked_in and st.session_state.check_in_time:
        elapsed = (datetime.now() - st.session_state.check_in_time).total_seconds()
        if elapsed < 2:
            st_autorefresh(interval=1000, key="datarefresh")

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Luckiest+Guy&display=swap');
    .pokemon-logo {
        font-family:'Luckiest Guy',cursive;font-size:80px;color:#ffcb05;
        letter-spacing:3px;display:inline-block;transform:rotate(-4deg);
        text-shadow:-4px -4px 0 #2a75bb,4px -4px 0 #2a75bb,
                    -4px 4px 0 #2a75bb,4px 4px 0 #2a75bb,0px 10px 0 #1b4f9c;
    }
    </style>
    <div class="pokemon-logo">Schedulémon</div>
    """, unsafe_allow_html=True)

    st.markdown("<h2>Collect lecture cards by showing up and staying focused</h2>", unsafe_allow_html=True)

    # Streaks
    st.markdown("<p style='color:#5a7fa8;font-family:Luckiest Guy,cursive;font-size:22px;'>🔥 Current streaks:</p>", unsafe_allow_html=True)
    for course, value in st.session_state.streaks.items():
        st.markdown(f"<p style='color:#5a7fa8;font-family:Luckiest Guy,cursive;font-size:18px;'>{course}: {value}</p>", unsafe_allow_html=True)

    with st.expander("Share my streaks"):
        streak_share_text = build_streak_share_text()
        render_share_buttons(streak_share_text, "streaks")

    # Today's schedule cards
    st.markdown("<p style='color:#5a7fa8;font-family:Luckiest Guy,cursive;font-size:22px;'>📅 Today's Schedule:</p>", unsafe_allow_html=True)
    for cls in schedule:
        active       = is_class_active(cls["course"])
        border_color = "#4fa46d" if active else "#BED9F4"
        glow         = "0 0 16px rgba(79,164,109,0.6)" if active else "none"
        badge        = ('<span style="background:#d8f6df;color:#4fa46d;font-size:12px;'
                        'padding:4px 10px;border-radius:10px;margin-left:8px;'
                        'font-family:Luckiest Guy,cursive;display:inline-block;">LIVE NOW</span>'
                        if active else "")
        st.markdown(f"""
        <div style="background:#FEFDD0;padding:18px;border-radius:20px;margin-bottom:14px;
                    border:2px solid {border_color};box-shadow:{glow};">
            <div style="font-size:22px;font-weight:700;color:#5a7fa8;font-family:'Luckiest Guy',cursive;">
                {cls['course']} {badge}
            </div>
            <div style="font-size:15px;color:#8ab4d4;margin-top:6px;font-family:'Fredoka One',cursive;">
                {", ".join(cls.get("days") or [cls.get("day", "")])} &bull; {cls['start']} &ndash; {cls['end']}
            </div>
            <div style="font-size:14px;color:#aac4d8;margin-top:4px;font-family:'Fredoka One',cursive;">
                📍 {cls.get('location','No location added')}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── PRE-CHECK-IN GATE ─────────────────────────────────────────────────────
    if not st.session_state.checked_in:

        st.markdown("<h3 style='font-family:Luckiest Guy,cursive;color:#ffcb05;"
                    "text-shadow:-4px -4px 0 #2a75bb,4px -4px 0 #2a75bb,-4px 4px 0 #2a75bb,"
                    "4px 4px 0 #2a75bb,0px 6px 0 #1b4f9c;'>Check In</h3>", unsafe_allow_html=True)

        active_courses = [cls["course"] for cls in schedule if is_class_active(cls["course"])]

        if not active_courses:
            st.info("No classes are active right now. Add more classes in My Schedule if needed.")

        else:
            selected_course = st.selectbox("Choose your class", active_courses)
            cls_info        = get_class_info(selected_course)
            has_coords      = cls_info and "lat" in cls_info and "lon" in cls_info

            # ── STEP 1: Time confirmed ────────────────────────────────────────
            st.markdown(gps_box(
                "✅", "#4fa46d", "#d8f6df", "#a7dfb6",
                f"{selected_course} is live right now!"
            ), unsafe_allow_html=True)

            # ── STEP 2: GPS check ─────────────────────────────────────────────
            st.markdown("<p style='color:#5a7fa8;font-family:Luckiest Guy,cursive;font-size:20px;'>📍 Location Check</p>", unsafe_allow_html=True)

            if not has_coords:
                # No GPS coordinates stored for this class — skip location check
                st.markdown(gps_box(
                    "⚠️", "#a06030", "#fff8e8", "#f0c060",
                    "No GPS set for this class.",
                    "Add coordinates in My Schedule to enable location verification."
                ), unsafe_allow_html=True)
                st.session_state.gps_verified = True

            elif not st.session_state.gps_verified:
                st.markdown("""
                <p style='color:#5a7fa8;font-family:Fredoka One,cursive;font-size:16px;'>
                We need to confirm you're physically in the lecture hall.<br>
                Allow location access when your browser asks.
                </p>
                """, unsafe_allow_html=True)

                # Triggers browser location prompt — returns None while waiting
                location = get_geolocation(component_key="gps_check")

                at_hall = None
                distance = None

                if location is None:
                    # Still waiting for the browser to respond
                    st.markdown(gps_box(
                        "🔍", "#5a7fa8", "#e8f4ff", "#BED9F4",
                        "Waiting for your location...",
                        "Please tap Allow in the browser popup."
                    ), unsafe_allow_html=True)

                else:
                    if not isinstance(location, dict) or "coords" not in location:
                        st.markdown(gps_box(
                            "🔍", "#5a7fa8", "#e8f4ff", "#BED9F4",
                            "Waiting for your location...",
                            "Please tap Allow in the browser popup."
                        ), unsafe_allow_html=True)
                    else:
                        user_lat = location["coords"]["latitude"]
                        user_lon = location["coords"]["longitude"]
                        accuracy = location["coords"].get("accuracy", "?")
                        at_hall, distance = is_user_at_hall(user_lat, user_lon, selected_course)

                    if at_hall:
                        # ✅ GPS passed
                        st.session_state.gps_verified = True
                        st.markdown(gps_box(
                            "📍", "#4fa46d", "#d8f6df", "#a7dfb6",
                            f"You're at {cls_info.get('location', 'the hall')}!",
                            f"Distance: {distance}m · GPS accuracy: ±{round(accuracy) if isinstance(accuracy, (int, float)) else accuracy}m"
                        ), unsafe_allow_html=True)
                        st.rerun()
                    else:
                        # ❌ GPS failed — too far
                        st.markdown(gps_box(
                            "🚫", "#c0392b", "#ffeaea", "#e74c3c",
                            "You're not at the lecture hall!",
                            f"You are {distance}m away — must be within {cls_info.get('radius', 80)}m of {cls_info.get('location', 'the hall')}."
                        ), unsafe_allow_html=True)
                        st.markdown("""
                        <p style='color:#5a7fa8;font-family:Fredoka One,cursive;font-size:15px;'>
                        💡 Try moving closer to a window — GPS can be less accurate indoors.
                        </p>
                        """, unsafe_allow_html=True)
                        if st.button("Try Again"):
                            st.session_state.gps_verified = False
                            st.rerun()

            # ── STEP 3: Both checks passed → show Check In button ─────────────
            if st.session_state.gps_verified:
                if has_coords:
                    st.markdown(gps_box(
                        "✅", "#4fa46d", "#d8f6df", "#a7dfb6",
                        f"Location confirmed: {cls_info.get('location', 'Hall')}",
                        "You're good to go!"
                    ), unsafe_allow_html=True)

                if st.button("✅ Check In to Class"):
                    st.session_state.checked_in      = True
                    st.session_state.selected_course = selected_course
                    st.session_state.check_in_time   = datetime.now()
                    st.session_state.gps_verified    = False   # reset for next session
                    st.rerun()

    # ── ACTIVE SESSION ────────────────────────────────────────────────────────
    else:
        st.markdown("<h3 style='font-family:Luckiest Guy,cursive;color:#ffcb05;"
                    "text-shadow:-4px -4px 0 #2a75bb,4px -4px 0 #2a75bb,-4px 4px 0 #2a75bb,"
                    "4px 4px 0 #2a75bb,0px 6px 0 #1b4f9c;'>Active Session</h3>", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:#FEFDD0;color:#5a7fa8;font-family:Luckiest Guy,cursive;
                    font-size:20px;padding:14px 18px;border-radius:16px;
                    border:2px solid #BED9F4;margin-bottom:12px;">
            🎴 Card pending for {st.session_state.selected_course}
        </div>
        """, unsafe_allow_html=True)

        now            = datetime.now()
        elapsed        = now - st.session_state.check_in_time
        seconds_stayed = int(elapsed.total_seconds())
        GOAL_SECONDS   = 2   # ← change to full lecture duration for production

        progress_value    = min(seconds_stayed / GOAL_SECONDS, 1.0)
        remaining_seconds = max(0, GOAL_SECONDS - seconds_stayed)

        st.progress(progress_value)
        st.markdown(f"<p style='color:#5a7fa8;font-family:Luckiest Guy,cursive;font-size:22px;'>Time in class: {seconds_stayed // 60}m {seconds_stayed % 60}s</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#5a7fa8;font-family:Luckiest Guy,cursive;font-size:22px;'>Time remaining: {remaining_seconds // 60}m {remaining_seconds % 60}s</p>", unsafe_allow_html=True)

        if seconds_stayed >= GOAL_SECONDS:
            if st.session_state.pending_reward is None:
                new_pull           = pull_random_card()
                new_pull["course"] = st.session_state.selected_course
                new_pull["image"]  = random.choice(CARD_LIBRARY[new_pull["rarity"]])
                st.session_state.pending_reward = new_pull

            reward = st.session_state.pending_reward

            st.markdown(f"""
            <div style="background:#d8f6df;color:#4fa46d;font-family:Luckiest Guy,cursive;
                        font-size:22px;padding:16px;border-radius:16px;border:2px solid #a7dfb6;">
                🎉 Session Complete! Your card is revealed!
            </div>
            """, unsafe_allow_html=True)

            card_html    = build_card_html_with_image(reward)
            preview_html = f"""
            <div style="background:linear-gradient(180deg,#BED9F4 0%,#FEFDD0 100%);padding:1rem;border-radius:20px;">
                {CARD_CSS}
                <div class="cards-grid">{card_html}</div>
                {CARD_JS}
            </div>
            """
            components.html(preview_html, height=380)

            if st.button("Claim Card"):
                st.session_state.cards.append(reward)
                st.session_state.streaks[reward["course"]] += 1
                st.session_state.checked_in     = False
                st.session_state.check_in_time  = None
                st.session_state.pending_reward = None
                st.rerun()

        else:
            # Show card back while waiting
            back_html    = build_card_back_html()
            waiting_html = f"""
            <div style="background:linear-gradient(180deg,#BED9F4 0%,#FEFDD0 100%);padding:1rem;border-radius:20px;">
                {CARD_CSS}
                <div class="cards-grid">{back_html}</div>
            </div>
            """
            components.html(waiting_html, height=380)
            st.markdown("<p style='color:#5a7fa8;font-family:Luckiest Guy,cursive;font-size:20px;'>Stay in class to reveal your card!</p>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: MY SCHEDULE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "My Schedule":
    st.markdown("""
    <h1 style="
        font-family:Luckiest Guy,cursive;
        color:#ffcb05;
        letter-spacing:4px;
        margin-top:10px;
        margin-bottom:28px;
        line-height:1.1;
        text-shadow:
            -4px -4px 0 #2a75bb,
            4px -4px 0 #2a75bb,
            -4px  4px 0 #2a75bb,
            4px  4px 0 #2a75bb,
            0px  6px 0 #1b4f9c;
    ">
            My Schedule
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="
        color:#5a7fa8;
        font-family:Luckiest Guy,cursive;
        font-size:20px;
        margin-top:0;
        margin-bottom:20px;
    ">
        Add your classes here:
    </p>
    """, unsafe_allow_html=True)

    # add form
    with st.form("add_schedule_form"):
        course = st.text_input("Course Name")
        days = st.multiselect(
            "Days",
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        )
        start = st.text_input("Start Time (HH:MM)")
        end = st.text_input("End Time (HH:MM)")
        location = st.text_input(
            "Location Name",
            placeholder="e.g. Snow Hall, University of Kansas"
        )
        radius = st.text_input("Radius (m)", value="80")

        submitted = st.form_submit_button("Add Class")

        if submitted:
            if course and days and start and end and location:
                new_cls = {
                    "course": course.strip(),
                    "days": days,
                    "start": start.strip(),
                    "end": end.strip(),
                    "location": location.strip(),
                }

                lat, lon = geocode_location_name(location.strip())

                if lat is not None and lon is not None:
                    new_cls["lat"] = lat
                    new_cls["lon"] = lon
                    try:
                        new_cls["radius"] = int(radius.strip()) if radius.strip() else 80
                    except ValueError:
                        new_cls["radius"] = 80
                else:
                    st.warning("Could not find coordinates.")

                st.session_state.schedule.append(new_cls)
                if course.strip() not in st.session_state.streaks:
                    st.session_state.streaks[course.strip()] = 0
                st.success("Class added!")
                st.rerun()
            else:
                st.error("Fill everything")

    st.markdown("<p style='color:#5a7fa8;font-family:Luckiest Guy,cursive;font-size:22px;'>Your classes:</p>", unsafe_allow_html=True)

    if st.session_state.schedule:
        for i, cls in enumerate(st.session_state.schedule):
            has_gps = "lat" in cls and "lon" in cls
            gps_line = (
                f"🛰️ {cls['lat']:.4f}, {cls['lon']:.4f} · radius {cls.get('radius', 80)}m"
                if has_gps else "🛰️ No GPS coordinates — location check skipped"
            )

            display_days = ", ".join(cls.get("days", [cls.get("day", "")]))
            is_editing = st.session_state.editing_index == i

            if not is_editing:
                card_col, btn_col = st.columns([9, 1.3], vertical_alignment="top")

                with card_col:
                    st.markdown(f"""
                    <div style="
                        background:#FEFDD0;
                        padding:20px 22px;
                        border-radius:22px;
                        margin-bottom:16px;
                        border:2px solid #BED9F4;
                        box-shadow:0 6px 18px rgba(90,127,168,0.08);
                    ">
                        <div style="
                            font-size:22px;
                            font-weight:700;
                            color:#5a7fa8;
                            font-family:'Luckiest Guy',cursive;
                            margin-bottom:10px;
                        ">
                            {cls['course']}
                        </div>
                        <div style="
                            font-size:15px;
                            color:#8ab4d4;
                            margin-top:4px;
                            font-family:'Fredoka One',cursive;
                        ">
                            {display_days} &bull; {cls['start']} &ndash; {cls['end']}
                        </div>
                        <div style="
                            font-size:14px;
                            color:#aac4d8;
                            margin-top:8px;
                            font-family:'Fredoka One',cursive;
                        ">
                            📍 {cls.get('location', 'No location added')}
                        </div>
                        <div style="
                            font-size:13px;
                            color:#b8d0e4;
                            margin-top:6px;
                            font-family:'Fredoka One',cursive;
                        ">
                            {gps_line}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with btn_col:
                    edit_clicked = st.button("✏️", key=f"edit_icon_{i}", use_container_width=True)
                    delete_clicked = st.button("🗑️", key=f"delete_icon_{i}", use_container_width=True)

                if edit_clicked:
                    st.session_state.editing_index = i
                    st.rerun()

                if delete_clicked:
                    removed = st.session_state.schedule.pop(i)
                    st.session_state.editing_index = None
                    st.success(f"Deleted {removed['course']}")
                    st.rerun()

            else:
                st.markdown('<div class="edit-panel">', unsafe_allow_html=True)

                st.markdown(f"""
                <div style="
                    font-size:22px;
                    font-weight:700;
                    color:#5a7fa8;
                    font-family:'Luckiest Guy',cursive;
                    margin-bottom:14px;
                ">
                    Editing {cls['course']}
                </div>
                """, unsafe_allow_html=True)

                with st.form(f"edit_schedule_form_{i}"):

                    edit_course = st.text_input("Course Name", value=cls.get("course", ""))
                    edit_days = st.multiselect(
                        "Days",
                        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                        default=cls.get("days", [cls.get("day", "")])
                    )

                    time_col1, time_col2 = st.columns(2)
                    with time_col1:
                        edit_start = st.text_input("Start Time (HH:MM)", value=cls.get("start", ""))
                    with time_col2:
                        edit_end = st.text_input("End Time (HH:MM)", value=cls.get("end", ""))

                    edit_location = st.text_input("Location Name", value=cls.get("location", ""))
                    edit_radius = st.text_input("Radius (m)", value=str(cls.get("radius", 80)))

                    action_col1, action_col2 = st.columns(2)
                    with action_col1:
                        save_edit = st.form_submit_button("Save", use_container_width=True)
                    with action_col2:
                        cancel_edit = st.form_submit_button("Cancel", use_container_width=True)

                    if save_edit:
                        if edit_course and edit_days and edit_start and edit_end and edit_location:
                            updated_cls = {
                                "course": edit_course.strip(),
                                "days": edit_days,
                                "start": edit_start.strip(),
                                "end": edit_end.strip(),
                                "location": edit_location.strip(),
                            }

                            lat, lon = geocode_location_name(edit_location.strip())

                            if lat is not None and lon is not None:
                                updated_cls["lat"] = lat
                                updated_cls["lon"] = lon
                                try:
                                    updated_cls["radius"] = int(edit_radius.strip()) if edit_radius.strip() else 80
                                except ValueError:
                                    updated_cls["radius"] = 80
                            else:
                                updated_cls["radius"] = cls.get("radius", 80)
                                if "lat" in cls and "lon" in cls:
                                    updated_cls["lat"] = cls["lat"]
                                    updated_cls["lon"] = cls["lon"]

                            st.session_state.schedule[i] = updated_cls

                            if edit_course.strip() not in st.session_state.streaks:
                                st.session_state.streaks[edit_course.strip()] = 0

                            st.session_state.editing_index = None
                            st.success("Class updated!")
                            st.rerun()
                        else:
                            st.error("Fill everything")

                    if cancel_edit:
                        st.session_state.editing_index = None
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.info("No classes added yet.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: MY COLLECTION
# ══════════════════════════════════════════════════════════════════════════════
elif page == "My Collection":
    st.markdown("""
    <h1 style="
        font-family:Luckiest Guy,cursive;
        color:#ffcb05;
        margin-top:10px;
        margin-bottom:28px;
        line-height:1.1;
        text-shadow:
            -4px -4px 0 #2a75bb,
            4px -4px 0 #2a75bb,
            -4px  4px 0 #2a75bb,
            4px  4px 0 #2a75bb,
            0px  6px 0 #1b4f9c;
    ">
        My Collection
    </h1>
    """, unsafe_allow_html=True)

    with st.expander("Share my collection"):
        collection_share_text = build_collection_share_text()
        render_share_buttons(collection_share_text, "collection")

    grouped_cards = {k: [] for k in ["common","uncommon","rare","dr","ir","ur","sir"]}
    for card in st.session_state.cards:
        rarity_key = RARITY_LABELS.get(card["rarity"])
        if rarity_key in grouped_cards:
            grouped_cards[rarity_key].append(card)

    for rarity_folder, cards_in_group in grouped_cards.items():
        st.markdown(f"<h3 style='color:#5a7fa8;font-family:Luckiest Guy,cursive;text-transform:uppercase;'>{rarity_folder}</h3>", unsafe_allow_html=True)
        if cards_in_group:
            all_cards_html  = "".join(build_card_html_revealed(c) for c in cards_in_group)
            collection_html = f"""
            <div style='background:linear-gradient(180deg,#BED9F4 0%,#FEFDD0 100%);padding:1rem;border-radius:16px;margin-bottom:20px;'>
                {CARD_CSS}
                <div style='max-height:420px;overflow-y:auto;padding-right:8px;scrollbar-width:thin;scrollbar-color:#BED9F4 #FEFDD0;'>
                    <div class='cards-grid'>{all_cards_html}</div>
                </div>
                {CARD_JS}
            </div>
            """
            components.html(collection_html, height=460)
        else:
            st.markdown(f"<p style='color:#5a7fa8;font-family:Luckiest Guy,cursive;font-size:18px;margin-bottom:20px;'>No cards in {rarity_folder} yet.</p>", unsafe_allow_html=True)
