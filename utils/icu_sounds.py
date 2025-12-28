# -*- coding: utf-8 -*-
"""
ICU Ambient Sounds Component
Uses real audio files for realistic PICU monitor sounds
"""

import streamlit.components.v1 as components
from pathlib import Path
import base64

def create_icu_ambient_sound(vitals):
    """
    Create ambient ICU sounds using real audio files
    
    Parameters:
    - vitals: dict with keys: hr, sat, bp
    
    Features:
    - QRS beep synchronized with heart rate (real audio)
    - Pulse oximeter tone that changes with SpO2 (real audio)
    - Alarms for critical values (real audio)
    - Ventilator sounds (real background audio)
    """
    
    hr = vitals.get('hr', 100)
    sat = vitals.get('sat', 98)
    
    # Handle non-numeric values
    if hr == '--' or not isinstance(hr, (int, float)):
        hr = 100
    if sat == '--' or not isinstance(sat, (int, float)):
        sat = 98
    
    # Load audio files as base64
    sounds_dir = Path(__file__).parent.parent / "data" / "sounds"
    audio_data = {}
    
    # Try to load real audio files
    sound_files = {
        'qrs': 'qrs_beep.mp3',
        'alarm': 'alarm_critical.mp3',
        'vent_alarm': 'ventilator_alarm.mp3',
        'spo2_high': 'spo2_high.mp3',
        'spo2_med': 'spo2_medium.mp3',
        'spo2_low': 'spo2_low.mp3'
    }
    
    for key, filename in sound_files.items():
        sound_path = sounds_dir / filename
        if sound_path.exists():
            try:
                with open(sound_path, 'rb') as f:
                    audio_data[key] = base64.b64encode(f.read()).decode()
            except:
                audio_data[key] = None
        else:
            audio_data[key] = None
    
    # Build audio file objects for JavaScript
    audio_objects = []
    for key, data in audio_data.items():
        if data:
            audio_objects.append(f'"{key}": "data:audio/mp3;base64,{data}"')
    
    audio_files_js = '{' + ','.join(audio_objects) + '}' if audio_objects else '{}'
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .sound-control {{
                position: fixed;
                top: 10px;
                right: 10px;
                z-index: 10000;
                background: rgba(0, 0, 0, 0.8);
                padding: 10px 15px;
                border-radius: 8px;
                color: white;
                font-family: sans-serif;
                font-size: 14px;
                display: flex;
                align-items: center;
                gap: 10px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.5);
            }}
            
            .sound-btn {{
                background: #667eea;
                border: none;
                color: white;
                padding: 8px 15px;
                border-radius: 6px;
                cursor: pointer;
                font-weight: bold;
                transition: all 0.3s;
            }}
            
            .sound-btn:hover {{
                background: #5568d3;
                transform: scale(1.05);
            }}
            
            .sound-btn.muted {{
                background: #dc2626;
            }}
            
            .volume-slider {{
                width: 80px;
                cursor: pointer;
            }}
            
            .sound-indicator {{
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #10b981;
                animation: pulse 1s infinite;
            }}
            
            @keyframes pulse {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.3; }}
            }}
        </style>
    </head>
    <body>
        <div class="sound-control">
            <button class="sound-btn" onclick="toggleSound()">🔊 סאונד ICU</button>
            <input type="range" class="volume-slider" min="0" max="100" value="40" onchange="updateVolume(this.value)">
            <div class="sound-indicator" id="indicator"></div>
        </div>
        
        <script>
            const HR = {hr};
            const SAT = {sat};
            let isPlaying = false;
            let qrsInterval;
            let alarmTimeout;
            let masterVolume = 0.4;
            
            // Audio files loaded from server
            const audioFiles = {audio_files_js};
            
            function playAudio(key, volume = 1.0) {{
                if (!isPlaying || !audioFiles[key]) return;
                
                try {{
                    const audio = new Audio(audioFiles[key]);
                    audio.volume = masterVolume * volume;
                    audio.play().catch(e => console.log('Audio play failed:', e));
                }} catch (e) {{
                    console.log('Error playing audio:', e);
                }}
            }}
            
            function playQRSBeep() {{
                playAudio('qrs', 0.8);
            }}
            
            function playPulseOxTone() {{
                // Play appropriate SpO2 tone based on saturation
                if (SAT >= 95) {{
                    playAudio('spo2_high', 0.6);
                }} else if (SAT >= 90) {{
                    playAudio('spo2_med', 0.6);
                }} else {{
                    playAudio('spo2_low', 0.7);
                }}
            }}
            
            function playAlarm() {{
                playAudio('alarm', 1.0);
            }}
            
            function playVentilatorAlarm() {{
                playAudio('vent_alarm', 0.7);
            }}
            
            function startSounds() {{
                if (Object.keys(audioFiles).length === 0) {{
                    alert('לא נמצאו קבצי סאונד. נא להעלות קבצי MP3 לתיקיית data/sounds/');
                    return;
                }}
                
                // QRS beep interval based on HR
                const qrsIntervalMs = 60000 / HR;
                qrsInterval = setInterval(() => {{
                    playQRSBeep();
                    // Pulse ox tone plays with QRS for synchronization
                    setTimeout(() => playPulseOxTone(), 100);
                }}, qrsIntervalMs);
                
                // Alarms for critical values
                if (SAT < 90 || HR > 160 || HR < 60) {{
                    alarmTimeout = setInterval(() => {{
                        playAlarm();
                    }}, 15000); // Every 15 seconds
                }}
                
                // Occasional ventilator alarm for low SpO2
                if (SAT < 92) {{
                    setInterval(() => {{
                        if (Math.random() > 0.8) {{ // 20% chance
                            playVentilatorAlarm();
                        }}
                    }}, 20000);
                }}
            }}
            
            function stopSounds() {{
                if (qrsInterval) clearInterval(qrsInterval);
                if (alarmTimeout) clearInterval(alarmTimeout);
            }}
            
            function toggleSound() {{
                const btn = document.querySelector('.sound-btn');
                const indicator = document.getElementById('indicator');
                
                if (isPlaying) {{
                    stopSounds();
                    isPlaying = false;
                    btn.classList.add('muted');
                    btn.textContent = '🔇 סאונד ICU';
                    indicator.style.background = '#dc2626';
                }} else {{
                    isPlaying = true;
                    startSounds();
                    btn.classList.remove('muted');
                    btn.textContent = '🔊 סאונד ICU';
                    indicator.style.background = '#10b981';
                }}
            }}
            
            function updateVolume(value) {{
                masterVolume = value / 100;
            }}
            
            // Note: Audio will NOT auto-start due to browser policies
            // User must click the sound button to enable
        </script>
    </body>
    </html>
    """
    
    components.html(html_code, height=0)
