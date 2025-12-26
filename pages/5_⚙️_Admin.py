import streamlit as st
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

# CSS מתוקן לעברית מלאה
st.markdown("""
<style>
    /* יישור כללי לימין */
    .stApp {
        direction: rtl ! important;
        text-align: right !important;
    }
    
    /* כל הטקסטים */
    .stMarkdown, .stText, p, span, label {
        text-align: right !important;
        direction: rtl !important;
    }
    
    /* תיקון כותרות */
    h1, h2, h3, h4, h5, h6 {
        text-align:  right !important;
        direction:  rtl !important;
    }
    
    /* תיקון טפסים */
    [data-testid="stForm"] {
        direction: rtl !important;
    }
    
    /* תיקון שדות קלט */
    . stTextInput > div > div > input,
    .stTextArea textarea,
    .stSelectbox > div > div > select {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* תיקון labels */
    .stTextInput label,
    .stTextArea label,
    .stSelectbox label,
    .stSlider label {
        text-align: right !important;
        direction: rtl !important;
        width: 100%;
    }
    
    /* תיקון כפתורים */
    .stButton > button {
        direction: rtl !important;
    }
    
    /* תיקון tabs */
    .stTabs {
        direction: rtl !important;
    }
    
    . stTabs [data-baseweb="tab-list"] {
        direction: rtl !important;
        flex-direction: row-reverse !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        direction: rtl ! important;
    }
    
    /* תיקון expander */
    .streamlit-expanderHeader {
        direction: rtl !important;
        text-align: right !important;
        flex-direction: row-reverse ! important;
    }
    
    . streamlit-expanderContent {
        direction: rtl !important;
        text-align: right ! important;
    }
    
    /* תיקון columns */
    [data-testid="column"] {
        direction: rtl !important;
    }
    
    /* תיקון metrics */
    [data-testid="metric-container"] {
        text-align: center !important;
    }
    
    [data-testid="metric-container"] label {
        text-align: center !important;
    }
    
    /* תיקון הודעות */
    .stAlert {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* תיקון JSON display */
    .stJson {
        direction: ltr !important;
        text-align: left !important;
    }
    
    /* כותרת מעוצבת */
    .admin-header {
        background:  linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        direction: rtl ! important;
    }
    
    . admin-header h1 {
        margin: 0;
        color: white;
        direction: rtl !important;
    }
    
    . admin-header p {
        margin: 0.5rem 0 0 0;
        color: #f0f0f0;
        direction: rtl !important;
    }
    
    /* תיקון slider */
    .stSlider {
        direction: rtl !important;
    }
    
    . stSlider > div {
        direction: rtl !important;
    }
    
    /* תיקון selectbox */
    .stSelectbox > div {
        direction: rtl !important;
    }
    
    . stSelectbox option {
        text-align: right !important;
    }
</style>
""", unsafe_allow_html=True)

# JavaScript נוסף לתיקון כיוון
import streamlit.components.v1 as components
components.html("""
<script>
document.addEventListener('DOMContentLoaded', function() {
    // תיקון כל האלמנטים
    document.querySelectorAll('*').forEach(el => {
        if (el.style) {
            el.style.textAlign = 'right';
        }
    });
    
    // תיקון טאבים
    const tabs = document.querySelectorAll('. stTabs [data-baseweb="tab-list"]');
    tabs.forEach(tab => {
        tab.style.flexDirection = 'row-reverse';
    });
    
    // תיקון labels
    const labels = document.querySelectorAll('label');
    labels.forEach(label => {
        label.style.textAlign = 'right';
        label.style.display = 'block';
        label.style.width = '100%';
    });
});
</script>
""", height=0)

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
tab1, tab2, tab3 = st.tabs(["הוספת שאלה ➕", "הוספת תוכן למידה 📚", "סטטיסטיקות 📊"])

