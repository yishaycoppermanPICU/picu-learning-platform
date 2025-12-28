# -*- coding: utf-8 -*-
"""
Corrections Manager for PICU Learning Platform
Manages user-reported content corrections
"""

import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime

# Base paths
CORRECTIONS_DIR = Path(__file__).parent.parent / "data" / "corrections"

def save_correction(category: str, topic_id: str, user_email: str, correction_text: str) -> bool:
    """
    Save a user correction report
    
    Args:
        category: Content category
        topic_id: Topic ID
        user_email: Reporter's email
        correction_text: Correction details
    
    Returns:
        True if saved successfully
    """
    try:
        # Create corrections directory if doesn't exist
        CORRECTIONS_DIR.mkdir(exist_ok=True)
        
        # Load existing corrections
        corrections_file = CORRECTIONS_DIR / "corrections.json"
        if corrections_file.exists():
            with open(corrections_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {"corrections": []}
        
        # Add new correction
        correction = {
            "id": f"corr_{len(data['corrections']) + 1:04d}",
            "category": category,
            "topic_id": topic_id,
            "user_email": user_email,
            "correction_text": correction_text,
            "timestamp": datetime.now().isoformat(),
            "status": "pending"  # pending, reviewed, fixed, rejected
        }
        
        data['corrections'].append(correction)
        
        # Save
        with open(corrections_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True
        
    except Exception as e:
        print(f"Error saving correction: {e}")
        return False

def get_all_corrections(status: str = None) -> List[Dict]:
    """
    Get all correction reports, optionally filtered by status
    
    Args:
        status: Filter by status (pending, reviewed, fixed, rejected)
    
    Returns:
        List of corrections
    """
    corrections_file = CORRECTIONS_DIR / "corrections.json"
    
    if not corrections_file.exists():
        return []
    
    try:
        with open(corrections_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        corrections = data.get('corrections', [])
        
        if status:
            corrections = [c for c in corrections if c.get('status') == status]
        
        return corrections
    
    except Exception as e:
        print(f"Error loading corrections: {e}")
        return []

def update_correction_status(correction_id: str, new_status: str) -> bool:
    """
    Update correction status
    
    Args:
        correction_id: Correction ID
        new_status: New status (reviewed, fixed, rejected)
    
    Returns:
        True if updated successfully
    """
    corrections_file = CORRECTIONS_DIR / "corrections.json"
    
    if not corrections_file.exists():
        return False
    
    try:
        with open(corrections_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Find and update
        for correction in data.get('corrections', []):
            if correction.get('id') == correction_id:
                correction['status'] = new_status
                correction['updated_at'] = datetime.now().isoformat()
                break
        
        # Save
        with open(corrections_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True
    
    except Exception as e:
        print(f"Error updating correction: {e}")
        return False

def get_corrections_by_topic(category: str, topic_id: str) -> List[Dict]:
    """
    Get corrections for specific topic
    
    Args:
        category: Content category
        topic_id: Topic ID
    
    Returns:
        List of corrections for this topic
    """
    all_corrections = get_all_corrections()
    return [
        c for c in all_corrections 
        if c.get('category') == category and c.get('topic_id') == topic_id
    ]
