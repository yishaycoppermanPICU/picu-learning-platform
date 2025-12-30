# -*- coding: utf-8 -*-
"""
מערכת תגי הישגים (Badges System)
"""

# הגדרת סוגי תגים
BADGE_TYPES = {
    'excellence': {
        'name': 'מצטיין שבועי',
        'icon': '⭐',
        'color': '#FFD700',
        'description': 'השלמת תוכן שבועי עם ציון מעל 80%'
    },
    'consistent': {
        'name': 'עקביות',
        'icon': '🔥',
        'color': '#FF4500',
        'description': 'השלמת 4 שבועות רצופים'
    },
    'master': {
        'name': 'מאסטר',
        'icon': '👑',
        'color': '#9370DB',
        'description': 'השלמת 10 שבועות מצטברים'
    },
    'perfect': {
        'name': 'מושלם',
        'icon': '💎',
        'color': '#00CED1',
        'description': 'ציון 100% במבחן שבועי'
    },
    'champion': {
        'name': 'אלוף',
        'icon': '🏆',
        'color': '#FF6347',
        'description': 'מקום ראשון במוסד'
    },
    'dedicated': {
        'name': 'מסור',
        'icon': '💪',
        'color': '#32CD32',
        'description': 'השלמת 5 שבועות מצטברים'
    }
}

def get_badge_html(badge_type, size='medium'):
    """
    מחזיר HTML מעוצב של תג
    """
    if badge_type not in BADGE_TYPES:
        return ""
    
    badge = BADGE_TYPES[badge_type]
    
    sizes = {
        'small': {'icon': '1.5rem', 'padding': '0.3rem 0.6rem', 'font': '0.75rem'},
        'medium': {'icon': '2rem', 'padding': '0.5rem 1rem', 'font': '0.9rem'},
        'large': {'icon': '3rem', 'padding': '1rem 1.5rem', 'font': '1.1rem'}
    }
    
    size_config = sizes.get(size, sizes['medium'])
    
    # Special styling for weekly excellence: outlined with subtle glow, star after text
    if badge_type == 'excellence':
        return f"""
        <div style="
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            background: rgba(255,255,255,0.92);
            color: #b38700;
            padding: {size_config['padding']};
            border-radius: 26px;
            margin: 0.3rem;
            border: 2px solid #f5c200;
            box-shadow: 0 0 12px rgba(245, 194, 0, 0.35), 0 6px 12px rgba(0,0,0,0.08);
            text-align: center;
            font-weight: 700;
        ">
            <span style="font-size: {size_config['font']};">{badge['name']}</span>
            <span style="font-size: {size_config['icon']}; color: #e0a800;">{badge['icon']}</span>
        </div>
        """

    return f"""
    <div style="
        display: inline-block;
        background: linear-gradient(135deg, {badge['color']} 0%, {badge['color']}dd 100%);
        color: white;
        padding: {size_config['padding']};
        border-radius: 25px;
        margin: 0.3rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        text-align: center;
        font-weight: 600;
    ">
        <span style="font-size: {size_config['icon']};">{badge['icon']}</span>
        <span style="font-size: {size_config['font']}; margin-right: 0.5rem;">{badge['name']}</span>
    </div>
    """

def get_badge_card_html(badge_type, earned_date=None, score=None):
    """
    מחזיר כרטיס מפורט של תג
    """
    if badge_type not in BADGE_TYPES:
        return ""
    
    badge = BADGE_TYPES[badge_type]
    
    date_str = ""
    if earned_date:
        date_str = f"<p style='color: #6c757d; font-size: 0.85rem; margin: 0.3rem 0;'>התקבל: {earned_date}</p>"
    
    score_str = ""
    if score:
        score_str = f"<p style='color: #28a745; font-weight: 600; margin: 0.3rem 0;'>ציון: {score}%</p>"
    
    return f"""
    <div style="
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-right: 5px solid {badge['color']};
        transition: transform 0.3s ease;
    ">
        <div style="text-align: center;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">{badge['icon']}</div>
            <h3 style="color: {badge['color']}; margin: 0.5rem 0;">{badge['name']}</h3>
            <p style="color: #6c757d; margin: 0.5rem 0;">{badge['description']}</p>
            {date_str}
            {score_str}
        </div>
    </div>
    """

def get_progress_badges_html(completed_weeks, total_badges):
    """
    מחזיר HTML של סטטוס התקדמות לתגים
    """
    milestones = [
        {'weeks': 5, 'badge': 'dedicated', 'reached': completed_weeks >= 5},
        {'weeks': 10, 'badge': 'master', 'reached': completed_weeks >= 10},
        {'weeks': 20, 'badge': 'champion', 'reached': completed_weeks >= 20}
    ]
    
    html = '<div style="margin: 1rem 0; padding: 1rem; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 14px;">'
    html += '<div style="display:flex; flex-wrap: wrap; gap: 0.75rem; align-items: center;">'
    
    for milestone in milestones:
        badge = BADGE_TYPES[milestone['badge']]
        reached = milestone['reached']
        opacity = '1' if reached else '0.35'
        bar_color = badge['color'] if reached else '#cbd5e1'
        html += f"""
        <div style="min-width: 140px; padding: 0.75rem; border: 1px solid #d7dde4; border-radius: 12px; background: white; box-shadow: 0 3px 10px rgba(0,0,0,0.05);">
            <div style="display:flex; align-items:center; justify-content: space-between;">
                <span style="font-size: 1.6rem; opacity:{opacity};">{badge['icon']}</span>
                <span style="font-size: 0.95rem; color: #0f172a; font-weight: 700;">{milestone['weeks']} שבועות</span>
            </div>
            <div style="margin-top: 0.5rem; height: 8px; background: #e5e7eb; border-radius: 999px; overflow: hidden;">
                <div style="width: { '100%' if reached else '20%' }; height: 100%; background: {bar_color}; opacity:{opacity};"></div>
            </div>
            <div style="font-size: 0.78rem; color: #475569; margin-top: 0.35rem;">{ 'הושג' if reached else 'עוד מעט מגיעים' }</div>
        </div>
        """
    
    html += '</div></div>'
    return html

def calculate_user_achievements(user_stats, badges_list):
    """
    מחשב הישגים נוספים שהמשתמש זכאי להם
    """
    achievements = []
    completed_weeks = user_stats.get('completed_weeks', 0)
    
    # תג עקביות
    if completed_weeks >= 4:
        achievements.append('consistent')
    
    # תג מסירות
    if completed_weeks >= 5:
        achievements.append('dedicated')
    
    # תג מאסטר
    if completed_weeks >= 10:
        achievements.append('master')
    
    # בדיקת ציון מושלם
    for badge in badges_list:
        if badge.get('score') == 100 and 'perfect' not in achievements:
            achievements.append('perfect')
            break
    
    return achievements

def get_all_badges_showcase():
    """
    מחזיר תצוגה של כל התגים האפשריים
    """
    html = '<div style="display: flex; flex-wrap: wrap; justify-content: center;">'
    
    for badge_type, badge in BADGE_TYPES.items():
        html += f"""
        <div style="
            background: white;
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            min-width: 150px;
        ">
            <div style="font-size: 2.5rem;">{badge['icon']}</div>
            <h4 style="color: {badge['color']}; margin: 0.5rem 0;">{badge['name']}</h4>
            <p style="color: #6c757d; font-size: 0.8rem; margin: 0;">{badge['description']}</p>
        </div>
        """
    
    html += '</div>'
    return html
