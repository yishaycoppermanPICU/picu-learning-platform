import streamlit as st
from supabase import create_client, Client
import os

def init_supabase() -> Client:
    """Initialize Supabase client"""
    url = st.secrets. get("SUPABASE_URL", "")
    key = st.secrets.get("SUPABASE_KEY", "")
    
    if not url or not key: 
        st.error("Please configure Supabase credentials in Streamlit secrets")
        st.stop()
    
    return create_client(url, key)

def get_topics():
    """Get all learning topics"""
    supabase = init_supabase()
    response = supabase.table('topics').select("*").order('order_index').execute()
    return response.data

def get_questions_by_topic(topic_id):
    """Get questions for a specific topic"""
    supabase = init_supabase()
    response = supabase.table('questions').select("*").eq('topic_id', topic_id).execute()
    return response.data

def save_quiz_result(user_id, topic_id, score, total_questions):
    """Save quiz result to database"""
    supabase = init_supabase()
    data = {
        'user_id': user_id,
        'topic_id': topic_id,
        'score': score,
        'total_questions': total_questions
    }
    response = supabase.table('quiz_results').insert(data).execute()
    return response.data

def get_leaderboard():
    """Get institution leaderboard"""
    supabase = init_supabase()
    response = supabase. rpc('get_institution_stats').execute()
    return response.data

def create_user(username, email, full_name, institution_name):
    """Create a new user"""
    supabase = init_supabase()
    
    # Get institution ID
    inst_response = supabase.table('institutions').select("id").eq('name', institution_name).execute()
    
    if not inst_response.data:
        # Create institution if doesn't exist
        inst_response = supabase.table('institutions').insert({'name': institution_name}).execute()
    
    institution_id = inst_response.data[0]['id']
    
    # Create user
    user_data = {
        'username': username,
        'email': email,
        'full_name': full_name,
        'institution_id': institution_id
    }
    
    response = supabase.table('users').insert(user_data).execute()
    return response.data[0] if response.data else None

def authenticate_user(username):
    """Simple authentication - get user by username"""
    supabase = init_supabase()
    response = supabase.table('users').select("*").eq('username', username).execute()
    return response.data[0] if response.data else None
