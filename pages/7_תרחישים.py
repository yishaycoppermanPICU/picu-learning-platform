# -*- coding: utf-8 -*-
import streamlit as st
import sys
import json
from pathlib import Path
from datetime import datetime

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.content_manager import restore_user_session
from utils.styles import get_common_styles

st.set_page_config(
    page_title="תרחישים מתגלגלים",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Restore user session if available
restore_user_session(st)

# CSS מרכזי
st.markdown(get_common_styles(), unsafe_allow_html=True)

# CSS נוסף ספציפי לדף
st.markdown("""
<style>
    /* סיידבר סגור תמיד */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    /* רקע כללי - חזק וברור */
    .main {
        background: linear-gradient(135deg, #1a1f2e 0%, #2a2f3e 50%, #1f2329 100%) !important;
    }
    
    .main * {
        color: #ffffff !important;
        font-size: 1.3rem !important;
    }
    
    /* הגדלת כל הפונטים */
    body {
        font-size: 1.3rem !important;
    }
    
    h1 {
        font-size: 3rem !important;
    }
    
    h2 {
        font-size: 2.5rem !important;
    }
    
    h3 {
        font-size: 2rem !important;
    }
    
    p, div, span, label {
        font-size: 1.3rem !important;
    }
    
    button {
        font-size: 1.2rem !important;
    }
    
    /* כרטיס התרחיש */
    .scenario-container {
        background: rgba(46, 54, 72, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 
            0 10px 40px rgba(0,0,0,0.5),
            inset 0 1px 0 rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .scenario-header {
        background: rgba(102, 126, 234, 0.95);
        backdrop-filter: blur(10px);
        color: #ffffff !important;
        padding: 2.5rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 
            0 8px 32px rgba(102, 126, 234, 0.4),
            inset 0 1px 0 rgba(255,255,255,0.2);
    }
    
    .scenario-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    /* כרטיס שלב */
    .stage-card {
        background: linear-gradient(145deg, #2a3548 0%, #1f2937 100%);
        padding: 2.5rem;
        border-radius: 15px;
        box-shadow: 
            0 8px 24px rgba(0,0,0,0.4),
            inset 0 1px 0 rgba(255,255,255,0.1);
        margin: 1.5rem 0;
        border-right: 5px solid #667eea;
        color: #e5e7eb;
    }
    
    /* רשימת בדיקה */
    .checklist-item {
        background: linear-gradient(135deg, #374151 0%, #1f2937 100%);
        padding: 1.2rem;
        margin: 0.8rem 0;
        border-radius: 10px;
        border-right: 4px solid #10b981;
        color: #f3f4f6;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    }
    
    .checklist-item:hover {
        transform: translateX(-5px);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.3);
    }
    
    /* אזהרה קריטית */
    .critical-warning {
        background: linear-gradient(135deg, #991b1b 0%, #7f1d1d 100%);
        color: #fecaca;
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #dc2626;
        margin: 1.5rem 0;
        font-weight: bold;
        font-size: 1.1rem;
        box-shadow: 
            0 8px 24px rgba(220, 38, 38, 0.4),
            inset 0 1px 0 rgba(255,255,255,0.1);
        animation: pulse-warning 2s ease-in-out infinite;
    }
    
    @keyframes pulse-warning {
        0%, 100% { box-shadow: 0 8px 24px rgba(220, 38, 38, 0.4); }
        50% { box-shadow: 0 8px 32px rgba(220, 38, 38, 0.7); }
    }
    
    /* הודעת הצלחה */
    .success-message {
        background: linear-gradient(135deg, #065f46 0%, #064e3b 100%);
        color: #d1fae5;
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #10b981;
        margin: 1.5rem 0;
        font-weight: 600;
        box-shadow: 
            0 8px 24px rgba(16, 185, 129, 0.4),
            inset 0 1px 0 rgba(255,255,255,0.1);
    }
    
    /* טיימר */
    .timer {
        position: fixed;
        top: 80px;
        left: 20px;
        background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
        color: white;
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        font-size: 1.5rem;
        font-weight: bold;
        z-index: 1000;
        box-shadow: 
            0 8px 24px rgba(220, 38, 38, 0.6),
            inset 0 1px 0 rgba(255,255,255,0.2);
        animation: pulse-timer 1s ease-in-out infinite;
    }
    
    @keyframes pulse-timer {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* כפתורים משופרים */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 28px rgba(102, 126, 234, 0.6);
    }
    
    /* תיבות סימון - טקסט כהה וקריא */
    .stCheckbox {
        background: rgba(255, 255, 255, 0.15) !important;
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .stCheckbox label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
    }
    
    .stCheckbox label span {
        color: #ffffff !important;
    }
    
    /* כותרות - טקסט ממש כהה */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        text-shadow: 0 2px 8px rgba(0,0,0,0.8);
        font-weight: 700 !important;
    }
    
    /* פסקאות וטקסט - כל הטקסט כהה */
    p, li, span, div, label, a {
        color: #ffffff !important;
        font-weight: 500 !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.5);
    }
    
    /* טקסט חזק יותר */
    strong, b {
        color: #ffffff !important;
        font-weight: 800 !important;
    }
    
    /* תיבות מידע - טקסט כהה */
    .stAlert, .stInfo, .stWarning, .stSuccess, .stError {
        background: rgba(255, 255, 255, 0.2) !important;
        color: #ffffff !important;
        color: #f3f4f6 !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
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

# Add background image if scenario has one
def add_background_image(scenario):
    """הוסף תמונת רקע לתרחיש אם קיימת"""
    bg_image = scenario.get('background_image', '')
    if bg_image:
        import base64
        img_path = Path(__file__).parent.parent / "data" / "scenarios" / "images" / bg_image
        if img_path.exists():
            try:
                from PIL import Image
                import io
                
                # Compress and encode image
                img = Image.open(img_path)
                if img.width > 1920:
                    ratio = 1920 / img.width
                    new_size = (1920, int(img.height * ratio))
                    img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                buffer = io.BytesIO()
                img.save(buffer, format='JPEG', quality=75, optimize=True)
                img_base64 = base64.b64encode(buffer.getvalue()).decode()
                
                st.markdown(f"""
                <style>
                    .stApp {{
                        background-image: url(data:image/jpeg;base64,{img_base64});
                        background-size: cover;
                        background-position: center;
                        background-repeat: no-repeat;
                        background-attachment: fixed;
                    }}
                    .stApp::before {{
                        content: "";
                        position: fixed;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        background: rgba(0, 0, 0, 0.5);
                        z-index: -1;
                    }}
                </style>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.warning(f"לא ניתן לטעון תמונת רקע: {e}")
    if bg_image:
        # Settings
        settings = scenario.get('background_settings', {})
        overlay_opacity = settings.get('overlay_opacity', 0.6)
        
        # Display image using st.image with custom CSS
        bg_path = Path(__file__).parent.parent / "data" / "scenarios" / "images" / bg_image
        
        if bg_path.exists():
            # Use custom HTML/CSS for background
            st.markdown(f"""
            <style>
                [data-testid="stAppViewContainer"] {{
                    background: linear-gradient(180deg, 
                        rgba(26,31,46,{overlay_opacity}) 0%, 
                        rgba(31,35,41,{overlay_opacity + 0.1}) 100%);
                }}
                
                [data-testid="stAppViewContainer"]::before {{
                    content: '';
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background-image: url('data:image/png;base64,__IMAGE_PLACEHOLDER__');
                    background-size: cover;
                    background-position: center;
                    background-repeat: no-repeat;
                    z-index: -1;
                    opacity: 0.4;
                }}
                
                .main {{
                    background: transparent !important;
                }}
            </style>
            """, unsafe_allow_html=True)
        
        elif bg_image.startswith('http'):
            # URL image
            gradient_css = ""
            if use_gradient:
                gradient_css = "linear-gradient(180deg, rgba(10,14,39,0.7) 0%, rgba(10,14,39,0.9) 100%),"
            
            st.markdown(f"""
            <style>
                .main {{
                    background: 
                        {gradient_css}
                        url({bg_image});
                    background-size: cover;
                    background-position: center;
                    background-attachment: fixed;
                    background-repeat: no-repeat;
                }}
                
                .main::before {{
                    content: '';
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(10, 14, 39, {overlay_opacity});
                    backdrop-filter: blur({blur_amount}px);
                    z-index: -1;
                }}
            </style>
            """, unsafe_allow_html=True)

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

# Add background image to main selection page too
default_bg = Path(__file__).parent.parent / "data" / "scenarios" / "images" / "תמונת חדר טיפול נמרץ ילדים.png"
if default_bg.exists():
    try:
        import base64
        from PIL import Image
        import io
        
        img = Image.open(default_bg)
        if img.width > 1920:
            ratio = 1920 / img.width
            new_size = (1920, int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=75, optimize=True)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        st.markdown(f"""
        <style>
            .stApp {{
                background-image: url(data:image/jpeg;base64,{img_base64});
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            .stApp::before {{
                content: "";
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.6);
                z-index: -1;
            }}
        </style>
        """, unsafe_allow_html=True)
    except:
        pass

# Scenario Selection Screen
if not st.session_state.scenario_active:
    st.markdown("### 🎯 בחר תרחיש")
    
    for scenario in scenarios:
        # כל תרחיש בקופסה חצי שקופה
        st.markdown("""
        <div style="background: rgba(30, 35, 50, 0.9); 
                    backdrop-filter: blur(10px);
                    border-radius: 15px; 
                    padding: 2rem; 
                    margin: 1.5rem 0;
                    border: 1px solid rgba(102, 126, 234, 0.3);
                    box-shadow: 0 8px 24px rgba(0,0,0,0.4);">
        """, unsafe_allow_html=True)
        
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
                    
                    # Apply background image
                    add_background_image(scenario)
                    
                    st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")

# Active Scenario Screen
else:
    scenario = st.session_state.current_scenario
    current_stage_idx = st.session_state.current_stage
    
    # Apply background image for active scenario
    add_background_image(scenario)
    
    # Check if scenario is complete or if we're at conclusion stage
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
        
        # Display learning points from conclusion stage if exists
        if len(scenario['stages']) > 0 and scenario['stages'][-1].get('type') == 'conclusion':
            learning_points = scenario['stages'][-1].get('learning_points', [])
            if learning_points:
                st.markdown("#### נקודות למידה:")
                for point in learning_points:
                    st.markdown(f"💡 {point}")
            
            # Display references if exists
            references = scenario['stages'][-1].get('references', [])
            if references:
                with st.expander("📚 מקורות"):
                    for ref in references:
                        st.markdown(f"• {ref}")
        # Otherwise display learning points from main scenario
        elif scenario.get('learning_points'):
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
    
    # Display patient vitals on monitor (left side, smaller)
    if st.session_state.patient_state:
        from utils.monitor_display import create_monitor_display
        from utils.icu_sounds import create_icu_ambient_sound
        import random
        
        # Create three columns: left for monitor, middle for images, right for text
        mon_col, img_col, info_col = st.columns([1, 1, 2])
        
        with mon_col:
            # Add slight variation to vitals for realism (±1-2)
            # Use stage number as seed for consistency within same stage
            random.seed(current_stage_idx * 100)
            
            def add_variation(value, variation_range=2):
                """הוסף וריאציה קלה לערך"""
                if value == '--' or not isinstance(value, (int, float)):
                    return value
                variation = random.randint(-variation_range, variation_range)
                return max(0, int(value + variation))
            
            def vary_bp(bp_str):
                """הוסף וריאציה ללחץ דם"""
                if bp_str == '--/--' or '/' not in str(bp_str):
                    return bp_str
                try:
                    sys, dia = map(int, str(bp_str).split('/'))
                    sys_var = random.randint(-3, 3)
                    dia_var = random.randint(-2, 2)
                    return f"{max(40, sys + sys_var)}/{max(20, dia + dia_var)}"
                except:
                    return bp_str
            
            vitals = {
                'hr': add_variation(st.session_state.patient_state.get('hr', '--'), 3),
                'bp': vary_bp(st.session_state.patient_state.get('bp', '--/--')),
                'sat': add_variation(st.session_state.patient_state.get('sat', '--'), 1),
                'rr': add_variation(st.session_state.patient_state.get('rr', '--'), 2),
                'temp': st.session_state.patient_state.get('temp', '--')
            }
            
            # Scale down monitor for side display
            st.markdown('<div style="transform: scale(0.65); transform-origin: top left;">', unsafe_allow_html=True)
            create_monitor_display(vitals)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Add ICU ambient sounds
            create_icu_ambient_sound(vitals)
        
        with img_col:
            # Display clinical images between monitor and text
            if 'context' in stage:
                context = stage['context']
                if isinstance(context, dict) and 'clinical_images' in context:
                    st.markdown("### 📸 ממצאים")
                    for img_info in context['clinical_images']:
                        img_path = Path(__file__).parent.parent / "data" / "scenarios" / "images" / img_info['file']
                        if img_path.exists():
                            st.image(str(img_path), caption=img_info.get('caption', ''), use_container_width=True)
                        else:
                            st.markdown(f"""
                            <div style="background: rgba(102, 126, 234, 0.2); 
                                        padding: 1rem; 
                                        border-radius: 8px; 
                                        border: 2px dashed rgba(102, 126, 234, 0.5);
                                        text-align: center;
                                        margin: 1rem 0;">
                                <p style="font-size: 1rem !important;">🔍 {img_info.get('description', img_info['file'])}</p>
                            </div>
                            """, unsafe_allow_html=True)
        
        with info_col:
            # Display clinical information in right column
            st.markdown("""
            <div style="background: rgba(0, 0, 0, 0.7); padding: 2rem; border-radius: 15px; margin-top: 1rem;">
            """, unsafe_allow_html=True)
            
            # Context information
            if 'context' in stage:
                context = stage['context']
                if isinstance(context, dict):
                    if 'text' in context:
                        st.markdown(f"### 📋 מצב קליני")
                        st.markdown(f"<p style='font-size: 1.4rem !important;'>{context['text']}</p>", unsafe_allow_html=True)
                    
                    if 'physical_exam' in context:
                        st.markdown(f"### 🔍 בדיקה גופנית")
                        st.markdown(f"<p style='font-size: 1.3rem !important;'>{context['physical_exam']}</p>", unsafe_allow_html=True)
                    
                    if 'labs' in context:
                        st.markdown(f"### 🧪 בדיקות מעבדה")
                        st.markdown(f"<p style='font-size: 1.3rem !important;'>{context['labs']}</p>", unsafe_allow_html=True)
                    
                    if 'labs_pending' in context:
                        st.markdown(f"### ⏳ ממתין לתוצאות")
                        st.markdown(f"<p style='font-size: 1.3rem !important;'>{context['labs_pending']}</p>", unsafe_allow_html=True)
                    
                    if 'abg' in context:
                        st.markdown(f"### 💨 גזי דם (ABG)")
                        st.markdown(f"<p style='font-size: 1.3rem !important; font-family: monospace;'>{context['abg']}</p>", unsafe_allow_html=True)
                
                else:
                    st.markdown(f"### 📋 מצב")
                    st.markdown(f"<p style='font-size: 1.4rem !important;'>{context}</p>", unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Display stage content with semi-transparent background
    st.markdown("""
    <div style="background: rgba(30, 35, 50, 0.9); 
                backdrop-filter: blur(10px);
                border-radius: 15px; 
                padding: 2rem; 
                margin: 1.5rem 0;
                border: 1px solid rgba(102, 126, 234, 0.3);
                box-shadow: 0 8px 24px rgba(0,0,0,0.4);">
    """, unsafe_allow_html=True)
    
    st.markdown(f"## שלב {current_stage_idx + 1}: {stage['title']}")
    
    # Display stage image if exists
    if stage.get('image'):
        image_path = Path(__file__).parent.parent / "data" / "scenarios" / "images" / stage['image']
        if image_path.exists():
            st.image(str(image_path), use_container_width=True)
        else:
            # If it's a URL
            if stage['image'].startswith('http'):
                st.image(stage['image'], use_container_width=True)
    
    # Handle conclusion stage specially
    if stage.get('type') == 'conclusion':
        context = stage.get('context', {})
        
        # Display success outcome by default (or based on score)
        outcome_type = 'success' if st.session_state.score >= 0 else 'failure'
        outcome_info = context.get(outcome_type, {})
        
        if outcome_info:
            st.markdown("### סיכום התרחיש")
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
            
            # Display lesson if failure
            if outcome_type == 'failure' and outcome_info.get('lesson'):
                st.error(f"**לקח:** {outcome_info['lesson']}")
        
        # Display learning points
        learning_points = stage.get('learning_points', [])
        if learning_points:
            st.markdown("#### נקודות למידה:")
            for point in learning_points:
                st.markdown(f"{point}")
        
        # Display references
        references = stage.get('references', [])
        if references:
            with st.expander("📚 מקורות"):
                for ref in references:
                    st.markdown(f"• {ref}")
        
        # Navigation buttons
        st.divider()
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
        
        st.stop()  # Don't process further
    
    
    # Display stage content
    st.markdown(f"## שלב {current_stage_idx + 1}: {stage['title']}")
    
    # Handle different stage types
    if stage['type'] == 'interactive_examination':
        # Interactive physical examination with real image
        from utils.interactive_patient_image import create_interactive_patient_with_image
        
        st.markdown("### 🩺 בדיקה פיזיקלית אינטראקטיבית")
        
        patient_findings = stage.get('patient_findings', {})
        create_interactive_patient_with_image(patient_findings)
        
        # Continue button
        if st.button("המשך ➡️", type="primary", use_container_width=True):
            st.session_state.current_stage += 1
            st.session_state.stage_start_time = datetime.now()
            st.rerun()
    
    elif stage['type'] == 'checklist_selection':
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
        
        # Shuffle options to randomize order
        import random
        options = stage.get('options', [])[:]  # Create a copy
        
        # Create a seed based on stage ID to keep shuffling consistent per stage
        random.seed(stage.get('id', 0))
        random.shuffle(options)
        
        # Display options as buttons
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
    
    # Close the semi-transparent div for stage content
    st.markdown("</div>", unsafe_allow_html=True)

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
