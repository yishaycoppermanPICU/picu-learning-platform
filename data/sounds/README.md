# קבצי סאונד לתרחישים

## קבצים נדרשים
העלה קבצי אודיו אמיתיים לתיקייה זו:

### צלילי מוניטור
- `qrs_beep.mp3` או `qrs_beep.wav` - צפצוף QRS מוניטור לב (קצר, חד)
- `spo2_high.mp3` - טון SpO2 גבוה (95-100%)
- `spo2_medium.mp3` - טון SpO2 בינוני (90-94%)
- `spo2_low.mp3` - טון SpO2 נמוך (<90%)

### התראות
- `alarm_critical.mp3` - התראה קריטית (3 צפצופים)
- `alarm_warning.mp3` - אזהרה
- `ventilator_alarm.mp3` - התראת מכשיר הנשמה

### רקע
- `ventilator_breath.mp3` - קול נשימה של מכשיר הנשמה (רקע עדין)

## מקורות מומלצים
1. חפש ב-YouTube "ICU monitor sounds" והורד את הצלילים
2. FreeSound.org - חפש "hospital monitor", "ECG beep", "ventilator"
3. SoundBible.com - צלילי בית חולים

## המרת קבצים
אם יש לך קבצי WAV, המר ל-MP3 עם:
```bash
ffmpeg -i input.wav -codec:a libmp3lame -b:a 128k output.mp3
```
