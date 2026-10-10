import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>
    /* Import Inter Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #F8F7FC !important;
        color: #1E1F2D !important;
    }

    /* Main container padding */
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1280px !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #ECEAF2 !important;
        box-shadow: 2px 0 12px rgba(30, 31, 45, 0.04) !important;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    /* Universal High Contrast Sidebar Text Fix */
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #1E1F2D !important;
        font-weight: 600 !important;
    }

    /* Sidebar Brand Box */
    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 12px 14px;
        margin-bottom: 20px;
        background: #F4F2FA;
        border-radius: 12px;
        border: 1px solid #E2DEF0;
    }
    .sidebar-brand-icon {
        width: 34px;
        height: 34px;
        border-radius: 8px;
        background: #5C54E5;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        color: #FFFFFF !important;
        font-size: 18px;
    }
    .sidebar-brand-title {
        font-size: 17px;
        font-weight: 800;
        color: #1E1F2D !important;
        letter-spacing: -0.3px;
    }
    .sidebar-brand-subtitle {
        font-size: 11px;
        font-weight: 500;
        color: #4B4C63 !important;
    }

    /* Radio button custom styling for sidebar menu */
    div[data-testid="stSidebar"] div[role="radiogroup"] label {
        background-color: #F8F7FC !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        margin-bottom: 6px !important;
        border: 1px solid #ECEAF2 !important;
        transition: all 0.15s ease-in-out !important;
        cursor: pointer !important;
    }
    div[data-testid="stSidebar"] div[role="radiogroup"] label p,
    div[data-testid="stSidebar"] div[role="radiogroup"] label span,
    div[data-testid="stSidebar"] div[role="radiogroup"] label div {
        color: #2D2E40 !important;
        font-weight: 700 !important;
        font-size: 14px !important;
    }
    div[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background-color: #ECE8FC !important;
        border-color: #DCD6F7 !important;
    }
    
    /* Selected Active Navigation Pill */
    div[data-testid="stSidebar"] div[role="radiogroup"] label[aria-checked="true"],
    div[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
        background-color: #5C54E5 !important;
        border-color: #5C54E5 !important;
        box-shadow: 0 4px 10px rgba(92, 84, 229, 0.25) !important;
    }
    div[data-testid="stSidebar"] div[role="radiogroup"] label[aria-checked="true"] p,
    div[data-testid="stSidebar"] div[role="radiogroup"] label[aria-checked="true"] span,
    div[data-testid="stSidebar"] div[role="radiogroup"] label[aria-checked="true"] div,
    div[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p,
    div[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) span,
    div[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) div {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }

    /* Card Containers */
    .eduguard-card {
        background-color: #FFFFFF;
        border: 1px solid #ECEAF2;
        border-radius: 12px;
        padding: 20px 22px;
        margin-bottom: 18px;
        box-shadow: 0 2px 8px rgba(30, 31, 45, 0.03);
    }

    /* Metric Card Component */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #ECEAF2;
        border-radius: 12px;
        padding: 18px 20px;
        display: flex;
        align-items: center;
        gap: 16px;
        box-shadow: 0 2px 8px rgba(30, 31, 45, 0.03);
    }
    .metric-icon-box {
        width: 48px;
        height: 48px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        flex-shrink: 0;
    }
    .metric-icon-lavender { background: #E8E4FA; color: #34354A; }
    .metric-icon-blue { background: #DCEBFA; color: #1E40AF; }
    .metric-icon-green { background: #DDF3E4; color: #166534; }
    .metric-icon-peach { background: #FCE6DA; color: #991B1B; }

    .metric-value {
        font-size: 26px;
        font-weight: 800;
        color: #1E1F2D !important;
        line-height: 1.1;
    }
    .metric-label {
        font-size: 13px;
        font-weight: 600;
        color: #4B4C63 !important;
        margin-top: 3px;
    }
    .metric-trend {
        font-size: 11px;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 3px;
        margin-top: 4px;
    }
    .trend-up { color: #166534; background: #DDF3E4; padding: 2px 8px; border-radius: 4px; }
    .trend-warn { color: #991B1B; background: #FCE6DA; padding: 2px 8px; border-radius: 4px; }

    /* Top Navigation Bar Header */
    .top-header {
        background: #FFFFFF;
        border: 1px solid #ECEAF2;
        border-radius: 12px;
        padding: 14px 22px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 8px rgba(30, 31, 45, 0.03);
    }
    .top-header-title {
        font-size: 20px;
        font-weight: 800;
        color: #1E1F2D !important;
    }
    .top-header-subtitle {
        font-size: 13px;
        font-weight: 500;
        color: #4B4C63 !important;
    }
    .top-header-right {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .user-pill {
        background: #F4F2FA;
        border: 1px solid #E2DEF0;
        border-radius: 20px;
        padding: 6px 16px;
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 13px;
        font-weight: 700;
        color: #1E1F2D !important;
    }
    .notif-badge {
        width: 34px;
        height: 34px;
        border-radius: 50%;
        background: #DCEBFA;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 15px;
        color: #1E1F2D;
        position: relative;
    }
    .notif-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #EF4444;
        position: absolute;
        top: 4px;
        right: 4px;
    }

    /* Status Pills */
    .badge-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 14px;
        font-size: 12px;
        font-weight: 700;
        text-align: center;
    }
    .badge-low {
        background-color: #DDF3E4;
        color: #166534;
    }
    .badge-medium {
        background-color: #FEF08A;
        color: #854D0E;
    }
    .badge-high {
        background-color: #FCE6DA;
        color: #991B1B;
    }

    /* Streamlit Button Overrides */
    div.stButton > button {
        background-color: #5C54E5 !important;
        color: #FFFFFF !important;
        border: 1px solid #5C54E5 !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        padding: 8px 18px !important;
        transition: all 0.15s ease !important;
    }
    div.stButton > button:hover {
        background-color: #4B43D1 !important;
        border-color: #4B43D1 !important;
        box-shadow: 0 4px 10px rgba(92, 84, 229, 0.3) !important;
    }

    /* Form Inputs Overrides */
    div.stTextInput > div > div > input,
    div.stSelectbox > div > div,
    div.stNumberInput > div > div > input {
        border-radius: 8px !important;
        border: 1px solid #CBD5E1 !important;
        background-color: #FFFFFF !important;
        color: #1E1F2D !important;
        font-weight: 500 !important;
    }
    div.stTextInput > div > div > input:focus,
    div.stSelectbox > div > div:focus {
        border-color: #5C54E5 !important;
        box-shadow: 0 0 0 2px rgba(92, 84, 229, 0.3) !important;
    }

    /* Streamlit Metric Overrides for Crisp Visibility */
    div[data-testid="stMetricValue"] div,
    div[data-testid="stMetricValue"] span,
    div[data-testid="stMetricValue"] {
        color: #1E1F2D !important;
        font-weight: 800 !important;
        font-size: 24px !important;
    }
    div[data-testid="stMetricLabel"] label,
    div[data-testid="stMetricLabel"] p,
    div[data-testid="stMetricLabel"] span,
    div[data-testid="stMetricLabel"] {
        color: #4B4C63 !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }

    /* Section Heading Styling */
    .section-title {
        font-size: 17px;
        font-weight: 800;
        color: #1E1F2D !important;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-subtitle {
        font-size: 13px;
        font-weight: 500;
        color: #4B4C63 !important;
        margin-bottom: 16px;
    }

    /* Callout / Warning box */
    .eduguard-disclaimer {
        background-color: #FEE2E2;
        border-left: 4px solid #EF4444;
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 13px;
        font-weight: 500;
        color: #7F1D1D;
        margin-bottom: 16px;
    }

    .eduguard-info {
        background-color: #DBEAFE;
        border-left: 4px solid #3B82F6;
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 13px;
        font-weight: 500;
        color: #1E3A8A;
        margin-bottom: 16px;
    }

    /* Hide Streamlit header & footer elements for clean SaaS look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {background: transparent !important;}
    </style>
    """, unsafe_allow_html=True)

def apply_plotly_theme(fig, height=280):
    fig.update_layout(
        font=dict(color="#1E1F2D", family="Inter, sans-serif", size=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            tickfont=dict(color="#1E1F2D", size=11),
            title_font=dict(color="#1E1F2D", size=12, family="Inter"),
            showgrid=True,
            gridcolor="#ECEAF2"
        ),
        yaxis=dict(
            tickfont=dict(color="#1E1F2D", size=11),
            title_font=dict(color="#1E1F2D", size=12, family="Inter"),
            showgrid=True,
            gridcolor="#ECEAF2"
        ),
        legend=dict(
            font=dict(color="#1E1F2D", size=11)
        )
    )
    if height:
        fig.update_layout(height=height)
    return fig

def render_top_header(title="Student Success Overview", subtitle="Understand student risk early and take action that makes a difference."):
    st.markdown(f"""
    <div class="top-header">
        <div>
            <div class="top-header-title">{title}</div>
            <div class="top-header-subtitle">{subtitle}</div>
        </div>
        <div class="top-header-right">
            <div class="notif-badge" title="Notifications">
                🔔
                <div class="notif-dot"></div>
            </div>
            <div class="user-pill">
                <span>👤 Counsellor Portal</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_metric_card(icon_emoji, label, value, trend_text, trend_type="up", color_theme="lavender"):
    trend_class = "trend-up" if trend_type == "up" else "trend-warn"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon-box metric-icon-{color_theme}">
            {icon_emoji}
        </div>
        <div>
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
            <div class="metric-trend"><span class="{trend_class}">{trend_text}</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_risk_pill(risk_level):
    level = str(risk_level).lower()
    if level == "low":
        return f'<span class="badge-pill badge-low">🟢 Low Risk</span>'
    elif level == "medium":
        return f'<span class="badge-pill badge-medium">🟡 Medium Risk</span>'
    else:
        return f'<span class="badge-pill badge-high">🔴 High Risk</span>'
