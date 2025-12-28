#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
הוספת שאלות מבחן על מתן מוצרי דם
"""

import json
from utils.database import init_supabase, create_quiz_question, get_topics, get_quiz_questions, delete_quiz_question

def add_blood_products_quiz():
    """הוספת 10 שאלות על מתן מוצרי דם למסד הנתונים"""
    
    print("🔄 מתחבר למסד הנתונים...")
    supabase = init_supabase()
    
    if not supabase:
        print("❌ שגיאה בחיבור למסד נתונים")
        return False
    
    print("✅ חיבור הצליח!")
    
    # מציאת ה-content_item_id של מתן מוצרי דם
    print("\n🔍 מחפש את נושא מתן מוצרי דם...")
    topics = get_topics()
    blood_products_topic = None
    
    for topic in topics:
        if topic.get('slug') == 'blood_products_administration':
            blood_products_topic = topic
            break
    
    if not blood_products_topic:
        print("❌ לא נמצא נושא מתן מוצרי דם במסד הנתונים")
        print("💡 יש להריץ את add_blood_products.py קודם")
        return False
    
    content_item_id = blood_products_topic['id']
    print(f"✅ נמצא מתן מוצרי דם! ID: {content_item_id}")
    
    # טעינת השאלות מקובץ JSON
    print("\n📂 טוען שאלות מקובץ...")
    with open('blood_products_quiz.json', 'r', encoding='utf-8') as f:
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
    print("💉 הוספת מבחן מתן מוצרי דם למערכת")
    print("="*50)
    
    success = add_blood_products_quiz()
    
    if success:
        print("\n🎉 המבחן נוסף בהצלחה!")
        print("\n💡 כעת ניתן:")
        print("   1. להיכנס לדף התוכן של מתן מוצרי דם")
        print("   2. ללחוץ על 'בחן את עצמך'")
        print("   3. לענות על 10 השאלות החדשות")
        print("   4. לקבל תג הישג אם משיגים 80%+")
    else:
        print("\n⚠️  ההוספה לא הושלמה במלואה")
