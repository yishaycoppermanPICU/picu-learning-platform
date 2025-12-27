#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
הוספת תוכן: פאנציטופניה
"""

from utils.database import init_supabase, create_content_item, create_content_section

def add_pancytopenia_content():
    """הוספת נושא פאנציטופניה עם כל המקטעים"""
    
    print("🔄 מתחבר למסד הנתונים...")
    supabase = init_supabase()
    
    if not supabase:
        print("❌ שגיאה בחיבור למסד נתונים")
        return False
    
    print("✅ חיבור הצליח!")
    
    # יצירת הנושא הראשי
    print("\n📝 יוצר נושא: פאנציטופניה...")
    
    topic_data = {
        "title": "פאנציטופניה",
        "category": "hematology",
        "description": "ירידה משמעותית בכל שורות הדם - טרומבוציטופניה, נויטרופניה ואנמיה",
        "icon": "🩸",
        "slug": "pancytopenia",
        "tags": ["המטולוגיה", "אונקולוגיה", "מח עצם", "אנמיה"],
        "order_index": 10
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
            "title": "הגדרה",
            "section_type": "text",
            "content": """פאנציטופניה מתייחסת למצב בו ישנה ירידה משמעותית בכל שורות הדם. 

כלומר:
- **טרומבוציטופניה** - ירידה בטסיות דם
- **נויטרופניה** - ירידה בנויטרופילים
- **אנמיה** - ירידה בהמוגלובין""",
            "order_index": 0
        },
        {
            "title": "גורמים לפאנציטופניה",
            "section_type": "text",
            "content": "ישנם שני גורמים עיקריים לפאנציטופניה:",
            "order_index": 1
        },
        {
            "title": "לוקמיה",
            "section_type": "text",
            "content": """**סרטן הפוגע במח העצם**

**סימנים נוספים המעידים על לוקמיה:**
- אורגנומגלי (הגדלה של אברים)
- לימפאדנופתיה (הגדלת קשריות לימפה)
- כאבי עצמות""",
            "order_index": 2
        },
        {
            "title": "אנמיה אפלסטית",
            "section_type": "text",
            "content": """מצב בו יש **היפופלזיה או אפלזיה של מח העצם**, וכתוצאה מכך ירידה בכל השורות, בהתאם לחומרת האנמיה.

**סיבות לאנמיה אפלסטית:**
- אדיופטית (לא ידועה)
- תרופות ציטוטוקסיות והקרנות
- זיהומים ויראליים
- חשיפה לחומרים מסוכנים (בנזין, אדי דבק)
- מחלות אוטואימוניות (לופוס, GVHD)
- הריון
- אנורקסיה נרבוזה""",
            "order_index": 3
        },
        {
            "title": "טיפול באנמיה אפלסטית",
            "section_type": "options",
            "content": "שתי אפשרויות טיפול עיקריות:",
            "metadata": {
                "options": [
                    {
                        "title": "השתלת מח עצם",
                        "description": "מתורם קרוב משפחה מתאים. **יתרונות בטווח הקרוב:** פחות בעיות, פחות קשיים בטיפול, החזרת ספירת דם מהירה יותר.",
                        "indication": "טיפול מועדף כאשר יש תורם מתאים"
                    },
                    {
                        "title": "טיפול אימונוסופרסיבי",
                        "description": "בטווח הארוך, שני הטיפולים (השתלה ואימונוסופרסיה) יעילים ללא יתרון משמעותי.",
                        "indication": "חלופה כאשר אין תורם מתאים"
                    }
                ]
            },
            "order_index": 4
        },
        {
            "title": "טיפול באנמיה אפלסטית לא חמורה",
            "section_type": "steps",
            "content": "במקרה בו האנמיה אפלסטית אינה חמורה:",
            "metadata": {
                "steps": [
                    "השגחה ומעקב צמוד",
                    "טיפול תומך",
                    "מתן דם בעת צורך",
                    "מניעת זיהומים",
                    "המתנה לשיפור שורות"
                ]
            },
            "order_index": 5
        },
        {
            "title": "נקודות מפתח",
            "section_type": "alert",
            "content": """⚠️ **חשוב לזכור:**

- פאנציטופניה = ירידה בכל 3 שורות הדם
- יש לחשוד בלוקמיה במקרה של אורגנומגלי + לימפאדנופתיה + כאבי עצמות
- אנמיה אפלסטית חמורה דורשת החלטה בין השתלה לטיפול אימונוסופרסיבי
- באנמיה לא חמורה - טיפול תומך ומעקב""",
            "order_index": 6
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
    print(f"   נושא: פאנציטופניה")
    print(f"   קטגוריה: המטולוגיה")
    print(f"   מקטעים: {len(sections)}")
    print(f"   ID: {topic_id}")
    
    return True

if __name__ == "__main__":
    print("🩸 PICU Learning Platform - הוספת תוכן")
    print("="*60)
    print("נושא: פאנציטופניה")
    print("="*60)
    
    try:
        success = add_pancytopenia_content()
        
        if success:
            print("\n🎉 הושלם בהצלחה!")
            print("\n💡 עכשיו תוכל:")
            print("   1. להריץ: streamlit run app.py")
            print("   2. לעבור לעמוד 'תוכן' או 'עורך מסד נתונים'")
            print("   3. לראות את הנושא החדש!")
        else:
            print("\n❌ הייתה בעיה בהוספת התוכן")
    
    except Exception as e:
        print(f"\n❌ שגיאה: {e}")
        import traceback
        traceback.print_exc()
