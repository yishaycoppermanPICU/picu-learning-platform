#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
הוספת תוכן: תוצרי דם (Blood Products)
"""

from utils.database import init_supabase, create_content_item, create_content_section

def add_blood_products():
    """הוספת תוצרי דם"""
    
    print("🔄 מתחבר למסד הנתונים...")
    supabase = init_supabase()
    
    if not supabase:
        print("❌ שגיאה בחיבור למסד נתונים")
        return False
    
    print("✅ חיבור הצליח!")
    
    # יצירת הנושא הראשי
    print("\n📝 יוצר נושא: תוצרי דם...")
    
    topic_data = {
        "title": "תוצרי דם - Blood Products",
        "category": "medications",
        "description": "מדריך מקיף לתוצרי דם: טסיות, קריופרסיפיטט, דם ארוז, פלזמה טרייה קפואה, גרנולוציטים",
        "icon": "🩸",
        "slug": "blood-products",
        "tags": ["תרופות", "תוצרי דם", "טסיות", "PLT", "FFP", "PRBCs", "קריו", "גרנולוציטים", "עירוי דם"],
        "order_index": 11
    }
    
    topic = create_content_item(topic_data)
    
    if not topic:
        print("❌ שגיאה ביצירת הנושא")
        return False
    
    topic_id = topic['id']
    print(f"✅ נושא נוצר בהצלחה! ID: {topic_id}")
    
    # הוספת מקטעים
    sections = [
        {
            "title": "טסיות - Platelets (PLT)",
            "section_type": "text",
            "content": """**Platelets - טסיות / PLT / Thrombocytes**

**תיאור:**
תוצר דם המכיל טסיות מרוכזות ממספר תורמים (Random Donor) או תורם יחיד (Apheresis/Single Donor)

---

**📊 מינון:**

**ילדים:**
🩸 **10-20 ml/kg** (כל שקית ~50-60 ml)
או
🩸 **1 unit/10 kg** משקל גוף

**מבוגרים:**
🩸 **1 unit (apheresis)** או **4-6 units (random donor)**

**עליה צפויה:**
- **1 unit PLT** ← עליה של **~5,000-10,000/µL**
- **1 apheresis unit** ← עליה של **~30,000-60,000/µL**

---

**🎯 התוויות:**

✅ **דימום פעיל עם תרומבוציטופניה**
✅ **PLT <10,000/µL** (מניעת דימום ספונטני)
✅ **PLT <50,000/µL** עם ניתוח/פרוצדורה פולשנית
✅ **PLT <100,000/µL** עם נוירוכירורגיה או דימום CNS
✅ **PLT dysfunction** (תפקוד לקוי למרות ספירה תקינה)

---

**⏰ תדירות:**

**משך חיים של טסיות:**
- **in vivo:** ~7-10 ימים (טסיות עצמיות)
- **לאחר עירוי:** ~3-5 ימים (קצר יותר בצריכה, זיהום, DIC)

**ניטור:**
- ספירת PLT **1 שעה ו-24 שעות** לאחר עירוי
- CCI (Corrected Count Increment) - מדד יעילות

---

**✅ יתרונות:**

✅ **עליה מהירה בטסיות**
✅ **מניעת דימום ספונטני**
✅ **חיוני בדימום טרומבוציטופני**

---

**⚠️ תופעות לוואי:**

**שכיחות:**
- **חום** (Febrile Non-Hemolytic Transfusion Reaction - FNHTR)
- **אלרגיה** (פריחה, גרד)
- **TRALI** (Transfusion-Related Acute Lung Injury) - נדיר אך חמור

**נדירות חמורות:**
- **אנפילקסיס**
- **Septic transfusion** (זיהום בשקית)
- **TACO** (Transfusion-Associated Circulatory Overload)
- **Refractoriness** (אי-תגובה בעקבות נוגדנים)

---

**🚨 TRALI:**

**הגדרה:**
פגיעה ריאתית חריפה תוך 6 שעות מעירוי

**סימנים:**
- קוצר נשימה חמור
- היפוקסמיה
- אדמה ריאתית (בצילום חזה)
- ללא עומס נוזלים

**טיפול:**
- תמיכה נשימתית (חמצן, אוורור)
- הפסקת עירוי
- דיאורטיקה בד"כ לא עוזרת (להבדיל מ-TACO)

