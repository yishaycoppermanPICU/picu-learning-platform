# -*- coding: utf-8 -*-
"""
עמוד תוכן - קריאה ממסד נתונים
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.content_manager import restore_user_session
from utils.database import get_topics, get_content_item

st.set_page_config(
    page_title="תוכן רפואי",
    page_icon="📖",
    layout="wide"
)

restore_user_session(st)

# RTL CSS
st.markdown("""
<style>
    .stApp { direction: rtl; }
    h1, h2, h3, h4, h5, h6, p, label, span, li { text-align: right; direction: rtl; }
    .content-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-right: 4px solid #007bff;
        margin: 1rem 0;
    }
    .alert-box {
        background: #fff3cd;
        border: 2px solid #ffc107;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Check authentication
if not st.session_state.get('logged_in', False):
    st.error("יש להתחבר כדי לצפות בתוכן")
    if st.button("חזור לדף הראשי"):
        st.switch_page("app.py")
    st.stop()

st.title("📖 תוכן רפואי")

# Get all topics
topics = get_topics()

if not topics:
    st.warning("אין עדיין תוכן במסד הנתונים")
    st.stop()

# Group by category
categories = {}
for topic in topics:
    cat = topic.get('category', 'general')
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(topic)

# Category selection
category_names = {
    'hematology': '🩸 המטולוגיה ואונקולוגיה',
    'immunology': '🛡️ אימונולוגיה',
    'resuscitation': '🚨 החייאה וטיפול דחוף',
    'infections': '🦠 זיהומים',
    'cardiology': '🫀 קרדיולוגיה',
    'medications': '💊 תרופות',
    'monitoring': '📊 ניטור ונהלים',
    'fluids_electrolytes': '💧 נוזלים ואלקטרוליטים',
    'trauma': '🚑 טראומה',
    'general': '📚 כללי'
}

selected_category = st.selectbox(
    "בחר קטגוריה:",
    options=list(categories.keys()),
    format_func=lambda x: category_names.get(x, x)
)

# Topic selection
if selected_category in categories:
    category_topics = categories[selected_category]
    
    selected_topic_title = st.selectbox(
        "בחר נושא:",
        options=[t['title'] for t in category_topics]
    )
    
    # Find selected topic
    selected_topic = next((t for t in category_topics if t['title'] == selected_topic_title), None)
    
    if selected_topic:
        st.markdown("---")
        
        # Load full topic with sections
        full_topic = get_content_item(selected_topic['id'])
        
        if full_topic:
            # Display topic header
            icon = full_topic.get('icon', '📄')
            st.header(f"{icon} {full_topic['title']}")
            
            if full_topic.get('description'):
                st.info(full_topic['description'])
            
            # Display sections
            sections = full_topic.get('sections', [])
            
            if sections:
                st.markdown("---")
                
                for section in sorted(sections, key=lambda x: x.get('order_index', 0)):
                    section_type = section.get('section_type', 'text')
                    title = section.get('title', '')
                    content = section.get('content', '')
                    metadata = section.get('metadata', {})
                    
                    # Display section title
                    st.subheader(title)
                    
                    # Display content based on type
                    if section_type == 'alert':
                        st.markdown(f'<div class="alert-box">{content}</div>', unsafe_allow_html=True)
                    
                    elif section_type == 'steps':
                        if content:
                            st.markdown(content)
                        if metadata and 'steps' in metadata:
                            for i, step in enumerate(metadata['steps'], 1):
                                st.markdown(f"{i}. {step}")
                    
                    elif section_type == 'options':
                        if content:
                            st.markdown(content)
                        if metadata and 'options' in metadata:
                            for opt in metadata['options']:
                                with st.expander(f"**{opt.get('title', '')}**"):
                                    st.markdown(opt.get('description', ''))
                                    if 'indication' in opt:
                                        st.info(f"**התוויה:** {opt['indication']}")
                                    if 'duration' in opt:
                                        st.success(f"**משך:** {opt['duration']}")
                    
                    elif section_type == 'list':
                        st.markdown(content)
                    
                    else:  # text
                        st.markdown(content)
                    
                    st.markdown("---")
            else:
                st.warning("אין מקטעים לנושא זה")
        else:
            st.error("לא ניתן לטעון את הנושא")
