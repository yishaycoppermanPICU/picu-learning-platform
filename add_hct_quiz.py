#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
סקריפט להוספת מבחן HCT למסד הנתונים
"""

import json
from utils.database import init_supabase, create_quiz_question, get_topics, get_quiz_questions, delete_quiz_question

def main():
    print("=" * 80)
    print("🧪 הוספת מבחן HCT Complications למערכת")
    print("=" * 80)
    
    # חיבור למסד נתונים
    print("\n🔄 מתחבר למסד הנתונים...")
    supabase = init_supabase()
    
    if not supabase:
        print("❌ שגיאה בחיבור למסד נתונים")
        return
    
    print("✅ חיבור הצליח!")
    
    # מחפש את הנושא HCT
    print("\n🔍 מחפש את נושא HCT Complications...")
    topics = get_topics()
    
    content_item_id = None
    for topic in topics:
        if 'hct' in topic.get('slug', '').lower() or 'השתלת מח' in topic.get('title', ''):
            content_item_id = topic['id']
            print(f"✅ נמצא HCT! ID: {content_item_id}")
            break
    
    if not content_item_id:
        print("❌ לא נמצא נושא HCT! יש ליצור אותו קודם.")
        return
    
    # טוען שאלות מקובץ
    print("📂 טוען שאלות מקובץ...")
    with open('hct_quiz.json', 'r', encoding='utf-8') as f:
        quiz_data = json.load(f)
    
    questions = quiz_data['questions']
    print(f"✅ נטענו {len(questions)} שאלות")
    
    # בודק אם יש שאלות קיימות
    print("\n🔍 בודק אם יש שאלות קיימות...")
    existing = get_quiz_questions(content_item_id=content_item_id)
    
    if existing:
        print(f"⚠️  נמצאו {len(existing)} שאלות קיימות. מוחק...")
        for q in existing:
            delete_quiz_question(q['id'])
        print("✅ שאלות קיימות נמחקו")
    
    # מוסיף שאלות חדשות
    print("\n📝 מוסיף שאלות חדשות...")
    success_count = 0
    
    for idx, q in enumerate(questions, 1):
        question_data = {
            'topic_id': content_item_id,
            'question_text': q['question'],
            'options': q['options'],
            'correct_answer': q['correct_answer'],
            'explanation': q['explanation'],
            'difficulty': q['difficulty']
        }
        
        try:
            response = create_quiz_question(question_data)
            if response:
                print(f"✅ שאלה {idx}/{len(questions)}: {q['id']}")
                success_count += 1
            else:
                print(f"❌ שאלה {idx}/{len(questions)} נכשלה")
        except Exception as e:
            print(f"❌ שגיאה בשאלה {idx}: {str(e)}")
    
    # סיכום
    print("\n" + "=" * 80)
    print(f"✨ סיכום: {success_count}/{len(questions)} שאלות נוספו בהצלחה!")
    print("=" * 80)
    
    if success_count == len(questions):
        print("\n🎉 המבחן נוסף בהצלחה!")
        print("\n💡 כעת ניתן:")
        print("   1. להיכנס לדף התוכן של HCT Complications")
        print("   2. ללחוץ על 'בחן את עצמך'")
        print(f"   3. לענות על {len(questions)} השאלות החדשות")
        print("   4. לקבל תג הישג אם משיגים 80%+")
    else:
        print("\n⚠️  ההוספה לא הושלמה במלואה")

if __name__ == '__main__':
    main()
