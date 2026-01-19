# PICU Learning Platform - AI Coding Agent Guide

## Project Overview
Educational platform for Pediatric Intensive Care Unit (PICU) medical training. Built with Streamlit, featuring Hebrew RTL interface, medical content library, interactive quizzes, clinical scenarios, and gamification with weekly challenges and achievement badges.

## Architecture & Data Flow

### Hybrid Storage System
- **Database (Supabase/PostgreSQL)**: Primary storage for structured data (users, institutions, quiz results, metadata)
- **JSON Files**: Content storage in `data/` directory for portability and version control
  - `data/content/{category}/*.json` - Medical content organized by category
  - `data/questions.json` - Quiz questions database
  - `data/users.json`, `data/editors.json`, `data/weekly_progress.json` - User data
- **Migration**: System is transitioning from JSON-only to hybrid model (see `MIGRATION_GUIDE.md`)

### Core Components
1. **Main App** (`app.py`): Landing page with authentication, weekly content display, and navigation
2. **Pages** (`pages/*.py`): Streamlit multipage app using Hebrew filenames
   - `1_ספריית_תוכן.py` - Content library browser
   - `5_בחנים.py` - Quiz system
   - `6_תרחישים.py` - Interactive clinical scenarios
   - `8_⚙️_Admin.py` - Content management (editor role required)
   - `9_✏️_Content_Editor.py` - Database content editor
3. **Utils** (`utils/*.py`): Shared functionality
   - `content_manager.py` - JSON-based content CRUD operations
   - `database.py` - Supabase client and database operations
   - `quiz_manager.py` - Quiz logic and result tracking
   - `weekly_content.py` - Weekly challenge system
   - `badges.py` - Achievement badge system
   - `interactive_patient.py` - Clinical scenario rendering

## Critical Patterns & Conventions

### 1. Hebrew RTL Support
**Every page MUST include:**
```python
st.set_page_config(page_icon="🏥", layout="wide")
st.markdown(get_common_styles(), unsafe_allow_html=True)
```
- `get_common_styles()` provides RTL CSS, custom color scheme (`--navy`, `--teal`, `--orange-accent`), and consistent styling
- All user-facing text is in Hebrew; code comments can be Hebrew or English

### 2. Session State Management
Critical session state variables initialized in `app.py`:
```python
st.session_state.logged_in  # Boolean - authentication status
st.session_state.user       # Dict - user data (username, email, full_name, institution)
st.session_state.user_scores  # List - quiz performance history
```
- **Authentication**: Uses cookie-based email persistence via `extra_streamlit_components.CookieManager`
- Call `restore_user_session(st)` in pages to restore login state after navigation

### 3. Content Structure Convention
Medical content JSON follows strict schema (see `data/content/` examples):
```json
{
  "id": "uuid-v4",
  "title": "Hebrew title",
  "category": "hematology|cardiology|resuscitation|trauma|etc",
  "subtitle": "Brief description",
  "sections": [
    {
      "title": "Section title",
      "type": "text|list|table|alert|steps|options",
      "content": "Markdown or JSON-structured content",
      "metadata": {}
    }
  ],
  "clinical_definition": "Medical definition",
  "tags": ["tag1", "tag2"]
}
```

### 4. Database Fallback Pattern
Always wrap database calls with fallback to JSON:
```python
try:
    from utils.database import get_topics, DB_CONNECTED
    if DB_CONNECTED:
        topics = get_topics(category)
    else:
        topics = get_category_topics(category)  # JSON fallback
except Exception:
    topics = get_category_topics(category)  # JSON fallback
```

### 5. Weekly Content System
- Defined in `utils/weekly_content.py` with hardcoded week-to-topic mapping
- Week calculation: `(datetime.now() - PROGRAM_START_DATE).days // 7 + 1`
- Users earn badges by completing weekly content + quiz with 80%+ score
- Check user progress via `data/weekly_progress.json` or Supabase `user_weekly_progress` table

## Developer Workflows

### Running the App
```bash
streamlit run app.py
# Auto-starts on port 8501 via devcontainer postAttachCommand
```

### Database Setup
1. SQL schema: `create_tables.sql` (run manually in Supabase SQL Editor)
2. Test connection: `python test_connection.py`
3. Migration scripts: `migrate_content.py`, `migrate_weekly_progress.py`

### Adding Medical Content
Two approaches:
1. **Script approach**: Create `add_{topic}.py` following pattern in `add_sepsis.py`, `add_hlh.py`
   - Constructs JSON structure programmatically
   - Saves to `data/content/{category}/{slug}.json`
2. **Admin UI**: Use page 9 (Content Editor) - requires editor role in `data/editors.json`

### Quiz Management
- Questions stored in `data/questions.json` with structure:
  ```json
  {
    "category": "category_id",
    "topic": "topic_id",
    "question": "Question text",
    "options": ["A", "B", "C", "D"],
    "correct": 0,  # index
    "explanation": "Why this answer"
  }
  ```
- Add quiz scripts: `add_{topic}_quiz.py` files
- Results tracked in `data/quiz_results/` (JSON) and `quiz_results` table (Supabase)

### Styling & CSS
- Central styles: `utils/styles.py` exports `get_common_styles()`
- Color palette CSS variables: `--navy`, `--slate`, `--teal`, `--teal-light`, `--orange-accent`, `--danger`
- Page-specific styles: Embedded in page files with `st.markdown("<style>...", unsafe_allow_html=True)`

## Common Pitfalls

1. **Missing RTL styles**: Always import and apply `get_common_styles()` - UI will break without it
2. **Session state not restored**: Pages must call `restore_user_session(st)` or auth state is lost
3. **Hardcoded paths**: Use `Path(__file__).parent` for relative paths, not `./` or `../`
4. **Database credentials**: Already configured in `utils/database.py` - never commit new credentials
5. **JSON encoding**: Always use `encoding='utf-8'` when reading/writing Hebrew content
6. **Streamlit multipage**: Page order determined by filename prefix (1_, 2_, etc.), not by code

## Integration Points

- **Supabase**: Connection via `init_supabase()` in `utils/database.py`
- **External auth**: Cookie manager for email persistence across sessions
- **Static files**: Images in `data/scenarios/images/`, sounds in `data/sounds/`
- **Markdown rendering**: Content supports full markdown in `section.content` fields

## Testing Shortcuts

- Check database: `python test_connection.py`
- Verify content structure: `python check_content.py`
- Reset user stats: `python reset_statistics.py`
- SQL operations: `python run_sql.py` (interactive SQL runner)

## Role-Based Access
- **Users**: All registered users can access content and quizzes
- **Editors**: Listed in `data/editors.json`, access Admin panel (page 8) and Content Editor (page 9)
- Check editor status: `is_editor(email)` from `utils/content_manager`
