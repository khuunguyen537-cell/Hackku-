import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
import time
import random
import base64
from pathlib import Path

st.set_page_config(page_title="Schedulémon", layout="centered")

def load_pokemon_font():
    import base64

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
        -4px -4px 0 #2a75bb,
         4px -4px 0 #2a75bb,
        -4px  4px 0 #2a75bb,
         4px  4px 0 #2a75bb,
         0px  6px 0 #1b4f9c;
}

header[data-testid="stHeader"] {
    background: #BED9F4 !important;
}

.stToolbar, [data-testid="stToolbar"] {
    background: #BED9F4 !important;
}

[data-testid="stToolbar"] button,
[data-testid="stToolbar"] * {
    color: #5a7fa8 !important;
}

/* closed select box */
[data-testid="stSelectbox"] > div > div,
[data-baseweb="select"] > div {
    background: #FEFDD0 !important;
    border: 2px solid #BED9F4 !important;
    border-radius: 12px !important;
    color: #5a7fa8 !important;
    font-family: 'Luckiest Guy', cursive !important;
    font-size: 18px !important;
    box-shadow: none !important;
}

/* selected value inside box */
[data-baseweb="select"] span,
[data-baseweb="select"] div {
    font-family: 'Luckiest Guy', cursive !important;
    color: #5a7fa8 !important;
}

/* dropdown popup */
ul[role="listbox"] {
    background: #FEFDD0 !important;
    border: 2px solid #BED9F4 !important;
    border-radius: 12px !important;
    padding: 6px !important;
}

/* each option */
li[role="option"] {
    background: #FEFDD0 !important;
    color: #5a7fa8 !important;
    font-family: 'Luckiest Guy', cursive !important;
    font-size: 18px !important;
    border-radius: 8px !important;
}

/* hovered option */
li[role="option"]:hover {
    background: #BED9F4 !important;
    color: white !important;
}

/* selected option */
li[aria-selected="true"] {
    background: #a8cce8 !important;
    color: white !important;
}

/* buttons */
[data-testid="stButton"] button {
    background: #BED9F4 !important;
    color: #5a7fa8 !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Luckiest Guy', cursive !important;
    font-size: 16px !important;
    letter-spacing: 1px !important;
}

