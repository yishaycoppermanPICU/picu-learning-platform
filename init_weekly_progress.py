#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Initialize weekly_progress for all existing users
אתחול עמודת weekly_progress לכל המשתמשים הקיימים
"""

from utils.database import init_supabase
import json

def init_all_users_weekly_progress():
    """
    מאתחל את עמודת weekly_progress לכל המשתמשים
    """
    print("🔄 מאתחל weekly_progress לכל המשתמשים...")
    
    supabase = init_supabase()
    if not supabase:
        print("❌ שגיאה: לא ניתן להתחבר למסד הנתונים")
        return
    
    # קריאת כל המשתמשים
    response = supabase.table('users').select('id, email, username, weekly_progress').execute()
    
    if not response.data:
        print("⚠️  אין משתמשים במסד הנתונים")
        return
    
    print(f"📊 נמצאו {len(response.data)} משתמשים")
    
    # בדיקה ועדכון כל משתמש
    for user in response.data:
        email = user.get('email', '')
        username = user.get('username', '')
        weekly_progress = user.get('weekly_progress')
        
        if not weekly_progress or weekly_progress == {}:
            # אתחול ברירת מחדל
            default_progress = {
                'completed_weeks': [],
                'badges': [],
                'total_points': 0
            }
            
            try:
                # ניסיון לטעון נתונים מהקובץ המקומי אם קיים
                import sys
                from pathlib import Path
                sys.path.append(str(Path(__file__).parent))
                
                from utils.weekly_content import load_weekly_progress
                file_progress = load_weekly_progress()
                
                # חיפוש המשתמש בקובץ (עם ועם לי case sensitivity)
                user_data = None
                for file_email, data in file_progress.items():
                    if file_email.lower() == email.lower():
                        user_data = data
                        break
                
                if user_data:
                    default_progress = user_data
                    print(f"  📥 {email}: העתקה מקובץ JSON ({len(user_data.get('badges', []))} תגים)")
                else:
                    print(f"  🆕 {email}: אתחול חדש")
            except Exception as e:
                print(f"  ⚠️  {email}: אתחול חדש (לא נמצא בקובץ)")
            
            # עדכון במסד הנתונים
            supabase.table('users').update({
                'weekly_progress': default_progress
            }).eq('email', email).execute()
        else:
            badges_count = len(weekly_progress.get('badges', []))
            weeks_count = len(weekly_progress.get('completed_weeks', []))
            print(f"  ✅ {email}: כבר מאותחל ({weeks_count} שבועות, {badges_count} תגים)")
    
    print("\n✅ הושלם!")

if __name__ == "__main__":
    init_all_users_weekly_progress()
