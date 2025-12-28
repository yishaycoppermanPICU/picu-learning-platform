# -*- coding: utf-8 -*-
"""
Database module for PICU Learning Platform
Manages all interactions with Supabase PostgreSQL database
"""

import os
from supabase import create_client, Client
from typing import Optional, List, Dict, Any

# Supabase credentials
SUPABASE_URL = "https://xdzpnlqzlopxgktltvif.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhkenBubHF6bG9weGdrdGx0dmlmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjY2OTI5MjgsImV4cCI6MjA4MjI2ODkyOH0.TJ4K4kqBhmb6JQo7iZAfC4UvI019JYhLLnM2NDVdA6k"

_supabase_client: Optional[Client] = None

def init_supabase() -> Optional[Client]:
    """Initialize Supabase client"""
    global _supabase_client, DB_CONNECTED
    
    if _supabase_client:
        return _supabase_client
    
    try:
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        DB_CONNECTED = True
        return _supabase_client
    except Exception as e:
        print(f"Failed to initialize Supabase: {e}")
        return None

DB_CONNECTED = init_supabase() is not None

def get_institutions() -> List[Dict]:
    """Get all institutions"""
    try:
        supabase = init_supabase()
        if not supabase:
            return []
        response = supabase.table('institutions').select("*").order('name').execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error getting institutions: {e}")
        return []

def get_topics(category: Optional[str] = None) -> List[Dict]:
    """Get all topics, optionally filtered by category"""
    try:
        supabase = init_supabase()
        if not supabase:
            return []
        
        query = supabase.table('topics').select("*")
        if category:
            query = query.eq('category', category)
        
        response = query.order('order_index').execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error getting topics: {e}")
        return []

