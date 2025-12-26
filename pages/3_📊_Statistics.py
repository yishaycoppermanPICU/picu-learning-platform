import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="הסטטיסטיקות שלי", page_icon="📊", layout="wide")

# CSS לעברית
st.markdown("""
<style>
    .stApp {
        direction: rtl ! important;
        text-align: right !important;
    }
    
    .stat-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius:  10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    [data-testid="metric-container"] {
        text-align: center ! important;
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# בדיקת התחברות
if not st.session_state.get('logged_in', False):
    st.error("יש להתחבר כדי לראות את הסטטיסטיקות שלך")
    st.stop()

user = st.session_state.get('user', {})

st.markdown("""
<div class="stat-header">
    <h1>הסטטיסטיקות שלי 📊</h1>
    <p>מעקב אחר ההתקדמות שלך</p>
</div>
""", unsafe_allow_html=True)

# טאבים
tab1, tab2, tab3, tab4 = st.tabs(["סקירה כללית 📈", "מבחנים 📝", "למידה 📚", "השוואה 🏆"])

with tab1:
    st.subheader("סקירה כללית")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("ימים פעילים", "7", "2+")
    with col2:
        st.metric("זמן למידה כולל", "12. 5 שעות", "1.5+")
    with col3:
        st.metric("מבחנים שהושלמו", len(st.session_state.get('user_scores', [])))
    with col4:
        scores = st.session_state.get('user_scores', [])
        avg_score = sum(scores) / len(scores) if scores else 0
        st.metric("ציון ממוצע", f"{avg_score:.1f}%")
    
    st.divider()
    
    # גרף התקדמות
    st.subheader("התקדמות לאורך זמן 📈")
    
    # נתונים לדוגמה
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    progress_data = pd.DataFrame({
        'תאריך': dates,
        'ציון': [random.randint(70, 100) for _ in range(30)],
        'זמן למידה (דקות)': [random.randint(10, 60) for _ in range(30)]
    })
    
    fig = px.line(progress_data, x='תאריך', y='ציון', 
                  title='ציונים במבחנים',
                  markers=True)
    fig.update_layout(
        xaxis_title="תאריך",
        yaxis_title="ציון (%)",
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("היסטוריית מבחנים 📝")
    
    if st.session_state.get('user_scores'):
        # יצירת טבלה עם היסטוריית מבחנים
        quiz_history = []
        for i, score in enumerate(st.session_state.user_scores, 1):
            quiz_history.append({
                'מבחן מס׳': i,
                'נושא': 'החייאה - BLS & PALS',
                'ציון':  f"{score}%",
                'תאריך': (datetime.now() - timedelta(days=i)).strftime('%d/%m/%Y'),
                'משך זמן': f"{random.randint(5, 20)} דקות"
            })
        
        df = pd.DataFrame(quiz_history)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("עדיין לא ביצעת מבחנים")
    
    # כפתור למבחן חדש
    if st.button("התחל מבחן חדש 🚀", type="primary"):
        st.switch_page("pages/2_📝_Quizzes.py")

with tab3:
    st.subheader("התקדמות בלמידה 📚")
    
    # נושאי למידה
    topics_progress = [
        {"נושא": "החייאה - BLS & PALS", "התקדמות": 75, "שעות": 3. 5},
        {"נושא":  "הנשמה מכנית", "התקדמות": 50, "שעות": 2.0},
        {"נושא":  "תרופות בטיפול נמרץ", "התקדמות": 30, "שעות": 1.5},
        {"נושא": "נוזלים ואלקטרוליטים", "התקדמות": 60, "שעות": 2.5},
        {"נושא": "זיהומים ואנטיביוטיקה", "התקדמות": 40, "שעות": 2.0},
    ]
    
    for topic in topics_progress:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown(f"**{topic['נושא']}**")
            st.progress(topic['התקדמות'] / 100)
        with col2:
            st.metric("התקדמות", f"{topic['התקדמות']}%", label_visibility="collapsed")
        with col3:
            st.metric("שעות", topic['שעות'], label_visibility="collapsed")
    
    st.divider()
    
    # המלצות ללמידה
    st.subheader("המלצות ללמידה 💡")
    st.info("""
    • המשך עם נושא 'החייאה' - אתה כמעט מסיים! 
    • כדאי להתחיל לתרגל 'תרופות בטיפול נמרץ'
    • נסה להקדיש לפחות 30 דקות ביום ללמידה
    """)

with tab4:
    st.subheader("השוואה למשתמשים אחרים 🏆")
    
    col1, col2 = st. columns(2)
    
    with col1:
        st. markdown("### הדירוג שלך במוסד")
        
        # דירוג במוסד
        institution_ranking = pd.DataFrame({
            'משתמש': ['אתה', 'משתמש א', 'משתמש ב', 'משתמש ג', 'משתמש ד'],
            'ציון ממוצע': [85, 92, 88, 82, 79],
            'מבחנים': [5, 12, 8, 6, 4]
        })
        
        fig = px.bar(institution_ranking, x='משתמש', y='ציון ממוצע',
                    color='ציון ממוצע',
                    color_continuous_scale='Viridis',
                    title='דירוג במוסד שלך')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### השוואה ארצית")
        
        st.metric("הדירוג הארצי שלך", "127 מתוך 543")
        st.metric("אחוזון", "76%", "5%+")
        
        # התפלגות ציונים ארצית
        fig = px.histogram(
            x=[random.gauss(75, 15) for _ in range(500)],
            nbins=30,
            title='התפלגות ציונים ארצית',
            labels={'x': 'ציון', 'y': 'מספר משתמשים'}
        )
        fig.add_vline(x=85, line_dash="dash", line_color="red", 
                     annotation_text="הציון שלך")
        st.plotly_chart(fig, use_container_width=True)

# כפתור חזרה
st.divider()
if st.button("חזרה לעמוד הראשי 🏠", use_container_width=True):
    st.switch_page("app.py")
