import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils.content_manager import restore_user_session
from utils.styles import get_common_styles

st.set_page_config(page_title="לוח תוצאות", page_icon="🏆", layout="wide")

# Restore user session if available
restore_user_session(st)

# CSS מרכזי
st.markdown(get_common_styles(), unsafe_allow_html=True)

# CSS נוסף ספציפי לדף
st.markdown("""
<style>
    /* תיקון טבלה */
    [data-testid="stDataFrameResizable"] {
        direction: ltr !important;
    }
    
    [data-testid="stDataFrameResizable"] td {
        text-align: right !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="leaderboard-header">
    <h1>🏆 לוח תוצאות - תחרות בין מוסדית</h1>
</div>
""", unsafe_allow_html=True)

# יצירת נתונים ריאליים
current_date = datetime.now().strftime("%d/%m/%Y")
st.caption(f"📅 עדכון:  {current_date}")

# הצגת הודעה שאין עדיין נתונים
st.info("🎯 לוח התוצאות יתעדכן ברגע שמשתמשים יתחילו להשתמש במערכת!")

st.markdown("""
<div style='text-align: center; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin: 20px 0;'>
    <h2 style='color: white; margin: 0;'>🏆 המרוץ מתחיל!</h2>
    <p style='color: white; margin-top: 10px; font-size: 1.2rem;'>השלימו מבחנים, צברו נקודות והובילו את המוסד שלכם לפסגה!</p>
</div>
""", unsafe_allow_html=True)

# דוגמה להדמיה - נתונים דמה רק למראה
st.markdown("### 📊 כך ייראה לוח התוצאות:")

data = {
    'דירוג': range(1, 6),
    'מוסד': [
        'המוסד שלך',
        'מוסד דוגמה 2', 
        'מוסד דוגמה 3',
        'מוסד דוגמה 4',
        'מוסד דוגמה 5'
    ],
    'ציון ממוצע': [0, 0, 0, 0, 0],
    'משתתפים': [0, 0, 0, 0, 0],
    'מבחנים כולל': [0, 0, 0, 0, 0]
}

df = pd.DataFrame(data)

# עיצוב המדליות
def get_medal(rank):
    if rank == 1:
        return "🥇"
    elif rank == 2:
        return "🥈"
    elif rank == 3:
        return "🥉"
    else: 
        return f"{rank}"

df['מקום'] = df['דירוג'].apply(get_medal)

# הפודיום - תיקון היישור
st.subheader("הפודיום 🏆")

# CSS מיוחד לפודיום - נסתיר על מובייל ונציג אנכית
st.markdown("""
<style>
    .podium-container {
        display: flex;
        justify-content: center;
        align-items: flex-end;
        gap: 10px;
        margin: 20px 0;
    }
    
    .podium-place {
        text-align: center;
        padding: 20px;
        border-radius: 10px;
        color: white;
        flex: 1;
        max-width: 250px;
    }
    
    .podium-first {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        order: 2;
    }
    
    .podium-second {
        background: linear-gradient(135deg, #C0C0C0, #808080);
        margin-top: 40px;
        order: 1;
    }
    
    .podium-third {
        background: linear-gradient(135deg, #CD7F32, #8B4513);
        margin-top: 60px;
        order: 3;
    }
    
    /* מובייל - הצגה אנכית */
    @media (max-width: 768px) {
        .podium-container {
            flex-direction: column;
            align-items: stretch;
        }
        
        .podium-place {
            max-width: 100%;
            margin-top: 0 !important;
        }
        
        .podium-first {
            order: 1;
        }
        
        .podium-second {
            order: 2;
        }
        
        .podium-third {
            order: 3;
        }
    }
</style>
""", unsafe_allow_html=True)

