-- PICU Learning Platform Database Schema
-- Create tables for content management

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop existing tables if they exist (careful - this deletes data!)
-- DROP TABLE IF EXISTS quiz_results CASCADE;
-- DROP TABLE IF EXISTS quiz_questions CASCADE;
-- DROP TABLE IF EXISTS content_sections CASCADE;
-- DROP TABLE IF EXISTS content_items CASCADE;
-- DROP TABLE IF EXISTS users CASCADE;
-- DROP TABLE IF EXISTS institutions CASCADE;

-- Content Items Table (main topics/articles)
CREATE TABLE IF NOT EXISTS content_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    slug TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    subtitle TEXT,
    description TEXT,
    clinical_definition TEXT,
    tags TEXT[], -- Array of tags for searching/filtering
    icon TEXT, -- Emoji or icon identifier
    order_index INTEGER DEFAULT 0,
    is_published BOOLEAN DEFAULT true,
    created_by TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Content Sections Table (subsections within content items)
CREATE TABLE IF NOT EXISTS content_sections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content_item_id UUID NOT NULL REFERENCES content_items(id) ON DELETE CASCADE,
    section_type TEXT NOT NULL, -- 'text', 'list', 'table', 'alert', 'steps', 'options'
    title TEXT NOT NULL,
    content TEXT, -- Markdown content
    metadata JSONB, -- For additional structured data (options, steps, etc.)
    order_index INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Users Table (if not already exists)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE,
    full_name TEXT NOT NULL,
    institution TEXT,
    role TEXT DEFAULT 'user', -- 'user', 'editor', 'admin'
    score INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE
);

-- Institutions Table
CREATE TABLE IF NOT EXISTS institutions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT UNIQUE NOT NULL,
    name_he TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Quiz Questions Table (linked to content items)
CREATE TABLE IF NOT EXISTS quiz_questions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content_item_id UUID REFERENCES content_items(id) ON DELETE SET NULL,
    question_text TEXT NOT NULL,
    question_type TEXT NOT NULL DEFAULT 'multiple_choice', -- 'multiple_choice', 'true_false', 'open'
    options JSONB, -- Array of answer options with correct flag
    correct_answer TEXT,
    explanation TEXT, -- Markdown explanation
    difficulty TEXT DEFAULT 'medium', -- 'easy', 'medium', 'hard'
    tags TEXT[],
    points INTEGER DEFAULT 1,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Quiz Results Table (track user performance)
CREATE TABLE IF NOT EXISTS quiz_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    question_id UUID REFERENCES quiz_questions(id) ON DELETE CASCADE,
    content_item_id UUID REFERENCES content_items(id) ON DELETE SET NULL,
    is_correct BOOLEAN,
    user_answer TEXT,
    time_spent_seconds INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_content_items_category ON content_items(category);
CREATE INDEX IF NOT EXISTS idx_content_items_slug ON content_items(slug);
CREATE INDEX IF NOT EXISTS idx_content_sections_item ON content_sections(content_item_id, order_index);
CREATE INDEX IF NOT EXISTS idx_quiz_questions_item ON quiz_questions(content_item_id);
CREATE INDEX IF NOT EXISTS idx_quiz_results_user ON quiz_results(user_id);
CREATE INDEX IF NOT EXISTS idx_quiz_results_question ON quiz_results(question_id);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Add triggers for updated_at
CREATE TRIGGER update_content_items_updated_at
    BEFORE UPDATE ON content_items
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_content_sections_updated_at
    BEFORE UPDATE ON content_sections
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_quiz_questions_updated_at
    BEFORE UPDATE ON quiz_questions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Row Level Security (RLS) - Disable first to avoid conflicts
ALTER TABLE IF EXISTS content_items DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS content_sections DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS quiz_questions DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS users DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS quiz_results DISABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Allow public read access on content_items" ON content_items;
DROP POLICY IF EXISTS "Allow public read access on content_sections" ON content_sections;
DROP POLICY IF EXISTS "Allow public read access on quiz_questions" ON quiz_questions;
DROP POLICY IF EXISTS "Allow insert quiz_results" ON quiz_results;
DROP POLICY IF EXISTS "Allow all on content_items" ON content_items;
DROP POLICY IF EXISTS "Allow all on content_sections" ON content_sections;
DROP POLICY IF EXISTS "Allow all on quiz_questions" ON quiz_questions;
DROP POLICY IF EXISTS "Allow all on users" ON users;

-- Enable Row Level Security
ALTER TABLE content_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_sections ENABLE ROW LEVEL SECURITY;
ALTER TABLE quiz_questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE quiz_results ENABLE ROW LEVEL SECURITY;

-- Create policies for public read access
CREATE POLICY "Allow public read access on content_items"
    ON content_items FOR SELECT
    USING (is_published = true);

CREATE POLICY "Allow public read access on content_sections"
    ON content_sections FOR SELECT
    USING (true);

CREATE POLICY "Allow public read access on quiz_questions"
    ON quiz_questions FOR SELECT
    USING (is_active = true);

-- Allow authenticated users to insert quiz results
CREATE POLICY "Allow insert quiz_results"
    ON quiz_results FOR INSERT
    WITH CHECK (true);

-- Allow all operations for now (you can restrict later)
CREATE POLICY "Allow all on content_items"
    ON content_items FOR ALL
    USING (true);

CREATE POLICY "Allow all on content_sections"
    ON content_sections FOR ALL
    USING (true);

CREATE POLICY "Allow all on quiz_questions"
    ON quiz_questions FOR ALL
    USING (true);

CREATE POLICY "Allow all on users"
    ON users FOR ALL
    USING (true);
