# תמונות לתרחישים מתגלגלים

תיקייה זו מכילה תמונות לתרחישים המתגלגלים.

## איך להוסיף תמונה לשלב בתרחיש

### דרך 1: העלאת קובץ תמונה
1. העתק את קובץ התמונה לתיקייה זו (`data/scenarios/images/`)
2. שם הקובץ צריך להיות תיאורי, לדוגמה: `room_preparation.jpg`, `patient_critical.png`
3. בקובץ התרחיש (JSON), הוסף שדה `image` לשלב:

```json
{
  "id": 1,
  "type": "checklist_selection",
  "title": "הכנת החדר",
  "image": "room_preparation.jpg",
  "context": {
    "text": "..."
  }
}
```

### דרך 2: שימוש ב-URL
אם התמונה מאוחסנת באינטרנט, אפשר להשתמש ב-URL ישירות:

```json
{
  "id": 2,
  "type": "multiple_choice",
  "title": "בחירת טיפול",
  "image": "https://example.com/images/patient_xray.jpg",
  "context": {
    "text": "..."
  }
}
```

## פורמטים נתמכים
- JPG / JPEG
- PNG
- GIF
- WebP

## המלצות
- גודל תמונה מומלץ: עד 2MB
- רזולוציה: 1200x800 פיקסלים (או יחס גובה-רוחב דומה)
- השתמש בתמונות איכותיות שממחישות את המצב הקליני
- וודא שהתמונות לא מכילות מידע מזהה של חולים אמיתיים

## דוגמאות לתמונות שימושיות
- חדר PICU עם ציוד מוכן
- מוניטור עם סימנים חיוניים
- צילומי רנטגן / CT (אנונימיים)
- ממצאים פיזיקליים (פטכיות, בצקת, וכו')
- ציוד רפואי (אינטובציה, קטטרים, וכו')
- תרשימי זרימה (אלגוריתמים)

## יצירת תמונות
אפשר להשתמש ב:
1. **צילומי אילוסטרציה** מספרות רפואית (בהיתר)
2. **תמונות AI** - DALL-E, Midjourney, Stable Diffusion
3. **תרשימים** שנוצרו ב-PowerPoint/Canva
4. **צילומי מסך** ממסמכים רפואיים (ללא מידע מזהה)

### דוגמה ליצירת תמונה עם AI:
```
Prompt: "Hospital ICU room preparation with medical equipment, 
monitors, ventilator, IV poles, organized and ready, 
medical illustration style, clean professional"
```