[data-testid="stButton"] button:hover {
    background: #a8cce8 !important;
}
</style>
""", unsafe_allow_html=True)


# ── 1. Session State Initialization ──────────────────────────────────────────
if "checked_in" not in st.session_state:
    st.session_state.checked_in = False
if "selected_course" not in st.session_state:
    st.session_state.selected_course = None
if "cards" not in st.session_state:
    st.session_state.cards = []
if "streaks" not in st.session_state:
    st.session_state.streaks = {}
if "check_in_time" not in st.session_state:
    st.session_state.check_in_time = None
if "pending_reward" not in st.session_state:
    st.session_state.pending_reward = None

# ── 2. Schedule & Probability Logic ──────────────────────────────────────────
# NOTE: Update these times to match your current testing time!
schedule = [
    {"course": "CHEM 135", "day": "Saturday", "start": "00:00", "end": "18:00"},
    {"course": "MATH 125", "day": "Friday", "start": "11:00", "end": "12:15"},
    {"course": "BIOL 240", "day": "Friday", "start": "14:00", "end": "14:50"},
]
for cls in schedule:
    if cls["course"] not in st.session_state.streaks:
        st.session_state.streaks[cls["course"]] = 0

# Updated weights based on your request
RARITY_CHANCES = {
    "Common": 600,
    "Uncommon": 250,
    "Rare": 100,
    "Double Rare": 35,
    "Illustration Rare": 9,     # More common than UR now
    "Ultra Rare": 6,
    "Special Illustration Rare": 3
}

def pull_random_card():
    rarities = list(RARITY_CHANCES.keys())
    weights = list(RARITY_CHANCES.values())
    selected_rarity = random.choices(rarities, weights=weights, k=1)[0]
    
    name_map = {
        "Common": "Lecture Starter Card",
        "Uncommon": "Steady Learner Card",
        "Rare": "Focused Scholar Card",
        "Double Rare": "Double Grind Card",
        "Ultra Rare": "Ultra Focus Card",
        "Illustration Rare": "Showcase Scholar Card",
        "Special Illustration Rare": "Master Collector Card"
    }
    return {"name": name_map[selected_rarity], "rarity": selected_rarity}

def is_class_active(selected_class):
    now = datetime.now()
    current_day = now.strftime("%A")
    current_time = now.strftime("%H:%M")
    for cls in schedule:
        if cls["course"] == selected_class:
            if cls["day"] == current_day and cls["start"] <= current_time <= cls["end"]:
                return True
    return False

# ── 3. Pokemon card images ────────────────────────────────────────────────────────────
# Assuming your images are in 'assets/[rarity]/' folder
CARD_LIBRARY = {
    "Common": [f"151/common/c{i}.png" for i in range(1, 7)],
    "Uncommon": [f"151/uncommon/u{i}.png" for i in range(1, 10)],
    "Rare": [f"151/rare/r{i}.png" for i in range(1, 6)],
    "Double Rare": [f"151/dr/dr{i}.png" for i in range(1, 7)],
    "Illustration Rare": [f"151/ir/ir{i}.png" for i in range(1, 9)],
    "Ultra Rare": [f"151/ur/ur{i}.png" for i in range(1, 6)],
    "Special Illustration Rare": [f"151/sir/sir{i}.png" for i in range(1, 6)],
}
RARITY_LABELS = {
    "Common": "common",
    "Uncommon": "uncommon",
    "Rare": "rare",
    "Double Rare": "dr",
    "Illustration Rare": "ir",
    "Ultra Rare": "ur",
    "Special Illustration Rare": "sir"
}
# ── 4. Styling (CSS & HTML Builders) ─────────────────────────────────────────
# [Keep your existing CARD_CSS, CARD_JS, RARITY_CONFIG, SPARKLES, and build_card_html here]
# ... (I'm skipping the long CSS blocks for brevity, but keep them in your file!)
# ── Card CSS (injected once) ───────────────────────────────────────────────────
CARD_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Nunito:wght@400;700;900&display=swap');

/* --- Add this to your existing CARD_CSS block --- */
.card-inner {
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden; /* Important for tilt */
    padding: 0; /* Important so image fills the 'card' space */
}

.pokemon-sprite {
    width: 100%;
    height: 100%;
    object-fit: cover; /* Important: image fills the card without stretching */
    transition: transform 0.3s;
    filter: none !important; /* IMPORTANT: DISABLE THE DROP-SHADOWS from the old text sprites */
}

/* The tilt logic requires we target the wrap */
.card-wrap { perspective: 900px; cursor: pointer; }
.card {
    transition: transform 0.15s ease;
    will-change: transform;
}
/* Re-enable old JS tilt effect on the card element, not inner */

.cards-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 2rem;
    justify-content: center;
    padding: 1rem 0 2rem;
}

.card-wrap { perspective: 900px; cursor: pointer; }

.card {
    width: 200px;
    height: 300px;
    border-radius: 18px;
    position: relative;
    transform-style: preserve-3d;
    transition: transform 0.15s ease;
    user-select: none;
}

.card-inner {
    width: 100%;
    height: 100%;
    border-radius: 18px;
    padding: 14px;
    display: flex;
    flex-direction: column;
    position: relative;
    overflow: hidden;
    border: 2px solid transparent;
}

.card-inner::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 18px;
    opacity: 0;
    transition: opacity 0.3s;
    pointer-events: none;
    z-index: 10;
    mix-blend-mode: screen;
}

.card-wrap:hover .card-inner::before {
    opacity: 1;
    animation: shimmerPink 1.6s linear infinite;
}

@keyframes shimmerPink {
    0% {
        background: linear-gradient(
            120deg,
            rgba(255,255,255,0) 25%,
            rgba(255,182,222,0.18) 45%,
            rgba(255,255,255,0.28) 50%,
            rgba(255,105,180,0.16) 55%,
            rgba(255,255,255,0) 75%
        );
        background-position: 0% 0%;
    }
    100% {
        background: linear-gradient(
            120deg,
            rgba(255,255,255,0) 25%,
            rgba(255,182,222,0.18) 45%,
            rgba(255,255,255,0.28) 50%,
            rgba(255,105,180,0.16) 55%,
            rgba(255,255,255,0) 75%
        );
        background-position: 100% 100%;
    }
}

/* COMMON */
.card {
    box-shadow: none;
}

.card-inner {
    box-shadow: none;
    border: none;
}

.pokemon-sprite {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 18px;

    /* 🔥 THIS IS THE MAGIC */
    box-shadow:
        0 0 12px rgba(255, 182, 222, 0.35),
        0 0 24px rgba(255, 105, 180, 0.25),
        0 0 40px rgba(255, 105, 180, 0.15);
}


.card-common .card-inner::after {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 16px;
    pointer-events: none;
    background:
        radial-gradient(circle at 18% 22%, rgba(255,255,255,0.30) 0 1.5px, transparent 2px),
        radial-gradient(circle at 82% 18%, rgba(255,192,203,0.28) 0 1.5px, transparent 2px),
        radial-gradient(circle at 74% 74%, rgba(255,255,255,0.22) 0 1.5px, transparent 2px),
        radial-gradient(circle at 28% 78%, rgba(255,182,193,0.26) 0 1.5px, transparent 2px),
        linear-gradient(135deg, rgba(255,255,255,0.06), rgba(255,105,180,0.06), rgba(255,255,255,0.02));
    opacity: 0.95;
    animation: pinkFoilTwinkle 2.8s ease-in-out infinite;
    mix-blend-mode: screen;
}

.card-common .pokemon-sprite {
    filter:
        drop-shadow(0 0 2px rgba(255,255,255,0.18))
        drop-shadow(0 0 8px rgba(255,105,180,0.14)) !important;
}

.card-common .course-tag {
    background: rgba(255,182,222,0.14);
    color: #ffd8ef;
    border-color: rgba(255,182,222,0.28);
}

.card-common .stat-row span:last-child {
    color: #ffd8ef;
}

.card-common .bottom-glow {
    background: radial-gradient(ellipse, rgba(255,105,180,0.16), transparent 70%);
}

@keyframes pinkFoilTwinkle {
    0%, 100% {
        opacity: 0.72;
        transform: scale(1);
    }
    50% {
        opacity: 1;
        transform: scale(1.01);
    }
}

/* UNCOMMON */
.card-uncommon .card-inner { background: linear-gradient(160deg,#1b2e1b,#2f5a2f,#1a3d1a); border-color:#66bb6a; box-shadow:0 0 18px rgba(102,187,106,0.35),0 8px 32px rgba(0,0,0,0.6); }
.card-uncommon .card-header { border-bottom-color: rgba(102,187,106,0.4); }
.card-uncommon .rarity-badge { background:#66bb6a; color:#fff; }
.card-uncommon .card-icon-bg { background:radial-gradient(circle,#356b35,#1a3d1a); border:2px solid rgba(102,187,106,0.5); }
.card-uncommon .pokemon-sprite { filter:drop-shadow(0 0 8px #66bb6a); }
.card-uncommon .card-name { color:#c8e6c9; }
.card-uncommon .course-tag { background:rgba(102,187,106,0.18); color:#a5d6a7; border-color:rgba(102,187,106,0.3); }
.card-uncommon .stat-row span:last-child { color:#c8e6c9; }
.card-uncommon .bottom-glow { background:radial-gradient(ellipse,rgba(102,187,106,0.18),transparent 70%); }

/* DOUBLE RARE */
.card-double-rare .card-inner { background:linear-gradient(160deg,#1e123a,#35205f,#180d33); border-color:#9575cd; box-shadow:0 0 24px rgba(149,117,205,0.45),0 8px 32px rgba(0,0,0,0.7); }
.card-double-rare .card-header { border-bottom-color:rgba(149,117,205,0.45); }
.card-double-rare .rarity-badge { background:linear-gradient(90deg,#7e57c2,#9575cd); color:#fff; }
.card-double-rare .card-icon-bg { background:radial-gradient(circle,#40246d,#180d33); border:2px solid rgba(149,117,205,0.5); }
.card-double-rare .pokemon-sprite { filter:drop-shadow(0 0 10px #b39ddb); }
.card-double-rare .card-name { color:#d1c4e9; }
.card-double-rare .course-tag { background:rgba(149,117,205,0.18); color:#d1c4e9; border-color:rgba(149,117,205,0.3); }
.card-double-rare .stat-row span:last-child { color:#d1c4e9; }
.card-double-rare .bottom-glow { background:radial-gradient(ellipse,rgba(149,117,205,0.2),transparent 70%); }
.card-double-rare .sparkle { display:block; }

/* ULTRA RARE */
.card-ultra-rare .card-inner { background:linear-gradient(160deg,#3a2a00,#6b4f00,#2b1f00); border-color:#ffca28; box-shadow:0 0 28px rgba(255,202,40,0.5),0 8px 32px rgba(0,0,0,0.75); }
.card-ultra-rare .card-header { border-bottom-color:rgba(255,202,40,0.45); }
.card-ultra-rare .rarity-badge { background:linear-gradient(90deg,#f9a825,#ffca28); color:#1a1a1a; }
.card-ultra-rare .card-icon-bg { background:radial-gradient(circle,#7a5c00,#2b1f00); border:2px solid rgba(255,202,40,0.55); }
.card-ultra-rare .pokemon-sprite { filter:drop-shadow(0 0 12px #ffd54f); }
.card-ultra-rare .card-name { color:#fff3c4; }
.card-ultra-rare .course-tag { background:rgba(255,202,40,0.18); color:#ffe082; border-color:rgba(255,202,40,0.35); }
.card-ultra-rare .stat-row span:last-child { color:#fff3c4; }
.card-ultra-rare .bottom-glow { background:radial-gradient(ellipse,rgba(255,202,40,0.22),transparent 70%); }
.card-ultra-rare .sparkle { display:block; }

/* ILLUSTRATION RARE */
.card-illustration-rare .card-inner { background:linear-gradient(160deg,#10243d,#1f4b5f,#3d1f52); border-color:#4dd0e1; box-shadow:0 0 28px rgba(77,208,225,0.35),0 0 40px rgba(244,143,177,0.18),0 8px 32px rgba(0,0,0,0.75); }
.card-illustration-rare .card-header { border-bottom-color:rgba(77,208,225,0.4); }
.card-illustration-rare .rarity-badge { background:linear-gradient(90deg,#26c6da,#ec407a); color:#fff; }
.card-illustration-rare .card-icon-bg { background:radial-gradient(circle,#245d70,#25153d); border:2px solid rgba(77,208,225,0.45); }
.card-illustration-rare .pokemon-sprite { filter:drop-shadow(0 0 12px #80deea); }
.card-illustration-rare .card-name { color:#d1f5ff; }
.card-illustration-rare .course-tag { background:rgba(77,208,225,0.16); color:#b2ebf2; border-color:rgba(77,208,225,0.3); }
.card-illustration-rare .stat-row span:last-child { color:#d1f5ff; }
.card-illustration-rare .bottom-glow { background:radial-gradient(ellipse,rgba(77,208,225,0.2),transparent 70%); }
.card-illustration-rare .sparkle { display:block; }

/* SPECIAL ILLUSTRATION RARE */
.card-special-illustration-rare .card-inner {
    background:linear-gradient(160deg,#24103d,#4a1f5f,#5f2a3d,#1f3f5f);
    border-color:#ff80ab;
    box-shadow:0 0 34px rgba(255,128,171,0.45),0 0 60px rgba(255,241,118,0.18),0 8px 32px rgba(0,0,0,0.82);
}
.card-special-illustration-rare .card-inner::after {
    content:'';
    position:absolute;
    inset:0;
    border-radius:16px;
    background:linear-gradient(135deg,rgba(255,255,255,0.05) 0%,rgba(255,241,118,0.08) 35%,rgba(255,128,171,0.08) 70%,rgba(179,157,219,0.08) 100%);
    pointer-events:none;
    animation:epicPulse 3s ease-in-out infinite;
}
.card-special-illustration-rare .card-header { border-bottom-color:rgba(255,128,171,0.45); }
.card-special-illustration-rare .rarity-badge { background:linear-gradient(90deg,#ff80ab,#fff176,#b39ddb); color:#1a1a1a; font-weight:900; }
.card-special-illustration-rare .card-icon-bg { background:radial-gradient(circle,#5c2b70,#1f173d); border:2px solid rgba(255,128,171,0.5); box-shadow:0 0 18px rgba(255,128,171,0.25) inset; }
.card-special-illustration-rare .pokemon-sprite { filter:drop-shadow(0 0 14px #fff59d) drop-shadow(0 0 8px #f8bbd0); }
.card-special-illustration-rare .card-name { color:#fff1f7; text-shadow:0 0 8px rgba(255,255,255,0.18); }
.card-special-illustration-rare .course-tag { background:rgba(255,128,171,0.16); color:#ffe4ef; border-color:rgba(255,128,171,0.28); }
.card-special-illustration-rare .stat-row span:last-child { color:#fff1f7; }
.card-special-illustration-rare .bottom-glow { background:radial-gradient(ellipse,rgba(255,128,171,0.22),transparent 70%); }
.card-special-illustration-rare .sparkle { display:block; }

/* SHARED INTERNALS */
.card-header { display:flex; justify-content:space-between; align-items:center; padding-bottom:10px; border-bottom:1px solid; margin-bottom:12px; }
.card-number { font-family:'Press Start 2P',monospace; font-size:9px; color:rgba(255,255,255,0.35); }
.rarity-badge { font-size:9px; font-weight:900; letter-spacing:1.5px; text-transform:uppercase; padding:3px 9px; border-radius:20px; }
.card-icon-bg { width:110px; height:100px; border-radius:14px; margin:0 auto 10px; display:flex; align-items:center; justify-content:center; }
.pokemon-sprite { font-size:56px; line-height:1; transition:transform 0.3s; }
.card-wrap:hover .pokemon-sprite { transform:scale(1.1) translateY(-3px); }
.card-name { font-family:'Nunito',sans-serif; font-weight:900; font-size:14px; text-align:center; margin-bottom:4px; }
.course-tag { display:inline-block; font-size:10px; font-weight:700; padding:2px 10px; border-radius:20px; border:1px solid; margin:0 auto 10px; letter-spacing:1px; text-align:center; }
.stats { margin-top:auto; display:flex; flex-direction:column; gap:4px; }
.stat-row { display:flex; justify-content:space-between; font-size:10px; color:rgba(255,255,255,0.5); padding:3px 6px; border-radius:6px; background:rgba(0,0,0,0.2); }
.stat-row span:last-child { font-weight:700; }
.bottom-glow { position:absolute; bottom:0; left:0; right:0; height:80px; border-radius:0 0 18px 18px; pointer-events:none; }
.sparkle { display:none; position:absolute; top:0; left:0; right:0; bottom:0; pointer-events:none; z-index:5; }
.sparkle span { position:absolute; width:4px; height:4px; border-radius:50%; background:white; animation:float 2s ease-in-out infinite; }
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
/* Scrolling background Pokémon */
.poke-runner {
    position: fixed;
    bottom: 60px;
    width: 64px;
    height: 64px;
    image-rendering: pixelated;
    z-index: 0;
    pointer-events: none;
    animation: runAcross linear infinite;
    opacity: 0.55;
}

@keyframes runAcross {
    0%   { left: -80px;  transform: scaleX(1); }
    49%  { left: 110%;   transform: scaleX(1); }
    50%  { left: 110%;   transform: scaleX(-1); }
    99%  { left: -80px;  transform: scaleX(-1); }
    100% { left: -80px;  transform: scaleX(1); }
}

/* Stagger each Pokémon at different heights & speeds */
.poke-1 { bottom: 50px;  animation-duration: 9s;  animation-delay: 0s; }
.poke-2 { bottom: 120px; animation-duration: 13s; animation-delay: -4s; }
.poke-3 { bottom: 200px; animation-duration: 17s; animation-delay: -8s; }
.poke-4 { bottom: 280px; animation-duration: 11s; animation-delay: -2s; }
.poke-5 { bottom: 350px; animation-duration: 15s; animation-delay: -6s; }

/* Dark background */
body, .stApp {
    background: linear-gradient(180deg, #BED9F4 0%, #FEFDD0 100%) !important;
}

/* Subtle pokeball pattern overlay */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: 
        radial-gradient(circle, rgba(255,255,255,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}
</style>

<!-- Pokémon sprites from PokeAPI — mix of fan-favourites -->
<img class="poke-runner poke-1" src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png"  alt="" />
<img class="poke-runner poke-2" src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/39.png"  alt="" />
<img class="poke-runner poke-3" src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/133.png" alt="" />
<img class="poke-runner poke-4" src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/52.png"  alt="" />
<img class="poke-runner poke-5" src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/129.png" alt="" />
"""

