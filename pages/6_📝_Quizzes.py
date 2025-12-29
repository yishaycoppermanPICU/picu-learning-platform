# -*- coding: utf-8 -*-
import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import time

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.quiz_manager import (
    create_quiz, 
    check_answer, 
    save_quiz_result,
    get_quiz_categories,
    get_all_questions
)
from utils.content_manager import get_all_categories
from utils.styles import get_common_styles

st.set_page_config(
    page_title="מבחנים",
    page_icon="📝",
    layout="wide"
)

# טעינת CSS מרכזי
st.markdown(get_common_styles(), unsafe_allow_html=True)

# CSS
st.markdown("""
<style>
    .stApp {
        direction: rtl;
        text-align: right;
    }
    
    h1, h2, h3, h4, h5, h6, p, label, span, li {
        text-align: right;
        direction: rtl;
    }
    
    .quiz-header {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .question-card {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .option-button {
        width: 100%;
        text-align: right;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# בדיקת התחברות
if not st.session_state.get('logged_in', False):
    st.error("יש להתחבר כדי לבצע מבחנים ❌")
    if st.button("חזור לדף הראשי 🏠"):
        st.switch_page("app.py")
    st.stop()

user = st.session_state.get('user', {})

# Initialize quiz state
if 'quiz_active' not in st.session_state:
    st.session_state.quiz_active = False
if 'quiz_questions' not in st.session_state:
    st.session_state.quiz_questions = []
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = []
if 'quiz_start_time' not in st.session_state:
    st.session_state.quiz_start_time = None
if 'quiz_config' not in st.session_state:
    st.session_state.quiz_config = {}

# Header
st.markdown("""
<div class="quiz-header">
    <h1>📝 מבחנים</h1>
    <p>בדוק את הידע שלך במבחנים מותאמים אישית</p>
</div>
""", unsafe_allow_html=True)

# Quiz Setup Screen
if not st.session_state.quiz_active:
    
    # Check if coming from weekly content - auto-start quiz
    if st.session_state.get('weekly_quiz') and st.session_state.get('selected_quiz_category'):
        selected_category = st.session_state.get('selected_quiz_category')
        
        # Get questions for this category
        from utils.quiz_manager import get_questions_by_category
        category_questions = get_questions_by_category(selected_category)
        
        if len(category_questions) > 0:
            # Start quiz automatically with 15 questions
            import random
            random.shuffle(category_questions)
            quiz_questions = category_questions[:min(15, len(category_questions))]
            
            st.session_state.quiz_questions = quiz_questions
            st.session_state.quiz_active = True
            st.session_state.current_question = 0
            st.session_state.quiz_answers = []
            st.session_state.quiz_start_time = time.time()
            st.session_state.quiz_config = {
                'category': selected_category,
                'difficulty': 'all',
                'quiz_type': 'all',
                'show_timer': True,
                'num_questions': len(quiz_questions),
                'topic_title': 'מבחן שבועי',
                'weekly': True
            }
            # Clear flags
            st.session_state['weekly_quiz'] = False
            st.rerun()
        else:
            st.error(f"❌ לא נמצאו שאלות עבור קטגוריה זו")
            st.session_state['weekly_quiz'] = False
            st.session_state['selected_quiz_category'] = None
    
    # Check if coming from a specific topic - auto-start quiz
    from_topic = st.session_state.get('quiz_topic')
    from_category = st.session_state.get('quiz_category')
    
    if from_topic:
        # Auto-start quiz with all available questions for this topic
        all_questions = get_all_questions()
        topic_questions = [q for q in all_questions if q.get('topic') == from_topic]
        
        if len(topic_questions) > 0:
            # Start quiz automatically with all topic questions
            import random
            random.shuffle(topic_questions)
            st.session_state.quiz_questions = topic_questions
            st.session_state.quiz_active = True
            st.session_state.current_question = 0
            st.session_state.quiz_answers = []
            st.session_state.quiz_start_time = time.time()
            st.session_state.quiz_config = {
                'category': from_category,
                'difficulty': 'all',
                'quiz_type': 'all',
                'show_timer': True,
                'from_topic': from_topic
            }
            # Clear topic filter
            st.session_state['quiz_topic'] = None
            st.session_state['quiz_category'] = None
            st.rerun()
        else:
            st.error(f"❌ לא נמצאו שאלות עבור נושא: {from_topic}")
            if st.button("🔙 חזור לספרייה"):
                st.session_state['quiz_topic'] = None
                st.session_state['quiz_category'] = None
                st.switch_page("pages/1_📚_Library.py")
            st.stop()
    
    st.markdown("### 🎯 הגדר את המבחן שלך")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Category selection
        st.markdown("#### בחר נושא")
        
        categories = get_all_categories()
        category_options = {"all": "🔀 מבחן מעורבב (כל הנושאים)"}
        
        for cat in categories:
            # Count questions in this category
            from utils.quiz_manager import get_questions_by_category
            q_count = len(get_questions_by_category(cat['id']))
            if q_count > 0:
                category_options[cat['id']] = f"{cat['emoji']} {cat['name']} ({q_count} שאלות)"
        
        selected_category = st.selectbox(
            "נושא:",
            options=list(category_options.keys()),
            format_func=lambda x: category_options[x],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        # Quiz type filter
        st.markdown("#### סוג השאלות")
        quiz_type = st.radio(
            "בחר סוג:",
            ["all", "conditions", "medications"],
            format_func=lambda x: {
                "all": "🔀 הכל - מצבים ותרופות",
                "conditions": "🩺 רק מצבים מייצגים (המטולוגיה, החייאה, זיהומים וכו')",
                "medications": "💊 רק תרופות"
            }[x],
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("#### הגדרות מבחן")
        
        # Number of questions - spinner
        num_questions = st.number_input(
            "מספר שאלות:",
            min_value=1,
            max_value=200,
            value=10,
            step=1
        )
        
        # Difficulty level
        difficulty = st.selectbox(
            "רמת קושי:",
            options=["all", "beginner", "intermediate", "advanced"],
            format_func=lambda x: {
                "all": "🔀 מעורבב",
                "beginner": "🟢 קל",
                "intermediate": "🟡 בינוני",
                "advanced": "🔴 קשה"
            }[x]
        )
        
        # Show timer option
        show_timer = st.checkbox("⏱️ הצג טיימר לכל שאלה", value=True)
    
    st.divider()
    
    # Start quiz button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 התחל מבחן", type="primary", use_container_width=True):
            # Create quiz based on filters
            all_questions = get_all_questions()
            
            # Filter by topic if coming from content page
            from_topic = st.session_state.get('quiz_topic')
            if from_topic:
                all_questions = [q for q in all_questions if q.get('topic') == from_topic]
                st.info(f"🎯 סינון לפי נושא: {from_topic} ({len(all_questions)} שאלות זמינות)")
            
            # Filter by category
            if selected_category != "all":
                all_questions = [q for q in all_questions if q.get('category') == selected_category]
            
            # Filter by type
            if quiz_type == "medications":
                all_questions = [q for q in all_questions if q.get('category') == 'medications']
            elif quiz_type == "conditions":
                all_questions = [q for q in all_questions if q.get('category') != 'medications']
            
            # Filter by difficulty
            if difficulty != "all":
                all_questions = [q for q in all_questions if q.get('difficulty') == difficulty]
            
            # Check if we have enough questions
            if len(all_questions) < num_questions:
                st.error(f"❌ לא מספיק שאלות זמינות. יש רק {len(all_questions)} שאלות בהגדרות שבחרת.")
            else:
                # Create quiz
                import random
                random.shuffle(all_questions)
                st.session_state.quiz_questions = all_questions[:num_questions]
                st.session_state.quiz_active = True
                st.session_state.current_question = 0
                st.session_state.quiz_answers = []
                st.session_state.quiz_start_time = time.time()
                st.session_state.quiz_config = {
                    'category': selected_category,
                    'difficulty': difficulty,
                    'quiz_type': quiz_type,
                    'show_timer': show_timer,
                    'from_topic': from_topic
                }
                # Clear topic filter after use
                st.session_state['quiz_topic'] = None
                st.session_state['quiz_category'] = None
                st.rerun()
    
    # Statistics preview
    st.divider()
    st.markdown("### 📊 סטטיסטיקות זמינות")
    
    all_q = get_all_questions()
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("סה\"כ שאלות", len(all_q))
    with col2:
        beginner = len([q for q in all_q if q.get('difficulty') == 'beginner'])
        st.metric("שאלות קלות", beginner)
    with col3:
        intermediate = len([q for q in all_q if q.get('difficulty') == 'intermediate'])
        st.metric("שאלות בינוניות", intermediate)
    with col4:
        advanced = len([q for q in all_q if q.get('difficulty') == 'advanced'])
        st.metric("שאלות קשות", advanced)

# Quiz Active Screen
else:
    # Progress bar
    progress = (st.session_state.current_question) / len(st.session_state.quiz_questions)
    st.progress(progress)
    
    st.markdown(f"### שאלה {st.session_state.current_question + 1} מתוך {len(st.session_state.quiz_questions)}")
    
    # Get current question
    question = st.session_state.quiz_questions[st.session_state.current_question]
    
    # Timer
    if st.session_state.quiz_config.get('show_timer'):
        time_limit = question.get('time_limit', 90)
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            st.info(f"⏱️ זמן מומלץ: {time_limit} שניות")
    
    # Question card
    st.markdown(f"""
    <div class="question-card">
        <h3>{question['question']}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Difficulty indicator
    difficulty_map = {
        "beginner": "🟢 קל",
        "intermediate": "🟡 בינוני",
        "advanced": "🔴 קשה"
    }
    st.caption(f"**רמת קושי:** {difficulty_map.get(question.get('difficulty', 'intermediate'))}")
    
    st.divider()
    
    # Answer options
    st.markdown("### בחר תשובה:")
    
    selected_answer = st.radio(
        "אפשרויות:",
        options=range(len(question['options'])),
        format_func=lambda x: f"{x+1}. {question['options'][x]}",
        label_visibility="collapsed",
        key=f"q_{st.session_state.current_question}"
    )
    
    st.divider()
    
    # Navigation buttons
    col1, col2, col3, col4 = st.columns([1, 1, 2, 1])
    
    with col1:
        # Previous question button
        if st.session_state.current_question > 0:
            if st.button("⬅️ שאלה קודמת"):
                # Remove last answer if exists
                if st.session_state.quiz_answers:
                    st.session_state.quiz_answers.pop()
                st.session_state.current_question -= 1
                st.rerun()
        else:
            st.empty()  # Placeholder when no previous question
    
    with col2:
        if st.button("⏭️ דלג"):
            st.session_state.quiz_answers.append({
                'question_id': question['id'],
                'user_answer': None,
                'skipped': True
            })
            st.session_state.current_question += 1
            
            if st.session_state.current_question >= len(st.session_state.quiz_questions):
                st.session_state.quiz_active = False
            st.rerun()
    
    with col3:
        if st.button("✅ אשר תשובה ועבור הלאה", type="primary", use_container_width=True):
            st.session_state.quiz_answers.append({
                'question_id': question['id'],
                'user_answer': selected_answer,
                'skipped': False
            })
            st.session_state.current_question += 1
            
            if st.session_state.current_question >= len(st.session_state.quiz_questions):
                st.session_state.quiz_active = False
            st.rerun()
    
    with col4:
        pass  # Empty for symmetry
    
    with col3:
        if st.button("🚫 צא מהמבחן"):
            st.session_state.quiz_active = False
            st.session_state.quiz_questions = []
            st.session_state.current_question = 0
            st.session_state.quiz_answers = []
            st.rerun()

# Quiz Results Screen
if not st.session_state.quiz_active and st.session_state.quiz_answers:
    st.markdown("### 🎉 סיימת את המבחן!")
    
    # Calculate results
    total_questions = len(st.session_state.quiz_questions)
    answered_questions = len([a for a in st.session_state.quiz_answers if not a.get('skipped')])
    
    correct_count = 0
    total_points = 0
    earned_points = 0
    
    for answer in st.session_state.quiz_answers:
        if not answer.get('skipped'):
            result = check_answer(answer['question_id'], answer['user_answer'])
            if result['is_correct']:
                correct_count += 1
                
            question = next((q for q in st.session_state.quiz_questions if q['id'] == answer['question_id']), None)
            if question:
                q_points = question.get('points', 2)
                total_points += q_points
                if result['is_correct']:
                    earned_points += q_points
    
    # Calculate score out of 100 (normalize the points)
    score_out_of_100 = (earned_points / total_points * 100) if total_points > 0 else 0
    time_taken = int(time.time() - st.session_state.quiz_start_time) if st.session_state.quiz_start_time else 0
    
    # Display results
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("תשובות נכונות", f"{correct_count}/{answered_questions}")
    with col2:
        st.metric("ציון", f"{score_out_of_100:.0f}/100")
    with col3:
        st.metric("זמן", f"{time_taken//60}:{time_taken%60:02d}")
    
    # Performance message
    if score_out_of_100 >= 90:
        st.success("🌟 מצוין! אתה שולט בנושא!")
    elif score_out_of_100 >= 70:
        st.info("👍 יפה מאוד! עם עוד קצת תרגול תהיה מושלם")
    else:
        st.warning("💪 כדאי לחזור על החומר ולנסות שוב")
    
    st.divider()
    
    # Detailed results
    st.markdown("### 📋 סקירת השאלות")
    
    for idx, answer in enumerate(st.session_state.quiz_answers, 1):
        question = next((q for q in st.session_state.quiz_questions if q['id'] == answer['question_id']), None)
        
        if not question:
            continue
        
        with st.expander(f"שאלה {idx}: {question['question'][:80]}..."):
            st.markdown(f"**שאלה מלאה:** {question['question']}")
            
            if answer.get('skipped'):
                st.warning("⏭️ דילגת על שאלה זו")
            else:
                result = check_answer(answer['question_id'], answer['user_answer'])
                
                # Show user's answer
                st.markdown(f"**התשובה שלך:** {question['options'][answer['user_answer']]}")
                
                if result['is_correct']:
                    st.success("✅ תשובה נכונה!")
                else:
                    st.error(f"❌ תשובה שגויה. התשובה הנכונה: {question['options'][result['correct_answer']]}")
                
                # Show explanation
                st.markdown("**הסבר:**")
                st.info(result['explanation'])
    
    # Save results
    if st.button("💾 שמור תוצאות", type="primary"):
        quiz_data = {
            'quiz_id': f"quiz_{int(time.time())}",
            'category': st.session_state.quiz_config.get('category'),
            'topic': None,
            'difficulty': st.session_state.quiz_config.get('difficulty'),
            'total_questions': answered_questions,
            'correct_answers': correct_count,
            'score_percentage': score_out_of_100,
            'time_taken': time_taken,
            'points_earned': earned_points
        }
        
        user_email = user.get('email', 'unknown')
        if save_quiz_result(user_email, quiz_data):
            st.success("✅ התוצאות נשמרו בהצלחה!")
        else:
            st.error("❌ שגיאה בשמירת התוצאות")
    
    st.divider()
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 מבחן חדש", use_container_width=True):
            st.session_state.quiz_answers = []
            st.session_state.quiz_questions = []
            st.session_state.current_question = 0
            st.rerun()
    with col2:
        if st.button("📊 לסטטיסטיקות", use_container_width=True):
            st.switch_page("pages/3_📊_Statistics.py")

# Back button
if not st.session_state.quiz_active:
    st.divider()
    if st.button("🏠 חזרה לעמוד הראשי", use_container_width=True):
        st.switch_page("app.py")
