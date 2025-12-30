# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os
import base64
import streamlit.components.v1 as components
import extra_streamlit_components as stx
from urllib.parse import quote
import re

# ייבוא פונקציות ניהול תוכן
from utils.content_manager import get_user_by_email, save_user, update_last_login
from utils.styles import get_common_styles
from utils.weekly_content import (
    get_current_weekly_content,
    get_week_start_end,
    format_hebrew_date,
    get_user_weekly_stats,
    check_weekly_completion
)
from utils.badges import get_badge_html, get_badge_card_html

# ייבוא פונקציות מסד נתונים
try:
    from utils.database import (
        init_supabase,
        get_topics,
        get_institutions,
        create_user,
        authenticate_user,
        get_leaderboard,
        get_content_item
    )
    DB_CONNECTED = True
except Exception as e:
    DB_CONNECTED = False
    print(f"Database connection error: {e}")

# הגדרות עמוד
st.set_page_config(
    page_title="ישי קופרמן | טיפול נמרץ ילדים",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="auto"  # אוטומטי - פתוח בדסקטופ, סגור במובייל
)

# טעינת Material Icons (תיקון סופי ל-ke / אייקונים שבורים)
st.markdown('<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">', unsafe_allow_html=True)

# טעינת CSS מרכזי
st.markdown(get_common_styles(), unsafe_allow_html=True)

# יצירת cookie manager לשמירת מייל
cookie_manager = stx.CookieManager()

# אתחול session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'user_scores' not in st.session_state:
    st.session_state.user_scores = []

# בדיקה אם יש משתמש שמור (שחזור לאחר רענון)
try:
    # טעינת המייל השמור מ-cookies
    saved_email = cookie_manager.get('user_email')
    
    if saved_email and not st.session_state.logged_in:
        # Try to restore user session
        existing_user = get_user_by_email(saved_email)
        
        if existing_user:
            # Restore session
            username = saved_email.split('@')[0].replace('.', '_').replace('-', '_')
            st.session_state.logged_in = True
            st.session_state.user = {
                'username': username,
                'full_name': existing_user.get('name', ''),
                'email': saved_email,
                'institution': existing_user.get('hospital', ''),
                'institutions': {'name': existing_user.get('hospital', '')}
            }
            update_last_login(saved_email)
except:
    pass

# כותרת ראשית - לוגו ללא רקע, מיושר לימין (RTL)
st.markdown("""
<style>
/* חסימה מוחלטת של קישור GitHub בלבד */
header a[href*="github"],
header a[href*="github"] * {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    width: 0 !important;
    height: 0 !important;
    position: absolute !important;
    left: -9999px !important;
    pointer-events: none !important;
}

/* מאפשר לכפתור הסיידבר המקורי לעבוד */
button[kind="header"],
button[data-testid="collapsedControl"],
button[kind="header"] *,
button[data-testid="collapsedControl"] * {
    pointer-events: all !important;
    cursor: pointer !important;
}
</style>
""", unsafe_allow_html=True)

logo_candidates = [
    "לוגו רשמי ישי רקע שקוף.png",
    "לוגו רשמי ישי ללא רקע.png",
    "לוגו רשמי של ישי.png",
]

logo_to_show = next((path for path in logo_candidates if os.path.exists(path)), None)

