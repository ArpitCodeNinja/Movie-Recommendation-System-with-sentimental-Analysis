import requests
import streamlit as st
from datetime import datetime


# =============================
# CONFIG
# =============================
API_BASE = "https://movie-rec-466x.onrender.com" or "http://127.0.0.1:8000"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(
    page_title="Movie Recommender", 
    page_icon="🎬", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================
# THEME CONFIGURATION (CRYSTAL-LUMINA)
# =============================
def get_theme_styles():
    """Unified Signature Design: Crystal-Lumina (Ultra-Premium White)"""
    return {
        "bg": "#fdfdfd",
        "card_bg": "rgba(255, 255, 255, 0.75)",
        "card_blur": "blur(30px)",
        "text": "#1e293b",
        "text_muted": "rgba(30, 41, 59, 0.65)",
        "border": "rgba(0, 0, 0, 0.04)",
        "accent": "#0ea5e9",
        "accent_hover": "#d946ef",
        "gradient": "linear-gradient(135deg, #0ea5e9 0%, #d946ef 50%, #f59e0b 100%)",
        "shadow": "0 25px 60px rgba(0, 0, 0, 0.05), 0 5px 15px rgba(0, 0, 0, 0.02)",
        "button_text": "#ffffff",
        "input_text": "#2563eb",
        "input_bg": "rgba(255, 255, 255, 0.95)",
        "sidebar_bg": "#ffffff",
        "link_color": "#d946ef",
    }

# =============================
def apply_custom_styles():
    theme = get_theme_styles()
    
    # Base CSS with placeholders
    css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&family=Space+Grotesk:wght@300;500;700&display=swap');

        /* Main container */
        .stApp {
            background: [BG] !important;
            color: [TEXT];
            font-family: 'Space Grotesk', sans-serif !important;
            background-image: 
                radial-gradient(at 0% 0%, rgba(109, 40, 217, 0.2) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(219, 39, 119, 0.2) 0px, transparent 50%),
                radial-gradient(at 50% 50%, rgba(37, 99, 235, 0.1) 0px, transparent 70%) !important;
            color: [TEXT] !important;
            font-family: 'Space Grotesk', sans-serif !important;
        }

        .stApp::before {
            content: "";
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: 
                radial-gradient(at 0% 0%, rgba(14, 165, 233, 0.15) 0, transparent 50%), 
                radial-gradient(at 100% 0%, rgba(217, 70, 239, 0.15) 0, transparent 50%), 
                radial-gradient(at 50% 100%, rgba(245, 158, 11, 0.1) 0, transparent 50%);
            z-index: -1;
            pointer-events: none;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: [SIDEBAR_BG] !important;
            border-right: 1px solid [BORDER] !important;
            box-shadow: 10px 0 30px rgba(0,0,0,0.02);
        }

        section[data-testid="stSidebar"] .stMarkdown p {
            color: [TEXT] !important;
        }

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: transparent;
        }
        
        ::-webkit-scrollbar-thumb {
            background: [GRADIENT];
            border-radius: 10px;
        }
        
        /* Typography */
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
        .stApp p, .stApp li, .stApp label, .stMarkdown p {
            color: [TEXT] !important;
            font-family: 'Space Grotesk', sans-serif !important;
        }
        
        /* DateTime display */
        .datetime-container {
            background: [CARD_BG];
            backdrop-filter: [CARD_BLUR];
            padding: 10px 25px;
            border-radius: 50px;
            display: inline-block;
            margin-bottom: 20px;
            border: 1px solid [BORDER];
            color: [TEXT] !important;
            font-weight: 600;
            box-shadow: [SHADOW];
        }
        
        /* Movie cards with Crystal Liquid Border */
        .movie-card {
            background: [CARD_BG] !important;
            backdrop-filter: [CARD_BLUR] !important;
            border-radius: 20px !important;
            padding: 12px;
            margin-bottom: 25px;
            transition: all 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);
            box-shadow: [SHADOW];
            height: 100%;
            display: flex;
            flex-direction: column;
            border: 3px solid transparent !important;
            background-image: linear-gradient([CARD_BG], [CARD_BG]), 
                               conic-gradient(from var(--border-angle, 0deg), #0ea5e9, #d946ef, #f59e0b, #0ea5e9) !important;
            background-origin: border-box !important;
            background-clip: padding-box, border-box !important;
        }

        @property --border-angle {
          syntax: '<angle>';
          initial-value: 0deg;
          inherits: false;
        }

        @keyframes border-run {
          to { --border-angle: 360deg; }
        }

        .movie-card:hover {
            transform: translateY(-10px) scale(1.02);
            animation: border-run 4s linear infinite !important;
            box-shadow: 0 30px 60px rgba(0,0,0,0.12) !important;
        }
        
        .movie-poster {
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 12px;
            aspect-ratio: 2/3;
            position: relative;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        }
        
        .movie-poster img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.5s ease;
        }
        
        .movie-card:hover .movie-poster img {
            transform: scale(1.08);
        }
        
        .movie-title {
            font-size: 1rem;
            font-weight: 700;
            color: [TEXT] !important;
            margin-bottom: 6px;
            line-height: 1.2;
            height: 2.4rem;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            font-family: 'Montserrat', sans-serif;
        }
        
        .movie-rating {
            color: [ACCENT] !important;
            font-size: 0.9rem;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 4px;
            font-weight: 700;
        }
        
        .movie-year {
            color: [TEXT_MUTED] !important;
            font-size: 0.85rem;
            font-weight: 500;
        }
        
        /* Buttons - Prismatic Pill Style */
        .stButton > button {
            background: [GRADIENT];
            color: [BUTTON_TEXT] !important;
            border: none;
            border-radius: 50px;
            padding: 0.7rem 2.5rem;
            font-weight: 700;
            letter-spacing: 1px;
            transition: all 0.4s ease;
            width: 100%;
            box-shadow: 0 4px 15px [ACCENT]40;
            text-transform: uppercase;
            font-size: 0.85rem;
            font-family: 'Montserrat', sans-serif;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px [ACCENT]60;
            filter: saturate(1.2);
        }
        
        /* Sidebar buttons */
        .stSidebar .stButton > button {
            color: [BUTTON_TEXT] !important;
        }
        
        /* Link buttons */
        .stLinkButton > a {
            color: [LINK_COLOR] !important;
            background: [CARD_BG];
            border: 1px solid [BORDER];
        }
        
        /* Headers - Montserrat 900 Luxury */
        h1, h2, h3 {
            font-family: 'Montserrat', sans-serif !important;
            background: [GRADIENT];
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 900 !important;
            letter-spacing: -1.5px !important;
            text-transform: uppercase;
        }
        
        /* Sidebar headers */
        .stSidebar h1, .stSidebar h2, .stSidebar h3 {
            background: [GRADIENT];
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* UNIFIED INPUT & SELECTBOX VISIBILITY OVERRIDE (ROYAL BLUE) */
        .stTextInput input, 
        .stSelectbox div[data-baseweb="select"] *, 
        .stSelectbox input,
        .stSlider label,
        .stSelectbox label {
            color: #2563eb !important;
            -webkit-text-fill-color: #2563eb !important;
            opacity: 1 !important;
            visibility: visible !important;
        }

        /* Ensure the background stays solid white for these containers */
        .stTextInput > div > div, 
        .stSelectbox > div > div,
        .stSlider > div {
            background-color: #ffffff !important;
            border: 1px solid [BORDER] !important;
            border-radius: 12px !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
        }
        
        /* Dropdown arrow */
        .stSelectbox svg {
            fill: #2563eb !important;
        }
        
        /* Dropdown options (popover) */
        div[data-baseweb="popover"] ul li * {
            color: #2563eb !important;
            background-color: transparent !important;
        }
 
        /* Slider */
        .stSlider > div > div {
            color: [TEXT] !important;
        }
        
        /* Divider */
        hr {
            border-color: [BORDER];
            opacity: 0.1;
        }
        
        /* Theme toggle button */
        .theme-toggle {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 1000;
            background: [GRADIENT];
            border: none;
            border-radius: 50px;
            padding: 10px 20px;
            color: [BUTTON_TEXT] !important;
            font-weight: 600;
            cursor: pointer;
            box-shadow: [SHADOW];
            transition: all 0.3s ease;
            border: 1px solid [BORDER];
        }
        
        .theme-toggle:hover {
            transform: scale(1.05);
            box-shadow: 0 15px 30px -5px [ACCENT];
        }
        
        /* Loading animation */
        @keyframes pulse {
            0% { opacity: 0.6; }
            50% { opacity: 1; }
            100% { opacity: 0.6; }
        }
        
        .loading {
            animation: pulse 1.5s ease-in-out infinite;
        }
        
        /* Backdrop image */
        .backdrop-container {
            border-radius: 20px;
            overflow: hidden;
            margin: 20px 0;
            position: relative;
        }
        
        .backdrop-container img {
            width: 100%;
            max-height: 300px;
            object-fit: cover;
        }
        
        .backdrop-overlay {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(to top, [BG], transparent);
            height: 50%;
        }
        
        /* Genre tags */
        .genre-tag {
            background: [GRADIENT];
            padding: 0.4rem 1.2rem;
            border-radius: 50px;
            margin-right: 0.6rem;
            display: inline-block;
            margin-bottom: 0.6rem;
            color: [BUTTON_TEXT] !important;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }
        
        /* Error and info messages */
        .stAlert {
            background: [CARD_BG] !important;
            backdrop-filter: [CARD_BLUR];
            border: 1px solid [BORDER] !important;
            border-radius: 15px !important;
        }
        
        .stAlert > div {
            color: [TEXT] !important;
        }
        
        /* Info boxes */
        .stInfo {
            background-color: [CARD_BG] !important;
            color: [TEXT] !important;
        }
        
        /* Metrics */
        [data-testid="stMetricValue"] {
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 900 !important;
            color: [TEXT] !important;
        }
        
        .stMetric label {
            color: [TEXT_MUTED] !important;
        }
        
        .stMetric .metric-value {
            color: [TEXT] !important;
        }
    </style>
    """
    
    # Replace placeholders with theme values
    css = css.replace("[BG]", theme['bg'])
    css = css.replace("[CARD_BG]", theme['card_bg'])
    css = css.replace("[CARD_BLUR]", theme['card_blur'])
    css = css.replace("[TEXT]", theme['text'])
    css = css.replace("[TEXT_MUTED]", theme['text_muted'])
    css = css.replace("[BORDER]", theme['border'])
    css = css.replace("[ACCENT]", theme['accent'])
    css = css.replace("[GRADIENT]", theme['gradient'])
    css = css.replace("[SHADOW]", theme['shadow'])
    css = css.replace("[BUTTON_TEXT]", theme['button_text'])
    css = css.replace("[LINK_COLOR]", theme['link_color'])
    css = css.replace("[INPUT_BG]", theme['input_bg'])
    css = css.replace("[INPUT_TEXT]", theme['input_text'])
    css = css.replace("[SIDEBAR_BG]", theme['sidebar_bg'])
        
    st.markdown(css, unsafe_allow_html=True)

# Apply styles
apply_custom_styles()

# =============================
# DATE AND TIME DISPLAY
# =============================
def display_datetime():
    # Get current time
    now = datetime.now()
    formatted_date = now.strftime("%A, %B %d, %Y")
    formatted_time = now.strftime("%I:%M:%S %p")
    
    # Using fixed Lumina colors for the single theme
    # Create a placeholder that will be updated
    datetime_placeholder = st.empty()
    
    with datetime_placeholder.container():
        st.markdown(f"""
        <div style='text-align: center; margin-bottom: 20px;'>
            <div class='datetime-container'>
                <span style='font-size: 1.1rem; margin-right: 10px; color: #1e293b !important;'>📅 {formatted_date}</span>
                <span style='font-size: 1.1rem; color: #1e293b !important;'>⏰ {formatted_time}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Add a small refresh counter to force updates
    if "time_counter" not in st.session_state:
        st.session_state.time_counter = 0
    
    # Auto-refresh every second using JavaScript
    st.markdown("""
    <script>
        function updateTime() {
            var elements = document.getElementsByClassName('datetime-container');
            if (elements.length > 0) {
                var now = new Date();
                var dateStr = now.toLocaleDateString('en-US', { 
                    weekday: 'long', 
                    year: 'numeric', 
                    month: 'long', 
                    day: 'numeric' 
                });
                var timeStr = now.toLocaleTimeString('en-US', { 
                    hour12: true,
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit'
                });
                elements[0].innerHTML = '<span style=\"font-size: 1.1rem; margin-right: 10px;\">📅 ' + dateStr + '</span>' +
                                       '<span style=\"font-size: 1.1rem;\">⏰ ' + timeStr + '</span>';
            }
            setTimeout(updateTime, 1000);
        }
        setTimeout(updateTime, 1000);
    </script>
    """, unsafe_allow_html=True)
# Display date and time
display_datetime()

# =============================
# STATE + ROUTING (single-file pages)
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"  # home | details | sentiment
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")
if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except:
        pass


def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()


# =============================
# API HELPERS
# =============================
@st.cache_data(ttl=30)
def api_get_json(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"


def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.info("No movies to show.")
        return

    rows = (len(cards) + cols - 1) // cols
    idx = 0
    for r in range(rows):
        colset = st.columns(cols)
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]
            idx += 1

            tmdb_id = m.get("tmdb_id")
            title = m.get("title", "Untitled")
            poster = m.get("poster_url")
            year = m.get("release_date", "")[:4] if m.get("release_date") else ""
            
            # Safely handle vote_average
            rating = m.get("vote_average")
            rating_display = f"{float(rating):.1f}" if rating is not None else ""

            with colset[c]:
                # Movie card HTML
                rating_html = f"<div class='movie-rating'>⭐ {rating_display}</div>" if rating_display else ""
                year_html = f"<div class='movie-year'>{year}</div>" if year else ""
                
                poster_url = poster if poster else "https://via.placeholder.com/500x750?text=No+Poster"
                
                card_html = f"""
                <div class='movie-card'>
                    <div class='movie-poster'>
                        <img src='{poster_url}' alt='{title}'>
                    </div>
                    <div class='movie-title'>{title}</div>
                    {rating_html}
                    {year_html}
                </div>
                """
                
                st.markdown(card_html, unsafe_allow_html=True)
                
                if st.button("🎬 View Details", key=f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}"):
                    if tmdb_id:
                        goto_details(tmdb_id)


def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append(
                {
                    "tmdb_id": tmdb["tmdb_id"],
                    "title": tmdb.get("title") or x.get("title") or "Untitled",
                    "poster_url": tmdb.get("poster_url"),
                    "release_date": tmdb.get("release_date"),
                    "vote_average": tmdb.get("vote_average"),
                }
            )
    return cards


def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    """
    Returns:
      suggestions: list[(label, tmdb_id)]
      cards: list[{tmdb_id,title,poster_url}]
    """
    keyword_l = keyword.strip().lower()

    if isinstance(data, dict) and "results" in data:
        raw = data.get("results") or []
        raw_items = []
        for m in raw:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                    "release_date": m.get("release_date", ""),
                    "vote_average": m.get("vote_average", 0),
                }
            )

    elif isinstance(data, list):
        raw_items = []
        for m in data:
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title = (m.get("title") or "").strip()
            poster_url = m.get("poster_url")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": poster_url,
                    "release_date": m.get("release_date", ""),
                    "vote_average": m.get("vote_average", 0),
                }
            )
    else:
        return [], []

    matched = [x for x in raw_items if keyword_l in x["title"].lower()]
    final_list = matched if matched else raw_items

    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    cards = [
        {
            "tmdb_id": x["tmdb_id"], 
            "title": x["title"], 
            "poster_url": x["poster_url"],
            "release_date": x["release_date"],
            "vote_average": x["vote_average"]
        }
        for x in final_list[:limit]
    ]
    return suggestions, cards


