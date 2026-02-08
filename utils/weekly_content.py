# -*- coding: utf-8 -*-
"""
מערכת ניהול תוכן שבועי מומלץ
Weekly recommended content management system
"""

from datetime import datetime, timedelta
import json
from pathlib import Path

# תוכן שבועי מומלץ - מפת שבועות לנושאים
WEEKLY_CONTENT = {
    1: {
        "topic_id": "094309da-dbf5-498f-b41c-83d1d2aff23e",  # ספסיס ושוק ספטי
        "title": "ספסיס ושוק ספטי",
        "category": "infections",  # תוקן - הקובץ נמצא ב-infections
        "json_file": "sepsis_protocol",  # שם הקובץ JSON
        "description": "למידה מעמיקה של פרוטוקול הזהב בטיפול בספסיס בילדים",
        "quiz_category": "resuscitation",
        "quiz_topic": "sepsis_protocol",
        "min_quiz_score": 80,
        "icon": "🦠"
    },
    2: {
        "topic_id": "96858c04-abc4-46d7-a14e-9530b3bbbda3",  # הלם/שוק היפוולמי
        "title": "הלם/שוק היפוולמי-המורגי",
        "category": "resuscitation",
        "json_file": "hypovolemic_shock",  # שם הקובץ JSON
        "description": "זיהוי וטיפול בשוק היפובולמי-המורגי בילדים",
        "quiz_category": "resuscitation",
        "quiz_topic": "hypovolemic_shock",
        "min_quiz_score": 80,
        "icon": "🚨"
    },
    3: {
        "topic_id": "f7ec21b4-68f1-4a4e-987b-e80da1ca1c84",  # HLH
        "title": "HLH - המופגוציטיק לימפוהיסטיאוציטוזיס",
        "category": "hematology",
        "json_file": "hlh_syndrome",  # שם הקובץ JSON
        "description": "המופגוציטיק לימפוהיסטיאוציטוזיס - אבחון וטיפול",
        "quiz_category": "hematology",
        "quiz_topic": "hlh_syndrome",
        "min_quiz_score": 80,
        "icon": "🩸"
    },
    4: {
        "topic_id": "c42fc8b6-af80-4900-b262-20268d3100b4",  # TBI - זה הנכון!
        "title": "TBI - Traumatic Brain Injury (טראומת ראש)",
        "category": "trauma",
        "json_file": "tbi_management",  # שם הקובץ JSON
        "description": "ניהול טראומטי של פגיעות ראש בילדים",
        "quiz_category": "trauma",
        "quiz_topic": "tbi_management",
        "min_quiz_score": 80,
        "icon": "🤕"
    },
    5: {
        "topic_id": "95cf4af2-4f44-48d5-87e0-2029bf976d8d",  # TLS
        "title": "Tumor Lysis Syndrome - TLS",
        "category": "hematology",
        "json_file": "tumor_lysis_syndrome",  # שם הקובץ JSON
        "description": "זיהוי מוקדם וטיפול בתסמונת תמוגת גידול",
        "quiz_category": "hematology",
        "quiz_topic": "tumor_lysis_syndrome",
        "min_quiz_score": 80,
        "icon": "🩸"
    },
    6: {
        "topic_id": "4080ae23-293a-4794-9a73-db3a03588d30",  # SCID
        "title": "SCID - חוסר חיסוני משולב חמור",
        "category": "immunology",
        "json_file": "scid_management",  # שם הקובץ JSON
        "description": "חוסר חיסוני משולב חמור - טיפול מיידי",
        "quiz_category": "immunology",
        "quiz_topic": "scid_management",
        "min_quiz_score": 80,
        "icon": "🛡️"
    },
    7: {
        "topic_id": "5ed35c74-4e2e-439f-98ca-44cdef50b360",  # HCT
        "title": "השתלת מח עצם - HCT",
        "category": "hematology",
        "json_file": "hct_complications",  # שם הקובץ JSON
        "description": "סיבוכים וטיפול בהשתלת מח עצם",
        "quiz_category": "hematology",
        "quiz_topic": "hct_complications",
        "min_quiz_score": 80,
        "icon": "🩺"
    },
    8: {
        "topic_id": "74cd0d61-0b7a-480f-ad3b-a642c0348090",  # מתן מוצרי דם - ID מתוקן!
        "title": "מתן מוצרי דם",
        "category": "hematology",
        "json_file": "blood_products_admin",  # שם הקובץ JSON
        "description": "פרוטוכולים למתן בטוח של מוצרי דם",
        "quiz_category": "hematology",
        "quiz_topic": "blood_products_admin",
        "min_quiz_score": 80,
        "icon": "🩸"
    }
}

