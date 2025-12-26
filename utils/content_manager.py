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
