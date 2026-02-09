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
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

    :root {
        --navy: #1f2f3d;
        --slate: #2c4156;
        --teal: #0d8a7b;
        --teal-light: #1ab0a0;
        --orange-accent: #f5a524;
        --bg: #f5f7fb;
    }

    /* תיקון ke / אייקונים שבורים: הסתרת anchor של כותרות והבטחת טעינת פונט אייקונים */
    h1 a[href^="#"], h2 a[href^="#"], h3 a[href^="#"],
    h4 a[href^="#"], h5 a[href^="#"], h6 a[href^="#"],
    h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        pointer-events: none !important;
    }
    
    /* חסימה של קישור GitHub וכפתורים מיותרים */
    header a[href*="github"],
    header a[href*="github"] *,
    header button[kind="header"],
    header button[kind="header"] *,
    header > div > div > a {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        position: absolute !important;
        left: -9999px !important;
        pointer-events: none !important;
    }
    
    /* כפתור פתיחת סיידבר - רק הכפתור האמיתי */
    button[data-testid="collapsedControl"],
    button[kind="header"],
    section[data-testid="stSidebar"] button[kind="header"] {
        background: linear-gradient(135deg, var(--teal) 0%, var(--teal-light) 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        width: 70px !important;
        height: 40px !important;
        box-shadow: 0 4px 15px rgba(13, 138, 123, 0.35) !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        margin: 0.5rem !important;
        pointer-events: all !important;
        cursor: pointer !important;
        overflow: hidden !important;
        font-size: 0 !important;
        color: transparent !important;
        text-indent: -9999px !important;
        line-height: 0 !important;
    }
    
    button[data-testid="collapsedControl"]:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 6px 20px rgba(13, 138, 123, 0.5) !important;
    }
    
    /* הסתרה מוחלטת של כל התוכן המקורי - חזק יותר */
    button[data-testid="collapsedControl"] *,
    button[data-testid="collapsedControl"] span,
    button[data-testid="collapsedControl"] svg,
    button[data-testid="collapsedControl"] [data-icon],
    button[data-testid="collapsedControl"] > div,
    button[data-testid="collapsedControl"] > span,
    button[kind="header"] *,
    button[kind="header"] span,
    button[kind="header"] svg,
    section[data-testid="stSidebar"] button *,
    section[data-testid="stSidebar"] button span,
    section[data-testid="stSidebar"] button svg,
    button[data-testid="collapsedControl"] path,
    button[data-testid="collapsedControl"]::after,
    button[kind="header"]::before,
    section[data-testid="stSidebar"] button[kind="header"]::before {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        font-size: 0 !important;
        width: 0 !important;
        height: 0 !important;
        position: absolute !important;
        left: -9999px !important;
    }
    
    /* אייקון תפריט (חץ Unicode פשוט) כדי למנוע טקסט שבור */
    button[data-testid="collapsedControl"]::before {
        content: "☰" !important;
        text-indent: 0 !important;
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        font-size: 28px !important;
        font-weight: 700 !important;
        color: white !important;
        line-height: 1 !important;
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        z-index: 999 !important;
    }
    
    /* ================= RTL & Basic Layout ================= */
    .stApp {
        direction: rtl;

        background: linear-gradient(135deg, #f8fbff 0%, var(--bg) 100%);
        font-family: 'Heebo', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* ================= Header כהה ================= */
    header[data-testid="stHeader"] {
        background: linear-gradient(135deg, var(--navy) 0%, var(--slate) 100%) !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.12) !important;
    }
    
    header[data-testid="stHeader"] * {
        color: white !important;
    }

    /* Hero title under header */
    .hero-title {
        position: relative;
        margin: 0 auto 1.5rem auto;
        padding: 1.4rem 1.8rem;
        max-width: 920px;
        background: linear-gradient(135deg, rgba(255,255,255,0.82) 0%, rgba(232,240,244,0.92) 100%);
        border-radius: 18px;
        overflow: hidden;
        box-shadow: 0 14px 32px rgba(0,0,0,0.08);
        border: 2px solid rgba(245, 165, 36, 0.35);
        direction: rtl;
        text-align: center;
    }

    .hero-title__bg {
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at 20% 30%, rgba(26, 176, 160, 0.12), transparent 55%),
                    radial-gradient(circle at 80% 10%, rgba(31, 47, 61, 0.12), transparent 50%),
                    radial-gradient(circle at 50% 90%, rgba(245, 165, 36, 0.10), transparent 55%);
        filter: blur(6px);
        pointer-events: none;
    }

    .hero-title__content {
        position: relative;
        z-index: 2;
    }

    .hero-title h1 {
        margin: 0.2rem 0 0 0;
        font-size: 3.4rem !important;
        font-weight: 800 !important;
        color: #1b2735 !important;
        letter-spacing: -0.6px;
    }

    .hero-title p {
        margin: 0.5rem 0 0 0;
        font-size: 1.45rem !important;
        font-weight: 600 !important;
        color: #304050 !important;
    }

    html, body { overflow-x: hidden; }

    /* Header layout + responsive text */
    .app-header-bar {
        display: flex;
        flex-wrap: wrap;
        align-items: flex-start;
        justify-content: flex-start;
        gap: 0.6rem;
        padding: 0;
        direction: rtl;
    }

    .app-header-logo {
        max-width: 600px;
        width: 100vw;
        min-width: 520px;
        margin-top: 0;
        align-self: center;
    }

    .app-header-logo img {
        width: 100%;
        height: auto;
        display: block;
        max-height: 1200px;
        object-fit: contain;
    }

    .app-header-text {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        gap: 4px;
        text-align: right;
        margin-top: -6px;
    }

    /* Header topline/tagline responsive */
    .hero-topline {
        font-size: 2rem;
        line-height: 1.05;
        margin: 0;
        text-align: right;
    }
    .hero-tagline {
        font-size: 1rem;
        line-height: 1.2;
        margin: 0;
        text-align: right;
    }

    @media (max-width: 768px) {
        .app-header-bar {
            flex-direction: column;
            align-items: flex-start;
            gap: 0.25rem;
            padding-top: 0;
            max-width: 100%;
        }
        .app-header-logo {
            order: -1;
            width: 86vw;
            max-width: 340px;
            min-width: 170px;
            margin-top: 8px;
            margin-bottom: 8px;
        }
        .app-header-logo img { max-height: clamp(260px, 32vh, 400px); }
        .app-header-text { margin-top: 0; }
        .hero-topline { font-size: 0.9rem !important; line-height: 1.1; white-space: nowrap; }
        .hero-tagline { font-size: 0.78rem !important; }
    }

    @media (min-width: 769px) {
        .app-header-bar { align-items: center; }
        .app-header-logo { margin-top: 0; }
    }

    @media (max-width: 600px) {
        .hero-title h1 { font-size: 2.5rem !important; }
        .hero-title p { font-size: 1.1rem !important; }
        .hero-topline { font-size: 1.45rem; }
        .hero-tagline { font-size: 0.85rem; }
    }
    
    /* ================= Typography - גדלים מוגדלים ================= */
    body, .stApp,
    h1, h2, h3, h4, h5, h6,
    p, li, label, span, div,
    input, textarea, select,
    .stMarkdown, .stMarkdown * {
        font-family: 'Heebo', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* שמירה על פונט אייקונים */
    .material-icons, .material-symbols-outlined {
        font-family: 'Material Icons', 'Material Symbols Outlined' !important;
        -webkit-font-feature-settings: 'liga';
    }
    
    /* ================= תיקון אייקוני Expander - הסתרת keyboard text בלבד ================= */
    
    /* הגדרות בסיס ל-summary */
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] details > summary {
        position: relative !important;
        display: flex !important;
        align-items: center !important;
        direction: rtl !important;
        padding: 0.75rem 1rem !important;
        cursor: pointer !important;
    }
    
    /* הסתרת האלמנטים המקוריים שיוצרים את keyboard */
    [data-testid="stExpander"] summary svg,
    [data-testid="stExpander"] summary span:not([data-testid="stExpander"] summary > div span),
    [data-testid="stExpander"] summary i {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        font-size: 0 !important;
    }
    
    /* הצגת הכותרת */
    [data-testid="stExpander"] summary > div:first-child,
    [data-testid="stExpander"] details > summary > div:first-child {
        display: block !important;
        visibility: visible !important;
        color: var(--navy) !important;
        font-size: 1.05rem !important;
        line-height: 1.5 !important;
        font-weight: 600 !important;
        max-width: calc(100% - 2rem) !important;
        opacity: 1 !important;
        flex: 1 !important;
    }
    
    /* הוספת חיצים מותאמים אישית */
    [data-testid="stExpander"] summary::after {
        content: "◀" !important;
        position: absolute !important;
        left: 1rem !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        font-size: 1.2rem !important;
        color: var(--teal) !important;
        font-family: 'Heebo', sans-serif !important;
        transition: transform 0.2s ease !important;
        display: inline-block !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    [data-testid="stExpander"][open] summary::after {
        content: "▼" !important;
        transform: translateY(-50%) !important;
    }
    
    h1 {
        font-size: 2.9rem !important;
        font-weight: 800 !important;
        line-height: 1.25 !important;
        margin-bottom: 1.1rem !important;
    }
    
    h2 {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        line-height: 1.35 !important;
        margin-bottom: 0.9rem !important;
    }
    
    h3 {
        font-size: 1.85rem !important;
        font-weight: 700 !important;
        line-height: 1.35 !important;
        margin-bottom: 0.8rem !important;
    }
    
    h4 {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
    }
    
    p, li, span, div {
        font-size: 1.2rem !important;
        line-height: 1.9 !important;
        color: #1f2f3d;
    }

    .stCaption, .stCaption * {
        color: #111827 !important;
        font-size: 0.98rem !important;
        line-height: 1.5 !important;
    }
    
    h1, h2, h3, h4, h5, h6, p, label, span, li, div {
        text-align: right;
        direction: rtl;
    }

    /* שמירה על סדר אמוג'י/חיצים בטקסט RTL */
    .stMarkdown p, .stMarkdown li, .stMarkdown span {
        unicode-bidi: plaintext;
    }
    
    /* טקסט בתוך כפתורים */
    button, button * {
        font-size: 1.15rem !important;
        font-weight: 600 !important;
    }
    
    /* ================= Sidebar ================= */
    section[data-testid="stSidebar"] {
        right: 0;
        left: auto;
        background: linear-gradient(180deg, var(--navy) 0%, var(--teal) 100%);
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
        padding-top: 1.4rem;
        padding-bottom: 4rem;
        max-width: 1400px;
    }

    @media (max-width: 768px) {
        .main .block-container {
            padding-top: 0.6rem;
        }
    }
    
    /* ================= Headers - משופרים ================= */
    .main-header {
        background: linear-gradient(135deg, var(--navy) 0%, var(--teal) 100%);
        padding: 3rem 2.5rem;
        border-radius: 20px;
        margin-bottom: 2.5rem;
        color: white;
        text-align: center;
        box-shadow: 0 15px 40px rgba(31, 47, 61, 0.28);
        position: relative;
        overflow: hidden;
        border-bottom: 4px solid var(--orange-accent);
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
        margin: 0.4rem 0;
        font-size: 3.2rem !important;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.95) !important;
        margin: 0.5rem 0;
        font-size: 1.2rem !important;
    }
    
    /* ================= Cards - עיצוב משופר ================= */
    .category-card {
        background: rgba(255,255,255,0.85);
        padding: 1.5rem 1.75rem;
        border-radius: 14px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        margin-bottom: 1.2rem;
        border: 2px solid rgba(245, 165, 36, 0.6);
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
        position: relative;
        overflow: hidden;
    }
    
    .category-card::after {
        content: "";
        position: absolute;
        inset: -40%;
        background: radial-gradient(circle at 20% 20%, rgba(26, 176, 160, 0.08), transparent 60%),
                    radial-gradient(circle at 80% 0%, rgba(31, 47, 61, 0.06), transparent 55%);
        transform: rotate(-4deg);
        pointer-events: none;
        transition: opacity 0.3s ease;
    }
    
    .category-card:hover {
        transform: translateY(-6px) scale(1.01);
        box-shadow: 0 18px 36px rgba(0,0,0,0.16);
        border-color: var(--teal);
    }
    
    .category-card h3 {
        font-size: 1.8rem !important;
        margin-bottom: 1rem !important;
    }
    
    .topic-card {
        background: rgba(255,255,255,0.9);
        padding: 1.25rem 1.5rem;
        border-radius: 12px;
        border: 1.5px solid rgba(245, 165, 36, 0.7);
        margin-bottom: 0.9rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
        position: relative;
        overflow: hidden;
    }
    
    .topic-card::after {
        content: "";
        position: absolute;
        right: -20%;
        top: -20%;
        width: 60%;
        height: 60%;
        background: radial-gradient(circle, rgba(26, 176, 160, 0.08) 0%, transparent 70%);
        pointer-events: none;
        transition: opacity 0.3s ease;
    }
    
    .topic-card:hover {
        transform: translateY(-4px) translateX(-4px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.14);
        border-color: var(--teal);
    }
    
    .topic-card h4 {
        font-size: 1.4rem !important;
    }
    
    /* ================= Content Sections - משופר ================= */
    .content-section {
        background: rgba(255,255,255,0.94);
        padding: 2.2rem;
        border-radius: 16px;
        margin: 2rem 0;
        box-shadow: 0 6px 18px rgba(0,0,0,0.08);
        border: 2px solid rgba(245, 165, 36, 0.55);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        color: #0f172a !important;
    }

    .content-section * {
        color: #0f172a !important;
        font-size: 1.12rem !important;
        line-height: 1.85 !important;
    }

    .content-section::after {
        content: "";
        position: absolute;
        left: -30%;
        bottom: -40%;
        width: 70%;
        height: 70%;
        background: radial-gradient(circle, rgba(13, 138, 123, 0.1) 0%, transparent 70%);
        pointer-events: none;
    }

    .content-section:hover {
        box-shadow: 0 10px 28px rgba(0,0,0,0.14);
        border-color: var(--teal);
    }
    
    .section-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        cursor: pointer;
        padding: 1.5rem;
        background: linear-gradient(135deg, #f9fbff 0%, #eef2f7 100%);
        border-radius: 12px;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        border-right: 4px solid var(--orange-accent);
    }

    .section-header:hover {
        background: linear-gradient(135deg, #eef2f7 0%, #e3e8ef 100%);
        transform: translateX(-5px);
        box-shadow: 0 3px 10px rgba(31, 47, 61, 0.12);
    }
    
    .section-title {
        font-size: 1.65rem !important;
        font-weight: 700 !important;
        color: #1f2f3d;
        margin: 0;
    }

    .section-preview {
        color: #4d5b6a;
        font-size: 1.15rem !important;
        margin: 0.45rem 0 0 0;
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
        border-top: 5px solid var(--orange-accent);
        transition: all 0.3s ease;
    }
    
    .stat-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    
    .stat-box h3 {
        color: var(--teal);
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
        background: linear-gradient(135deg, var(--teal) 0%, var(--teal-light) 100%);
        color: white !important;
        border: none;
        padding: 0.8rem 2.5rem !important;
        border-radius: 12px;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 5px 15px rgba(13, 138, 123, 0.35);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(13, 138, 123, 0.45);
        background: linear-gradient(135deg, #0b7c6f 0%, #139c8c 100%);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(13, 138, 123, 0.35);
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
        border-color: var(--teal);
        box-shadow: 0 0 0 3px rgba(13, 138, 123, 0.12);
        outline: none;
    }
    }
    
    input:focus, textarea:focus, select:focus {
        border-color: var(--teal);
        box-shadow: 0 0 0 3px rgba(13, 138, 123, 0.12);
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
        background: linear-gradient(135deg, var(--teal) 0%, var(--teal-light) 100%);
        color: white;
    }
    
    /* ================= Expander ================= */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f9fbff 0%, #eef2f7 100%);
        border-radius: 8px;
        border-right: 3px solid var(--orange-accent);
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
    }
    
    /* ================= Dividers ================= */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, var(--orange-accent) 50%, transparent 100%);
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
        background: linear-gradient(135deg, var(--navy) 0%, var(--teal) 100%);
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
        background: linear-gradient(90deg, var(--teal) 0%, var(--teal-light) 100%) !important;
        height: 14px !important;
        border-radius: 7px !important;
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