# =============================
# SIDEBAR
# =============================


home_category = "trending"
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <h1 style='font-size: 1.8rem; margin: 0;'>🌌</h1>
        <h2 style='margin: 0; font-size: 1.4rem; letter-spacing: 1px;'>LUMINA ENGINE</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    if st.button("🏠 Home", use_container_width=True):
        goto_home()

    st.markdown("---")

    st.markdown("### 💬 Movie Analysis Tools 💬")

    st.link_button(
        "🎭 Open Sentiment Analysis 🎭",
        "https://arpitsaxena856-movie-sentiment-analysis.hf.space/"
    )

    st.markdown("---")
    st.markdown("### 🎯 Feed Category")
    home_category = st.selectbox(
        "Select category",
        ["trending", "popular", "top_rated", "now_playing", "upcoming"],
        index=0
    )
    
    grid_cols = st.slider("Grid columns", 4, 8, 6)
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #94a3b8; font-size: 0.8rem;'>
        Made with ❤️ using Streamlit
    </div>
    """, unsafe_allow_html=True)

# =============================
# HEADER
# =============================
st.markdown("""
<div style='text-align: center; padding: 3rem 0;'>
    <h1 style='font-size: 3.8rem; margin-bottom: 0.5rem; letter-spacing: -2px;'>🎬 MOVIE DISCOVERY ENGINE</h1>
    <p style='color: #64748b; font-size: 1.2rem; font-weight: 600; letter-spacing: 2px; text-transform: uppercase;'>
        The Future of Cinematic Exploration
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# VIEW: HOME
# ==========================================================
if st.session_state.view == "home":
    typed = st.text_input(
        "🔍 Search movies",
        placeholder="Type movie title (e.g., Avengers, Batman, Inception...)",
        help="Start typing to search for movies"
    )

    if typed.strip():
        if len(typed.strip()) < 2:
            st.info("💡 Type at least 2 characters to see suggestions")
        else:
            with st.spinner("🔍 Searching movies..."):
                data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})

            if err or data is None:
                st.error(f"Search failed: {err}")
            else:
                suggestions, cards = parse_tmdb_search_to_cards(
                    data, typed.strip(), limit=24
                )

                if suggestions:
                    st.markdown("### 📝 Quick Select")
                    labels = ["-- Select a movie --"] + [s[0] for s in suggestions]
                    selected = st.selectbox("Suggestions", labels, index=0, label_visibility="collapsed")

                    if selected != "-- Select a movie --":
                        label_to_id = {s[0]: s[1] for s in suggestions}
                        goto_details(label_to_id[selected])
                else:
                    st.info("No suggestions found. Try another keyword.")

                st.markdown("### 🎬 Search Results")
                poster_grid(cards, cols=grid_cols, key_prefix="search_results")

        st.stop()

    # HOME FEED MODE
    category_display = str(home_category).replace('_', ' ').title() if home_category else "Movies"
    st.markdown(f"### 📈 {category_display}")
    
    with st.spinner("Loading movies..."):
        home_cards, err = api_get_json(
            "/home", params={"category": home_category, "limit": 24}
        )
    
    if err or not home_cards:
        st.error(f"Home feed failed: {err or 'Unknown error'}")
        st.stop()

    poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")

