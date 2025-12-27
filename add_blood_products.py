#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
הוספת תוכן: מתן מוצרי דם
"""

from utils.database import init_supabase, create_content_item, create_content_section

def add_blood_products_content():
    """הוספת נושא מתן מוצרי דם עם כל המקטעים"""
    
    print("🔄 מתחבר למסד הנתונים...")
    supabase = init_supabase()
    
    if not supabase:
        print("❌ שגיאה בחיבור למסד נתונים")
        return False
    
    print("✅ חיבור הצליח!")
    
    # יצירת הנושא הראשי
    print("\n📝 יוצר נושא: מתן מוצרי דם...")
    
    topic_data = {
        "title": "מתן מוצרי דם",
        "category": "hematology",
        "description": "פרוטוקולים למתן מוצרי דם: טסיות, תאי דם אדומים, פלזמה, קריופרציפיטט וגרנולוציטים",
        "icon": "🩸",
        "slug": "blood_products_administration",
        "tags": ["המטולוגיה", "מוצרי דם", "טסיות", "דם", "פלזמה", "נהלים"],
        "order_index": 20
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
            "title": "טסיות (PLT - Platelets)",
            "section_type": "text",
            "content": """**התוויות למתן:**
- טרומבוציטופניה מתחת ל-10,000
- מתן פרופילקטי בילדים עם לויקמיה
- לאחר כימותרפיה
- לאחר השתלת מח עצם
- אנמיה אפלסטית
- טרומבוציטופניה אימונית
- TTP או HIT

**מינון:** 5 מ״ל/ק״ג

**תוקף:** עד 5 ימים מרגע ההנפקה (מאוחסנות באוויר חדר)""",
            "order_index": 0
        },
        {
            "title": "טסיות - דרך מתן וניטור",
            "section_type": "steps",
            "content": "פרוטוקול מתן טסיות:",
            "metadata": {
                "steps": [
                    "חייבת הקרנה לפני מתן ⚠️",
                    "מתן בעזרת מזרק פאמפ + פילטר טרומבוציטים",
                    "⚠️ אין לתת דרך IVAC - דחיפת הנוזל דרך הצינור הורסת את הטרומבוציטים",
                    "ניטור המטופל בתחילת המתן",
                    "ניטור המטופל בסיום המתן"
                ]
            },
            "order_index": 1
        },
        {
            "title": "Packed RBCs (PC - תאי דם אדומים מרוכזים)",
            "section_type": "text",
            "content": """**תיאור:** מנה של 250 מ״ל עם מעט מאוד פלזמה, המטוקריט 70% (מאוד מרוכזת)

**התוויה:** המוגלובין נמוך

**מינון:** לפי צורך קליני

**משך מתן:** 
- מקסימום 4 שעות
- בדרך כלל 2 שעות
- ניתן לתת במהירות במידת הצורך

**תוקף:** 35 ימים

⚠️ **חייבת הקרנה לפני מתן**""",
            "order_index": 2
        },
        {
            "title": "Packed RBCs - דרך מתן וניטור",
            "section_type": "steps",
            "content": "פרוטוקול מתן PC:",
            "metadata": {
                "steps": [
                    "מתן דרך IVAC",
                    "שימוש בסט המיועד למנת דם עם פילטר",
                    "ניטור: איש צוות ישגיח על המטופל ב-5 הדקות הראשונות ויתעד סימנים",
                    "מדידת סימנים: בתחילת מתן → לאחר 15 דקות → לאחר שעה → לאחר שעתיים",
                    "מעקב אחר המטופל במשך העירוי ובסיומו לזיהוי תגובות אפשריות"
                ]
            },
            "order_index": 3
        },
        {
            "title": "FFP (Fresh Frozen Plasma - פלזמה טרייה קפואה)",
            "section_type": "text",
            "content": """**תיאור:** נפח 200 מ״ל, המנה מכילה את כל חלבוני הקרישה

**התוויות:**
- חוסר בפקטורי קרישה בגלל מחלות כבד
- דימום מסיבי
- DIC (קרישה תוך-וסקולרית מפושטת)
- אנטידוט לוורפרין
- TTP (פורפורה טרומבוציטופנית טרומבוטית)
- חסר מולד בחלבוני קרישה (פקטור 9/פקטור 11)

**תוקף:**
- בהקפאה של -20°C: עד שנה
- לאחר הפשרה מבוקרת: עד 5 ימים ב-4°C
- ניתן להקפיא שוב עד 24 שעות מרגע ההפשרה

✅ **אין צורך בהקרנה**""",
            "order_index": 4
        },
        {
            "title": "FFP - התאמת סוג דם",
            "section_type": "alert",
            "content": """⚠️ **דגש חשוב - אנטיגנים בפלזמה:**