st.markdown(RUNNING_POKEMON_HTML, unsafe_allow_html=True)
RARITY_CONFIG = {
    "Common": ("card-common", "⚪", "#001"),
    "Uncommon": ("card-uncommon", "🟢", "#002"),
    "Rare": ("card-rare", "🔵", "#003"),
    "Double Rare": ("card-double-rare", "💎", "#004"),
    "Ultra Rare": ("card-ultra-rare", "🟡", "#005"),
    "Illustration Rare": ("card-illustration-rare", "🎨", "#006"),
    "Special Illustration Rare": ("card-special-illustration-rare", "✨", "#007"),
}

# 👇 ADD HERE
RARITY_GLOW = {
    "Common": "255,182,222",
    "Uncommon": "102,187,106",
    "Rare": "144,202,249",
    "Double Rare": "179,157,219",
    "Ultra Rare": "255,202,40",
    "Illustration Rare": "77,208,225",
    "Special Illustration Rare": "255,128,171"
}

SPARKLES = {
    "Common": "",
    "Uncommon": "",
    "Rare": """
    <div class="sparkle">
        <span style="top:20%;left:15%;animation-delay:0.2s;background:#90caf9"></span>
        <span style="top:60%;left:80%;animation-delay:0.7s;background:#bbdefb"></span>
    </div>
    """,
    "Double Rare": """
    <div class="sparkle">
        <span style="top:15%;left:20%;animation-delay:0s;background:#b39ddb"></span>
        <span style="top:25%;left:78%;animation-delay:0.5s;background:#ce93d8"></span>
        <span style="top:70%;left:85%;animation-delay:0.3s;background:#e1bee7"></span>
    </div>
    """,
    "Ultra Rare": """
    <div class="sparkle">
        <span style="top:15%;left:20%;animation-delay:0s;background:#ffd54f"></span>
        <span style="top:25%;left:78%;animation-delay:0.5s;background:#fff176"></span>
        <span style="top:65%;left:12%;animation-delay:0.9s;background:#ffecb3"></span>
    </div>
    """,
    "Illustration Rare": """
    <div class="sparkle">
        <span style="top:18%;left:22%;animation-delay:0s;background:#80deea"></span>
        <span style="top:30%;left:76%;animation-delay:0.4s;background:#f48fb1"></span>
        <span style="top:62%;left:18%;animation-delay:0.8s;background:#a5d6a7"></span>
    </div>
    """,
    "Special Illustration Rare": """
    <div class="sparkle">
        <span style="top:15%;left:20%;animation-delay:0s;background:#ffffff"></span>
        <span style="top:25%;left:78%;animation-delay:0.5s;background:#ffd1dc"></span>
        <span style="top:65%;left:12%;animation-delay:0.9s;background:#fff59d"></span>
        <span style="top:70%;left:85%;animation-delay:0.3s;background:#b39ddb"></span>
        <span style="top:50%;left:50%;animation-delay:1.3s;background:#ffffff"></span>
    </div>
    """,

}
def image_to_base64(image_path):
    path = Path(image_path)
    if not path.exists():
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
    