def get_week_number(date=None):
    """
    מחזיר את מספר השבוע בשנה (1-52)
    """
    if date is None:
        date = datetime.now()
    return date.isocalendar()[1]

def get_current_weekly_content():
    """
    מחזיר את התוכן המומלץ לשבוע הנוכחי
    """
    week_num = get_week_number()
    # מחזור על התוכן - אם יש 8 נושאים, נחזור עליהם
    cycle_week = ((week_num - 1) % len(WEEKLY_CONTENT)) + 1
    
    content = WEEKLY_CONTENT.get(cycle_week, WEEKLY_CONTENT[1])
    content['week_number'] = week_num
    content['cycle_week'] = cycle_week
    
    return content

def get_weekly_content_by_week(week_num):
    """
    מחזיר תוכן מומלץ לשבוע מסוים
    """
    cycle_week = ((week_num - 1) % len(WEEKLY_CONTENT)) + 1
    content = WEEKLY_CONTENT.get(cycle_week, WEEKLY_CONTENT[1])
    content['week_number'] = week_num
    content['cycle_week'] = cycle_week
    return content

def get_week_start_end(date=None):
    """
    מחזיר תאריכי תחילת וסיום השבוע
    """
    if date is None:
        date = datetime.now()
    
    # תחילת השבוע (ראשון)
    start = date - timedelta(days=date.weekday() + 1)  # Python: Monday=0
    if date.weekday() == 6:  # ראשון
        start = date
    
    start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=6, hours=23, minutes=59, seconds=59)
    
    return start, end

def format_hebrew_date(date):
    """
    עיצוב תאריך בעברית
    """
    hebrew_days = ['ראשון', 'שני', 'שלישי', 'רביעי', 'חמישי', 'שישי', 'שבת']
    hebrew_months = [
        'ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני',
        'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר', 'דצמבר'
    ]
    
    day_name = hebrew_days[date.weekday()]
    month_name = hebrew_months[date.month - 1]
    
    return f"יום {day_name}, {date.day} ב{month_name} {date.year}"

def get_weekly_progress_file():
    """
    מחזיר נתיב לקובץ מעקב התקדמות שבועי (מיושן - משתמשים ב-DB)
    """
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    return data_dir / "weekly_progress.json"

def load_weekly_progress():
    """
    טוען נתוני התקדמות שבועית (fallback - ניסיון לקרוא מקובץ ישן)
    """
    file_path = get_weekly_progress_file()
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_weekly_progress(progress_data):
    """
    שומר נתוני התקדמות שבועית (מיושן - כעת נשמר ב-DB)
    נשאר רק לצורך תאימות אחורה
    """
    file_path = get_weekly_progress_file()
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(progress_data, f, ensure_ascii=False, indent=2)

