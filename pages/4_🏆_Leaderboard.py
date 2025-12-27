import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils.content_manager import restore_user_session

st.set_page_config(page_title="לוח תוצאות", page_icon="🏆", layout="wide")

# Restore user session if available
restore_user_session(st)

# CSS לעברית
st.markdown("""
<style>
    .stApp {
        direction: rtl !important;
        text-align: right ! important;
    }
    
    h1, h2, h3 {
        text-align: center !important;
    }
    
    .leaderboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
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

# הכנת נתונים מעודכנים
data = {
    'דירוג': range(1, 11),
    'מוסד': [
        'שיבא - תל השומר',
        'איכילוב - תל אביב', 
        'רמב"ם - חיפה',
        'הדסה עין כרם - ירושלים',
        'סורוקה - באר שבע',
        'מרכז שניידר לרפואת ילדים',
        'בלינסון - פתח תקווה',
        'אסף הרופא - צריפין',
        'שערי צדק - ירושלים',
        'וולפסון - חולון'
    ],
    'ציון ממוצע': [88.4, 88.3, 88.1, 86.0, 82.9, 82.4, 77.8, 76.9, 71.9, 72.4],
    'משתתפים': [10, 27, 9, 8, 30, 27, 13, 19, 21, 18],
    'מבחנים כולל': [113, 148, 95, 31, 67, 88, 45, 117, 71, 64]
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

# שינוי הסדר - מקום שני, ראשון, שלישי
col1, col2, col3 = st.columns([1, 1, 1])

with col2:  # מקום ראשון במרכז
    st.markdown("""
    <div style='text-align: center; padding:  20px; background:  linear-gradient(135deg, #FFD700, #FFA500); border-radius: 10px; margin: 0 5px;'>
        <h2 style='color: white; margin: 0;'>🥇</h2>
        <h3 style='color: white; margin: 10px 0;'>מקום ראשון</h3>
        <h4 style='color: white; margin: 10px 0;'>{}</h4>
        <p style='color: white; margin: 0;'>ציון ממוצע: {:.1f}%</p>
        <p style='color: white; margin: 0;'>משתתפים: {}</p>
    </div>
    """. format(df.iloc[0]['מוסד'], df.iloc[0]['ציון ממוצע'], df.iloc[0]['משתתפים']), unsafe_allow_html=True)

with col1:  # מקום שני משמאל
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #C0C0C0, #808080); border-radius: 10px; margin-top: 40px; margin-left: 5px;'>
        <h2 style='color: white; margin: 0;'>🥈</h2>
        <h3 style='color: white; margin:  10px 0;'>מקום שני</h3>
        <h4 style='color: white; margin: 10px 0;'>{}</h4>
        <p style='color: white; margin: 0;'>ציון ממוצע: {:.1f}%</p>
        <p style='color: white; margin:  0;'>משתתפים: {}</p>
    </div>
    """.format(df.iloc[1]['מוסד'], df.iloc[1]['ציון ממוצע'], df.iloc[1]['משתתפים']), unsafe_allow_html=True)

with col3:  # מקום שלישי מימין
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #CD7F32, #8B4513); border-radius: 10px; margin-top: 60px; margin-right: 5px;'>
        <h2 style='color: white; margin: 0;'>🥉</h2>
        <h3 style='color: white; margin: 10px 0;'>מקום שלישי</h3>
        <h4 style='color: white; margin: 10px 0;'>{}</h4>
        <p style='color: white; margin: 0;'>ציון ממוצע: {:.1f}%</p>
        <p style='color:  white; margin: 0;'>משתתפים: {}</p>
    </div>
    """.format(df.iloc[2]['מוסד'], df.iloc[2]['ציון ממוצע'], df.iloc[2]['משתתפים']), unsafe_allow_html=True)
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