def get_back_card_base64():             # ← ADD RIGHT HERE
    path = Path("back.png")
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
def build_card_back_html():
    back_base64 = image_to_base64("back.png")
    return f"""
    <div class="card-wrap">
      <div class="card" style="border-radius:18px;">
        <div class="card-inner" style="padding:0;">
          <img src="data:image/png;base64,{back_base64}" 
               style="width:100%;height:100%;object-fit:cover;border-radius:14px;" />
        </div>
      </div>
    </div>
    """        
def build_card_html_with_image(card):
    css_class_map = {
        "Common": ("card-common", "#f0a0c0", "rgba(240,160,192,0.4)"),
        "Uncommon": ("card-uncommon", "#66bb6a", "rgba(102,187,106,0.4)"),
        "Rare": ("card-rare", "#90caf9", "rgba(144,202,249,0.4)"),
        "Double Rare": ("card-double-rare", "#9575cd", "rgba(149,117,205,0.4)"),
        "Ultra Rare": ("card-ultra-rare", "#ffca28", "rgba(255,202,40,0.4)"),
        "Illustration Rare": ("card-illustration-rare", "#4dd0e1", "rgba(77,208,225,0.4)"),
        "Special Illustration Rare": ("card-special-illustration-rare", "#ff80ab", "rgba(255,128,171,0.4)"),
    }

    css_class, border_color, glow_color = css_class_map.get(card["rarity"], ("card-common", "#f0a0c0", "rgba(240,160,192,0.4)"))
    image_base64 = image_to_base64(card["image"])
    back_base64 = image_to_base64("back.png")
    card_id = f"card_{random.randint(10000,99999)}"

    if image_base64:
        front_img = f'<img src="data:image/png;base64,{image_base64}" style="width:94%;height:94%;object-fit:cover;border-radius:14px;" />'
    else:
        front_img = f'<div style="color:white;padding:20px;">Image not found</div>'

    return f"""
    <style>
    .flip-container-{card_id} {{
        perspective: 1000px;
        width: 200px;
        height: 300px;
        cursor: pointer;
    }}
    .flipper-{card_id} {{
        width: 100%;
        height: 100%;
        position: relative;
        transform-style: preserve-3d;
        transform: rotateY(180deg);
        transition: transform 0.8s ease;
    }}
    .flipper-{card_id}.flipped {{
        transform: rotateY(0deg);
    }}
    .card-face-{card_id} {{
        position: absolute;
        width: 100%;
        height: 100%;
        border-radius: 18px;
        backface-visibility: hidden;
        -webkit-backface-visibility: hidden;
    }}
    .card-front-{card_id} {{
        transform: rotateY(0deg);
        border: 6px solid {border_color};
        box-shadow: 0 0 12px {glow_color}, 0 0 24px {glow_color};
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }}
    .card-back-{card_id} {{
        transform: rotateY(180deg);
        border-radius: 18px;
        overflow: hidden;
    }}
    </style>

    <div class="flip-container-{card_id}"
         onclick="
            var flipper = document.getElementById('flipper-{card_id}');
            if (!flipper.classList.contains('flipped')) {{
                flipper.classList.add('flipped');
            }} else {{
                document.getElementById('modal-{card_id}').style.display='flex';
            }}
         ">
      <div id="flipper-{card_id}" class="flipper-{card_id}">

        <!-- FRONT -->
        <div class="card-face-{card_id} card-front-{card_id} card {css_class}">
          {front_img}
        </div>

        <!-- BACK -->
        <div class="card-face-{card_id} card-back-{card_id}">
          <img src="data:image/png;base64,{back_base64}"
               style="width:100%;height:100%;object-fit:cover;border-radius:12px;" />
        </div>

      </div>
    </div>

    <!-- Modal -->
    <div id="modal-{card_id}" style="
        display:none;
        position:fixed;
        inset:0;
        background:rgba(0,0,0,0.6);
        z-index:9999;
        justify-content:center;
        align-items:center;
    " onclick="this.style.display='none'">
        <div style="
            background:#FEFDD0;
            border-radius:20px;
            padding:28px;
            max-width:320px;
            width:90%;
            border: 3px solid {border_color};
            box-shadow: 0 0 30px {glow_color};
            text-align:center;
        " onclick="event.stopPropagation()">
            <img src="data:image/png;base64,{image_base64}"
                 style="width:180px;border-radius:12px;margin-bottom:16px;" />
            <div style="font-family:'Luckiest Guy',cursive;font-size:20px;color:#5a7fa8;margin-bottom:8px;">
                {card['rarity']}
            </div>
            <div style="font-family:'Fredoka One',cursive;font-size:16px;color:#8ab4d4;">
                Course: {card['course']}
            </div>
            <div style="margin-top:16px;font-family:'Fredoka One',cursive;font-size:13px;color:#aac4d8;">
                Tap outside to close
            </div>
        </div>
    </div>
    """


