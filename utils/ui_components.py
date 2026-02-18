"""
CSS Component cho Mind Balance App - SIMPLIFIED VERSION
"""

GRADIENT_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&family=Poppins:wght@400;600;700&display=swap');
    
    /* RESET & BASE */
    * {
        font-family: 'Quicksand', sans-serif;
    }
    
    /* GRADIENT BACKGROUND ANIMATED */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #667eea 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
    }
    
    @keyframes sparkle {
        0%, 100% { opacity: 0; transform: scale(0.5); }
        50% { opacity: 1; transform: scale(1.2); }
    }
    
    /* GLASSMORPHISM CONTAINER */
    .main .block-container {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        border-radius: 30px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        padding: 3rem 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    /* FOX HEADER */
    .fox-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .fox-emoji {
        font-size: 6rem;
        animation: bounce 2s ease-in-out infinite;
        display: inline-block;
        filter: drop-shadow(0 8px 16px rgba(0, 0, 0, 0.2));
    }
    
    .sparkles {
        font-size: 1.5rem;
        display: inline-block;
        margin: 0 0.5rem;
        animation: sparkle 2s ease-in-out infinite;
    }
    
    /* METRICS CARDS */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.15) 100%);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.5rem !important;
        border: 2px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        border-color: rgba(255, 255, 255, 0.5);
    }
    
    [data-testid="metric-container"] label {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* BUTTONS */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        box-shadow: 0 4px 15px rgba(240, 147, 251, 0.5);
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%);
        box-shadow: 0 6px 20px rgba(240, 147, 251, 0.7);
    }
    
    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(102, 126, 234, 0.95) 0%, rgba(118, 75, 162, 0.95) 100%);
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* INFO BOXES */
    .element-container .stAlert {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.1) 100%);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        color: white !important;
    }
    
    /* TEXT INPUT - NỀN TRẮNG CHỮ ĐEN */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px);
        border: 2px solid rgba(102, 126, 234, 0.5);
        border-radius: 12px;
        color: #2C3E50 !important;
        font-weight: 500;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(0, 0, 0, 0.4) !important;
    }
    
    /* TEXT AREA - NỀN TRẮNG CHỮ ĐEN */
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px);
        border: 2px solid rgba(102, 126, 234, 0.5);
        border-radius: 12px;
        color: #2C3E50 !important;
        font-weight: 500;
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: rgba(0, 0, 0, 0.4) !important;
    }
    
    /* SELECT BOX */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 12px;
    }
    
    /* SLIDER */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* TABS */
    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.1) 100%);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: rgba(255, 255, 255, 0.8) !important;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border-radius: 8px;
    }
    
    /* TEXT COLORS */
    h1, h2, h3, h4, h5, h6, p, span, div, li, label {
        color: white !important;
    }
    
    /* EXPANDER */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.1) 100%);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        color: white !important;
        font-weight: 600;
    }
    
    .streamlit-expanderContent {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.05) 100%);
        backdrop-filter: blur(10px);
        border-radius: 0 0 12px 12px;
    }
    
    /* DATAFRAME */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border-radius: 12px;
    }
    
    /* CODE BLOCK - NỀN TỐI */
    .stCodeBlock {
        background: rgba(30, 30, 50, 0.95) !important;
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 2px solid rgba(102, 126, 234, 0.5);
    }
    
    pre {
        background: rgba(30, 30, 50, 0.95) !important;
        color: #E0E0E0 !important;
        border-radius: 12px;
        padding: 1rem;
    }
    
    code {
        background: rgba(30, 30, 50, 0.95) !important;
        color: #E0E0E0 !important;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
    }
</style>
"""

def apply_gradient_theme():
    """Apply gradient theme to page"""
    import streamlit as st
    st.markdown(GRADIENT_CSS, unsafe_allow_html=True)

def show_fox_header(title):
    """Show fox mascot with page title using emoji"""
    import streamlit as st
    st.markdown(f"""
    <div class="fox-header">
        <div>
            <span class="sparkles">✨</span>
            <span class="fox-emoji">🦊</span>
            <span class="sparkles">✨</span>
        </div>
        <h1 style="margin: 1rem 0 0 0; font-family: 'Poppins', sans-serif; font-size: 2.5rem; font-weight: 700; color: white;">{title}</h1>
    </div>
    """, unsafe_allow_html=True)