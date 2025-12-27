# -*- coding: utf-8 -*-
import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import uuid

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.database import (
    get_topics, 
    get_content_item, 
    create_content_item, 
    update_content_item,
    delete_content_item,
    create_content_section,
    update_content_section,
    delete_content_section
)

st.set_page_config(
    page_title="ניהול תוכן",
    page_icon="⚙️",
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
    
    .admin-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="admin-header">
    <h1>⚙️ ניהול תוכן רפואי</h1>
    <p>הוספה, עריכה ומחיקה של נושאים וסעיפים</p>
</div>
""", unsafe_allow_html=True)

# Navigation
if st.button("🏠 חזור לדף הבית"):
    st.switch_page("app.py")

st.divider()

# Category definitions
CATEGORY_OPTIONS = {
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

SECTION_TYPES = {
    'text': 'טקסט רגיל',
    'alert': 'אזהרה/הערה',
    'steps': 'שלבים',
    'options': 'אפשרויות',
    'list': 'רשימה',
    'table': 'טבלה'
}

# Tabs
tab1, tab2, tab3 = st.tabs(["➕ נושא חדש", "✏️ עריכת נושא", "📋 רשימת נושאים"])

# TAB 1: Create New Topic
with tab1:
    st.subheader("➕ הוספת נושא חדש")
    
    with st.form("new_topic_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_title = st.text_input("כותרת הנושא*", placeholder="לדוגמה: טיפול בהלם ספטי")
            new_category = st.selectbox("קטגוריה*", options=list(CATEGORY_OPTIONS.keys()), 
                                       format_func=lambda x: CATEGORY_OPTIONS[x])
            new_icon = st.text_input("אייקון", value="📄", placeholder="📄")
        
        with col2:
            new_slug = st.text_input("Slug (אופציונלי)", placeholder="septic-shock")
            new_tags = st.text_input("תגיות (מופרדות בפסיק)", placeholder="הלם, זיהומים, אנטיביוטיקה")
            new_order = st.number_input("סדר תצוגה", min_value=0, value=999)
        
        new_description = st.text_area("תיאור קצר*", height=100, 
                                       placeholder="תיאור קצר של הנושא שיוצג ברשימה")
        
        st.divider()
        st.markdown("### סעיפי התוכן")
        st.info("לאחר יצירת הנושא, תוכל להוסיף לו סעיפים בטאב 'עריכת נושא'")
        
        submitted = st.form_submit_button("✅ צור נושא", type="primary", use_container_width=True)
        
        if submitted:
            if not new_title or not new_description:
                st.error("❌ יש למלא את כל השדות החובה (מסומנים ב-*)")
            else:
                # Parse tags
                tags_list = [tag.strip() for tag in new_tags.split(',') if tag.strip()] if new_tags else []
                
                # Create topic data
                topic_data = {
                    'title': new_title,
                    'description': new_description,
                    'category': new_category,
                    'icon': new_icon or '📄',
                    'slug': new_slug or new_title.lower().replace(' ', '-'),
                    'tags': tags_list,
                    'order_index': new_order
                }
                
                result = create_content_item(topic_data)
                
                if result:
                    st.success(f"✅ הנושא '{new_title}' נוצר בהצלחה!")
                    st.balloons()
                    st.info("💡 עבור לטאב 'עריכת נושא' כדי להוסיף סעיפי תוכן")
                else:
                    st.error("❌ שגיאה ביצירת הנושא")

# TAB 2: Edit Topic
with tab2:
    st.subheader("✏️ עריכת נושא קיים")
    
    # Get all topics
    topics = get_topics()
    
    if not topics:
        st.warning("אין נושאים במערכת. צור נושא חדש בטאב הראשון.")
    else:
        # Topic selector
        topic_options = {t['id']: f"{t.get('icon', '📄')} {t['title']}" for t in topics}
        selected_topic_id = st.selectbox(
            "בחר נושא לעריכה",
            options=list(topic_options.keys()),
            format_func=lambda x: topic_options[x]
        )
        
        if selected_topic_id:
            # Load full topic
            full_topic = get_content_item(selected_topic_id)
            
            if full_topic:
                st.divider()
                
                # Topic metadata editor
                with st.expander("📝 עריכת פרטי הנושא", expanded=False):
                    with st.form("edit_topic_metadata"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            edit_title = st.text_input("כותרת", value=full_topic['title'])
                            edit_category = st.selectbox(
                                "קטגוריה",
                                options=list(CATEGORY_OPTIONS.keys()),
                                index=list(CATEGORY_OPTIONS.keys()).index(full_topic.get('category', 'hematology')),
                                format_func=lambda x: CATEGORY_OPTIONS[x]
                            )
                            edit_icon = st.text_input("אייקון", value=full_topic.get('icon', '📄'))
                        
                        with col2:
                            edit_slug = st.text_input("Slug", value=full_topic.get('slug', ''))
                            tags_str = ', '.join(full_topic.get('tags', []))
                            edit_tags = st.text_input("תגיות", value=tags_str)
                            edit_order = st.number_input("סדר", value=full_topic.get('order_index', 999))
                        
                        edit_description = st.text_area("תיאור", value=full_topic.get('description', ''), height=100)
                        
                        col1, col2 = st.columns([1, 4])
                        with col1:
                            if st.form_submit_button("💾 שמור", type="primary"):
                                updated_data = {
                                    'title': edit_title,
                                    'description': edit_description,
                                    'category': edit_category,
                                    'icon': edit_icon,
                                    'slug': edit_slug,
                                    'tags': [t.strip() for t in edit_tags.split(',') if t.strip()],
                                    'order_index': edit_order
                                }
                                
                                if update_content_item(selected_topic_id, updated_data):
                                    st.success("✅ הנושא עודכן!")
                                    st.rerun()
                                else:
                                    st.error("❌ שגיאה בעדכון")
                        
                        with col2:
                            if st.form_submit_button("🗑️ מחק נושא", type="secondary"):
                                if delete_content_item(selected_topic_id):
                                    st.success("✅ הנושא נמחק!")
                                    st.rerun()
                                else:
                                    st.error("❌ שגיאה במחיקה")
                
                st.divider()
                
                # Sections management
                st.markdown("### 📋 ניהול סעיפים")
                
                sections = full_topic.get('sections', [])
                
                # Add new section
                with st.expander("➕ הוסף סעיף חדש", expanded=False):
                    with st.form("add_section_form", clear_on_submit=True):
                        sec_title = st.text_input("כותרת הסעיף")
                        sec_type = st.selectbox("סוג סעיף", options=list(SECTION_TYPES.keys()),
                                               format_func=lambda x: SECTION_TYPES[x])
                        
                        st.markdown("**תוכן הסעיף** (תומך ב-Markdown)")
                        sec_content = st.text_area("תוכן", height=200, 
                                                   placeholder="כתוב כאן את התוכן. אפשר להשתמש ב-Markdown:\n\n**מודגש**\n*נטוי*\n- רשימה\n1. רשימה ממוספרת")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            sec_order = st.number_input("מיקום", min_value=0, value=len(sections) + 1)
                        
                        with col2:
                            if sec_type == 'alert':
                                alert_type = st.selectbox("סוג אזהרה", ['info', 'warning', 'error', 'success'])
                        
                        # Preview
                        if sec_content:
                            st.markdown("**👁️ תצוגה מקדימה:**")
                            if sec_type == 'alert':
                                if alert_type == 'warning':
                                    st.warning(sec_content)
                                elif alert_type == 'error':
                                    st.error(sec_content)
                                elif alert_type == 'success':
                                    st.success(sec_content)
                                else:
                                    st.info(sec_content)
                            else:
                                st.markdown(sec_content)
                        
                        if st.form_submit_button("➕ הוסף סעיף", type="primary", use_container_width=True):
                            if not sec_content:
                                st.error("❌ יש למלא את תוכן הסעיף")
                            else:
                                section_data = {
                                    'topic_id': selected_topic_id,
                                    'section_type': sec_type,
                                    'title': sec_title,
                                    'content': sec_content,
                                    'order_index': sec_order,
                                    'metadata': {'alert_type': alert_type} if sec_type == 'alert' else {}
                                }
                                
                                if create_content_section(section_data):
                                    st.success("✅ הסעיף נוסף!")
                                    st.rerun()
                                else:
                                    st.error("❌ שגיאה בהוספת הסעיף")
                
                # Display existing sections
                if sections:
                    st.markdown(f"**{len(sections)} סעיפים קיימים:**")
                    
                    for idx, section in enumerate(sorted(sections, key=lambda x: x.get('order_index', 999))):
                        with st.expander(f"{idx+1}. {SECTION_TYPES.get(section['section_type'], 'טקסט')}: {section.get('title', '(ללא כותרת)')}"):
                            with st.form(f"edit_section_{section['id']}"):
                                edit_sec_title = st.text_input("כותרת", value=section.get('title', ''), key=f"title_{section['id']}")
                                edit_sec_type = st.selectbox(
                                    "סוג", 
                                    options=list(SECTION_TYPES.keys()),
                                    index=list(SECTION_TYPES.keys()).index(section['section_type']),
                                    format_func=lambda x: SECTION_TYPES[x],
                                    key=f"type_{section['id']}"
                                )
                                edit_sec_content = st.text_area("תוכן", value=section.get('content', ''), height=150, key=f"content_{section['id']}")
                                edit_sec_order = st.number_input("מיקום", value=section.get('order_index', idx), key=f"order_{section['id']}")
                                
                                edit_alert_type = 'info'  # Default value
                                if edit_sec_type == 'alert':
                                    metadata = section.get('metadata')
                                    current_alert = metadata.get('alert_type', 'info') if metadata else 'info'
                                    edit_alert_type = st.selectbox("סוג אזהרה", ['info', 'warning', 'error', 'success'],
                                                                  index=['info', 'warning', 'error', 'success'].index(current_alert),
                                                                  key=f"alert_{section['id']}")
                                
                                col1, col2 = st.columns(2)
                                with col1:
                                    if st.form_submit_button("💾 שמור שינויים", type="primary"):
                                        updated_section = {
                                            'section_type': edit_sec_type,
                                            'title': edit_sec_title,
                                            'content': edit_sec_content,
                                            'order_index': edit_sec_order,
                                            'metadata': {'alert_type': edit_alert_type} if edit_sec_type == 'alert' else {}
                                        }
                                        
                                        if update_content_section(section['id'], updated_section):
                                            st.success("✅ הסעיף עודכן!")
                                            st.rerun()
                                        else:
                                            st.error("❌ שגיאה בעדכון")
                                
                                with col2:
                                    if st.form_submit_button("🗑️ מחק סעיף", type="secondary"):
                                        if delete_content_section(section['id']):
                                            st.success("✅ הסעיף נמחק!")
                                            st.rerun()
                                        else:
                                            st.error("❌ שגיאה במחיקה")
                else:
                    st.info("אין סעיפים לנושא זה. הוסף סעיף ראשון למעלה.")

# TAB 3: List Topics
with tab3:
    st.subheader("📋 כל הנושאים במערכת")
    
    topics = get_topics()
    
    if not topics:
        st.warning("אין נושאים במערכת")
    else:
        # Group by category
        by_category = {}
        for topic in topics:
            cat = topic.get('category', 'other')
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(topic)
        
        for cat_id, cat_topics in sorted(by_category.items()):
            cat_name = CATEGORY_OPTIONS.get(cat_id, cat_id)
            st.markdown(f"### {cat_name}")
            
            for topic in sorted(cat_topics, key=lambda x: x.get('order_index', 999)):
                col1, col2, col3 = st.columns([1, 3, 1])
                
                with col1:
                    st.markdown(f"{topic.get('icon', '📄')}")
                
                with col2:
                    st.markdown(f"**{topic['title']}**")
                    st.caption(topic.get('description', ''))
                    if topic.get('tags'):
                        st.caption(' • '.join([f"`{tag}`" for tag in topic['tags']]))
                
                with col3:
                    # Count sections
                    full = get_content_item(topic['id'])
                    section_count = len(full.get('sections', [])) if full else 0
                    st.metric("סעיפים", section_count)
            
            st.divider()
        
        # Summary stats
        st.markdown("### 📊 סטטיסטיקה")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("קטגוריות", len(by_category))
        with col2:
            st.metric("נושאים", len(topics))
        with col3:
            total_sections = sum(len(get_content_item(t['id']).get('sections', [])) for t in topics)
            st.metric("סעיפים", total_sections)
