import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

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
</style>
""", unsafe_allow_html=True)

# אתחול session state
if 'logged_in' not in st.session_state:
    st.session_state. logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'institution' not in st.session_state:
    st.session_state.institution = None
if 'user_scores' not in st.session_state:
    st.session_state.user_scores = []

# כותרת ראשית
st.markdown("""
<div class="main-header">
    <h1>🏥 PICU Learning Platform</h1>
    <p>פלטפורמת למידה מתקדמת לטיפול נמרץ ילדים</p>
</div>
""", unsafe_allow_html=True)

# סרגל צד - התחברות
with st.sidebar:
    st.title("🔐 כניסה למערכת")
    
    if not st.session_state.logged_in:
        with st.form("login_form"):
            username = st.text_input("שם משתמש")
            password = st.text_input("סיסמה", type="password")
            institution = st.selectbox("מוסד רפואי", [
                "",
                "מרכז שניידר לרפואת ילדים",
                "הדסה עין כרם",
                "רמב״ם",
                "סורוקה",
                "שיבא - תל השומר",
                "אסף הרופא",
                "וולפסון",
                "מרכז רפואי אחר"
            ])
            
            submitted = st.form_submit_button("התחבר", type="primary")
            
            if submitted: 
                if username and password and institution:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.institution = institution
                    st.rerun()
                else:
                    st.error("נא למלא את כל השדות")
    else:
        st.success(f"שלום, {st.session_state.username}!")
        st.info(f"מוסד: {st.session_state.institution}")
        if st.button("התנתק"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st. session_state.institution = None
            st.rerun()
    
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
            st.metric("מבחנים שהושלמו", "0")
        with col2:
            st.metric("ציון ממוצע", "0%")
        with col3:
            st.metric("זמן למידה כולל", "0 שעות")
        with col4:
            st.metric("דירוג במוסד", "-")
    
    with tab2:
        st.title("📚 חומרי למידה")
        
        # בחירת נושא
        topic = st.selectbox("בחר נושא ללמידה:", [
            "",
            "החייאה - BLS & PALS",
            "הנשמה מכנית",
            "תרופות בטיפול נמרץ",
            "הלם ספטי",
            "טראומה בילדים",
            "נוירולוגיה",
            "קרדיולוגיה",
            "נפרולוגיה ודיאליזה"
        ])
        
        if topic == "החייאה - BLS & PALS":
            st.header("החייאה בילדים - PALS 2020")
            
            with st.expander("📖 אלגוריתם PALS", expanded=True):
                st. markdown("""
                ### שלבי ההחייאה הבסיסיים:
                
                **1. בדיקת תגובתיות**
                - קריאה בקול רם
                - נגיעה עדינה
                
                **2. קריאה לעזרה**
                - הפעלת צוות החייאה
                - הבאת עגלת החייאה ודפיברילטור
                
                **3. בדיקת דופק (עד 10 שניות)**
                - תינוקות:  ברכיאלי או פמורלי
                - ילדים:  קרוטידי
                
                **4. החייאה בסיסית**
                - יחס לחיצות: הנשמות = 30:2 (מטפל יחיד)
                - יחס לחיצות: הנשמות = 15:2 (2 מטפלים)
                - קצב:  100-120 לחיצות לדקה
                - עומק: 1/3 מעומק בית החזה (4 ס"מ בתינוק, 5 ס"מ בילד)
                """)
            
            with st.expander("💊 תרופות בהחייאה"):
                st.markdown("""
                ### תרופות עיקריות:
                
                **אפינפרין (אדרנלין)**
                - מינון: 0.01 מ"ג/ק"ג IV/IO
                - ריכוז: 1: 10,000 (0.1 מ"ג/מ"ל)
                - נפח: 0.1 מ"ל/ק"ג
                - מתן כל 3-5 דקות
                
                **אמיודרון**
                - מינון ראשון: 5 מ"ג/ק"ג בולוס
                - מינון חוזר: 5 מ"ג/ק"ג (עד 3 מנות)
                - מקסימום: 15 מ"ג/ק"ג
                
                **סידן כלוריד 10%**
                - מינון:  20 מ"ג/ק"ג (0.2 מ"ל/ק"ג)
                - אינדיקציות: היפרקלמיה, היפוקלצמיה, מנת יתר של חוסמי סידן
                """)
    
    with tab3:
        st.title("📝 מבחנים ותרגול")
        
        quiz_type = st.selectbox("בחר סוג מבחן:", [
            "",
            "מבחן קצר (10 שאלות)",
            "מבחן מלא (25 שאלות)",
            "תרגול לפי נושא"
        ])
        
        if quiz_type == "מבחן קצר (10 שאלות)":
            if st.button("התחל מבחן", type="primary"):
                st. session_state.quiz_active = True
                st.info("המבחן יתחיל בקרוב...")
    
    with tab4:
        st.title("📊 הסטטיסטיקות שלי")
        st.info("כאן יופיעו הסטטיסטיקות האישיות שלך")
    
    with tab5:
        st.title("🏆 לוח תוצאות - תחרות בין מוסדית")
        
        # דוגמה לטבלת דירוג
        leaderboard_data = pd.DataFrame({
            "דירוג": [1, 2, 3, 4, 5],
            "מוסד": [
                "הדסה עין כרם",
                "מרכז שניידר",
                "רמב״ם",
                "סורוקה",
                "שיבא"
            ],
            "ציון ממוצע": [92, 88, 85, 82, 80],
            "משתתפים": [15, 12, 18, 10, 14]
        })
        
        st.dataframe(leaderboard_data, hide_index=True)

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
