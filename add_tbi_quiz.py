#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
הוספת שאלות מבחן על TBI - Traumatic Brain Injury
"""

import json
from utils.database import init_supabase, create_quiz_question, get_topics, get_quiz_questions, delete_quiz_question

def add_tbi_quiz():
    """הוספת 10 שאלות על TBI למסד הנתונים"""
    
    print("🔄 מתחבר למסד הנתונים...")
    supabase = init_supabase()
    
    if not supabase:
        print("❌ שגיאה בחיבור למסד נתונים")
        return False
    
    print("✅ חיבור הצליח!")
    
    # מציאת ה-content_item_id של TBI
    print("\n🔍 מחפש את נושא TBI...")
    topics = get_topics()
    tbi_topic = None
    
    for topic in topics:
        if topic.get('slug') == 'tbi_management':
            tbi_topic = topic
            break
    
    if not tbi_topic:
        print("❌ לא נמצא נושא TBI במסד הנתונים")
        print("💡 יש להריץ את add_tbi.py קודם")
        return False
    
    content_item_id = tbi_topic['id']
    print(f"✅ נמצא TBI! ID: {content_item_id}")
    
    # טעינת השאלות מקובץ JSON
    print("\n📂 טוען שאלות מקובץ...")
    with open('tbi_quiz.json', 'r', encoding='utf-8') as f:
        quiz_data = json.load(f)
    
    questions = quiz_data['questions']
    print(f"✅ נטענו {len(questions)} שאלות")
    
    # בדיקה אם כבר קיימות שאלות לנושא זה
    print("\n🔍 בודק אם יש שאלות קיימות...")
    existing = get_quiz_questions(content_item_id=content_item_id)
    
    if existing and len(existing) > 0:
        print(f"⚠️  נמצאו {len(existing)} שאלות קיימות")
        print("🗑️  מוחק שאלות קיימות...")
        for q in existing:
            delete_quiz_question(q['id'])
        print("✅ שאלות קיימות נמחקו")
    
    # הוספת השאלות החדשות
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
                print(f"✅ שאלה {idx}/10: {question['id']}")
                success_count += 1
            else:
                print(f"❌ שאלה {idx}/10 נכשלה")
        except Exception as e:
            print(f"❌ שגיאה בשאלה {idx}: {str(e)}")
    
    print(f"\n{'='*50}")
    print(f"✨ סיכום: {success_count}/{len(questions)} שאלות נוספו בהצלחה!")
    print(f"{'='*50}")
    
    return success_count == len(questions)

if __name__ == "__main__":
    print("="*50)
    print("🧠 הוספת מבחן TBI למערכת")
    print("="*50)
    
    success = add_tbi_quiz()
    
    if success:
        print("\n🎉 המבחן נוסף בהצלחה!")
        print("\n💡 כעת ניתן:")
        print("   1. להיכנס לדף התוכן של TBI")
        print("   2. ללחוץ על 'בחן את עצמך'")
        print("   3. לענות על 10 השאלות החדשות")
        print("   4. לקבל תג הישג אם משיגים 80%+")
    else:
        print("\n⚠️  ההוספה לא הושלמה במלואה")
