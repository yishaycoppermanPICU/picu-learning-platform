import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import sys

# הוסף את התיקייה הראשית ל-path
sys.path.append(str(Path(__file__).parent.parent))

from utils.content_manager import get_all_categories, get_category_topics, get_topic, update_topic, is_editor

st.set_page_config(
    page_title="עורך תוכן | PICU Learning",
    page_icon="✏️",
    layout="wide"
)

# בדיקת הרשאות
if 'user_email' not in st.session_state:
    st.warning("⚠️ נא להתחבר תחילה")
    st.stop()

user_email = st.session_state['user_email']

if not is_editor(user_email):
    st.error("🚫 אין לך הרשאה לעריכת תוכן")
    st.stop()

st.title("✏️ עורך תוכן ידידותי")
st.markdown("ערוך תוכן קיים בממשק פשוט וקליל")

# בחירת קטגוריה
categories = get_all_categories()
category_names = {cat['id']: f"{cat['emoji']} {cat['name']}" for cat in categories}

selected_category_name = st.selectbox(
    "בחר קטגוריה",
    options=list(category_names.values())
)

# מצא את הקטגוריה
selected_category_id = None
for cat_id, cat_name in category_names.items():
    if cat_name == selected_category_name:
        selected_category_id = cat_id
        break

if selected_category_id:
    # בחירת נושא
    topics = get_category_topics(selected_category_id)
    
    if not topics:
        st.info("אין נושאים בקטגוריה זו")
    else:
        topic_options = {t['id']: t['title'] for t in topics}
        selected_topic_name = st.selectbox(
            "בחר נושא",
            options=list(topic_options.values())
        )
        
        # מצא את הנושא
        selected_topic_id = None
        for topic_id, topic_name in topic_options.items():
            if topic_name == selected_topic_name:
                selected_topic_id = topic_id
                break
        
        if selected_topic_id:
            # טען את הנושא
            content_dir = Path('data/content')
            topic_file = content_dir / selected_category_id / f"{selected_topic_id}.json"
            
            if not topic_file.exists():
                st.error("❌ קובץ התוכן לא נמצא")
                st.stop()
            
            with open(topic_file, 'r', encoding='utf-8') as f:
                topic_data = json.load(f)
            
            st.divider()
            st.markdown(f"### 📝 עריכת: {topic_data.get('title', '')}")
            
            # טאבים
            tab1, tab2 = st.tabs(["📝 עריכה פשוטה", "🔧 JSON מתקדם"])
            
            with tab1:
                st.info("✏️ ערוך את התוכן בשדות טקסט פשוטים - בלי JSON!")
                
                with st.form("simple_edit_form", clear_on_submit=False):
                    # פרטים כלליים
                    st.markdown("#### פרטים כלליים")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        title = st.text_input("כותרת", value=topic_data.get('title', ''))
                        generic_name = st.text_input("שם גנרי", value=topic_data.get('genericName', ''))
                    
                    with col2:
                        commercial_names = st.text_input(
                            "שמות מסחריים (מופרדים בפסיק)",
                            value=', '.join(topic_data.get('commercialNames', []))
                        )
                        tags = st.text_input(
                            "תגיות (מופרדות בפסיק)",
                            value=', '.join(topic_data.get('tags', []))
                        )
                    
                    st.divider()
                    st.markdown("#### תוכן הנושא")
                    
                    # עריכת content sections
                    content_sections = topic_data.get('content', [])
                    edited_content = []
                    
                    for idx, section in enumerate(content_sections):
                        section_type = section.get('type', 'section')
                        section_title = section.get('title', f'סעיף {idx+1}')
                        
                        with st.expander(f"📌 {section_title}", expanded=True):
                            
                            if section_type == 'definition':
                                # הגדרה פשוטה
                                st.markdown("**סוג:** הגדרה")
                                sec_title = st.text_input(
                                    "כותרת הסעיף",
                                    value=section.get('title', ''),
                                    key=f"sec_title_{idx}"
                                )
                                sec_text = st.text_area(
                                    "טקסט ההגדרה",
                                    value=section.get('text', ''),
                                    height=120,
                                    key=f"sec_text_{idx}"
                                )
                                edited_content.append({
                                    'type': 'definition',
                                    'title': sec_title,
                                    'text': sec_text
                                })
                            
                            elif section_type == 'treatment':
                                # מינונים וטיפול
                                st.markdown("**סוג:** מינונים וטיפול")
                                sec_title = st.text_input(
                                    "כותרת",
                                    value=section.get('title', 'מינונים'),
                                    key=f"treat_title_{idx}"
                                )
                                
                                sections_list = section.get('sections', [])
                                edited_sections = []
                                
                                for sidx, subsection in enumerate(sections_list):
                                    st.markdown(f"**קבוצה {sidx+1}:**")
                                    subsec_name = st.text_input(
                                        "שם הקבוצה (לדוגמה: ילדים, תינוקות)",
                                        value=subsection.get('name', ''),
                                        key=f"subsec_name_{idx}_{sidx}"
                                    )
                                    
                                    options_list = subsection.get('options', [])
                                    edited_options = []
                                    
                                    st.markdown("**אפשרויות מינון:**")
                                    for oidx, option in enumerate(options_list):
                                        col_a, col_b = st.columns([1, 3])
                                        with col_a:
                                            method = st.text_input(
                                                f"דרך מתן #{oidx+1}",
                                                value=option.get('method', ''),
                                                key=f"method_{idx}_{sidx}_{oidx}",
                                                help="לדוגמה: IV, PO, IM"
                                            )
                                        with col_b:
                                            details = st.text_area(
                                                f"פרטי מינון #{oidx+1}",
                                                value=option.get('details', ''),
                                                height=100,
                                                key=f"details_{idx}_{sidx}_{oidx}",
                                                help="כאן תוכל לתקן סדר mg/kg ופרטים נוספים"
                                            )
                                        
                                        if method or details:
                                            edited_options.append({
                                                'method': method,
                                                'details': details
                                            })
                                    
                                    edited_sections.append({
                                        'name': subsec_name,
                                        'options': edited_options
                                    })
                                
                                edited_content.append({
                                    'type': 'treatment',
                                    'title': sec_title,
                                    'sections': edited_sections
                                })
                            
                            elif section_type == 'section':
                                # סעיף רגיל עם items
                                st.markdown("**סוג:** סעיף מידע")
                                sec_title = st.text_input(
                                    "כותרת הסעיף",
                                    value=section.get('title', ''),
                                    key=f"item_sec_title_{idx}"
                                )
                                
                                items_list = section.get('items', [])
                                edited_items = []
                                
                                st.markdown("**פריטי מידע:**")
                                for iidx, item in enumerate(items_list):
                                    col_x, col_y = st.columns([1, 2])
                                    with col_x:
                                        item_name = st.text_input(
                                            f"שם פריט #{iidx+1}",
                                            value=item.get('name', ''),
                                            key=f"item_name_{idx}_{iidx}"
                                        )
                                    with col_y:
                                        item_desc = st.text_area(
                                            f"תיאור פריט #{iidx+1}",
                                            value=item.get('description', ''),
                                            height=80,
                                            key=f"item_desc_{idx}_{iidx}"
                                        )
                                    
                                    if item_name or item_desc:
                                        edited_items.append({
                                            'name': item_name,
                                            'description': item_desc
                                        })
                                
                                edited_content.append({
                                    'type': 'section',
                                    'title': sec_title,
                                    'items': edited_items
                                })
                    
                    st.divider()
                    st.markdown("#### נקודות מפתח")
                    
                    key_points = topic_data.get('key_points', [])
                    key_points_text = '\n'.join(key_points)
                    
                    edited_key_points = st.text_area(
                        "נקודות מפתח (כל שורה = נקודה אחת)",
                        value=key_points_text,
                        height=150,
                        help="כל שורה תהפוך לנקודה נפרדת"
                    )
                    
                    st.divider()
                    
                    # כפתורי פעולה
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        submit_simple = st.form_submit_button(
                            "💾 שמור שינויים",
                            type="primary",
                            use_container_width=True
                        )
                    with col2:
                        preview = st.form_submit_button(
                            "👁️ תצוגה מקדימה",
                            use_container_width=True
                        )
                    with col3:
                        cancel = st.form_submit_button(
                            "❌ בטל",
                            use_container_width=True
                        )
                    
                    if submit_simple:
                        try:
                            # בנה את האובייקט המעודכן
                            updated_data = {
                                'id': topic_data.get('id'),
                                'title': title,
                                'genericName': generic_name,
                                'commercialNames': [n.strip() for n in commercial_names.split(',') if n.strip()],
                                'category': topic_data.get('category'),
                                'type': topic_data.get('type'),
                                'difficulty': topic_data.get('difficulty'),
                                'order': topic_data.get('order'),
                                'tags': [t.strip() for t in tags.split(',') if t.strip()],
                                'content': edited_content,
                                'key_points': [line.strip() for line in edited_key_points.split('\n') if line.strip()],
                                'last_updated': datetime.now().strftime('%Y-%m-%d'),
                                'author': topic_data.get('author', 'PICU Team')
                            }
                            
                            # שמור לקובץ
                            with open(topic_file, 'w', encoding='utf-8') as f:
                                json.dump(updated_data, f, ensure_ascii=False, indent=2)
                            
                            st.success("✅ התוכן נשמר בהצלחה!")
                            st.balloons()
                            
                            # רענן את העמוד
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"❌ שגיאה בשמירה: {str(e)}")
                            st.exception(e)
                    
                    if preview:
                        st.info("👁️ תצוגה מקדימה תופיע למטה")
            
            with tab2:
                st.warning("⚠️ עריכה מתקדמת - רק למשתמשים מנוסים!")
                st.info("💡 ערוך את ה-JSON ישירות. שים לב לתחביר!")
                
                with st.form("advanced_edit_form"):
                    topic_json = json.dumps(topic_data, ensure_ascii=False, indent=2)
                    edited_json = st.text_area(
                        "JSON",
                        value=topic_json,
                        height=600
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        submit_json = st.form_submit_button(
                            "💾 שמור",
                            type="primary",
                            use_container_width=True
                        )
                    with col2:
                        validate_json = st.form_submit_button(
                            "✅ בדוק תקינות",
                            use_container_width=True
                        )
                    
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
                                st.rerun()
                        
                        except json.JSONDecodeError as e:
                            st.error(f"❌ שגיאת JSON: {str(e)}")
                        except Exception as e:
                            st.error(f"❌ שגיאה: {str(e)}")

# הוספת רווח בתחתית
st.markdown("<br><br>", unsafe_allow_html=True)
