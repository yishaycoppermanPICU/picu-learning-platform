-- הוספות לטבלאות הקיימות של PICU Learning Platform
-- רק מה שחסר, ללא מחיקת טבלאות קיימות!

-- הוספת עמודות לטבלת topics (אם לא קיימות)
DO $$ 
BEGIN
    -- בדיקה והוספת עמודת category
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name='topics' AND column_name='category') THEN
        ALTER TABLE topics ADD COLUMN category TEXT;
    END IF;
    
    -- בדיקה והוספת עמודת slug
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name='topics' AND column_name='slug') THEN
        ALTER TABLE topics ADD COLUMN slug TEXT;
    END IF;
    
    -- בדיקה והוספת עמודת tags
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name='topics' AND column_name='tags') THEN
        ALTER TABLE topics ADD COLUMN tags TEXT[];
    END IF;
    
    -- בדיקה והוספת עמודת content_type
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name='topics' AND column_name='content_type') THEN
        ALTER TABLE topics ADD COLUMN content_type TEXT DEFAULT 'topic';
    END IF;
END $$;

-- טבלת מקטעי תוכן (חדשה - לתוכן מפורט עם subsections)
CREATE TABLE IF NOT EXISTS topic_sections (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    topic_id UUID REFERENCES topics(id) ON DELETE CASCADE,
    section_type TEXT NOT NULL, -- 'text', 'list', 'steps', 'options', 'table'
    title TEXT NOT NULL,
    content TEXT,
    metadata JSONB,
    order_index INTEGER NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- אינדקסים לביצועים
CREATE INDEX IF NOT EXISTS idx_topic_sections_topic ON topic_sections(topic_id, order_index);
CREATE INDEX IF NOT EXISTS idx_topics_category ON topics(category);
CREATE INDEX IF NOT EXISTS idx_topics_slug ON topics(slug);

-- Trigger לעדכון updated_at
CREATE OR REPLACE FUNCTION update_topic_sections_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_topic_sections_updated_at ON topic_sections;
CREATE TRIGGER update_topic_sections_updated_at
    BEFORE UPDATE ON topic_sections
    FOR EACH ROW
    EXECUTE FUNCTION update_topic_sections_updated_at();

-- הוספת הרשאות (RLS)
ALTER TABLE topic_sections ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "allow_all_topic_sections" ON topic_sections;
CREATE POLICY "allow_all_topic_sections" 
    ON topic_sections FOR ALL 
    USING (true);
