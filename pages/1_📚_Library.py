# -*- coding: utf-8 -*-
import streamlit as st
import sys
from pathlib import Path

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.database import get_topics, get_content_item

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

# Header
st.title("📚 ספריית תוכן רפואי")
st.markdown("### גישה לחומרי למידה מקיפים לטיפול נמרץ ילדים")

# Navigation
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("🏠 דף הבית"):
        st.switch_page("app.py")

st.divider()

# Get all topics from database
topics = get_topics()

if not topics:
    st.warning("אין תוכן זמין כרגע במסד הנתונים")
    st.stop()

# Statistics
st.markdown("### 📊 סטטיסטיקה")
col1, col2, col3 = st.columns(3)

categories = {}
for topic in topics:
    cat = topic.get('category', 'כללי')
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(topic)

with col1:
    st.metric("קטגוריות", len(categories))
with col2:
    st.metric("נושאים", len(topics))
with col3:
    # Count total sections
    total_sections = 0
    for topic in topics:
        full_topic = get_content_item(topic['id'])
        if full_topic:
            total_sections += len(full_topic.get('sections', []))
    st.metric("פריטי תוכן", total_sections)

st.divider()

# Category selector
category_names = {
    'hematology': '🩸 המטולוגיה',
    'immunology': '🛡️ אימונולוגיה',
    'resuscitation': '🚨 החייאה',
    'infections': '🦠 זיהומים',
    'cardiology': '❤️ קרדיולוגיה',
    'medications': '💊 תרופות',
    'fluids_electrolytes': '💧 נוזלים ואלקטרוליטים',
    'monitoring': '📊 ניטור',
    'trauma': '🤕 טראומה'
}

st.markdown("### קטגוריות")

for cat_id, cat_topics in sorted(categories.items()):
    cat_display = category_names.get(cat_id, cat_id)
    
    with st.expander(f"{cat_display} ({len(cat_topics)} נושאים)", expanded=True):
        for topic in sorted(cat_topics, key=lambda x: x.get('order_index', 999)):
            col1, col2 = st.columns([5, 1])
            
            with col1:
                icon = topic.get('icon', '📄')
                st.markdown(f"**{icon} {topic['title']}**")
                st.caption(topic.get('description', ''))
                if topic.get('tags'):
                    tags_str = ' • '.join([f"`{tag}`" for tag in topic['tags']])
                    st.markdown(tags_str)
            
            with col2:
                if st.button("פתח", key=f"view_{topic['id']}"):
                    st.session_state['selected_topic_id'] = topic['id']
                    st.rerun()
            
            st.divider()

# Display selected topic
if st.session_state.get('selected_topic_id'):
    topic_id = st.session_state['selected_topic_id']
    
    # Back button
    if st.button("← חזור לרשימת הנושאים"):
        del st.session_state['selected_topic_id']
        st.rerun()
    
    st.divider()
    
    # Load full topic with sections
    full_topic = get_content_item(topic_id)
    
    if full_topic:
        # Topic header
        icon = full_topic.get('icon', '📄')
        st.title(f"{icon} {full_topic['title']}")
        st.markdown(full_topic.get('description', ''))
        
        if full_topic.get('tags'):
            tags_str = ' • '.join([f"`{tag}`" for tag in full_topic['tags']])
            st.markdown(tags_str)
        
        st.divider()
        
        # Display sections
        sections = full_topic.get('sections', [])
        if sections:
            for section in sorted(sections, key=lambda x: x.get('order_index', 999)):
                section_type = section.get('section_type', 'text')
                title = section.get('title', '')
                content = section.get('content', '')
                
                if title:
                    st.subheader(title)
                
                if section_type == 'alert':
                    alert_type = section.get('metadata', {}).get('alert_type', 'info')
                    if alert_type == 'warning':
                        st.warning(content)
                    elif alert_type == 'error':
                        st.error(content)
                    elif alert_type == 'success':
                        st.success(content)
                    else:
                        st.info(content)
                
                elif section_type == 'steps':
                    st.markdown(content)
                
                elif section_type == 'options':
                    st.markdown(content)
                
                elif section_type == 'list':
                    st.markdown(content)
                
                elif section_type == 'table':
                    # Display table content
                    st.markdown(content)
                
                else:  # text or default
                    st.markdown(content)
                
                st.markdown("")  # Add spacing
        else:
            st.info("אין תוכן זמין לנושא זה")
    else:
        st.error("שגיאה בטעינת התוכן")