if logo_to_show:
    with open(logo_to_show, "rb") as logo_file:
        logo_base64 = base64.b64encode(logo_file.read()).decode()
    st.markdown(
        f"""
        <div class="app-header-bar">
            <div class="app-header-logo">
                <img src="data:image/png;base64,{logo_base64}" alt="לוגו ישי קופרמן" class="app-header-logo-img" />
            </div>
            <div class="app-header-text">
                <h1 class="hero-topline">ישי קופרמן | טיפול נמרץ ילדים</h1>
                <p class="hero-tagline">פלטפורמת למידה מתקדמת לצוותי PICU</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.warning("לא נמצא קובץ הלוגו", icon="⚠️")

# בדיקת חיבור למסד נתונים
if DB_CONNECTED:
    db_status = "מחובר 🟢"
else: 
    db_status = "לא מחובר 🔴"

# סרגל צד
with st.sidebar:
    # כותרת - אימוג'י בסוף
    st.markdown("## מערכת כניסה 🔐")
    st.caption(f"סטטוס מסד נתונים: {db_status}")
    
    if not st.session_state.logged_in:
        st.markdown("### התחברות מהירה 🚀")
        
        # Initialize session state for form fields
        if 'form_email' not in st.session_state:
            # נסה לטעון מייל שמור מ-cookies
            saved_email = cookie_manager.get('user_email')
            st.session_state.form_email = saved_email if saved_email else ""
        if 'form_name' not in st.session_state:
            st.session_state.form_name = ""
        if 'form_hospital' not in st.session_state:
            st.session_state.form_hospital = ""
        
        # Email input with auto-complete
        email_input = st.text_input(
            "דואר אלקטרוני:",
            value=st.session_state.form_email,
            placeholder="your@email.com",
            key="email_field"
        )
        
        # Auto-fill when email changes
        if email_input and email_input != st.session_state.form_email:
            st.session_state.form_email = email_input
            # Check if user exists
            existing_user = get_user_by_email(email_input)
            if existing_user:
                st.session_state.form_name = existing_user.get('name', '')
                st.session_state.form_hospital = existing_user.get('hospital', '')
                st.info("✨ מצאתי את הפרטים שלך! נא לאשר או לעדכן")
                st.rerun()
        
        with st.form("login_form"):
            # שדות - מוזנים אוטומטית אם המשתמש קיים
            full_name = st.text_input(
                "שם מלא:",
                value=st.session_state.form_name,
                placeholder="הזן את שמך המלא"
            )
            
            # כפל את המייל (מוסתר)
            email = st.session_state.form_email
            st.caption(f"📧 מייל: {email if email else 'לא הוזן'}")
            
            # רשימת מוסדות
            if DB_CONNECTED:
                try:
                    institutions = get_institutions()
                    inst_names = [inst['name'] for inst in institutions] if institutions else []
                except: 
                    inst_names = []
            else:
                inst_names = [
                    "שיבא - תל השומר",
                    "איכילוב - תל אביב",
                    "רמב״ם - חיפה",
                    "הדסה עין כרם - ירושלים",
                    "סורוקה - באר שבע",
                    "מרכז שניידר לרפואת ילדים",
                    "בלינסון - פתח תקווה"
                ]
            
            if inst_names:
                # Find index of saved hospital
                default_idx = 0
                if st.session_state.form_hospital:
                    hospital_list = [""] + sorted(inst_names) + ["אחר ➕"]
                    if st.session_state.form_hospital in hospital_list:
                        default_idx = hospital_list.index(st.session_state.form_hospital)
                
                institution = st.selectbox(
                    "בחר מוסד רפואי:",
                    [""] + sorted(inst_names) + ["אחר ➕"],
                    index=default_idx
                )
            else:
                institution = st.text_input(
                    "שם המוסד:",
                    value=st.session_state.form_hospital
                )
            
            if institution == "אחר ➕": 
                institution = st.text_input("הכנס שם מוסד:")
            
            agree = st.checkbox("מאשר/ת שימוש למטרות למידה ✓")
            
            # כפתור - אימוג'י בסוף
            submitted = st.form_submit_button("🔐 התחבר למערכת", type="primary", use_container_width=True)
            
            if submitted: 
                if full_name and email and institution and institution != "" and agree:
                    # Save user to local file
                    save_user(email, full_name, institution)
                    
                    username = email.split('@')[0].replace('.', '_').replace('-', '_')
                    
                    # שמירת המייל ב-cookies (נשמר 30 ימים)
                    try:
                        cookie_manager.set('user_email', email, expires_at=datetime.now() + pd.Timedelta(days=30))
                    except:
                        pass  # אם יש בעיה עם cookies, ממשיכים בלי
                    
                    # עדכון session state מיידי
                    st.session_state.logged_in = True
                    
                    if DB_CONNECTED:
                        try:
                            existing = authenticate_user(username)
                            if existing:
                                st.session_state.user = existing
                                update_last_login(email)
                                st.success(f"ברוך שובך, {existing['full_name']} 👋")
                            else: 
                                new_user = create_user(username, email, full_name, institution)
                                if new_user: 
                                    st.session_state.user = new_user
                                    st.success(f"ברוך הבא, {full_name} 🎉")
                                    st.balloons()
                                else:
                                    # אם נכשל ליצור במסד, ניצור משתמש מקומי
                                    st.session_state.user = {
                                        'username': username,
                                        'full_name': full_name,
                                        'email': email,
                                        'institutions': {'name': institution}
                                    }
                        except Exception as e:
                            # במקרה של שגיאה, ניצור משתמש מקומי
                            st.session_state.user = {
                                'username': username,
                                'full_name': full_name,
                                'email': email,
                                'institutions': {'name': institution}
                            }
                            st.warning(f"התחברת במצב מקומי")
                    else:
                        st.session_state.user = {
                            'username': username,
                            'full_name': full_name,
                            'email': email,
                            'institutions': {'name': institution}
                        }
                        st.success(f"ברוך הבא, {full_name}!")
                    
                    # רענון מיידי
                    st.rerun()
                else:
                    if not email:
                        st.error("נא להזין כתובת מייל תחילה ❌")
                    else:
                        st.error("נא למלא את כל השדות ❌")
        
        st.divider()
        
        with st.expander("למה כניסה בלי סיסמה? ❓"):
            st.write("**יתרונות:**")
            st.write("- ללא צורך בסיסמה מסובכת")
            st.write("- גישה מיידית לתוכן")
            st.write("- המידע נשמר לפי המייל שלך")
            st.write("- אפשרות לכניסה עם Google בקרוב")
        
        with st.expander("✨ שמירה אוטומטית של פרטים"):
            st.write("**המערכת זוכרת אותך!**")
            st.write("- הזן את המייל שלך")
            st.write("- אם התחברת בעבר, הפרטים ימולאו אוטומטית")
            st.write("- פשוט אשר ולחץ התחבר")
            st.write("- חוסך זמן בכל כניסה למערכת 🚀")
    
    else:
        # משתמש מחובר
        user = st.session_state.user
        st.success(f"מחובר: {user.get('full_name', 'משתמש')} ✓")
        
        if 'institutions' in user and user['institutions']:
            st.info(f"מוסד: {user['institutions'].get('name', '')} 🏥")
        
        if st.button("📊 הנתונים שלי", use_container_width=True):
            st.switch_page("pages/3_סטטיסטיקה.py")
        
        if st.button("🚪 התנתק", use_container_width=True):
            # מחיקת המייל מה-cookies
            cookie_manager.delete('user_email')
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
    
    st.divider()
    
    # אודות
    with st.expander("אודות המערכת"):
        st.write("**פותח על ידי:** ישי קופרמן")
        st.write("**תפקיד:** אח בטיפול נמרץ ילדים")
        st.write("**מייל:** yishaycopp@gmail.com")
        st.write("**גרסה:** 1.0.0")
        st.write("**עדכון אחרון:** 26/12/2024")

# תוכן ראשי
if st.session_state.logged_in:
    user = st.session_state.user
    user_email = user.get('email', '')
    st.markdown(f"**שלום {user.get('full_name', 'משתמש')}!** 👋")
    
    st.divider()
    
    # ===== תוכן שבועי מומלץ =====
    weekly_content = get_current_weekly_content()
    week_start, week_end = get_week_start_end()
    
    # בדיקה אם השלים את התוכן השבועי
    is_completed = False
    if user_email:
        is_completed = check_weekly_completion(user_email)
    
    # כרטיס תוכן שבועי בולט (לבן, קריא, ללא אימוג'ים)
    completion_badge = "הושלם" if is_completed else "ממתין לביצוע"
    completion_color = "#28a745" if is_completed else "#ffc107"
    
    week_title = weekly_content['title']
    week_desc = weekly_content['description']
    week_icon = weekly_content['icon']
    week_num = weekly_content['week_number']
    start_date = format_hebrew_date(week_start)
    end_date = format_hebrew_date(week_end).split(',')[1].strip()
    
    weekly_html = f'''<div style="background: #FFFFFF; border-radius: 10px; padding: 2rem; box-shadow: 0 4px 12px rgba(0,0,0,0.08); border: 1px solid #E0E0E0; border-top: 4px solid #00796B; margin-bottom: 2rem;">
        <div style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">{week_icon}</div>
            <h2 style="color: #333333; font-size: 1.9rem; font-weight: 700; margin: 0;">תוכן מומלץ השבוע</h2>
            <p style="color: #666666; font-size: 1rem; margin-top: 0.3rem;">שבוע {week_num} • {start_date} - {end_date}</p>
        </div>
        <div style="margin: 1.5rem 0; padding: 1.5rem; background: #F8F9FA; border-radius: 8px; border: 1px solid #EEEEEE;">
            <h3 style="color: #00796B; text-align: center; margin: 0 0 0.5rem 0; font-size: 1.4rem; font-weight: 600;">{week_title}</h3>
            <p style="color: #333333; text-align: center; line-height: 1.6; font-size: 1.05rem; margin: 0;">{week_desc}</p>
        </div>
        <div style="text-align: center;">
            <span style="background: {completion_color}; color: white; padding: 0.5rem 1.5rem; border-radius: 6px; font-weight: 600; font-size: 1rem;">{completion_badge}</span>
        </div>
    </div>'''
    
    st.markdown(weekly_html, unsafe_allow_html=True)
    
    # כפתורי פעולה לתוכן השבועי
    st.markdown("##### פעולות לתוכן השבועי")
    col1, col2, col3 = st.columns(3)
    
    # Callback functions for buttons
    def start_weekly_quiz():
        st.session_state['selected_quiz_category'] = weekly_content.get('quiz_category', weekly_content['category'])
        st.session_state['weekly_topic_id'] = weekly_content.get('topic_id')
        st.session_state['weekly_title'] = weekly_content.get('title')
        st.session_state['weekly_topic_slug'] = weekly_content.get('quiz_topic')
        st.session_state['weekly_quiz'] = True
    
    def view_weekly_topic():
        st.session_state['selected_topic_id'] = weekly_content['topic_id']
        st.session_state['view_weekly_content'] = True
    
    with col1:
        if st.button(f"למד: {weekly_content['title'][:20]}...", type="primary", use_container_width=True, key="weekly_learn", on_click=view_weekly_topic):
            st.switch_page("pages/7_נושאי_לימוד.py")
    
    with col2:
        if st.button(f"מבחן בנושא", use_container_width=True, key="weekly_quiz_btn", on_click=start_weekly_quiz):
            st.switch_page("pages/5_בחנים.py")
    
    with col3:
        if st.button("תגי ההישגים שלי", use_container_width=True):
            st.switch_page("pages/3_סטטיסטיקה.py")
    
    # בדיקה אם יש מבחן שמור
    if st.session_state.get('quiz_paused') and st.session_state.get('quiz_active') and st.session_state.get('quiz_questions'):
        st.divider()
        st.warning("📝 יש לך מבחן שמור שלא הושלם!")
        
        topic_title = st.session_state.quiz_config.get('topic_title', 'מבחן')
        current = st.session_state.current_question + 1
        total = len(st.session_state.quiz_questions)
        answered = len([a for a in st.session_state.quiz_answers if not a.get('skipped')])
        
        st.info(f"""
        **{topic_title}**
        
        📊 התקדמות: שאלה {current} מתוך {total}
        
        ✅ נענית על {answered} שאלות
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➡️ המשך מבחן", type="primary", use_container_width=True):
                st.session_state['quiz_paused'] = False
                st.switch_page("pages/5_בחנים.py")
        with col2:
            if st.button("🗑️ מחק ותתחיל מחדש", use_container_width=True):
                st.session_state.quiz_active = False
                st.session_state.quiz_questions = []
                st.session_state.current_question = 0
                st.session_state.quiz_answers = []
                st.session_state['quiz_paused'] = False
                st.session_state['weekly_quiz'] = False
                if 'selected_topic_for_quiz' in st.session_state:
                    del st.session_state['selected_topic_for_quiz']
                st.success("✅ המבחן נמחק")
                st.rerun()
    
    # הצגת תגים קיימים אם יש
    if user_email:
        user_stats = get_user_weekly_stats(user_email)
        if user_stats['total_badges'] > 0:
            st.markdown("### התגים שלך השבוע 🎖️")
            badges_html = ""
            recent_badges = user_stats.get('badges', [])[-3:]  # 3 האחרונים
            for badge in recent_badges:
                badges_html += get_badge_html('excellence', 'medium')
            st.markdown(badges_html, unsafe_allow_html=True)
    
    st.divider()
    
    # כרטיסיות ראשיות בעיצוב "ספרייה רפואית" – קליקים על כל הכרטיס
    st.markdown("### ניווט מהיר 🚀")

    nav_cards = [
        {
            "title": "ספריית תוכן",
            "desc": "חומרי למידה מקצועיים ומעודכנים",
            "svg": """
                <svg width='56' height='56' viewBox='0 0 120 120' fill='none' xmlns='http://www.w3.org/2000/svg'>
                    <rect x='18' y='24' width='84' height='72' rx='10' stroke='#1f2f3d' stroke-width='5' opacity='0.9'/>
                    <path d='M24 44h72' stroke='#0d8a7b' stroke-width='5' stroke-linecap='round'/>
                    <path d='M36 86l12-18 10 10 14-22 12 14 10-18' stroke='#f5a524' stroke-width='6' stroke-linecap='round' stroke-linejoin='round'/>
                    <circle cx='36' cy='86' r='4' fill='#1f2f3d'/>
                    <circle cx='48' cy='68' r='4' fill='#1f2f3d'/>
                    <circle cx='58' cy='78' r='4' fill='#1f2f3d'/>
                    <circle cx='72' cy='56' r='4' fill='#1f2f3d'/>
                    <circle cx='84' cy='70' r='4' fill='#1f2f3d'/>
                    <circle cx='94' cy='52' r='4' fill='#1f2f3d'/>
                </svg>
            """,
            "page": "pages/1_ספריית_תוכן.py"
        },
        {
            "title": "הנתונים שלי",
            "desc": "מעקב התקדמות וסטטיסטיקות",
            "svg": """
                <svg width='56' height='56' viewBox='0 0 120 120' fill='none' xmlns='http://www.w3.org/2000/svg'>
                    <rect x='24' y='20' width='20' height='80' rx='3' fill='#1ab0a0' opacity='0.85'/>
                    <rect x='48' y='24' width='20' height='76' rx='3' fill='#1f2f3d' opacity='0.9'/>
                    <rect x='72' y='30' width='20' height='70' rx='3' fill='#0d8a7b' opacity='0.9'/>
                    <path d='M26 42h16M26 54h16M50 50h16M74 58h16' stroke='white' stroke-width='3' stroke-linecap='round' opacity='0.9'/>
                    <circle cx='32' cy='32' r='3' fill='white'/>
                    <circle cx='56' cy='36' r='3' fill='white'/>
                    <circle cx='80' cy='42' r='3' fill='white'/>
                </svg>
            """,
            "page": "pages/3_סטטיסטיקה.py"
        },
        {
            "title": "לוח הישגים",
            "desc": "תחרות בין-מוסדית",
            "svg": """
                <svg width='56' height='56' viewBox='0 0 120 120' fill='none' xmlns='http://www.w3.org/2000/svg'>
                    <path d='M40 24h40v32a20 20 0 0 1-40 0V24z' fill='#1f2f3d'/>
                    <path d='M36 24h48v10H36z' fill='#0d8a7b'/>
                    <circle cx='60' cy='46' r='12' fill='#f5a524'/>
                    <path d='M52 92l8-24 8 24' stroke='#1f2f3d' stroke-width='6' stroke-linecap='round' stroke-linejoin='round'/>
                    <rect x='44' y='92' width='32' height='10' rx='3' fill='#1ab0a0'/>
                </svg>
            """,
            "page": "pages/4_דירוג.py"
        }
    ]

    def _page_param(page_path: str) -> str:
        """Convert page file name to Streamlit page query param."""
        fname = page_path.split('/')[-1]
        stem = fname[:-3] if fname.endswith('.py') else fname
        if re.match(r"^\d+_", stem):
            stem = stem.split('_', 1)[1]
        page_title = stem.replace('_', ' ')
        return quote(page_title)

    st.markdown(
        """
<style>
.nav-card-box {
    background: #ffffff;
    border: 1.5px solid #e6e9ed;
    border-radius: 14px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.05);
    padding: 1.25rem 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    direction: rtl;
    position: relative;
    overflow: hidden;
    transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
}
.nav-card-box::before {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(120deg, rgba(13,138,123,0.08), transparent 45%);
    pointer-events: none;
}
.nav-card-box::after {
    content: "";
    position: absolute;
    inset-inline-start: 0;
    top: 0;
    width: 6px;
    height: 100%;
    background: linear-gradient(180deg, var(--teal, #0d8a7b) 0%, var(--teal-light, #1ab0a0) 100%);
    border-radius: 0 10px 10px 0;
}
.nav-card-box:hover {
    transform: translateY(-6px);
    box-shadow: 0 16px 32px rgba(0,0,0,0.08);
    border-color: var(--teal, #0d8a7b);
}
.nav-illus {
    flex: 0 0 88px;
    height: 88px;
    border-radius: 12px;
    background: radial-gradient(circle at 30% 30%, rgba(13,138,123,0.18), transparent 60%),
                radial-gradient(circle at 70% 70%, rgba(31,47,61,0.12), transparent 65%);
    display: grid;
    place-items: center;
}
.nav-copy h3 {
    margin: 0 0 0.25rem 0;
    font-size: 1.32rem;
    font-weight: 800;
    color: #1b2735;
    letter-spacing: -0.2px;
}
.nav-copy p {
    margin: 0;
    font-size: 1.05rem;
    color: #3b4a5a;
    font-weight: 500;
}
.nav-button {
    margin-top: 0.4rem;
}
</style>
""",
        unsafe_allow_html=True,
    )

    cols = st.columns(3)
    for idx, card in enumerate(nav_cards):
        with cols[idx % 3]:
            st.markdown(
                f"""
<div class='nav-card-box'>
    <div class='nav-illus'>{card['svg']}</div>
    <div class='nav-copy'>
        <h3>{card['title']}</h3>
        <p>{card['desc']}</p>
    </div>
</div>
""",
                unsafe_allow_html=True,
            )
            if st.button(
                "פתח",
                key=f"nav-card-{idx}",
                type="secondary",
                use_container_width=True,
            ):
                st.switch_page(card["page"])
    
    st.divider()
    
    # סטטיסטיקות מהירות
    st.markdown("### הסטטיסטיקות שלך במבט 📈")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("מבחנים שהושלמו", len(st.session_state.user_scores))
    with col2:
        if st.session_state.user_scores:
            avg = sum(st.session_state.user_scores) / len(st.session_state.user_scores)
            st.metric("ציון ממוצע", f"{avg:.1f}%")
        else:
            st.metric("ציון ממוצע", "—")
    with col3:
        if user_email:
            user_stats = get_user_weekly_stats(user_email)
            st.metric("שבועות שהושלמו", user_stats['completed_weeks'])
        else:
            st.metric("שבועות שהושלמו", "0")
    with col4:
        if user_email:
            user_stats = get_user_weekly_stats(user_email)
            st.metric("תגי מצטיין", user_stats['total_badges'])
        else:
            st.metric("תגי מצטיין", "0")
    
    st.divider()
    
    # מידע נוסף
    with st.expander("💡 עצות למידה", expanded=False):
        st.write("**כיצד להפיק את המרב מהפלטפורמה:**")
        st.write("- התחל עם נושאים בסיסיים ועבור לנושאים מתקדמים")
        st.write("- הקדש לפחות 5 דקות ביום ללמידה")
        st.write("- השלם את התוכן המומלץ מדי שבוע לצבירת תגים")
        st.write("- חזור על חומרים שקשים לך")
        st.write("- השתמש בחומרים כהשלמה לניסיון הקליני")
        st.write("- שתף ידע עם עמיתים")

else:
    # משתמש לא מחובר
    st.warning("יש להתחבר כדי לגשת לתוכן 🔐")
    
    # כרטיסיות מידע
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("### למידה מתקדמת 📚\nחומרי למידה מעודכנים ומותאמים לצוותי PICU")
    
    with col2:
        st.info("### מבחנים אינטראקטיביים 📝\nתרגול עם משוב מיידי ומעקב התקדמות")
    
    with col3:
        st.info("### תחרות ארצית 🏆\nהשווה את עצמך לעמיתים מכל הארץ")
    
    with st.expander("מידע על הפלטפורמה", expanded=False):
        st.write("**מטרת הפלטפורמה:**")
        st.write("פלטפורמה זו נוצרה כדי להעשיר ולחדד את הידע של צוותי טיפול נמרץ ילדים.")
        st.write("")
        st.write("**מה תמצאו כאן:**")
        st.write("- חומרי למידה מעודכנים על בסיס UpToDate 📚")
        st.write("- מבחנים אינטראקטיביים עם משוב מיידי 📝")
        st.write("- מעקב אחר התקדמות אישית 📈")
        st.write("- תחרות בריאה בין מוסדות רפואיים 🏆")
        st.write("")
        st.write("**איך מתחילים:**")
        st.write("פשוט הירשמו עם המייל שלכם - ללא סיסמה!")

# כתב ויתור בתחתית
st.divider()
st.caption("הערה: האתר מיועד למטרות למידה בלבד.  האחריות לאימות התוכן עם מקורות רפואיים מעודכנים היא על המשתמש ⚠️")
