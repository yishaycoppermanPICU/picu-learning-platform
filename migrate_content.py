#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Content Migration Script
Migrates content from JSON files to Supabase database
"""

import json
import os
from pathlib import Path
from typing import Dict, List
from utils.database import init_supabase, create_content_item, create_content_section, create_quiz_question

def load_json_files(base_path: str) -> List[Dict]:
    """Load all JSON files from content directory"""
    content_files = []
    
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                category = os.path.basename(root)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        data['_file_path'] = file_path
                        data['_category'] = category
                        content_files.append(data)
                except Exception as e:
                    print(f"❌ שגיאה בקריאת {file}: {e}")
    
    return content_files

def convert_json_to_db_format(json_data: Dict) -> tuple:
    """Convert JSON format to database format"""
    
    # Create content item
    slug = json_data.get('id', json_data.get('title', '')).lower().replace(' ', '_')
    
    content_item = {
        'slug': slug,
        'title': json_data.get('title', json_data.get('name', 'Untitled')),
        'category': json_data.get('_category', 'general'),
        'subtitle': json_data.get('subtitle', ''),
        'description': json_data.get('description', ''),
        'clinical_definition': json_data.get('clinical_definition', json_data.get('definition', '')),
        'tags': json_data.get('tags', []),
        'icon': json_data.get('icon', '📄'),
        'order_index': json_data.get('order', 0),
        'is_published': True
    }
    
    # Extract sections
    sections = []
    order = 0
    
    # Common section mappings
    section_mappings = {
        'epidemiology': 'אפידמיולוגיה',
        'pathophysiology': 'פתופיזיולוגיה',
        'clinical_presentation': 'מצגת קלינית',
        'diagnosis': 'אבחון',
        'differential_diagnosis': 'אבחנה מבדלת',
        'treatment': 'טיפול',
        'complications': 'סיבוכים',
        'prognosis': 'פרוגנוזה',
        'references': 'מקורות',
        'key_points': 'נקודות מפתח',
        'clinical_pearls': 'פנינים קליניות',
        'mechanism': 'מנגנון פעולה',
        'indications': 'אינדיקציות',
        'contraindications': 'התוויות נגד',
        'dosing': 'מינון',
        'side_effects': 'תופעות לוואי',
        'monitoring': 'מעקב',
        'administration': 'מתן',
    }
    
    for key, title in section_mappings.items():
        if key in json_data:
            value = json_data[key]
            
            # Determine section type
            if isinstance(value, list):
                section_type = 'list'
                content = '\n'.join([f"- {item}" for item in value])
                metadata = {'items': value}
            elif isinstance(value, dict):
                # Check if it's steps or options format
                if 'steps' in value:
                    section_type = 'steps'
                    content = value.get('description', '')
                    metadata = value
                elif 'options' in value:
                    section_type = 'options'
                    content = value.get('description', '')
                    metadata = value
                else:
                    section_type = 'text'
                    content = str(value)
                    metadata = {}
            else:
                section_type = 'text'
                content = str(value)
                metadata = {}
            
            sections.append({
                'section_type': section_type,
                'title': title,
                'content': content,
                'metadata': metadata,
                'order_index': order
            })
            order += 1
    
    return content_item, sections

def migrate_content():
    """Main migration function"""
    
    print("🚀 מתחיל העברת תוכן...")
    print("=" * 60)
    
    # Initialize database
    supabase = init_supabase()
    if not supabase:
        print("❌ לא ניתן להתחבר למסד הנתונים")
        return False
    
    print("✅ התחברות למסד נתונים הצליחה")
    
    # Load JSON files
    base_path = 'data/content'
    print(f"\n📂 קורא קבצי JSON מ-{base_path}...")
    
    json_files = load_json_files(base_path)
    print(f"✅ נמצאו {len(json_files)} קבצים")
    
    # Migrate each file
    success_count = 0
    error_count = 0
    
    for idx, json_data in enumerate(json_files, 1):
        try:
            title = json_data.get('title', json_data.get('name', 'Unknown'))
            print(f"\n[{idx}/{len(json_files)}] 🔄 מעביר: {title}...")
            
            # Convert to DB format
            content_item, sections = convert_json_to_db_format(json_data)
            
            # Create content item
            created_item = create_content_item(content_item)
            
            if not created_item:
                print(f"❌ נכשל ביצירת פריט תוכן")
                error_count += 1
                continue
            
            item_id = created_item['id']
            print(f"✅ נוצר פריט תוכן: {item_id}")
            
            # Create sections
            for section in sections:
                section['content_item_id'] = item_id
                created_section = create_content_section(section)
                
                if created_section:
                    print(f"  ✅ נוצר מקטע: {section['title']}")
                else:
                    print(f"  ⚠️  נכשל מקטע: {section['title']}")
            
            success_count += 1
            
        except Exception as e:
            print(f"❌ שגיאה: {e}")
            error_count += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 סיכום:")
    print(f"✅ הצליחו: {success_count}")
    print(f"❌ נכשלו: {error_count}")
    print(f"📝 סה\"כ: {len(json_files)}")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    print("🎯 PICU Learning Platform - Content Migration")
    print("=" * 60)
    
    try:
        migrate_content()
        print("\n✅ ההעברה הושלמה!")
        print("\n📝 שלבים הבאים:")
        print("1. בדוק בSupabase Dashboard שהנתונים נוספו")
        print("2. הרץ את האפליקציה: streamlit run app.py")
        print("3. עבור לעמוד התוכן ובדוק שהכל מוצג נכון")
        
    except Exception as e:
        print(f"\n❌ שגיאה קריטית: {e}")
        import traceback
        traceback.print_exc()
