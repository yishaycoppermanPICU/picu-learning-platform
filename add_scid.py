#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
הוספת תוכן: SCID - Severe Combined Immunodeficiency
"""

from utils.database import init_supabase, create_content_item, create_content_section

def add_scid_content():
    """הוספת נושא SCID עם כל המקטעים"""
    
    print("🔄 מתחבר למסד הנתונים...")
    supabase = init_supabase()
    
    if not supabase:
        print("❌ שגיאה בחיבור למסד נתונים")
        return False
    
    print("✅ חיבור הצליח!")
    
    # יצירת הנושא הראשי
    print("\n📝 יוצר נושא: SCID...")
    
    topic_data = {
        "title": "SCID - חוסר חיסוני משולב חמור",
        "category": "immunology",
        "description": "מחלה חיסונית חמורה עם פגיעה בתאי T, B ולעיתים NK - אמצעי הגנה, טיפול פרופילקטי והשתלת מח עצם",
        "icon": "🛡️",
        "slug": "scid_management",
        "tags": ["אימונולוגיה", "SCID", "חוסר חיסוני", "השתלת מח עצם", "בידוד", "זיהומים"],
        "order_index": 30
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
            "title": "הגדרה - SCID",
            "section_type": "text",
            "content": """**Severe Combined Immunodeficiency (SCID)**

מחלה הנגרמת ממוטציה בגנים האחראים על התפתחות תקינה של מערכת החיסון:

**פגיעה בתאים:**
- **תאי T** - פגיעה תמיד
- **תאי B** - פגיעה תמיד (ישירה או עקיפה)
- **תאי NK** (Natural Killers) - פגיעה ב-50% מהמקרים

💡 **חשוב:** לעיתים הפגיעה תהיה בתאי T בלבד, אך תהיה השפעה גם על תאי B כי כדי לפעול הם צריכים לקבל סיגנל מתאי T.

⚠️ **דחיפות:** מרגע שילד אובחן עם SCID, יש לנקוט באמצעי הגנה במהירות האפשרית.""",
            "order_index": 0
        },
        {
            "title": "אמצעי הגנה לילד עם SCID",
            "section_type": "text",
            "content": """ילדים שאובחנו עם SCID צריכים הגנה מקסימלית עד לקבלת טיפול דפיניטיבי:""",
            "order_index": 1
        },
        {
            "title": "1. בידוד",
            "section_type": "alert",
            "content": """🛡️ **בידוד חובה**

ילדים עם SCID צריכים לשהות בבידוד עד לקבלת טיפול דפיניטיבי וייצור תאי T.""",
            "order_index": 2
        },
        {
            "title": "2. הימנעות מחיסון חי מוחלש",
            "section_type": "alert",
            "content": """⚠️ **איסור חיסונים חיים**

- אין לתת חיסון חי מוחלש לילד
- אין לתת חיסון חי מוחלש לקרובי משפחה

**יוצא מן הכלל:** מקרים בהם כבר ניתן חיסון ולא התפתח זיהום""",
            "order_index": 3
        },
        {
            "title": "3. מוצרי דם",
            "section_type": "steps",
            "content": "כל מוצרי הדם חייבים להיות:",
            "metadata": {
                "steps": [
                    "מוקרנים ☢️",
                    "מסוננים",
                    "שליליים ל-CMV"
                ]
            },
            "order_index": 4
        },
        {
            "title": "4. הנקה",
            "section_type": "alert",
            "content": """⚠️ **זהירות עם הנקה**

אם לאם ישנם נוגדנים מסוג **IgG או IgM ל-CMV** - יש להימנע מהנקה.

💡 **CMV וזיהומים ויראליים הם הסיבות השכיחות ביותר למוות בילדי SCID**""",
            "order_index": 5
        },
        {
            "title": "5. טיפול פרופילקטי",
            "section_type": "list",
            "content": """**תרופות מניעתיות חובה:**

