# -*- coding: utf-8 -*-
import streamlit as st
import sys
from pathlib import Path

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.content_manager import get_topic, get_category_topics

st.set_page_config(
    page_title="תוכן רפואי",
    page_icon="📖",
    layout="wide"
)

# CSS
st.markdown("""
<style>
    .stApp {
        direction: rtl;
    }
    
    h1, h2, h3, h4, h5, h6, p, label, span, li {
        text-align: right;
        direction: rtl;
    }
    
    input, textarea, select {
        direction: rtl;
        text-align: right;
    }
    
    .definition-box {
        background: #f0f8ff;
        padding: 1.5rem;
        border-radius: 10px;
        border-right: 4px solid #007bff;
        margin: 1rem 0;
    }
    
    .key-points-box {
        background: #fff3cd;
        padding: 1.5rem;
        border-radius: 10px;
        border-right: 4px solid #ffc107;
        margin: 1rem 0;
    }
    
    .treatment-box {
        background: #f0fff4;
        padding: 1.5rem;
        border-radius: 10px;
        border-right: 4px solid #28a745;
        margin: 1rem 0;
    }
    
    .section-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .metadata {
        background: #e9ecef;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Check authentication
if not st.session_state.get('logged_in', False):
    st.error("יש להתחבר כדי לצפות בתוכן")
    if st.button("חזור לדף הראשי"):
        st.switch_page("app.py")
    st.stop()

# Get selected topic from session state
category_id = st.session_state.get('selected_category')
topic_id = st.session_state.get('selected_topic')

if not category_id or not topic_id:
    st.warning("לא נבחר נושא")
    if st.button("חזור לספרייה"):
        st.switch_page("pages/1_📚_Library.py")
    st.stop()

# Load topic
topic = get_topic(category_id, topic_id)

if not topic:
    st.error("נושא לא נמצא")
    if st.button("חזור לספרייה"):
        st.switch_page("pages/1_📚_Library.py")
    st.stop()

# Navigation
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("◀ חזור לספרייה"):
        st.switch_page("pages/1_📚_Library.py")

# Title and metadata
st.title(topic['title'])
st.markdown(f"*{topic['description']}*")

# Metadata
difficulty_map = {
    "beginner": "🟢 מתחיל",
    "intermediate": "🟡 בינוני",
    "advanced": "🔴 מתקדם"
}

col1, col2, col3 = st.columns(3)
with col1:
    st.caption(f"**רמת קושי:** {difficulty_map.get(topic.get('difficulty', ''), 'לא צוין')}")
with col2:
    st.caption(f"**עודכן:** {topic.get('last_updated', 'לא צוין')}")
with col3:
    st.caption(f"**מחבר:** {topic.get('author', 'לא צוין')}")

if topic.get('tags'):
    st.caption(f"**תגיות:** {', '.join(topic['tags'])}")

st.divider()

# Render content
for item in topic.get('content', []):
    item_type = item.get('type')
    
    if item_type == 'definition':
        st.markdown(f"""
        <div class="definition-box">
            <h3>{item.get('title', 'הגדרה')}</h3>
            <p>{item.get('text', '')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    elif item_type == 'section':
        st.markdown(f"### {item.get('title', '')}")
        
        for section_item in item.get('items', []):
            with st.expander(f"**{section_item.get('name', '')}**", expanded=False):
                if section_item.get('description'):
                    st.write(section_item['description'])
                
                if section_item.get('signs'):
                    st.write("**סימנים וביטויים:**")
                    for sign in section_item['signs']:
                        st.write(f"- {sign}")
                
                if section_item.get('tests'):
                    st.write("**בדיקות:**")
                    for test in section_item['tests']:
                        st.write(f"- {test}")
                
                if section_item.get('causes'):
                    st.write("**סיבות:**")
                    for cause in section_item['causes']:
                        st.write(f"- {cause}")
    
    elif item_type == 'treatment':
        st.markdown(f"""
        <div class="treatment-box">
            <h3>{item.get('title', 'טיפול')}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        for section in item.get('sections', []):
            st.markdown(f"#### {section.get('name', '')}")
            for step in section.get('steps', []):
                st.write(f"• {step}")
            st.write("")
    
    elif item_type == 'key_points':
        st.markdown(f"### {item.get('title', 'נקודות מפתח')}")
        for point in item.get('points', []):
            st.write(f"- {point}")
    
    elif item_type == 'table':
        st.markdown(f"### {item.get('title', 'טבלה')}")
        # Render table (simplified)
        if item.get('data'):
            st.table(item['data'])

# Key points section
if topic.get('key_points'):
    st.markdown("""
    <div class="key-points-box">
        <h3>נקודות מפתח 🔑</h3>
    </div>
    """, unsafe_allow_html=True)
    
    for point in topic['key_points']:
        st.write(f"✓ {point}")

st.divider()

# Navigation footer
col1, col2 = st.columns(2)
with col1:
    if st.button("◀ חזור לספרייה", key="back_bottom"):
        st.switch_page("pages/1_📚_Library.py")
