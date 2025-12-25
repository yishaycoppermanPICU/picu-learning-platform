import streamlit as st
import pandas as pd
import plotly. express as px
import plotly. graph_objects as go
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="לוח תוצאות", page_icon="🏆", layout="wide")

# CSS
st.markdown("""
<style>
    .stApp {
        direction: rtl;
    }
    .medal-gold {
        color: #FFD700;
        font-size: 2rem;
    }
    .medal-silver {
        color: #C0C0C0;
        font-size: 2rem;
    }
    .medal-bronze {
        color: #CD7F32;
        font-size:  2rem;
    }
    .institution-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin:  0.5rem 0;
    }
    .rank-display {
        font-size: 3rem;
        font-weight:  bold;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏆 לוח תוצאות - תחרות בין מוסדית")
st.markdown("---")

# יצירת נתונים לדוגמה
institutions = [
    "מרכז שניידר לרפואת ילדים",
    "הדסה עין כרם",
    "רמב״ם",
    "סורוקה",
    "שיבא - תל השומר",
    "אסף הרופא",
    "וולפסון",
    "קפלן",
    "מעייני הישועה",
    "איכילוב"
]

# נתוני מוסדות
data = []
for inst in institutions:
    data.append({
        'institution':  inst,
        'avg_score': random.randint(70, 95) + random.random(),
        'participants': random.randint(5, 30),
        'total_tests': random.randint(20, 200),
        'weekly_tests': random.randint(5, 50),
        'trend': random.choice(['↑', '↓', '→'])
    })

df = pd.DataFrame(data)
df = df.sort_values('avg_score', ascending=False).reset_index(drop=True)
df['rank'] = df.index + 1

# כותרת עם התאריך
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(f"""
    <div style="text-align: center;">
        <h3>🗓️ עדכון: {datetime.now().strftime('%d/%m/%Y')}</h3>
    </div>
    """, unsafe_allow_html=True)

# הפודיום - Top 3
st.subheader("🥇🥈🥉 הפודיום")

podium_cols = st.columns(3)

# מקום שני (כסף)
with podium_cols[0]:
    if len(df) >= 2:
        st.markdown("""
        <div style="text-align: center;">
            <div class="medal-silver">🥈</div>
            <h4>מקום שני</h4>
        </div>
        """, unsafe_allow_html=True)
        st.info(f"""
        **{df.iloc[1]['institution']}**
        
        ציון ממוצע: **{df.iloc[1]['avg_score']:.1f}%**
        
        משתתפים: {df.iloc[1]['participants']}
        """)

# מקום ראשון (זהב)
with podium_cols[1]:
    if len(df) >= 1:
        st.markdown("""
        <div style="text-align: center;">
            <div class="medal-gold">🥇</div>
            <h4>מקום ראשון</h4>
        </div>
        """, unsafe_allow_html=True)
        st.success(f"""
        **{df.iloc[0]['institution']}**
        
        ציון ממוצע: **{df.iloc[0]['avg_score']:.1f}%**
        
        משתתפים: {df.iloc[0]['participants']}
        """)

# מקום שלישי (ארד)
with podium_cols[2]:
    if len(df) >= 3:
        st.markdown("""
        <div style="text-align: center;">
            <div class="medal-bronze">🥉</div>
            <h4>מקום שלישי</h4>
        </div>
        """, unsafe_allow_html=True)
        st.warning(f"""
        **{df. iloc[2]['institution']}**
        
        ציון ממוצע: **{df.iloc[2]['avg_score']:.1f}%**
        
        משתתפים: {df.iloc[2]['participants']}
        """)

st.markdown("---")

# טבלת דירוג מלאה
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 טבלת דירוג מלאה")
    
    # הכנת הטבלה לתצוגה
    df_display = df[['rank', 'institution', 'avg_score', 'participants', 'total_tests', 'trend']].copy()
    df_display.columns = ['דירוג', 'מוסד', 'ציון ממוצע', 'משתתפים', 'סה"כ מבחנים', 'מגמה']
    
    # הוספת אימוג'י למדליות
    df_display['דירוג'] = df_display['דירוג'].apply(lambda x: 
        f"🥇 {x}" if x == 1 else 
        f"🥈 {x}" if x == 2 else 
        f"🥉 {x}" if x == 3 else 
        f"{x}")
    
    # עיצוב הטבלה
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ציון ממוצע":  st.column_config.ProgressColumn(
                "ציון ממוצע",
                help="הציון הממוצע של המוסד",
                format="%.1f%%",
                min_value=0,
                max_value=100,
            ),
            "משתתפים": st.column_config.NumberColumn(
                "משתתפים",
                help="מספר המשתתפים הפעילים"
            ),
        }
    )

with col2:
    st.subheader("📈 התפלגות ציונים")
    
    # גרף עמודות
    fig = px.bar(
        df. head(5),
        x='avg_score',
        y='institution',
        orientation='h',
        color='avg_score',
        color_continuous_scale='Viridis',
        text='avg_score'
    )
    
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(
        xaxis_title="ציון ממוצע (%)",
        yaxis_title="",
        showlegend=False,
        height=300,
        xaxis_range=[60, 100]
    )
    
    st.plotly_chart(fig, use_container_width=True)

# סטטיסטיקות נוספות
st.subheader("📊 סטטיסטיקות כלליות")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_participants = df['participants'].sum()
    st.metric("סה״כ משתתפים", total_participants, f"+{random.randint(5,15)} השבוע")

with col2:
    total_tests = df['total_tests'].sum()
    st.metric("סה״כ מבחנים", total_tests, f"+{random. randint(20,50)} השבוע")

with col3:
    avg_all = df['avg_score'].mean()
    st.metric("ממוצע כללי", f"{avg_all:. 1f}%", "+2.3%")

with col4:
    active_institutions = len(df[df['weekly_tests'] > 0])
    st.metric("מוסדות פעילים", f"{active_institutions}/{len(df)}")

# גרף מגמות
st.subheader("📈 מגמות חודשיות")

# יצירת נתוני מגמה לדוגמה
months = pd.date_range(start='2024-01', periods=12, freq='M')
trend_data = []

for inst in institutions[: 5]:  # רק 5 המובילים
    for month in months:
        trend_data.append({
            'month': month,
            'institution': inst,
            'score': random.randint(70, 95) + random.random()
        })

df_trend = pd.DataFrame(trend_data)

fig_trend = px.line(
    df_trend,
    x='month',
    y='score',
    color='institution',
    title='מגמת ציונים - 5 המוסדות המובילים'
)

fig_trend.update_layout(
    xaxis_title="חודש",
    yaxis_title="ציון ממוצע (%)",
    legend_title="מוסד",
    hovermode='x unified',
    height=400
)

st.plotly_chart(fig_trend, use_container_width=True)

# המוסד שלי
if st.session_state.get('logged_in', False) and st.session_state.get('institution'):
    st.subheader("🏥 המוסד שלי")
    
    my_inst = st.session_state.institution
    my_data = df[df['institution'] == my_inst]
    
    if not my_data.empty:
        my_rank = my_data.iloc[0]['rank']
        my_score = my_data.iloc[0]['avg_score']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("הדירוג שלכם", f"#{my_rank}")
        
        with col2:
            st.metric("הציון הממוצע שלכם", f"{my_score:.1f}%")
        
        with col3:
            if my_rank <= 3:
                st.success("🎉 אתם על הפודיום!")
            elif my_rank <= 5:
                st.info("💪 קרובים לפודיום!")
            else:
                to_podium = df. iloc[2]['avg_score'] - my_score
                st. warning(f"📈 עוד {to_podium:.1f}% לפודיום")
    else:
        st.info("המוסד שלך עדיין לא מופיע בדירוג.  המשך להתאמן!")

# סרגל צד - פילטרים
with st.sidebar:
    st.subheader("🔍 סינון תוצאות")
    
    min_participants = st.slider(
        "מינימום משתתפים",
        0, 30, 0
    )
    
    df_filtered = df[df['participants'] >= min_participants]
    
    if len(df_filtered) < len(df):
        st.info(f"מציג {len(df_filtered)} מתוך {len(df)} מוסדות")
    
    st.divider()
    
    # הסברים
    st.subheader("ℹ️ על הדירוג")
    st.info("""
    **איך מחושב הדירוג?**
    
    🔸 ממוצע הציונים של כל המשתתפים במוסד
    
    🔸 מינימום 5 משתתפים פעילים
    
    🔸 עדכון יומי של הנתונים
    
    🔸 כל המוסדות מתחרים בתנאים שווים
    """)
    
    st.divider()
    
    # פרסים
    st.subheader("🎁 פרסים חודשיים")
    st.success("""
    **המוסד המוביל בסוף החודש:**
    
    🥇 תעודת הוקרה דיגיטלית
    
    🏆 אזכור מיוחד באתר
    
    📚 גישה לתכנים מיוחדים
    """)
