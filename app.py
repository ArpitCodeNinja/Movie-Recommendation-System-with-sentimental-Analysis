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
# THEME MANAGEMENT
# =============================
if "theme" not in st.session_state:
    st.session_state.theme = "bw"  # default theme: black & white

def toggle_theme():
    # Cycle through themes: bw -> forest -> bw
    if st.session_state.theme == "bw":
        st.session_state.theme = "forest"
    else:
        st.session_state.theme = "bw"

# Theme-specific styles
def get_theme_styles():
    if st.session_state.theme == "bw":
        return {
            "bg": "#000000",
            "card_bg": "#1a1a1a",
            "text": "#ffffff",  # Pure white text
            "text_muted": "#e0e0e0",  # Light gray for muted text
            "border": "#333333",
            "accent": "#ffffff",
            "accent_hover": "#cccccc",
            "gradient": "linear-gradient(135deg, #ffffff 0%, #cccccc 100%)",
            "shadow": "0 10px 25px -5px rgba(255, 255, 255, 0.2)",
            "button_text": "#000000",
            "input_text": "#ffffff",  # White text in inputs
            "input_bg": "#2a2a2a",  # Slightly lighter black for inputs
            "sidebar_bg": "#1a1a1a",
            "link_color": "#ffffff",
        }
    else:  # forest light mode
        return {
            "bg": "#e8f5e9",  # Light forest green background
            "card_bg": "#ffffff",
            "text": "#1b5e20",  # Dark green text
            "text_muted": "#2e7d32",  # Medium green
            "border": "#a5d6a7",  # Light green border
            "accent": "#2e7d32",  # Forest green
            "accent_hover": "#1b5e20",  # Darker green
            "gradient": "linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%)",  # Forest green gradient
            "shadow": "0 10px 25px -5px rgba(46, 125, 50, 0.2)",
            "button_text": "#ffffff",
            "input_text": "#1b5e20",
            "input_bg": "#ffffff",
            "sidebar_bg": "#ffffff",
            "link_color": "#2e7d32",
        }

