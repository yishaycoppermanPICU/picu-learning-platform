# הוראות להוספת עמודת weekly_progress

## שלב 1: הוספת העמודה ב-Supabase

1. גש ל-Supabase Dashboard: https://xdzpnlqzlopxgktltvif.supabase.co
2. לחץ על **SQL Editor** בתפריט השמאלי
3. לחץ על **New Query**
4. העתק והדבק את הקוד הבא:

```sql
-- הוספת עמודה לשמירת התקדמות שבועית
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS weekly_progress JSONB DEFAULT '{
    "completed_weeks": [],
    "badges": [],
    "total_points": 0
}'::jsonb;

-- יצירת אינדקס לשיפור ביצועים
CREATE INDEX IF NOT EXISTS idx_users_weekly_progress ON users USING gin(weekly_progress);
```

5. לחץ על **RUN** (או Ctrl+Enter)
6. וודא שקיבלת הודעת הצלחה

## שלב 2: העברת נתונים קיימים (אם יש)

אם יש לך משתמשים עם נתוני התקדמות שבועית בקובץ JSON, הרץ:

```bash
python migrate_weekly_progress.py
```

## שלב 3: אתחול מחדש של השרת

```bash
pkill -f streamlit && sleep 2 && python -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &
```

## מה השתנה?

- **לפני**: נתוני ההתקדמות השבועית נשמרו בקובץ JSON מקומי (`data/weekly_progress.json`)
  - בעיה: כל מכשיר שומר נתונים נפרדים, אין סנכרון בין מחשב לטלפון
  
- **אחרי**: נתונים נשמרים בטבלת `users` במסד הנתונים Supabase
  - יתרון: סנכרון אוטומטי בין כל המכשירים (מחשב, טלפון, טאבלט)
  - יתרון: גיבוי אוטומטי, ניתן לשחזר נתונים

## מבנה הנתונים ב-weekly_progress

```json
{
  "completed_weeks": ["week_1", "week_2", "week_3"],
  "badges": [
    {
      "week": 1,
      "date": "2024-12-27T10:00:00",
      "score": 85,
      "type": "excellence"
    }
  ],
  "total_points": 30
}
```

## בדיקה

לאחר ההרצה, כל משתמש שמתחבר למערכת יראה את אותם הנתונים בכל המכשירים:
- תגי הצטיינות
- אתגרים שבועיים שבוצעו
- סטטיסטיקות נקודות

