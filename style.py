import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>
    /* Import Inter Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #F8F7FC !important;
        color: #34354A !important;
    }

    /* Main container padding */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1250px !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #ECEAF2 !important;
        box-shadow: 2px 0 10px rgba(52, 53, 74, 0.02) !important;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    /* Sidebar Brand Box */
    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 12px 14px;
        margin-bottom: 20px;
        background: #F8F7FC;
        border-radius: 12px;
        border: 1px solid #ECEAF2;
    }
    .sidebar-brand-icon {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        background: #DCD6F7;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        color: #34354A;
        font-size: 16px;
    }
    .sidebar-brand-title {
        font-size: 16px;
        font-weight: 700;
        color: #34354A;
        letter-spacing: -0.3px;
    }
    .sidebar-brand-subtitle {
        font-size: 11px;
        color: #77798B;
    }

    /* Radio button custom styling for sidebar menu */
    div[data-testid="stSidebar"] div[role="radiogroup"] > label {
        background-color: transparent !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        margin-bottom: 4px !important;
        border: 1px solid transparent !important;
        transition: all 0.15s ease-in-out !important;
    }
    div[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
        background-color: #F8F7FC !important;
        border-color: #ECEAF2 !important;
    }
    div[data-testid="stSidebar"] div[role="radiogroup"] label[aria-checked="true"] {
        background-color: #DCD6F7 !important;
        color: #34354A !important;
        font-weight: 600 !important;
        border-color: #DCD6F7 !important;
    }

    /* Card Containers */
    .eduguard-card {
        background-color: #FFFFFF;
        border: 1px solid #ECEAF2;
        border-radius: 12px;
        padding: 18px 20px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(52, 53, 74, 0.03);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .eduguard-card:hover {
        box-shadow: 0 4px 12px rgba(52, 53, 74, 0.06);
    }

    /* Metric Card Component */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #ECEAF2;
        border-radius: 12px;
        padding: 16px 18px;
        display: flex;
        align-items: center;
        gap: 14px;
        box-shadow: 0 2px 6px rgba(52, 53, 74, 0.03);
    }
    .metric-icon-box {
        width: 44px;
        height: 44px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        flex-shrink: 0;
    }
    .metric-icon-lavender { background: #DCD6F7; color: #34354A; }
    .metric-icon-blue { background: #DCEBFA; color: #2B5797; }
    .metric-icon-green { background: #DDF3E4; color: #1E5631; }
    .metric-icon-peach { background: #FCE6DA; color: #8B263E; }

    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #34354A;
        line-height: 1.1;
    }
    .metric-label {
        font-size: 12px;
        font-weight: 500;
        color: #77798B;
        margin-top: 2px;
    }
    .metric-trend {
        font-size: 11px;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 3px;
        margin-top: 4px;
    }
    .trend-up { color: #1E5631; background: #DDF3E4; padding: 2px 6px; border-radius: 4px; }
    .trend-warn { color: #8B263E; background: #FCE6DA; padding: 2px 6px; border-radius: 4px; }

    /* Top Navigation Bar Header */
    .top-header {
        background: #FFFFFF;
        border: 1px solid #ECEAF2;
        border-radius: 12px;
        padding: 12px 20px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 6px rgba(52, 53, 74, 0.02);
    }
    .top-header-title {
        font-size: 18px;
        font-weight: 700;
        color: #34354A;
    }
    .top-header-subtitle {
        font-size: 12px;
        color: #77798B;
    }
    .top-header-right {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .user-pill {
        background: #F8F7FC;
        border: 1px solid #ECEAF2;
        border-radius: 20px;
        padding: 6px 14px;
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 12px;
        font-weight: 600;
        color: #34354A;
    }
    .notif-badge {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: #DCEBFA;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        color: #34354A;
        position: relative;
    }
    .notif-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #E57373;
        position: absolute;
        top: 4px;
        right: 4px;
    }

    /* Status Pills */
    .badge-pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 14px;
        font-size: 12px;
        font-weight: 600;
        text-align: center;
    }
    .badge-low {
        background-color: #DDF3E4;
        color: #1E5631;
    }
    .badge-medium {
        background-color: #FFF4D2;
        color: #7A5200;
    }
    .badge-high {
        background-color: #FCE6DA;
        color: #8B263E;
    }

    /* Streamlit Button Overrides */
    div.stButton > button {
        background-color: #DCD6F7 !important;
        color: #34354A !important;
        border: 1px solid #ECEAF2 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        padding: 6px 16px !important;
        transition: all 0.15s ease !important;
    }
    div.stButton > button:hover {
        background-color: #CEC5F5 !important;
        border-color: #CEC5F5 !important;
        box-shadow: 0 2px 6px rgba(52, 53, 74, 0.08) !important;
    }

    /* Form Inputs Overrides */
    div.stTextInput > div > div > input,
    div.stSelectbox > div > div,
    div.stNumberInput > div > div > input {
        border-radius: 8px !important;
        border: 1px solid #ECEAF2 !important;
        background-color: #FFFFFF !important;
        color: #34354A !important;
    }
    div.stTextInput > div > div > input:focus,
    div.stSelectbox > div > div:focus {
        border-color: #DCD6F7 !important;
        box-shadow: 0 0 0 2px rgba(220, 214, 247, 0.4) !important;
    }

    /* DataFrame & Table overrides */
    div[data-testid="stDataFrame"] {
        border: 1px solid #ECEAF2 !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }

    /* Expander styling */
    div[data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 1px solid #ECEAF2 !important;
        border-radius: 10px !important;
    }

    /* Section Heading Styling */
    .section-title {
        font-size: 16px;
        font-weight: 700;
        color: #34354A;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-subtitle {
        font-size: 12px;
        color: #77798B;
        margin-bottom: 14px;
    }

    /* Callout / Warning box */
    .eduguard-disclaimer {
        background-color: #F8DFE8;
        border-left: 4px solid #E57373;
        border-radius: 6px;
        padding: 10px 14px;
        font-size: 12px;
        color: #5C222E;
        margin-bottom: 14px;
    }

    .eduguard-info {
        background-color: #DCEBFA;
        border-left: 4px solid #4A90E2;
        border-radius: 6px;
        padding: 10px 14px;
        font-size: 12px;
        color: #1C3D6E;
        margin-bottom: 14px;
    }

    /* Hide Streamlit header & footer elements for clean SaaS look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {background: transparent !important;}
    </style>
    """, unsafe_allow_html=True)

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
