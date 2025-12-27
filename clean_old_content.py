#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""מחיקת תוכן ישן - השארת רק פאנציטופניה"""

from utils.database import init_supabase

def clean_old_content():
    """מחק את כל התוכן הישן, השאר רק פאנציטופניה"""
    
    print("🗑️  מנקה תוכן ישן...")
    print("="*60)
    
    supabase = init_supabase()
    
    if not supabase:
        print("❌ שגיאה בחיבור")
        return False
    
    # ID של פאנציטופניה
    pancytopenia_id = 'b21b1fe0-577c-4904-989e-f88f501abf45'
    
    # מחיקת נושאים ישנים
    print("\n🔄 מוחק נושאים ישנים...")
    try:
        # מחיקת topic_sections של נושאים אחרים (יימחקו אוטומטית עם CASCADE)
        
        # מחיקת שאלות שלא קשורות לפאנציטופניה
        supabase.table('questions').delete().neq('topic_id', pancytopenia_id).execute()
        print("✅ שאלות ישנות נמחקו")
        
        # מחיקת נושאים שאינם פאנציטופניה
        result = supabase.table('topics').delete().neq('id', pancytopenia_id).execute()
        print("✅ נושאים ישנים נמחקו")
        
        # ניקוי quiz_results
        supabase.table('quiz_results').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
        print("✅ תוצאות quiz נוקו")
        
    except Exception as e:
        print(f"⚠️  שגיאה: {e}")
        return False
    
    print("\n" + "="*60)
    print("✅ ניקוי הושלם בהצלחה!")
    print("="*60)
    
    # בדיקת מצב
    print("\n📊 מצב נוכחי:")
    
    topics = supabase.table('topics').select("*").execute()
    print(f"   📚 נושאים: {len(topics.data)}")
    
    sections = supabase.table('topic_sections').select("*").execute()
    print(f"   📑 מקטעים: {len(sections.data)}")
    
    questions = supabase.table('questions').select("*").execute()
    print(f"   ❓ שאלות: {len(questions.data)}")
    
    print("\n✨ מוכן להוספת תוכן חדש מהימן!")
    
    return True

if __name__ == "__main__":
    print("🧹 PICU Learning Platform - ניקוי תוכן")
    print("="*60)
    print("⚠️  ימחקו כל הנושאים למעט: פאנציטופניה")
    print("="*60)
    
    try:
        success = clean_old_content()
        
        if success:
            print("\n🎉 הסתיים בהצלחה!")
            print("\n📝 עכשיו אפשר להוסיף תוכן חדש אמין")
        else:
            print("\n❌ הייתה בעיה")
    
    except Exception as e:
        print(f"\n❌ שגיאה: {e}")
        import traceback
        traceback.print_exc()