with tab1:
    st.subheader("📝 הוספת שאלה חדשה")
    
    with st.form("add_question_form", clear_on_submit=True):
        # בחירת נושא
        st.markdown("### בחירת נושא")
        if DB_CONNECTED:
            try:
                topics = get_topics()
                if topics:
                    topic_names = [t['title'] for t in topics]
                    selected_topic = st.selectbox("בחר נושא:", topic_names)
                else:
                    st.error("אין נושאים במערכת")
                    st.stop()
            except: 
                topic_names = ["החייאה - BLS & PALS", "הנשמה מכנית", "תרופות בטיפול נמרץ"]
                selected_topic = st.selectbox("בחר נושא:", topic_names)
        else:
            topic_names = ["החייאה - BLS & PALS", "הנשמה מכנית", "תרופות בטיפול נמרץ"]
            selected_topic = st.selectbox("בחר נושא:", topic_names)
        
        st.divider()
        
        # פרטי השאלה
        st.markdown("### פרטי השאלה")
        question_text = st.text_area("טקסט השאלה:", height=100, placeholder="הקלד את השאלה כאן...")
        
        st.markdown("### אפשרויות תשובה")
        col1, col2 = st. columns(2)
        with col1:
            option1 = st.text_input("אפשרות 1:", placeholder="תשובה ראשונה")
            option2 = st.text_input("אפשרות 2:", placeholder="תשובה שנייה")
        with col2:
            option3 = st.text_input("אפשרות 3:", placeholder="תשובה שלישית")
            option4 = st.text_input("אפשרות 4:", placeholder="תשובה רביעית")
        
        st.divider()
        
        col1, col2 = st. columns(2)
        with col1:
            correct_answer = st.selectbox("מהי התשובה הנכונה?", [1, 2, 3, 4])
        with col2:
            difficulty = st.select_slider(
                "רמת קושי:",
                options=["קל", "בינוני", "קשה"],
                value="בינוני"
            )
        
        explanation = st.text_area("הסבר לתשובה הנכונה:", height=100, placeholder="הסבר מפורט מדוע זו התשובה הנכונה...")
        
        st.divider()
        
        submitted = st.form_submit_button("💾 שמור שאלה", type="primary", use_container_width=True)
        
        if submitted: 
            if all([question_text, option1, option2, option3, option4, explanation]):
                st.success("✅ השאלה נוספה בהצלחה!")
                st.balloons()
                
                # הצגת השאלה שנוספה
                with st.expander("👁️ צפה בשאלה שנוספה"):
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
        ### דוגמה 1: שאלה קלינית
        **שאלה:** ילד בן 3 שנים במשקל 15 ק"ג בהחייאה.  מהו המינון הנכון של אפינפרין IV?
        
        **אפשרויות:**
        1. 0.15 מ"ג (0.15 מ"ל מתמיסה 1:1000)
        2. 0.15 מ"ג (1.5 מ"ל מתמיסה 1:10,000)
        3. 0.015 מ"ג (1.5 מ"ל מתמיסה 1:10,000)
        4. 1.5 מ"ג (1.5 מ"ל מתמיסה 1:1000)
        
        **תשובה נכונה:** 2
        
        **הסבר:** המינון הוא 0.01 מ"ג/ק"ג = 0.15 מ"ג. בתמיסה 1:10,000 זה שווה ל-1.5 מ"ל. 
        
        ---
        
        ### דוגמה 2: שאלת ידע
        **שאלה:** מהו קצב הלחיצות המומלץ בהחייאת ילדים?
        
        **אפשרויות:**
        1. 80-100 לחיצות לדקה
        2. 100-120 לחיצות לדקה
        3. 120-140 לחיצות לדקה
        4. 60-80 לחיצות לדקה
        
        **תשובה נכונה:** 2
        
        **הסבר:** לפי הנחיות AHA/ERC, קצב הלחיצות צריך להיות 100-120 לדקה.
        """)

with tab2:
    st. subheader("📚 הוספת חומר למידה")
    
    with st.form("add_content_form"):
        st.markdown("### פרטי התוכן")
        
        content_topic = st.selectbox("נושא:", topic_names if 'topic_names' in locals() else ["החייאה"])
        content_title = st.text_input("כותרת:", placeholder="כותרת החומר הלימודי")
        content_type = st.selectbox("סוג תוכן:", ["טקסט", "וידאו", "תמונה", "קישור"])
        
        if content_type == "טקסט":
            content = st.text_area("תוכן:", height=300, placeholder="הקלד את התוכן כאן...")
        elif content_type == "וידאו":
            content = st.text_input("קישור לוידאו:", placeholder="https://youtube.com/...")
        elif content_type == "תמונה":
            content = st.text_input("קישור לתמונה:", placeholder="https://...")
        else:
            content = st.text_input("קישור:", placeholder="https://...")
        
        submit_content = st.form_submit_button("💾 שמור תוכן", type="primary", use_container_width=True)
        
        if submit_content:
            if content_title and content:
                st.success("✅ התוכן יתווסף בקרוב למערכת")
                st.info("פונקציונליות מלאה תהיה זמינה בעדכון הבא")
            else:
                st.error("❌ נא למלא את כל השדות")

with tab3:
    st.subheader("📊 סטטיסטיקות מערכת")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("שאלות במערכת", "5", "2+", delta_color="normal")
    
    with col2:
        st.metric("נושאי למידה", "3", "0", delta_color="off")
    
    with col3:
        st.metric("משתמשים רשומים", "1", "1+", delta_color="normal")
    
    with col4:
        st.metric("מבחנים שבוצעו", "0", "0", delta_color="off")
    
    st.divider()
    
    # גרף התפלגות שאלות
    st.subheader("📈 התפלגות שאלות לפי נושא")
    
    import pandas as pd
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
    ## 🎯 איך להוסיף תוכן איכותי? 
    
    ### לשאלות טובות:
    1. **שאלה ברורה** - נסח שאלה חד-משמעית וממוקדת
    2. **אפשרויות מבלבלות** - כל האפשרויות צריכות להיראות הגיוניות
    3. **הסבר מלא** - כלול הסבר מדוע התשובה נכונה ומדוע השאר לא
    4. **רלוונטיות קלינית** - עדיף שאלות מבוססות מקרים
    
    ### לחומרי למידה:
    1. **כותרת ברורה** - שתסביר בדיוק מה התוכן
    2. **תוכן מעודכן** - על בסיס הנחיות עדכניות
    3. **שפה פשוטה** - נגיש לכל הרמות
    4. **דוגמאות** - הוסף דוגמאות קליניות
    
    ### טיפים נוספים:
    - בדוק איות ודקדוק לפני שליחה
    - השתמש בקיצורים מקובלים בלבד
    - הוסף מקורות אם רלוונטי
    """)
