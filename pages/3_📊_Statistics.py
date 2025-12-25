import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="סטטיסטיקות", page_icon="📊", layout="wide")

# CSS
st.markdown("""
<style>
    .stApp {
        direction: rtl;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 הסטטיסטיקות שלי")
st.markdown("---")

# בדיקת התחברות
if not st.session_state.get('logged_in', False):
    st.warning("יש להתחבר כדי לראות סטטיסטיקות")
    st.stop()

# נתונים לדוגמה - במציאות יגיעו ממסד נתונים
if 'user_scores' not in st.session_state or len(st.session_state.user_scores) == 0:
    # יצירת נתונים לדוגמה
    st.session_state.user_scores = []
    for i in range(15):
        date = datetime.now() - timedelta(days=random.randint(1, 30))
        st.session_state.user_scores.append({
            'date':  date.strftime("%Y-%m-%d"),
            'score': random.randint(60, 100),
            'questions': random.choice([5, 10, 20]),
            'correct': 0,
            'topic': random.choice(['החייאה', 'הנשמה', 'תרופות', 'כללי'])
        })
    for score in st.session_state.user_scores:
        score['correct'] = int(score['questions'] * score['score'] / 100)

# המרה ל-DataFrame
df = pd. DataFrame(st.session_state. user_scores)
df['date'] = pd.to_datetime(df['date'])

# סטטיסטיקות ראשיות
col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_score = df['score'].mean()
    st.markdown(f"""
    <div class="stat-card">
        <div>ציון ממוצע</div>
        <div class="stat-number">{avg_score:. 1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    total_tests = len(df)
    st.markdown(f"""
    <div class="stat-card">
        <div>מבחנים שהושלמו</div>
        <div class="stat-number">{total_tests}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    total_questions = df['questions'].sum()
    st.markdown(f"""
    <div class="stat-card">
        <div>סה"כ שאלות</div>
        <div class="stat-number">{total_questions}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    best_score = df['score'].max()
    st.markdown(f"""
    <div class="stat-card">
        <div>הציון הטוב ביותר</div>
        <div class="stat-number">{best_score}%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# גרפים
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 התקדמות לאורך זמן")
    
    # גרף התקדמות
    fig_progress = go.Figure()
    
    df_sorted = df.sort_values('date')
    fig_progress.add_trace(go.Scatter(
        x=df_sorted['date'],
        y=df_sorted['score'],
        mode='lines+markers',
        name='ציון',
        line=dict(color='#667eea', width=3),
        marker=dict(size=8)
    ))
    
    # הוספת קו ממוצע
    fig_progress.add_hline(
        y=avg_score, 
        line_dash="dash", 
        line_color="gray",
        annotation_text=f"ממוצע: {avg_score:.1f}%"
    )
    
    fig_progress.update_layout(
        xaxis_title="תאריך",
        yaxis_title="ציון (%)",
        yaxis_range=[0, 105],
        hovermode='x unified',
        showlegend=False,
        height=350
    )
    
    st.plotly_chart(fig_progress, use_container_width=True)

with col2:
    st.subheader("📊 התפלגות ציונים")
    
    # היסטוגרמה של ציונים
    fig_hist = px.histogram(
        df, 
        x='score', 
        nbins=10,
        color_discrete_sequence=['#764ba2']
    )
    
    fig_hist.update_layout(
        xaxis_title="ציון",
        yaxis_title="מספר מבחנים",
        showlegend=False,
        height=350
    )
    
    st.plotly_chart(fig_hist, use_container_width=True)

# ביצועים לפי נושא
st.subheader("🎯 ביצועים לפי נושא")

if 'topic' in df.columns:
    topic_stats = df.groupby('topic').agg({
        'score':  'mean',
        'questions': 'sum',
        'correct': 'sum'
    }).round(1)
    
    topic_stats['accuracy'] = (topic_stats['correct'] / topic_stats['questions'] * 100).round(1)
    topic_stats = topic_stats.rename(columns={
        'score': 'ציון ממוצע (%)',
        'questions': 'סה"כ שאלות',
        'correct': 'תשובות נכונות',
        'accuracy': 'אחוז דיוק (%)'
    })
    
    st.dataframe(topic_stats, use_container_width=True)
    
    # גרף עמודות לפי נושא
    fig_topics = px.bar(
        x=topic_stats.index,
        y=topic_stats['ציון ממוצע (%)'],
        color=topic_stats['ציון ממוצע (%)'],
        color_continuous_scale='Viridis'
    )
    
    fig_topics.update_layout(
        xaxis_title="נושא",
        yaxis_title="ציון ממוצע (%)",
        showlegend=False,
        height=300
    )
    
    st.plotly_chart(fig_topics, use_container_width=True)

# היסטוריית מבחנים
st.subheader("📜 היסטוריית מבחנים אחרונים")

df_recent = df.sort_values('date', ascending=False).head(10)
df_display = df_recent[['date', 'topic', 'score', 'questions', 'correct']].copy()
df_display. columns = ['תאריך', 'נושא', 'ציון (%)', 'שאלות', 'נכונות']
df_display['תאריך'] = df_display['תאריך'].dt.strftime('%d/%m/%Y')

st.dataframe(
    df_display,
    use_container_width=True,
    hide_index=True,
    column_config={
        "ציון (%)": st.column_config.ProgressColumn(
            "ציון (%)",
            help="הציון במבחן",
            min_value=0,
            max_value=100,
        ),
    }
)

# המלצות אישיות
st.subheader("💡 המלצות אישיות")

weak_topics = df. groupby('topic')['score'].mean().sort_values().head(2)

if len(weak_topics) > 0:
    st.info(f"""
    **בהתבסס על הביצועים שלך, מומלץ:**
    
    🔸 להתמקד בנושאים:  {', '.join(weak_topics.index)}
    
    🔸 לחזור על חומר הלמידה בנושאים אלו
    
    🔸 לבצע תרגול נוסף של שאלות
    
    🔸 הממוצע שלך ({avg_score:.1f}%) {'מעל הממוצע הכללי - כל הכבוד!' if avg_score > 75 else 'יש מקום לשיפור - המשך להתאמן! '}
    """)

# סרגל צד - יעדים
with st.sidebar:
    st.subheader("🎯 היעדים שלך")
    
    target_score = st.slider("יעד ציון ממוצע", 60, 100, 85)
    
    if avg_score >= target_score:
        st. success(f"✅ הגעת ליעד! ({avg_score:.1f}%)")
    else:
        gap = target_score - avg_score
        st.warning(f"📈 {gap:.1f}% עד היעד")
        
        # חישוב כמה מבחנים טובים נדרשים
        tests_needed = int(gap / 5) + 1
        st.info(f"💪 עוד {tests_needed} מבחנים עם ציון {target_score}+ יביאו אותך ליעד!")
    
    st.divider()
    
    # סטטיסטיקת השבוע
    st.subheader("📅 השבוע שלך")
    
    week_ago = datetime.now() - timedelta(days=7)
    week_tests = df[df['date'] > week_ago]
    
    if len(week_tests) > 0:
        st.metric("מבחנים השבוע", len(week_tests))
        st.metric("ממוצע השבוע", f"{week_tests['score']. mean():.1f}%")
    else:
        st. info("אין פעילות השבוע")