---

**⚠️ זהירות:**

🚨 **אלואימוניזציה:** חשיפה חוזרת ← נוגדנים ← אי-תגובה (refractoriness)
🚨 **ITP/TTP:** זהירות! לפעמים טסיות מחמירות מצב
🚨 **HIT (Heparin-Induced Thrombocytopenia):** לא לתת טסיות אם יש HIT פעיל
🚨 **Septic shock:** טסיות בדימום, לא רק כדי "לתקן" מספר

---

**⚠️ התוויות נגד יחסיות:**

❌ **TTP/HUS** ללא דימום (עלול להחמיר!)
❌ **ITP** ללא דימום מסכן חיים
❌ **HIT פעיל** (Heparin-Induced Thrombocytopenia)

---

**💡 פנינים קליניות:**

💎 **Threshold להעברה:**
- <10K: מניעה (prophylactic)
- <50K: ניתוח/פרוצדורה
- <100K: נוירוכירורגיה, דימום CNS

💎 **1 hour post-transfusion count:** מדד ליעילות העירוי

💎 **Refractoriness:** אי-עליה בטסיות ← נוגדנים (HLA, HPA). צריך matched platelets

💎 **CMV-negative:** חשוב בחסרי חיסון (premies, BMT)

💎 **Irradiated PLT:** חובה בחולי BMT, חסרי חיסון (מניעת TA-GVHD)

💎 **ABO matching:** לא הכרחי אך עדיף (מפחית המוליזה קלה)

💎 **Apheresis vs Random:** Apheresis = תורם יחיד, פחות חשיפה אנטיגנית

💎 **חום פוסט-עירוי:** שכיח. פרצטמול לפני עירוי (premedication)

