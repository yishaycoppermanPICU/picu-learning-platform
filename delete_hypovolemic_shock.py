#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
מחיקת נושא הלם היפוולמי לפני הוספה מחדש
"""

from utils.database import init_supabase

def delete_hypovolemic_shock_topic():
    """מחיקת נושא הלם היפוולמי"""
    
    print("🔄 מתחבר למסד הנתונים...")
    supabase = init_supabase()
    
    if not supabase:
        print("❌ שגיאה בחיבור למסד נתונים")
        return False
    
    print("✅ חיבור הצליח!")
    
    try:
        # מחיקת כל הנושאים עם slug 'hypovolemic_shock'
        print("\n🗑️ מוחק נושא הלם היפוולמי ישן...")
        
        # קודם מוצאים את ה-ID
        response = supabase.table('topics').select("id, title").eq('slug', 'hypovolemic_shock').execute()
        
        if response.data:
            for topic in response.data:
                topic_id = topic['id']
                title = topic['title']
                print(f"   מוחק נושא: {title} (ID: {topic_id})")
                
                # מחיקת כל המקטעים
                sections_response = supabase.table('topic_sections').delete().eq('topic_id', topic_id).execute()
                print(f"   ✅ מקטעים נמחקו")
                
                # מחיקת הנושא
                supabase.table('topics').delete().eq('id', topic_id).execute()
                print(f"   ✅ נושא נמחק")
        else:
            print("   ℹ️ לא נמצא נושא הלם היפוולמי קיים")
        
        print("\n✅ מחיקה הושלמה בהצלחה!")
        return True
        
    except Exception as e:
        print(f"❌ שגיאה: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*60)
    print("💧 מחיקת תוכן הלם היפוולמי")
    print("="*60)
    
    success = delete_hypovolemic_shock_topic()
    
    if success:
        print("\n🎉 המחיקה הושלמה בהצלחה!")
        print("💡 כעת ניתן להריץ: python add_hypovolemic_shock.py")
    else:
        print("\n❌ המחיקה נכשלה")
