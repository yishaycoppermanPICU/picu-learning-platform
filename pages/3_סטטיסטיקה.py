import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random
import sys
from pathlib import Path

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils.content_manager import restore_user_session
from utils.styles import get_common_styles
from utils.weekly_content import get_user_weekly_stats, get_current_weekly_content
from utils.quiz_manager import get_user_stats, get_user_quiz_history
from utils.badges import (
    get_badge_html, 
    get_badge_card_html, 
    get_progress_badges_html,
    calculate_user_achievements,
    get_all_badges_showcase
)

st.set_page_config(page_title="הסטטיסטיקות שלי", page_icon="📊", layout="wide")

# Restore user session if available
restore_user_session(st)

# CSS מרכזי
st.markdown(get_common_styles(), unsafe_allow_html=True)

# CSS נוסף ספציפי לדף
st.markdown("""
<style>
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
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "סקירה כללית 📈",
    "תגי הישגים 🏅",
    "היסטוריית מבחנים 📝",
    "התקדמות בלמידה 📚",
    "השוואה לאחרים 🏆"
])

with tab1:
    st.markdown("### נתונים כלליים 📊")
    
    # קבלת נתונים שבועיים ונתוני מבחנים
    user_email = user.get('email', '')
    weekly_stats = get_user_weekly_stats(user_email) if user_email else {}
    quiz_stats = get_user_stats(user_email) if user_email else {}
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("שבועות שהושלמו", weekly_stats.get('completed_weeks', 0))
    with col2:
        st.metric("תגי מצטיין", weekly_stats.get('total_badges', 0))
    with col3:
        st.metric("מבחנים שבוצעו", quiz_stats.get('total_quizzes', 0))
    with col4:
        avg = quiz_stats.get('average_score', 0)
        st.metric("ציון ממוצע", f"{avg:.0f}/100")
    
    st.divider()
    
    # תוכן שבועי נוכחי
    weekly_content = get_current_weekly_content()
    is_completed = weekly_stats.get('current_week_completed', False)
    
    completion_status = "✅ הושלם השבוע" if is_completed else "⏳ ממתין להשלמה"
    status_color = "#28a745" if is_completed else "#ffc107"
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-right: 5px solid {status_color};
    ">
        <h3 style="margin: 0 0 1rem 0;">📅 תוכן השבוע הנוכחי</h3>
        <div style="display: flex; align-items: center; gap: 1rem;">
            <span style="font-size: 3rem;">{weekly_content['icon']}</span>
            <div>
                <h4 style="margin: 0;">{weekly_content['title']}</h4>
                <p style="color: #6c757d; margin: 0.3rem 0;">{weekly_content['description']}</p>
                <span style="
                    background: {status_color};
                    color: white;
                    padding: 0.3rem 0.8rem;
                    border-radius: 15px;
                    font-size: 0.85rem;
                    font-weight: 600;
                ">{completion_status}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
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
    st.markdown("### תגי ההישגים שלך 🏅")
    
    user_email = user.get('email', '')
    if user_email:
        weekly_stats = get_user_weekly_stats(user_email)
        badges_list = weekly_stats.get('badges', [])
        
        if badges_list:
            st.success(f"🎉 יש לך {len(badges_list)} תגים!")
            
            # הצגת התגים
            st.markdown("#### התגים שצברת")
            
            for badge in sorted(badges_list, key=lambda x: x.get('date', ''), reverse=True):
                badge_date = datetime.fromisoformat(badge['date']).strftime('%d/%m/%Y %H:%M')
                st.markdown(
                    get_badge_card_html(
                        'excellence',
                        earned_date=badge_date,
                        score=badge.get('score')
                    ),
                    unsafe_allow_html=True
                )
            
            st.divider()
            
            # התקדמות לתגים נוספים
            st.markdown("#### התקדמות לתגים נוספים")
            st.markdown(get_progress_badges_html(
                weekly_stats['completed_weeks'],
                weekly_stats['total_badges']
            ), unsafe_allow_html=True)
            
            # הישגים זמינים
            achievements = calculate_user_achievements(weekly_stats, badges_list)
            if achievements:
                st.markdown("#### הישגים שזכית להם")
                for achievement in achievements:
                    st.markdown(get_badge_html(achievement, 'medium'), unsafe_allow_html=True)
        else:
            st.info("עדיין לא צברת תגים. השלם את המשימה השבועית כדי לקבל את התג הראשון!")
            
            st.markdown("#### תגים זמינים")
            st.markdown(get_all_badges_showcase(), unsafe_allow_html=True)
    else:
        st.warning("לא ניתן לטעון תגים - אין מידע על משתמש")

with tab3:
    st.markdown("### היסטוריית המבחנים שלך 📝")
    
    # קבלת היסטוריה אמיתית
    quiz_history = get_user_quiz_history(user_email) if user_email else []
    
    if quiz_history:
        # הצגת טבלה
        history_data = []
        for quiz in quiz_history:
            history_data.append({
                'תאריך': datetime.fromisoformat(quiz['timestamp']).strftime('%d/%m/%Y %H:%M'),
                'קטגוריה': quiz.get('category', 'כללי'),
                'רמת קושי': quiz.get('difficulty', 'כללי'),
                'שאלות': f"{quiz['correct_answers']}/{quiz['total_questions']}",
                'ציון': f"{quiz['score_percentage']:.0f}/100",
                'זמן': f"{quiz['time_taken']//60}:{quiz['time_taken']%60:02d}"
            })
        
        df = pd.DataFrame(history_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # סטטיסטיקות
        col1, col2, col3 = st.columns(3)
        with col1:
            best = quiz_stats.get('best_score', 0)
            st.success(f"הציון הטוב ביותר: {best:.0f}/100 🌟")
        with col2:
            avg = quiz_stats.get('average_score', 0)
            st.info(f"ממוצע ציונים: {avg:.0f}/100 📊")
        with col3:
            total = quiz_stats.get('total_questions', 0)
            correct = quiz_stats.get('total_correct', 0)
            st.metric("סה\"כ תשובות נכונות", f"{correct}/{total}")
    else:
        st.info("עדיין לא ביצעת מבחנים 📝")
        if st.button("התחל מבחן ראשון 🚀", type="primary"):
            st.switch_page("pages/5_בחנים.py")

with tab4:
    st.markdown("### ההתקדמות שלך בנושאי הלמידה 📚")
    
    topics = [
        {"נושא": "החייאה - BLS & PALS", "התקדמות": 75, "שעות": 3.5},
        {"נושא": "הנשמה מכנית", "התקדמות": 50, "שעות": 2.0},
        {"נושא": "תרופות בטיפול נמרץ", "התקדמות": 30, "שעות": 1.5},
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
    st.success("כל הכבוד! אתה מתקדם יפה בנושא 'החייאה' 🎉")
    st.info("כדאי להתמקד בנושא 'תרופות בטיפול נמרץ' 💊")
    st.warning("נסה להקדיש לפחות 30 דקות ביום ללמידה ⏰")

with tab5:
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
