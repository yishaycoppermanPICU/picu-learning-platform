# -*- coding: utf-8 -*-
"""
מרכיב ויזואלי של מוניטור PICU - מציג פרמטרים חיוניים בצורה ריאליסטית
"""
import streamlit as st
import streamlit.components.v1 as components

def create_monitor_display(vitals):
    """
    יוצר תצוגת מוניטור PICU אינטראקטיבית
    
    Parameters:
    -----------
    vitals : dict
        מילון עם פרמטרים חיוניים:
        - hr: Heart Rate (מספר)
        - bp: Blood Pressure (string, e.g., "120/80")
        - sat: SpO2 (מספר, 0-100)
        - rr: Respiratory Rate (מספר)
        - temp: טמפרטורה (אופציונלי, מספר)
        - etco2: End-Tidal CO2 (אופציונלי, מספר)
    """
    
    # ערכים דיפולטיביים
    hr = vitals.get('hr', '--')
    bp = vitals.get('bp', '--/--')
    sat = vitals.get('sat', '--')
    rr = vitals.get('rr', '--')
    temp = vitals.get('temp', '--')
    etco2 = vitals.get('etco2', '--')
    
    # קביעת צבעים לפי ערכים
    def get_hr_color(hr_val):
        if hr_val == '--': return '#666'
        try:
            hr_num = int(hr_val)
            if hr_num < 60 or hr_num > 160: return '#ff3333'  # אדום
            if hr_num < 70 or hr_num > 140: return '#ffaa00'  # כתום
            return '#00ff00'  # ירוק
        except:
            return '#666'
    
    def get_sat_color(sat_val):
        if sat_val == '--': return '#666'
        try:
            sat_num = int(sat_val)
            if sat_num < 88: return '#ff3333'  # אדום
            if sat_num < 92: return '#ffaa00'  # כתום
            return '#00ff00'  # ירוק
        except:
            return '#666'
    
    def get_bp_color(bp_val):
        if bp_val == '--/--': return '#666'
        try:
            systolic = int(bp_val.split('/')[0])
            if systolic < 70 or systolic > 130: return '#ff3333'  # אדום
            if systolic < 80 or systolic > 120: return '#ffaa00'  # כתום
            return '#00ff00'  # ירוק
        except:
            return '#666'
    
    hr_color = get_hr_color(hr)
    sat_color = get_sat_color(sat)
    bp_color = get_bp_color(bp)
    rr_color = '#00ff00' if rr != '--' else '#666'
    
    # HTML של המוניטור
    monitor_html = f"""
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <meta charset="utf-8">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Courier New', monospace;
            }}
            
            body {{
                background: #000;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }}
            
            .monitor {{
                background: linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%);
                border: 8px solid #2a2a2a;
                border-radius: 20px;
                padding: 30px;
                box-shadow: 
                    0 0 30px rgba(0,255,255,0.3),
                    inset 0 0 20px rgba(0,0,0,0.8);
                width: 100%;
                max-width: 900px;
            }}
            
            .monitor-header {{
                text-align: center;
                color: #00ffff;
                font-size: 18px;
                margin-bottom: 20px;
                text-shadow: 0 0 10px #00ffff;
                letter-spacing: 3px;
            }}
            
            .monitor-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
            }}
            
            .vital-box {{
                background: #0a0a0a;
                border: 2px solid #333;
                border-radius: 10px;
                padding: 20px;
                position: relative;
                box-shadow: inset 0 0 15px rgba(0,0,0,0.8);
            }}
            
            .vital-label {{
                font-size: 14px;
                color: #888;
                margin-bottom: 5px;
                letter-spacing: 1px;
            }}
            
            .vital-value {{
                font-size: 48px;
                font-weight: bold;
                text-shadow: 0 0 15px currentColor;
                animation: pulse 2s ease-in-out infinite;
                direction: ltr;
                text-align: center;
            }}
            
            .vital-unit {{
                font-size: 20px;
                color: #888;
                margin-right: 10px;
            }}
            
            @keyframes pulse {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.8; }}
            }}
            
            .hr-box {{
                grid-column: 1 / 2;
            }}
            
            .hr-box .vital-value {{
                color: {hr_color};
            }}
            
            .bp-box {{
                grid-column: 2 / 3;
            }}
            
            .bp-box .vital-value {{
                color: {bp_color};
                font-size: 40px;
            }}
            
            .sat-box {{
                grid-column: 1 / 2;
            }}
            
            .sat-box .vital-value {{
                color: {sat_color};
            }}
            
            .rr-box {{
                grid-column: 2 / 3;
            }}
            
            .rr-box .vital-value {{
                color: {rr_color};
            }}
            
            .waveform {{
                width: 100%;
                height: 60px;
                margin-top: 10px;
                background: #000;
                border-radius: 5px;
                position: relative;
                overflow: hidden;
            }}
            
            .ecg-line {{
                position: absolute;
                bottom: 30px;
                left: 0;
                width: 200%;
                height: 2px;
                background: {hr_color};
                animation: ecg-move 2s linear infinite;
                box-shadow: 0 0 10px {hr_color};
            }}
            
            @keyframes ecg-move {{
                0% {{ transform: translateX(0); }}
                100% {{ transform: translateX(-50%); }}
            }}
            
            .pleth-wave {{
                position: absolute;
                bottom: 0;
                left: 0;
                width: 100%;
                height: 100%;
            }}
            
            .pleth-wave svg {{
                width: 100%;
                height: 100%;
            }}
            
            .alarm-indicator {{
                position: absolute;
                top: 10px;
                left: 10px;
                width: 12px;
                height: 12px;
                border-radius: 50%;
                background: #333;
            }}
            
            .alarm-active {{
                background: #ff3333;
                animation: blink 0.5s ease-in-out infinite;
            }}
            
            @keyframes blink {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.3; }}
            }}
            
            .monitor-footer {{
                margin-top: 20px;
                text-align: center;
                color: #666;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="monitor">
            <div class="monitor-header">
                PEDIATRIC ICU MONITOR
            </div>
            
            <div class="monitor-grid">
                <!-- Heart Rate -->
                <div class="vital-box hr-box">
                    <div class="alarm-indicator {'alarm-active' if hr_color == '#ff3333' else ''}"></div>
                    <div class="vital-label">HR (Heart Rate)</div>
                    <div class="vital-value">
                        {hr}
                        <span class="vital-unit">bpm</span>
                    </div>
                    <div class="waveform">
                        <div class="ecg-line"></div>
                    </div>
                </div>
                
                <!-- Blood Pressure -->
                <div class="vital-box bp-box">
                    <div class="alarm-indicator {'alarm-active' if bp_color == '#ff3333' else ''}"></div>
                    <div class="vital-label">BP (Blood Pressure)</div>
                    <div class="vital-value">
                        {bp}
                        <span class="vital-unit">mmHg</span>
                    </div>
                </div>
                
                <!-- SpO2 -->
                <div class="vital-box sat-box">
                    <div class="alarm-indicator {'alarm-active' if sat_color == '#ff3333' else ''}"></div>
                    <div class="vital-label">SpO₂ (Oxygen Saturation)</div>
                    <div class="vital-value">
                        {sat}
                        <span class="vital-unit">%</span>
                    </div>
                    <div class="waveform">
                        <div class="pleth-wave">
                            <svg viewBox="0 0 200 60" xmlns="http://www.w3.org/2000/svg">
                                <path d="M0,30 Q10,30 20,10 T40,30 Q50,30 60,10 T80,30 Q90,30 100,10 T120,30 Q130,30 140,10 T160,30 Q170,30 180,10 T200,30" 
                                      fill="none" 
                                      stroke="{sat_color}" 
                                      stroke-width="2"
                                      style="filter: drop-shadow(0 0 5px {sat_color});">
                                    <animate attributeName="d" 
                                             dur="2s" 
                                             repeatCount="indefinite"
                                             values="M0,30 Q10,30 20,10 T40,30 Q50,30 60,10 T80,30 Q90,30 100,10 T120,30 Q130,30 140,10 T160,30 Q170,30 180,10 T200,30;
                                                     M0,30 Q10,30 20,15 T40,30 Q50,30 60,15 T80,30 Q90,30 100,15 T120,30 Q130,30 140,15 T160,30 Q170,30 180,15 T200,30;
                                                     M0,30 Q10,30 20,10 T40,30 Q50,30 60,10 T80,30 Q90,30 100,10 T120,30 Q130,30 140,10 T160,30 Q170,30 180,10 T200,30"/>
                                </path>
                            </svg>
                        </div>
                    </div>
                </div>
                
                <!-- Respiratory Rate -->
                <div class="vital-box rr-box">
                    <div class="alarm-indicator"></div>
                    <div class="vital-label">RR (Respiratory Rate)</div>
                    <div class="vital-value">
                        {rr}
                        <span class="vital-unit">br/min</span>
                    </div>
                </div>
            </div>
            
            <div class="monitor-footer">
                SIMULATED MONITOR - FOR EDUCATIONAL USE ONLY
            </div>
        </div>
    </body>
    </html>
    """
    
    # הצגת המוניטור
    components.html(monitor_html, height=600, scrolling=False)
