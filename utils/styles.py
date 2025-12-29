# -*- coding: utf-8 -*-
"""
קובץ עיצוב מרכזי לכל האפליקציה
"""

def get_common_styles():
    """החזרת CSS משותף לכל הדפים"""
    return """
<style>
    /* ================= הסתרת קישור GitHub וכלים מפריעים ================= */
    /* הסתרה מוחלטת של קישורי GitHub ב-Streamlit Cloud */
    a[href*="github.com"],
    a[href*="github"],
    [data-testid="stToolbar"] a,
    header a,
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    .stActionButton {
        display: none !important;
        visibility: hidden !important;
        pointer-events: none !important;
        opacity: 0 !important;
        position: absolute !important;
        top: -9999px !important;
        z-index: -1 !important;
    }
    
    /* ================= RTL & Basic Layout ================= */
    .stApp {
        direction: rtl;
        background: linear-gradient(135deg, #f5f7fa 0%, #e8eef5 100%);
    }
    
    h1, h2, h3, h4, h5, h6, p, label, span, li, div {
        text-align: right;
        direction: rtl;
    }
    
    /* ================= Sidebar ================= */
    section[data-testid="stSidebar"] {
        right: 0;
        left: auto;
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    section[data-testid="stSidebar"] > div {
        right: 0;
        left: auto;
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: white !important;
    }
    
    /* תצוגה רגילה בדסקטופ */
    @media (min-width: 769px) {
        section[data-testid="stSidebar"] {
            display: block !important;
            position: relative !important;
            width: auto !important;
        }
        
        section[data-testid="stSidebar"][aria-expanded="false"] {
            display: block !important;
        }
    }
    
    /* תיקון תצוגת סיידבר במובייל */
    @media (max-width: 768px) {
        /* הסתרת הסיידבר כשהוא מכווץ */
        section[data-testid="stSidebar"][aria-expanded="false"] {
            display: none !important;
        }
        
        /* כפתור ההמבורגר תמיד נראה - גירסה משופרת */
        button[kind="header"],
        button[data-testid="collapsedControl"] {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            position: fixed !important;
            top: 4.5rem !important;
            right: 1rem !important;
            z-index: 999999 !important;
            background: white !important;
            border: 2px solid #667eea !important;
            border-radius: 8px !important;
            padding: 0 !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.25) !important;
            width: 44px !important;
            height: 44px !important;
            min-width: 44px !important;
            min-height: 44px !important;
            pointer-events: all !important;
            cursor: pointer !important;
        }
        
        /* הסרת כל האייקונים הקיימים */
        button[kind="header"] svg,
        button[data-testid="collapsedControl"] svg,
        button[kind="header"] img,
        button[data-testid="collapsedControl"] img {
            display: none !important;
            opacity: 0 !important;
            visibility: hidden !important;
        }
        
        /* יצירת אייקון המבורגר - גירסה משופרת */
        button[kind="header"]::after,
        button[data-testid="collapsedControl"]::after {
            content: "" !important;
            display: block !important;
            position: absolute !important;
            top: 50% !important;
            left: 50% !important;
            transform: translate(-50%, -50%) !important;
            width: 24px !important;
            height: 3px !important;
            background: #667eea !important;
            border-radius: 3px !important;
            box-shadow: 
                0 -8px 0 0 #667eea, 
                0 8px 0 0 #667eea !important;
        }
        
        /* הסיידבר כשהוא פתוח */
        section[data-testid="stSidebar"][aria-expanded="true"] {
            position: fixed !important;
            top: 0 !important;
            right: 0 !important;
            height: 100vh !important;
            width: 80% !important;
            max-width: 300px !important;
            z-index: 999998 !important;
            box-shadow: -4px 0 20px rgba(0,0,0,0.3) !important;
        }
        
        /* רקע כהה מאחורי הסיידבר */
        section[data-testid="stSidebar"][aria-expanded="true"]::before {
            content: "";
            position: fixed;
            top: 0;
            right: 0;
            bottom: 0;
            left: 0;
            background: rgba(0,0,0,0.5);
            z-index: -1;
        }
        
        /* התאמת התוכן הראשי */
        .main .block-container {
            padding-right: 1rem;
            padding-left: 1rem;
        }
    }
    
    /* ================= Main Container ================= */
    .main .block-container {
        padding-right: 3rem;
        padding-left: 1rem;
        padding-bottom: 4rem; /* מרווח לזכויות יוצרים */
        max-width: 1200px;
    }
    
    /* ================= Headers ================= */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1, .main-header p {
        color: white !important;
        margin: 0.5rem 0;
    }
    
    /* ================= Cards ================= */
    .category-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        border-right: 5px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .category-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.2);
    }
    
    .topic-card {
        background: white;
        padding: 1.2rem;
        border-radius: 10px;
        border-right: 4px solid #667eea;
        margin-bottom: 0.8rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .topic-card:hover {
        transform: translateX(-5px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* ================= Content Sections ================= */
    .content-section {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        border-right: 4px solid #667eea;
    }
    
    .section-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        cursor: pointer;
        padding: 1rem;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 8px;
        margin-bottom: 0.5rem;
        transition: all 0.3s ease;
        border-right: 3px solid #667eea;
    }
    
    .section-header:hover {
        background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
        transform: translateX(-3px);
    }
    
    .section-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 0;
    }
    
    .section-preview {
        color: #6c757d;
        font-size: 0.95rem;
        margin: 0.5rem 0 0 0;
        line-height: 1.6;
    }
    
    /* ================= Alert Boxes ================= */
    .alert-box {
        padding: 1.2rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-right: 5px solid;
    }
    
    .alert-warning {
        background: #fff3cd;
        border-color: #ffc107;
        color: #856404;
    }
    
    .alert-info {
        background: #d1ecf1;
        border-color: #17a2b8;
        color: #0c5460;
    }
    
    .alert-success {
        background: #d4edda;
        border-color: #28a745;
        color: #155724;
    }
    
    .alert-danger {
        background: #f8d7da;
        border-color: #dc3545;
        color: #721c24;
    }
    
    /* ================= Stat Boxes ================= */
    .stat-box {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        text-align: center;
        border-top: 4px solid #667eea;
    }
    
    .stat-box h3 {
        color: #667eea;
        font-size: 2.5rem;
        margin: 0.5rem 0;
    }
    
    .stat-box p {
        color: #6c757d;
        margin: 0;
    }
    
    /* ================= Buttons ================= */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.6rem 2rem;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* ================= Inputs ================= */
    input, textarea, select {
        direction: rtl;
        text-align: right;
        border-radius: 8px;
        border: 2px solid #e9ecef;
        padding: 0.5rem;
    }
    
    input:focus, textarea:focus, select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* ================= Tabs ================= */
    .stTabs [data-baseweb="tab-list"] {
        flex-direction: row-reverse;
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        background: #f8f9fa;
        padding: 0.8rem 1.5rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* ================= Expander ================= */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 8px;
        border-right: 3px solid #667eea;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
    }
    
    /* ================= Dividers ================= */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #667eea 50%, transparent 100%);
        margin: 2rem 0;
    }
    
    /* ================= Lists ================= */
    ul, ol {
        padding-right: 2rem;
        line-height: 1.8;
    }
    
    li {
        margin: 0.5rem 0;
    }
    
    /* ================= Code Blocks ================= */
    code {
        background: #f8f9fa;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        color: #e83e8c;
        font-size: 0.9em;
    }
    
    pre {
        background: #282c34;
        color: #abb2bf;
        padding: 1rem;
        border-radius: 8px;
        overflow-x: auto;
        direction: ltr;
    }
    
    /* ================= Responsive ================= */
    @media (max-width: 768px) {
        .main .block-container {
            padding-right: 1rem;
            padding-left: 1rem;
        }
        
        .main-header {
            padding: 1.5rem;
        }
    }
</style>
"""


