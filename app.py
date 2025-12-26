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

# CSS חזק ומקיף - תיקון אמיתי
st.markdown("""
<style>
    /* יישור גלובלי לימין - חזק */
    * {
        direction: rtl ! important;
        text-align:  right !important;
    }
    
    /* תיקון כל הקונטיינרים */
    .main, .block-container, .element-container, .stApp {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* הסרגל הצדדי - העברה לימין */
    section[data-testid="stSidebar"] {
        right: 0 !important;
        left: auto !important;
        direction: rtl !important;
        text-align: right !important;
    }
    
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* תיקון טאבים - מימין לשמאל */
    . stTabs [data-baseweb="tab-list"] {
        direction: rtl !important;
        flex-direction: row-reverse !important;
    }
    
    . stTabs [data-baseweb="tab"] {
        direction: rtl ! important;
    }
    
    /* תיקון כותרות */
    h1, h2, h3, h4, h5, h6 {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* תיקון טקסט */
    p, span, div, label {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* תיקון כפתורים */
    . stButton > button {
        direction: rtl !important;
    }
    
    /* תיקון שדות טקסט */
    . stTextInput > div > div > input {
        direction: rtl !important;
        text-align: right !important;
    }
    
    . stSelectbox label,
    .stTextInput label,
    .stTextArea label {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* תיקון metrics */
    [data-testid="metric-container"] {
        text-align: center !important;
    }
    
    /* כותרת ראשית */
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
        direction: rtl !important;
    }
    
    . main-header h1, .main-header p {
        direction: rtl !important;
    }
</style>
""", unsafe_allow_html=True)

# JavaScript חזק לתיקון נוסף
import streamlit.components.v1 as components
components.html("""
<script>
// המתן לטעינת הדף
setTimeout(function() {
    // הזז סרגל צד לימין בכוח
    const sidebar = document.querySelector('section[data-testid="stSidebar"]');
    if (sidebar) {
        sidebar.style.cssText = 'right: 0 !important; left: auto !important; direction: rtl !important;';
    }
    
    // תקן את כל האלמנטים
    document.querySelectorAll('*').forEach(function(el) {
        if (el.style) {
            el.style. direction = 'rtl';
        }
    });
    
    // תקן טאבים
    const tabList = document.querySelector('[data-baseweb="tab-list"]');
    if (tabList) {
        tabList.style.flexDirection = 'row-reverse';
    }
}, 100);
</script>
""", height=0)

# אתחול session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state. user = None
if 'user_scores' not in st.session_state:
    st.session_state.user_scores = []

