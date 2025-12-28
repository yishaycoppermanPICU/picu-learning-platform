# -*- coding: utf-8 -*-
"""
Quiz Manager for PICU Learning Platform
Manages quiz questions and user quiz sessions
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
import random
from datetime import datetime

# Base paths
QUESTIONS_FILE = Path(__file__).parent.parent / "data" / "questions.json"
QUIZ_RESULTS_DIR = Path(__file__).parent.parent / "data" / "quiz_results"

def get_all_questions() -> List[Dict]:
    """
    Get all available questions
    
    Returns:
        List of question dictionaries
    """
    if not QUESTIONS_FILE.exists():
        return []
    
    try:
        with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("questions", [])
    except Exception as e:
        print(f"Error loading questions: {e}")
        return []

def get_questions_by_category(category: str) -> List[Dict]:
    """
    Get questions for a specific category
    
    Args:
        category: Category ID (e.g., 'hematology')
    
    Returns:
        List of questions in that category
    """
    all_questions = get_all_questions()
    return [q for q in all_questions if q.get('category') == category]

def get_questions_by_topic(topic: str) -> List[Dict]:
    """
    Get questions for a specific topic
    
    Args:
        topic: Topic ID (e.g., 'tumor_lysis_syndrome')
    
    Returns:
        List of questions about that topic
    """
    all_questions = get_all_questions()
    return [q for q in all_questions if q.get('topic') == topic]

def get_questions_by_difficulty(difficulty: str) -> List[Dict]:
    """
    Get questions by difficulty level
    
    Args:
        difficulty: 'beginner', 'intermediate', or 'advanced'
    
    Returns:
        List of questions at that difficulty
    """
    all_questions = get_all_questions()
    return [q for q in all_questions if q.get('difficulty') == difficulty]

def create_quiz(
    num_questions: int = 10,
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    topic: Optional[str] = None,
    randomize: bool = True
) -> List[Dict]:
    """
    Create a quiz with specified parameters
    
    Args:
        num_questions: Number of questions
        category: Filter by category (optional)
        difficulty: Filter by difficulty (optional)
        topic: Filter by topic (optional)
        randomize: Whether to randomize question order
    
    Returns:
        List of questions for the quiz
    """
    # Start with all questions
    questions = get_all_questions()
    
    # Apply filters
    if category:
        questions = [q for q in questions if q.get('category') == category]
    
    if difficulty:
        questions = [q for q in questions if q.get('difficulty') == difficulty]
    
    if topic:
        questions = [q for q in questions if q.get('topic') == topic]
    
    # Randomize if requested
    if randomize:
        random.shuffle(questions)
    
    # Limit to requested number
    return questions[:num_questions]

def check_answer(question_id: str, user_answer: int) -> Dict:
    """
    Check if an answer is correct
    
    Args:
        question_id: ID of the question
        user_answer: User's answer (0-3)
    
    Returns:
        Dictionary with is_correct, explanation, and points
    """
    questions = get_all_questions()
    question = next((q for q in questions if q.get('id') == question_id), None)
    
    if not question:
        return {
            "is_correct": False,
            "explanation": "שאלה לא נמצאה",
            "points": 0
        }
    
    correct = question.get('correct_answer')
    is_correct = user_answer == correct
    
    return {
        "is_correct": is_correct,
        "correct_answer": correct,
        "explanation": question.get('explanation', ''),
        "points": question.get('points', 0) if is_correct else 0
    }

def save_quiz_result(user_email: str, quiz_data: Dict) -> bool:
    """
    Save quiz result for a user
    
    Args:
        user_email: User's email
        quiz_data: Quiz results data
    
    Returns:
        True if successful
    """
    QUIZ_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load existing results or create new
    user_file = QUIZ_RESULTS_DIR / f"{user_email.replace('@', '_at_').replace('.', '_')}.json"
    
    if user_file.exists():
        with open(user_file, 'r', encoding='utf-8') as f:
            user_data = json.load(f)
    else:
        user_data = {"email": user_email, "quizzes": []}
    
    # Add new quiz result
    quiz_result = {
        "quiz_id": quiz_data.get('quiz_id'),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "category": quiz_data.get('category'),
        "topic": quiz_data.get('topic'),
        "difficulty": quiz_data.get('difficulty'),
        "total_questions": quiz_data.get('total_questions'),
        "correct_answers": quiz_data.get('correct_answers'),
        "score_percentage": quiz_data.get('score_percentage'),
        "time_taken": quiz_data.get('time_taken'),
        "points_earned": quiz_data.get('points_earned')
    }
    
    user_data['quizzes'].append(quiz_result)
    
    # Save to file
    try:
        with open(user_file, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, ensure_ascii=False, indent=2)
        
        # עדכון ניקוד המשתמש במסד הנתונים
        try:
            from utils.database import init_supabase
            supabase = init_supabase()
            if supabase:
                # קבלת הניקוד הנוכחי
                current_user = supabase.table('users').select('score').eq('email', user_email).execute()
                current_score = 0
                if current_user.data and len(current_user.data) > 0:
                    current_score = current_user.data[0].get('score', 0)
                
                # הוספת הנקודות החדשות
                new_score = current_score + int(quiz_data.get('points_earned', 0))
                
                # עדכון במסד הנתונים
                supabase.table('users').update({'score': new_score}).eq('email', user_email).execute()
        except Exception as db_error:
            print(f"Warning: Could not update user score in database: {db_error}")
        
        return True
    except Exception as e:
        print(f"Error saving quiz result: {e}")
        return False

def get_user_quiz_history(user_email: str) -> List[Dict]:
    """
    Get quiz history for a user
    
    Args:
        user_email: User's email
    
    Returns:
        List of quiz results
    """
    user_file = QUIZ_RESULTS_DIR / f"{user_email.replace('@', '_at_').replace('.', '_')}.json"
    
    if not user_file.exists():
        return []
    
    try:
        with open(user_file, 'r', encoding='utf-8') as f:
            user_data = json.load(f)
            return user_data.get('quizzes', [])
    except Exception as e:
        print(f"Error loading quiz history: {e}")
        return []

def get_user_stats(user_email: str) -> Dict:
    """
    Get statistics for a user
    
    Args:
        user_email: User's email
    
    Returns:
        Dictionary with user stats
    """
    history = get_user_quiz_history(user_email)
    
    if not history:
        return {
            "total_quizzes": 0,
            "average_score": 0,
            "best_score": 0,
            "total_questions": 0,
            "total_correct": 0
        }
    
    total_quizzes = len(history)
    scores = [q.get('score_percentage', 0) for q in history]
    total_questions = sum(q.get('total_questions', 0) for q in history)
    total_correct = sum(q.get('correct_answers', 0) for q in history)
    
    return {
        "total_quizzes": total_quizzes,
        "average_score": sum(scores) / total_quizzes if total_quizzes > 0 else 0,
        "best_score": max(scores) if scores else 0,
        "total_questions": total_questions,
        "total_correct": total_correct,
        "recent_quizzes": history[-5:]  # Last 5 quizzes
    }

def get_quiz_categories() -> List[Dict]:
    """
    Get all available quiz categories with question counts
    
    Returns:
        List of categories with counts
    """
    from utils.content_manager import get_all_categories
    
    all_categories = get_all_categories()
    questions = get_all_questions()
    
    result = []
    for cat in all_categories:
        cat_id = cat['id']
        cat_questions = [q for q in questions if q.get('category') == cat_id]
        
        if cat_questions:  # Only include categories with questions
            result.append({
                "id": cat_id,
                "name": cat['name'],
                "emoji": cat['emoji'],
                "description": cat['description'],
                "question_count": len(cat_questions)
            })
    
    return result
