#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Supabase Connection
"""

from utils.database import init_supabase, DB_CONNECTED

def test_connection():
    """Test the Supabase connection"""
    
    print("🔍 בודק חיבור ל-Supabase...")
    print("=" * 60)
    
    supabase = init_supabase()
    
    if supabase and DB_CONNECTED:
        print("✅ החיבור הצליח!")
        print(f"📡 Supabase Client: {type(supabase).__name__}")
        
        # Try a simple query
        try:
            print("\n🔍 מנסה לקרוא טבלאות קיימות...")
            
            # Try to check existing tables
            result = supabase.table('topics').select("*").limit(1).execute()
            
            print(f"✅ טבלת topics קיימת!")
            print(f"📊 מספר רשומות: {len(result.data) if result.data else 0}")
            
            if result.data:
                print(f"📝 רשומה ראשונה: {result.data[0].get('title', 'N/A')}")
            
            # Check other tables
            tables_to_check = ['institutions', 'users', 'questions', 'quiz_results', 'topic_sections']
            for table in tables_to_check:
                try:
                    check = supabase.table(table).select("count", count="exact").limit(0).execute()
                    count = check.count if hasattr(check, 'count') else '?'
                    print(f"✅ טבלת {table}: {count} רשומות")
                except:
                    print(f"⚠️  טבלת {table}: לא נמצאה")
            
        except Exception as e:
            print(f"⚠️  בעיה בטבלאות: {e}")
            print("\n📝 הוראות:")
            print("1. אם הטבלאות לא קיימות, הרץ את ה-SQL שנתתי לך")
            print("2. אם קיימות אבל ריקות, הרץ: insert_sample_data.sql")
        
        return True
    else:
        print("❌ החיבור נכשל!")
        print("\n🔍 בדיקות:")
        print("1. ודא שSupabase URL נכון")
        print("2. ודא שה-API Key תקין")
        print("3. בדוק חיבור אינטרנט")
        return False

if __name__ == "__main__":
    test_connection()
