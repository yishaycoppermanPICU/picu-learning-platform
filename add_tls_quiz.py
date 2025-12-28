#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
הוספת שאלות מבחן על Tumor Lysis Syndrome
"""

import json
from utils.database import init_supabase, create_quiz_question, get_topics, get_quiz_questions, delete_quiz_question

def add_tls_quiz():
    """הוספת 15 שאלות על TLS למסד הנתונים"""
    
    print("🔄 מתחבר למסד הנתונים...")
    supabase = init_supabase()
    
    if not supabase:
        print("❌ שגיאה בחיבור למסד נתונים")
        return False
    
    print("✅ חיבור הצליח!")
    
    # מציאת ה-content_item_id של TLS
    print("\n🔍 מחפש את נושא Tumor Lysis Syndrome...")
    topics = get_topics()
    tls_topic = None
    
    for topic in topics:
        if 'tumor' in topic.get('slug', '').lower() or 'tls' in topic.get('title', '').lower():
            tls_topic = topic
            break
    
    if not tls_topic:
        print("❌ לא נמצא נושא TLS במסד הנתונים")
        print("💡 יש להריץ את add_tls.py קודם")
        return False
    
    content_item_id = tls_topic['id']
    print(f"✅ נמצא TLS! ID: {content_item_id}")
    
    # טעינת השאלות מקובץ JSON
    print("\n📂 טוען שאלות מקובץ...")
    with open('tls_quiz.json', 'r', encoding='utf-8') as f:
        quiz_data = json.load(f)
    
    questions = quiz_data['questions']
    print(f"✅ נטענו {len(questions)} שאלות")
    
    # בדיקה אם כבר קיימות שאלות לנושא זה
    print("\n🔍 בודק אם יש שאלות קיימות...")
    existing = get_quiz_questions(content_item_id=content_item_id)
    
    if existing:
        print(f"⚠️  נמצאו {len(existing)} שאלות קיימות")
        print("🗑️  מוחק שאלות קיימות...")
        for q in existing:
            delete_quiz_question(q['id'])
        print("✅ שאלות קיימות נמחקו")
    
    print("\n📝 מוסיף שאלות חדשות...")
    success_count = 0
    
    for idx, question in enumerate(questions, 1):
        question_data = {
            'topic_id': content_item_id,
            'question_text': question['question'],
            'options': question['options'],
            'correct_answer': question['correct_answer'],
            'explanation': question['explanation'],
            'difficulty': question['difficulty']
        }
        
        try:
            response = create_quiz_question(question_data)
            if response:
                print(f"✅ שאלה {idx}/{len(questions)}: {question['id']}")
                success_count += 1
            else:
                print(f"❌ שאלה {idx}/{len(questions)} נכשלה")
        except Exception as e:
            print(f"❌ שגיאה בשאלה {idx}: {str(e)}")
    
    print(f"\n{'='*50}")
    print(f"✨ סיכום: {success_count}/{len(questions)} שאלות נוספו בהצלחה!")
    print(f"{'='*50}")
    
    return success_count == len(questions)

if __name__ == "__main__":
    print("="*50)
    print("🧪 הוספת מבחן Tumor Lysis Syndrome למערכת")
    print("="*50)
    
    success = add_tls_quiz()
    
    if success:
        print("\n🎉 המבחן נוסף בהצלחה!")
        print("\n💡 כעת ניתן:")
        print("   1. להיכנס לדף התוכן של TLS")
        print("   2. ללחוץ על 'בחן את עצמך'")
        print("   3. לענות על 15 השאלות החדשות")
        print("   4. לקבל תג הישג אם משיגים 80%+")
    else:
        print("\n⚠️  ההוספה לא הושלמה במלואה")
