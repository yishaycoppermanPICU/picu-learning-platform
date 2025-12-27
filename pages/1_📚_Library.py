# -*- coding: utf-8 -*-
import streamlit as st
import sys
from pathlib import Path

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.content_manager import (
    get_all_categories,
    get_category_topics,
    search,
    get_stats
)

st.set_page_config(
    page_title="ספריית תוכן",
    page_icon="📚",
    layout="wide"
)

# CSS
st.markdown("""
<style>
    .stApp {
        direction: rtl;
    }
    
    h1, h2, h3, h4, h5, h6, p, label, span {
        text-align: right;
        direction: rtl;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        flex-direction: row-reverse;
    }
    
    input, textarea, select {
        direction: rtl;
        text-align: right;
    }
    
    .category-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .stat-box {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .topic-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-right: 4px solid #667eea;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Check authentication
if not st.session_state.get('logged_in', False):
    st.error("יש להתחבר כדי לגשת לספרייה")
    if st.button("חזור לדף הראשי"):
        st.switch_page("app.py")
    st.stop()

# Header
st.title("📚 ספריית תוכן רפואי")
st.markdown("### גישה לחומרי למידה מקיפים לטיפול נמרץ ילדים")

# Navigation breadcrumb
col1, col2, col3 = st.columns([1, 4, 1])
with col1:
    if st.button("🏠 דף הבית"):
        # Clear selection when going to home
        if 'selected_category' in st.session_state:
            del st.session_state['selected_category']
        if 'selected_topic' in st.session_state:
            del st.session_state['selected_topic']
        st.switch_page("app.py")
with col2:
    # Show breadcrumb if returning from a topic
    if st.session_state.get('selected_category'):
        from utils.content_manager import get_all_categories
        categories = get_all_categories()
        cat_info = next((c for c in categories if c['id'] == st.session_state.get('selected_category')), None)
        if cat_info:
            st.markdown(f"**נמצא בקטגוריה:** {cat_info['emoji']} {cat_info['name']}")

st.divider()

# Statistics
stats = get_stats()
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("קטגוריות", stats["total_categories"])
with col2:
    st.metric("נושאים", stats["total_topics"])
with col3:
    st.metric("פריטי תוכן", stats["total_content_items"])

st.divider()

# Search
search_query = st.text_input("🔍 חיפוש בספרייה", placeholder="הקלד מילת חיפוש...")

if search_query:
    results = search(search_query)
    st.markdown(f"### תוצאות חיפוש: {len(results)} נמצאו")
    
    if results:
        for result in results:
            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**{result['title']}**")
                    st.caption(f"{result['category_name']} • {result['description']}")
                with col2:
                    if st.button("פתח", key=f"open_{result['topic_id']}"):
                        st.session_state['selected_category'] = result['category_id']
                        st.session_state['selected_topic'] = result['topic_id']
                        st.switch_page("pages/2_📖_Content.py")
                st.divider()
    else:
        st.info("לא נמצאו תוצאות")
else:
    # Display categories
    categories = get_all_categories()
    
    st.markdown("### קטגוריות")
    st.info("💡 לחץ על קטגוריה כדי לראות את הנושאים שבה")
    
    # Check if returning from a specific category (to keep it expanded)
    last_category = st.session_state.get('selected_category')
    
    for category in categories:
        # Expand the category if user just came back from viewing a topic in it
        is_expanded = (category['id'] == last_category)
        
        with st.expander(f"{category['emoji']} {category['name']}", expanded=is_expanded):
            st.markdown(f"*{category['description']}*")
            st.divider()
            
            topics = get_category_topics(category['id'])
            
            if topics:
                st.markdown(f"**{len(topics)} נושאים זמינים:**")
                
                for topic in topics:
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        difficulty_badge = {
                            "beginner": "🟢 מתחיל",
                            "intermediate": "🟡 בינוני",
                            "advanced": "🔴 מתקדם"
                        }.get(topic.get('difficulty', ''), '')
                        
                        st.markdown(f"**{topic['title']}** {difficulty_badge}")
                        st.caption(topic['description'])
                        if topic.get('tags'):
                            st.caption(f"תגיות: {', '.join(topic['tags'])}")
                    
                    with col2:
                        if st.button("פתח", key=f"view_{category['id']}_{topic['id']}"):
                            st.session_state['selected_category'] = category['id']
                            st.session_state['selected_topic'] = topic['id']
                            st.switch_page("pages/2_📖_Content.py")
                    
                    st.divider()
            else:
                st.info("אין נושאים זמינים בקטגוריה זו")