<script>
// תיקון חזק לאייקונים - רץ מיד ואחרי כל עדכון
(function() {
    function fixIcons() {
        // תיקון כפתור סיידבר
        const sidebarBtn = document.querySelector('button[data-testid="collapsedControl"]');
        if (sidebarBtn) {
            // הסרת כל הטקסט הפנימי
            const textNodes = [];
            sidebarBtn.childNodes.forEach(node => {
                if (node.nodeType === Node.TEXT_NODE) {
                    textNodes.push(node);
                }
            });
            textNodes.forEach(node => node.remove());
            
            // וידוא שהכפתור ריק מטקסט
            if (sidebarBtn.textContent && sidebarBtn.textContent.trim() !== '') {
                sidebarBtn.textContent = '';
            }
        }
        
        // תיקון expanders
        document.querySelectorAll('[data-testid="stExpander"] summary').forEach(summary => {
            // מציאת SVG והסתרתו
            const svg = summary.querySelector('svg');
            if (svg) {
                svg.style.display = 'none';
                svg.style.visibility = 'hidden';
                svg.style.width = '0';
                svg.style.height = '0';
            }
        });
    }
    
    // הרצה מיידית
    fixIcons();
    
    // הרצה אחרי טעינת DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', fixIcons);
    }
    
    // הרצה אחרי שינויים בדף
    const observer = new MutationObserver(fixIcons);
    observer.observe(document.body, { 
        childList: true, 
        subtree: true,
        characterData: true
    });
    
    // הרצה כל 100ms בשנייה הראשונה (לוודא שתופס את ה-RTL shift)
    let counter = 0;
    const interval = setInterval(() => {
        fixIcons();
        counter++;
        if (counter >= 10) clearInterval(interval);
    }, 100);
})();
</script>
"""


def get_collapsible_section_script():
    """JavaScript לטיפול בסקשנים מתקפלים"""
    return """
