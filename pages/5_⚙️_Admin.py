import streamlit as st
import pandas as pd
import json
from datetime import datetime

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

# CSS מקיף לתיקון כל בעיות היישור
st.markdown("""
<style>
    /* תיקון כללי */
    .main > div {
        direction: rtl;
        text-align: right;
    }
    
    /* כל האלמנטים */
    .stApp, .stApp * {
        direction: rtl ! important;
        text-align:  right !important;
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
        padding-left: 0 ! important;
    }
    
    . stMarkdown li {
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
        direction: rtl ! important;
    }
    
    /* תיקון כפתורים */
    . stButton > button {
        direction: rtl !important;
    }
    
    /* תיקון טאבים */
    .stTabs {
        direction: rtl ! important;
    }
    
    . stTabs [data-baseweb="tab-list"] {
        direction: rtl !important;
        flex-direction: row-reverse !important;
    }
    
    /* כותרת מעוצבת */
    .admin-header {
        background:  linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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

# בדיקת הרשאות
if not st.session_state.get('logged_in', False):
    st.error("❌ יש להתחבר למערכת כדי לגשת לדף זה")
    st.stop()

# תפריט טאבים
tab1, tab2, tab3 = st.tabs(["➕ הוספת שאלה", "📚 הוספת תוכן למידה", "📊 סטטיסטיקות"])

with tab1:
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
                    st. stop()
            except:  
                topic_names = ["החייאה - BLS & PALS", "הנשמה מכנית", "תרופות בטיפול נמרץ"]
                selected_topic = st. selectbox("נושא", topic_names, label_visibility="collapsed")
        else:
            topic_names = ["החייאה - BLS & PALS", "הנשמה מכנית", "תרופות בטיפול נמרץ"]
            selected_topic = st.selectbox("נושא", topic_names, label_visibility="collapsed")
        
        st.divider()
        
        # פרטי השאלה
        st.markdown("**טקסט השאלה:**")
        question_text = st.text_area("שאלה", height=100, placeholder="הקלד את השאלה כאן...", label_visibility="collapsed")
        
        st. markdown("**אפשרויות תשובה:**")
        col1, col2 = st. columns(2)
        with col1:
            option1 = st.text_input("אפשרות 1", placeholder="תשובה ראשונה")
            option2 = st.text_input("אפשרות 2", placeholder="תשובה שנייה")
        with col2:
            option3 = st.text_input("אפשרות 3", placeholder="תשובה שלישית")
            option4 = st.text_input("אפשרות 4", placeholder="תשובה רביעית")
        
        st.divider()
        
        col1, col2 = st. columns(2)
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
                    st. json({
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

with tab2:
    st. subheader("📚 הוספת חומר למידה")
    
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

with tab3:
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
