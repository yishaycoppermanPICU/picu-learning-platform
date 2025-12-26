# PICU Learning Platform - Content Library

## Structure

```
data/content/
├── hematology/          # Hematology/Oncology topics
│   └── pancytopenia.json
├── respiratory/         # Respiratory topics (future)
├── cardiology/          # Cardiology topics (future)
└── metadata/            # Category metadata
```

## Content Format

Each topic is stored as a JSON file with the following structure:

```json
{
  "id": "topic-id",
  "title": "Topic Title in Hebrew",
  "description": "Short description",
  "category": "category-id",
  "difficulty": "beginner|intermediate|advanced",
  "order": 1,
  "tags": ["tag1", "tag2"],
  "content": [...],
  "key_points": [...],
  "last_updated": "YYYY-MM-DD",
  "author": "Author Name"
}
```

## Content Types

- **definition**: Blue box with definition text
- **section**: Expandable sections with structured items
- **treatment**: Green boxes with treatment protocols
- **key_points**: Yellow highlighted box with bullet points
- **table**: Data tables

## Adding New Content

1. Create JSON file in appropriate category folder
2. Follow the schema above
3. Content will automatically appear in the Library

## Categories

- 🩸 **Hematology/Oncology**: Blood disorders and cancer in children
