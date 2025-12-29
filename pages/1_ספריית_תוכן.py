# -*- coding: utf-8 -*-
import streamlit as st
import sys
from pathlib import Path

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.content_manager import get_all_categories, get_category_topics
from utils.styles import get_common_styles

st.set_page_config(
    page_title="ספריית תוכן",
    page_icon="📚",
    layout="wide"
)

# טעינת CSS מרכזי
st.markdown(get_common_styles(), unsafe_allow_html=True)

# Header
st.title("📚 ספריית תוכן רפואי")
st.markdown("### גישה לחומרי למידה מקיפים לטיפול נמרץ ילדים")

# Navigation
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("🏠 דף הבית"):
        st.switch_page("app.py")

st.divider()

# Get all categories from content manager
categories = get_all_categories()

if not categories:
    st.warning("אין תוכן זמין כרגע")
    st.stop()

# Statistics
st.markdown("### 📊 סטטיסטיקה")
col1, col2, col3 = st.columns(3)

total_topics = 0
for category in categories:
    topics = get_category_topics(category['id'])
    total_topics += len(topics)

with col1:
    st.metric("קטגוריות", len(categories))
with col2:
    st.metric("נושאים", total_topics)
with col3:
    st.metric("זמין לקריאה", "✅")

st.divider()

# Display categories
st.markdown("### 📚 קטגוריות לימוד")

# Check if we need to auto-expand a specific category (when returning from content page)
last_category = st.session_state.get('selected_category')

for category in categories:
    topics = get_category_topics(category['id'])
    
    if len(topics) > 0:
        # Auto-expand if this was the last selected category
        should_expand = (category['id'] == last_category)
        
        with st.expander(f"{category['emoji']} {category['name']} ({len(topics)} נושאים)", expanded=should_expand):
            for topic in topics:
                col1, col2 = st.columns([5, 1])
                
                with col1:
                    st.markdown(f"**📄 {topic['title']}**")
                    if topic.get('description'):
                        st.caption(topic['description'])
                    if topic.get('tags'):
                        tags_str = ' • '.join([f"`{tag}`" for tag in topic['tags'][:5]])
                        st.markdown(tags_str)
                
                with col2:
                    # Store topic info in session state and navigate
                    if st.button("פתח", key=f"view_{category['id']}_{topic['id']}"):
                        st.session_state['selected_category'] = category['id']
                        st.session_state['selected_topic'] = topic['id']
                        st.switch_page("pages/2_קטגוריות.py")
            
            st.divider()

st.markdown("---")
st.caption("💡 טיפ: לחץ על 'פתח' כדי לצפות בתוכן המלא של כל נושא")

