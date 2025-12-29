# -*- coding: utf-8 -*-
import streamlit as st
import sys
from pathlib import Path
import json
from datetime import datetime

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.content_manager import get_topic, is_editor, get_category_topics
from utils.styles import get_common_styles
from utils.corrections_manager import save_correction

st.set_page_config(
    page_title="צפייה בתוכן",
    page_icon="📖",
    layout="wide"
)

# טעינת CSS מרכזי
st.markdown(get_common_styles(), unsafe_allow_html=True)

# Check if user is logged in
if not st.session_state.get('logged_in', False):
    st.error("יש להתחבר כדי לצפות בתוכן ❌")
    if st.button("חזור לדף הראשי 🏠"):
        st.switch_page("app.py")
    st.stop()

# Get selected topic from session state
category = st.session_state.get('selected_category')
topic_id = st.session_state.get('selected_topic')

if not category or not topic_id:
    st.warning("לא נבחר נושא לצפייה")
    if st.button("🏠 חזור לספרייה"):
        st.switch_page("pages/1_ספריית_תוכן.py")
    st.stop()

# Get topic content
topic = get_topic(category, topic_id)

if not topic:
    st.error(f"❌ לא נמצא תוכן עבור: {topic_id} בקטגוריה {category}")
    if st.button("🏠 חזור לספרייה"):
        st.switch_page("pages/1_ספריית_תוכן.py")
    st.stop()

# Navigation buttons
user_email = st.session_state.get('user', {}).get('email', '')
is_user_editor = is_editor(user_email)

# Check if we're in edit mode
edit_mode = st.session_state.get('content_edit_mode', False)

col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
with col1:
    if st.button("🔙 חזור"):
        # Exit edit mode if active
        if 'content_edit_mode' in st.session_state:
            del st.session_state['content_edit_mode']
        # Return to category topics list
        st.switch_page("pages/1_ספריית_תוכן.py")

with col2:
    pass  # Empty space

with col3:
    if is_user_editor:
        if edit_mode:
            if st.button("👁️ תצוגה"):
                st.session_state['content_edit_mode'] = False
                st.rerun()
        else:
            if st.button("✏️ עריכה"):
                st.session_state['content_edit_mode'] = True
                st.rerun()

with col4:
    if not edit_mode:
        if st.button("⚠️ דווח על טעות"):
            st.session_state['show_correction_form'] = True

# Correction form
if st.session_state.get('show_correction_form', False):
    st.markdown("### 📝 דיווח על טעות")
    st.info("אם מצאת טעות או אי דיוק בתוכן, נשמח לשמוע ממך!")
    
    correction_text = st.text_area(
        "תאר את הטעות:",
        placeholder="לדוגמה: המינון כתוב 0.5 mg/kg אבל צריך להיות 0.05 mg/kg",
        height=100,
        key="correction_input"
    )
    
    col_a, col_b, col_c = st.columns([1, 1, 2])
    with col_a:
        if st.button("📤 שלח", type="primary"):
            if correction_text.strip():
                user_email = st.session_state.get('user', {}).get('email', 'anonymous')
                if save_correction(category, topic_id, user_email, correction_text):
                    st.success("✅ הדיווח נשלח בהצלחה! תודה רבה 🙏")
                    st.session_state['show_correction_form'] = False
                    st.rerun()
                else:
                    st.error("❌ אירעה שגיאה בשליחת הדיווח")
            else:
                st.warning("נא למלא את תיאור הטעות")
    
    with col_b:
        if st.button("ביטול"):
            st.session_state['show_correction_form'] = False
            st.rerun()

st.divider()

