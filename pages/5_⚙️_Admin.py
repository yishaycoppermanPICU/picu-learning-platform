import streamlit as st
import json
from utils.database import (
    get_topics,
    add_question,
    init_supabase,
    DB_CONNECTED
)

st.set_page_config(page_title="ניהול תוכן", page_icon="⚙️", layout="wide")

# CSS
st.markdown("""
<style>
    .stApp {
        direction: rtl;
    }
    .admin-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
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
    st.error("יש להתחבר למערכת כדי לגשת לדף זה")
    st.stop()

# בדיקת חיבור למסד נתונים
if not DB_CONNECTED:
    st.warning("מסד הנתונים אינו מחובר - פועל במצב דמו")

# תפריט
tab1, tab2, tab3 = st.tabs(["➕ הוספת שאלה", "📚 הוספת תוכן למידה", "📊 סטטיסטיקות"])

with tab1:
    st.subheader("הוספת שאלה חדשה")
    
    with st.form("add_question_form"):
        # בחירת נושא
        if DB_CONNECTED:
            topics = get_topics()
            if topics:
                topic_names = [t['title'] for t in topics]
                selected_topic = st.selectbox("נושא", topic_names)
                topic_id = next((t['id'] for t in topics if t['title'] == selected_topic), None)
            else:
                st.error("אין נושאים במערכת")
                st.stop()
        else:
            topic_names = ["החייאה", "הנשמה", "תרופות"]
            selected_topic = st. selectbox("נושא", topic_names)
            topic_id = "demo"
        
        # פרטי השאלה
        question_text = st.text_area("טקסט השאלה", height=100)
        
        st.write("אפשרויות תשובה:")
        col1, col2 = st.columns(2)
        with col1:
            option1 = st.text_input("אפשרות 1")
            option2 = st.text_input("אפשרות 2")
        with col2:
            option3 = st. text_input("אפשרות 3")
            option4 = st.text_input("אפשרות 4")
        
        correct_answer = st.selectbox("תשובה נכונה", [1, 2, 3, 4])
        
        explanation = st.text_area("הסבר לתשובה", height=100)
        
        difficulty = st.select_slider("רמת קושי", options=["easy", "medium", "hard"], value="medium")
        
        submitted = st.form_submit_button("הוסף שאלה", type="primary")
        
        if submitted:
            if all([question_text, option1, option2, option3, option4, explanation]):
                options = [option1, option2, option3, option4]
                
                if DB_CONNECTED:
                    result = add_question(
                        topic_id=topic_id,
                        question_text=question_text,
                        options=options,
                        correct_answer=correct_answer - 1,  # Convert to 0-based index
                        explanation=explanation,
                        difficulty=difficulty
                    )
                    if result: 
                        st.success("✅ השאלה נוספה בהצלחה!")
                        st.balloons()
                    else:
                        st.error("❌ שגיאה בהוספת השאלה")
                else:
                    st.success("✅ השאלה נוספה בהצלחה!  (Demo Mode)")
                    st.json({
                        "topic":  selected_topic,
                        "question": question_text,
                        "options": options,
                        "correct":  correct_answer,
                        "explanation": explanation,
                        "difficulty": difficulty
                    })
            else:
                st.error("נא למלא את כל השדות")

    # דוגמאות לשאלות
    with st.expander("💡 דוגמאות לשאלות טובות"):
        st.markdown("""
        ### שאלה טובה:
        **שאלה:** מהו המינון המומלץ של אפינפרין IV בהחייאת ילדים?
        
        **אפשרויות:**
        1. 0.01 מ"ג/ק"ג
        2. 0.1 מ"ג/ק"ג  
        3. 1 מ"ג/ק"ג
        4. 0.001 מ"ג/ק"ג
        
        **תשובה נכונה:** 1
        
        **הסבר:** המינון המומלץ הוא 0.01 מ"ג/ק"ג (0.1 מ"ל/ק"ג מתמיסה 1: 10,000) IV/IO כל 3-5 דקות בזמן החייאה.
        """)

with tab2:
    st. subheader("הוספת חומר למידה")
    
    with st.form("add_content_form"):
        content_topic = st.selectbox("נושא", topic_names if 'topic_names' in locals() else ["החייאה"])
        content_title = st.text_input("כותרת")
        content_type = st.selectbox("סוג תוכן", ["טקסט", "וידאו", "תמונה"])
        
        if content_type == "טקסט":
            content = st.text_area("תוכן", height=300)
        elif content_type == "וידאו":
            content = st.text_input("קישור לוידאו (YouTube)")
        else:
            content = st.text_input("קישור לתמונה")
        
        submit_content = st.form_submit_button("הוסף תוכן")
        
        if submit_content:
            st.info("פונקציונליות זו תהיה זמינה בקרוב")

with tab3:
    st.subheader("📊 סטטיסטיקות תוכן")
    
    if DB_CONNECTED:
        try:
            supabase = init_supabase()
            
            # ספירת שאלות
            questions_count = supabase.table('questions').select("id", count='exact').execute()
            
            # ספירת נושאים
            topics_count = supabase.table('topics').select("id", count='exact').execute()
            
            # ספירת משתמשים
            users_count = supabase.table('users').select("id", count='exact').execute()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("שאלות במערכת", len(questions_count.data) if questions_count.data else 0)
            with col2:
                st.metric("נושאים", len(topics_count.data) if topics_count.data else 0)
            with col3:
                st.metric("משתמשים רשומים", len(users_count.data) if users_count.data else 0)
        except: 
            st.info("אין נתונים זמינים")
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("שאלות במערכת", "0")
        with col2:
            st.metric("נושאים", "3")
        with col3:
            st.metric("משתמשים רשומים", "0")

# הוראות שימוש
st. divider()
with st.expander("📖 הוראות שימוש"):
    st.markdown("""
    ### איך להוסיף שאלה טובה? 
    
    1. **שאלה ברורה** - נסח שאלה חד-משמעית
    2. **אפשרויות הגיוניות** - כל האפשרויות צריכות להיות סבירות
    3. **הסבר מפורט** - הסבר למה התשובה נכונה
    4. **רמת קושי מתאימה** - התאם את הקושי לקהל היעד
    
    ### טיפים: 
    - השתמש בשאלות מבוססות מקרה קליני
    - הוסף ערכים מספריים ספציפיים
    - התבסס על הנחיות עדכניות
    """)