<script>
// תיקון חזק לאייקונים - רץ מיד ואחרי כל עדכון
(function() {
    function fixIcons() {
        // תיקון כפתור סיידבר
        const sidebarBtn = document.querySelector('button[data-testid="collapsedControl"]');
        if (sidebarBtn) {
            // הסרת כל הטקסט הפנימי
            const textNodes = [];
            sidebarBtn.childNodes.forEach(node => {
                if (node.nodeType === Node.TEXT_NODE) {
                    textNodes.push(node);
                }
            });
            textNodes.forEach(node => node.remove());
            
            // וידוא שהכפתור ריק מטקסט
            if (sidebarBtn.textContent && sidebarBtn.textContent.trim() !== '') {
                sidebarBtn.textContent = '';
            }
        }
        
        // תיקון expanders
        document.querySelectorAll('[data-testid="stExpander"] summary').forEach(summary => {
            // מציאת SVG והסתרתו
            const svg = summary.querySelector('svg');
            if (svg) {
                svg.style.display = 'none';
                svg.style.visibility = 'hidden';
                svg.style.width = '0';
                svg.style.height = '0';
            }
        });
    }
    
    // הרצה מיידית
    fixIcons();
    
    // הרצה אחרי טעינת DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', fixIcons);
    }
    
    // הרצה אחרי שינויים בדף
    const observer = new MutationObserver(fixIcons);
    observer.observe(document.body, { 
        childList: true, 
        subtree: true,
        characterData: true
    });
    
    // הרצה כל 100ms בשנייה הראשונה (לוודא שתופס את ה-RTL shift)
    let counter = 0;
    const interval = setInterval(() => {
        fixIcons();
        counter++;
        if (counter >= 10) clearInterval(interval);
    }, 100);
})();