# =============================
# CUSTOM CSS
# =============================
def apply_custom_styles():
    theme = get_theme_styles()
    
    st.markdown(f"""
    <style>
        /* Main container */
        .stApp {{
            background-color: {theme['bg']};
            color: {theme['text']};
        }}
        
        /* Override Streamlit's default text colors */
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
        .stApp p, .stApp span, .stApp div, .stApp label,
        .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
        .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {{
            color: {theme['text']} !important;
        }}
        
        /* Sidebar styling */
        .css-1d391kg, .stSidebar, [data-testid="stSidebar"] {{
            background-color: {theme['sidebar_bg']} !important;
        }}
        
        .stSidebar .stMarkdown, .stSidebar p, .stSidebar h1, .stSidebar h2, .stSidebar h3,
        .stSidebar h4, .stSidebar h5, .stSidebar h6, .stSidebar label {{
            color: {theme['text']} !important;
        }}
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {theme['bg']};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {theme['accent']};
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {theme['accent_hover']};
        }}
        
        /* DateTime display */
        .datetime-container {{
            background: {theme['card_bg']};
            padding: 10px 20px;
            border-radius: 30px;
            display: inline-block;
            margin-bottom: 20px;
            border: 1px solid {theme['border']};
            color: {theme['text']} !important;
            font-weight: 500;
        }}
        
        /* Movie cards */
        .movie-card {{
            background: {theme['card_bg']};
            border-radius: 16px;
            padding: 12px;
            margin-bottom: 16px;
            border: 1px solid {theme['border']};
            transition: all 0.3s ease;
            box-shadow: {theme['shadow']};
            height: 100%;
            display: flex;
            flex-direction: column;
        }}
        
        .movie-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 20px 30px -10px {theme['accent']}80;
            border-color: {theme['accent']};
        }}
        
        .movie-poster {{
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 10px;
            aspect-ratio: 2/3;
            position: relative;
        }}
        
        .movie-poster img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s ease;
        }}
        
        .movie-card:hover .movie-poster img {{
            transform: scale(1.05);
        }}
        
        .movie-title {{
            font-size: 0.95rem;
            font-weight: 600;
            color: {theme['text']} !important;
            margin-bottom: 8px;
            line-height: 1.3;
            height: 2.6rem;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
        }}
        
        .movie-rating {{
            color: {theme['accent']} !important;
            font-size: 0.85rem;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 4px;
        }}
        
        .movie-year {{
            color: {theme['text_muted']} !important;
            font-size: 0.8rem;
        }}
        
        /* Buttons */
        .stButton > button {{
            background: {theme['gradient']};
            color: {theme['button_text']} !important;
            border: none;
            border-radius: 25px;
            padding: 0.5rem 1.5rem;
            font-weight: 500;
            transition: all 0.3s ease;
            width: 100%;
            border: 1px solid {theme['border']};
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 20px -5px {theme['accent']};
            color: {theme['button_text']} !important;
        }}
        
        /* Sidebar buttons */
        .stSidebar .stButton > button {{
            color: {theme['button_text']} !important;
        }}
        
        /* Link buttons */
        .stLinkButton > a {{
            color: {theme['link_color']} !important;
            background: {theme['card_bg']};
            border: 1px solid {theme['border']};
        }}
        
        /* Headers */
        h1, h2, h3 {{
            background: {theme['gradient']};
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }}
        
        /* Sidebar headers */
        .stSidebar h1, .stSidebar h2, .stSidebar h3 {{
            background: {theme['gradient']};
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        /* Search box and inputs */
        .stTextInput > div > div > input,
        .stSelectbox > div > div,
        .stSlider > div {{
            background-color: {theme['input_bg']} !important;
            color: {theme['input_text']} !important;
            border: 2px solid {theme['border']} !important;
            border-radius: 30px !important;
            padding: 0.75rem 1.5rem !important;
            font-size: 1rem !important;
        }}
        
        .stTextInput > div > div > input::placeholder {{
            color: {theme['text_muted']} !important;
            opacity: 0.7;
        }}
        
        .stTextInput > div > div > input:focus {{
            border-color: {theme['accent']} !important;
            box-shadow: 0 0 0 3px {theme['accent']}40 !important;
        }}
        
        /* Selectbox */
        .stSelectbox > div > div {{
            background-color: {theme['input_bg']} !important;
            color: {theme['input_text']} !important;
            border-radius: 20px !important;
        }}
        
        .stSelectbox > div > div > div {{
            color: {theme['input_text']} !important;
        }}
        
        /* Slider */
        .stSlider > div > div {{
            color: {theme['text']} !important;
        }}
        
        /* Divider */
        hr {{
            border-color: {theme['border']};
            margin: 2rem 0;
        }}
        
        /* Theme toggle button */
        .theme-toggle {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 1000;
            background: {theme['gradient']};
            border: none;
            border-radius: 50px;
            padding: 10px 20px;
            color: {theme['button_text']} !important;
            font-weight: 600;
            cursor: pointer;
            box-shadow: {theme['shadow']};
            transition: all 0.3s ease;
            border: 1px solid {theme['border']};
        }}
        
        .theme-toggle:hover {{
            transform: scale(1.05);
            box-shadow: 0 15px 30px -5px {theme['accent']};
        }}
        
        /* Loading animation */
        @keyframes pulse {{
            0% {{ opacity: 0.6; }}
            50% {{ opacity: 1; }}
            100% {{ opacity: 0.6; }}
        }}
        
        .loading {{
            animation: pulse 1.5s ease-in-out infinite;
        }}
        
        /* Backdrop image */
        .backdrop-container {{
            border-radius: 20px;
            overflow: hidden;
            margin: 20px 0;
            position: relative;
        }}
        
        .backdrop-container img {{
            width: 100%;
            max-height: 300px;
            object-fit: cover;
        }}
        
        .backdrop-overlay {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(to top, {theme['bg']}, transparent);
            height: 50%;
        }}
        
        /* Genre tags */
        .genre-tag {{
            background: {theme['card_bg']};
            padding: 0.3rem 1rem;
            border-radius: 20px;
            margin-right: 0.5rem;
            display: inline-block;
            margin-bottom: 0.5rem;
            border: 1px solid {theme['border']};
            color: {theme['text']} !important;
            font-size: 0.9rem;
        }}
        
        /* Error and info messages */
        .stAlert {{
            background-color: {theme['card_bg']} !important;
            color: {theme['text']} !important;
            border: 1px solid {theme['border']} !important;
            border-radius: 10px !important;
        }}
        
        .stAlert > div {{
            color: {theme['text']} !important;
        }}
        
        /* Info boxes */
        .stInfo {{
            background-color: {theme['card_bg']} !important;
            color: {theme['text']} !important;
        }}
        
        /* Metrics */
        .stMetric {{
            background-color: {theme['card_bg']};
            color: {theme['text']} !important;
        }}
        
        .stMetric label {{
            color: {theme['text_muted']} !important;
        }}
        
        .stMetric .metric-value {{
            color: {theme['text']} !important;
        }}
        
        /* Specific fixes for black & white mode */
        {'''
        /* Black & White specific overrides */
        .stApp[data-theme="bw"] .stMarkdown,
        .stApp[data-theme="bw"] .stMarkdown p,
        .stApp[data-theme="bw"] .stMarkdown h1,
        .stApp[data-theme="bw"] .stMarkdown h2,
        .stApp[data-theme="bw"] .stMarkdown h3,
        .stApp[data-theme="bw"] .stMarkdown h4,
        .stApp[data-theme="bw"] .stMarkdown h5,
        .stApp[data-theme="bw"] .stMarkdown h6 {{
            color: #ffffff !important;
        }}
        ''' if st.session_state.theme == "bw" else ''}
        
        /* Ensure all text in sidebar is white in BW mode */
        {'''
        .stSidebar .stMarkdown,
        .stSidebar p,
        .stSidebar h1,
        .stSidebar h2,
        .stSidebar h3,
        .stSidebar h4,
        .stSidebar h5,
        .stSidebar h6,
        .stSidebar label,
        .stSidebar div {{
            color: #ffffff !important;
        }}
        ''' if st.session_state.theme == "bw" else ''}
    </style>
    """, unsafe_allow_html=True)

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
    
    theme = get_theme_styles()
    
    # Create a placeholder that will be updated
    datetime_placeholder = st.empty()
    
    with datetime_placeholder.container():
        st.markdown(f"""
        <div style='text-align: center; margin-bottom: 20px;'>
            <div class='datetime-container'>
                <span style='font-size: 1.1rem; margin-right: 10px; color: {theme["text"]} !important;'>📅 {formatted_date}</span>
                <span style='font-size: 1.1rem; color: {theme["text"]} !important;'>⏰ {formatted_time}</span>
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
# =============================
# THEME TOGGLE BUTTON
# =============================
col1, col2, col3 = st.columns([4, 1, 1])
with col2:
    if st.button("🎨 Switch Theme", key="theme_toggle"):
        toggle_theme()
        st.rerun()

with col3:
    # Theme indicator
    theme = get_theme_styles()
    theme_name = "Black & White" if st.session_state.theme == "bw" else "Light Mode"
    st.markdown(f"""
    <div style='background: {theme["card_bg"]}; 
                padding: 8px 15px; 
                border-radius: 20px; 
                text-align: center;
                border: 1px solid {theme["border"]};'>
        <span style='color: {theme["text"]} !important;'>{theme_name}</span>
    </div>
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
        <h1 style='font-size: 2rem; margin: 0;'>🎬</h1>
        <h3 style='margin: 0;'>Movie Recommender</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    if st.button("🏠 Home", use_container_width=True):
        goto_home()

    st.markdown("---")

    st.markdown("### 💬 Movie Analysis Tools 💬")

    st.link_button(
        "🎭 Open Sentiment Analysis 🎭",
        "https://e0dc0435984884f137.gradio.live"
    )

    st.markdown("---")
    st.markdown("### 🎯 Feed Category")
    home_category = st.selectbox(
        "Select category",
        ["trending", "popular", "top_rated", "now_playing", "upcoming"],
        index=0,
        label_visibility="collapsed"
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
<div style='text-align: center; padding: 2rem 0;'>
    <h1>🎬 Movie Recommender</h1>
    <p style='color: #94a3b8; font-size: 1.1rem;'>Discover your next favorite movie</p>
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