💎 **תקף 5 ימים:** בד"כ טסיות תקפות 5 ימים מתרומה (צריך אחסון בטמפ' חדר + תנועה מתמדת)""",
            "order_index": 0
        },
        {
            "title": "קריופרסיפיטט - Cryoprecipitate",
            "section_type": "text",
            "content": """**Cryoprecipitate - קריופרסיפיטט / Cryo**

**תיאור:**
תוצר דם עשיר בגורמי קרישה: **Fibrinogen, Factor VIII, vWF, Factor XIII, Fibronectin**

---

**📊 מינון:**

**ילדים:**
🩸 **1-2 units/10 kg** משקל גוף
- כל unit ≈ 10-15 ml

**מבוגרים:**
🩸 **10 units** (dose טיפוסית)

**עליה צפויה:**
- **1 unit Cryo** ← עליה של **~5-10 mg/dL Fibrinogen**
- **10 units** ← עליה של **~50-100 mg/dL Fibrinogen**

---

**🎯 התוויות:**

✅ **היפופיברינוגנמיה** (Fibrinogen <100 mg/dL)
✅ **DIC** עם היפופיברינוגנמיה ודימום
✅ **דימום מסיבי** עם מחסור ב-Fibrinogen
✅ **vWD** (von Willebrand Disease) - אם אין DDAVP/Factor VIII concentrate
✅ **Uremic bleeding** (דימום אורמי)
✅ **פצעים שלא מתרפאים** (Fibrin glue)

---

**⏰ תדירות:**

**משך השפעה:**
- **Fibrinogen:** זמן מחצית חיים ~3-5 ימים
- **Factor VIII:** זמן מחצית חיים ~8-12 שעות

**ניטור:**
- Fibrinogen level לפני ואחרי
- PTT (אם מטרה גם Factor VIII)

---

**✅ יתרונות:**

✅ **מרוכז בFibrinogen** (יעיל יותר מ-FFP)
✅ **נפח קטן** (פחות עומס נוזלים)
✅ **מכיל vWF** (מתאים ל-vWD)

---

**⚠️ תופעות לוואי:**

**שכיחות:**
- **חום, צמרמורות** (FNHTR)
- **אלרגיה** (פריחה, אורטיקריה)

**נדירות חמורות:**
- **TRALI** (Transfusion-Related Acute Lung Injury)
- **TACO** (Circulatory Overload) - נדיר (נפח קטן)
- **אנפילקסיס** (נדיר)
- **זיהום** (viruses - נדיר מאוד כיום)

---

**⚠️ זהירות:**

🚨 **עומס נוזלים:** פחות בעייתי מ-FFP (נפח קטן), אך עדיין לשקול
🚨 **ABO matching:** רצוי (מכיל קצת פלזמה)
🚨 **זיהומים:** סיכון נמוך (סקרינינג תורמים)

---

**💡 פנינים קליניות:**

💎 **מתי לתת:** Fibrinogen <100 mg/dL + דימום. או <50 mg/dL מניעתי

💎 **Massive transfusion:** קריו חשוב! Fibrinogen יורד מהר בדימום מסיבי

💎 **יותר יעיל מ-FFP:** לתיקון Fibrinogen, Cryo מרוכז יותר (פחות נפח)

💎 **vWD:** Cryo אופציה אם אין DDAVP או concentrates ייעודיים

💎 **Fibrin glue:** משתמשים בCryo ליצירת דבק פיברין (Fibrin glue) לפצעים

💎 **Uremic bleeding:** Cryo + DDAVP משפרים תפקוד טסיות באורמיה

💎 **10 units standard:** מינון סטנדרטי במבוגרים = 10 units (bag אחד)

💎 **אחסון:** קפוא. הפשרה לוקחת זמן. לתכנן מראש!

💎 **תקף 6 שעות:** לאחר הפשרה, Cryo תקף 6 שעות (4°C) או 4 שעות (טמפ' חדר)""",
            "order_index": 1
        },
        {
            "title": "תאי דם אדומים ארוזים - Packed Red Blood Cells (PRBCs)",
            "section_type": "text",
            "content": """**Packed Red Blood Cells - תאי דם אדומים ארוזים / PRBCs / Packed Cells**

**תיאור:**
תוצר דם המכיל תאי דם אדומים מרוכזים (Hct ~55-60%), לאחר הסרת רוב הפלזמה

---

**📊 מינון:**

**ילדים:**
🩸 **10-15 ml/kg** (עירוי אחד)
- עליה צפויה: **~2-3 g/dL Hb** (או ~6-9% Hct)

**מבוגרים:**
🩸 **1 unit** (≈ 250-350 ml)
- עליה צפויה: **~1 g/dL Hb** (או ~3% Hct)

**דימום מסיבי:**
🩸 עירוי רציף עד להשגת יציבות Hemodynamic + Hb מתאים

---

**🎯 התוויות:**

✅ **אנמיה סימפטומטית** (קוצר נשימה, טכיקרדיה, חולשה)
✅ **דימום פעיל** עם ירידה ב-Hb
✅ **Hb <7 g/dL** (בד"כ threshold בחולים יציבים)
✅ **Hb <8-10 g/dL** בחולים לא יציבים (לב, נשימה, neurologic)
✅ **Massive transfusion** (דימום מסיבי)
✅ **תלות בעירויים כרוניים** (תלסמיה, SCD, MDS)

---

**⏰ תדירות:**

**משך חיים:**
- **תאי דם אדומים עצמיים:** ~120 ימים
- **תאים לאחר עירוי:** ~60 ימים (תורם) + משתנה לפי המוליזה

**אחסון:**
- **1-42 ימים** (תלוי תמיסת אחסון)
- טמפרטורה: **1-6°C**

---

**✅ יתרונות:**

✅ **עליה מהירה ב-Hb** ובהובלת חמצן
✅ **משפר perfusion** רקמתי
✅ **מציל חיים בדימום** חמור

---

**⚠️ תופעות לוואי:**

**שכיחות:**
- **חום** (FNHTR - Febrile Non-Hemolytic Transfusion Reaction)
- **אלרגיה** (פריחה, גרד)
- **עומס ברזל** (Iron overload) - בעירויים כרוניים

**חמורות (נדירות):**
- **תגובה המוליטית חריפה** (Acute Hemolytic Transfusion Reaction - AHTR)
- **TRALI** (Transfusion-Related Acute Lung Injury)
- **TACO** (Transfusion-Associated Circulatory Overload)
- **היפרקלמיה** (בעירוי מהיר/מסיבי)
- **היפוקלצמיה** (ציטראט בשקית קושר Ca²⁺)
- **היפותרמיה** (בעירוי מסיבי)

---

**🚨 תגובה המוליטית חריפה (AHTR):**

**סיבה:**
שקית לא תואמת (ABO incompatibility) ← המוליזה תוך-וסקולרית

**סימנים:**
- **חום, צמרמורות**
- **כאבי גב/חזה**
- כאבי בטן
- **המוגלובינוריה** (שתן אדום/חום)
- **DIC**
- **אי-ספיקת כליות חריפה**
- **הלם**

**טיפול:**
🚨 **להפסיק עירוי מיידית!**
- תמיכה Hemodynamic
- דיאוריזה (נוזלים + Furosemide)
- ניטור כליות (אוריאה, קריאטינין)
- בדיקת שקית + דגימת דם מחולה
- DIC management במידת הצורך

---

**🚨 TACO (Circulatory Overload):**

**סיבה:**
עומס נוזלים ← אי-ספיקת לב

**סימנים:**
- קוצר נשימה
- טכיקרדיה
- היפרטנסיה
- JVD (גודש ורידים צווארי)
- אדמה ריאתית בצילום

**טיפול:**
- **Furosemide** (Lasix)
- חמצן
- הפחתת קצב עירוי
- ניטרטים במידת הצורך

---

**⚠️ זהירות:**

🚨 **ABO matching חובה!** טעות = המוליזה קטלנית
🚨 **Crossmatch:** תמיד לעשות (חוץ מחירום קיצוני)
🚨 **עירוי מהיר:** סיכון היפרקלמיה, היפוקלצמיה, היפותרמיה
🚨 **חימום דם:** בעירוי מסיבי (מניעת היפותרמיה)
🚨 **Iron overload:** בעירויים כרוניים (>20 units) ← Chelation (Deferoxamine, Deferasirox)

---

**⚠️ התוויות נגד יחסיות:**

❌ **אי-ספיקת לב לא מאוזנת** (סכנת TACO)
❌ **אנמיה כרונית סימפטומטית** ללא אינדיקציה חריפה

---

**💡 פנינים קליניות:**

💎 **Restrictive strategy:** Hb >7 g/dL מספיק ברוב החולים (TRICC trial)

💎 **Liberal strategy:** Hb >8-10 g/dL בחולים לא יציבים (לב, CVA, ACS)

💎 **10 ml/kg ≈ עליה 2 g/dL:** חישוב מהיר לילדים

💎 **1 unit ≈ עליה 1 g/dL:** חישוב מהיר למבוגרים

💎 **O negative = Universal donor:** לחירום (לא ידוע סוג דם)

💎 **AB positive = Universal recipient:** יכול לקבל הכל

💎 **Leukoreduction:** סינון לויקוציטים (מפחית FNHTR, CMV, HLA alloimmunization)

💎 **Irradiation:** חובה בחסרי חיסון (myeloma, BMT, premies) - מניעת TA-GVHD

💎 **Washed RBCs:** שטיפת תאים (מסיר פלזמה לחלוטין) - ל-IgA deficiency, PNH, אלרגיות חמורות

💎 **CMV-negative:** חשוב בפגים, BMT, חסרי חיסון

💎 **Massive transfusion protocol:** 1:1:1 ratio (PRBCs:FFP:PLT) בדימום מסיבי

💎 **Calcium:** בעירוי מסיבי, לתת Calcium (ציטראט קושר Ca²⁺)

💎 **חימום דם:** Blood warmer בעירוי מסיבי (מניעת היפותרמיה)

💎 **עירוי איטי:** במטופלים בסיכון TACO (אי-ספיקת לב, קשישים, ילדים)""",
            "order_index": 2
        },
        {
            "title": "פלזמה טרייה קפואה - Fresh Frozen Plasma (FFP)",
            "section_type": "text",
            "content": """**Fresh Frozen Plasma - פלזמה טרייה קפואה / FFP**

**תיאור:**
תוצר דם המכיל את כל גורמי הקרישה, אלבומין, ואימונוגלובולינים מפלזמה תקינה

---

**📊 מינון:**

**ילדים:**
🩸 **10-20 ml/kg**
- לתיקון קרישה: **10-15 ml/kg**
- Massive transfusion: **15-20 ml/kg**

**מבוגרים:**
🩸 **10-20 ml/kg** (או 2-4 units)
- 1 unit ≈ 250-300 ml

**עליה צפויה:**
- **10-15 ml/kg** ← עליה של **~20-30%** ברמות גורמי קרישה

---

**🎯 התוויות:**

✅ **דימום + קואגולופתיה** (INR >1.6, PTT מוארך)
✅ **Massive transfusion** (דימום מסיבי)
✅ **DIC** עם דימום
✅ **TTP** (Thrombotic Thrombocytopenic Purpura) - Plasma exchange
✅ **מחסור בגורמי קרישה מרובים** (כבד, Warfarin, ויטמין K)
✅ **פרוצדורה פולשנית** עם קואגולופתיה (INR >1.6)

---

**⏰ תדירות:**

**משך השפעה:**
- **גורמי קרישה:** זמן מחצית חיים משתנה
  - Factor VII: ~4-6 שעות (הקצר ביותר)
  - Factor II, IX, X: ~24-72 שעות

**ניטור:**
- **INR, PTT** לפני ואחרי
- **Fibrinogen** (אם נמוך)

---

**✅ יתרונות:**

✅ **מכיל כל גורמי הקרישה**
✅ **תיקון קואגולופתיה רב-גורמית**
✅ **חיוני בDIC, Massive transfusion**

---

**⚠️ תופעות לוואי:**

**שכיחות:**
- **עומס נוזלים** (TACO) - נפח גדול!
- **חום, צמרמורות** (FNHTR)
- **אלרגיה** (פריחה, אורטיקריה)

**חמורות (נדירות):**
- **TRALI** (Transfusion-Related Acute Lung Injury) - **FFP הגורם השכיח ביותר!**
- **אנפילקסיס** (במחסור IgA)
- **זיהומים** (viruses - נדיר מאוד כיום)
- **ציטראט-טוקסיות** (בעירוי מסיבי): היפוקלצמיה

---

**🚨 TRALI:**

**הגדרה:**
פגיעה ריאתית חריפה תוך **6 שעות** מעירוי FFP

**סיבה:**
נוגדנים בפלזמה של תורם ← פעילות לויקוציטים ← פגיעה ריאתית

**סימנים:**
- **קוצר נשימה חמור**
- **היפוקסמיה**
- **אדמה ריאתית דו-צדדית** (בצילום)
- **חום**
- **היפוטנסיה** (לפעמים)

**טיפול:**
- **תמיכה נשימתית** (חמצן, אוורור מכני)
- הפסקת עירוי
- supportive care
- **לא דיאורטיקה!** (לא עומס נוזלים)

**מניעה:**
- FFP ממתרימות גברים (פחות נוגדנים)

---

**⚠️ זהירות:**

🚨 **עומס נוזלים:** נפח גדול (10-20 ml/kg) ← סכנת TACO
🚨 **TRALI:** FFP הגורם השכיח ביותר
🚨 **ABO matching רצוי** (לא הכרחי כמו ב-PRBCs)
🚨 **ציטראט:** בעירוי מסיבי ← היפוקלצמיה. לתת Calcium!
🚨 **הפשרה:** לוקחת זמן (~30-45 דקות). לתכנן מראש!

---

**⚠️ התוויות נגד יחסיות:**

❌ **אי-ספיקת לב לא מאוזנת** (סכנת TACO)
❌ **קואגולופתיה ללא דימום/פרוצדורה** (אין אינדיקציה)
❌ **מחסור בגורם בודד** (עדיף concentrate ספציפי)

---

**💡 פנינים קליניות:**

💎 **מתי לתת:** דימום + INR >1.6 או PTT מוארך. או פרוצדורה + INR >1.6

💎 **לא לתיקון INR ללא דימום:** FFP לא מתאים רק לתיקון מספר

💎 **Massive transfusion:** יחס **1:1:1** (PRBCs:FFP:PLT) = אופטימלי

💎 **Reversal Warfarin:** FFP + Vitamin K. אם דימום מסכן חיים: PCC (Prothrombin Complex Concentrate) מהיר יותר

💎 **TTP:** FFP בplasma exchange (החלפת פלזמה) = טיפול עיקרי

💎 **10-15 ml/kg מספיק:** לתיקון קואגולופתיה קלה-בינונית

💎 **ABO matching לא הכרחי:** אך עדיף (פחות תגובות)

💎 **AB plasma = Universal donor:** יכול לתת לכולם

💎 **הפשרה 30-45 דקות:** לתכנן מראש! אין זמן בחירום

💎 **תקף 24 שעות:** לאחר הפשרה (אם שומרים ב-1-6°C)

💎 **Calcium supplement:** בעירוי מסיבי FFP, לתת Calcium (ציטראט קושר Ca²⁺)

💎 **לא מרחיב נפח:** FFP לא לשימוש כמרחיב נפח! (יש Albumin, Crystalloid לזה)

💎 **מחסור IgA:** חולים עם IgA deficiency ← סכנת אנפילקסיס. השתמש בwashed plasma""",
            "order_index": 3
        },
        {
            "title": "גרנולוציטים - Granulocytes",
            "section_type": "text",
            "content": """**Granulocytes - גרנולוציטים / White Blood Cells Transfusion**

**תיאור:**
תוצר דם המכיל לויקוציטים (בעיקר neutrophils) מתורם, לטיפול בזיהומים חמורים בנויטרופניה

---

**📊 מינון:**

**ילדים ומבוגרים:**
🩸 **10 ml/kg** (או 1 unit ממבוגר)
- כל unit מכיל ≥ **1×10¹⁰ גרנולוציטים**

**תדירות:**
🩸 **יומי** (או כל 48 שעות) עד לשיפור קליני או עליית ANC

---

**🎯 התוויות:**

✅ **נויטרופניה חמורה** (ANC <500/µL) + **זיהום מסכן חיים** לא מגיב לאנטיביוטיקה
✅ **Sepsis** בנויטרופניה עמוקה (ANC <100/µL)
✅ **Fungal infection** חמור בנויטרופניה
✅ **CGD** (Chronic Granulomatous Disease) עם זיהום לא מגיב
✅ **חוסר ייצור מח עצם זמני** (כימותרפיה, BMT) עם זיהום חמור

---

**⏰ תדירות:**

**משך חיים:**
- **גרנולוציטים לאחר עירוי:** **<24 שעות** (חיים קצרים מאוד!)
- לכן: עירויים **יומיים**

**ניטור:**
- **ANC** יומי
- **סימנים חיוניים** (חום, לחץ דם)
- **תרביות** (blood, urine, etc.)

---

**✅ יתרונות (תיאורטיים):**

✅ **תמיכה חיסונית זמנית**
✅ **לחימה בזיהום** בנויטרופניה

---

**⚠️ תופעות לוואי:**

**שכיחות מאוד:**
- **חום, צמרמורות** (כמעט תמיד!)
- **היפוטנסיה**
- **קוצר נשימה, Dyspnea**
- **אלרגיה**

**חמורות:**
- **TRALI** (Transfusion-Related Acute Lung Injury)
- **Pulmonary reactions** (distress נשימתי חמור)
- **אלואימוניזציה** (נוגדנים ← אי-תגובה)
- **CMV transmission** (אם תורם CMV+)
- **TA-GVHD** (Transfusion-Associated GVHD) - נדיר אך קטלני

---

**🚨 TA-GVHD:**

**הגדרה:**
לויקוציטים של תורם תוקפים רקמות מטופל (חסר חיסון)

**סימנים:**
- פריחה
- שלשולים
- הפטיטיס
- פנציטופניה
- קטלני ב->90%

**מניעה:**
🚨 **חובה להקרין גרנולוציטים!** (Irradiation 25 Gy) - הורג לימפוציטים

---

**⚠️ זהירות:**

🚨 **Irradiation חובה!** (מניעת TA-GVHD)
🚨 **תגובות ריאתיות:** שכיחות! ניטור צמוד במהלך עירוי
🚨 **CMV-negative:** עדיף בחולים CMV-negative (או leukoreduced)
🚨 **HLA matching:** עדיף (מפחית תגובות)
🚨 **לא לשלב עם Amphotericin B:** סיכון גבוה לפגיעה ריאתית חמורה!

---

**⚠️ התוויות נגד:**

❌ **נויטרופניה כרונית ללא זיהום פעיל**
❌ **זיהום מגיב לאנטיביוטיקה**
❌ **פרוגנוזה גרועה מאוד** (אין תועלת)

---

**💡 פנינים קליניות:**

💎 **שימוש נדיר:** גרנולוציטים נדירים מאוד בשימוש (סיבוכים רבים, יעילות לא מוכחת)

💎 **Amphotericin B = התווית נגד:** אסור לשלב! (פגיעה ריאתית חמורה)

💎 **חום תמיד:** כמעט כל מטופל מפתח חום. Premedication (פרצטמול, אנטיהיסטמין)

💎 **Irradiation 25 Gy חובה:** מניעת TA-GVHD (קטלני!)

💎 **יומי:** גרנולוציטים חיים <24 שעות ← צריך עירוי יומי

💎 **ANC >500:** מטרה - להגיע ל-ANC >500/µL + שיפור קליני

💎 **G-CSF לתורם:** תורמים מקבלים G-CSF לפני תרומה (mobilization של גרנולוציטים)

💎 **אלטרנטיבות עדיפות:** G-CSF למטופל, אנטיביוטיקה רחבה, פטריות ייעודיות

💎 **Controversial:** יעילות גרנולוציטים שנויה במחלוקת. אין מחקרים גדולים מוצקים

💎 **Last resort:** גרנולוציטים = אופציה אחרונה, כשהכל נכשל

💎 **CGD:** בחולי CGD (Chronic Granulomatous Disease), גרנולוציטים יעילים יותר (הם תקינים)

💎 **הערה:** השימוש בגרנולוציטים ירד מאוד עם השיפור ב-G-CSF, אנטיביוטיקה, אנטי-פטריות""",
            "order_index": 4
        },
        {
            "title": "נקודות מפתח - תוצרי דם",
            "section_type": "text",
            "content": """**🎯 נקודות מפתח:**

✅ **טסיות (PLT):** 10-20 ml/kg. Threshold: <10K (מניעה), <50K (ניתוח), <100K (נוירוכירורגיה)

✅ **קריופרסיפיטט (Cryo):** 1-2 units/10kg. עשיר בFibrinogen. יעיל לHypofibrinogenemia (<100 mg/dL)

✅ **תאי דם אדומים (PRBCs):** 10-15 ml/kg. עליה ~2-3 g/dL Hb. Threshold: Hb <7 g/dL (יציב), <8-10 (לא יציב)

✅ **פלזמה טרייה (FFP):** 10-20 ml/kg. כל גורמי קרישה. מתי: INR >1.6 + דימום/פרוצדורה

✅ **גרנולוציטים:** 10 ml/kg יומי. נדיר! ANC <500 + זיהום מסכן חיים לא מגיב. Irradiation חובה!

✅ **Massive transfusion:** יחס 1:1:1 (PRBCs:FFP:PLT) אופטימלי

✅ **ABO matching:** קריטי ב-PRBCs (המוליזה קטלנית!), רצוי באחרים

✅ **Leukoreduction:** סינון לויקוציטים (מפחית FNHTR, CMV, HLA)

✅ **Irradiation:** חובה בחסרי חיסון (BMT, premies, Granulocytes) - מניעת TA-GVHD

✅ **CMV-negative:** חשוב בפגים, BMT, חסרי חיסון""",
            "order_index": 5
        },
        {
            "title": "אזהרות קריטיות",
            "section_type": "text",
            "content": """**🚨 אזהרות חשובות:**

🔴 **ABO mismatch (PRBCs):** המוליזה קטלנית! חום, כאבי גב, המוגלובינוריה, DIC, אי-ספיקת כליות

🔴 **TRALI:** פגיעה ריאתית חריפה תוך 6 שעות. קוצר נשימה, היפוקסמיה, אדמה ריאתית. FFP הגורם השכיח!

🔴 **TACO:** עומס נוזלים ← אי-ספיקת לב. קוצר נשימה, JVD, אדמה ריאתית. טיפול: Furosemide

🔴 **TA-GVHD:** לויקוציטים של תורם תוקפים מטופל. קטלני >90%! מניעה: Irradiation (חובה בחסרי חיסון, גרנולוציטים)

🔴 **היפרקלמיה:** בעירוי מהיר/מסיבי PRBCs. ניטור K⁺, ECG

🔴 **היפוקלצמיה:** ציטראט בשקיות קושר Ca²⁺. בעירוי מסיבי FFP/PRBCs - לתת Calcium!

🔴 **היפותרמיה:** עירוי מסיבי. להשתמש בBlood warmer!

🔴 **Iron overload:** עירויים כרוניים >20 units. Chelation (Deferoxamine, Deferasirox)

🔴 **PLT dysfunction:** ITP, TTP, HIT - זהירות בעירוי טסיות (עלול להחמיר!)

🔴 **גרנולוציטים + Amphotericin B:** אסור לחלוטין! פגיעה ריאתית חמורה

🔴 **גרנולוציטים ללא Irradiation:** TA-GVHD קטלני! Irradiation 25 Gy חובה""",
            "order_index": 6
        },
        {
            "title": "פנינים קליניות",
            "section_type": "text",
            "content": """**💎 פנינים קליניות:**

💎 **Restrictive transfusion:** Hb >7 g/dL מספיק ברוב החולים (TRICC trial). Liberal (Hb >8-10) רק בלא יציבים

💎 **10-15 ml/kg PRBCs ≈ עליה 2-3 g/dL Hb:** חישוב מהיר לילדים. 1 unit ≈ 1 g/dL במבוגרים

💎 **O negative = Universal donor RBCs:** לחירום (סוג דם לא ידוע)

💎 **AB plasma = Universal donor FFP:** יכול לתת לכולם

💎 **Massive transfusion protocol (MTP):** 1:1:1 ratio (PRBCs:FFP:PLT) = אופטימלי בדימום מסיבי

💎 **Calcium בעירוי מסיבי:** ציטראט בשקיות קושר Ca²⁺ ← להוסיף Calcium Gluconate!

💎 **Blood warmer:** חובה בעירוי מסיבי (מניעת היפותרמיה)

💎 **Crossmatch time:** ~45 דקות (Type & Screen ~15 דקות). לתכנן מראש!

💎 **PLT 1h post-transfusion count:** מדד ליעילות. אם אין עליה ← Refractoriness (נוגדנים)

💎 **Cryo יעיל מFFP:** לתיקון Fibrinogen, Cryo מרוכז יותר (פחות נפח, מהיר יותר)

💎 **Fibrinogen threshold:** <100 mg/dL + דימום ← Cryo. <50 mg/dL מניעתי

💎 **FFP לא לתיקון INR לבד:** רק אם דימום או פרוצדורה. אחרת: Vitamin K

💎 **PCC מהיר מFFP:** Prothrombin Complex Concentrate (PCC) לreversal Warfarin מהיר יותר (אך יקר)

💎 **Washed RBCs:** שטיפת תאים (מסיר פלזמה) ל-IgA deficiency, אלרגיות חמורות חוזרות

💎 **Irradiated products:** חובה ב-BMT, Hodgkin's, חסרי חיסון מולדים, גרנולוציטים (מניעת TA-GVHD)

💎 **CMV-negative vs Leukoreduced:** CMV-negative עדיף בפגים <1200g, BMT. Leukoreduced מפחית 90% CMV

💎 **Premedication:** פרצטמול + אנטיהיסטמין לפני עירוי (מפחית FNHTR, אלרגיות)

💎 **חום פוסט-עירוי:** שכיח (FNHTR). אם >1°C או חוזר ← בדיקת Hemolysis, תרבית שקית

💎 **גרנולוציטים נדירים:** שימוש ירד עם G-CSF. אופציה אחרונה (יעילות לא מוכחת, סיבוכים רבים)""",
            "order_index": 7
        }
    ]
    
    # הוספת כל המקטעים
    print(f"\n📚 מוסיף {len(sections)} מקטעים...")
    
    for idx, section_data in enumerate(sections, 1):
        section_data['topic_id'] = topic_id
        
        section = create_content_section(section_data)
        
        if section:
            print(f"   ✅ מקטע {idx}/{len(sections)}: {section_data['title']}")
        else:
            print(f"   ❌ שגיאה במקטע {idx}: {section_data['title']}")
            return False
    
    return True

if __name__ == "__main__":
    print("="*60)
    print("🩸 הוספת תוכן: תוצרי דם")
    print("="*60)
    
    try:
        success = add_blood_products()
        
        if success:
            print("\n🎉 הושלם בהצלחה!")
            print("\n💡 התוכן כולל:")
            print("   - טסיות (Platelets)")
            print("   - קריופרסיפיטט (Cryoprecipitate)")
            print("   - תאי דם אדומים (PRBCs)")
            print("   - פלזמה טרייה (FFP)")
            print("   - גרנולוציטים (Granulocytes)")
        else:
            print("\n❌ הייתה בעיה בהוספת התוכן")
    
    except Exception as e:
        print(f"\n❌ שגיאה: {e}")
        import traceback
        traceback.print_exc()
