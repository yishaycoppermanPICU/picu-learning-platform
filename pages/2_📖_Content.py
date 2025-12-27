# -*- coding: utf-8 -*-
import streamlit as st
import sys
from pathlib import Path

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.content_manager import restore_user_session, is_editor
from utils.database import get_topics, get_content_item, update_content_item

# Import rich text editor
try:
    from streamlit_quill import st_quill
    RICH_EDITOR_AVAILABLE = True
except ImportError:
    RICH_EDITOR_AVAILABLE = False

st.set_page_config(
    page_title="תוכן רפואי",
    page_icon="📖",
    layout="wide"
)

# Restore user session if available
restore_user_session(st)

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
    
    .definition-box div, .definition-box p {
        direction: rtl;
        text-align: right;
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
    
    /* Rich text content styling */
    .ql-editor {
        direction: rtl;
        text-align: right;
        min-height: 200px;
    }
    
    /* Style the rendered rich text */
    .definition-box strong, .definition-box b {
        font-weight: bold;
    }
    
    .definition-box em, .definition-box i {
        font-style: italic;
    }
    
    .definition-box u {
        text-decoration: underline;
    }
    
    .definition-box ul, .definition-box ol {
        padding-right: 20px;
        text-align: right;
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

# Breadcrumb navigation
from utils.content_manager import get_all_categories

# Get category name
categories = get_all_categories()
category_info = next((cat for cat in categories if cat['id'] == category_id), None)
category_name = category_info['name'] if category_info else category_id

# Display breadcrumbs
st.markdown(f"🏠 [ספרייה](/) > {category_info['emoji']} {category_name} > **{topic['title']}**")
st.divider()

# Navigation
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    if st.button("◀ חזור לקטגוריה"):
        # Reset edit mode when leaving
        st.session_state.edit_mode = False
        # Stay in the same category - just go back to library with category selected
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
    
    with st.form("edit_topic_metadata"):
        new_title = st.text_input("כותרת", value=topic['title'])
        new_description = st.text_area("תיאור", value=topic['description'], height=100)
        
        col1, col2 = st.columns(2)
        with col1:
            difficulty_options = ["beginner", "intermediate", "advanced"]
            current_diff = topic.get('difficulty', 'intermediate')
            new_difficulty = st.selectbox(
                "רמת קושי",
                difficulty_options,
                index=difficulty_options.index(current_diff) if current_diff in difficulty_options else 1
            )
        with col2:
            tags_str = ', '.join(topic.get('tags', []))
            new_tags_str = st.text_input("תגיות (מופרדות בפסיקים)", value=tags_str)
        
        # Save button
        col1, col2 = st.columns(2)
        with col1:
            submit_save = st.form_submit_button("💾 שמור את כל השינויים", type="primary", use_container_width=True)
        with col2:
            submit_cancel = st.form_submit_button("🚫 בטל ויצא (ללא שמירה)", use_container_width=True)
        
        if submit_save:
            from datetime import datetime
            # Update topic with new values
            topic['title'] = new_title
            topic['description'] = new_description
            topic['difficulty'] = new_difficulty
            topic['tags'] = [tag.strip() for tag in new_tags_str.split(',') if tag.strip()]
            topic['last_updated'] = datetime.now().strftime("%Y-%m-%d")
            
            if update_topic(category_id, topic_id, topic):
                st.success("✅ השינויים נשמרו בהצלחה!")
                st.session_state.edit_mode = False
                st.rerun()
            else:
                st.error("❌ שגיאה בשמירת השינויים")
        
        if submit_cancel:
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
        with st.expander(f"✏️ עריכת סעיף {idx + 1}: {item.get('title', item.get('type', 'ללא כותרת'))}", expanded=False):
            with st.form(f"edit_section_{idx}"):
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
                
                # כותרת
                new_title = st.text_input(
                    "כותרת הסעיף",
                    value=item.get('title', ''),
                    key=f"title_{idx}",
                    placeholder="הזן כותרת לסעיף"
                )
                
                # תוכן טקסטואלי
                new_text = None
                if 'text' in item or selected_type == 'definition':
                    st.info("""
                    💡 **טיפים לעיצוב הטקסט:**
                    - `**טקסט מודגש**` → **טקסט מודגש**
                    - `*טקסט נטוי*` → *טקסט נטוי*
                    - `~~טקסט עם קו חוצה~~` → ~~טקסט עם קו חוצה~~
                    - `- פריט ברשימה` → רשימה
                    - `1. פריט ברשימה ממוספרת` → רשימה ממוספרת
                    - `[טקסט קישור](https://example.com)` → קישור
                    """)
                    
                    new_text = st.text_area(
                        "תוכן (תמיכה ב-Markdown)",
                        value=item.get('text', ''),
                        height=300,
                        key=f"text_{idx}",
                        placeholder="הזן את תוכן הסעיף. השתמש בסימני Markdown לעיצוב!"
                    )
                    
                    # Preview
                    if new_text and new_text != item.get('text', ''):
                        with st.expander("👁️ תצוגה מקדימה", expanded=False):
                            st.markdown(new_text)
                
                # נקודות / פריטים
                new_points = None
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
                
                # פריטים מורכבים
                if 'items' in item:
                    st.markdown("**פריטים מורכבים:**")
                    with st.expander("הצג JSON", expanded=False):
                        st.json(item['items'])
                    st.info("💡 לעריכה של מבנים מורכבים, השתמש בעורך JSON המתקדם למטה")
                
                # סעיפי טיפול
                if 'sections' in item:
                    st.markdown("**סעיפי טיפול:**")
                    with st.expander("הצג JSON", expanded=False):
                        st.json(item['sections'])
                    st.info("💡 לעריכה של מבנים מורכבים, השתמש בעורך JSON המתקדם למטה")
                
                # Save section button
                st.divider()
                submit_section = st.form_submit_button("💾 שמור סעיף זה", type="primary", use_container_width=True)
                
                if submit_section:
                    # Update the specific section
                    topic['content'][idx]['type'] = selected_type
                    topic['content'][idx]['title'] = new_title
                    if new_text is not None:
                        topic['content'][idx]['text'] = new_text
                    if new_points is not None:
                        topic['content'][idx]['points'] = [p.strip() for p in new_points.split('\n') if p.strip()]
                    
                    # Save to file
                    from datetime import datetime
                    topic['last_updated'] = datetime.now().strftime("%Y-%m-%d")
                    if update_topic(category_id, topic_id, topic):
                        st.success(f"✅ סעיף {idx + 1} נשמר בהצלחה!")
                        st.rerun()
                    else:
                        st.error("❌ שגיאה בשמירת הסעיף")
    else:
        # Normal render mode
        item_type = item.get('type')
        
        if item_type == 'definition':
            text_content = item.get('text', '')
            # Render as Markdown
            st.markdown(f"""
            <div class="definition-box">
                <h3>{item.get('title', 'הגדרה')}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Render markdown content
            st.markdown(f'<div style="padding: 0 1.5rem 1rem 1.5rem;">', unsafe_allow_html=True)
            st.markdown(text_content)
            st.markdown('</div>', unsafe_allow_html=True)
        
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
                
                # Handle 'steps' format
                if 'steps' in section:
                    for step in section.get('steps', []):
                        st.write(f"• {step}")
                
                # Handle 'options' format (like in HLH)
                if 'options' in section:
                    for option in section.get('options', []):
                        if option.get('method'):
                            st.markdown(f"**{option.get('method')}**")
                        if option.get('details'):
                            st.write(option.get('details'))
                        if option.get('dosing'):
                            st.write(f"*{option.get('dosing')}*")
                        st.write("")
                
                # Handle direct text
                if 'text' in section:
                    st.write(section.get('text'))
                
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