# ==========================================================
# VIEW: DETAILS
# ==========================================================
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("No movie selected.")
        if st.button("← Back to Home"):
            goto_home()
        st.stop()

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("← Back to Home", use_container_width=True):
            goto_home()

    with st.spinner("Loading movie details..."):
        data, err = api_get_json(f"/movie/id/{tmdb_id}")
    
    if err or not data:
        st.error(f"Could not load details: {err or 'Unknown error'}")
        st.stop()

    # Display backdrop if available
    if data.get("backdrop_url"):
        st.markdown(f"""
        <div class='backdrop-container'>
            <img src='{data["backdrop_url"]}' alt='Backdrop'>
            <div class='backdrop-overlay'></div>
        </div>
        """, unsafe_allow_html=True)

    # Main content
    left, right = st.columns([1, 2], gap="large")

    with left:
        st.markdown("<div class='movie-card'>", unsafe_allow_html=True)
        if data.get("poster_url"):
            st.image(data["poster_url"], use_column_width=True)
        else:
            st.markdown("""
            <div style='background: #1e293b; border-radius: 12px; padding: 2rem; text-align: center;'>
                🖼️ No poster available
            </div>
            """, unsafe_allow_html=True)
        
        # Safely handle vote_average
        vote_average = data.get("vote_average")
        if vote_average is not None:
            st.markdown(f"<div class='movie-rating' style='justify-content: center;'>⭐ {float(vote_average):.1f}/10</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown(f"<h1>{data.get('title','')}</h1>", unsafe_allow_html=True)
        
        # Movie metadata with safe handling
        release = data.get("release_date")
        release_year = release[:4] if release and len(release) >= 4 else "N/A"
        
        genres = data.get("genres", [])
        genres_str = ", ".join([g["name"] for g in genres]) if genres else "Genres not specified"
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Release Year", release_year)
        with col2:
            runtime = data.get("runtime")
            st.metric("Runtime", f"{runtime} min" if runtime else "N/A")
        with col3:
            status = data.get("status", "N/A")
            st.metric("Status", status)
        
        st.markdown("---")
        st.markdown("### 📖 Overview")
        st.write(data.get("overview") or "No overview available.")
        
        if genres:
            st.markdown("### 🎭 Genres")
            genre_html = ""
            for genre in genres:
                genre_html += f"<span class='genre-tag'>{genre['name']}</span>"
            st.markdown(genre_html, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 🎯 You Might Also Like")

    title = (data.get("title") or "").strip()
    if title:
        with st.spinner("Finding recommendations..."):
            bundle, err2 = api_get_json(
                "/movie/search",
                params={"query": title, "tfidf_top_n": 12, "genre_limit": 12},
            )

        if not err2 and bundle:
            tfidf_recs = bundle.get("tfidf_recommendations")
            if tfidf_recs:
                st.markdown("### 📊 Based on Plot Similarity")
                poster_grid(
                    to_cards_from_tfidf_items(tfidf_recs),
                    cols=grid_cols,
                    key_prefix="details_tfidf",
                )

            genre_recs = bundle.get("genre_recommendations", [])
            if genre_recs:
                st.markdown("### 🎭 Based on Genre")
                poster_grid(
                    genre_recs,
                    cols=grid_cols,
                    key_prefix="details_genre",
                )
            
            if not tfidf_recs and not genre_recs:
                st.info("No recommendations available for this movie.")
        else:
            st.info("Showing Genre-based recommendations...")
            genre_only, err3 = api_get_json(
                "/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18}
            )
            if not err3 and genre_only:
                poster_grid(
                    genre_only, cols=grid_cols, key_prefix="details_genre_fallback"
                )
            else:
                st.warning("No recommendations available right now.")
    else:
        st.warning("No title available to compute recommendations.")