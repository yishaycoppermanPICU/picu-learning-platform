# 🎨 מדריך שילוב תמונת רקע PICU

## 📸 איך להוסיף תמונת רקע לתרחיש?

### שלב 1: הוספת התמונה
שים את התמונה בתיקייה:
```
data/scenarios/images/picu_background.jpg
```

### שלב 2: בקובץ התרחיש
הוסף את השדה הבא ברמת השורש של התרחיש:

```json
{
  "scenario_id": "hidden_enemy_01",
  "title": "תרחיש מתגלגל 1",
  "background_image": "picu_background.jpg",
  ...
}
```

---

## 🎨 המלצות לתמונה

### גודל ורזולוציה:
- **רזולוציה:** 1920x1080 או יותר
- **גודל קובץ:** עד 5MB
- **פורמט:** JPG, PNG, WebP

### תוכן התמונה:
- ✅ יחידת טיפול נמרץ ילדים ריקה
- ✅ מוניטורים, משאבות עירוי, ציוד רפואי
- ✅ תאורה מקצועית
- ❌ ללא מטופלים או צוות רפואי מזוהה
- ❌ ללא מידע מזהה של בית חולים

### עיבוד התמונה:
- הוסף **שכבת כהייה** (overlay) כדי שהטקסט יהיה קריא
- המערכת תוסיף אוטומטית:
  - שכבה שקופה כהה (40% opacity)
  - טשטוש קל (blur) ברקע
  - גרדיאנט למעבר חלק

---

## 🖼️ דוגמת שימוש

```json
{
  "scenario_id": "hidden_enemy_01",
  "title": "תרחיש מתגלגל 1",
  "description": "תרחיש קליני מורכב",
  "background_image": "picu_room.jpg",
  "background_settings": {
    "overlay_opacity": 0.4,
    "blur_amount": 2,
    "gradient": true
  }
}
```

---

## 💡 איפה להשיג תמונות?

### 1. צילום עצמי (מומלץ!)
- צלם את יחידת הטיפול הנמרץ במחלקה
- וודא שאין חולים או צוות מזוהה
- שעות הערב/לילה - פחות אנשים

### 2. בנקי תמונות חופשיים
- **Unsplash:** https://unsplash.com/s/photos/icu
- **Pexels:** https://www.pexels.com/search/hospital/
- **Pixabay:** https://pixabay.com/images/search/intensive-care/

### 3. AI (DALL-E, Midjourney)
Prompt דוגמה:
```
"Modern pediatric ICU room, empty, medical equipment, 
monitors, IV pumps, professional lighting, realistic, 
photorealistic, hospital setting, no people"
```

---

## 🔧 השלבים הטכניים

### הקוד מטפל אוטומטית:
1. ✅ טוען את התמונה מהתיקייה
2. ✅ מוסיף שכבת כהייה
3. ✅ מיישם טשטוש קל
4. ✅ מוסיף גרדיאנט
5. ✅ מוודא שהטקסט קריא

### אין צורך לעבד את התמונה בעצמך!

---

## 📤 שליחת התמונה

כשתהיה מוכן, פשוט שלח את התמונה ואני:
1. אשמור אותה בתיקייה הנכונה
2. אוסיף את השדה בקובץ התרחיש
3. אוודא שהעיצוב עובד בצורה מושלמת

**העיצוב החדש כבר מוכן לקבל את התמונה!** 🎨✨
