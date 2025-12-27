#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""בדיקת תוכן במסד נתונים"""

from utils.database import init_supabase, get_topics, get_content_item

supabase = init_supabase()

print("📚 רשימת נושאים:")
print("="*60)

topics = get_topics()
print(f"סה\"כ נושאים: {len(topics)}\n")

for topic in topics:
    print(f"🩸 {topic['title']}")
    print(f"   ID: {topic['id']}")
    print(f"   קטגוריה: {topic.get('category', 'לא מוגדר')}")
    print(f"   תיאור: {topic.get('description', 'אין תיאור')[:50]}...")
    
    # Get full topic with sections
    full_topic = get_content_item(topic['id'])
    if full_topic and full_topic.get('sections'):
        print(f"   📑 מקטעים: {len(full_topic['sections'])}")
        for sec in full_topic['sections']:
            print(f"      - {sec['title']}")
    print()