# If in edit mode, show editor
if edit_mode and is_user_editor:
    st.warning("🔧 **מצב עריכה פעיל** - שים לב: שינויים יישמרו מיד!")
    
    # Load the raw JSON file
    content_dir = Path('data/content')
    topic_file = content_dir / category / f"{topic_id}.json"
    
    if topic_file.exists():
        with open(topic_file, 'r', encoding='utf-8') as f:
            topic_data = json.load(f)
        
        # Create tabs for simple and advanced editing
        edit_tab1, edit_tab2 = st.tabs(["📝 עריכה פשוטה", "🔧 JSON מתקדם"])
        
        with edit_tab1:
            st.info("✏️ ערוך את התוכן בשדות טקסט פשוטים")
            
            with st.form("inline_simple_edit", clear_on_submit=False):
                # Basic info
                st.markdown("#### פרטים כלליים")
                col_a, col_b = st.columns(2)
                
                with col_a:
                    title_edit = st.text_input("כותרת", value=topic_data.get('title', ''))
                    generic_name_edit = st.text_input("שם גנרי", value=topic_data.get('genericName', ''))
                
                with col_b:
                    commercial_names_edit = st.text_input(
                        "שמות מסחריים (מופרדים בפסיק)",
                        value=', '.join(topic_data.get('commercialNames', []))
                    )
                    tags_edit = st.text_input(
                        "תגיות (מופרדות בפסיק)",
                        value=', '.join(topic_data.get('tags', []))
                    )
                
                st.divider()
                st.markdown("#### תוכן")
                
                # Edit content sections
                content_sections = topic_data.get('content', [])
                edited_content = []
                
                for idx, section in enumerate(content_sections):
                    section_type = section.get('type', 'section')
                    
                    with st.expander(f"📌 {section.get('title', f'סעיף {idx+1}')}", expanded=True):
                        
                        if section_type == 'definition':
                            sec_title = st.text_input(f"כותרת", value=section.get('title', ''), key=f"st_{idx}")
                            sec_text = st.text_area(f"טקסט", value=section.get('text', ''), height=120, key=f"txt_{idx}")
                            edited_content.append({'type': 'definition', 'title': sec_title, 'text': sec_text})
                        
                        elif section_type == 'treatment':
                            sec_title = st.text_input(f"כותרת", value=section.get('title', 'מינונים'), key=f"treat_{idx}")
                            sections_list = section.get('sections', [])
                            edited_sections = []
                            
                            for sidx, subsection in enumerate(sections_list):
                                st.markdown(f"**קבוצה {sidx+1}:**")
                                subsec_name = st.text_input(
                                    "שם קבוצה",
                                    value=subsection.get('name', ''),
                                    key=f"sn_{idx}_{sidx}"
                                )
                                
                                options_list = subsection.get('options', [])
                                edited_options = []
                                
                                for oidx, option in enumerate(options_list):
                                    col_x, col_y = st.columns([1, 3])
                                    with col_x:
                                        method = st.text_input(
                                            f"דרך מתן #{oidx+1}",
                                            value=option.get('method', ''),
                                            key=f"m_{idx}_{sidx}_{oidx}"
                                        )
                                    with col_y:
                                        details = st.text_area(
                                            f"פרטי מינון #{oidx+1}",
                                            value=option.get('details', ''),
                                            height=100,
                                            key=f"d_{idx}_{sidx}_{oidx}",
                                            help="כאן תוכל לתקן את סדר mg/kg!"
                                        )
                                    
                                    if method or details:
                                        edited_options.append({'method': method, 'details': details})
                                
                                edited_sections.append({'name': subsec_name, 'options': edited_options})
                            
                            edited_content.append({'type': 'treatment', 'title': sec_title, 'sections': edited_sections})
                        
                        elif section_type == 'section':
                            sec_title = st.text_input(f"כותרת", value=section.get('title', ''), key=f"sec_{idx}")
                            items_list = section.get('items', [])
                            edited_items = []
                            
                            for iidx, item in enumerate(items_list):
                                col_i, col_j = st.columns([1, 2])
                                with col_i:
                                    item_name = st.text_input(
                                        f"פריט #{iidx+1} - שם",
                                        value=item.get('name', ''),
                                        key=f"in_{idx}_{iidx}"
                                    )
                                with col_j:
                                    item_desc = st.text_area(
                                        f"פריט #{iidx+1} - תיאור",
                                        value=item.get('description', ''),
                                        height=80,
                                        key=f"id_{idx}_{iidx}"
                                    )
                                
                                if item_name or item_desc:
                                    edited_items.append({'name': item_name, 'description': item_desc})
                            
                            edited_content.append({'type': 'section', 'title': sec_title, 'items': edited_items})
                
                st.divider()
                st.markdown("#### נקודות מפתח")
                
                key_points = topic_data.get('key_points', [])
                key_points_text = '\n'.join(key_points)
                edited_key_points = st.text_area(
                    "נקודות מפתח (כל שורה = נקודה)",
                    value=key_points_text,
                    height=120
                )
                
                st.divider()
                
                col_save, col_cancel = st.columns(2)
                with col_save:
                    submit_simple = st.form_submit_button("💾 שמור שינויים", type="primary", use_container_width=True)
                with col_cancel:
                    cancel_simple = st.form_submit_button("❌ בטל", use_container_width=True)
                
                if submit_simple:
                    try:
                        updated_data = {
                            'id': topic_data.get('id'),
                            'title': title_edit,
                            'genericName': generic_name_edit,
                            'commercialNames': [n.strip() for n in commercial_names_edit.split(',') if n.strip()],
                            'category': topic_data.get('category'),
                            'type': topic_data.get('type'),
                            'difficulty': topic_data.get('difficulty'),
                            'order': topic_data.get('order'),
                            'tags': [t.strip() for t in tags_edit.split(',') if t.strip()],
                            'content': edited_content,
                            'key_points': [line.strip() for line in edited_key_points.split('\n') if line.strip()],
                            'last_updated': datetime.now().strftime('%Y-%m-%d'),
                            'author': topic_data.get('author', 'PICU Team')
                        }
                        
                        with open(topic_file, 'w', encoding='utf-8') as f:
                            json.dump(updated_data, f, ensure_ascii=False, indent=2)
                        
                        st.success("✅ התוכן נשמר בהצלחה!")
                        st.balloons()
                        st.session_state['content_edit_mode'] = False
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ שגיאה: {str(e)}")
                
                if cancel_simple:
                    st.session_state['content_edit_mode'] = False
                    st.rerun()
        
        with edit_tab2:
            st.warning("⚠️ עריכה מתקדמת - שים לב לתחביר JSON!")
            
            with st.form("inline_json_edit"):
                topic_json = json.dumps(topic_data, ensure_ascii=False, indent=2)
                edited_json = st.text_area("JSON", value=topic_json, height=600)
                
                col_save2, col_valid, col_cancel2 = st.columns(3)
                with col_save2:
                    submit_json = st.form_submit_button("💾 שמור", type="primary", use_container_width=True)
                with col_valid:
                    validate_json = st.form_submit_button("✅ בדוק תקינות", use_container_width=True)
                with col_cancel2:
                    cancel_json = st.form_submit_button("❌ בטל", use_container_width=True)
                
                if submit_json or validate_json:
                    try:
                        edited_data = json.loads(edited_json)
                        
                        if validate_json:
                            st.success("✅ ה-JSON תקין!")
                        else:
                            with open(topic_file, 'w', encoding='utf-8') as f:
                                json.dump(edited_data, f, ensure_ascii=False, indent=2)
                            
                            st.success("✅ נשמר בהצלחה!")
                            st.balloons()
                            st.session_state['content_edit_mode'] = False
                            st.rerun()
                    
                    except json.JSONDecodeError as e:
                        st.error(f"❌ שגיאת JSON: {str(e)}")
                    except Exception as e:
                        st.error(f"❌ שגיאה: {str(e)}")
                
                if cancel_json:
                    st.session_state['content_edit_mode'] = False
                    st.rerun()
    
    else:
        st.error("❌ קובץ התוכן לא נמצא")
    
    st.stop()  # Don't show content below in edit mode

