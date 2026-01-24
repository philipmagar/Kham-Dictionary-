import streamlit as st
import json
from difflib import get_close_matches
import os

# Page configuration
st.set_page_config(
    page_title="English to Kham Translator",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimal CSS for basic styling
st.markdown("""
<style>
    .main {
        max-width: 800px;
        margin: 0 auto;
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
        st.error("❌ Dictionary file 'kham_index.json' not found!")
        return {}
    except json.JSONDecodeError:
        st.error("❌ Error reading dictionary file!")
        return {}

def find_translation(word, dictionary):
    """Find translation for a given English word"""
    # Convert to lowercase for case-insensitive search
    word_lower = word.lower().strip()
    
    # Direct match
    for key in dictionary.keys():
        if key.lower() == word_lower:
            return dictionary[key], key, True
    
    # Partial match
    for key in dictionary.keys():
        if word_lower in key.lower():
            return dictionary[key], key, True
    
    # No match found
    return None, None, False

def get_suggestions(word, dictionary, n=5):
    """Get close matches for a word"""
    all_keys = list(dictionary.keys())
    matches = get_close_matches(word, all_keys, n=n, cutoff=0.6)
    return matches

def main():
    # Load dictionary
    kham_dict = load_dictionary()
    
    if not kham_dict:
        st.stop()
    
    # Header
    st.title("🌐 English to Kham Translator")
    st.subheader("Discover the beauty of the Kham language")
    st.divider()
    
    # Search input
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔍 Enter an English word")
        search_word = st.text_input(
            "",
            placeholder="Type an English word here...",
            label_visibility="collapsed",
            key="search_input"
        )
        
        # Search button
        search_button = st.button("🔎 Translate")
    
    # Display results
    if search_word or search_button:
        if search_word.strip():
            translation, matched_key, found = find_translation(search_word, kham_dict)
            
            if found:
                st.success("✅ Translation found!")
                st.markdown(f"**📖 English:** {matched_key}")
                st.markdown(f"**🗣️ Kham:** {translation}")
            else:
                # No exact match found
                st.error("❌ No exact translation found.")
                
                # Get suggestions
                suggestions = get_suggestions(search_word, kham_dict)
                
                if suggestions:
                    st.info("💡 Did you mean:")
                    
                    for suggestion in suggestions:
                        if st.button(f"➡️ {suggestion}", key=f"sug_{suggestion}"):
                            st.session_state.search_input = suggestion
                            st.rerun()
        else:
            st.warning("⚠️ Please enter a word to translate.")
    
    
    
    # Statistics
    st.divider()
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    
    with col_stat1:
        st.metric("Total Words", f"{len(kham_dict):,}")
    
    with col_stat2:
        st.metric("Languages", "2")
    
    with col_stat3:
        st.metric("Dictionary", "Kham")
    
    # Sidebar
    with st.sidebar:
        st.markdown("## About")
        st.markdown("""
        This translator helps you discover **Kham** translations for English words.
        
        **Kham** is a Tibeto-Burman language spoken in Nepal.
        """)
        
        st.divider()
        st.markdown("### How to use")
        st.markdown("""
        1. Type an English word
        2. Click "Translate"
        3. View the Kham translation
        """)
        
        st.divider()
        st.metric("Dictionary Size", f"{len(kham_dict):,} entries")


if __name__ == "__main__":
    main()
