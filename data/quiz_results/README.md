# Quiz Results Directory

This directory stores user quiz results.
Each user has their own JSON file named: `{email}_at_{domain}.json`

## Structure:
```json
{
  "email": "user@example.com",
  "quizzes": [
    {
      "quiz_id": "unique_id",
      "date": "2025-12-26 10:30:00",
      "category": "hematology",
      "total_questions": 10,
      "correct_answers": 8,
      "score_percentage": 80,
      "time_taken": 300
    }
  ]
}
```