# Display topic header
st.title(f"📖 {topic.get('title', 'ללא כותרת')}")

if topic.get('description'):
    st.markdown(f"**תיאור:** {topic['description']}")

# Display tags if available
if topic.get('tags'):
    tags_html = ' '.join([f'<span style="background-color: #667eea; color: white; padding: 0.2rem 0.5rem; border-radius: 5px; margin: 0.2rem; display: inline-block;">{tag}</span>' for tag in topic['tags']])
    st.markdown(f"**תגיות:** {tags_html}", unsafe_allow_html=True)

# Display difficulty
difficulty_map = {
    'beginner': '🟢 קל',
    'intermediate': '🟡 בינוני',
    'advanced': '🔴 מתקדם'
}
if topic.get('difficulty'):
    st.markdown(f"**רמת קושי:** {difficulty_map.get(topic['difficulty'], topic['difficulty'])}")

st.divider()

# Display content sections
content_sections = topic.get('content', [])

if not content_sections:
    st.warning("⚠️ אין סעיפי תוכן זמינים לנושא זה")
else:
    st.markdown("### 📚 תוכן הנושא")
    st.divider()
    
    def display_value(value, indent=0):
        """Display any value recursively"""
        prefix = "  " * indent
        
        if isinstance(value, dict):
            for k, v in value.items():
                key_display = k.replace('_', ' ').title()
                if isinstance(v, (dict, list)):
                    st.markdown(f"{prefix}**{key_display}:**")
                    display_value(v, indent + 1)
                else:
                    st.markdown(f"{prefix}**{key_display}:** {v}")
        
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    display_value(item, indent)
                    if indent > 0:
                        st.markdown("---")
                else:
                    st.markdown(f"{prefix}• {item}")
        
        else:
            st.write(f"{prefix}{value}")
    
    for idx, section in enumerate(content_sections):
        section_title = section.get('title', f'סעיף {idx + 1}')
        
        # Create expandable section
        with st.expander(f"📖 {section_title}", expanded=(idx == 0)):
            
            # Display text if exists
            if section.get('text'):
                st.markdown(section['text'])
                st.markdown("")
            
            # Display subtitle if exists
            if section.get('subtitle'):
                st.info(section['subtitle'])
            
            # Display items list with full details
            if section.get('items'):
                for item_idx, item in enumerate(section['items']):
                    if isinstance(item, dict):
                        # Display item name as header
                        if item.get('name'):
                            st.markdown(f"### 🔹 {item['name']}")
                        
                        # Display all fields of the item
                        for key, value in item.items():
                            if key == 'name':
                                continue  # Already displayed as header
                            
                            key_display = key.replace('_', ' ').title()
                            
                            if key == 'description':
                                st.write(value)
                            elif key == 'note':
                                st.info(f"ℹ️ {value}")
                            elif key in ['pathogens', 'causes', 'symptoms', 'signs', 'mimics']:
                                st.markdown(f"**{key_display}:**")
                                for v in value:
                                    st.markdown(f"- {v}")
                            elif isinstance(value, list):
                                st.markdown(f"**{key_display}:**")
                                for v in value:
                                    if isinstance(v, dict):
                                        display_value(v, 1)
                                    else:
                                        st.markdown(f"- {v}")
                            elif isinstance(value, dict):
                                st.markdown(f"**{key_display}:**")
                                display_value(value, 1)
                            else:
                                st.markdown(f"**{key_display}:** {value}")
                        
                        if item_idx < len(section['items']) - 1:
                            st.divider()
                    else:
                        st.markdown(f"- {item}")
            
            # Display data dictionary with full details
            if section.get('data'):
                data = section['data']
                for key, value in data.items():
                    key_display = key.replace('_', ' ').title()
                    
                    if isinstance(value, list):
                        st.markdown(f"**{key_display}:**")
                        for v in value:
                            st.markdown(f"- {v}")
                    elif isinstance(value, dict):
                        st.markdown(f"**{key_display}:**")
                        display_value(value, 1)
                    else:
                        st.markdown(f"**{key_display}:** {value}")
            
            # Display presentations with full details
            if section.get('presentations'):
                for pres_idx, pres in enumerate(section['presentations']):
                    st.markdown(f"### 🔸 {pres.get('name', '')}")
                    
                    # Display all fields
                    for key, value in pres.items():
                        if key == 'name':
                            continue
                        
                        key_display = key.replace('_', ' ').title()
                        
                        if key == 'description':
                            st.write(value)
                        elif key == 'note':
                            st.info(value)
                        elif key in ['timeline', 'population']:
                            st.caption(f"**{key_display}:** {value}")
                        elif key == 'symptoms':
                            st.markdown("**תסמינים:**")
                            for s in value:
                                st.markdown(f"- {s}")
                        elif key == 'mimics':
                            st.warning("**יכול לחקות:**")
                            for m in value:
                                st.markdown(f"- {m}")
                        elif isinstance(value, list):
                            st.markdown(f"**{key_display}:**")
                            for v in value:
                                st.markdown(f"- {v}")
                        else:
                            st.markdown(f"**{key_display}:** {value}")
                    
                    if pres_idx < len(section['presentations']) - 1:
                        st.divider()
            
            # Display goals
            if section.get('goals'):
                st.markdown("**מטרות:**")
                for goal in section['goals']:
                    if isinstance(goal, dict):
                        st.markdown(f"- **{goal.get('goal', '')}**")
                        for key, value in goal.items():
                            if key != 'goal':
                                st.caption(f"  → {key.replace('_', ' ').title()}: {value}")
                    else:
                        st.markdown(f"- {goal}")
            
            # Display critical_note
            if section.get('critical_note'):
                st.error(section['critical_note'])
            
            # Display list
            if section.get('list'):
                for item in section['list']:
                    st.markdown(f"- {item}")
            
            # Display categories with full drugs info
            if section.get('categories'):
                for cat in section['categories']:
                    if isinstance(cat, dict):
                        cat_name = cat.get('category_name', cat.get('category', ''))
                        st.markdown(f"### 💊 {cat_name}")
                        
                        if cat.get('reason'):
                            st.info(cat['reason'])
                        
                        if cat.get('drugs'):
                            for drug in cat['drugs']:
                                if isinstance(drug, dict):
                                    st.markdown(f"**🔹 {drug.get('name', '')}**")
                                    for key, value in drug.items():
                                        if key == 'name':
                                            continue
                                        key_display = key.replace('_', ' ').title()
                                        if key == 'mechanism':
                                            st.caption(f"מנגנון: {value}")
                                        elif key == 'dosage':
                                            st.success(f"💉 {value}")
                                        elif key == 'indication':
                                            st.caption(f"אינדיקציה: {value}")
                                        elif key == 'contraindication':
                                            st.error(f"⚠️ התווית נגד: {value}")
                                        elif isinstance(value, list):
                                            st.markdown(f"**{key_display}:**")
                                            for v in value:
                                                st.markdown(f"  - {v}")
                                        else:
                                            st.markdown(f"**{key_display}:** {value}")
                                else:
                                    st.markdown(f"- {drug}")
                        
                        st.divider()
            
            # Display any remaining fields that weren't handled
            for key, value in section.items():
                if key not in ['type', 'title', 'text', 'subtitle', 'items', 'data', 
                               'presentations', 'goals', 'critical_note', 'list', 'categories']:
                    key_display = key.replace('_', ' ').title()
                    st.markdown(f"**{key_display}:**")
                    display_value(value)


st.divider()

# Quiz button
st.markdown("### 🎯 בדוק את הידע שלך")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("📝 בחן את עצמך בנושא זה", type="primary", use_container_width=True):
        st.session_state['quiz_topic'] = topic_id
        st.session_state['quiz_category'] = category
        st.switch_page("pages/6_בחנים.py")