def build_card_html_revealed(card):
    css_class_map = {
        "Common": ("card-common", "#f0a0c0", "rgba(240,160,192,0.4)"),
        "Uncommon": ("card-uncommon", "#66bb6a", "rgba(102,187,106,0.4)"),
        "Rare": ("card-rare", "#90caf9", "rgba(144,202,249,0.4)"),
        "Double Rare": ("card-double-rare", "#9575cd", "rgba(149,117,205,0.4)"),
        "Ultra Rare": ("card-ultra-rare", "#ffca28", "rgba(255,202,40,0.4)"),
        "Illustration Rare": ("card-illustration-rare", "#4dd0e1", "rgba(77,208,225,0.4)"),
        "Special Illustration Rare": ("card-special-illustration-rare", "#ff80ab", "rgba(255,128,171,0.4)"),
    }
    css_class, border_color, glow_color = css_class_map.get(card["rarity"], ("card-common", "#f0a0c0", "rgba(240,160,192,0.4)"))
    image_base64 = image_to_base64(card["image"])
    card_id = f"card_{random.randint(10000,99999)}"
    if image_base64:
        front_img = f'<img src="data:image/png;base64,{image_base64}" style="width:94%;height:94%;object-fit:cover;border-radius:14px;" />'
    else:
        front_img = f'<div style="color:white;padding:20px;">Image not found</div>'
    return f"""
    <div class="card-wrap" onclick="document.getElementById('modal-{card_id}').style.display='flex'">
      <div class="card {css_class}" style="border:6px solid {border_color};box-shadow:0 0 12px {glow_color},0 0 24px {glow_color};border-radius:18px;display:flex;align-items:center;justify-content:center;overflow:hidden;">
        {front_img}
      </div>
    </div>
    <div id="modal-{card_id}" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.6);z-index:9999;justify-content:center;align-items:center;" onclick="this.style.display='none'">
        <div style="background:#FEFDD0;border-radius:20px;padding:28px;max-width:320px;width:90%;border:3px solid {border_color};box-shadow:0 0 30px {glow_color};text-align:center;" onclick="event.stopPropagation()">
            <img src="data:image/png;base64,{image_base64}" style="width:180px;border-radius:12px;margin-bottom:16px;" />
            <div style="font-family:'Luckiest Guy',cursive;font-size:20px;color:#5a7fa8;margin-bottom:8px;">{card['rarity']}</div>
            <div style="font-family:'Fredoka One',cursive;font-size:16px;color:#8ab4d4;">Course: {card['course']}</div>
            <div style="margin-top:16px;font-family:'Fredoka One',cursive;font-size:13px;color:#aac4d8;">Tap outside to close</div>
        </div>
    </div>
    """

