# -*- coding: utf-8 -*-
import streamlit as st
import sys
from pathlib import Path

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.content_manager import get_topic, get_category_topics, update_topic, is_editor

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

# Check if user is admin (your email)
user = st.session_state.get('user', {})
user_email = user.get('email', '')
is_admin = is_editor(user_email)

# Initialize edit mode in session state
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False

# Navigation
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    if st.button("◀ חזור לספרייה"):
        # Reset edit mode when leaving
        st.session_state.edit_mode = False
        st.switch_page("pages/1_📚_Library.py")
with col2:
    if st.button("📝 היבחן בנושא", type="primary"):
        # Save topic info for quiz
        st.session_state.quiz_topic = topic_id
        st.session_state.quiz_category = category_id
        st.switch_page("pages/6_📝_Quizzes.py")
with col4:
    if is_admin:
        if st.session_state.edit_mode:
            # In edit mode - show exit button
            if st.button("❌ יציאה ממצב עריכה", type="secondary"):
                st.session_state.edit_mode = False
                st.rerun()
        else:
            if st.button("✏️ מצב עריכה", type="secondary"):
                st.session_state.edit_mode = True
                st.rerun()

# Title and metadata - editable in edit mode
if st.session_state.edit_mode and is_admin:
    st.markdown("### ✏️ מצב עריכה - ערוך את התוכן")
    topic['title'] = st.text_input("כותרת", value=topic['title'])
    topic['description'] = st.text_area("תיאור", value=topic['description'], height=100)
    
    col1, col2 = st.columns(2)
    with col1:
        difficulty_options = ["beginner", "intermediate", "advanced"]
        current_diff = topic.get('difficulty', 'intermediate')
        topic['difficulty'] = st.selectbox(
            "רמת קושי",
            difficulty_options,
            index=difficulty_options.index(current_diff) if current_diff in difficulty_options else 1
        )
    with col2:
        tags_str = ', '.join(topic.get('tags', []))
        new_tags = st.text_input("תגיות (מופרדות בפסיקים)", value=tags_str)
        topic['tags'] = [tag.strip() for tag in new_tags.split(',') if tag.strip()]
    
    # Save button
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 שמור את כל השינויים", type="primary", use_container_width=True):
            from datetime import datetime
            topic['last_updated'] = datetime.now().strftime("%Y-%m-%d")
            if update_topic(category_id, topic_id, topic):
                st.success("✅ השינויים נשמרו בהצלחה!")
                st.session_state.edit_mode = False
                st.rerun()
            else:
                st.error("❌ שגיאה בשמירת השינויים")
    
    with col2:
        if st.button("🚫 בטל ויצא (ללא שמירה)", use_container_width=True):
            st.warning("⚠️ השינויים לא יישמרו!")
            st.session_state.edit_mode = False
            st.rerun()
    
    st.divider()
    
    # אופציה לעריכת JSON מלא
    with st.expander("🔧 עריכה מתקדמת (JSON מלא)", expanded=False):
        st.warning("⚠️ עריכה ישירה של JSON דורשת ידע טכני. שגיאות עלולות לגרום לבעיות בתצוגה.")
        
        import json
        json_str = json.dumps(topic, ensure_ascii=False, indent=2)
        edited_json = st.text_area(
            "ערוך את ה-JSON כאן:",
            value=json_str,
            height=400,
            key="json_editor"
        )
        
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("💾 שמור JSON", type="primary"):
                try:
                    edited_topic = json.loads(edited_json)
                    from datetime import datetime
                    edited_topic['last_updated'] = datetime.now().strftime("%Y-%m-%d")
                    
                    if update_topic(category_id, topic_id, edited_topic):
                        st.success("✅ השינויים נשמרו בהצלחה!")
                        st.session_state.edit_mode = False
                        st.rerun()
                    else:
                        st.error("❌ שגיאה בשמירת השינויים")
                except json.JSONDecodeError as e:
                    st.error(f"❌ שגיאה בפורמט JSON: {str(e)}")
        with col2:
            st.caption("💡 טיפ: העתק את ה-JSON לעורך חיצוני כמו https://jsoneditoronline.org לעריכה נוחה יותר")
    
    st.markdown("### עריכת תוכן:")
    
else:
    # Normal view mode
    st.title(topic['title'])
    st.markdown(f"*{topic['description']}*")

# Metadata (view only)
if not st.session_state.edit_mode:
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

# Render content - with edit capability
st.markdown("### 📄 תוכן הנושא")

for idx, item in enumerate(topic.get('content', [])):
    if st.session_state.edit_mode and is_admin:
        with st.expander(f"✏️ עריכת סעיף {idx + 1}: {item.get('title', item.get('type', 'ללא כותרת'))}", expanded=True):
            # סוג הסעיף
            type_options = {
                "definition": "הגדרה",
                "section": "סעיף",
                "treatment": "טיפול",
                "key_points": "נקודות מפתח",
                "symptoms": "תסמינים",
                "indications": "התוויות",
                "dosing": "מינון",
                "table": "טבלה"
            }
            
            current_type = item.get('type', 'section')
            selected_type = st.selectbox(
                "סוג התוכן",
                options=list(type_options.keys()),
                format_func=lambda x: type_options[x],
                index=list(type_options.keys()).index(current_type) if current_type in type_options else 0,
                key=f"type_{idx}"
            )
            topic['content'][idx]['type'] = selected_type
            
            # כותרת
            new_title = st.text_input(
                "כותרת הסעיף",
                value=item.get('title', ''),
                key=f"title_{idx}",
                placeholder="הזן כותרת לסעיף"
            )
            topic['content'][idx]['title'] = new_title
            
            # תוכן טקסטואלי
            if 'text' in item or selected_type == 'definition':
                new_text = st.text_area(
                    "תוכן",
                    value=item.get('text', ''),
                    height=200,
                    key=f"text_{idx}",
                    placeholder="הזן את תוכן הסעיף"
                )
                topic['content'][idx]['text'] = new_text
            
            # נקודות / פריטים
            if 'points' in item:
                st.markdown("**נקודות מפתח (אחת בכל שורה):**")
                points_text = '\n'.join(item.get('points', []))
                new_points = st.text_area(
                    "נקודות",
                    value=points_text,
                    height=150,
                    key=f"points_{idx}",
                    label_visibility="collapsed"
                )
                topic['content'][idx]['points'] = [p.strip() for p in new_points.split('\n') if p.strip()]
            
            # פריטים מורכבים
            if 'items' in item:
                st.markdown("**פריטים מורכבים:**")
                st.json(item['items'])
                st.info("💡 לעריכה של פריטים מורכבים, ערוך את קובץ ה-JSON ישירות או השתמש בעורך JSON מקוון")
            
            # סעיפי טיפול
            if 'sections' in item:
                st.markdown("**סעיפי טיפול:**")
                st.json(item['sections'])
                st.info("💡 לעריכה של סעיפים מורכבים, ערוך את קובץ ה-JSON ישירות")
            
            st.divider()
    else:
        # Normal render mode
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