# הפודיום בHTML
st.markdown(f"""
<div class="podium-container">
    <div class="podium-place podium-first">
        <h2 style='margin: 0;'>🥇</h2>
        <h3 style='margin: 10px 0;'>מקום ראשון</h3>
        <h4 style='margin: 10px 0;'>{df.iloc[0]['מוסד']}</h4>
        <p style='margin: 0;'>ציון ממוצע: {df.iloc[0]['ציון ממוצע']:.1f}%</p>
        <p style='margin: 0;'>משתתפים: {df.iloc[0]['משתתפים']}</p>
    </div>
    
    <div class="podium-place podium-second">
        <h2 style='margin: 0;'>🥈</h2>
        <h3 style='margin: 10px 0;'>מקום שני</h3>
        <h4 style='margin: 10px 0;'>{df.iloc[1]['מוסד']}</h4>
        <p style='margin: 0;'>ציון ממוצע: {df.iloc[1]['ציון ממוצע']:.1f}%</p>
        <p style='margin: 0;'>משתתפים: {df.iloc[1]['משתתפים']}</p>
    </div>
    
    <div class="podium-place podium-third">
        <h2 style='margin: 0;'>🥉</h2>
        <h3 style='margin: 10px 0;'>מקום שלישי</h3>
        <h4 style='margin: 10px 0;'>{df.iloc[2]['מוסד']}</h4>
        <p style='margin: 0;'>ציון ממוצע: {df.iloc[2]['ציון ממוצע']:.1f}%</p>
        <p style='margin: 0;'>משתתפים: {df.iloc[2]['משתתפים']}</p>
    </div>
</div>
""", unsafe_allow_html=True)
st.divider()

# טבלה מלאה
st.subheader("📊 טבלת דירוג מלאה")

# הצגת הטבלה
display_df = df[['מקום', 'מוסד', 'ציון ממוצע', 'משתתפים', 'מבחנים כולל']]. copy()

# עיצוב הטבלה
st.dataframe(
    display_df,
    hide_index=True,
    use_container_width=True,
    column_config={
        "מקום": st.column_config.TextColumn("מקום", width="small"),
        "מוסד":  st.column_config.TextColumn("מוסד", width="large"),
        "ציון ממוצע": st.column_config. ProgressColumn(
            "ציון ממוצע",
            help="ציון ממוצע של כל המשתתפים מהמוסד",
            format="%.1f%%",
            min_value=0,
            max_value=100,
        ),
        "משתתפים": st.column_config.NumberColumn("משתתפים", help="מספר משתתפים פעילים"),
        "מבחנים כולל": st.column_config.NumberColumn("סה״כ מבחנים", help="מספר מבחנים שבוצעו")
    }
)

# גרפים
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 התפלגות ציונים")
    
    # יצירת גרף עמודות
    fig = px.bar(
        df.head(5), 
        x='ציון ממוצע', 
        y='מוסד',
        orientation='h',
        color='ציון ממוצע',
        color_continuous_scale='Viridis',
        title='חמשת המובילים'
    )
    fig.update_layout(
        xaxis_title="ציון ממוצע (%)",
        yaxis_title="",
        showlegend=False,
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("👥 מספר משתתפים")
    
    # יצירת גרף עוגה
    fig = px.pie(
        df.head(5),
        values='משתתפים',
        names='מוסד',
        title='התפלגות משתתפים - חמשת המובילים'
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# הוסף מידע נוסף
st.divider()
with st.expander("ℹ️ על התחרות"):
    st.info("""
    ### איך מחושב הדירוג?
    
    - **ציון ממוצע**: ממוצע הציונים של כל המשתתפים מהמוסד
    - **מינימום משתתפים**: נדרשים לפחות 5 משתתפים פעילים
    - **מינימום מבחנים**:  כל משתתף צריך לבצע לפחות 3 מבחנים
    - **עדכון**: הדירוג מתעדכן בזמן אמת
    
    ### פרסים: 
    🥇 **מקום ראשון**:  תעודת הצטיינות + השתלמות מקצועית  
    🥈 **מקום שני**: תעודת הצטיינות  
    🥉 **מקום שלישי**: תעודת הערכה
    
    ### תקופת התחרות:
    1. 1.2025 - 31.12.2025
    """)