# ── 5. Main UI ──────────────────────────────────────────────────────────────

# ── 5. Main UI ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<h2 style='color:#5a7fa8; font-family:Luckiest Guy,cursive;'>Menu</h2>",
        unsafe_allow_html=True
    )
    page = st.radio(
        "Go to",
        ["Check In", "My Collection"],
        label_visibility="collapsed"
    )

if page == "Check In":
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Luckiest+Guy&display=swap');
    .pokemon-logo {
        font-family: 'Luckiest Guy', cursive;
        font-size: 80px;
        color: #ffcb05;
        letter-spacing: 3px;
        display: inline-block;
        transform: rotate(-4deg);
        text-shadow:
            -4px -4px 0 #2a75bb,
             4px -4px 0 #2a75bb,
            -4px  4px 0 #2a75bb,
             4px  4px 0 #2a75bb,
             0px  10px 0 #1b4f9c;
    }
    </style>
    <div class="pokemon-logo">Schedulémon</div>
    """, unsafe_allow_html=True)

    st.markdown("<h2>Collect lecture cards by showing up and staying focused</h2>", unsafe_allow_html=True)

    st.markdown("<p style='color:#5a7fa8; font-family:Luckiest Guy,cursive; font-size:22px;'>🔥 Current streaks:</p>", unsafe_allow_html=True)
    for course, value in st.session_state.streaks.items():
        st.markdown(
            f"<p style='color:#5a7fa8; font-family:Luckiest Guy,cursive; font-size:18px;'>{course}: {value}</p>",
            unsafe_allow_html=True
        )

    st.markdown("<p style='color:#5a7fa8; font-family:Luckiest Guy,cursive; font-size:22px;'>📅 Today's Schedule:</p>", unsafe_allow_html=True)
    
    for cls in schedule:
        active = is_class_active(cls["course"])
        border_color = "#4fa46d" if active else "#BED9F4"
        glow = "0 0 16px rgba(79,164,109,0.6)" if active else "none"
        badge_html = '<span style="background:#d8f6df;color:#4fa46d;font-size:12px;padding:4px 10px;border-radius:10px;margin-left:8px;font-family:Luckiest Guy,cursive;display:inline-block;">LIVE NOW</span>' if active else ""

        st.markdown(f"""
            <div style="background:#FEFDD0;padding:18px;border-radius:20px;margin-bottom:14px;border:2px solid {border_color};box-shadow:{glow};">
                <div style="font-size:22px;font-weight:700;color:#5a7fa8;font-family:'Luckiest Guy',cursive;letter-spacing:1px;">
                    {cls['course']} {badge_html}
                </div>
                <div style="font-size:15px;color:#8ab4d4;margin-top:6px;font-family:'Fredoka One',cursive;">
                    {cls['day']} &bull; {cls['start']} &ndash; {cls['end']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    # Check In Section
    if not st.session_state.checked_in:
        st.markdown("<h3 style='font-family:Luckiest Guy,cursive;color:#ffcb05;text-shadow:-4px -4px 0 #2a75bb, 4px -4px 0 #2a75bb, -4px 4px 0 #2a75bb, 4px 4px 0 #2a75bb, 0px 6px 0 #1b4f9c;'>Check In</h3>", unsafe_allow_html=True)
        course_names = [cls["course"] for cls in schedule]
        selected_course = st.selectbox("Choose your class", course_names)

        if st.button("Check In"):
            if is_class_active(selected_course):
                st.session_state.checked_in = True
                st.session_state.selected_course = selected_course
                st.session_state.check_in_time = datetime.now()
                st.rerun()
            else:
                st.error("This class is not active right now.")

    else:
        st.markdown("<h3 style='font-family:Luckiest Guy,cursive;color:#ffcb05;text-shadow:-4px -4px 0 #2a75bb, 4px -4px 0 #2a75bb, -4px 4px 0 #2a75bb, 4px 4px 0 #2a75bb, 0px 6px 0 #1b4f9c;'>Active Session</h3>", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:#FEFDD0;color:#5a7fa8;font-family:Luckiest Guy,cursive;
                    font-size:20px;padding:14px 18px;border-radius:16px;
                    border:2px solid #BED9F4;margin-bottom:12px;">
        🎴 Card pending for {st.session_state.selected_course}
        </div>
        """, unsafe_allow_html=True)

        now = datetime.now()
        elapsed = now - st.session_state.check_in_time
        seconds_stayed = int(elapsed.total_seconds())

        GOAL_SECONDS = 2

        # ✅ Only refresh while timer is still counting
        if seconds_stayed < GOAL_SECONDS:
            st_autorefresh(interval=1000, key="datarefresh")

        progress_value = min(seconds_stayed / GOAL_SECONDS, 1.0)
        st.progress(progress_value)

        remaining_seconds = max(0, GOAL_SECONDS - seconds_stayed)

        st.markdown(f"""
        <p style="color:#5a7fa8;font-family:Luckiest Guy,cursive;font-size:22px;">
        Time in class: {seconds_stayed // 60}m {seconds_stayed % 60}s
        </p>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <p style="color:#5a7fa8;font-family:Luckiest Guy,cursive;font-size:22px;">
        Time remaining: {remaining_seconds // 60}m {remaining_seconds % 60}s
        </p>
        """, unsafe_allow_html=True)

        if seconds_stayed >= GOAL_SECONDS:
            if st.session_state.pending_reward is None:
                new_pull = pull_random_card()
                new_pull["course"] = st.session_state.selected_course
                new_pull["image"] = random.choice(CARD_LIBRARY[new_pull["rarity"]])
                st.session_state.pending_reward = new_pull

            reward = st.session_state.pending_reward

            st.markdown(f"""
            <div style="background:#d8f6df;color:#4fa46d;font-family:Luckiest Guy,cursive;
                        font-size:22px;padding:16px;border-radius:16px;border:2px solid #a7dfb6;">
            🎉 Session Complete! Your card is revealed!
            </div>
            """, unsafe_allow_html=True)

            # ✅ FLIP animation — shows back first, flips to front
            card_html = build_card_html_with_image(reward)
            preview_html = f"""
            <div style="background:linear-gradient(180deg,#BED9F4 0%,#FEFDD0 100%);
                        padding:1rem;border-radius:20px;">
                {CARD_CSS}
                <div class="cards-grid">{card_html}</div>
                {CARD_JS}
            </div>
            """
            components.html(preview_html, height=380)

            if st.button("Claim Card"):
                st.session_state.cards.append(reward)
                st.session_state.streaks[reward["course"]] += 1
                st.session_state.checked_in = False
                st.session_state.check_in_time = None
                st.session_state.pending_reward = None
                st.rerun()

        else:
            # ✅ Show BACK of card while waiting
            back_html = build_card_back_html()
            waiting_html = f"""
            <div style="background:linear-gradient(180deg,#BED9F4 0%,#FEFDD0 100%);
                        padding:1rem;border-radius:20px;">
                {CARD_CSS}
                <div class="cards-grid">{back_html}</div>
            </div>
            """
            components.html(waiting_html, height=380)

            st.markdown("""
            <p style="color:#5a7fa8;font-family:Luckiest Guy,cursive;font-size:20px;">
            Stay in class to reveal your card!
            </p>
            """, unsafe_allow_html=True)

elif page == "My Collection":
    st.markdown("<h1 style='font-family:Luckiest Guy,cursive;color:#ffcb05;text-shadow:-4px -4px 0 #2a75bb, 4px -4px 0 #2a75bb, -4px 4px 0 #2a75bb, 4px 4px 0 #2a75bb, 0px 6px 0 #1b4f9c;'>My Collection</h1>", unsafe_allow_html=True)

    grouped_cards = {
        "common": [], "uncommon": [], "rare": [],
        "dr": [], "ir": [], "ur": [], "sir": []
    }

    for card in st.session_state.cards:
        rarity_key = RARITY_LABELS.get(card["rarity"])
        if rarity_key in grouped_cards:
            grouped_cards[rarity_key].append(card)

    for rarity_folder, cards_in_group in grouped_cards.items():
        st.markdown(
            f"<h3 style='color:#5a7fa8; font-family:Luckiest Guy,cursive; text-transform:uppercase;'>{rarity_folder}</h3>",
            unsafe_allow_html=True
        )

        if cards_in_group:
            all_cards_html = "".join(build_card_html_revealed(c) for c in cards_in_group)
            collection_html = f"""
            <div style='background:linear-gradient(180deg, #BED9F4 0%, #FEFDD0 100%); padding:1rem; border-radius:16px; margin-bottom:20px;'>
                {CARD_CSS}
                <div style='
                    max-height: 420px;
                    overflow-y: auto;
                    padding-right: 8px;
                    scrollbar-width: thin;
                    scrollbar-color: #BED9F4 #FEFDD0;
                '>
                    <div class='cards-grid'>{all_cards_html}</div>
                </div>
                {CARD_JS}
            </div>
            """
            components.html(collection_html, height=460)
        else:
            st.markdown(f"""
            <p style="color:#5a7fa8; font-family:Luckiest Guy,cursive; font-size:18px; margin-bottom:20px;">
            No cards in {rarity_folder} yet.
            </p>
            """, unsafe_allow_html=True)