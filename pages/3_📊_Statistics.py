import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="הסטטיסטיקות שלי", page_icon="📊", layout="wide")

# CSS לעברית
st.markdown("""
<style>
    /* יישור גלובלי */
    * {
        direction: rtl !important;
        text-align: right !important;
    }
    
    .stApp, .main {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* תיקון טאבים */
    .stTabs [data-baseweb="tab-list"] {
        direction: rtl !important;
        flex-direction: row-reverse !important;
    }
    
    /* כותרת */
    .stat-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* metrics */
    [data-testid="metric-container"] {
        text-align: center !important;
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# בדיקת התחברות
if not st.session_state.get('logged_in', False):
    st.error("יש להתחבר כדי לראות את הסטטיסטיקות שלך ❌")
    if st.button("חזור לדף הראשי 🏠"):
        st.switch_page("app.py")
    st.stop()

user = st.session_state.get('user', {})

# כותרת
st.markdown("""
<div class="stat-header">
    <h1>הסטטיסטיקות שלי 📊</h1>
    <p>מעקב אחר ההתקדמות האישית שלך</p>
</div>
""", unsafe_allow_html=True)

# טאבים - אימוג'י בסוף! 
tab1, tab2, tab3, tab4 = st.tabs([
    "סקירה כללית 📈",
    "היסטוריית מבחנים 📝",
    "התקדמות בלמידה 📚",
    "השוואה לאחרים 🏆"
])

with tab1:
    st.markdown("### נתונים כלליים 📊")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("ימים פעילים", "7", "2+ מאתמול")
    with col2:
        st.metric("שעות למידה", "12.5", "1.5+ השבוע")
    with col3:
        scores = st.session_state.get('user_scores', [])
        st.metric("מבחנים שבוצעו", len(scores))
    with col4:
        avg = sum(scores) / len(scores) if scores else 0
        st.metric("ציון ממוצע", f"{avg:.1f}%")
    
    st.divider()
    
    # גרף התקדמות
    st.markdown("### התקדמות לאורך זמן 📈")
    
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    data = pd.DataFrame({
        'תאריך': dates,
        'ציון': [random.randint(70, 100) for _ in range(30)]
    })
    
    fig = px.line(data, x='תאריך', y='ציון', 
                  title='הציונים שלך ב-30 הימים האחרונים',
                  markers=True)
    fig.update_layout(
        xaxis_title="תאריך",
        yaxis_title="ציון (%)",
        hovermode='x unified',
        font=dict(size=14)
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("### היסטוריית המבחנים שלך 📝")
    
    if st.session_state.get('user_scores'):
        scores = st.session_state.user_scores
        history = []
        for i, score in enumerate(scores, 1):
            history.append({
                'מבחן': f"מבחן {i}",
                'נושא': 'החייאה',
                'ציון': f"{score}%",
                'תאריך': (datetime.now() - timedelta(days=i)).strftime('%d/%m/%Y'),
                'משך': f"{random.randint(5, 20)} דקות"
            })
        
        df = pd.DataFrame(history)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # סטטיסטיקות
        col1, col2, col3 = st.columns(3)
        avg = sum(scores) / len(scores)
        with col1:
            best = max(scores)
            st.success(f"הציון הטוב ביותר: {best}% 🌟")
        with col2:
            st.info(f"ממוצע ציונים: {avg:.1f}% 📊")
        with col3:
            st.warning(f"צריך שיפור: {100-avg:.0f}% 📈")
    else:
        st.info("עדיין לא ביצעת מבחנים 📝")
        if st.button("התחל מבחן ראשון 🚀", type="primary"):
            st.switch_page("pages/2_📝_Quizzes.py")

with tab3:
    st.markdown("### ההתקדמות שלך בנושאי הלמידה 📚")
    
    topics = [
        {"נושא": "החייאה - BLS & PALS", "התקדמות": 75, "שעות": 3. 5},
        {"נושא": "הנשמה מכנית", "התקדמות": 50, "שעות": 2.0},
        {"נושא":  "תרופות בטיפול נמרץ", "התקדמות": 30, "שעות": 1.5},
        {"נושא": "נוזלים ואלקטרוליטים", "התקדמות": 60, "שעות": 2.5},
        {"נושא": "זיהומים ואנטיביוטיקה", "התקדמות": 40, "שעות": 2.0}
    ]
    
    for topic in topics:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown(f"**{topic['נושא']}**")
            st.progress(topic['התקדמות'] / 100)
        with col2:
            st.metric("", f"{topic['התקדמות']}%", label_visibility="collapsed")
        with col3:
            st.metric("", f"{topic['שעות']}h", label_visibility="collapsed")
    
    st.divider()
    st.markdown("### המלצות אישיות 💡")
    st.success("כל הכבוד!  אתה מתקדם יפה בנושא 'החייאה' 🎉")
    st.info("כדאי להתמקד בנושא 'תרופות בטיפול נמרץ' 💊")
    st.warning("נסה להקדיש לפחות 30 דקות ביום ללמידה ⏰")

with tab4:
    st.markdown("### איך אתה מסתדר לעומת אחרים?  🏆")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### הדירוג שלך במוסד 🏥")
        
        ranking_data = pd.DataFrame({
            'שם': ['אתה 🎯', 'משתמש א', 'משתמש ב', 'משתמש ג'],
            'ציון': [85, 92, 88, 82]
        })
        
        fig = px.bar(ranking_data, x='ציון', y='שם',
                    orientation='h',
                    color='ציון',
                    color_continuous_scale='Blues')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### הדירוג הארצי שלך 🇮🇱")
        st.metric("מקום", "127 מתוך 543")
        st.metric("אחוזון", "76%", "5%+ מהשבוע שעבר")
        st.progress(0.76)
        st.success("אתה בין ה-25% הטובים ביותר!  🌟")

# כפתור חזרה
st.divider()
if st.button("חזרה לעמוד הראשי 🏠", use_container_width=True):
    st.switch_page("app.py")
