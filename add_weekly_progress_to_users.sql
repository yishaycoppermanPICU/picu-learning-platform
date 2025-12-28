-- הוספת עמודה לשמירת התקדמות שבועית בטבלת המשתמשים
-- Adding weekly progress column to users table for cross-device sync

ALTER TABLE users 
ADD COLUMN IF NOT EXISTS weekly_progress JSONB DEFAULT '{
    "completed_weeks": [],
    "badges": [],
    "total_points": 0
}'::jsonb;

-- יצירת אינדקס לשיפור ביצועים
CREATE INDEX IF NOT EXISTS idx_users_weekly_progress ON users USING gin(weekly_progress);

-- הערות:
-- השדה weekly_progress יכיל:
-- {
--   "completed_weeks": ["week_1", "week_2", ...],
--   "badges": [
--     {"week": 1, "date": "2024-01-01T10:00:00", "score": 85, "type": "excellence"},
--     ...
--   ],
--   "total_points": 50
-- }
