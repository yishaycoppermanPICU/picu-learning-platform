# -*- coding: utf-8 -*-
import streamlit as st
import sys
import json
from pathlib import Path
from datetime import datetime

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))

st.set_page_config(
    page_title="תרחישים מתגלגלים",
    page_icon="🎬",
    layout="wide"
)

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
    
    .scenario-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .stage-card {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-right: 4px solid #667eea;
    }
    
    .checklist-item {
        background: #f8f9fa;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
        border-right: 3px solid #28a745;
    }
    
    .patient-vitals {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 5px;
        border: 2px solid #ffc107;
        margin: 1rem 0;
    }
    
    .critical-warning {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 2px solid #dc3545;
        margin: 1rem 0;
        font-weight: bold;
    }
    
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 2px solid #28a745;
        margin: 1rem 0;
    }
    
    .timer {
        position: fixed;
        top: 80px;
        left: 20px;
        background: #dc3545;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        font-size: 1.5rem;
        font-weight: bold;
        z-index: 1000;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# Load scenarios
def load_scenarios():
    """טען את כל התרחישים מתיקיית data/scenarios"""
    scenarios_dir = Path(__file__).parent.parent / "data" / "scenarios"
    scenarios = []
    
    if scenarios_dir.exists():
        for file in scenarios_dir.glob("*.json"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    scenario = json.load(f)
                    scenarios.append(scenario)
            except Exception as e:
                st.error(f"שגיאה בטעינת תרחיש {file.name}: {e}")
    
    return scenarios

# Initialize session state
if 'scenario_active' not in st.session_state:
    st.session_state.scenario_active = False
if 'current_scenario' not in st.session_state:
    st.session_state.current_scenario = None
if 'current_stage' not in st.session_state:
    st.session_state.current_stage = 0
if 'patient_state' not in st.session_state:
    st.session_state.patient_state = {}
if 'selections' not in st.session_state:
    st.session_state.selections = {}
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'stage_start_time' not in st.session_state:
    st.session_state.stage_start_time = None

# בדיקת התחברות
if not st.session_state.get('logged_in', False):
    st.error("יש להתחבר כדי לגשת לתרחישים מתגלגלים ❌")
    if st.button("חזור לדף הראשי 🏠"):
        st.switch_page("app.py")
    st.stop()

user = st.session_state.get('user', {})

# Header
st.markdown("""
<div class="scenario-header">
    <h1>🎬 תרחישים מתגלגלים (Rolling Scenarios)</h1>
    <p>סימולציות רפואיות אינטראקטיביות עם החלטות בזמן אמת</p>
</div>
""", unsafe_allow_html=True)

# Load available scenarios
scenarios = load_scenarios()

if not scenarios:
    st.warning("לא נמצאו תרחישים זמינים. נא ליצור קבצי תרחישים בתיקייה data/scenarios/")
    st.stop()

# Scenario Selection Screen
if not st.session_state.scenario_active:
    st.markdown("### 🎯 בחר תרחיש")
    
    for scenario in scenarios:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"### {scenario['title']}")
                st.markdown(f"**תיאור:** {scenario['description']}")
                
                # Display tags
                tags_html = " ".join([f"<span style='background:#667eea; color:white; padding:0.2rem 0.5rem; border-radius:3px; margin:0.2rem; display:inline-block;'>{tag}</span>" for tag in scenario.get('tags', [])])
                st.markdown(tags_html, unsafe_allow_html=True)
                
            with col2:
                difficulty_colors = {
                    'beginner': '🟢',
                    'intermediate': '🟡',
                    'advanced': '🟠',
                    'hard': '🔴'
                }
                st.markdown(f"**רמת קושי:** {difficulty_colors.get(scenario['difficulty'], '⚪')} {scenario['difficulty']}")
                st.markdown(f"**זמן משוער:** {scenario.get('estimated_time', 'N/A')} דקות")
                
            with col3:
                if st.button(f"התחל תרחיש", key=f"start_{scenario['scenario_id']}"):
                    st.session_state.scenario_active = True
                    st.session_state.current_scenario = scenario
                    st.session_state.current_stage = 0
                    st.session_state.patient_state = scenario.get('patient_profile', {})
                    st.session_state.selections = {}
                    st.session_state.score = 0
                    st.session_state.stage_start_time = datetime.now()
                    st.rerun()
            
            st.markdown("---")

# Active Scenario Screen
else:
    scenario = st.session_state.current_scenario
    current_stage_idx = st.session_state.current_stage
    
    # Check if scenario is complete
    if current_stage_idx >= len(scenario['stages']):
        st.success("🎉 סיימת את התרחיש!")
        st.markdown(f"### ציון סופי: {st.session_state.score}")
        
        # Display summary - check if last stage exists and is conclusion
        if len(scenario['stages']) > 0:
            last_stage = scenario['stages'][-1]
            if last_stage.get('type') == 'conclusion':
                conclusion = last_stage
                context = conclusion.get('context', {})
                
                # Check for success or other outcomes
                for outcome_type in ['success', 'partial_success', 'failure']:
                    outcome_info = context.get(outcome_type, {})
                    if outcome_info:
                        st.markdown("### סיכום")
                        if outcome_info.get('text'):
                            st.markdown(outcome_info['text'])
                        
                        # Display outcomes
                        if outcome_info.get('outcomes'):
                            st.markdown("#### תוצאות:")
                            for outcome in outcome_info['outcomes']:
                                st.markdown(f"• {outcome}")
                        
                        # Display key decisions
                        if outcome_info.get('key_decisions'):
                            st.markdown("#### החלטות מפתח:")
                            for decision in outcome_info['key_decisions']:
                                st.markdown(f"✅ {decision}")
                        break
        
        # Display learning points from main scenario
        if scenario.get('learning_points'):
            st.markdown("#### נקודות למידה:")
            for point in scenario['learning_points']:
                st.markdown(f"💡 {point}")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("חזור לרשימת תרחישים", use_container_width=True):
                st.session_state.scenario_active = False
                st.session_state.current_scenario = None
                st.session_state.current_stage = 0
                st.rerun()
        
        with col2:
            if st.button("נסה שוב", use_container_width=True):
                st.session_state.current_stage = 0
                st.session_state.patient_state = scenario.get('patient_profile', {})
                st.session_state.selections = {}
                st.session_state.score = 0
                st.session_state.stage_start_time = datetime.now()
                st.rerun()
        
        st.stop()
    
    stage = scenario['stages'][current_stage_idx]
    
    # Display timer if applicable
    if st.session_state.stage_start_time and stage.get('time_limit'):
        elapsed = (datetime.now() - st.session_state.stage_start_time).seconds
        remaining = stage['time_limit'] - elapsed
        
        if remaining > 0:
            st.markdown(f"""
            <div class="timer">
                ⏱️ זמן נותר: {remaining // 60}:{remaining % 60:02d}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="timer">⏱️ הזמן תם!</div>', unsafe_allow_html=True)
    
    # Display patient vitals
    if st.session_state.patient_state:
        st.markdown(f"""
        <div class="patient-vitals">
            <h4>פרמטרים המודינמיים</h4>
            <p><strong>BP:</strong> {st.session_state.patient_state.get('bp', 'N/A')} | 
            <strong>HR:</strong> {st.session_state.patient_state.get('hr', 'N/A')} | 
            <strong>SpO2:</strong> {st.session_state.patient_state.get('sat', 'N/A')}% |
            <strong>RR:</strong> {st.session_state.patient_state.get('rr', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display stage content
    st.markdown(f"## שלב {current_stage_idx + 1}: {stage['title']}")
    
    # Display context
    if 'context' in stage:
        context = stage['context']
        if isinstance(context, dict):
            st.markdown(f"**מצב קליני:** {context.get('text', '')}")
            if 'vitals' in context:
                st.info(f"סימנים חיוניים: {context['vitals']}")
        else:
            st.markdown(f"**מצב:** {context}")
    
    # Handle different stage types
    if stage['type'] == 'checklist_selection':
        st.markdown("### בחר את הפריטים הנחוצים:")
        st.markdown(stage.get('instructions', ''))
        
        # Group items by category
        items = stage.get('items', [])
        categories = {}
        for item in items:
            cat = item.get('category', 'אחר')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(item)
        
        # Display checkboxes by category
        selected_items = []
        for category, cat_items in categories.items():
            st.markdown(f"#### {category}")
            for item in cat_items:
                checked = st.checkbox(
                    item['name'],
                    key=f"item_{item['id']}",
                    value=st.session_state.selections.get(item['id'], False)
                )
                if checked:
                    selected_items.append(item['id'])
        
        # Submit button
        if st.button("המשך ➡️", type="primary"):
            st.session_state.selections = {item: True for item in selected_items}
            
            # Calculate score based on selections
            required = [i['id'] for i in items if i.get('is_required', False)]
            required_standard = [i['id'] for i in items if i.get('is_required', False) and i.get('type') == 'standard']
            required_specific = [i['id'] for i in items if i.get('is_required', False) and i.get('type') == 'specific']
            
            selected_required = [i for i in required if i in selected_items]
            selected_standard = [i for i in required_standard if i in selected_items]
            selected_specific = [i for i in required_specific if i in selected_items]
            distractors = [i for i in selected_items if i not in required]
            
            # Determine outcome and apply consequences
            outcome_type = None
            next_stage = current_stage_idx + 1  # Default
            
            # Check scoring conditions
            if len(selected_required) == len(required) and len(distractors) == 0:
                outcome_type = "optimal_start"
                st.session_state.score += 100
                st.success("✅ הכנה מושלמת!")
            elif len(selected_required) == len(required) and len(distractors) <= 2:
                outcome_type = "good_start"
                st.session_state.score += 80
                st.warning("✓ הכנה טובה, אך החדר מעט צפוף")
            elif len(selected_standard) < len(required_standard):
                outcome_type = "safety_violation"
                st.session_state.score -= 50
                st.error("⚠️ חסר ציוד בטיחות בסיסי! זו הפרת פרוטוקול חמורה")
            elif len(selected_specific) < len(required_specific):
                outcome_type = "hemodynamic_crisis"
                st.session_state.score -= 30
                st.error("⚠️ חסרות משאבות/נוראפינפרין! המטופל יגיע במצב קריטי")
            elif len(distractors) > 3:
                outcome_type = "time_penalty"
                st.session_state.score -= 20
                st.warning("⏱️ החדר צפוף מדי! ההערכה מתעכבת")
            else:
                # Missing some required but not critical
                st.session_state.score += 60
                st.warning("✓ הכנה סבירה, אך חסרים פריטים")
                outcome_type = "good_start"  # Default to reasonable outcome
            
            # Apply consequences if they exist
            if 'consequences' in stage and outcome_type and outcome_type in stage['consequences']:
                cons = stage['consequences'][outcome_type]
                
                # Update patient state
                if 'patient_state' in cons:
                    st.session_state.patient_state.update(cons['patient_state'])
                
                # Get next stage from consequences
                if 'next_stage' in cons:
                    # Convert stage ID to stage index
                    for idx, s in enumerate(scenario['stages']):
                        if s.get('id') == cons['next_stage']:
                            next_stage = idx
                            break
            
            st.session_state.current_stage = next_stage
            st.session_state.stage_start_time = datetime.now()
            st.rerun()
    
    elif stage['type'] == 'branching_choice':
        st.markdown(f"### {stage.get('question', '')}")
        
        # Display options as buttons
        options = stage.get('options', [])
        
        for idx, option in enumerate(options):
            if st.button(option['text'], key=f"option_{idx}", use_container_width=True):
                # Display feedback
                if option.get('is_correct', False):
                    st.success(f"✅ {option.get('explanation', 'נכון!')}")
                    st.session_state.score += option.get('points', 100)
                else:
                    if option.get('is_critical_error', False):
                        st.markdown(f"""
                        <div class="critical-warning">
                            ❌ טעות קטלנית!<br>
                            {option.get('explanation', '')}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error(f"❌ {option.get('explanation', 'לא נכון')}")
                    
                    st.session_state.score += option.get('points', 0)
                
                # Default next stage
                next_stage = current_stage_idx + 1
                
                # Handle consequences if they exist
                if 'consequences' in option:
                    cons = option['consequences']
                    
                    # Update patient state
                    if 'state_change' in cons:
                        st.session_state.patient_state.update(cons['state_change'])
                    
                    # Update patient vitals
                    if 'patient_state' in cons:
                        for key, value in cons['patient_state'].items():
                            st.session_state.patient_state[key] = value
                    
                    # Get next stage from consequences
                    if 'next_stage' in cons:
                        next_stage = cons['next_stage']
                    
                    # Check for game over
                    if cons.get('outcome') == 'death':
                        st.error(f"💀 {cons.get('death_description', 'המטופל נפטר')}")
                        st.markdown(f"**לקח:** {cons.get('lesson', '')}")
                        
                        if st.button("נסה שוב", key="retry_death"):
                            st.session_state.scenario_active = False
                            st.rerun()
                        st.stop()
                    
                    # Check for cardiac arrest (needs CPR)
                    if cons.get('outcome') == 'cardiac_arrest':
                        st.error(f"⚠️ עצירת לב! {cons.get('arrest_description', '')}")
                        if 'next_stage' in cons:
                            next_stage = cons['next_stage']
                
                # Move to next stage
                if isinstance(next_stage, str):
                    # Handle special cases like "game_over"
                    if next_stage == "game_over":
                        st.session_state.current_stage = len(scenario['stages'])
                    else:
                        st.session_state.current_stage = current_stage_idx + 1
                else:
                    # Convert stage ID to stage index
                    # Find the stage with this ID
                    stage_found = False
                    for idx, s in enumerate(scenario['stages']):
                        if s.get('id') == next_stage:
                            st.session_state.current_stage = idx
                            stage_found = True
                            break
                    
                    # If not found by ID, treat as direct index (backward compatibility)
                    if not stage_found:
                        st.session_state.current_stage = next_stage
                
                st.session_state.stage_start_time = datetime.now()
                
                # Small delay to show feedback
                import time
                time.sleep(1.5)
                st.rerun()

# Sidebar with scenario info
with st.sidebar:
    if st.session_state.scenario_active:
        st.markdown("### מידע על התרחיש")
        st.markdown(f"**שם:** {scenario['title']}")
        st.markdown(f"**שלב נוכחי:** {st.session_state.current_stage + 1}/{len(scenario['stages'])}")
        st.markdown(f"**ציון:** {st.session_state.score}")
        
        # Progress bar
        progress = min((st.session_state.current_stage) / len(scenario['stages']), 1.0)
        st.progress(progress)
        
        st.markdown("---")
        
        # Debug info (expandable)
        with st.expander("🔍 מידע טכני"):
            st.json({
                "current_stage_idx": st.session_state.current_stage,
                "total_stages": len(scenario['stages']),
                "patient_state": st.session_state.patient_state,
                "score": st.session_state.score
            })
        
        st.markdown("---")
        
        if st.button("יציאה מהתרחיש", use_container_width=True):
            if st.button("אישור יציאה", key="confirm_exit"):
                st.session_state.scenario_active = False
                st.rerun()
        
        # Learning objectives
        st.markdown("### מטרות למידה")
        for obj in scenario.get('learning_objectives', []):
            st.markdown(f"• {obj}")
