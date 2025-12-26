# -*- coding: utf-8 -*-
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
""", unsafe_allow_html=True)

# אתחול session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state. user = None
if 'user_scores' not in st.session_state:
    st.session_state.user_scores = []

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
        
        with st.form("login_form"):
            # שדות - אימוג'י בסוף התווית
            full_name = st.text_input("שם מלא:", placeholder="הזן את שמך המלא")
            email = st.text_input("דואר אלקטרוני:", placeholder="your@email.com")
            
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
                institution = st.selectbox("בחר מוסד רפואי:", [""] + sorted(inst_names) + ["אחר ➕"])
            else:
                institution = st.text_input("שם המוסד:")
            
            if institution == "אחר ➕": 
                institution = st.text_input("הכנס שם מוסד:")
            
            agree = st.checkbox("מאשר/ת שימוש למטרות למידה ✓")
            
            # כפתור - אימוג'י בסוף
            submitted = st.form_submit_button("התחבר למערכת ◀", type="primary", use_container_width=True)
            
            if submitted: 
                if full_name and email and institution and institution != "" and agree:
                    username = email.split('@')[0].replace('.', '_').replace('-', '_')
                    
                    if DB_CONNECTED:
                        try:
                            existing = authenticate_user(username)
                            if existing:
                                st.session_state.logged_in = True
                                st.session_state.user = existing
                                st.success(f"ברוך שובך, {existing['full_name']} 👋")
                                st.rerun()
                            else: 
                                new_user = create_user(username, email, full_name, institution)
                                if new_user: 
                                    st.session_state.logged_in = True
                                    st.session_state. user = new_user
                                    st.success(f"ברוך הבא, {full_name} 🎉")
                                    st.balloons()
                                    st. rerun()
                        except Exception as e:
                            st. error(f"שגיאה: {e}")
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
                    st.error("נא למלא את כל השדות ❌")
        
        st.divider()
        
        with st.expander("למה כניסה בלי סיסמה? ❓"):
            st.markdown("""
            **יתרונות:**
            - ללא צורך בסיסמה מסובכת
            - גישה מיידית לתוכן
            - המידע נשמר לפי המייל שלך
            - אפשרות לכניסה עם Google בקרוב
            """)
    
    else:
        # משתמש מחובר
        user = st.session_state.user
        st.success(f"מחובר: {user.get('full_name', 'משתמש')} ✓")
        
        if 'institutions' in user and user['institutions']:
            st.info(f"מוסד: {user['institutions'].get('name', '')} 🏥")
        
        col1, col2 = st. columns(2)
        with col1:
            if st.button("הנתונים שלי 📊", use_container_width=True):
                st.switch_page("pages/3_📊_Statistics.py")
        with col2:
            if st.button("התנתק 🚪", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.user = None
                st.rerun()
    
    st.divider()
    
    # אודות
    with st.expander("אודות המערכת ℹ️"):
        st.markdown("""
        **פותח על ידי:** ישי קופרמן 👨‍⚕️  
        **תפקיד:** אח בטיפול נמרץ ילדים  
        **מייל:** yishaycopp@gmail.com 📧  
        **גרסה:** 1.0.0  
        **עדכון אחרון:** 26/12/2024 📅
        """)

# תוכן ראשי
if st.session_state.logged_in:
    # טאבים - אימוג'ים בסוף! 
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "דף הבית 🏠",
        "חומרי למידה 📚",
        "מבחנים ותרגול 📝",
        "הנתונים שלי 📊",
        "לוח הישגים 🏆"
    ])
    
    with tab1:
        st.markdown("### ברוכים הבאים לפלטפורמת הלמידה!  🎯")
        
        # כרטיסיות
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="feature-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                <h3>חומרי למידה 📚</h3>
                <p>גישה לחומרי למידה מעודכנים מבוססי UpToDate</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                <h3>תרגול ומבחנים 📝</h3>
                <p>מבחנים אינטראקטיביים עם משוב מיידי</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="feature-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                <h3>תחרות בין-מוסדית 🏆</h3>
                <p>השווה את הביצועים שלך מול מוסדות אחרים</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        st.markdown("### הסטטיסטיקות שלך 📈")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("מבחנים שהושלמו", len(st.session_state.user_scores))
        with col2:
            if st.session_state.user_scores:
                avg = sum(st.session_state. user_scores) / len(st.session_state.user_scores)
                st.metric("ציון ממוצע", f"{avg:.1f}%")
            else:
                st.metric("ציון ממוצע", "—")
        with col3:
            st.metric("זמן למידה", "0 שעות")
        with col4:
            st.metric("דירוג במוסד", "—")
    
    with tab2:
        st.markdown("### חומרי למידה 📚")
        
        if DB_CONNECTED:
            try:
                topics = get_topics()
                if topics:
                    for topic in topics:
                        title = topic. get('title', 'נושא')
                        icon = topic.get('icon', '📖')
                        with st.expander(f"{title} {icon}"):
                            st.write(topic.get('description', ''))
                            st.info("תוכן מפורט יתווסף בקרוב ⏳")
                else:
                    st.info("אין נושאים זמינים כרגע 📭")
            except: 
                st.warning("בעיה בטעינת הנושאים ⚠️")
        else:
            st.warning("חומרי למידה יהיו זמינים בקרוב 🔜")
    
    with tab3:
        st.markdown("### מבחנים ותרגול 📝")
        st.info("מערכת המבחנים תהיה זמינה בקרוב 🚀")
        
        # כפתורים לדוגמה
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("מבחן אקראי 🎲", disabled=True, use_container_width=True)
        with col2:
            st.button("מבחן לפי נושא 📚", disabled=True, use_container_width=True)
        with col3:
            st.button("מבחן מותאם אישית ⚙", disabled=True, use_container_width=True)
    
    with tab4:
        st. markdown("### הסטטיסטיקות שלי 📊")
        
        if st.session_state.user_scores:
            df = pd.DataFrame({
                'מספר מבחן': range(1, len(st.session_state.user_scores) + 1),
                'ציון':  st.session_state.user_scores
            })
            st.line_chart(df.set_index('מספר מבחן'))
            
            # סטטיסטיקות
            col1, col2, col3 = st.columns(3)
            with col1:
                best_score = max(st.session_state.user_scores)
                st.success(f"הציון הטוב ביותר: {best_score}% 🌟")
            with col2:
                avg_score = sum(st.session_state.user_scores) / len(st.session_state.user_scores)
                st.info(f"ממוצע:  {avg_score:.1f}% 📊")
            with col3:
                last_score = st.session_state.user_scores[-1]
                st.warning(f"ציון אחרון: {last_score}% 📝")
        else:
            st.info("עדיין אין נתונים להצגה 📈")
            if st.button("התחל את המבחן הראשון שלך 🚀", type="primary"):
                st.switch_page("pages/2_📝_Quizzes.py")
    
    with tab5:
        st.markdown("### לוח הישגים - תחרות בין-מוסדית 🏆")
        
        if DB_CONNECTED:
            try: 
                leaderboard = get_leaderboard()
                if leaderboard:
                    df = pd.DataFrame(leaderboard)
                    st.dataframe(df, hide_index=True, use_container_width=True)
                else:
                    st.info("אין נתונים להצגה עדיין 📊")
            except:
                st.warning("בעיה בטעינת הנתונים ⚠️")
        else:
            # נתוני דמו
            demo_data = pd.DataFrame({
                'דירוג': ['🥇', '🥈', '🥉', '4', '5'],
                'מוסד': [
                    'שיבא - תל השומר',
                    'איכילוב - תל אביב',
                    'רמב״ם - חיפה',
                    'הדסה עין כרם',
                    'סורוקה - באר שבע'
                ],
                'ציון ממוצע': [88.4, 88.3, 88.1, 86.0, 82.9],
                'משתתפים': [10, 27, 9, 8, 30]
            })
            st.dataframe(demo_data, hide_index=True, use_container_width=True)
            
            # גרף
            st.bar_chart(demo_data.set_index('מוסד')['ציון ממוצע'])

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
    
    with st.expander("מידע על הפלטפורמה ℹ"):
        st.markdown("""
        **מטרת הפלטפורמה:**
        פלטפורמה זו נוצרה כדי להעשיר ולחדד את הידע של צוותי טיפול נמרץ ילדים.
        
        **מה תמצאו כאן:**
        • חומרי למידה מעודכנים על בסיס UpToDate 📚  
        • מבחנים אינטראקטיביים עם משוב מיידי 📝  
        • מעקב אחר התקדמות אישית 📈  
        • תחרות בריאה בין מוסדות רפואיים 🏆  
        
        **איך מתחילים:**
        פשוט הירשמו עם המייל שלכם - ללא סיסמה! ✨
        
        **פותח על ידי:**
        ישי קופרמן - אח בטיפול נמרץ ילדים
        """)

# כתב ויתור בתחתית
st.divider()
st.caption("הערה: האתר מיועד למטרות למידה בלבד.  האחריות לאימות התוכן עם מקורות רפואיים מעודכנים היא על המשתמש ⚠️")
