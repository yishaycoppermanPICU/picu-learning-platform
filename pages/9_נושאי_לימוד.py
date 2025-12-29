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
from utils.styles import get_common_styles

st.set_page_config(
    page_title="תוכן רפואי",
    page_icon="📖",
    layout="wide"
)

restore_user_session(st)

# טעינת CSS מרכזי
st.markdown(get_common_styles(), unsafe_allow_html=True)

# Check authentication
if not st.session_state.get('logged_in', False):
    st.error("יש להתחבר כדי לצפות בתוכן")
    if st.button("חזור לדף הראשי"):
        st.switch_page("app.py")
    st.stop()

st.title("📖 תוכן רפואי")
# בדיקה אם הגענו מהתוכן השבועי
if st.session_state.get('view_weekly_content') and st.session_state.get('selected_topic_id'):
    weekly_topic_id = st.session_state['selected_topic_id']
    
    # כפתור חזרה
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("🏠 חזור לדף הבית"):
            st.session_state['view_weekly_content'] = False
            st.session_state['selected_topic_id'] = None
            st.switch_page("app.py")
    
    with col2:
        st.info("🎯 תוכן מומלץ השבוע")
    
    st.divider()
    
    # טען את התוכן השבועי
    full_topic = get_content_item(weekly_topic_id)
    
    if full_topic:
        # Display topic header
        icon = full_topic.get('icon', '📄')
        st.header(f"{icon} {full_topic['title']}")
        
        if full_topic.get('description'):
            st.markdown(f"""
            <div class="content-section" style="background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%); border-color: #17a2b8;">
                <p style="font-size: 1.1rem; line-height: 1.8; margin: 0; color: #0c5460;">{full_topic['description']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Display sections with expand/collapse
        sections = full_topic.get('sections', [])
        
        if sections:
            st.markdown("---")
            
            for idx, section in enumerate(sorted(sections, key=lambda x: x.get('order_index', 0))):
                section_type = section.get('section_type', 'text')
                title = section.get('title', '')
                content = section.get('content', '')
                metadata = section.get('metadata')
                if metadata is None:
                    metadata = {}
                elif isinstance(metadata, str):
                    try:
                        import json
                        metadata = json.loads(metadata)
                    except:
                        metadata = {}
                
                # Create expander with section title
                with st.expander(f"**{title}**", expanded=False):
                    # Display content based on type
                    if section_type == 'alert':
                        alert_type = metadata.get('alert_type', 'info') if isinstance(metadata, dict) else 'info'
                        alert_class = f"alert-{alert_type}"
                        st.markdown(f'<div class="alert-box {alert_class}">{content}</div>', unsafe_allow_html=True)
                    
                    elif section_type == 'steps':
                        if content:
                            st.markdown(content)
                        if metadata and 'steps' in metadata:
                            for i, step in enumerate(metadata['steps'], 1):
                                st.markdown(f"**{i}.** {step}")
                    
                    elif section_type == 'options':
                        if content:
                            st.markdown(content)
                        if metadata and 'options' in metadata:
                            for opt in metadata['options']:
                                st.markdown(f"### {opt.get('title', '')}")
                                st.markdown(opt.get('description', ''))
                                if 'indication' in opt:
                                    st.info(f"**התוויה:** {opt['indication']}")
                                if 'duration' in opt:
                                    st.success(f"**משך:** {opt['duration']}")
                                st.markdown("---")
                    
                    elif section_type == 'list':
                        st.markdown(f'<div class="content-section">{content}</div>', unsafe_allow_html=True)
                    
                    else:  # text
                        st.markdown(f'<div class="content-section">{content}</div>', unsafe_allow_html=True)
        else:
            st.warning("אין מקטעים לנושא זה")
        
        # כפתור למבחן
        st.divider()
        if st.button("✍️ עבור למבחן בנושא זה", type="primary", use_container_width=True):
            st.session_state['selected_quiz_category'] = full_topic.get('category')
            st.switch_page("pages/6_בחנים.py")
    else:
        st.error("לא ניתן לטעון את הנושא")
    
    st.stop()
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
                st.markdown(f"""
                <div class="content-section" style="background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%); border-color: #17a2b8;">
                    <p style="font-size: 1.1rem; line-height: 1.8; margin: 0; color: #0c5460;">{full_topic['description']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Display sections with expand/collapse
            sections = full_topic.get('sections', [])
            
            if sections:
                st.markdown("---")
                
                for idx, section in enumerate(sorted(sections, key=lambda x: x.get('order_index', 0))):
                    section_type = section.get('section_type', 'text')
                    title = section.get('title', '')
                    content = section.get('content', '')
                    metadata = section.get('metadata')
                    if metadata is None:
                        metadata = {}
                    elif isinstance(metadata, str):
                        try:
                            import json
                            metadata = json.loads(metadata)
                        except:
                            metadata = {}
                    
                    # Create expander with section title
                    with st.expander(f"**{title}**", expanded=False):
                        # Display content based on type
                        if section_type == 'alert':
                            alert_type = metadata.get('alert_type', 'info') if isinstance(metadata, dict) else 'info'
                            alert_class = f"alert-{alert_type}"
                            st.markdown(f'<div class="alert-box {alert_class}">{content}</div>', unsafe_allow_html=True)
                        
                        elif section_type == 'steps':
                            if content:
                                st.markdown(content)
                            if metadata and 'steps' in metadata:
                                for i, step in enumerate(metadata['steps'], 1):
                                    st.markdown(f"**{i}.** {step}")
                        
                        elif section_type == 'options':
                            if content:
                                st.markdown(content)
                            if metadata and 'options' in metadata:
                                for opt in metadata['options']:
                                    st.markdown(f"### {opt.get('title', '')}")
                                    st.markdown(opt.get('description', ''))
                                    if 'indication' in opt:
                                        st.info(f"**התוויה:** {opt['indication']}")
                                    if 'duration' in opt:
                                        st.success(f"**משך:** {opt['duration']}")
                                    st.markdown("---")
                        
                        elif section_type == 'list':
                            st.markdown(f'<div class="content-section">{content}</div>', unsafe_allow_html=True)
                        
                        else:  # text
                            st.markdown(f'<div class="content-section">{content}</div>', unsafe_allow_html=True)
            else:
                st.warning("אין מקטעים לנושא זה")
        else:
            st.error("לא ניתן לטעון את הנושא")
