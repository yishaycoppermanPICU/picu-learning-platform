-- מחיקת כל הנושאים למעט פאנציטופניה
-- ID של פאנציטופניה: b21b1fe0-577c-4904-989e-f88f501abf45

-- מחיקת כל הנושאים שאינם פאנציטופניה
DELETE FROM topics 
WHERE id != 'b21b1fe0-577c-4904-989e-f88f501abf45';

-- מחיקת כל השאלות שלא קשורות לפאנציטופניה
DELETE FROM questions 
WHERE topic_id != 'b21b1fe0-577c-4904-989e-f88f501abf45';

-- ניקוי תוצאות quiz (כיוון שאין משתמשים)
TRUNCATE TABLE quiz_results;
