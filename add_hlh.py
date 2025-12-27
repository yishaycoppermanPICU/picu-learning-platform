#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
הוספת תוכן: HLH - Hemophagocytic Lymphohistiocytosis
"""

from utils.database import init_supabase, create_content_item, create_content_section

def add_hlh_content():
    """הוספת נושא HLH עם כל המקטעים"""
    
    print("🔄 מתחבר למסד הנתונים...")
    supabase = init_supabase()
    
    if not supabase:
        print("❌ שגיאה בחיבור למסד נתונים")
        return False
    
    print("✅ חיבור הצליח!")
    
    # יצירת הנושא הראשי
    print("\n📝 יוצר נושא: HLH...")
    
    topic_data = {
        "title": "HLH - המופגוציטיק לימפוהיסטיאוציטוזיס",
        "category": "hematology",
        "description": "סינדרום אגרסיבי ומסכן חיים עם פעילות יתר של מערכת החיסון - אבחון מהיר וטיפול קריטי",
        "icon": "⚡",
        "slug": "hlh_syndrome",
        "tags": ["המטולוגיה", "אונקולוגיה", "HLH", "מערכת חיסון", "ציטוקינים", "חירום"],
        "order_index": 40
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
            "title": "הגדרה - HLH",
            "section_type": "text",
            "content": """**Hemophagocytic Lymphohistiocytosis (HLH)**

סינדרום אגרסיבי ומסכן חיים המאופיין ב**פעילות יתר של מערכת החיסון**.

**אפידמיולוגיה:**
- נפוץ בעיקר אצל ילדים עד גיל **שנה וחצי**
- יכול להופיע בכל הגילאים

**סיבות:**
- על רקע גנטי/משפחתי
- באקראיות ללא סיבה ברורה

⚠️ **האתגר הגדול:** זיהוי המחלה
- המחלה נדירה מאוד
- התייצגות קלינית וריאבילית
- מחסור בממצאים קלינים ולבורטורים ספציפיים

⏰ **טיפול מהיר הינו קריטי!**""",
            "order_index": 0
        },
        {
            "title": "התאים המעורבים",
            "section_type": "text",
            "content": """התגובה האימונית המוגזמת ב-HLH מערבת שני סוגי תאים עיקריים:""",
            "order_index": 1
        },
        {
            "title": "מקרופגים",
            "section_type": "text",
            "content": """**תפקיד תקין:** תאים האחראיים בעיקר על הצגת אנטיגנים

**ב-HLH:**
- ⚡ משופעלים ביתר
- מפרישים כמות מוגברת של ציטוקינים
- מגבירים את התגובה החיסונית שכבר קיימת

→ **יוצרים מעגל של פעילות יתר**""",
            "order_index": 2
        },
        {
            "title": "תאי NK ולימפוציטים ציטוטוקסיים",
            "section_type": "text",
            "content": """**תפקיד תקין:** חיסול תאים נגועים או לא תקינים

**ב-HLH:**
- ⚡ פעילות מוגברת ולא מבוקרת
- תורמים להרס רקמות""",
            "order_index": 3
        },
        {
            "title": "טריגרים נפוצים ל-HLH",
            "section_type": "list",
            "content": """**הגורמים המעוררים את ההתפרצות:**

**זיהומים ויראליים** 🦠 (הנפוץ ביותר)
- EBV (Epstein-Barr Virus)
- CMV
- HSV
- HHV6
- Parvovirus

**מחלות ראומטיות** 🔥

**ממאירות לימפואידית** 🎗️

💡 **חשוב:** במטופלים עם ממאירות המטולוגית, הטיפול יכלול גם כימותרפיה והשתלת מח עצם.""",
            "order_index": 4
        },
        {
            "title": "טיפול במטופלים יציבים",
            "section_type": "text",
            "content": """**עקרונות הטיפול:**
1. טיפול בטריגר במהירות האפשרית
2. טיפול סטרואידלי
3. מעקב צמוד אחר החולה""",
            "order_index": 5
        },
        {
            "title": "בדיקות זיהומיות - מטופלים יציבים",
            "section_type": "steps",
            "content": "יש לבדוק רשימה של זיהומים נפוצים אפשריים:",
            "metadata": {
                "steps": [
                    "EBV (Epstein-Barr Virus)",
                    "CMV (Cytomegalovirus)",
                    "HSV (Herpes Simplex Virus)",
                    "HHV6 (Human Herpesvirus 6)",
                    "Parvovirus",
                    "ברטונלה (Bartonella)",
                    "לישמאניאזיס (Leishmaniasis)",
                    "תרבית לחיידקים",
                    "תרבית לפטריות"
                ]
            },
            "order_index": 6
        },
        {
            "title": "טיפול אנטי-מיקרוביאלי - מטופלים יציבים",
            "section_type": "text",
            "content": """**שיקולים לטיפול לפי הזיהום שאובחן:**

