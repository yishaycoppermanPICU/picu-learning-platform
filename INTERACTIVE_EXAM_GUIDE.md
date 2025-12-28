# 🩺 סימולטור בדיקה פיזיקלית אינטראקטיבי

## 🎯 מה זה?

מרכיב חדש שמאפשר **בדיקה פיזיקלית אינטראקטיבית** של מטופל וירטואלי!

---

## ✨ תכונות

### 👆 אזורים אינטראקטיביים (Hotspots):
1. **🧠 מרפק (Fontanelle)** - בולט/שקוע/נורמלי
2. **👁️ אישונים (Pupils)** - גודל, תגובה לאור, אסימטריה
3. **🫀 לב (Heart)** - האזנה, קולות לב, אוושה
4. **🤚 בטן (Abdomen)** - קשיות, רגישות, הגנה
5. **💧 נקז חזה (Chest Drain)** - תפוקה, צבע
6. **🩸 עור (Skin)** - צבע, פטכיות, טורגור

---

## 📖 איך להשתמש?

### בתרחיש JSON:

```json
{
  "id": 2,
  "type": "interactive_examination",
  "title": "בדיקה פיזיקלית",
  "patient_findings": {
    "fontanelle": {
      "description": "מרפק בולט",
      "status_class": "abnormal",
      "interpretation": "עליה בלחץ תוך גולגולתי"
    },
    "pupils": {
      "left": {
        "size": 3,
        "reactive": true
      },
      "right": {
        "size": 6,
        "reactive": false
      }
    },
    "abdomen": {
      "rigidity": "קשה וכואבת",
      "rigidity_class": "critical",
      "tenderness": "רגישות חמורה, הילד צורח",
      "guarding": "כן - הגנה בולטת"
    },
    "heart": {
      "sounds": "S1+S2 תקינים, טכיקרדיה",
      "murmur": "אין"
    },
    "chest_drain": {
      "output": "150 ml/hr",
      "status_class": "critical",
      "color": "דם טרי (bright red)"
    },
    "skin": {
      "color": "חיוור ומנומר",
      "petechiae": "פטכיות מפושטות בחזה ובגפיים",
      "petechiae_class": "critical",
      "turgor": "ירוד - סימן להתייבשות"
    }
  }
}
```

---

## 🎨 התאמה אישית

### סטטוסים (Classes):
- `status-normal` - ירוק (תקין)
- `status-abnormal` - צהוב/כתום (לא תקין)
- `status-critical` - אדום (קריטי)

### דוגמה לממצא מורכב:

```json
"pupils": {
  "left": {
    "size": 3,
    "reactive": true,
    "description": "אישון שמאל תקין - 3mm מגיב לאור"
  },
  "right": {
    "size": 7,
    "reactive": false,
    "description": "אישון ימין מורחב - 7mm אינו מגיב לאור",
    "note": "⚠️ חשד ל-Uncal Herniation"
  }
}
```

---

## 🔧 שילוב בקוד Python

```python
from utils.interactive_patient import create_interactive_patient

# הגדרת ממצאים
patient_data = {
    'fontanelle': {
        'description': 'מרפק בולט',
        'status_class': 'critical',
        'interpretation': 'עליית לחץ תוך גולגולתי משמעותית'
    },
    'pupils': {
        'left': {'size': 3, 'reactive': True},
        'right': {'size': 7, 'reactive': False}
    },
    # ... שאר הממצאים
}

# הצגת המרכיב האינטראקטיבי
create_interactive_patient(patient_data)
```

---

## 🎬 שילוב בתרחיש מתגלגל

בקובץ `pages/7_🎬_Scenarios.py`, הוסף טיפול בשלב מסוג `interactive_examination`:

```python
if stage.get('type') == 'interactive_examination':
    st.markdown("### 🩺 בדיקה פיזיקלית")
    st.info("לחץ על אזורים שונים בגוף לבדיקה")
    
    from utils.interactive_patient import create_interactive_patient
    patient_findings = stage.get('patient_findings', {})
    create_interactive_patient(patient_findings)
```

---

## 💡 רעיונות לשיפור עתידי

1. **אנימציות:**
   - אישונים שמתכווצים בלחיצה (סימולציה של פנס)
   - חזה שעולה ויורד (נשימה)
   - דופק מהבהב

2. **קול:**
   - סאונד של קולות לב (auscultation)
   - קולות נשימה (wheezing, crackles)

3. **אזורים נוספים:**
   - טונוס שרירים (hypertonic/hypotonic)
   - רפלקסים (DTRs)
   - נפיחות מפרקים
   - עמוד שדרה

4. **תמונות אמיתיות:**
   - במקום SVG, השתמש בציור/תמונה של ילד
   - Overlay של hotspots שקופים

---

## 🎯 דוגמה מלאה לתרחיש

```json
{
  "scenario_id": "interactive_exam_01",
  "title": "תרחיש מתגלגל 2",
  "stages": [
    {
      "id": 1,
      "type": "context",
      "title": "רקע",
      "context": {
        "text": "ילד בן 6 הגיע ל-PICU לאחר התמוטטות במיון..."
      }
    },
    {
      "id": 2,
      "type": "interactive_examination",
      "title": "בדיקה פיזיקלית",
      "instructions": "בצע בדיקה פיזיקלית מלאה. לחץ על כל אזור לבדיקה.",
      "patient_findings": {
        "fontanelle": {
          "description": "מרפק שקוע",
          "status_class": "critical",
          "interpretation": "התייבשות חמורה"
        },
        "pupils": {
          "left": {"size": 5, "reactive": false},
          "right": {"size": 5, "reactive": false}
        },
        "abdomen": {
          "rigidity": "רכה",
          "rigidity_class": "normal",
          "tenderness": "אין רגישות",
          "guarding": "אין"
        },
        "heart": {
          "sounds": "טכיקרדיה 180, קולות עמומים",
          "murmur": "אין"
        },
        "chest_drain": {
          "output": "אין נקז",
          "status_class": "normal",
          "color": "N/A"
        },
        "skin": {
          "color": "חיוור, קר וליח",
          "petechiae": "פטכיות מפושטות",
          "petechiae_class": "critical",
          "turgor": "טורגור ירוד מאוד"
        }
      }
    }
  ]
}
```

---

## 🚀 הבא

כעת תוכל:
1. ליצור תרחישים עם בדיקות פיזיקליות אינטראקטיביות
2. להתאים ממצאים לפי המצב הקליני
3. לאפשר לסטודנטים "לגעת" ולבדוק את המטופל

**זה משנה את חוויית הלמידה ל-hands-on!** 🎉