def mark_weekly_content_completed(user_email, week_number=None, quiz_score=None):
    """
    מסמן שמשתמש השלים את התוכן השבועי - שומר גם ב-DB וגם בקובץ
    """
    # נרמול המייל לאותיות קטנות
    user_email = user_email.lower()
    
    if week_number is None:
        week_number = get_week_number()
    
    # תמיד נשמור בקובץ JSON תחילה (fallback מהימן)
    file_progress = load_weekly_progress()
    
    if user_email not in file_progress:
        file_progress[user_email] = {
            'completed_weeks': [],
            'badges': [],
            'total_points': 0
        }
    
    week_key = f"week_{week_number}"
    
    # בדיקה אם כבר השלים השבוע הזה
    if week_key not in file_progress[user_email]['completed_weeks']:
        file_progress[user_email]['completed_weeks'].append(week_key)
        file_progress[user_email]['total_points'] = file_progress[user_email].get('total_points', 0) + 10
        
        # הוספת תג אם עבר את הציון המינימלי
        if quiz_score and quiz_score >= 80:
            badge = {
                'week': week_number,
                'date': datetime.now().isoformat(),
                'score': quiz_score,
                'type': 'excellence'
            }
            if 'badges' not in file_progress[user_email]:
                file_progress[user_email]['badges'] = []
            file_progress[user_email]['badges'].append(badge)
    
    # שמירה בקובץ (תמיד!)
    save_weekly_progress(file_progress)
    
    # ניסיון לשמור גם ב-DB (אם זה עובד - נהדר, אם לא - לא נורא)
    try:
        from utils.database import get_user_weekly_progress, update_user_weekly_progress
        progress = file_progress[user_email]
        update_user_weekly_progress(user_email, progress)
    except Exception as e:
        print(f"Warning: Could not sync to database: {e}")
        # לא חמור - הנתונים כבר בקובץ
    
    return True

def check_weekly_completion(user_email, week_number=None):
    """
    בודק אם משתמש השלים את התוכן השבועי - קורא מהקובץ (מהימן)
    """
    # נרמול המייל לאותיות קטנות
    user_email = user_email.lower()
    
    if week_number is None:
        week_number = get_week_number()
    
    # קריאה ישירה מהקובץ (תמיד עובד)
    file_progress = load_weekly_progress()
    if user_email not in file_progress:
        return False
    
    week_key = f"week_{week_number}"
    return week_key in file_progress[user_email].get('completed_weeks', [])

def get_user_badges(user_email):
    """
    מחזיר את כל התגים של משתמש - קורא מהקובץ (מהימן)
    """
    # נרמול המייל לאותיות קטנות
    user_email = user_email.lower()
    
    # קריאה ישירה מהקובץ (תמיד עובד)
    file_progress = load_weekly_progress()
    if user_email not in file_progress:
        return []
    
    return file_progress[user_email].get('badges', [])

def get_user_weekly_stats(user_email):
    """
    מחזיר סטטיסטיקות שבועיות של משתמש - קורא מהקובץ (מהימן)
    """
    # נרמול המייל לאותיות קטנות
    user_email = user_email.lower()
    
    # קריאה ישירה מהקובץ (תמיד עובד)
    file_progress = load_weekly_progress()
    
    if user_email not in file_progress:
        return {
            'completed_weeks': 0,
            'total_badges': 0,
            'total_points': 0,
            'current_week_completed': False,
            'badges': []
        }
    
    progress = file_progress[user_email]
    current_week_completed = check_weekly_completion(user_email)
    
    return {
        'completed_weeks': len(progress.get('completed_weeks', [])),
        'total_badges': len(progress.get('badges', [])),
        'total_points': progress.get('total_points', 0),
        'current_week_completed': current_week_completed,
        'badges': progress.get('badges', [])
    }

def get_top_weekly_performers(limit=10):
    """
    מחזיר את המשתמשים המובילים בהישגים שבועיים
    """
    progress = load_weekly_progress()
    
    users_list = []
    for email, data in progress.items():
        users_list.append({
            'email': email,
            'completed_weeks': len(data.get('completed_weeks', [])),
            'total_badges': len(data.get('badges', [])),
            'total_points': data.get('total_points', 0)
        })
    
    # מיון לפי נקודות
    users_list.sort(key=lambda x: x['total_points'], reverse=True)
    
    return users_list[:limit]
