# -*- coding: utf-8 -*-
"""
קובץ עיצוב מרכזי לכל האפליקציה
"""

def get_common_styles():
    """החזרת CSS משותף לכל הדפים"""
    return """
<style>
    /* ================= Import Fonts ================= */
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;600;700&display=swap');
    
    /* חסימה של קישור GitHub בלבד */
    header a[href*="github"],
    header a[href*="github"] * {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        position: absolute !important;
        left: -9999px !important;
        pointer-events: none !important;
    }
    
    /* הסתרת תכונות data-key וטקסט key שעשוי להופיע */
    [data-key]::after,
    [data-testid*="key"]::after,
    button::before {
        content: none !important;
        display: none !important;
    }
    
    /* הסתרת כל טקסט שיכול להיות key */
    *[data-key],
    *[data-testid*="key"] {
        position: relative;
    }
    
    /* מניעת תצוגה של מאפיינים של Streamlit */
    [class*="st-emotion-cache"]::before,
    [class*="st-emotion-cache"]::after {
        content: none !important;
    }
    
    /* מאפשר לכפתור הסיידבר המקורי לעבוד */
    button[kind="header"],
    button[data-testid="collapsedControl"],
    button[kind="header"] *,
    button[data-testid="collapsedControl"] * {
        pointer-events: all !important;
        cursor: pointer !important;
    }
    
    /* הסתרת טקסט keyboard_double_arrow שמופיע בכפתור */
    button[data-testid="collapsedControl"] *[data-icon],
    button[data-testid="collapsedControl"] span,
    button[kind="header"] span {
        font-size: 0 !important;
        display: none !important;
    }
    
    /* עיצוב כפתור הסיידבר - בולט ויפה */
    button[data-testid="collapsedControl"],
    button[kind="header"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        width: 48px !important;
        height: 48px !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        margin: 0.5rem !important;
    }
    
    button[data-testid="collapsedControl"]:hover,
    button[kind="header"]:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* אייקון מעוצב בתוך הכפתור */
    button[data-testid="collapsedControl"]::before,
    button[kind="header"]::before {
        content: "" !important;
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        width: 24px !important;
        height: 24px !important;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white'%3E%3Cpath d='M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z'/%3E%3C/svg%3E") !important;
        background-size: contain !important;
        background-repeat: no-repeat !important;
        background-position: center !important;
        display: block !important;
    }
    
    /* ================= RTL & Basic Layout ================= */
    .stApp {
        direction: rtl;
        background: linear-gradient(135deg, #f5f7fa 0%, #e8eef5 100%);
        font-family: 'Heebo', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* ================= Typography - גדלים מוגדלים ================= */
    * {
        font-family: 'Heebo', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    h1 {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        line-height: 1.3 !important;
        margin-bottom: 1rem !important;
    }
    
    h2 {
        font-size: 2rem !important;
        font-weight: 600 !important;
        line-height: 1.4 !important;
        margin-bottom: 0.8rem !important;
    }
    
    h3 {
        font-size: 1.6rem !important;
        font-weight: 600 !important;
        line-height: 1.4 !important;
        margin-bottom: 0.7rem !important;
    }
    
    h4 {
        font-size: 1.3rem !important;
        font-weight: 500 !important;
    }
    
    p, li, span, div {
        font-size: 1.1rem !important;
        line-height: 1.8 !important;
        color: #2c3e50;
    }
    
    h1, h2, h3, h4, h5, h6, p, label, span, li, div {
        text-align: right;
        direction: rtl;
    }
    
    /* טקסט בתוך כפתורים */
    button, button * {
        font-size: 1.05rem !important;
        font-weight: 500 !important;
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
    
    /* כל הטקסטים בסיידבר יהיו לבנים */
    section[data-testid="stSidebar"] *,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] h5,
    section[data-testid="stSidebar"] h6,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] a,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stMarkdown * {
        color: white !important;
    }
    
    /* כפתורים בסיידבר */
    section[data-testid="stSidebar"] button {
        color: white !important;
        border-color: white !important;
    }
    
    /* שדות קלט בסיידבר */
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] textarea,
    section[data-testid="stSidebar"] select {
        color: #333 !important;
        background: white !important;
    }
    
    /* הסתרת תוכן הסיידבר כשהוא מכווץ */
    section[data-testid="stSidebar"][aria-expanded="false"] .stMarkdown,
    section[data-testid="stSidebar"][aria-expanded="false"] button,
    section[data-testid="stSidebar"][aria-expanded="false"] form,
    section[data-testid="stSidebar"][aria-expanded="false"] input,
    section[data-testid="stSidebar"][aria-expanded="false"] > div > div:not([data-testid="collapsedControl"]) {
        display: none !important;
    }
    
    /* הסיידבר כשהוא מכווץ - רק אייקון */
    section[data-testid="stSidebar"][aria-expanded="false"] {
        min-width: 0 !important;
        width: auto !important;
        overflow: hidden !important;
    }
    
    /* תצוגה רגילה בדסקטופ */
    @media (min-width: 769px) {
        section[data-testid="stSidebar"] {
            display: block !important;
            position: relative !important;
            width: auto !important;
        }
        
        /* גם בדסקטופ - הסתרת תוכן כשסגור */
        section[data-testid="stSidebar"][aria-expanded="false"] .stMarkdown,
        section[data-testid="stSidebar"][aria-expanded="false"] button:not([data-testid="collapsedControl"]),
        section[data-testid="stSidebar"][aria-expanded="false"] form {
            display: none !important;
        }
    }
    
    /* תיקון תצוגת סיידבר במובייל */
    @media (max-width: 768px) {
        /* הסתרת הסיידבר כשהוא מכווץ */
        section[data-testid="stSidebar"][aria-expanded="false"] {
            display: none !important;
        }
        
        /* כפתור הסיידבר המקורי עובד רגיל */
        
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
        padding-top: 2rem;
        padding-bottom: 4rem;
        max-width: 1400px;
    }
    
    /* ================= Headers - משופרים ================= */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2.5rem;
        border-radius: 20px;
        margin-bottom: 2.5rem;
        color: white;
        text-align: center;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.35);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: "";
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        pointer-events: none;
    }
    
    .main-header h1 {
        color: white !important;
        margin: 0.5rem 0;
        font-size: 3rem !important;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.95) !important;
        margin: 0.5rem 0;
        font-size: 1.2rem !important;
    }
    
    /* ================= Cards - עיצוב משופר ================= */
    .category-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
        border-right: 6px solid #667eea;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    
    .category-card:hover {
        transform: translateY(-5px) translateX(-3px);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.25);
        border-right-color: #764ba2;
    }
    
    .category-card h3 {
        font-size: 1.8rem !important;
        margin-bottom: 1rem !important;
    }
    
    .topic-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-right: 5px solid #667eea;
        margin-bottom: 1rem;
        box-shadow: 0 3px 12px rgba(0,0,0,0.06);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .topic-card:hover {
        transform: translateX(-8px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.12);
        border-right-color: #764ba2;
    }
    
    .topic-card h4 {
        font-size: 1.4rem !important;
    }
    
    /* ================= Content Sections - משופר ================= */
    .content-section {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        margin: 2rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-right: 5px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .content-section:hover {
        box-shadow: 0 6px 25px rgba(0,0,0,0.12);
    }
    
    .section-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        cursor: pointer;
        padding: 1.5rem;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        border-right: 4px solid #667eea;
    }
    
    .section-header:hover {
        background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
        transform: translateX(-5px);
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    }
    
    .section-title {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: #2c3e50;
        margin: 0;
    }
    
    .section-preview {
        color: #6c757d;
        font-size: 1.05rem !important;
        margin: 0.5rem 0 0 0;
        line-height: 1.8 !important;
    }
    
    /* ================= Alert Boxes - משופר ================= */
    .alert-box {
        padding: 1.5rem 1.8rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border-right: 6px solid;
        font-size: 1.1rem !important;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #fff8e1 0%, #fff3cd 100%);
        border-color: #ffc107;
        color: #856404;
    }
    
    .alert-info {
        background: linear-gradient(135deg, #e3f2fd 0%, #d1ecf1 100%);
        border-color: #17a2b8;
        color: #0c5460;
    }
    
    .alert-success {
        background: linear-gradient(135deg, #e8f5e9 0%, #d4edda 100%);
        border-color: #28a745;
        color: #155724;
    }
    
    .alert-danger {
        background: linear-gradient(135deg, #ffebee 0%, #f8d7da 100%);
        border-color: #dc3545;
        color: #721c24;
    }
    
    /* ================= Stat Boxes - משופר ================= */
    .stat-box {
        background: white;
        padding: 2rem 1.8rem;
        border-radius: 16px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        text-align: center;
        border-top: 5px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .stat-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    
    .stat-box h3 {
        color: #667eea;
        font-size: 3rem !important;
        font-weight: 700 !important;
        margin: 0.5rem 0;
    }
    
    .stat-box p {
        color: #6c757d;
        margin: 0;
        font-size: 1.15rem !important;
    }
    
    /* ================= Buttons - משופר ================= */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: none;
        padding: 0.8rem 2.5rem !important;
        border-radius: 12px;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.35);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.45);
        background: linear-gradient(135deg, #5568d3 0%, #653a8b 100%);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.35);
    }
    
    /* ================= Inputs - משופר ================= */
    input, textarea, select {
        direction: rtl;
        text-align: right;
        border-radius: 10px;
        border: 2px solid #e9ecef;
        padding: 0.75rem 1rem !important;
        font-size: 1.05rem !important;
        transition: all 0.3s ease;
    }
    
    input:focus, textarea:focus, select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        outline: none;
    }
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
        padding: 1.5rem;
        border-radius: 12px;
        overflow-x: auto;
        direction: ltr;
        font-size: 1rem !important;
        line-height: 1.6 !important;
    }
    
    /* ================= Tables - עיצוב משופר ================= */
    table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin: 1.5rem 0;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    
    thead {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    th {
        color: white !important;
        font-weight: 600 !important;
        font-size: 1.15rem !important;
        padding: 1.2rem 1rem !important;
        text-align: right !important;
    }
    
    td {
        padding: 1rem !important;
        font-size: 1.05rem !important;
        border-bottom: 1px solid #e9ecef;
        text-align: right !important;
    }
    
    tbody tr {
        background: white;
        transition: all 0.3s ease;
    }
    
    tbody tr:hover {
        background: #f8f9fa;
        transform: scale(1.01);
    }
    
    tbody tr:last-child td {
        border-bottom: none;
    }
    
    /* ================= Streamlit Components - משופר ================= */
    .stMarkdown {
        font-size: 1.1rem !important;
    }
    
    .stSelectbox label, .stMultiSelect label, .stTextInput label {
        font-size: 1.15rem !important;
        font-weight: 500 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stRadio label {
        font-size: 1.15rem !important;
        font-weight: 500 !important;
    }
    
    .stRadio > div {
        gap: 0.8rem !important;
    }
    
    /* ================= ניגודיות צבעים - טקסט על רקע ================= */
    /* טקסט לבן על רקעים כהים ומעברי צבע */
    [style*="background: linear-gradient"] h1,
    [style*="background: linear-gradient"] h2,
    [style*="background: linear-gradient"] h3,
    [style*="background: linear-gradient"] h4,
    [style*="background: linear-gradient"] p,
    [style*="background: linear-gradient"] span,
    [style*="background: linear-gradient"] div,
    [style*="background: linear-gradient"] label {
        color: white !important;
    }
    
    /* טקסט כהה על רקעים בהירים */
    [style*="background: white"] h1,
    [style*="background: white"] h2,
    [style*="background: white"] h3,
    [style*="background: white"] h4,
    [style*="background: white"] p,
    [style*="background: white"] span,
    [style*="background: white"] div {
        color: #2c3e50 !important;
    }
    
    [style*="background: #f"] h1,
    [style*="background: #f"] h2,
    [style*="background: #f"] h3,
    [style*="background: #f"] h4,
    [style*="background: #f"] p,
    [style*="background: #f"] span,
    [style*="background: #f"] div {
        color: #2c3e50 !important;
    }
    
    /* כפתורים - טקסט לבן תמיד */
    button, button * {
        color: white !important;
    }
    
    /* הודעות success/info/warning - טקסט כהה */
    .stSuccess, .stInfo, .stWarning {
        color: #2c3e50 !important;
    }
    
    .stSuccess *, .stInfo *, .stWarning * {
        color: #2c3e50 !important;
    }
    
    /* הודעות error - טקסט כהה */
    .stError {
        color: #721c24 !important;
    }
    
    .stError * {
        color: #721c24 !important;
    }
    
    .stRadio > div > label {
        font-size: 1.05rem !important;
        padding: 0.6rem 1rem !important;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stRadio > div > label:hover {
        background: #f8f9fa;
    }
    
    /* הודעות מערכת */
    .stAlert {
        border-radius: 12px !important;
        padding: 1.5rem !important;
        font-size: 1.1rem !important;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #e8f5e9 0%, #d4edda 100%) !important;
        border-right: 5px solid #28a745 !important;
    }
    
    .stError {
        background: linear-gradient(135deg, #ffebee 0%, #f8d7da 100%) !important;
        border-right: 5px solid #dc3545 !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fff8e1 0%, #fff3cd 100%) !important;
        border-right: 5px solid #ffc107 !important;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #e3f2fd 0%, #d1ecf1 100%) !important;
        border-right: 5px solid #17a2b8 !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1.15rem !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        height: 12px !important;
        border-radius: 6px !important;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0 !important;
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent 0%, #e9ecef 50%, transparent 100%) !important;
    }
    
    /* ================= Responsive ================= */
    @media (max-width: 768px) {
        h1 {
            font-size: 2rem !important;
        }
        
        h2 {
            font-size: 1.6rem !important;
        }
        
        h3 {
            font-size: 1.3rem !important;
        }
        
        p, li, span, div {
            font-size: 1rem !important;
        }
        
        .main .block-container {
            padding-right: 1rem;
            padding-left: 1rem;
        }
        
        .main-header {
            padding: 2rem 1.5rem;
        }
        
        .main-header h1 {
            font-size: 2rem !important;
        }
        
        .category-card, .topic-card, .content-section {
            padding: 1.5rem;
        }
        
        .stButton > button {
            padding: 0.7rem 1.5rem !important;
            font-size: 1rem !important;
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