def create_user(username: str, email: str, full_name: str, institution: str) -> Optional[Dict]:
    """Create a new user"""
    try:
        supabase = init_supabase()
        if not supabase:
            return None
        
        data = {
            'username': username,
            'email': email,
            'full_name': full_name,
            'institution': institution
        }
        
        response = supabase.table('users').insert(data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

def authenticate_user(username: str) -> Optional[Dict]:
    """Authenticate user by username"""
    try:
        supabase = init_supabase()
        if not supabase:
            return None
        
        response = supabase.table('users').select("*").eq('username', username).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error authenticating user: {e}")
        return None

def get_leaderboard(limit: int = 10) -> List[Dict]:
    """Get leaderboard data"""
    try:
        supabase = init_supabase()
        if not supabase:
            return []
        
        response = supabase.table('users').select("*").order('score', desc=True).limit(limit).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error getting leaderboard: {e}")
        return []

# ==================== Content Management ====================

def get_content_items(category: Optional[str] = None) -> List[Dict]:
    """Get all content items (topics), optionally filtered by category"""
    return get_topics(category)

def get_content_item(item_id: str) -> Optional[Dict]:
    """Get a specific topic with its sections"""
    try:
        supabase = init_supabase()
        if not supabase:
            return None
        
        # Get the topic
        response = supabase.table('topics').select("*").eq('id', item_id).execute()
        if not response.data:
            return None
        
        item = response.data[0]
        
        # Get its sections
        sections_response = supabase.table('topic_sections').select("*").eq('topic_id', item_id).order('order_index').execute()
        item['sections'] = sections_response.data if sections_response.data else []
        
        return item
    except Exception as e:
        print(f"Error getting content item: {e}")
        return None

def create_content_item(data: Dict) -> Optional[Dict]:
    """Create a new topic"""
    try:
        supabase = init_supabase()
        if not supabase:
            return None
        
        response = supabase.table('topics').insert(data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error creating content item: {e}")
        return None

def update_content_item(item_id: str, data: Dict) -> bool:
    """Update a topic"""
    try:
        supabase = init_supabase()
        if not supabase:
            return False
        
        supabase.table('topics').update(data).eq('id', item_id).execute()
        return True
    except Exception as e:
        print(f"Error updating content item: {e}")
        return False

def delete_content_item(item_id: str) -> bool:
    """Delete a topic and its sections"""
    try:
        supabase = init_supabase()
        if not supabase:
            return False
        
        # Delete sections first
        supabase.table('topic_sections').delete().eq('topic_id', item_id).execute()
        
        # Delete the topic
        supabase.table('topics').delete().eq('id', item_id).execute()
        return True
    except Exception as e:
        print(f"Error deleting content item: {e}")
        return False

# ==================== Content Sections ====================

def create_content_section(data: Dict) -> Optional[Dict]:
    """Create a new topic section"""
    try:
        supabase = init_supabase()
        if not supabase:
            return None
        
        response = supabase.table('topic_sections').insert(data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error creating content section: {e}")
        return None

def update_content_section(section_id: str, data: Dict) -> bool:
    """Update a topic section"""
    try:
        supabase = init_supabase()
        if not supabase:
            return False
        
        supabase.table('topic_sections').update(data).eq('id', section_id).execute()
        return True
    except Exception as e:
        print(f"Error updating content section: {e}")
        return False

def delete_content_section(section_id: str) -> bool:
    """Delete a topic section"""
    try:
        supabase = init_supabase()
        if not supabase:
            return False
        
        supabase.table('topic_sections').delete().eq('id', section_id).execute()
        return True
    except Exception as e:
        print(f"Error deleting content section: {e}")
        return False

# ==================== Quiz Questions ====================

def get_quiz_questions(content_item_id: Optional[str] = None, category: Optional[str] = None) -> List[Dict]:
    """Get quiz questions, optionally filtered"""
    try:
        supabase = init_supabase()
        if not supabase:
            return []
        
        query = supabase.table('questions').select("*")
        
        if content_item_id:
            query = query.eq('topic_id', content_item_id)
        
        response = query.order('created_at', desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error getting quiz questions: {e}")
        return []

def create_quiz_question(data: Dict) -> Optional[Dict]:
    """Create a new quiz question"""
    try:
        supabase = init_supabase()
        if not supabase:
            return None
        
        response = supabase.table('questions').insert(data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error creating quiz question: {e}")
        return None

def update_quiz_question(question_id: str, data: Dict) -> bool:
    """Update a quiz question"""
    try:
        supabase = init_supabase()
        if not supabase:
            return False
        
        supabase.table('questions').update(data).eq('id', question_id).execute()
        return True
    except Exception as e:
        print(f"Error updating quiz question: {e}")
        return False

def delete_quiz_question(question_id: str) -> bool:
    """Delete a quiz question"""
    try:
        supabase = init_supabase()
        if not supabase:
            return False
        
        supabase.table('questions').delete().eq('id', question_id).execute()
        return True
    except Exception as e:
        print(f"Error deleting quiz question: {e}")
        return False

def get_user_weekly_progress(user_email: str) -> Dict:
    """
    קבלת נתוני ההתקדמות השבועית של משתמש ממסד הנתונים
    Get user's weekly progress from database
    """
    try:
        supabase = init_supabase()
        if not supabase:
            return {'completed_weeks': [], 'badges': [], 'total_points': 0}
        
        # נרמול המייל לאותיות קטנות
        user_email = user_email.lower()
        
        # חיפוש המשתמש לפי email
        response = supabase.table('users').select('weekly_progress').eq('email', user_email).execute()
        
        if response.data and len(response.data) > 0:
            progress = response.data[0].get('weekly_progress')
            if progress:
                return progress
        
        # אם אין נתונים, החזר ברירת מחדל
        return {'completed_weeks': [], 'badges': [], 'total_points': 0}
    except Exception as e:
        print(f"Error getting user weekly progress: {e}")
        return {'completed_weeks': [], 'badges': [], 'total_points': 0}

def update_user_weekly_progress(user_email: str, progress_data: Dict) -> bool:
    """
    עדכון נתוני ההתקדמות השבועית של משתמש במסד הנתונים
    Update user's weekly progress in database
    """
    try:
        supabase = init_supabase()
        if not supabase:
            return False
        
        # נרמול המייל לאותיות קטנות
        user_email = user_email.lower()
        
        # עדכון ה-weekly_progress
        response = supabase.table('users').update({
            'weekly_progress': progress_data
        }).eq('email', user_email).execute()
        
        return True
    except Exception as e:
        print(f"Error updating user weekly progress: {e}")
        return False