- 💊 **אנטיביוטי** - לזיהומים חיידקיים
- 💊 **אנטי-ויראלי** - לזיהומים ויראליים
- 💊 **אנטי-פוגאלי** - לזיהומים פטרייתיים
- 💊 **אנטי-טפילי** - לזיהומים טפיליים

⚠️ **טיפול ספציפי ל-EBV:**
במידה והחולה מאובחן עם EBV - **הטיפול הדפיניטיבי הוא ריטוקסימב (Rituximab)**""",
            "order_index": 7
        },
        {
            "title": "טיפול במטופלים לא יציבים",
            "section_type": "alert",
            "content": """⚡ **דחיפות קיצונית!**

**אין זמן לחכות לתוצאות מעבדה**

לא ניתן לחכות לתוצאות כדי להתאים טיפול לטריגר.

→ **יש להתחיל מייד טיפול דפיניטיבי ב-HLH**""",
            "order_index": 8
        },
        {
            "title": "פרוטוקול טיפול - מטופלים לא יציבים",
            "section_type": "options",
            "content": "הטיפול הדפיניטיבי ב-HLH:",
            "metadata": {
                "options": [
                    {
                        "title": "טיפול סיסטמי",
                        "description": "**אטופוזיד (Etoposide)** - תרופה כימותרפית + **דקסמטזון (Dexamethasone)** - סטרואיד חזק",
                        "duration": "8 שבועות על פי פרוטוקול"
                    },
                    {
                        "title": "טיפול CNS (במעורבות מערכת עצבים מרכזית)",
                        "description": "טיפול אינטרתקל (לתוך תעלת השדרה): **Methotrexate** + **הידרוקורטיזון**",
                        "indication": "רק במעורבות של CNS"
                    }
                ]
            },
            "order_index": 9
        },
        {
            "title": "נקודות מפתח",
            "section_type": "alert",
            "content": """📋 **עיקרי הדברים:**

⚡ **מחלה מסכנת חיים** - דורשת זיהוי וטיפול מהיר

🎯 **אתגר האבחון:**
- מחלה נדירה
- התייצגות וריאבילית
- אין ממצאים ספציפיים

🔬 **הפתופיזיולוגיה:**
- פעילות יתר של מקרופגים
- הפרשת ציטוקינים מוגזמת
- תאי NK והלימפוציטים ציטוטוקסיים פעילים ביתר

🦠 **טריגרים עיקריים:**
- זיהומים ויראליים (EBV, CMV)
- מחלות ראומטיות
- ממאירות

💊 **טיפול במטופלים יציבים:**
- טיפול בטריגר + סטרואידים
- EBV → ריטוקסימב

⚡ **טיפול במטופלים לא יציבים:**
- אין זמן לחכות!
- אטופוזיד + דקסמטזון (8 שבועות)
- מעורבות CNS → טיפול אינטרתקל""",
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
    print(f"   נושא: HLH - המופגוציטיק לימפוהיסטיאוציטוזיס")
    print(f"   קטגוריה: המטולוגיה/אונקולוגיה")
    print(f"   מקטעים: {len(sections)}")
    print(f"   ID: {topic_id}")
    
    return True

if __name__ == "__main__":
    print("⚡ PICU Learning Platform - הוספת תוכן")
    print("="*60)
    print("נושא: HLH - Hemophagocytic Lymphohistiocytosis")
    print("="*60)
    
    try:
        success = add_hlh_content()
        
        if success:
            print("\n🎉 הושלם בהצלחה!")
            print("\n💡 התוכן כולל:")
            print("   - הגדרה ופתופיזיולוגיה")
            print("   - תאים מעורבים")
            print("   - טריגרים נפוצים")
            print("   - טיפול במטופלים יציבים")
            print("   - טיפול במטופלים לא יציבים")
            print("   - פרוטוקול טיפולי מלא")
        else:
            print("\n❌ הייתה בעיה בהוספת התוכן")
    
    except Exception as e:
        print(f"\n❌ שגיאה: {e}")
        import traceback
        traceback.print_exc()
