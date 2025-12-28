# 📸 מדריך הוספת תמונות לתרחישים

## ✅ התמיכה בתמונות מוכנה!

המערכת כעת תומכת בהוספת תמונות לכל שלב בתרחיש מתגלגל.

---

## 🎯 איך זה עובד?

כל שלב (stage) בתרחיש יכול להכיל שדה `"image"` שמציג תמונה בראש השלב.

---

## 📝 דוגמאות שימוש

### דוגמה 1: קובץ תמונה מקומי

```json
{
  "id": 1,
  "type": "checklist_selection",
  "title": "הכנת החדר",
  "image": "room_preparation.jpg",
  "context": {
    "text": "ילד מגיע למחלקה..."
  }
}
```

התמונה `room_preparation.jpg` צריכה להיות בתיקייה:
```
data/scenarios/images/room_preparation.jpg
```

---

### דוגמה 2: תמונה מאינטרנט (URL)

```json
{
  "id": 2,
  "type": "multiple_choice",
  "title": "אבחון ראשוני",
  "image": "https://example.com/medical-images/xray-chest.jpg",
  "context": {
    "text": "צילום החזה מראה..."
  }
}
```

---

## 📂 היכן לשים תמונות?

### אפשרות 1: קבצים מקומיים (מומלץ)
העתק קבצי תמונות לתיקייה:
```
/data/scenarios/images/
```

**שמות קבצים מומלצים:**
- `stage1_room_prep.jpg`
- `stage2_vital_signs.png`
- `stage3_xray_findings.jpg`
- `stage4_lab_results.png`

### אפשרות 2: קישורים (URLs)
השתמש בקישור ישיר לתמונה באינטרנט.

---

## 🎨 המלצות לתמונות

### גודל ואיכות
- ✅ **גודל מקסימלי:** 2-3 MB
- ✅ **רזולוציה מומלצת:** 1200x800 פיקסלים
- ✅ **יחס גובה-רוחב:** 3:2 או 16:9
- ✅ **פורמטים:** JPG, PNG, WebP, GIF

### תוכן
- ✅ תמונות ברורות ואיכותיות
- ✅ רלוונטיות למצב הקליני
- ❌ **אין** מידע מזהה של חולים
- ❌ **אין** פרטים אישיים או רגישים

---

## 💡 רעיונות לתמונות

### שלב 1: הכנת חדר
- חדר PICU מאורגן עם ציוד
- ציוד אינטובציה מוכן
- מוניטור ומכשור רפואי

### שלב 2-3: אבחון
- מוניטור עם סימנים חיוניים
- תוצאות מעבדה (ללא פרטים מזהים)
- צילומי רנטגן או CT (אנונימיים)

### שלב 4-5: טיפול
- עירוי תרופות
- התקן אוורור מכני
- הליך רפואי (אינטובציה, קו מרכזי)

### שלבי משבר
- מוניטור עם אלרמים
- מצב המודינמי לא יציב
- צוות בפעולת החייאה

---

## 🛠️ איך ליצור תמונות?

### 1. צילום (עם היתר)
צלם ציוד רפואי, חדרים, מוניטורים (ללא חולים אמיתיים).

### 2. AI - יצירת תמונות
השתמש ב-DALL-E, Midjourney, או Stable Diffusion:

**דוגמאות Prompts:**
```
"ICU room with medical equipment ready, ventilator, monitors, 
organized professional medical setting, photorealistic"

"Medical vital signs monitor showing elevated heart rate 
and low blood pressure, emergency room setting, detailed"

"Chest X-ray showing bilateral infiltrates, medical imaging, 
professional quality, anonymous patient"
```

### 3. תרשימים ואיורים
- PowerPoint / Keynote
- Canva
- Draw.io
- Medical illustration software

### 4. בנקי תמונות רפואיות
- Unsplash (medical category)
- Pexels (healthcare)
- Wikimedia Commons (medical images)
- OpenMD

---

## 📋 דוגמה מלאה

```json
{
  "stages": [
    {
      "id": 1,
      "type": "checklist_selection",
      "title": "הכנת החדר",
      "image": "stage1_icu_room.jpg",
      "time_limit": 120,
      "context": {
        "text": "🚨 ילד בן 6 מגיע ל-PICU..."
      }
    },
    {
      "id": 2,
      "type": "multiple_choice",
      "title": "בחירת טיפול ראשוני",
      "image": "stage2_vital_signs_critical.png",
      "context": {
        "text": "המטופל מגיע עם סימנים חיוניים..."
      }
    },
    {
      "id": 3,
      "type": "text_input",
      "title": "מינון תרופות",
      "image": "https://example.com/images/drug_calculation.jpg",
      "context": {
        "text": "חשב מינון אדרנלין..."
      }
    }
  ]
}
```

---

## 🧪 בדיקה

לאחר הוספת תמונה:
1. שמור את קובץ התרחיש (JSON)
2. רענן את דף התרחישים
3. התחל תרחיש
4. וודא שהתמונה מוצגת בראש השלב

---

## ❓ שאלות נפוצות

**ש: מה קורה אם שם הקובץ שגוי?**  
ת: התמונה לא תוצג, אבל התרחיש ימשיך לעבוד.

**ש: אפשר להשתמש בתמונות GIF מונפשות?**  
ת: כן! זה נתמך.

**ש: האם התמונה מוצגת גם במסך הסיכום?**  
ת: לא, רק בשלבים עצמם.

**ש: אפשר להוסיף מספר תמונות לשלב אחד?**  
ת: כרגע רק תמונה אחת לשלב. אפשר ליצור קולאז' אם צריך.

---

## 🎉 מוכן!

התמונות יעשו את התרחישים יותר אימרסיביים, מציאותיים ומושכים!

צור תיקייה עם תמונות איכותיות ותהנה מחוויית למידה משופרת! 🚀
