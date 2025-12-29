# -*- coding: utf-8 -*-
import streamlit as st
import sys
from pathlib import Path

# הוספת נתיב לתיקיית הבסיס
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.styles import get_common_styles

# הגדרות עמוד
st.set_page_config(
    page_title="מחשבונים רפואיים | PICU",
    page_icon="🧮",
    layout="wide"
)

# טעינת CSS
st.markdown(get_common_styles(), unsafe_allow_html=True)

# כותרת
st.title("🧮 מחשבונים רפואיים")

# תפריט בחירת מחשבון
calculator_type = st.selectbox(
    "בחר מחשבון:",
    ["מחשבון פרקלנד לכוויות", "אלגוריתם טיפול בשוק היפוולמי אינטראקטיבי"]
)

st.markdown("---")

# ===== מחשבון פרקלנד =====
if calculator_type == "מחשבון פרקלנד לכוויות":
    st.header("🔥 מחשבון פרקלנד לכוויות")
    
    st.info("""
    **נוסחת פרקלנד (Parkland Formula):**
    
    נפח נוזלים ב-24 שעות = 4ml × משקל (kg) × אחוז שטח גוף נכווה (TBSA%)
    
    - **50% מהנוזלים בשמונה שעות הראשונות** מזמן הכוויה
    - **50% הנותרים ב-16 שעות הבאות**
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        weight = st.number_input(
            "משקל הילד (ק\"ג):",
            min_value=1.0,
            max_value=150.0,
            value=20.0,
            step=0.5,
            help="הכנס את משקל הילד בקילוגרמים"
        )
        
        tbsa = st.number_input(
            "אחוז שטח גוף נכווה (TBSA %):",
            min_value=1,
            max_value=100,
            value=20,
            step=1,
            help="שטח הכוויות כאחוז מכלל משטח הגוף. השתמש ב-Rule of 9's או Lund-Browder"
        )
        
        hours_since_burn = st.number_input(
            "שעות מאז הכוויה:",
            min_value=0.0,
            max_value=24.0,
            value=2.0,
            step=0.5,
            help="כמה זמן עבר מאז הכוויה?"
        )
    
    with col2:
        if st.button("🧮 חשב", type="primary", use_container_width=True):
            # חישובים
            total_24h = 4 * weight * tbsa
            first_8h = total_24h / 2
            next_16h = total_24h / 2
            
            # חישוב נפח שכבר היה צריך להינתן
            if hours_since_burn <= 8:
                # עדיין בשמונה שעות ראשונות
                rate_first_8h = first_8h / 8
                already_given = rate_first_8h * hours_since_burn
                remaining_first_8h = first_8h - already_given
                time_left_first = 8 - hours_since_burn
                
                # אם יש זמן ב-8 שעות ראשונות
                if time_left_first > 0:
                    rate_now = remaining_first_8h / time_left_first
                else:
                    rate_now = next_16h / 16
                    
            else:
                # עברנו את 8 השעות הראשונות
                already_given = first_8h
                hours_in_second = hours_since_burn - 8
                rate_second_16h = next_16h / 16
                already_given_second = rate_second_16h * hours_in_second
                remaining_second = next_16h - already_given_second
                time_left_second = 16 - hours_in_second
                
                if time_left_second > 0:
                    rate_now = remaining_second / time_left_second
                else:
                    rate_now = 0
            
            # תצוגת תוצאות
            st.success("### 📊 תוצאות חישוב:")
            
            st.metric("נפח כולל ב-24 שעות", f"{total_24h:.0f} ml", f"{total_24h/1000:.1f} ליטר")
            
            col_res1, col_res2 = st.columns(2)
            with col_res1:
                st.metric("8 שעות ראשונות", f"{first_8h:.0f} ml")
                st.metric("קצב עירוי (8 שעות ראשונות)", f"{first_8h/8:.1f} ml/hr")
            
            with col_res2:
                st.metric("16 שעות הבאות", f"{next_16h:.0f} ml")
                st.metric("קצב עירוי (16 שעות)", f"{next_16h/16:.1f} ml/hr")
            
            if hours_since_burn > 0:
                st.markdown("---")
                st.warning(f"""
                ### ⚠️ התאמה לזמן שעבר ({hours_since_burn} שעות מאז הכוויה):
                
                **קצב עירוי מומלץ כעת:** `{rate_now:.1f} ml/hr`
                """)
            
            st.markdown("---")
            st.info("""
            ### 💡 נקודות חשובות:
            
            - השתמש ב-**Lactated Ringer (LR)** או **Normal Saline**
            - **התאם את הקצב לפי תפוקת שתן:** מטרה 0.5-1 ml/kg/hr
            - נוסחה זו היא **נקודת התחלה** - התאם לפי מצב קליני
            - בכוויות מעל 50% - חשב לפי 50% בלבד
            - **ניטור הכרחי:** תפוקת שתן, לחץ דם, גזים, לקטט
            - שקול **אלבומין/קולואיד** לאחר 12-24 שעות במקרים מסוימים
            - **זהירות מעומס נוזלים:** ARDS, Compartment Syndrome
            """)

# ===== אלגוריתם שוק היפוולמי אינטראקטיבי =====
elif calculator_type == "אלגוריתם טיפול בשוק היפוולמי אינטראקטיבי":
    st.header("💧 אלגוריתם טיפול בשוק היפוולמי - אינטראקטיבי")
    
    # Initialize session state
    if 'shock_step' not in st.session_state:
        st.session_state.shock_step = 0
    if 'shock_data' not in st.session_state:
        st.session_state.shock_data = {}
    
    def reset_algorithm():
        st.session_state.shock_step = 0
        st.session_state.shock_data = {}
    
    # Progress bar
    total_steps = 6
    progress = st.session_state.shock_step / total_steps
    st.progress(progress, text=f"שלב {st.session_state.shock_step} מתוך {total_steps}")
    
    # שלב 0: פרטי המטופל
    if st.session_state.shock_step == 0:
        st.subheader("📋 פרטי המטופל")
        
        weight = st.number_input("משקל (ק\"ג):", min_value=1.0, max_value=150.0, value=20.0, step=0.5)
        age = st.number_input("גיל (שנים):", min_value=0.0, max_value=18.0, value=5.0, step=0.5)
        
        if st.button("▶️ המשך", type="primary"):
            st.session_state.shock_data['weight'] = weight
            st.session_state.shock_data['age'] = age
            st.session_state.shock_step = 1
            st.rerun()
    
    # שלב 1: זיהוי וחשד
    elif st.session_state.shock_step == 1:
        st.subheader("🚨 שלב 1: זיהוי וחשד לשוק")
        
        st.info(f"**מטופל:** גיל {st.session_state.shock_data['age']} שנים, משקל {st.session_state.shock_data['weight']} ק\"ג")
        
        signs = st.multiselect(
            "סמן את הסימנים הקליניים הקיימים:",
            ["טכיקרדיה", "מילוי קפילרי איטי (>2 שניות)", "גפיים קרות", 
             "ירידה בתפוקת שתן", "היפוטנסיה", "שינוי במצב הכרה", "עייפות/חולשה"]
        )
        
        suspected_cause = st.radio(
            "גורם חשוד לשוק:",
            ["התייבשות (הקאות/שלשולים)", "דימום", "כוויות", "לא ברור"]
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("◀️ חזור"):
                st.session_state.shock_step = 0
                st.rerun()
        with col2:
            if st.button("▶️ המשך לטיפול", type="primary"):
                st.session_state.shock_data['signs'] = signs
                st.session_state.shock_data['cause'] = suspected_cause
                st.session_state.shock_step = 2
                st.rerun()
    
    # שלב 2: הערכה ראשונית
    elif st.session_state.shock_step == 2:
        st.subheader("🔍 שלב 2: הערכה ראשונית")
        
        st.success("""
        ### ✅ בצע:
        - **ABC** - וודא דרכי אוויר, נשימה, מחזור
        - **גישה ורידית** - 2 קטטרים היקפיים / תוך-עצמי
        - **מוניטור** - לחץ דם, דופק, סטורציה, טמפרטורה
        - **חמצן** - בזרימה גבוהה
        - **דגימות:**
          - CBC + כימיה + גזים + לקטט
          - תרבית דם (אם חשד לזיהום)
          - סוג דם וצלב (אם חשד לדימום)
        """)
        
        completed = st.checkbox("✅ ביצעתי את ההערכה הראשונית")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("◀️ חזור"):
                st.session_state.shock_step = 1
                st.rerun()
        with col2:
            if st.button("▶️ המשך לבולוס נוזלים", type="primary", disabled=not completed):
                st.session_state.shock_step = 3
                st.rerun()
    
    # שלב 3: בולוס נוזלים ראשון
    elif st.session_state.shock_step == 3:
        st.subheader("💧 שלב 3: בולוס נוזלים ראשון")
        
        weight = st.session_state.shock_data['weight']
        bolus_20 = weight * 20
        
        st.warning(f"""
        ### 💉 תן בולוס נוזלים:
        
        **מינון:** 20ml/kg
        **נפח לילד זה:** `{bolus_20:.0f} ml`
        
        **סוג נוזל:** Normal Saline (NS) או Lactated Ringer (LR)
        
        **קצב מתן:** מהיר - **10-20 דקות**
        """)
        
        st.info("⏱️ תן את הבולוס והערך מחדש את המטופל...")
        
        completed = st.checkbox("✅ נתתי את הבולוס הראשון")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("◀️ חזור"):
                st.session_state.shock_step = 2
                st.rerun()
        with col2:
            if st.button("▶️ הערך תגובה", type="primary", disabled=not completed):
                st.session_state.shock_data['boluses_given'] = 1
                st.session_state.shock_step = 4
                st.rerun()
    
    # שלב 4: הערכת תגובה
    elif st.session_state.shock_step == 4:
        st.subheader("❓ שלב 4: הערכת תגובה לטיפול")
        
        weight = st.session_state.shock_data['weight']
        boluses = st.session_state.shock_data.get('boluses_given', 1)
        total_fluid = boluses * weight * 20
        
        st.info(f"**נוזלים שניתנו עד כה:** {total_fluid:.0f} ml ({boluses} בולוסים)")
        
        response = st.radio(
            "האם המטופל הגיב לטיפול?",
            ["כן - יש שיפור קליני (דופק יציב, מילוי שיפר, BP תקין)", 
             "לא - אין שיפור / שיפור זמני"],
            help="שיפור = ירידה בדופק, שיפור במילוי קפילרי, יציבות לחץ דם"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("◀️ חזור"):
                st.session_state.shock_step = 3
                st.rerun()
        with col2:
            if st.button("▶️ המשך", type="primary"):
                if "כן" in response:
                    st.session_state.shock_data['response'] = 'yes'
                    st.session_state.shock_step = 6  # קפוץ לסיכום
                else:
                    st.session_state.shock_data['response'] = 'no'
                    # בדוק אם עברנו 60ml/kg
                    if total_fluid >= weight * 60:
                        st.session_state.shock_step = 5  # עבור לבדיקת דימום
                    else:
                        # תן בולוס נוסף
                        st.session_state.shock_data['boluses_given'] = boluses + 1
                        st.session_state.shock_step = 3
                st.rerun()
    
    # שלב 5: בדיקת דימום והסלמה
    elif st.session_state.shock_step == 5:
        st.subheader("🔎 שלב 5: בדיקת דימום והסלמה")
        
        weight = st.session_state.shock_data['weight']
        
        st.warning("⚠️ המטופל לא מגיב לנוזלים - צריך להסלים!")
        
        bleeding = st.radio(
            "האם יש דימום פעיל?",
            ["כן - יש דימום פעיל או חשד לדימום", "לא - אין דימום"]
        )
        
        if "כן" in bleeding:
            prbc_dose = weight * 10
            st.error(f"""
            ### 🩸 פרוטוקול דימום:
            
            1. **PRBC (דם):** `{prbc_dose:.0f} ml` (10ml/kg)
            2. **שקול FFP + Platelets** - יחס 1:1:1 במצבים חמורים
            3. **שקול TXA** (חומצה טרנקסמית) - 15mg/kg
            4. **חפש מקור דימום:**
               - שקול אולטרסאונד (FAST)
               - שקול CT במטופל יציב
               - **התייעץ עם כירורג** - האם נדרש טיפול כירורגי?
            """)
        else:
            st.info(f"""
            ### 💉 אין דימום - המשך נוזלים + אמינים:
            
            1. **המשך נוזלים** (עד 60ml/kg במידת הצורך)
            2. **התחל אמינים (Vasopressors):**
               - **נוראפינפרין (Norepinephrine):** התחל ב-0.05-0.1 mcg/kg/min
               - **אדרנלין (Epinephrine):** אם יש ברדיקרדיה
            3. **חפש גורמים נוספים:**
               - ספסיס?
               - שוק קרדיוגני?
               - אנפילקסיס?
               - פריקרדיאלי?
            """)
        
        critical = st.checkbox("🔴 המטופל עדיין לא יציב / מצב קריטי")
        
        if critical:
            st.error("""
            ### 🚨 הסלמה נוספת:
            
            - שקול **אינוטרופים:** Dobutamine, Milrinone
            - **העבר ל-PICU** אם עדיין לא שם
            - שקול **ניטור פולשני:** קטטר עורקי, CVP
            - במצב קיצון: שקול **ECMO**
            - **התייעץ עם בכיר!**
            """)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("◀️ חזור"):
                st.session_state.shock_step = 4
                st.rerun()
        with col2:
            if st.button("✅ סיים וסכם", type="primary"):
                st.session_state.shock_data['bleeding'] = bleeding
                st.session_state.shock_data['critical'] = critical
                st.session_state.shock_step = 6
                st.rerun()
    
    # שלב 6: סיכום והמלצות
    elif st.session_state.shock_step == 6:
        st.subheader("📋 סיכום והמלצות")
        
        weight = st.session_state.shock_data['weight']
        age = st.session_state.shock_data['age']
        boluses = st.session_state.shock_data.get('boluses_given', 1)
        total_fluid = boluses * weight * 20
        response = st.session_state.shock_data.get('response', 'no')
        
        if response == 'yes':
            st.success(f"""
            ## ✅ המטופל הגיב לטיפול!
            
            ### 📊 טיפול שניתן:
            - **נוזלים:** {total_fluid:.0f} ml ({boluses} בולוסים של 20ml/kg)
            - **משקל:** {weight} ק\"ג
            
            ### 📝 המלצות להמשך:
            
            1. **ניטור:**
               - דופק, BP, CRT כל 15-30 דקות
               - תפוקת שתן: מטרה 0.5-1 ml/kg/hr
               - גזים ולקטט לאחר 1-2 שעות
            
            2. **תחזוקת נוזלים:**
               - עבור לנוזלי תחזוקה (D5 0.45% NS/LR)
               - חשב לפי: 4-2-1 rule או 100-50-20
            
            3. **טיפול בגורם:**
               - התייבשות: המשך נוזלים פומיים הדרגתי
               - זיהום: אנטיביוטיקה
               - דימום: טפל במקור
            
            4. **מעקב:**
               - CBC, אלקטרוליטים בעוד 4-6 שעות
               - שקול אשפוז לתצפית
            """)
        else:
            st.warning(f"""
            ## ⚠️ שוק עמיד לטיפול - מצב מורכב
            
            ### 📊 טיפול שניתן:
            - **נוזלים:** {total_fluid:.0f} ml ({boluses} בולוסים)
            - **משקל:** {weight} ק\"ג
            
            ### 🔴 המטופל זקוק להסלמה:
            """)
            
            if 'bleeding' in st.session_state.shock_data:
                if 'כן' in st.session_state.shock_data['bleeding']:
                    st.error(f"""
                    #### 🩸 פרוטוקול דימום:
                    - PRBC: {weight * 10:.0f} ml (10ml/kg)
                    - שקול FFP + Platelets
                    - TXA: {weight * 15:.0f} mg
                    - **התייעץ עם כירורג**
                    """)
                else:
                    st.info("""
                    #### 💉 פרוטוקול ללא דימום:
                    - **אמינים:** Norepinephrine 0.05-0.1 mcg/kg/min
                    - **חפש גורם נוסף:** ספסיס, קרדיוגני, אנפילקסיס
                    - **שקול אינוטרופים**
                    """)
            
            st.error("""
            ### 🚨 פעולות דחופות:
            1. ✅ **העברה ל-PICU** (אם עדיין לא)
            2. ✅ **ניטור פולשני** (קטטר עורקי, CVP)
            3. ✅ **התייעצות עם בכיר**
            4. ✅ **בדיקות:**
               - אקו לב (תפקוד, נוזלים)
               - גזים + לקטט כל 1-2 שעות
               - ScvO2 במידת האפשר
            5. ✅ **שקול ECMO** במצב קיצון
            """)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 התחל מחדש", use_container_width=True):
                reset_algorithm()
                st.rerun()
        with col2:
            if st.button("📄 הדפס סיכום", use_container_width=True):
                st.info("💡 השתמש בתפריט הדפסה של הדפדפן (Ctrl+P)")

st.markdown("---")
st.caption("💡 מחשבונים אלו הם עזרים קליניים - יש להתאים את הטיפול למצב הספציפי של המטופל.")
