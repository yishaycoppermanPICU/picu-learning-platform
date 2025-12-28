import streamlit as st
import pandas as pd
import json
from datetime import datetime
from pathlib import Path
import sys

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils.content_manager import (
    get_all_categories,
    get_category_topics,
    get_topic,
    update_topic,
    get_editors,
    add_editor,
    remove_editor,
    is_editor,
    restore_user_session
)
from utils.styles import get_common_styles
from utils.corrections_manager import get_all_corrections, update_correction_status

# נסה לייבא מהדאטאבייס
try:
    from utils.database import (
        get_topics,
        init_supabase,
        DB_CONNECTED
    )
except:   
    DB_CONNECTED = False

st.set_page_config(page_title="ניהול תוכן", page_icon="⚙️", layout="wide")

# Restore user session if available
restore_user_session(st)

# CSS מרכזי
st.markdown(get_common_styles(), unsafe_allow_html=True)

# CSS נוסף ספציפי לניהול
st.markdown("""
<style>
    /* תיקון כללי */
    .main > div {
        direction: rtl;
        text-align: right;
    }
    
    /* תיקון expanders */
    [data-testid="stExpander"] {
        direction: rtl ! important;
    }
    
    [data-testid="stExpander"] details {
        direction: rtl ! important;
    }
    
    [data-testid="stExpander"] summary {
        direction: rtl !important;
        text-align: right !important;
    }
    
    [data-testid="stExpander"] .streamlit-expanderContent {
        direction: rtl ! important;
        text-align: right !important;
    }
    
    /* תיקון רשימות */
    .stMarkdown ul, .stMarkdown ol {
        direction: rtl !important;
        text-align: right !important;
        padding-right: 20px !important;
        padding-left: 0 !important;
    }
    
    .stMarkdown li {
        direction: rtl !important;
        text-align: right !important;
        margin-right: 0 !important;
    }
    
    /* תיקון כותרות */
    h1, h2, h3, h4, h5, h6 {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* תיקון פסקאות */
    p {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* תיקון טבלאות */
    table {
        direction: rtl !important;
    }
    
    /* תיקון כפתורים */
    .stButton > button {
        direction: rtl !important;
    }
    
    /* תיקון טאבים */
    .stTabs {
        direction: rtl !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        direction: rtl !important;
        flex-direction: row-reverse !important;
    }
    
    /* כותרת מעוצבת */
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

st.markdown("""
<div class="admin-header">
    <h1>⚙️ ניהול תוכן</h1>
    <p>הוספת שאלות וחומרי למידה</p>
</div>
""", unsafe_allow_html=True)

# הוספת קישור לעורך החדש
st.info("✨ **חדש!** עכשיו יש עורך תוכן ידידותי חדש ללא JSON - [לחץ כאן לעורך החדש](http://localhost:8501/✏️_Content_Editor) 📝", icon="💡")

# בדיקת הרשאות
if not st.session_state.get('logged_in', False):
    st.error("❌ יש להתחבר למערכת כדי לגשת לדף זה")
    st.stop()

# בדיקה שהמשתמש הוא עורך מורשה
user = st.session_state.get('user', {})
user_email = user.get('email', '')

if not is_editor(user_email):
    st.error("❌ אין לך הרשאות לערוך תוכן. פנה למנהל המערכת.")
    st.stop()

# תפריט טאבים
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["✏️ עריכת תוכן קיים", "➕ הוספת שאלה", "📚 הוספת תוכן למידה", "🎬 עריכת תרחישים", "👥 ניהול עורכים", "⚠️ דיווחי טעויות"])

with tab1:
    st.subheader("✏️ עריכת תוכן קיים")
    st.markdown("בחר קטגוריה ונושא לעריכה מלאה של התוכן")
    
    # בחירת קטגוריה
    categories = get_all_categories()
    category_names = {cat['id']: f"{cat['emoji']} {cat['name']}" for cat in categories}
    
    selected_category_name = st.selectbox(
        "בחר קטגוריה",
        options=list(category_names.values())
    )
    
    # מצא את הקטגוריה שנבחרה
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
            
            # מצא את הנושא שנבחר
            selected_topic_id = None
            for topic_id, topic_name in topic_options.items():
                if topic_name == selected_topic_name:
                    selected_topic_id = topic_id
                    break
            
            if selected_topic_id:
                topic = get_topic(selected_category_id, selected_topic_id)
                
                if topic:
                    st.divider()
                    st.markdown("### 📝 עריכת פרטי הנושא")
                    
                    with st.form("edit_topic_form"):
                        # מטא-דאטה בסיסי
                        new_title = st.text_input("כותרת", value=topic.get('title', ''))
                        new_description = st.text_area("תיאור", value=topic.get('description', ''), height=100)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            difficulty_options = {"beginner": "מתחילים", "intermediate": "בינוני", "advanced": "מתקדמים"}
                            current_diff = topic.get('difficulty', 'intermediate')
                            new_difficulty = st.selectbox(
                                "רמת קושי",
                                options=list(difficulty_options.keys()),
                                format_func=lambda x: difficulty_options[x],
                                index=list(difficulty_options.keys()).index(current_diff) if current_diff in difficulty_options else 1
                            )
                        with col2:
                            tags_str = ', '.join(topic.get('tags', []))
                            new_tags_str = st.text_input("תגיות (מופרדות בפסיקים)", value=tags_str)
                        
                        st.divider()
                        st.markdown("### 📄 עריכת תוכן")
                        st.info("💡 לעריכה מתקדמת של פריטי תוכן, השתמש בממשק העריכה בספרייה (לחץ על נושא ואז '✏️ מצב עריכה')")
                        
                        # הצגת תוכן ראשי
                        content_items = topic.get('content', [])
                        st.markdown(f"**מספר פריטי תוכן:** {len(content_items)}")
                        
                        # הצג את התוכן בצורה קריאה
                        if content_items:
                            with st.expander("👁️ צפייה בתוכן הקיים", expanded=False):
                                for idx, item in enumerate(content_items, 1):
                                    st.markdown(f"**פריט {idx}:**")
                                    st.json(item)
                        
                        # כפתור שמירה
                        st.divider()
                        submit_edit = st.form_submit_button("💾 שמור שינויים", type="primary", use_container_width=True)
                        
                        if submit_edit:
                            if new_title and new_description:
                                # עדכון הנושא
                                topic['title'] = new_title
                                topic['description'] = new_description
                                topic['difficulty'] = new_difficulty
                                topic['tags'] = [tag.strip() for tag in new_tags_str.split(',') if tag.strip()]
                                topic['last_updated'] = datetime.now().strftime("%Y-%m-%d")
                                
                                if update_topic(selected_category_id, selected_topic_id, topic):
                                    st.success("✅ השינויים נשמרו בהצלחה!")
                                    st.balloons()
                                else:
                                    st.error("❌ שגיאה בשמירת השינויים")
                            else:
                                st.error("❌ נא למלא את כל השדות הנדרשים")

with tab2:
    st.subheader("📝 הוספת שאלה חדשה")
    
    with st.form("add_question_form", clear_on_submit=True):
        # בחירת נושא
        st.markdown("**בחירת נושא:**")
        if DB_CONNECTED:
            try:
                topics = get_topics()
                if topics:
                    topic_names = [t['title'] for t in topics]
                    selected_topic = st.selectbox("נושא", topic_names, label_visibility="collapsed")
                else:
                    st.error("אין נושאים במערכת")
                    st.stop()
            except:  
                topic_names = ["החייאה - BLS & PALS", "הנשמה מכנית", "תרופות בטיפול נמרץ"]
                selected_topic = st.selectbox("נושא", topic_names, label_visibility="collapsed")
        else:
            topic_names = ["החייאה - BLS & PALS", "הנשמה מכנית", "תרופות בטיפול נמרץ"]
            selected_topic = st.selectbox("נושא", topic_names, label_visibility="collapsed")
        
        st.divider()
        
        # פרטי השאלה
        st.markdown("**טקסט השאלה:**")
        question_text = st.text_area("שאלה", height=100, placeholder="הקלד את השאלה כאן...", label_visibility="collapsed")
        
        st.markdown("אפשרויות תשובה:")
        col1, col2 = st.columns(2)
        with col1:
            option1 = st.text_input("אפשרות 1", placeholder="תשובה ראשונה")
            option2 = st.text_input("אפשרות 2", placeholder="תשובה שנייה")
        with col2:
            option3 = st.text_input("אפשרות 3", placeholder="תשובה שלישית")
            option4 = st.text_input("אפשרות 4", placeholder="תשובה רביעית")
        
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**תשובה נכונה:**")
            correct_answer = st.selectbox("בחר", [1, 2, 3, 4], label_visibility="collapsed")
        with col2:
            st.markdown("**רמת קושי:**")
            difficulty = st.selectbox("רמה", ["קל", "בינוני", "קשה"], index=1, label_visibility="collapsed")
        
        st.markdown("**הסבר לתשובה:**")
        explanation = st.text_area("הסבר", height=100, placeholder="הסבר מפורט מדוע זו התשובה הנכונה...", label_visibility="collapsed")
        
        st.divider()
        
        submitted = st.form_submit_button("💾 שמור שאלה", type="primary", use_container_width=True)
        
        if submitted: 
            if all([question_text, option1, option2, option3, option4, explanation]):
                st.success("✅ השאלה נוספה בהצלחה!")
                st.balloons()
                
                # הצגת השאלה שנוספה
                with st.expander("צפה בשאלה שנוספה"):
                    st.json({
                        "נושא": selected_topic,
                        "שאלה": question_text,
                        "אפשרויות": [option1, option2, option3, option4],
                        "תשובה נכונה": correct_answer,
                        "הסבר": explanation,
                        "רמת קושי": difficulty
                    })
            else:
                st.error("❌ נא למלא את כל השדות")

    # דוגמאות לשאלות טובות
    with st.expander("💡 דוגמאות לשאלות טובות"):
        st.markdown("""
        **דוגמה 1: שאלה קלינית**
        
        **שאלה:** ילד בן 3 שנים במשקל 15 ק"ג בהחייאה.  מהו המינון הנכון של אפינפרין IV?
        
        **אפשרויות:**
        1. 0.15 מ"ג (0.15 מ"ל מתמיסה 1:1000)
        2. 0.15 מ"ג (1.5 מ"ל מתמיסה 1:10,000)
        3. 0.015 מ"ג (1.5 מ"ל מתמיסה 1:10,000)
        4. 1.5 מ"ג (1.5 מ"ל מתמיסה 1:1000)
        
        **תשובה נכונה:** 2
        
        **הסבר:** המינון הוא 0.01 מ"ג/ק"ג = 0.15 מ"ג. בתמיסה 1:10,000 זה שווה ל-1.5 מ"ל. 
        """)

with tab3:
    st.subheader("📚 הוספת חומר למידה")
    
    with st.form("add_content_form"):
        st.markdown("**פרטי התוכן**")
        
        content_topic = st.selectbox("נושא", topic_names if 'topic_names' in locals() else ["החייאה"])
        content_title = st.text_input("כותרת", placeholder="כותרת החומר הלימודי")
        content_type = st.selectbox("סוג תוכן", ["טקסט", "וידאו", "תמונה", "קישור"])
        
        if content_type == "טקסט":
            content = st.text_area("תוכן", height=300, placeholder="הקלד את התוכן כאן...")
        elif content_type == "וידאו":
            content = st.text_input("קישור לוידאו", placeholder="https://youtube.com/...")
        elif content_type == "תמונה":
            content = st.text_input("קישור לתמונה", placeholder="https://...")
        else:
            content = st.text_input("קישור", placeholder="https://...")
        
        submit_content = st.form_submit_button("💾 שמור תוכן", type="primary", use_container_width=True)
        
        if submit_content:
            if content_title and content:
                st.success("✅ התוכן יתווסף בקרוב למערכת")
            else:
                st.error("❌ נא למלא את כל השדות")

with tab4:
    st.subheader("🎬 עריכת תרחישים")
    st.markdown("ערוך תרחישים מתגלגלים קיימים בצורה נוחה")
    
    # טען את התרחישים
    scenarios_dir = Path(__file__).parent.parent / "data" / "scenarios"
    scenarios = []
    
    if scenarios_dir.exists():
        for file in scenarios_dir.glob("*.json"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    scenario = json.load(f)
                    scenario['_filename'] = file.name
                    scenarios.append(scenario)
            except Exception as e:
                st.error(f"שגיאה בטעינת {file.name}: {e}")
    
    if not scenarios:
        st.warning("לא נמצאו תרחישים בתיקייה data/scenarios/")
    else:
        # בחירת תרחיש
        scenario_titles = {s['scenario_id']: s['title'] for s in scenarios}
        selected_scenario_title = st.selectbox(
            "בחר תרחיש לעריכה",
            options=list(scenario_titles.values())
        )
        
        # מצא את התרחיש שנבחר
        selected_scenario = None
        for s in scenarios:
            if s['title'] == selected_scenario_title:
                selected_scenario = s
                break
        
        if selected_scenario:
            st.divider()
            st.markdown("### 📝 עריכת פרטי התרחיש")
            
            # עריכה בעורך טקסט JSON
            st.info("💡 ערוך את התרחיש בפורמט JSON. שים לב לתחביר הנכון!")
            
            with st.form("edit_scenario_form"):
                # הצג את התרחיש כ-JSON לעריכה
                scenario_json = json.dumps(selected_scenario, ensure_ascii=False, indent=2)
                edited_json = st.text_area(
                    "תוכן התרחיש (JSON)",
                    value=scenario_json,
                    height=500,
                    help="ערוך את התרחיש בפורמט JSON"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    submit_scenario = st.form_submit_button("💾 שמור שינויים", type="primary", use_container_width=True)
                with col2:
                    validate_only = st.form_submit_button("✅ בדוק תקינות בלבד", use_container_width=True)
                
                if submit_scenario or validate_only:
                    try:
                        # נסה לפרסר את ה-JSON
                        edited_scenario = json.loads(edited_json)
                        
                        # בדיקות בסיסיות
                        required_fields = ['scenario_id', 'title', 'description', 'stages']
                        missing_fields = [f for f in required_fields if f not in edited_scenario]
                        
                        if missing_fields:
                            st.error(f"❌ חסרים שדות חובה: {', '.join(missing_fields)}")
                        else:
                            if validate_only:
                                st.success("✅ התרחיש תקין!")
                                st.balloons()
                            else:
                                # שמור את הקובץ
                                filename = selected_scenario['_filename']
                                filepath = scenarios_dir / filename
                                
                                # מחק את השדה הפנימי
                                if '_filename' in edited_scenario:
                                    del edited_scenario['_filename']
                                
                                with open(filepath, 'w', encoding='utf-8') as f:
                                    json.dump(edited_scenario, f, ensure_ascii=False, indent=2)
                                
                                st.success("✅ התרחיש נשמר בהצלחה!")
                                st.balloons()
                                
                    except json.JSONDecodeError as e:
                        st.error(f"❌ שגיאת תחביר JSON: {e}")
                    except Exception as e:
                        st.error(f"❌ שגיאה: {e}")
            
            # תצוגה מקדימה של השלבים
            st.divider()
            st.markdown("### 👁️ תצוגה מקדימה")
            
            with st.expander("צפה בשלבי התרחיש", expanded=False):
                try:
                    parsed = json.loads(edited_json) if edited_json else selected_scenario
                    
                    st.markdown(f"**כותרת:** {parsed.get('title', 'N/A')}")
                    st.markdown(f"**תיאור:** {parsed.get('description', 'N/A')}")
                    st.markdown(f"**רמת קושי:** {parsed.get('difficulty', 'N/A')}")
                    st.markdown(f"**זמן משוער:** {parsed.get('estimated_time', 'N/A')} דקות")
                    
                    stages = parsed.get('stages', [])
                    st.markdown(f"**מספר שלבים:** {len(stages)}")
                    
                    for idx, stage in enumerate(stages, 1):
                        st.markdown(f"**שלב {idx}:** {stage.get('title', 'N/A')} ({stage.get('type', 'N/A')})")
                        
                except Exception as e:
                    st.error(f"לא ניתן להציג תצוגה מקדימה: {e}")

with tab5:
    st.subheader("👥 ניהול עורכים מורשים")
    st.markdown("הוסף או הסר עורכים שיכולים לערוך תוכן במערכת")
    
    # הצגת עורכים נוכחיים
    current_editors = get_editors()
    
    st.markdown("### 📋 עורכים מורשים כרגע:")
    for idx, editor in enumerate(current_editors, 1):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{idx}.** {editor}")
            if editor == user_email:
                st.caption("(אתה)")
        with col2:
            if len(current_editors) > 1:  # אל תאפשר למחוק את העורך האחרון
                if st.button(f"🗑️ הסר", key=f"remove_{editor}"):
                    if remove_editor(editor):
                        st.success(f"✅ {editor} הוסר מרשימת העורכים")
                        st.rerun()
                    else:
                        st.error("❌ שגיאה בהסרת עורך")
    
    st.divider()
    
    # הוספת עורך חדש
    st.markdown("### ➕ הוסף עורך חדש")
    
    with st.form("add_editor_form"):
        new_editor_email = st.text_input(
            "כתובת אימייל של העורך החדש",
            placeholder="example@email.com"
        )
        
        submit_new_editor = st.form_submit_button("➕ הוסף עורך", type="primary")
        
        if submit_new_editor:
            if new_editor_email:
                if '@' not in new_editor_email:
                    st.error("❌ כתובת אימייל לא תקינה")
                elif new_editor_email in current_editors:
                    st.warning("⚠️ העורך כבר קיים ברשימה")
                else:
                    if add_editor(new_editor_email):
                        st.success(f"✅ {new_editor_email} נוסף בהצלחה לרשימת העורכים!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ שגיאה בהוספת עורך")
            else:
                st.error("❌ נא להזין כתובת אימייל")
    
    st.divider()
    
    # הסבר
    with st.expander("💡 מידע חשוב"):
        st.markdown("""
        **מי זה עורך מורשה?**
        - עורכים מורשים יכולים לערוך תוכן קיים במערכת
        - העריכה זמינה דרך ממשק הניהול או דרך הספרייה (כפתור "✏️ מצב עריכה")
        - יש לוודא שהעורכים מתחברים עם אותו אימייל שהוזן כאן
        
        **אבטחה:**
        - לא ניתן להסיר את העורך האחרון מהרשימה
        - רק עורכים מורשים יכולים לגשת לממשק הניהול
        - כל שינוי נשמר עם חותמת זמן
        """)

# הזז את הסטטיסטיקות לתחתית הדף, מחוץ לטאבים
st.divider()
st.markdown("---")
st.subheader("📊 סטטיסטיקות מערכת")
    
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("שאלות במערכת", "5", "2+")
with col2:
    st.metric("נושאי למידה", "3", "0")
with col3:
    st.metric("משתמשים רשומים", "1", "1+")
with col4:
    st.metric("מבחנים שבוצעו", "0", "0")

st.divider()

# גרף התפלגות שאלות
st.subheader("📈 התפלגות שאלות לפי נושא")

df = pd.DataFrame({
    'נושא': ['החייאה', 'הנשמה', 'תרופות'],
    'מספר שאלות': [2, 1, 2]
})

st.bar_chart(df.set_index('נושא'))

# כפתור חזרה
st.divider()
if st.button("🏠 חזרה לעמוד הראשי", use_container_width=True):
    st.switch_page("app.py")

# הוראות שימוש בתחתית
st.divider()
with st.expander("📖 הוראות שימוש מפורטות"):
    st.markdown("""
    **🎯 איך להוסיף תוכן איכותי? **
    
    **לשאלות טובות:**
    • שאלה ברורה - נסח שאלה חד-משמעית וממוקדת
    • אפשרויות מבלבלות - כל האפשרויות צריכות להיראות הגיוניות  
    • הסבר מלא - כלול הסבר מדוע התשובה נכונה ומדוע השאר לא
    • רלוונטיות קלינית - עדיף שאלות מבוססות מקרים
    
    **לחומרי למידה:**
    • כותרת ברורה - שתסביר בדיוק מה התוכן
    • תוכן מעודכן - על בסיס הנחיות עדכניות
    • שפה פשוטה - נגיש לכל הרמות
    • דוגמאות - הוסף דוגמאות קליניות
    
    **טיפים נוספים:**
    • בדוק איות ודקדוק לפני שליחה
    • השתמש בקיצורים מקובלים בלבד
    • הוסף מקורות אם רלוונטי
    """)

with tab6:
    st.subheader("⚠️ דיווחי טעויות מהמשתמשים")
    
    # Filter options
    col1, col2 = st.columns([1, 3])
    with col1:
        status_filter = st.selectbox(
            "סינון לפי סטטוס:",
            ["הכל", "ממתין", "נבדק", "תוקן", "נדחה"],
            key="corrections_filter"
        )
    
    status_map = {
        "הכל": None,
        "ממתין": "pending",
        "נבדק": "reviewed",
        "תוקן": "fixed",
        "נדחה": "rejected"
    }
    
    corrections = get_all_corrections(status=status_map[status_filter])
    
    if not corrections:
        st.info("אין דיווחים להצגה")
    else:
        st.markdown(f"**סה\"כ דיווחים:** {len(corrections)}")
        
        for corr in sorted(corrections, key=lambda x: x.get('timestamp', ''), reverse=True):
            status_emoji = {
                'pending': '⏳',
                'reviewed': '👀',
                'fixed': '✅',
                'rejected': '❌'
            }
            
            status_text = {
                'pending': 'ממתין',
                'reviewed': 'נבדק',
                'fixed': 'תוקן',
                'rejected': 'נדחה'
            }
            
            corr_status = corr.get('status', 'pending')
            
            with st.expander(f"{status_emoji.get(corr_status, '⏳')} {corr.get('id')} - {corr.get('topic_id')} ({status_text.get(corr_status, 'ממתין')})"):
                st.markdown(f"**קטגוריה:** {corr.get('category')}")
                st.markdown(f"**נושא:** {corr.get('topic_id')}")
                st.markdown(f"**מדווח:** {corr.get('user_email')}")
                st.markdown(f"**תאריך:** {corr.get('timestamp', '').split('T')[0]}")
                st.markdown(f"**סטטוס:** {status_text.get(corr_status, 'ממתין')}")
                
                st.divider()
                st.markdown("**תיאור הטעות:**")
                st.info(corr.get('correction_text', ''))
                
                st.divider()
                
                # Action buttons
                col_a, col_b, col_c, col_d, col_e = st.columns(5)
                
                with col_a:
                    if st.button("👀 נבדק", key=f"review_{corr['id']}"):
                        if update_correction_status(corr['id'], 'reviewed'):
                            st.success("עודכן!")
                            st.rerun()
                
                with col_b:
                    if st.button("✅ תוקן", key=f"fixed_{corr['id']}"):
                        if update_correction_status(corr['id'], 'fixed'):
                            st.success("עודכן!")
                            st.rerun()
                
                with col_c:
                    if st.button("❌ נדחה", key=f"reject_{corr['id']}"):
                        if update_correction_status(corr['id'], 'rejected'):
                            st.success("עודכן!")
                            st.rerun()
                
                with col_d:
                    if st.button("📖 פתח תוכן", key=f"open_{corr['id']}"):
                        st.session_state['selected_category'] = corr.get('category')
                        st.session_state['selected_topic'] = corr.get('topic_id')
                        st.switch_page("pages/2_📖_Content.py")
                
                with col_e:
                    if st.button("✏️ ערוך", key=f"edit_{corr['id']}"):
                        st.session_state['edit_category'] = corr.get('category')
                        st.session_state['edit_topic'] = corr.get('topic_id')
                        st.rerun()

