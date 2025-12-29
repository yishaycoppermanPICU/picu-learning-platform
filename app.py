# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os
import extra_streamlit_components as stx

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

# כותרת ראשית - מותאמת למובייל
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

.main-title {
        font-size: 1.3rem !important;
        line-height: 1.4 !important;
        text-align: center;
    }
    .main-subtitle {
        font-size: 0.9rem !important;
        text-align: center;
    }
}
.main-title {
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}
.main-subtitle {
    font-size: 1.2rem;
    color: #666;
}
</style>
<div class="main-title">🏥 ישי קופרמן | טיפול נמרץ ילדים</div>
<div class="main-subtitle">פלטפורמת למידה מתקדמת לצוותי PICU</div>
""", unsafe_allow_html=True)

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
            submitted = st.form_submit_button("התחבר למערכת ◀", type="primary", use_container_width=True)
            
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
    st.markdown("### ברוכים הבאים לפלטפורמת הלמידה! 🎯")
    
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
    
    # כרטיס תוכן שבועי בולט
    completion_badge = "✅ הושלם!" if is_completed else "📌 ממתין"
    completion_color = "#28a745" if is_completed else "#ffc107"
    
    week_title = weekly_content['title']
    week_desc = weekly_content['description']
    week_icon = weekly_content['icon']
    week_num = weekly_content['week_number']
    start_date = format_hebrew_date(week_start)
    end_date = format_hebrew_date(week_end).split(',')[1].strip()
    
    weekly_html = f'''<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; color: white; box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);">
        <div style="text-align: center;">
            <h1 style="color: white; font-size: 3rem; margin: 0;">{week_icon}</h1>
            <h2 style="color: white; margin: 0.5rem 0;">תוכן מומלץ השבוע</h2>
            <p style="color: rgba(255,255,255,0.9); font-size: 0.9rem; margin: 0.3rem 0;">שבוע {week_num} • {start_date} - {end_date}</p>
        </div>
        <div style="background: rgba(255,255,255,0.15); backdrop-filter: blur(10px); padding: 1.5rem; border-radius: 12px; margin-top: 1.5rem;">
            <h3 style="color: white; text-align: center; margin: 0 0 1rem 0;">{week_title}</h3>
            <p style="color: rgba(255,255,255,0.95); text-align: center; line-height: 1.8; margin: 0 0 1rem 0;">{week_desc}</p>
            <div style="text-align: center; margin-top: 1.5rem;">
                <span style="background: {completion_color}; color: white; padding: 0.5rem 1.5rem; border-radius: 20px; font-weight: 600; font-size: 1rem;">{completion_badge}</span>
            </div>
        </div>
        <div style="text-align: center; margin-top: 1.5rem;">
            <p style="color: rgba(255,255,255,0.9); font-size: 0.95rem;">💡 <strong>משימת השבוע:</strong> למד את הנושא המומלץ והשלם מבחן עם ציון מעל 80% לקבלת תג מצטיין!</p>
        </div>
    </div>'''
    
    st.markdown(weekly_html, unsafe_allow_html=True)
    
    # כפתורי פעולה לתוכן השבועי
    st.markdown("##### 🎯 פעולות לתוכן השבועי")
    col1, col2, col3 = st.columns(3)
    
    # Callback functions for buttons
    def start_weekly_quiz():
        st.session_state['selected_quiz_category'] = weekly_content.get('quiz_category', weekly_content['category'])
        st.session_state['weekly_quiz'] = True
    
    def view_weekly_topic():
        st.session_state['selected_topic_id'] = weekly_content['topic_id']
        st.session_state['view_weekly_content'] = True
    
    with col1:
        if st.button(f"📖 למד: {weekly_content['title'][:20]}...", type="primary", use_container_width=True, key="weekly_learn", on_click=view_weekly_topic):
            st.switch_page("pages/7_נושאי_לימוד.py")
    
    with col2:
        if st.button(f"✍️ התמחה בנושא: מבחן", use_container_width=True, key="weekly_quiz_btn", on_click=start_weekly_quiz):
            st.switch_page("pages/5_בחנים.py")
    
    with col3:
        if st.button("🏆 תגי ההישגים שלי", use_container_width=True):
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
            if st.button("▶️ המשך מבחן", type="primary", use_container_width=True):
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
    
    # כרטיסיות ראשיות עם כפתורים מובילים
    st.markdown("### ניווט מהיר 🚀")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2.5rem; border-radius: 16px; text-align: center; color: white;
                    box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);'>
            <svg width="80" height="80" viewBox="0 0 100 100" style="margin-bottom: 1rem;">
                <rect x="20" y="15" width="15" height="70" fill="white" opacity="0.9" rx="2"/>
                <rect x="40" y="20" width="15" height="65" fill="white" opacity="0.95" rx="2"/>
                <rect x="60" y="25" width="15" height="60" fill="white" rx="2"/>
                <circle cx="27.5" cy="30" r="2" fill="#667eea"/>
                <circle cx="47.5" cy="35" r="2" fill="#667eea"/>
                <circle cx="67.5" cy="40" r="2" fill="#667eea"/>
                <line x1="22" y1="40" x2="33" y2="40" stroke="#667eea" stroke-width="1.5"/>
                <line x1="22" y1="50" x2="33" y2="50" stroke="#667eea" stroke-width="1.5"/>
                <line x1="22" y1="60" x2="33" y2="60" stroke="#667eea" stroke-width="1.5"/>
                <line x1="42" y1="45" x2="53" y2="45" stroke="#667eea" stroke-width="1.5"/>
                <line x1="42" y1="55" x2="53" y2="55" stroke="#667eea" stroke-width="1.5"/>
                <line x1="62" y1="50" x2="73" y2="50" stroke="#667eea" stroke-width="1.5"/>
                <line x1="62" y1="60" x2="73" y2="60" stroke="#667eea" stroke-width="1.5"/>
            </svg>
            <h2 style='color: white; font-size: 2.8rem; margin: 1rem 0 0.5rem 0; font-weight: 700;'>ספריית תוכן</h2>
            <p style='color: rgba(255,255,255,0.95); font-size: 1.3rem; font-weight: 500;'>חומרי למידה מקצועיים ומעודכנים</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("כניסה לספרייה", key="library_btn", use_container_width=True, type="primary"):
            st.switch_page("pages/1_ספריית_תוכן.py")
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 2.5rem; border-radius: 16px; text-align: center; color: white;
                    box-shadow: 0 8px 24px rgba(240, 147, 251, 0.3);'>
            <svg width="80" height="80" viewBox="0 0 100 100" style="margin-bottom: 1rem;">
                <rect x="15" y="15" width="70" height="70" fill="none" stroke="white" stroke-width="3" rx="4"/>
                <line x1="15" y1="35" x2="85" y2="35" stroke="white" stroke-width="2"/>
                <line x1="35" y1="35" x2="35" y2="85" stroke="white" stroke-width="2"/>
                <polyline points="45,65 50,55 55,60 60,50 65,55 70,45 75,50" 
                          fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="45" cy="65" r="3" fill="white"/>
                <circle cx="50" cy="55" r="3" fill="white"/>
                <circle cx="55" cy="60" r="3" fill="white"/>
                <circle cx="60" cy="50" r="3" fill="white"/>
                <circle cx="65" cy="55" r="3" fill="white"/>
                <circle cx="70" cy="45" r="3" fill="white"/>
                <circle cx="75" cy="50" r="3" fill="white"/>
            </svg>
            <h2 style='color: white; font-size: 2.8rem; margin: 1rem 0 0.5rem 0; font-weight: 700;'>הנתונים שלי</h2>
            <p style='color: rgba(255,255,255,0.95); font-size: 1.3rem; font-weight: 500;'>מעקב התקדמות וסטטיסטיקות</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("צפייה בסטטיסטיקות", key="stats_btn", use_container_width=True, type="primary"):
            st.switch_page("pages/3_סטטיסטיקה.py")
    
    with col3:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 2.5rem; border-radius: 16px; text-align: center; color: white;
                    box-shadow: 0 8px 24px rgba(79, 172, 254, 0.3);'>
            <svg width="80" height="80" viewBox="0 0 100 100" style="margin-bottom: 1rem;">
                <path d="M 50 20 L 60 45 L 85 45 L 65 60 L 75 85 L 50 70 L 25 85 L 35 60 L 15 45 L 40 45 Z" 
                      fill="white" stroke="rgba(255,255,255,0.5)" stroke-width="2"/>
                <circle cx="50" cy="50" r="15" fill="none" stroke="white" stroke-width="2" opacity="0.5"/>
                <text x="50" y="58" font-size="20" font-weight="bold" fill="#4facfe" text-anchor="middle">1</text>
            </svg>
            <h2 style='color: white; font-size: 2.8rem; margin: 1rem 0 0.5rem 0; font-weight: 700;'>לוח הישגים</h2>
            <p style='color: rgba(255,255,255,0.95); font-size: 1.3rem; font-weight: 500;'>תחרות בין-מוסדית</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("לוח התוצאות", key="leaderboard_btn", use_container_width=True, type="primary"):
            st.switch_page("pages/4_דירוג.py")
    
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
