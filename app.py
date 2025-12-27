# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# ייבוא פונקציות ניהול תוכן
from utils.content_manager import get_user_by_email, save_user, update_last_login

# ייבוא פונקציות מסד נתונים
try:
    from utils.database import (
        init_supabase,
        get_topics,
        get_institutions,
        create_user,
        authenticate_user,
        get_leaderboard
    )
    DB_CONNECTED = True
except Exception as e:
    DB_CONNECTED = False
    print(f"Database connection error: {e}")

# הגדרות עמוד
st.set_page_config(
    page_title="PICU Learning Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS פשוט אבל יעיל
st.markdown("""
<style>
    /* RTL גלובלי */
    .stApp {
        direction: rtl;
    }
    
    /* הזזת סרגל צד לימין */
    section[data-testid="stSidebar"] {
        right: 0;
        left: auto;
    }
    
    section[data-testid="stSidebar"] > div {
        right: 0;
        left: auto;
    }
    
    /* תיקון התוכן הראשי */
    .main .block-container {
        padding-right: 5rem;
        padding-left: 1rem;
    }
    
    /* טקסט ימין */
    h1, h2, h3, h4, h5, h6, p, label, span {
        text-align: right;
        direction: rtl;
    }
    
    /* תיקון טאבים */
    .stTabs [data-baseweb="tab-list"] {
        flex-direction: row-reverse;
    }
    
    /* תיקון שדות קלט */
    input, textarea, select {
        direction: rtl;
        text-align: right;
    }
    
    /* הכותרת הראשית */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .main-header h1, .main-header p {
        color: white;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

# אתחול session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'user_scores' not in st.session_state:
    st.session_state.user_scores = []

# בדיקה אם יש משתמש שמור (שחזור לאחר רענון)
try:
    query_params = st.query_params
    if 'user_email' in query_params and not st.session_state.logged_in:
        # Try to restore user session
        saved_email = query_params['user_email']
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

# כותרת ראשית
st.title("🏥 פלטפורמת למידה PICU")
st.markdown("### פלטפורמת למידה מתקדמת לטיפול נמרץ ילדים")

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
            st.session_state.form_email = ""
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
                    
                    # Save email to query params for persistence
                    st.query_params['user_email'] = email
                    
                    if DB_CONNECTED:
                        try:
                            existing = authenticate_user(username)
                            if existing:
                                st.session_state.logged_in = True
                                st.session_state.user = existing
                                update_last_login(email)
                                st.success(f"ברוך שובך, {existing['full_name']} 👋")
                                st.rerun()
                            else: 
                                new_user = create_user(username, email, full_name, institution)
                                if new_user: 
                                    st.session_state.logged_in = True
                                    st.session_state.user = new_user
                                    st.success(f"ברוך הבא, {full_name} 🎉")
                                    st.balloons()
                                    st.rerun()
                        except Exception as e:
                            st.error(f"שגיאה: {e}")
                    else:
                        st.session_state.logged_in = True
                        st.session_state.user = {
                            'username': username,
                            'full_name': full_name,
                            'email': email,
                            'institutions': {'name': institution}
                        }
                        st.success(f"ברוך הבא, {full_name}!")
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
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("הנתונים שלי 📊", use_container_width=True):
                st.switch_page("pages/3_📊_Statistics.py")
        with col2:
            if st.button("התנתק 🚪", use_container_width=True):
                # Clear query params
                if 'user_email' in st.query_params:
                    del st.query_params['user_email']
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
    st.markdown(f"**שלום {user.get('full_name', 'משתמש')}!** 👋")
    
    st.divider()
    
    # כרטיסיות ראשיות עם כפתורים מובילים
    st.markdown("### ניווט מהיר 🚀")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 10px; text-align: center; color: white;'>
            <h2 style='color: white;'>📚</h2>
            <h3 style='color: white;'>ספריית תוכן</h3>
            <p style='color: white;'>חומרי למידה מקצועיים ומעודכנים</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("כניסה לספרייה", key="library_btn", use_container_width=True, type="primary"):
            st.switch_page("pages/1_📚_Library.py")
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 2rem; border-radius: 10px; text-align: center; color: white;'>
            <h2 style='color: white;'>📊</h2>
            <h3 style='color: white;'>הנתונים שלי</h3>
            <p style='color: white;'>מעקב התקדמות וסטטיסטיקות</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("צפייה בסטטיסטיקות", key="stats_btn", use_container_width=True, type="primary"):
            st.switch_page("pages/3_📊_Statistics.py")
    
    with col3:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 2rem; border-radius: 10px; text-align: center; color: white;'>
            <h2 style='color: white;'>🏆</h2>
            <h3 style='color: white;'>לוח הישגים</h3>
            <p style='color: white;'>תחרות בין-מוסדית</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("לוח התוצאות", key="leaderboard_btn", use_container_width=True, type="primary"):
            st.switch_page("pages/4_🏆_Leaderboard.py")
    
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
        st.metric("זמן למידה", "0 שעות")
    with col4:
        st.metric("דירוג במוסד", "—")
    
    st.divider()
    
    # מידע נוסף
    with st.expander("💡 עצות למידה"):
        st.write("**כיצד להפיק את המרב מהפלטפורמה:**")
        st.write("- התחל עם נושאים בסיסיים ועבור לנושאים מתקדמים")
        st.write("- הקדש לפחות 15-30 דקות ביום ללמידה")
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
    
    with st.expander("מידע על הפלטפורמה"):
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