# כותרת ראשית - אימוג'י בסוף! 
st.markdown("""
<div class="main-header">
    <h1 style="color: white;">פלטפורמת למידה PICU 🏥</h1>
    <p style="color: #f0f0f0;">פלטפורמת למידה מתקדמת לטיפול נמרץ ילדים</p>
</div>
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
                inst_names = ["שיבא - תל השומר", "איכילוב - תל אביב", "רמב״ם - חיפה"]
            
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
                if full_name and email and institution and agree:
                    username = email.split('@')[0].replace('.', '_')
                    
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
                            st. error(f"שגיאה:  {e}")
                    else:
                        st.session_state.logged_in = True
                        st.session_state.user = {
                            'username': username,
                            'full_name': full_name,
                            'email': email,
                            'institutions': {'name': institution}
                        }
                        st.success(f"ברוך הבא, {full_name} 👋")
                        st.rerun()
                else:
                    st.error("נא למלא את כל השדות ❌")
    
    else:
        # משתמש מחובר
        user = st.session_state.user
        st.success(f"מחובר:  {user. get('full_name', 'משתמש')} ✓")
        
        if 'institutions' in user and user['institutions']:
            st.info(f"מוסד:  {user['institutions']. get('name', '')} 🏥")
        
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
    
    # אודות - אימוג'ים בסוף
    with st.expander("אודות המערכת ℹ"):
        st.markdown("""
        פותח על ידי:  ישי קופרמן 👨‍⚕️
        תפקיד: אח בטיפול נמרץ ילדים
        מייל: yishaycopp@gmail.com 📧
        גרסה: 1.0.0
        עדכון אחרון:  26/12/2024 📅
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
        st.markdown("### ברוכים הבאים לפלטפורמת הלמידה! 🎯")
        
        # כרטיסיות
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="padding: 1. 5rem; border-radius: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-align: center;">
                <h3 style="color: white;">חומרי למידה 📚</h3>
                <p style="color: white;">גישה לחומרי למידה מעודכנים מבוססי UpToDate</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="padding: 1.5rem; border-radius: 10px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; text-align: center;">
                <h3 style="color: white;">תרגול ומבחנים 📝</h3>
                <p style="color: white;">מבחנים אינטראקטיביים עם משוב מיידי</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="padding: 1.5rem; border-radius: 10px; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; text-align: center;">
                <h3 style="color: white;">תחרות בין-מוסדית 🏆</h3>
                <p style="color: white;">השווה את הביצועים שלך מול מוסדות אחרים</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        st.markdown("### הסטטיסטיקות שלך 📈")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("מבחנים שהושלמו", "0")
        with col2:
            st.metric("ציון ממוצע", "—")
        with col3:
            st.metric("זמן למידה", "0 שעות")
        with col4:
            st.metric("דירוג במוסד", "—")
    
    with tab2:
        st.markdown("### חומרי למידה 📚")
        
        if DB_CONNECTED:
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
            st.button("מבחן מותאם אישית ⚙️", disabled=True, use_container_width=True)
    
    with tab4:
        st.markdown("### הסטטיסטיקות שלי 📊")
        
        if st.session_state.user_scores:
            df = pd.DataFrame({
                'מספר מבחן': range(1, len(st.session_state.user_scores) + 1),
                'ציון':  st.session_state.user_scores
            })
            st.line_chart(df.set_index('מספר מבחן'))
        else:
            st.info("עדיין אין נתונים להצגה 📈")
            st.button("התחל את המבחן הראשון שלך 🚀", type="primary")
    
    with tab5:
        st.markdown("### לוח הישגים - תחרות בין-מוסדית 🏆")
        
        if DB_CONNECTED:
            leaderboard = get_leaderboard()
            if leaderboard: 
                df = pd.DataFrame(leaderboard)
                st.dataframe(df, hide_index=True, use_container_width=True)
            else:
                st.info("אין נתונים להצגה עדיין 📊")
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
                'ציון ממוצע': [88. 4, 88.3, 88.1, 86.0, 82.9],
                'משתתפים': [10, 27, 9, 8, 30]
            })
            st.dataframe(demo_data, hide_index=True)

else:
    # משתמש לא מחובר
    st.warning("יש להתחבר כדי לגשת לתוכן 🔐")
    
    with st.expander("מידע על הפלטפורמה ℹ️"):
        st.markdown("""
        ### ברוכים הבאים לפלטפורמת PICU Learning!  🎓
        
        **מטרת הפלטפורמה:**
        פלטפורמה זו נוצרה כדי להעשיר ולחדד את הידע של צוותי טיפול נמרץ ילדים. 
        
        **מה תמצאו כאן:**
        • חומרי למידה מעודכנים על בסיס UpToDate 📚
        • מבחנים אינטראקטיביים עם משוב מיידי 📝
        • מעקב אחר התקדמות אישית 📈
        • תחרות בריאה בין מוסדות רפואיים 🏆
        
        **איך מתחילים:**
        פשוט הירשמו עם המייל שלכם - ללא סיסמה!  ✨
        """)

# כתב ויתור בתחתית
st.divider()
st.caption("הערה: האתר מיועד למטרות למידה בלבד. האחריות לאימות התוכן עם מקורות רפואיים מעודכנים היא על המשתמש ⚠️")