def get_collapsible_section_script():
    """JavaScript לטיפול בסקשנים מתקפלים"""
    return """
<script>
function toggleSection(sectionId) {
    const content = document.getElementById('content-' + sectionId);
    const icon = document.getElementById('icon-' + sectionId);
    
    if (content.style.display === 'none' || content.style.display === '') {
        content.style.display = 'block';
        icon.innerHTML = '▼';
    } else {
        content.style.display = 'none';
        icon.innerHTML = '◄';
    }
}

// סגירת סיידבר במובייל כשלוחצים מחוץ לו
document.addEventListener('DOMContentLoaded', function() {
    if (window.innerWidth <= 768) {
        document.addEventListener('click', function(event) {
            const sidebar = document.querySelector('section[data-testid="stSidebar"]');
            const sidebarButton = document.querySelector('button[kind="header"]');
            
            if (sidebar && sidebar.getAttribute('aria-expanded') === 'true') {
                if (!sidebar.contains(event.target) && !sidebarButton.contains(event.target)) {
                    // לחיצה על כפתור ההמבורגר לסגירה
                    if (sidebarButton) {
                        sidebarButton.click();
                    }
                }
            }
        });
    }
});
</script>

<!-- זכויות יוצרים -->
<div style="
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(102, 126, 234, 0.95);
    color: white;
    text-align: center;
    padding: 0.5rem;
    font-size: 0.9rem;
    z-index: 1000;
    box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
    direction: rtl;
">
    © כל הזכויות שמורות לישי קופרמן
</div>
"""