- **IVIG** - אימונוגלובולינים תוך ודריים
- **רספרים מניעתי** - נגד *P. jirovecii* pneumonia
- **פלוקנזול** - נגד זיהומים פטרייתיים
- **פליויזומב** - נוגדנים ל-RSV (רק בתקופה עם זיהום נפוץ של RSV)
- **אציקלוויר או אנטי-ויראלי אחר** - בעיקר נגד משפחת ה"הרפס", במיוחד אם האמא הייתה נשאית ל-HSV""",
            "order_index": 6
        },
        {
            "title": "טיפול דפיניטיבי - HCT",
            "section_type": "text",
            "content": """**השתלת מח עצם (Hematopoietic Cell Transplantation - HCT)**

הטיפול הדפיניטיבי היחיד הוא השתלת מח עצם מתורם מתאים.

⚠️ **חשוב להדגיש:** גם לאחר השתלת מח עצם, לוקח זמן עד שתאי T מתחדשים.

**הזיהומים השכיחים ביותר הגורמים למוות לאחר השתלה:**
- CMV (Cytomegalovirus)
- EBV (Epstein-Barr Virus)
- Adenovirus (אדנו וירוס)""",
            "order_index": 7
        },
        {
            "title": "פרוגנוזה",
            "section_type": "text",
            "content": """**ללא טיפול:** המחלה סופנית 💔

**עם טיפול מוקדם:**
📊 מחקרים הראו שבילדים מתחת גיל **3.5 חודשים** שלא נדבקו בזיהום והושתלו במח עצם:

✅ **סיכויי הישרדות: 96%**

💡 **מסקנה:** אבחון מוקדם וטיפול מיידי מציל חיים!""",
            "order_index": 8
        },
        {
            "title": "ילדי SCID במחלקה",
            "section_type": "text",
            "content": """**מצגת קלינית במחלקה:**

ילדי SCID מתייצגים בדרך כלל ב**ספסיס**.

**הטיפול:**
- כמו כל טיפול לספסיס
- פוש **מרופנם** 20 מ״ג/ק״ג
- מתן **אדרנלין** לפי צורך

**או:**
- השגחה לאחר השתלת מח עצם

📖 *פירוט נוסף על טיפול בספסיס בנושא נפרד*""",
            "order_index": 9
        },
        {
            "title": "נקודות מפתח",
            "section_type": "alert",
            "content": """📋 **עיקרי הדברים:**

🛡️ **בידוד מיידי** מרגע האבחון

⚠️ **אסור:**
- חיסונים חיים (לילד ולמשפחה)
- מוצרי דם לא מוקרנים
- הנקה אם האם CMV חיובית

💊 **טיפול פרופילקטי:**
- IVIG + רספרים + פלוקנזול + אציקלוויר

🏥 **טיפול דפיניטיבי:**
- השתלת מח עצם בלבד

⚡ **זיהומים קטלניים:**
- CMV, EBV, Adenovirus

✅ **פרוגנוזה מצוינת** אם מטפלים לפני 3.5 חודשים ללא זיהום (96% הישרדות)""",
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
    print(f"   נושא: SCID - חוסר חיסוני משולב חמור")
    print(f"   קטגוריה: אימונולוגיה")
    print(f"   מקטעים: {len(sections)}")
    print(f"   ID: {topic_id}")
    
    return True

if __name__ == "__main__":
    print("🛡️ PICU Learning Platform - הוספת תוכן")
    print("="*60)
    print("נושא: SCID - Severe Combined Immunodeficiency")
    print("="*60)
    
    try:
        success = add_scid_content()
        
        if success:
            print("\n🎉 הושלם בהצלחה!")
            print("\n💡 התוכן כולל:")
            print("   - הגדרה ופתופיזיולוגיה")
            print("   - אמצעי הגנה מלאים")
            print("   - טיפול פרופילקטי")
            print("   - השתלת מח עצם")
            print("   - פרוגנוזה")
            print("   - ניהול במחלקה")
        else:
            print("\n❌ הייתה בעיה בהוספת התוכן")
    
    except Exception as e:
        print(f"\n❌ שגיאה: {e}")
        import traceback
        traceback.print_exc()