function toggleSection(sectionId) {
    const content = document.getElementById('content-' + sectionId);
    const icon = document.getElementById('icon-' + sectionId);
    
    if (content.style.display === 'none' || content.style.display === '') {
        content.style.display = 'block';
        icon.innerHTML = '🔽';
    } else {
        content.style.display = 'none';
        icon.innerHTML = '◀';
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

<script>
// תיקון אייקוני חצים אחרי טעינת הדף
(function() {
    function fixIcons() {
        // תיקון כפתור סיידבר - כל הסוגים האפשריים
        const sidebarBtns = document.querySelectorAll(
            'button[data-testid="collapsedControl"], button[kind="header"], section[data-testid="stSidebar"] button'
        );
        sidebarBtns.forEach(btn => {
            if (btn) {
                // הסתרת כל התוכן הפנימי
                const children = btn.querySelectorAll('*');
                children.forEach(child => {
                    child.style.display = 'none';
                    child.style.visibility = 'hidden';
                    child.style.fontSize = '0';
                });
                btn.style.fontSize = '0';
                btn.style.textIndent = '-9999px';
                btn.textContent = '';
            }
        });
        
        // תיקון expanders - הסתרת SVG
        const expanderSvgs = document.querySelectorAll('[data-testid="stExpander"] svg');
        expanderSvgs.forEach(svg => {
            svg.style.display = 'none';
            svg.style.visibility = 'hidden';
            svg.style.opacity = '0';
        });
    }
    
    // הרצה ראשונית
    setTimeout(fixIcons, 100);
    
    // הרצה אחרי שהדף נטען לגמרי
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => setTimeout(fixIcons, 100));
    } else {
        setTimeout(fixIcons, 100);
    }
    
    // הרצה כל פעם שמשהו משתנה (למקרה ש-Streamlit מרנדר מחדש)
    const observer = new MutationObserver(() => setTimeout(fixIcons, 50));
    observer.observe(document.body, { childList: true, subtree: true });
    
    // הרצה נוספת אחרי 1 שניה (אחרי שה-RTL עושה את שלו)
    setTimeout(fixIcons, 1000);
})();
</script>
"""
