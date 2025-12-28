# -*- coding: utf-8 -*-
"""
Database Content Editor
Advanced editor for managing content in Supabase database
"""

import streamlit as st
from utils.content_manager import restore_user_session, get_user_by_username, is_editor
from utils.database import (
    init_supabase, get_content_items, get_content_item, 
    create_content_item, update_content_item, delete_content_item,
    create_content_section, update_content_section, delete_content_section,
    get_quiz_questions, create_quiz_question, update_quiz_question, delete_quiz_question
)
from utils.styles import get_common_styles
import json
from datetime import datetime

st.set_page_config(
    page_title="עורך מסד נתונים - PICU Learning",
    page_icon="🗄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Restore user session
restore_user_session(st)

# טעינת CSS מרכזי
st.markdown(get_common_styles(), unsafe_allow_html=True)

# CSS נוסף ספציפי לעורך
st.markdown("""
<style>
    .content-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-right: 4px solid #007bff;
        margin: 0.5rem 0;
    }
    .section-card {
        background: #fff;
        padding: 0.8rem;
        border-radius: 6px;
        border: 1px solid #dee2e6;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Check authentication and editor permissions
if 'user' not in st.session_state or not st.session_state.user:
    st.error("⛔ גישה נדרשת - אנא התחבר תחילה")
    st.stop()

username = st.session_state.user['username']
user_data = get_user_by_username(username)

if not user_data or not is_editor(username):
    st.error("⛔ אין לך הרשאות עריכה")
    st.stop()

# Initialize database
supabase = init_supabase()
if not supabase:
    st.error("❌ לא ניתן להתחבר למסד הנתונים")
    st.stop()

# Header
st.title("🗄️ עורך מסד נתונים")
st.markdown("### ניהול תוכן מתקדם עם Supabase")

# Main tabs
tab1, tab2, tab3 = st.tabs(["📚 פריטי תוכן", "❓ שאלות Quiz", "📊 סטטיסטיקה"])

# ==================== TAB 1: Content Items ====================
with tab1:
    st.subheader("📚 ניהול פריטי תוכן")
    
    col1, col2 = st.columns([2, 1])
    
    with col2:
        action = st.radio("בחר פעולה:", ["הצג", "צור חדש", "ערוך", "מחק"], key="content_action")
    
    with col1:
        if action == "צור חדש":
            st.markdown("### ➕ צור פריט תוכן חדש")
            
            with st.form("new_content_form", clear_on_submit=False):
                st.markdown("#### פרטי בסיס")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    title = st.text_input("כותרת *", key="new_title")
                    category = st.selectbox("קטגוריה *", [
                        "hematology", "resuscitation", "infections", "monitoring",
                        "medications", "cardiology", "fluids_electrolytes",
                        "immunology", "trauma"
                    ], key="new_category")
                    icon = st.text_input("אייקון (emoji)", "📄", key="new_icon")
                
                with col_b:
                    slug = st.text_input("Slug (מזהה ייחודי)", key="new_slug",
                                        help="באנגלית, עם _ במקום רווחים")
                    order_index = st.number_input("סדר תצוגה", 0, 1000, 0, key="new_order")
                
                description = st.text_area("תיאור קצר", height=80, key="new_description")
                
                tags_input = st.text_input("תגיות (מופרדות בפסיקים)", key="new_tags",
                                          help="לדוגמה: קרדיולוגיה, חירום, ילדים")
                
                is_published = st.checkbox("פרסם מיד", value=True, key="new_published")
                
                submitted = st.form_submit_button("💾 צור פריט תוכן", use_container_width=True)
                
                if submitted:
                    if not title or not category:
                        st.error("❌ נא למלא את כל השדות המסומנים ב-*")
                    else:
                        tags_list = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
                        
                        data = {
                            "title": title,
                            "category": category,
                            "description": description or "",
                            "icon": icon,
                            "order_index": order_index,
                        }
                        
                        if slug:
                            data["slug"] = slug
                        if tags_list:
                            data["tags"] = tags_list
                        
                        result = create_content_item(data)
                        
                        if result:
                            st.success(f"✅ נוצר בהצלחה! ID: {result['id']}")
                            st.balloons()
                            st.session_state.selected_item_id = result['id']
                            st.rerun()
                        else:
                            st.error("❌ שגיאה ביצירת הפריט")
        
        elif action == "הצג":
            st.markdown("### 📋 כל פריטי התוכן")
            
            # Filter options
            col_filter1, col_filter2 = st.columns(2)
            with col_filter1:
                filter_category = st.selectbox("סנן לפי קטגוריה:", 
                    ["הכל", "cardiology", "fluids_electrolytes", "hematology",
                     "immunology", "infections", "medications", "monitoring", 
                     "resuscitation", "trauma"], key="filter_cat")
            
            # Get items
            items = get_content_items(category=None if filter_category == "הכל" else filter_category)
            
            if items:
                st.info(f"📊 נמצאו {len(items)} פריטים")
                
                for item in items:
                    with st.expander(f"{item.get('icon', '📄')} {item['title']} ({item['category']})"):
                        st.markdown(f"**Slug:** `{item['slug']}`")
                        st.markdown(f"**ID:** `{item['id']}`")
                        
                        if item.get('subtitle'):
                            st.markdown(f"**כותרת משנה:** {item['subtitle']}")
                        
                        if item.get('description'):
                            st.markdown(f"**תיאור:** {item['description']}")
                        
                        if item.get('clinical_definition'):
                            st.markdown("**הגדרה קלינית:**")
                            st.markdown(item['clinical_definition'])
                        
                        if item.get('tags'):
                            st.markdown(f"**תגיות:** {', '.join(item['tags'])}")
                        
                        st.markdown(f"**סדר:** {item.get('order_index', 0)} | **מפורסם:** {'✅' if item.get('is_published') else '❌'}")
                        
                        col_btn1, col_btn2, col_btn3 = st.columns(3)
                        with col_btn1:
                            if st.button("➕ הוסף מקטע", key=f"add_section_{item['id']}"):
                                st.session_state.selected_item_id = item['id']
                                st.session_state.show_add_section = True
                                st.rerun()
                        
                        with col_btn2:
                            if st.button("✏️ ערוך", key=f"edit_{item['id']}"):
                                st.session_state.selected_item_id = item['id']
                                st.session_state.content_action = "ערוך"
                                st.rerun()
                        
                        with col_btn3:
                            if st.button("🗑️ מחק", key=f"del_{item['id']}"):
                                if delete_content_item(item['id']):
                                    st.success("✅ נמחק!")
                                    st.rerun()
                                else:
                                    st.error("❌ שגיאה במחיקה")
            else:
                st.info("📭 אין עדיין פריטי תוכן במסד הנתונים")
                st.markdown("👉 לחץ על 'צור חדש' כדי להתחיל")
        
        elif action == "ערוך":
            st.markdown("### ✏️ ערוך פריט תוכן")
            
            # Get all items for selection
            items = get_content_items()
            
            if not items:
                st.warning("אין פריטים לעריכה. צור פריט חדש תחילה.")
            else:
                # Select item
                item_options = {f"{item['title']} ({item['category']})": item['id'] for item in items}
                selected_title = st.selectbox("בחר פריט לעריכה:", list(item_options.keys()))
                selected_id = item_options[selected_title]
                
                # Load item details
                item = get_content_item(selected_id)
                
                if item:
                    st.markdown(f"#### עורך: {item['title']}")
                    
                    with st.form("edit_content_form"):
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            title = st.text_input("כותרת", value=item['title'])
                            category = st.selectbox("קטגוריה", [
                                "cardiology", "fluids_electrolytes", "hematology",
                                "immunology", "infections", "medications",
                                "monitoring", "resuscitation", "trauma"
                            ], index=["cardiology", "fluids_electrolytes", "hematology",
                                     "immunology", "infections", "medications",
                                     "monitoring", "resuscitation", "trauma"].index(item['category']))
                            icon = st.text_input("אייקון", value=item.get('icon', '📄'))
                        
                        with col_b:
                            slug = st.text_input("Slug", value=item['slug'])
                            subtitle = st.text_input("כותרת משנה", value=item.get('subtitle', ''))
                            order_index = st.number_input("סדר", value=item.get('order_index', 0))
                        
                        description = st.text_area("תיאור", value=item.get('description', ''), height=80)
                        clinical_definition = st.text_area("הגדרה קלינית", 
                                                          value=item.get('clinical_definition', ''), 
                                                          height=150)
                        
                        tags_input = st.text_input("תגיות", 
                                                   value=", ".join(item.get('tags', [])))
                        
                        is_published = st.checkbox("מפורסם", value=item.get('is_published', True))
                        
                        submitted = st.form_submit_button("💾 שמור שינויים", use_container_width=True)
                        
                        if submitted:
                            tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
                            
                            data = {
                                "title": title,
                                "slug": slug,
                                "category": category,
                                "subtitle": subtitle,
                                "description": description,
                                "clinical_definition": clinical_definition,
                                "tags": tags,
                                "icon": icon,
                                "order_index": order_index,
                                "is_published": is_published
                            }
                            
                            if update_content_item(selected_id, data):
                                st.success("✅ עודכן בהצלחה!")
                                st.rerun()
                            else:
                                st.error("❌ שגיאה בעדכון")
                    
                    # Show sections
                    st.markdown("---")
                    st.markdown("### 📑 מקטעי תוכן (Sections)")
                    
                    sections = item.get('sections', [])
                    
                    if sections:
                        for idx, section in enumerate(sections):
                            with st.expander(f"{idx+1}. {section['title']} ({section['section_type']})"):
                                st.markdown(f"**סוג:** {section['section_type']}")
                                st.markdown(f"**סדר:** {section['order_index']}")
                                
                                if section.get('content'):
                                    st.markdown("**תוכן:**")
                                    st.markdown(section['content'])
                                
                                if section.get('metadata'):
                                    st.markdown("**Metadata:**")
                                    st.json(section['metadata'])
                                
                                col1, col2 = st.columns(2)
                                with col1:
                                    if st.button("✏️ ערוך מקטע", key=f"edit_sec_{section['id']}"):
                                        st.session_state.edit_section_id = section['id']
                                        st.rerun()
                                
                                with col2:
                                    if st.button("🗑️ מחק מקטע", key=f"del_sec_{section['id']}"):
                                        if delete_content_section(section['id']):
                                            st.success("נמחק!")
                                            st.rerun()
                    else:
                        st.info("אין עדיין מקטעים")
                    
                    # Add new section
                    if st.button("➕ הוסף מקטע חדש", use_container_width=True):
                        st.session_state.show_add_section = True
                        st.rerun()
                    
                    if st.session_state.get('show_add_section'):
                        st.markdown("### ➕ מקטע חדש")
                        
                        with st.form("new_section_form"):
                            section_title = st.text_input("כותרת המקטע")
                            section_type = st.selectbox("סוג המקטע", [
                                "text", "list", "steps", "options", "table", "alert"
                            ])
                            section_content = st.text_area("תוכן (Markdown)", height=200)
                            section_order = st.number_input("סדר", value=len(sections))
                            
                            # Metadata for special types
                            if section_type in ["steps", "options"]:
                                metadata_json = st.text_area("Metadata (JSON)", 
                                    value='{"items": []}',
                                    help="למשל: {\"items\": [\"צעד 1\", \"צעד 2\"]}")
                            else:
                                metadata_json = "{}"
                            
                            if st.form_submit_button("💾 הוסף מקטע"):
                                try:
                                    metadata = json.loads(metadata_json)
                                except:
                                    metadata = {}
                                
                                section_data = {
                                    "content_item_id": selected_id,
                                    "section_type": section_type,
                                    "title": section_title,
                                    "content": section_content,
                                    "metadata": metadata,
                                    "order_index": section_order
                                }
                                
                                if create_content_section(section_data):
                                    st.success("✅ נוסף!")
                                    st.session_state.show_add_section = False
                                    st.rerun()
                                else:
                                    st.error("❌ שגיאה")

# ==================== TAB 2: Quiz Questions ====================
with tab2:
    st.subheader("❓ ניהול שאלות Quiz")
    st.info("🚧 בפיתוח - ממשק לניהול שאלות")
    
    # Get all questions
    questions = get_quiz_questions()
    st.write(f"📊 סה\"כ שאלות: {len(questions)}")

# ==================== TAB 3: Statistics ====================
with tab3:
    st.subheader("📊 סטטיסטיקה")
    
    items = get_content_items()
    questions = get_quiz_questions()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📚 פריטי תוכן", len(items))
    
    with col2:
        st.metric("❓ שאלות Quiz", len(questions))
    
    with col3:
        if items:
            total_sections = sum(len(item.get('sections', [])) for item in [get_content_item(item['id']) for item in items] if item)
            st.metric("📑 סה\"כ מקטעים", total_sections)
    
    # Category breakdown
    if items:
        st.markdown("### פילוח לפי קטגוריות")
        categories = {}
        for item in items:
            cat = item['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        for cat, count in sorted(categories.items()):
            st.write(f"**{cat}:** {count} פריטים")
