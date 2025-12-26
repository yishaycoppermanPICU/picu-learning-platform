def get_institutions():
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
