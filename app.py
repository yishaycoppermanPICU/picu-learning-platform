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
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom:  2rem;
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        margin:  0;
    }
    
    .main-header p {
        color: #f0f0f0;
        font-size: 1.2rem;
    }
    
    .feature-card {
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# אתחול session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st. session_state:
    st. session_state.user = None
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

# סרגל צד - כניסה מהירה
with st.sidebar:
    st.title("🔐 כניסה למערכת")
    st.caption(f"מסד נתונים: {db_status}")
    
    if not st.session_state.logged_in:
        st.subheader("כניסה מהירה - בלי סיסמה!")
        
        with st.form("quick_login_form"):
            full_name = st.text_input("👤 שם מלא", placeholder="לדוגמה: ישי קופרמן")
            email = st.text_input("📧 מייל", placeholder="example@hospital.org. il")
            
            # טעינת רשימת מוסדות
            if DB_CONNECTED:
                try:
                    institutions = get_institutions()
                    inst_names = [inst['name'] for inst in institutions] if institutions else []
                except: 
                    inst_names = []
            else:
                inst_names = ["מרכז שניידר", "הדסה עין כרם", "רמב״ם", "שיבא - תל השומר"]
            
            if inst_names:
                institution = st.selectbox("🏥 בחר מוסד", [""] + sorted(inst_names))
            else:
                institution = st.text_input("🏥 מוסד")
            
            agree_terms = st.checkbox("אני מאשר/ת שימוש למטרות למידה בלבד")
            
            submitted = st.form_submit_button("🚀 כניסה מהירה", type="primary", use_container_width=True)
            
            if submitted:
                if not all([full_name, email, institution, agree_terms]):
                    st.error("נא למלא את כל השדות ולאשר את התנאים")
                else: 
                    # יצירת username מהמייל
                    username = email. split('@')[0].replace('.', '_').replace('-', '_')
                    
                    if DB_CONNECTED:
                        # בדיקה אם המשתמש קיים
                        existing_user = authenticate_user(username)
                        
                        if existing_user: 
                            st.session_state.logged_in = True
                            st.session_state.user = existing_user
                            st.success(f"ברוך הבא חזרה, {existing_user['full_name']}!")
                            st.rerun()
                        else:
                            # יצירת משתמש חדש
                            import random
                            attempts = 0
                            while attempts < 5:
                                try:
                                    new_username = username if attempts == 0 else f"{username}{random.randint(100,999)}"
                                    new_user = create_user(new_username, email, full_name, institution)
                                    if new_user:
                                        st.session_state.logged_in = True
                                        st.session_state.user = new_user
                                        st.success(f"ברוך הבא, {full_name}!")
                                        st.balloons()
                                        st.rerun()
                                        break
                                except: 
                                    attempts += 1
                            
                            if attempts >= 5:
                                st. error("שגיאה ביצירת משתמש.  נסה שוב.")
                    else:
                        # Demo mode - כניסה בלי מסד נתונים
                        st.session_state.logged_in = True
                        st.session_state.user = {
                            'username': username,
                            'full_name':  full_name,
                            'email': email,
                            'institutions': {'name': institution}
                        }
                        st. success(f"ברוך הבא, {full_name}!  (Demo Mode)")
                        st.rerun()
        
        st.divider()
        
        with st.expander("💡 למה בלי סיסמה?"):
            st.info("""
            • פלטפורמה למידה פתוחה לכולם
            • אין מידע רפואי רגיש
            • גישה מהירה ונוחה
            • המידע שלך נשמר לפי המייל
            """)
    
    else:
        # משתמש מחובר
        user_info = st.session_state.user
        st. success(f"👋 שלום, {user_info. get('full_name', 'משתמש')}!")
        
        if 'institutions' in user_info and user_info['institutions']: 
            st.info(f"🏥 {user_info['institutions']. get('name', 'לא ידוע')}")
        
        col1, col2 = st. columns(2)
        with col1:
            if st.button("📊 הנתונים שלי", use_container_width=True):
                st.session_state.show_stats = True
        with col2:
            if st.button("🚪 יציאה", use_container_width=True):
                st. session_state.logged_in = False
                st.session_state.user = None
                st. rerun()
    
    st.divider()
    
    # מידע על המערכת
    with st.expander("ℹ️ אודות המערכת"):
        st.markdown("""
        **👨‍⚕️ פותח על ידי:**  
        ישי קופרמן  
        אח בטיפול נמרץ ילדים  
        מרצה בבית ספר לסיעוד
        
        **📧 יצירת קשר:**  
        yishay.cooperman@gmail. com
        
        **🎯 מטרת הפלטפורמה:**  
        שיפור הידע והמיומנויות של צוותי PICU
        
        **📅 גרסה:** 1.0.0  
        **🔄 עדכון אחרון:** 25/12/2024
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
        st.markdown("### ברוך הבא לפלטפורמת הלמידה!")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="feature-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                <h3>📚 חומרי למידה</h3>
                <p>גישה לחומרי למידה מעודכנים מבוססי UpToDate</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class="feature-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white;">
                <h3>📝 תרגול ומבחנים</h3>
                <p>מבחנים אינטראקטיביים עם משוב מיידי</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            <div class="feature-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white;">
                <h3>🏆 תחרות בין-מוסדית</h3>
                <p>השווה את הביצועים שלך מול מוסדות אחרים</p>
            </div>
            """, unsafe_allow_html=True)
        
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
                st.metric("ציון ממוצע", "—")
        with col3:
            st.metric("זמן למידה", "0 שעות")
        with col4:
            st.metric("דירוג במוסד", "—")
    
    with tab2:
        st.title("📚 חומרי למידה")
        
        if DB_CONNECTED:
            topics = get_topics()
            if topics:
                for topic in topics:
                    with st.expander(f"{topic. get('icon', '📚')} {topic['title']}"):
                        st. write(topic. get('description', ''))
                        st.info("תוכן מפורט יתווסף בקרוב")
            else:
                st.info("אין נושאים זמינים כרגע")
        else:
            st.info("חומרי הלמידה יהיו זמינים בקרוב")
    
    with tab3:
        st. title("📝 מבחנים ותרגול")
        st.info("המבחנים יהיו זמינים בקרוב")
    
    with tab4:
        st.title("📊 הסטטיסטיקות שלי")
        
        if st.session_state.user_scores:
            df = pd.DataFrame({
                'מבחן': range(1, len(st.session_state.user_scores) + 1),
                'ציון': st.session_state. user_scores
            })
            st.line_chart(df.set_index('מבחן'))
        else:
            st.info("עדיין אין נתונים להצגה")
    
    with tab5:
        st.title("🏆 לוח תוצאות - תחרות בין-מוסדית")
        
        if DB_CONNECTED:
            leaderboard = get_leaderboard()
            if leaderboard: 
                df = pd.DataFrame(leaderboard)
                df['דירוג'] = range(1, len(df) + 1)
                df['דירוג'] = df['דירוג'].apply(lambda x: 
                    f"🥇 {x}" if x == 1 else 
                    f"🥈 {x}" if x == 2 else 
                    f"🥉 {x}" if x == 3 else f"{x}")
                
                st.dataframe(df, hide_index=True, use_container_width=True)
            else:
                st.info("אין נתונים להצגה עדיין")
        else:
            # Demo data
            demo_data = pd.DataFrame({
                'דירוג': ['🥇 1', '🥈 2', '🥉 3'],
                'מוסד': ['הדסה עין כרם', 'מרכז שניידר', 'רמב״ם'],
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
        - 📚 חומרי למידה מעודכנים מבוססי UpToDate
        - 📝 מבחנים אינטראקטיביים עם משוב מיידי
        - 📊 מעקב אחר התקדמות אישית
        - 🏆 תחרות בריאה בין מוסדות רפואיים
        
        **הצטרף עכשיו - בלי סיסמה, בלי סיבוכים!**
        """)

# כתב ויתור
st.divider()
st.caption("""
⚠️ **כתב ויתור:** האתר מיועד למטרות למידה בלבד. האחריות לאימות התוכן עם מקורות רפואיים מעודכנים היא על המשתמש.
""")
