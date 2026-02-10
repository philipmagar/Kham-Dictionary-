import streamlit as st
import json
from difflib import get_close_matches
import os
import random

# Page configuration
st.set_page_config(
    page_title="English to Kham Translator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Premium Design System)
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">

<style>
    /* Global Styles */
    :root {
        --primary: #0d9488; /* Teal */
        --secondary: #0f766e; /* Dark Teal */
        --accent: #f59e0b; /* Amber/Gold */
        --bg-dark: #042f2e; /* Deep Teal Black */
        --card-bg: rgba(20, 184, 166, 0.05);
        --text-main: #f0fdfa;
        --text-dim: #99f6e4;
    }

    .main {
        background-color: var(--bg-dark);
        color: var(--text-main);
        font-family: 'Inter', sans-serif;
    }

    /* Background Animation */
    .stApp {
        background: radial-gradient(circle at top right, #134e4a, #042f2e);
        background-attachment: fixed;
    }

    /* Typography Overrides */
    h1, h2, h3, .stHeader {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em;
    }

    /* Glassmorphism Card for Results */
    .glass-card {
        background: var(--card-bg);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 40px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        margin-top: 20px;
        transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    .glass-card:hover {
        transform: translateY(-5px);
        border-color: rgba(99, 102, 241, 0.4);
    }

    /* Hero Section */
    .hero-container {
        text-align: center;
        padding: 60px 0 40px 0;
    }

    .hero-title {
        font-size: 3.5rem !important;
        background: linear-gradient(135deg, #f0fdfa 0%, #2dd4bf 50%, #0d9488 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }

    .hero-subtitle {
        font-size: 1.2rem !important;
        color: var(--text-dim);
        font-weight: 300 !important;
        max-width: 600px;
        margin: 0 auto;
    }

    /* Search Bar Styling */
    div[data-baseweb="input"] {
        background-color: rgba(30, 41, 59, 0.5) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        transition: all 0.3s ease;
    }

    div[data-baseweb="input"]:focus-within {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
    }

    input {
        color: white !important;
        font-size: 1.1rem !important;
        padding: 12px 20px !important;
    }

    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 30px !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        width: 100% !important;
        box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.3) !important;
    }

    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 20px 25px -5px rgba(99, 102, 241, 0.4) !important;
    }

    /* Metrics Styling */
    [data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
        color: var(--secondary) !important;
    }

    /* Hide Streamlit components for cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(4, 47, 46, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Translation result styling */
    .result-label {
        color: var(--text-dim);
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 4px;
    }
    .result-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: white;
        margin-bottom: 20px;
    }
    .kham-result {
        color: var(--accent);
        font-family: 'Outfit', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# Load the Kham dictionary
@st.cache_data
def load_dictionary():
    """Load the Kham dictionary from JSON file"""
    try:
        json_path = os.path.join(os.path.dirname(__file__), 'kham_index.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Dictionary file 'kham_index.json' not found!")
        return {}
    except json.JSONDecodeError:
        st.error("Error reading dictionary file!")
        return {}

def find_translation(word, dictionary):
    """Find translation for a given English word"""
    word_lower = word.lower().strip()
    
    # Precise direct match
    for key in dictionary.keys():
        if key.lower() == word_lower:
            return dictionary[key], key, True
    
    # Partial match (starting with)
    for key in dictionary.keys():
        if key.lower().startswith(word_lower):
            return dictionary[key], key, True
            
    # Substring match
    for key in dictionary.keys():
        if word_lower in key.lower():
            return dictionary[key], key, True
    
    return None, None, False

def get_suggestions(word, dictionary, n=5):
    """Get close matches for a word"""
    all_keys = list(dictionary.keys())
    matches = get_close_matches(word, all_keys, n=n, cutoff=0.5)
    return matches

def main():
    kham_dict = load_dictionary()
    
    if not kham_dict:
        st.stop()
    
    # Sidebar Enrichment
    with st.sidebar:
        st.markdown("<h2 style='text-align: center; color: #5eead4;'>Kham Explorer</h2>", unsafe_allow_html=True)
        st.markdown("""
        The **Kham language** is a beautiful Tibeto-Burman language spoken in the hills of Nepal.
        
        This dictionary aims to preserve the linguistic heritage of the Magar community.
        """)
        
        st.divider()
        
        # Word of the Day
        st.markdown("### Word of the Day")
        random_key = random.choice(list(kham_dict.keys()))
        st.info(f"**English:** {random_key}\n\n**Kham:** {kham_dict[random_key]}")
        
        st.divider()
        st.metric("Dictionary Capacity", f"{len(kham_dict):,} words", help="Total entries currently in the index")
        
    # Hero Section
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">English to Kham</h1>
        <p class="hero-subtitle">Preserving the linguistic soul of Nepal's remote hills. Search over 3,000 entries with fuzzy matching intelligence.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Centered Search Layout
    col_l, col_c, col_r = st.columns([1, 4, 1])
    
    with col_c:
        search_word = st.text_input(
            "",
            placeholder="Type an English word to discover its Kham equivalent...",
            label_visibility="collapsed",
            key="search_input"
        )
        
        btn_col_l, btn_col_c, btn_col_r = st.columns([1, 1, 1])
        with btn_col_c:
            search_button = st.button("Translate Now")
    
    # Results Area
    if search_word or search_button:
        st.markdown("<br>", unsafe_allow_html=True)
        res_col_l, res_col_c, res_col_r = st.columns([1, 6, 1])
        
        with res_col_c:
            if search_word.strip():
                translation, matched_key, found = find_translation(search_word, kham_dict)
                
                if found:
                    st.markdown(f"""
                    <div class="glass-card">
                        <div class="result-label">English Word Matches: <b>{matched_key}</b></div>
                        <div class="result-value" style="font-size: 1.2rem; color: #94a3b8; font-weight: 400;">Translation</div>
                        <div class="result-value kham-result">{translation}</div>
                        <div style="font-size: 0.8rem; color: #64748b; font-style: italic;">Verified entry in the Kham dictionary database</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("We couldn't find an exact match for that word.")
                    
                    suggestions = get_suggestions(search_word, kham_dict)
                    if suggestions:
                        st.markdown("### Did you potentially mean:")
                        suggestion_cols = st.columns(len(suggestions))
                        for i, suggestion in enumerate(suggestions):
                            if suggestion_cols[i].button(f"{suggestion}", key=f"sug_{suggestion}"):
                                st.session_state.search_input = suggestion
                                st.rerun()
            else:
                st.warning("Please enter a word to begin the translation journey.")
    
    # Footer Stats
    st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)
    f_col1, f_col2, f_col3 = st.columns(3)
    
    with f_col1:
        st.metric("Total Vocabulary", f"{len(kham_dict):,}")
    with f_col2:
        st.metric("Dialects", "Kham-Magar")
    with f_col3:
        st.metric("Status", "Archive Active")

if __name__ == "__main__":
    main()
