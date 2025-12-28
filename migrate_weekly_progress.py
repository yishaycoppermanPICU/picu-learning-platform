#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migrate Weekly Progress from JSON file to Database
העברת נתוני התקדמות שבועית מקובץ JSON למסד הנתונים
"""

import json
from pathlib import Path
from utils.database import init_supabase, update_user_weekly_progress

def migrate_weekly_progress():
    """
    מעביר נתוני התקדמות שבועית מקובץ JSON למסד הנתונים
    """
    print("🔄 מתחיל העברת נתוני התקדמות שבועית...")
    
    # טעינת נתונים מהקובץ הישן
    data_dir = Path(__file__).parent / "data"
    json_file = data_dir / "weekly_progress.json"
    
    if not json_file.exists():
        print("⚠️  לא נמצא קובץ weekly_progress.json - אין מה להעביר")
        return
    
    with open(json_file, 'r', encoding='utf-8') as f:
        file_data = json.load(f)
    
    if not file_data:
        print("⚠️  הקובץ ריק - אין מה להעביר")
        return
    
    print(f"📊 נמצאו נתונים של {len(file_data)} משתמשים")
    
    # התחברות למסד הנתונים
    supabase = init_supabase()
    if not supabase:
        print("❌ שגיאה: לא ניתן להתחבר למסד הנתונים")
        return
    
    # העברת כל משתמש
    success_count = 0
    error_count = 0
    
    for user_email, progress_data in file_data.items():
        try:
            # עדכון ההתקדמות השבועית במסד הנתונים
            if update_user_weekly_progress(user_email, progress_data):
                print(f"✅ {user_email}: {len(progress_data.get('completed_weeks', []))} שבועות, {len(progress_data.get('badges', []))} תגים")
                success_count += 1
            else:
                print(f"⚠️  {user_email}: נכשל בעדכון")
                error_count += 1
        except Exception as e:
            print(f"❌ שגיאה עם {user_email}: {e}")
            error_count += 1
    
    print("\n" + "="*60)
    print(f"✅ הושלם! {success_count} משתמשים הועברו בהצלחה")
    if error_count > 0:
        print(f"⚠️  {error_count} שגיאות")
    print("="*60)
    
    # יצירת גיבוי של הקובץ הישן
    backup_file = data_dir / "weekly_progress.json.backup"
    import shutil
    shutil.copy(json_file, backup_file)
    print(f"💾 גיבוי נוצר: {backup_file}")

if __name__ == "__main__":
    migrate_weekly_progress()
