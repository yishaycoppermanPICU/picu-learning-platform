-- PICU Learning Platform Database Schema - CLEAN VERSION
-- Run this after running drop_tables.sql

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Content Items Table (main topics/articles)
CREATE TABLE content_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    slug TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    subtitle TEXT,
    description TEXT,
    clinical_definition TEXT,
    tags TEXT[],
    icon TEXT,
    order_index INTEGER DEFAULT 0,
    is_published BOOLEAN DEFAULT true,
    created_by TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Content Sections Table
CREATE TABLE content_sections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content_item_id UUID NOT NULL REFERENCES content_items(id) ON DELETE CASCADE,
    section_type TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT,
    metadata JSONB,
    order_index INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE,
    full_name TEXT NOT NULL,
    institution TEXT,
    role TEXT DEFAULT 'user',
    score INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE
);

-- 4. Institutions Table
CREATE TABLE institutions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT UNIQUE NOT NULL,
    name_he TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. Quiz Questions Table
CREATE TABLE quiz_questions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content_item_id UUID REFERENCES content_items(id) ON DELETE SET NULL,
    question_text TEXT NOT NULL,
    question_type TEXT NOT NULL DEFAULT 'multiple_choice',
    options JSONB,
    correct_answer TEXT,
    explanation TEXT,
    difficulty TEXT DEFAULT 'medium',
    tags TEXT[],
    points INTEGER DEFAULT 1,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 6. Quiz Results Table
CREATE TABLE quiz_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    question_id UUID REFERENCES quiz_questions(id) ON DELETE CASCADE,
    content_item_id UUID REFERENCES content_items(id) ON DELETE SET NULL,
    is_correct BOOLEAN,
    user_answer TEXT,
    time_spent_seconds INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_content_items_category ON content_items(category);
CREATE INDEX idx_content_items_slug ON content_items(slug);
CREATE INDEX idx_content_sections_item ON content_sections(content_item_id, order_index);
CREATE INDEX idx_quiz_questions_item ON quiz_questions(content_item_id);
CREATE INDEX idx_quiz_results_user ON quiz_results(user_id);
CREATE INDEX idx_quiz_results_question ON quiz_results(question_id);

-- Create trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Add triggers
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

-- Enable RLS
ALTER TABLE content_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_sections ENABLE ROW LEVEL SECURITY;
ALTER TABLE quiz_questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE quiz_results ENABLE ROW LEVEL SECURITY;

-- Create policies - allow all for now
CREATE POLICY "allow_all_content_items" ON content_items FOR ALL USING (true);
CREATE POLICY "allow_all_content_sections" ON content_sections FOR ALL USING (true);
CREATE POLICY "allow_all_quiz_questions" ON quiz_questions FOR ALL USING (true);
CREATE POLICY "allow_all_users" ON users FOR ALL USING (true);
CREATE POLICY "allow_all_quiz_results" ON quiz_results FOR ALL USING (true);