- פלזמה מסוג **A**: יש אנטי-B
- פלזמה מסוג **B**: יש אנטי-A
- פלזמה מסוג **O**: יש אנטי-A ואנטי-B
- פלזמה מסוג **AB**: אין אנטיגנים - **Universal donor**

💡 **מנת פלזמה מסוג AB ניתנת לכל מטופל שלא ידוע סוג דמו**""",
            "order_index": 5
        },
        {
            "title": "FFP - דרך מתן וניטור",
            "section_type": "steps",
            "content": "פרוטוקול מתן FFP:",
            "metadata": {
                "steps": [
                    "מתן דרך IVAC או פאמפ",
                    "דרך סט עם פילטר דם",
                    "ניטור כמו במתן דם רגיל",
                    "מעקב אחר תגובות אפשריות"
                ]
            },
            "order_index": 6
        },
        {
            "title": "Cryoprecipitate (CRYO - קריופרציפיטט)",
            "section_type": "text",
            "content": """**תיאור:** מוצר דם שמקורו בפלזמה

**מכיל:**
- פיברינוגן (פקטור I)
- פקטור VIII
- פקטור XIII
- פקטור פון וילברנד
- פיברונקטין

**התוויות:**
- מחסור בפקטור 8
- מחסור בפיברינוגן
- מצבי דמם חריפים

**תוקף:**
- מנה מוקפאת ב-20°C: שנה שלמה
- לאחר הפשרה: 6 שעות בלבד ⚠️""",
            "order_index": 7
        },
        {
            "title": "Cryoprecipitate - דרך מתן",
            "section_type": "steps",
            "content": "פרוטוקול מתן CRYO:",
            "metadata": {
                "steps": [
                    "מתן דרך IVAC או פאמפ",
                    "עם פילטר דם",
                    "ניטור המטופל בתחילת המתן",
                    "ניטור המטופל בסיום המתן"
                ]
            },
            "order_index": 8
        },
        {
            "title": "Granulocytes (גרנולוציטים)",
            "section_type": "text",
            "content": """**התוויה:** הוראה של המטואונקולוג בלבד

**דרך מתן:** IVAC **ללא פילטר** ⚠️

💡 **סיבה:** גרנולוציטים נתקעים בפילטר דם, לכן אין להשתמש בפילטר""",
            "order_index": 9
        },
        {
            "title": "נקודות מפתח",
            "section_type": "alert",
            "content": """📋 **סיכום עיקרי:**

**טסיות:**
- ⚠️ רק פאמפ, לא IVAC
- חובה הקרנה
- תוקף: 5 ימים

**PC (דם):**
- חובה הקרנה
- מתן עד 4 שעות
- ניטור צמוד

**FFP (פלזמה):**
- AB = Universal donor
- אין צורך בהקרנה
- תוקף: שנה בהקפאה

**CRYO:**
- תוקף: 6 שעות בלבד לאחר הפשרה ⚠️

**Granulocytes:**
- ⚠️ ללא פילטר!
- רק לפי הוראת המטואונקולוג""",
            "order_index": 10
        }
    ]
    
    print(f"\n📑 מוסיף {len(sections)} מקטעים...")
    
    for idx, section in enumerate(sections, 1):
        section['topic_id'] = topic_id
        result = create_content_section(section)
        
        if result:
            print(f"  ✅ {idx}. {section['title']}")
        else:
            print(f"  ❌ {idx}. {section['title']} - נכשל")
    
    print("\n" + "="*60)
    print("✅ התוכן נוסף בהצלחה למסד הנתונים!")
    print("="*60)
    print(f"\n📊 סיכום:")
    print(f"   נושא: מתן מוצרי דם")
    print(f"   קטגוריה: המטולוגיה")
    print(f"   מקטעים: {len(sections)}")
    print(f"   ID: {topic_id}")
    
    return True

if __name__ == "__main__":
    print("🩸 PICU Learning Platform - הוספת תוכן")
    print("="*60)
    print("נושא: מתן מוצרי דם")
    print("="*60)
    
    try:
        success = add_blood_products_content()
        
        if success:
            print("\n🎉 הושלם בהצלחה!")
            print("\n💡 התוכן כולל:")
            print("   - טסיות (PLT)")
            print("   - תאי דם אדומים (PC)")
            print("   - פלזמה (FFP)")
            print("   - קריופרציפיטט (CRYO)")
            print("   - גרנולוציטים")
        else:
            print("\n❌ הייתה בעיה בהוספת התוכן")
    
    except Exception as e:
        print(f"\n❌ שגיאה: {e}")
        import traceback
        traceback.print_exc()
