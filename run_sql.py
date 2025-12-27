#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run SQL Script
Executes SQL commands directly via Supabase API
"""

from utils.database import init_supabase

def run_sql():
    """Execute SQL to create tables"""
    
    print("🔄 מתחבר ל-Supabase...")
    supabase = init_supabase()
    
    if not supabase:
        print("❌ שגיאה: לא ניתן להתחבר ל-Supabase")
        return False
    
    print("✅ התחברות הצליחה!")
    
    # Read SQL file
    with open('create_tables.sql', 'r', encoding='utf-8') as f:
        sql = f.read()
    
    print("\n📝 מריץ SQL...")
    
    try:
        # Execute SQL using RPC or direct query
        result = supabase.rpc('exec_sql', {'query': sql}).execute()
        print("✅ SQL הורץ בהצלחה!")
        return True
    except Exception as e:
        print(f"⚠️  שגיאה: {e}")
        print("\n📋 אנא הרץ את הפקודות הבאות ב-Supabase SQL Editor:")
        print("=" * 60)
        print("1. פתח את Supabase Dashboard: https://xdzpnlqzlopxgktltvif.supabase.co")
        print("2. לחץ על SQL Editor")
        print("3. צור New Query")
        print("4. העתק את התוכן מ-create_tables.sql")
        print("5. לחץ RUN")
        print("=" * 60)
        return False

if __name__ == "__main__":
    run_sql()
