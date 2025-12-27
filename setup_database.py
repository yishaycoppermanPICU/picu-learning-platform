#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup Database Script
Creates all required tables in Supabase
"""

import sys
from utils.database import init_supabase

def setup_database():
    """Create all database tables"""
    
    print("🔄 מתחבר ל-Supabase...")
    supabase = init_supabase()
    
    if not supabase:
        print("❌ שגיאה: לא ניתן להתחבר ל-Supabase")
        return False
    
    print("✅ התחברות הצליחה!")
    
    # Read SQL file
    try:
        with open('create_tables.sql', 'r', encoding='utf-8') as f:
            sql_commands = f.read()
        
        print("📄 קובץ SQL נטען בהצלחה")
        print("\n⚠️  הערה: יש להריץ את ה-SQL הבא ב-Supabase SQL Editor:")
        print("=" * 60)
        print("1. גש ל-Supabase Dashboard")
        print("2. לחץ על SQL Editor בתפריט השמאלי")
        print("3. צור Query חדש")
        print("4. העתק והדבק את התוכן מהקובץ create_tables.sql")
        print("5. לחץ על RUN")
        print("=" * 60)
        
        print("\n📋 או השתמש בפקודה:")
        print(f"cat create_tables.sql | psql <YOUR_DATABASE_URL>")
        
        return True
        
    except Exception as e:
        print(f"❌ שגיאה בקריאת קובץ SQL: {e}")
        return False

if __name__ == "__main__":
    print("🚀 PICU Learning Platform - Database Setup")
    print("=" * 60)
    
    success = setup_database()
    
    if success:
        print("\n✅ ההתקנה הושלמה!")
        print("\n📝 שלבים הבאים:")
        print("1. הרץ את ה-SQL בSupabase (ראה הוראות למעלה)")
        print("2. בדוק שהטבלאות נוצרו: Tables -> content_items")
        print("3. הרץ: python migrate_content.py להעברת תוכן מ-JSON")
    else:
        print("\n❌ ההתקנה נכשלה")
        sys.exit(1)
