"""
Interactive Patient Examination with Real Image
בדיקה פיזיקלית אינטראקטיבית עם תמונה אמיתית
"""

import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64

def create_interactive_patient_with_image(patient_data, patient_image="תמונת חדר טיפול נמרץ ילדים+ילד במיטה.png"):
    """
    בדיקה פיזיקלית עם תמונה אמיתית וטקסט ממצאים
    """
    
    # Load patient image
    img_path = Path(__file__).parent.parent / "data" / "scenarios" / "images" / patient_image
    
    if not img_path.exists():
        st.error(f"לא נמצאה תמונה: {patient_image}")
        return
    
    # Extract findings from patient_data
    pupils = patient_data.get('pupils', {})
    pupils_text = f"""
    <strong>אישונים (Pupils):</strong><br>
    {pupils.get('symmetry', 'לא זמין')}<br>
    {pupils.get('left', {}).get('description', '')}<br>
    {pupils.get('right', {}).get('description', '')}<br>
    {pupils.get('interpretation', '')}
    """
    
    skin = patient_data.get('skin', {})
    skin_text = f"""
    <strong>עור ופנים:</strong><br>
    <strong>צבע:</strong> {skin.get('color', 'לא זמין')}<br>
    <strong>פטכיות:</strong> {skin.get('petechiae', 'לא זמין')}<br>
    <strong>טמפרטורה:</strong> {skin.get('temperature', 'לא זמין')}<br>
    <strong>CRT:</strong> {skin.get('capillary_refill', 'לא זמין')}<br>
    {skin.get('interpretation', '')}
    """
    
    abdomen = patient_data.get('abdomen', {})
    abdomen_text = f"""
    <strong>בטן (Abdomen):</strong><br>
    <strong>קשיות:</strong> {abdomen.get('rigidity', 'לא זמין')}<br>
    <strong>רגישות:</strong> {abdomen.get('tenderness', 'לא זמין')}<br>
    <strong>הגנה:</strong> {abdomen.get('guarding', 'לא זמין')}<br>
    {abdomen.get('additional_findings', '')}
    """
    
    heart = patient_data.get('heart', {})
    heart_text = f"""
    <strong>לב (Heart):</strong><br>
    <strong>קולות:</strong> {heart.get('sounds', 'לא זמין')}<br>
    <strong>אוושה:</strong> {heart.get('murmur', 'לא זמין')}<br>
    {heart.get('interpretation', '')}
    """
    
    # HTML component with real image and clickable hotspots
    html_content = f"""
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <meta charset="utf-8">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            
            body {{
                background: #1a1f2e;
                color: #ffffff;
                padding: 20px;
                direction: rtl;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                position: relative;
            }}
            
            .instruction {{
                text-align: center;
                font-size: 1.3rem;
                color: #00ffff;
                margin-bottom: 20px;
                padding: 15px;
                background: rgba(0, 255, 255, 0.1);
                border-radius: 10px;
                font-weight: 600;
            }}
            
            .patient-container {{
                position: relative;
                width: 100%;
                margin: 0 auto;
            }}
            
            .patient-image {{
                width: 100%;
                height: auto;
                display: block;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.5);
            }}
            
            .hotspot {{
                position: absolute;
                border: 3px solid #00ffff;
                background: rgba(0, 255, 255, 0.2);
                border-radius: 50%;
                cursor: pointer;
                transition: all 0.3s ease;
                animation: pulse 2s ease-in-out infinite;
            }}
            
            .hotspot:hover {{
                background: rgba(0, 255, 255, 0.4);
                transform: scale(1.1);
                box-shadow: 0 0 20px rgba(0, 255, 255, 0.6);
            }}
            
            @keyframes pulse {{
                0%, 100% {{
                    box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
                }}
                50% {{
                    box-shadow: 0 0 25px rgba(0, 255, 255, 0.8);
                }}
            }}
            
            /* Hotspot positions - adjusted for child in bed image */
            .hotspot-eyes {{
                top: 18%;
                right: 42%;
                width: 80px;
                height: 40px;
                border-radius: 40px;
            }}
            
            .hotspot-face {{
                top: 16%;
                right: 38%;
                width: 110px;
                height: 110px;
            }}
            
            .hotspot-chest {{
                top: 32%;
                right: 40%;
                width: 100px;
                height: 80px;
                border-radius: 40px;
            }}
            
            .hotspot-abdomen {{
                top: 45%;
                right: 41%;
                width: 90px;
                height: 70px;
                border-radius: 35px;
            }}
            
            /* Modal */
            .modal {{
                display: none;
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: linear-gradient(145deg, #2e3648 0%, #353e55 100%);
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.8);
                z-index: 1000;
                max-width: 500px;
                width: 90%;
                border: 2px solid rgba(0, 255, 255, 0.3);
            }}
            
            .modal.active {{
                display: block;
                animation: modalAppear 0.3s ease;
            }}
            
            @keyframes modalAppear {{
                from {{
                    opacity: 0;
                    transform: translate(-50%, -60%);
                }}
                to {{
                    opacity: 1;
                    transform: translate(-50%, -50%);
                }}
            }}
            
            .modal h2 {{
                color: #00ffff;
                margin-bottom: 20px;
                font-size: 1.8rem;
                text-align: center;
            }}
            
            .modal-content {{
                color: #ffffff;
                font-size: 1.1rem;
                line-height: 1.8;
                text-align: right;
            }}
            
            .modal-content strong {{
                color: #00ffff;
                display: block;
                margin-top: 15px;
                margin-bottom: 5px;
            }}
            
            .close-btn {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 10px;
                cursor: pointer;
                font-size: 1.1rem;
                margin-top: 20px;
                width: 100%;
                font-weight: 600;
                transition: all 0.3s ease;
            }}
            
            .close-btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
            }}
            
            .overlay {{
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.8);
                z-index: 999;
            }}
            
            .overlay.active {{
                display: block;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="instruction">
                👆 לחץ על אזורים שונים בגוף לבדיקה פיזיקלית
            </div>
            
            <div class="patient-container">
                <img src="data:image/png;base64,__IMAGE_DATA__" class="patient-image" alt="Patient">
                
                <!-- Hotspots -->
                <div class="hotspot hotspot-eyes" onclick="showModal('eyes')" title="בדוק אישונים"></div>
                <div class="hotspot hotspot-face" onclick="showModal('skin')" title="בדוק עור ופנים"></div>
                <div class="hotspot hotspot-chest" onclick="showModal('heart')" title="האזן ללב"></div>
                <div class="hotspot hotspot-abdomen" onclick="showModal('abdomen')" title="מישוש בטן"></div>
            </div>
        </div>
        
        <!-- Overlay -->
        <div class="overlay" id="overlay" onclick="closeModal()"></div>
        
        <!-- Modals -->
        <div class="modal" id="modal-eyes">
            <h2>👁️ בדיקת אישונים</h2>
            <div class="modal-content">
                {pupils_text}
            </div>
            <button class="close-btn" onclick="closeModal()">סגור</button>
        </div>
        
        <div class="modal" id="modal-skin">
            <h2>🩸 בדיקת עור ופנים</h2>
            <div class="modal-content">
                {skin_text}
            </div>
            <button class="close-btn" onclick="closeModal()">סגור</button>
        </div>
        
        <div class="modal" id="modal-heart">
            <h2>🫀 האזנה ללב</h2>
            <div class="modal-content">
                {heart_text}
            </div>
            <button class="close-btn" onclick="closeModal()">סגור</button>
        </div>
        
        <div class="modal" id="modal-abdomen">
            <h2>🤚 מישוש בטן</h2>
            <div class="modal-content">
                {abdomen_text}
            </div>
            <button class="close-btn" onclick="closeModal()">סגור</button>
        </div>
        
        <script>
            function showModal(type) {{
                document.getElementById('overlay').classList.add('active');
                document.getElementById('modal-' + type).classList.add('active');
            }}
            
            function closeModal() {{
                document.querySelectorAll('.modal, .overlay').forEach(el => {{
                    el.classList.remove('active');
                }});
            }}
        </script>
    </body>
    </html>
    """
    
    # Load image and embed
    try:
        # For large images, use local path instead of base64
        import os
        
        # Get relative path from current working directory
        rel_path = os.path.relpath(img_path, Path.cwd())
        
        # Read image as base64 (but with compression)
        from PIL import Image
        import io
        
        # Open and compress image
        img = Image.open(img_path)
        # Resize if too large (max 1200px width)
        if img.width > 1200:
            ratio = 1200 / img.width
            new_size = (1200, int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Convert to base64 with compression
        buffer = io.BytesIO()
        img.save(buffer, format='PNG', optimize=True, quality=85)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        # Replace placeholder with actual image data
        html_content = html_content.replace('__IMAGE_DATA__', img_base64)
        
        # Display component
        components.html(html_content, height=900, scrolling=True)
        
    except Exception as e:
        st.error(f"שגיאה בטעינת התמונה: {e}")
        import traceback
        st.code(traceback.format_exc())
