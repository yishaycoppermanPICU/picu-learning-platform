#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
מחיקת נושא TBI הישן לפני הוספה מחדש
"""

from utils.database import init_supabase

def delete_tbi_topic():
    """מחיקת נושא TBI הישן"""
    
    print("🔄 מתחבר למסד הנתונים...")
    supabase = init_supabase()
    
    if not supabase:
        print("❌ שגיאה בחיבור למסד נתונים")
        return False
    
    print("✅ חיבור הצליח!")
    
    try:
        # מחיקת כל הנושאים עם slug 'tbi_management'
        print("\n🗑️ מוחק נושא TBI ישן...")
        
        # קודם מוצאים את ה-ID
        response = supabase.table('topics').select("id").eq('slug', 'tbi_management').execute()
        
        if response.data:
            for topic in response.data:
                topic_id = topic['id']
                print(f"   מוחק נושא ID: {topic_id}")
                
                # מחיקת כל המקטעים
                supabase.table('topic_sections').delete().eq('topic_id', topic_id).execute()
                print(f"   ✅ מקטעים נמחקו")
                
                # מחיקת הנושא
                supabase.table('topics').delete().eq('id', topic_id).execute()
                print(f"   ✅ נושא נמחק")
        else:
            print("   ℹ️ לא נמצא נושא TBI קיים")
        
        return True
        
    except Exception as e:
        print(f"❌ שגיאה: {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("🗑️ מחיקת נושא TBI ישן")
    print("="*60)
    
    success = delete_tbi_topic()
    
    if success:
        print("\n✅ הושלם בהצלחה!")
    else:
        print("\n❌ הייתה בעיה במחיקה")
