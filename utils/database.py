def get_learning_content(topic_id):
    """Get learning content for a topic"""
    try:
        supabase = init_supabase()
        response = supabase.table('learning_content').select("*").eq('topic_id', topic_id).order('order_index').execute()
        return response.data
    except:
        return []

def mark_content_as_completed(user_id, topic_id, content_id):
    """Mark content as completed"""
    try:
        supabase = init_supabase()
        data = {
            'user_id': user_id,
            'topic_id': topic_id,
            'content_id': content_id,
            'completed':  True,
            'completed_at': datetime.now().isoformat()
        }
        response = supabase.table('user_progress').upsert(data).execute()
        return True
    except: 
        return False

def get_user_progress(user_id, topic_id):
    """Get user progress for a topic"""
    try:
        supabase = init_supabase()
        
        # Get total content
        total = supabase.table('learning_content').select("id", count='exact').eq('topic_id', topic_id).execute()
        
        # Get completed content
        completed = supabase.table('user_progress').select("*").eq('user_id', user_id).eq('topic_id', topic_id).eq('completed', True).execute()
        
        total_count = len(total.data) if total.data else 0
        completed_count = len(completed.data) if completed.data else 0
        
        return {
            'total': total_count,
            'completed': completed_count,
            'percentage': (completed_count / total_count * 100) if total_count > 0 else 0
        }
    except:
        return None
