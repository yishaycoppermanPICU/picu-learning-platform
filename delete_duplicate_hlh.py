#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
מחיקת HLH כפול
"""

from utils.database import init_supabase, delete_content_item

def delete_duplicate_hlh():
    """מחק את HLH הכפול"""
    
    print("🔄 מתחבר למסד הנתונים...")
    supabase = init_supabase()
    
    if not supabase:
        print("❌ שגיאה בחיבור למסד נתונים")
        return False
    
    print("✅ חיבור הצליח!")
    
    # ID של HLH הישן שרוצים למחוק
    old_hlh_id = '1e2e22c9-ec01-49c8-91da-f3caf8d588e3'
    
    print(f"\n🗑️  מוחק HLH ישן (ID: {old_hlh_id})...")
    
    if delete_content_item(old_hlh_id):
        print("✅ HLH הישן נמחק בהצלחה!")
        return True
    else:
        print("❌ שגיאה במחיקה")
        return False

if __name__ == "__main__":
    print("🧹 מחיקת HLH כפול")
    print("="*60)
    
    success = delete_duplicate_hlh()
    
    if success:
        print("\n🎉 הושלם בהצלחה!")
    else:
        print("\n❌ הייתה בעיה")
