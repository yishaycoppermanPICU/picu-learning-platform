#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sync weekly progress from JSON file to database for a specific user
סנכרון נתוני התקדמות שבועית מקובץ JSON למסד נתונים למשתמש ספציפי
"""

import sys

def sync_user_progress(user_email):
    """
    מעתיק את נתוני ההתקדמות של משתמש מהקובץ JSON למסד הנתונים
    """
    from utils.database import init_supabase, update_user_weekly_progress
    from utils.weekly_content import load_weekly_progress
    
    # נרמול המייל
    user_email = user_email.lower()
    
    print(f"🔄 מסנכרן נתונים עבור: {user_email}")
    
    # טעינת נתונים מהקובץ
    file_progress = load_weekly_progress()
    
    if user_email not in file_progress:
        print(f"❌ משתמש {user_email} לא נמצא בקובץ JSON")
        return False
    
    user_data = file_progress[user_email]
    badges_count = len(user_data.get('badges', []))
    weeks_count = len(user_data.get('completed_weeks', []))
    
    print(f"📊 נמצאו נתונים בקובץ:")
    print(f"   - {weeks_count} שבועות שהושלמו")
    print(f"   - {badges_count} תגים")
    print(f"   - {user_data.get('total_points', 0)} נקודות")
    
    # עדכון במסד הנתונים
    if update_user_weekly_progress(user_email, user_data):
        print(f"✅ הנתונים סונכרנו בהצלחה!")
        return True
    else:
        print(f"❌ שגיאה בסנכרון")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        email = sys.argv[1]
    else:
        email = "yishaycopp@gmail.com"  # ברירת מחדל
    
    sync_user_progress(email)
