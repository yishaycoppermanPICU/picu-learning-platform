"""
Interactive Patient Examination Component
מרכיב בדיקה פיזיקלית אינטראקטיבית
"""

import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

def create_interactive_patient(patient_data):
    """
    יוצר מטופל אינטראקטיבי עם hotspots
    
    patient_data = {
        'fontanelle': {'status': 'bulging', 'description': 'מרפק בולט'},
        'pupils': {
            'left': {'size': 3, 'reactive': True},
            'right': {'size': 5, 'reactive': False}
        },
        'abdomen': {
            'rigidity': 'soft',
            'tenderness': True,
            'guarding': False
        },
        'chest_drain': {'output': '50 ml/hr', 'color': 'serosanguinous'},
        'skin': {'petechiae': True, 'color': 'pale'},
        'heart_sounds': {'s1': 'normal', 's2': 'split', 'murmur': None}
    }
    """
    
    html_code = f"""
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <meta charset="UTF-8">
        <style>
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }}
            
            body {{
                font-family: Arial, sans-serif;
                direction: rtl;
                background: #f0f2f6;
            }}
            
            .patient-container {{
                position: relative;
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            
            .patient-image {{
                width: 100%;
                height: auto;
                display: block;
                position: relative;
            }}
            
            .hotspot {{
                position: absolute;
                background: rgba(102, 126, 234, 0.3);
                border: 2px solid #667eea;
                border-radius: 50%;
                cursor: pointer;
                transition: all 0.3s;
            }}
            
            .hotspot:hover {{
                background: rgba(102, 126, 234, 0.6);
                transform: scale(1.1);
                box-shadow: 0 0 20px rgba(102, 126, 234, 0.8);
            }}
            
            .hotspot-label {{
                position: absolute;
                background: #667eea;
                color: white;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                white-space: nowrap;
                display: none;
                z-index: 10;
            }}
            
            .hotspot:hover .hotspot-label {{
                display: block;
            }}
            
            .modal {{
                display: none;
                position: fixed;
                z-index: 1000;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.6);
                animation: fadeIn 0.3s;
            }}
            
            @keyframes fadeIn {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}
            
            .modal-content {{
                position: relative;
                background: white;
                margin: 10% auto;
                padding: 30px;
                width: 80%;
                max-width: 500px;
                border-radius: 15px;
                box-shadow: 0 5px 30px rgba(0,0,0,0.3);
                animation: slideIn 0.3s;
                direction: rtl;
            }}
            
            @keyframes slideIn {{
                from {{ transform: translateY(-50px); opacity: 0; }}
                to {{ transform: translateY(0); opacity: 1; }}
            }}
            
            .close {{
                position: absolute;
                left: 15px;
                top: 15px;
                font-size: 28px;
                font-weight: bold;
                color: #aaa;
                cursor: pointer;
                transition: color 0.3s;
            }}
            
            .close:hover {{
                color: #000;
            }}
            
            .modal-title {{
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 20px;
                color: #667eea;
            }}
            
            .finding {{
                margin: 15px 0;
                padding: 15px;
                background: #f8f9fa;
                border-radius: 8px;
                border-right: 4px solid #667eea;
            }}
            
            .finding-label {{
                font-weight: bold;
                color: #333;
                margin-bottom: 5px;
            }}
            
            .finding-value {{
                color: #666;
            }}
            
            .pupil-display {{
                display: flex;
                justify-content: space-around;
                margin: 20px 0;
            }}
            
            .pupil {{
                width: 80px;
                height: 80px;
                background: #87CEEB;
                border-radius: 50%;
                position: relative;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            
            .pupil-inner {{
                background: #000;
                border-radius: 50%;
                transition: all 0.3s;
            }}
            
            .pupil-label {{
                text-align: center;
                margin-top: 10px;
                font-weight: bold;
            }}
            
            .status-badge {{
                display: inline-block;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 14px;
                font-weight: bold;
                margin: 5px 0;
            }}
            
            .status-normal {{
                background: #d4edda;
                color: #155724;
            }}
            
            .status-abnormal {{
                background: #f8d7da;
                color: #721c24;
            }}
            
            .status-critical {{
                background: #dc3545;
                color: white;
            }}
            
            .instruction {{
                background: #e7f3ff;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 20px;
                text-align: center;
                color: #004085;
                font-weight: 500;
            }}
        </style>
    </head>
    <body>
        <div class="patient-container">
            <div class="instruction">
                👆 לחץ על אזורים שונים בגוף לבדיקה פיזיקלית
            </div>
            
            <div style="position: relative;">
                <!-- Patient SVG/Image placeholder -->
                <svg width="100%" height="600" viewBox="0 0 400 600">
                    <!-- Simple patient outline -->
                    <ellipse cx="200" cy="80" rx="40" ry="50" fill="#ffd7b5" stroke="#333" stroke-width="2"/>
                    <rect x="160" y="120" width="80" height="150" rx="10" fill="#e0f7fa" stroke="#333" stroke-width="2"/>
                    <rect x="120" y="130" width="40" height="100" rx="5" fill="#e0f7fa" stroke="#333" stroke-width="2"/>
                    <rect x="240" y="130" width="40" height="100" rx="5" fill="#e0f7fa" stroke="#333" stroke-width="2"/>
                    <rect x="170" y="270" width="25" height="120" rx="5" fill="#e0f7fa" stroke="#333" stroke-width="2"/>
                    <rect x="205" y="270" width="25" height="120" rx="5" fill="#e0f7fa" stroke="#333" stroke-width="2"/>
                    
                    <!-- Eyes -->
                    <circle cx="185" cy="75" r="8" fill="white" stroke="#333" stroke-width="1"/>
                    <circle cx="215" cy="75" r="8" fill="white" stroke="#333" stroke-width="1"/>
                    <circle cx="185" cy="75" r="4" fill="#000"/>
                    <circle cx="215" cy="75" r="4" fill="#000"/>
                </svg>
                
                <!-- Hotspots -->
                <!-- Fontanelle -->
                <div class="hotspot" style="top: 5%; left: 45%; width: 50px; height: 50px;" onclick="showFindings('fontanelle')">
                    <div class="hotspot-label" style="top: -30px; right: -20px;">מרפק</div>
                </div>
                
                <!-- Eyes/Pupils -->
                <div class="hotspot" style="top: 11%; left: 42%; width: 80px; height: 25px; border-radius: 40%;" onclick="showFindings('pupils')">
                    <div class="hotspot-label" style="top: -30px; right: 10px;">אישונים</div>
                </div>
                
                <!-- Chest/Heart -->
                <div class="hotspot" style="top: 25%; left: 45%; width: 60px; height: 60px;" onclick="showFindings('heart')">
                    <div class="hotspot-label" style="top: 60px; right: -10px;">לב</div>
                </div>
                
                <!-- Abdomen -->
                <div class="hotspot" style="top: 38%; left: 43%; width: 70px; height: 70px;" onclick="showFindings('abdomen')">
                    <div class="hotspot-label" style="top: 70px; right: 0;">בטן</div>
                </div>
                
                <!-- Chest Drain -->
                <div class="hotspot" style="top: 30%; left: 70%; width: 40px; height: 40px;" onclick="showFindings('chest_drain')">
                    <div class="hotspot-label" style="top: -30px; left: -40px;">נקז חזה</div>
                </div>
                
                <!-- Skin -->
                <div class="hotspot" style="top: 22%; left: 25%; width: 40px; height="40px;" onclick="showFindings('skin')">
                    <div class="hotspot-label" style="top: -30px; left: -20px;">עור</div>
                </div>
            </div>
        </div>
        
        <!-- Modals -->
        <div id="fontanelleModal" class="modal">
            <div class="modal-content">
                <span class="close" onclick="closeModal('fontanelleModal')">&times;</span>
                <div class="modal-title">🧠 מרפק</div>
                <div class="finding">
                    <div class="finding-label">מצב:</div>
                    <div class="finding-value">
                        <span class="status-badge status-{patient_data.get('fontanelle', {}).get('status_class', 'normal')}">
                            {patient_data.get('fontanelle', {}).get('description', 'נורמוטנסיבי')}
                        </span>
                    </div>
                </div>
                <div class="finding">
                    <div class="finding-label">פרשנות:</div>
                    <div class="finding-value">{patient_data.get('fontanelle', {}).get('interpretation', 'תקין')}</div>
                </div>
            </div>
        </div>
        
        <div id="pupilsModal" class="modal">
            <div class="modal-content">
                <span class="close" onclick="closeModal('pupilsModal')">&times;</span>
                <div class="modal-title">👁️ אישונים</div>
                <div class="pupil-display">
                    <div>
                        <div class="pupil">
                            <div class="pupil-inner" id="leftPupil"></div>
                        </div>
                        <div class="pupil-label">שמאל</div>
                    </div>
                    <div>
                        <div class="pupil">
                            <div class="pupil-inner" id="rightPupil"></div>
                        </div>
                        <div class="pupil-label">ימין</div>
                    </div>
                </div>
                <div class="finding">
                    <div class="finding-label">תגובה לאור:</div>
                    <div class="finding-value" id="pupilReactivity"></div>
                </div>
            </div>
        </div>
        
        <div id="abdomenModal" class="modal">
            <div class="modal-content">
                <span class="close" onclick="closeModal('abdomenModal')">&times;</span>
                <div class="modal-title">🤚 בדיקת בטן</div>
                <div class="finding">
                    <div class="finding-label">קשיות:</div>
                    <div class="finding-value">
                        <span class="status-badge status-{patient_data.get('abdomen', {}).get('rigidity_class', 'normal')}">
                            {patient_data.get('abdomen', {}).get('rigidity', 'רכה')}
                        </span>
                    </div>
                </div>
                <div class="finding">
                    <div class="finding-label">רגישות:</div>
                    <div class="finding-value">{patient_data.get('abdomen', {}).get('tenderness', 'אין רגישות')}</div>
                </div>
                <div class="finding">
                    <div class="finding-label">הגנה (Guarding):</div>
                    <div class="finding-value">{patient_data.get('abdomen', {}).get('guarding', 'אין')}</div>
                </div>
            </div>
        </div>
        
        <div id="heartModal" class="modal">
            <div class="modal-content">
                <span class="close" onclick="closeModal('heartModal')">&times;</span>
                <div class="modal-title">🫀 האזנה ללב</div>
                <div class="finding">
                    <div class="finding-label">קולות לב:</div>
                    <div class="finding-value">{patient_data.get('heart', {}).get('sounds', 'S1+S2 תקינים')}</div>
                </div>
                <div class="finding">
                    <div class="finding-label">אוושה (Murmur):</div>
                    <div class="finding-value">{patient_data.get('heart', {}).get('murmur', 'אין')}</div>
                </div>
            </div>
        </div>
        
        <div id="chest_drainModal" class="modal">
            <div class="modal-content">
                <span class="close" onclick="closeModal('chest_drainModal')">&times;</span>
                <div class="modal-title">💧 נקז חזה</div>
                <div class="finding">
                    <div class="finding-label">תפוקה:</div>
                    <div class="finding-value">
                        <span class="status-badge status-{patient_data.get('chest_drain', {}).get('status_class', 'normal')}">
                            {patient_data.get('chest_drain', {}).get('output', '10 ml/hr')}
                        </span>
                    </div>
                </div>
                <div class="finding">
                    <div class="finding-label">צבע:</div>
                    <div class="finding-value">{patient_data.get('chest_drain', {}).get('color', 'serosanguinous')}</div>
                </div>
            </div>
        </div>
        
        <div id="skinModal" class="modal">
            <div class="modal-content">
                <span class="close" onclick="closeModal('skinModal')">&times;</span>
                <div class="modal-title">🩸 עור</div>
                <div class="finding">
                    <div class="finding-label">צבע:</div>
                    <div class="finding-value">{patient_data.get('skin', {}).get('color', 'ורוד')}</div>
                </div>
                <div class="finding">
                    <div class="finding-label">פטכיות:</div>
                    <div class="finding-value">
                        <span class="status-badge status-{patient_data.get('skin', {}).get('petechiae_class', 'normal')}">
                            {patient_data.get('skin', {}).get('petechiae', 'אין')}
                        </span>
                    </div>
                </div>
                <div class="finding">
                    <div class="finding-label">טורגור:</div>
                    <div class="finding-value">{patient_data.get('skin', {}).get('turgor', 'תקין')}</div>
                </div>
            </div>
        </div>
        
        <script>
            const patientData = {str(patient_data).replace("'", '"')};
            
            function showFindings(type) {{
                const modal = document.getElementById(type + 'Modal');
                modal.style.display = 'block';
                
                if (type === 'pupils') {{
                    updatePupils();
                }}
            }}
            
            function closeModal(modalId) {{
                document.getElementById(modalId).style.display = 'none';
            }}
            
            function updatePupils() {{
                const pupils = patientData.pupils || {{}};
                const left = pupils.left || {{size: 3, reactive: true}};
                const right = pupils.right || {{size: 3, reactive: true}};
                
                const leftPupil = document.getElementById('leftPupil');
                const rightPupil = document.getElementById('rightPupil');
                
                leftPupil.style.width = (left.size * 8) + 'px';
                leftPupil.style.height = (left.size * 8) + 'px';
                
                rightPupil.style.width = (right.size * 8) + 'px';
                rightPupil.style.height = (right.size * 8) + 'px';
                
                let reactivity = '';
                if (left.reactive && right.reactive) {{
                    reactivity = '✅ שני האישונים מגיבים לאור';
                }} else if (!left.reactive && !right.reactive) {{
                    reactivity = '❌ שני האישונים לא מגיבים לאור';
                }} else {{
                    reactivity = '⚠️ תגובה אסימטרית - אישון אחד לא מגיב';
                }}
                
                reactivity += `<br>גודל: שמאל ${left.size}mm, ימין ${right.size}mm`;
                
                document.getElementById('pupilReactivity').innerHTML = reactivity;
            }}
            
            // Close modals when clicking outside
            window.onclick = function(event) {{
                if (event.target.className === 'modal') {{
                    event.target.style.display = 'none';
                }}
            }}
        </script>
    </body>
    </html>
    """
    
    # Display the interactive component
    components.html(html_code, height=800, scrolling=True)
