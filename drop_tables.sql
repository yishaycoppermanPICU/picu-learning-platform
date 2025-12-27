-- Drop all tables - USE WITH CAUTION!
-- This will delete all data

DROP TABLE IF EXISTS quiz_results CASCADE;
DROP TABLE IF EXISTS quiz_questions CASCADE;
DROP TABLE IF EXISTS content_sections CASCADE;
DROP TABLE IF EXISTS content_items CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS institutions CASCADE;

-- Drop triggers
DROP TRIGGER IF EXISTS update_content_items_updated_at ON content_items;
DROP TRIGGER IF EXISTS update_content_sections_updated_at ON content_sections;
DROP TRIGGER IF EXISTS update_quiz_questions_updated_at ON quiz_questions;

-- Drop function
DROP FUNCTION IF EXISTS update_updated_at_column();
