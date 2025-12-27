# -*- coding: utf-8 -*-
"""
Content Manager for PICU Learning Platform
Manages medical content stored in JSON files
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
import os

# Base path for content
CONTENT_DIR = Path(__file__).parent.parent / "data" / "content"
EDITORS_FILE = Path(__file__).parent.parent / "data" / "editors.json"
USERS_FILE = Path(__file__).parent.parent / "data" / "users.json"

def get_all_categories() -> List[Dict]:
    """
    Get all available medical categories
    
    Returns:
        List of category dictionaries with id, name, emoji, and description
    """
    return [
        {
            "id": "hematology",
            "name": "המטולוגיה ואונקולוגיה",
            "emoji": "🩸",
            "description": "מחלות דם וסרטן בילדים"
        },
        {
            "id": "resuscitation",
            "name": "החייאה וטיפול דחוף",
            "emoji": "🚨",
            "description": "מצבי חירום והחייאה בטיפול נמרץ"
        },
        {
            "id": "infections",
            "name": "זיהומים",
            "emoji": "🦠",
            "description": "זיהומים חיידקיים וויראליים"
        },
        {
            "id": "monitoring",
            "name": "ניטור ונהלים",
            "emoji": "📊",
            "description": "ניטור המודינמי, נהלי סיעוד וציוד"
        },
        {
            "id": "medications",
            "name": "תרופות",
            "emoji": "💊",
            "description": "מדריך תרופות בטיפול נמרץ - מינונים, התוויות ותופעות לוואי"
        },
        {
            "id": "fluids_electrolytes",
            "name": "נוזלים ואלקטרוליטים",
            "emoji": "💧",
            "description": "ניהול נוזלים, תיקון אלקטרוליטים ואיזון חומצה-בסיס"
        },
        {
            "id": "immunology",
            "name": "אימונולוגיה",
            "emoji": "🛡️",
            "description": "מחלות חיסון, בידוד ופרוטוקולים למדוכאי חיסון"
        },
        {
            "id": "cardiology",
            "name": "קרדיולוגיה",
            "emoji": "❤️",
            "description": "מחלות לב, הפרעות קצב וטיפול בכשל לבבי"
        },
        {
            "id": "trauma",
            "name": "טראומה",
            "emoji": "🚑",
            "description": "פגיעות ראש, טראומה רב-מערכתית וניהול חירום"
        }
    ]

def get_category_topics(category_id: str) -> List[Dict]:
    """
    Get all topics in a specific category
    
    Args:
        category_id: Category identifier (e.g., 'hematology')
    
    Returns:
        List of topic dictionaries with basic info
    """
    category_path = CONTENT_DIR / category_id
    
    if not category_path.exists():
        return []
    
    topics = []
    for json_file in category_path.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                topics.append({
                    "id": data.get("id"),
                    "title": data.get("title"),
                    "description": data.get("description"),
                    "difficulty": data.get("difficulty"),
                    "order": data.get("order", 999),
                    "tags": data.get("tags", [])
                })
        except Exception as e:
            print(f"Error loading {json_file}: {e}")
            continue
    
    # Sort by order
    topics.sort(key=lambda x: x.get("order", 999))
    return topics

def get_topic(category_id: str, topic_id: str) -> Optional[Dict]:
    """
    Get full topic content
    
    Args:
        category_id: Category identifier
        topic_id: Topic identifier
    
    Returns:
        Full topic dictionary or None if not found
    """
    topic_path = CONTENT_DIR / category_id / f"{topic_id}.json"
    
    if not topic_path.exists():
        return None
    
    try:
        with open(topic_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading topic {topic_id}: {e}")
        return None

def create_topic(category_id: str, topic_data: Dict) -> bool:
    """
    Create a new topic
    
    Args:
        category_id: Category identifier
        topic_data: Topic data dictionary
    
    Returns:
        True if successful, False otherwise
    """
    category_path = CONTENT_DIR / category_id
    category_path.mkdir(parents=True, exist_ok=True)
    
    topic_id = topic_data.get("id")
    if not topic_id:
        return False
    
    topic_path = category_path / f"{topic_id}.json"
    
    try:
        with open(topic_path, 'w', encoding='utf-8') as f:
            json.dump(topic_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error creating topic: {e}")
        return False

def update_topic(category_id: str, topic_id: str, updated_data: Dict) -> bool:
    """
    Update an existing topic with new data
    
    Args:
        category_id: Category identifier
        topic_id: Topic identifier
        updated_data: Updated topic data
    
    Returns:
        True if successful, False otherwise
    """
    topic_path = CONTENT_DIR / category_id / f"{topic_id}.json"
    
    if not topic_path.exists():
        return False
    
    try:
        with open(topic_path, 'w', encoding='utf-8') as f:
            json.dump(updated_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error updating topic: {e}")
        return False

def add_content_item(category_id: str, topic_id: str, item: Dict) -> bool:
    """
    Add content item to existing topic
    
    Args:
        category_id: Category identifier
        topic_id: Topic identifier
        item: Content item to add
    
    Returns:
        True if successful, False otherwise
    """
    topic = get_topic(category_id, topic_id)
    if not topic:
        return False
    
    if "content" not in topic:
        topic["content"] = []
    
    topic["content"].append(item)
    
    return create_topic(category_id, topic)

def search(query: str) -> List[Dict]:
    """
    Full-text search across all content
    
    Args:
        query: Search query string
    
    Returns:
        List of matching topics with relevant info
    """
    if not query:
        return []
    
    query_lower = query.lower()
    results = []
    
    for category in get_all_categories():
        category_id = category["id"]
        topics = get_category_topics(category_id)
        
        for topic_info in topics:
            topic = get_topic(category_id, topic_info["id"])
            if not topic:
                continue
            
            # Search in title, description, tags
            if (query_lower in topic.get("title", "").lower() or
                query_lower in topic.get("description", "").lower() or
                any(query_lower in tag.lower() for tag in topic.get("tags", []))):
                
                results.append({
                    "category_id": category_id,
                    "category_name": category["name"],
                    "topic_id": topic["id"],
                    "title": topic["title"],
                    "description": topic["description"],
                    "match_type": "metadata"
                })
                continue
            
            # Search in content
            for content_item in topic.get("content", []):
                content_text = json.dumps(content_item, ensure_ascii=False).lower()
                if query_lower in content_text:
                    results.append({
                        "category_id": category_id,
                        "category_name": category["name"],
                        "topic_id": topic["id"],
                        "title": topic["title"],
                        "description": topic["description"],
                        "match_type": "content"
                    })
                    break
    
    return results

def get_stats() -> Dict:
    """
    Get library statistics
    
    Returns:
        Dictionary with statistics
    """
    categories = get_all_categories()
    total_topics = 0
    total_items = 0
    
    for category in categories:
        category_id = category["id"]
        topics = get_category_topics(category_id)
        total_topics += len(topics)
        
        for topic_info in topics:
            topic = get_topic(category_id, topic_info["id"])
            if topic:
                total_items += len(topic.get("content", []))
    
    return {
        "total_categories": len(categories),
        "total_topics": total_topics,
        "total_content_items": total_items
    }

def get_editors() -> List[str]:
    """
    Get list of authorized editors
    
    Returns:
        List of editor email addresses
    """
    if not EDITORS_FILE.exists():
        return ["yishaycopp@gmail.com"]
    
    try:
        with open(EDITORS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("editors", ["yishaycopp@gmail.com"])
    except Exception as e:
        print(f"Error loading editors: {e}")
        return ["yishaycopp@gmail.com"]

def is_editor(email: str) -> bool:
    """
    Check if a user is authorized to edit content
    
    Args:
        email: User email address
    
    Returns:
        True if user is authorized editor, False otherwise
    """
    editors = get_editors()
    return email in editors

def add_editor(email: str) -> bool:
    """
    Add a new editor
    
    Args:
        email: Email address to add
    
    Returns:
        True if successful, False otherwise
    """
    if not email or '@' not in email:
        return False
    
    editors = get_editors()
    if email not in editors:
        editors.append(email)
        return save_editors(editors)
    return True

def remove_editor(email: str) -> bool:
    """
    Remove an editor
    
    Args:
        email: Email address to remove
    
    Returns:
        True if successful, False otherwise
    """
    editors = get_editors()
    if email in editors:
        if len(editors) == 1:
            return False  # Don't remove last editor
        editors.remove(email)
        return save_editors(editors)
    return False

def save_editors(editors: List[str]) -> bool:
    """
    Save editors list to file
    
    Args:
        editors: List of editor emails
    
    Returns:
        True if successful, False otherwise
    """
    EDITORS_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    from datetime import datetime
    data = {
        "editors": editors,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    try:
        with open(EDITORS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving editors: {e}")
        return False

# ===== User Management Functions =====

def get_all_users() -> List[Dict]:
    """
    Get all registered users
    
    Returns:
        List of user dictionaries
    """
    if not USERS_FILE.exists():
        return []
    
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("users", [])
    except Exception as e:
        print(f"Error loading users: {e}")
        return []

def get_user_by_email(email: str) -> Optional[Dict]:
    """
    Get user details by email
    
    Args:
        email: User email address
    
    Returns:
        User dictionary or None if not found
    """
    users = get_all_users()
    for user in users:
        if user.get('email', '').lower() == email.lower():
            return user
    return None

def save_user(email: str, name: str, hospital: str) -> bool:
    """
    Save or update user information
    
    Args:
        email: User email address
        name: User full name
        hospital: User hospital
    
    Returns:
        True if successful, False otherwise
    """
    from datetime import datetime
    
    users = get_all_users()
    
    # Check if user exists
    user_exists = False
    for i, user in enumerate(users):
        if user.get('email', '').lower() == email.lower():
            # Update existing user
            users[i] = {
                "email": email,
                "name": name,
                "hospital": hospital,
                "last_login": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            user_exists = True
            break
    
    # Add new user
    if not user_exists:
        users.append({
            "email": email,
            "name": name,
            "hospital": hospital,
            "last_login": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "first_login": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    # Save to file
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    data = {
        "users": users,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving user: {e}")
        return False

def update_last_login(email: str) -> bool:
    """
    Update user's last login time
    
    Args:
        email: User email address
    
    Returns:
        True if successful, False otherwise
    """
    from datetime import datetime
    
    users = get_all_users()
    
    for i, user in enumerate(users):
        if user.get('email', '').lower() == email.lower():
            users[i]['last_login'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            data = {
                "users": users,
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            try:
                with open(USERS_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                return True
            except Exception as e:
                print(f"Error updating last login: {e}")
                return False
    
    return False


def restore_user_session(st_instance):
    """
    Restore user session from query params if available
    
    Args:
        st_instance: Streamlit instance
    
    Returns:
        True if session was restored, False otherwise
    """
    try:
        # Check if already logged in
        if st_instance.session_state.get('logged_in', False):
            return True
        
        # Try to restore from query params
        query_params = st_instance.query_params
        if 'user_email' in query_params:
            saved_email = query_params['user_email']
            existing_user = get_user_by_email(saved_email)
            
            if existing_user:
                # Restore session
                username = saved_email.split('@')[0].replace('.', '_').replace('-', '_')
                st_instance.session_state.logged_in = True
                st_instance.session_state.user = {
                    'username': username,
                    'full_name': existing_user.get('name', ''),
                    'email': saved_email,
                    'institution': existing_user.get('hospital', ''),
                    'institutions': {'name': existing_user.get('hospital', '')}
                }
                update_last_login(saved_email)
                return True
    except Exception as e:
        print(f"Error restoring session: {e}")
    
    return False
