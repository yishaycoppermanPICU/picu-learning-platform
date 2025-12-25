import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

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

# CSS לעברית ועיצוב
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;700&display=swap');
    
    * {
        font-family: 'Heebo', sans-serif;
    }
    
    .stApp {
        direction: rtl;
    }
    
    .main-header {
        text-align: center;
        color: #1f77b4;
        padding:  2rem;
        background:  linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom:  2rem;
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        margin: 0;
    }
    
    .main-header p {
        color: #f0f0f0;
        font-size: 1.2rem;
    }
    
    .feature-card {
        padding: 1.5rem;
        border-radius: 10px;
        height: 100%;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    
    . feature-card:hover {
        transform: translateY(-5px);
    }
    
    . success-message {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        color: #155724;
    }
    
    .error-message {
        padding: 1rem;
        background-color:  #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)

# אתחול session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state. user = None
if 'user_scores' not in st.session_state:
    st.session_state.user_scores = []

# כותרת ראשית
st.markdown("""
<div class="main-header">
    <h1>🏥 PICU Learning Platform</h1>
    <p>פלטפורמת למידה מתקדמת לטיפול נמרץ ילדים</p>
</div>
""", unsafe_allow_html=True)

# בדיקת חיבור למסד נתונים
if DB_CONNECTED:
    db_status = "🟢 מחובר"
else:
    db_status = "🔴 לא מחובר"

# סרגל צד - התחברות
with st.sidebar:
    st. title("🔐 כניסה למערכת")
    
    # הצגת סטטוס חיבור
    st.caption(f"מסד נתונים: {db_status}")
    
    if not st.session_state.logged_in:
        tab1, tab2 = st.tabs(["התחברות", "הרשמה"])
        
        with tab1:
            st. subheader("התחברות")
            with st.form("login_form"):
                username = st.text_input("שם משתמש")
                password = st.text_input("סיסמה", type="password")
                
                submitted = st.form_submit_button("התחבר", type="primary")
                
                if submitted:
                    if username and password:
                        if DB_CONNECTED:
                            user = authenticate_user(username)
                            if user:
                                st.session_state.logged_in = True
                                st.session_state.user = user
                                st.success(f"ברוך הבא, {user['full_name']}!")
                                st.rerun()
                            else:
                                st.error("שם משתמש לא קיים")
                        else: 
                            # Demo mode
                            st.session_state.logged_in = True
                            st.session_state. user = {
                                'username': username,
                                'full_name': username,
                                'institution': {'name': 'Demo'}
                            }
                            st.rerun()
                    else:
                        st. error("נא למלא את כל השדות")
        
        with tab2:
            st.subheader("הרשמה למערכת")
            with st.form("register_form"):
                new_username = st.text_input("בחר שם משתמש")
                email = st.text_input("כתובת מייל")
                full_name = st.text_input("שם מלא")
                
                # טעינת רשימת מוסדות
                if DB_CONNECTED:
                    institutions = get_institutions()
                    inst_names = [inst['name'] for inst in institutions]
                else:
                    inst_names = ["מרכז שניידר", "הדסה עין כרם", "רמב״ם"]
                
                institution = st.selectbox("מוסד", [""] + inst_names)
                new_password = st.text_input("סיסמה", type="password")
                confirm_password = st.text_input("אימות סיסמה", type="password")
                
                register_submitted = st.form_submit_button("הרשם", type="primary")
                
                if register_submitted:
                    if all([new_username, email, full_name, institution, new_password, confirm_password]):
                        if new_password != confirm_password:
                            st.error("הסיסמאות אינן תואמות")
                        elif DB_CONNECTED: 
                            user = create_user(new_username, email, full_name, institution)
                            if user:
                                st.success("נרשמת בהצלחה! התחבר עם שם המשתמש שלך")
                            else:
                                st.error("שגיאה בהרשמה - ייתכן ושם המשתמש תפוס")
                        else: 
                            st.success("נרשמת בהצלחה! (Demo Mode)")
                    else:
                        st.error("נא למלא את כל השדות")
    
    else:
        user_info = st.session_state.user
        st.success(f"שלום, {user_info. get('full_name', user_info. get('username', 'משתמש'))}!")
        
        if 'institutions' in user_info and user_info['institutions']:
            st.info(f"מוסד: {user_info['institutions']['name']}")
        elif 'institution' in user_info:
            st.info(f"מוסד: {user_info['institution']. get('name', 'לא ידוע')}")
        
        if st.button("התנתק"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st. rerun()
    
    st.divider()
    
    # מידע על המערכת
    st.info("""
    **פותח על ידי:**
    ישי קופרמן
    מרצה בבית ספר לסיעוד
    אח בטיפול נמרץ ילדים
    
    **גרסה:** 1.0.0
    
    **עדכון אחרון:** 
    25/12/2024
    """)

# תוכן ראשי
if st.session_state.logged_in:
    # תפריט ניווט
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏠 ראשי", 
        "📚 למידה", 
        "📝 מבחנים", 
        "📊 הסטטיסטיקות שלי",
        "🏆 לוח תוצאות"
    ])
    
    with tab1:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("""
            ### 📚 חומרי למידה
            גישה לחומרי למידה מעודכנים
            מבוססים על UpToDate
            """)
            
        with col2:
            st.success("""
            ### 📝 תרגול ומבחנים
            מבחנים אינטראקטיביים
            עם משוב מיידי
            """)
            
        with col3:
            st.warning("""
            ### 🏆 תחרות בין מוסדית
            השווה את הביצועים שלך
            מול מוסדות אחרים
            """)
        
        # סטטיסטיקות מהירות
        st.markdown("---")
        st.subheader("📈 הסטטיסטיקות שלך")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("מבחנים שהושלמו", len(st.session_state.user_scores))
        with col2:
            if st.session_state.user_scores:
                avg = sum(st.session_state. user_scores) / len(st.session_state.user_scores)
                st.metric("ציון ממוצע", f"{avg:.1f}%")
            else:
                st.metric("ציון ממוצע", "0%")
        with col3:
            st.metric("זמן למידה כולל", "0 שעות")
        with col4:
            st.metric("דירוג במוסד", "-")
    
    with tab2:
        st.title("📚 חומרי למידה")
        
        # טעינת נושאים ממסד הנתונים
        if DB_CONNECTED:
            topics = get_topics()
            if topics:
                topic_names = [t['title'] for t in topics]
                selected_topic = st.selectbox("בחר נושא ללמידה:", [""] + topic_names)
                
                if selected_topic: 
                    topic_data = next((t for t in topics if t['title'] == selected_topic), None)
                    if topic_data:
                        st.header(f"{topic_data. get('icon', '📚')} {selected_topic}")
                        st.info(topic_data.get('description', ''))
            else:
                st.warning("אין נושאים זמינים כרגע")
        else:
            st.info("חומרי למידה יהיו זמינים בקרוב")
    
    with tab3:
        st.title("📝 מבחנים ותרגול")
        st.info("המבחנים יהיו זמינים בקרוב")
    
    with tab4:
        st.title("📊 הסטטיסטיקות שלי")
        
        if st.session_state.user_scores:
            df = pd.DataFrame({
                'מבחן': range(1, len(st.session_state.user_scores) + 1),
                'ציון': st.session_state.user_scores
            })
            st.line_chart(df.set_index('מבחן'))
        else:
            st.info("עדיין אין נתונים להצגה")
    
    with tab5:
        st.title("🏆 לוח תוצאות - תחרות בין מוסדית")
        
        if DB_CONNECTED:
            leaderboard = get_leaderboard()
            if leaderboard: 
                df = pd.DataFrame(leaderboard)
                
                # עיצוב הטבלה
                df['דירוג'] = range(1, len(df) + 1)
                df['דירוג'] = df['דירוג'].apply(lambda x: 
                    f"🥇 {x}" if x == 1 else 
                    f"🥈 {x}" if x == 2 else 
                    f"🥉 {x}" if x == 3 else 
                    f"{x}")
                
                columns_order = ['דירוג', 'institution_name', 'avg_score', 'total_users', 'total_quizzes']
                df = df[columns_order]
                df.columns = ['דירוג', 'מוסד', 'ציון ממוצע', 'משתתפים', 'מבחנים']
                
                st.dataframe(df, hide_index=True, use_container_width=True)
            else:
                st.info("אין נתונים להצגה עדיין")
        else:
            # Demo data
            demo_data = pd.DataFrame({
                'דירוג': ['🥇 1', '🥈 2', '🥉 3'],
                'מוסד':  ['הדסה עין כרם', 'מרכז שניידר', 'רמב״ם'],
                'ציון ממוצע': [92, 88, 85],
                'משתתפים': [15, 12, 10]
            })
            st.dataframe(demo_data, hide_index=True)

else:
    # אם לא מחובר
    st.warning("👈 התחבר מהתפריט הצדדי כדי להתחיל ללמוד")
    
    with st.expander("ℹ️ אודות הפלטפורמה"):
        st.markdown("""
        ### ברוכים הבאים לפלטפורמת הלמידה PICU!
        
        פלטפורמה זו נוצרה כדי להעשיר ולחדד את הידע של צוותי טיפול נמרץ ילדים.
        
        **מה תמצאו כאן:**
        - חומרי למידה מעודכנים מבוססי UpToDate
        - מבחנים אינטראקטיביים עם משוב מיידי
        - מעקב אחר התקדמות אישית
        - תחרות בריאה בין מוסדות רפואיים
        
        **חשוב לדעת:**
        - התוכן מבוסס על מקורות רפואיים מהימנים
        - האתר למטרות למידה בלבד
        - האחריות לאימות המידע על המשתמש
        """)

# כתב ויתור
st.divider()
st.caption("""
⚠️ **כתב ויתור:** האתר מיועד למטרות למידה בלבד. האחריות לאימות התוכן עם מקורות רפואיים מעודכנים היא על המשתמש.
במקרה של טעות או אי דיוק, נא ליצור קשר:  yishay.cooperman@gmail.com
""")
