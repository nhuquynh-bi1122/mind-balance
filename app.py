import streamlit as st
from utils.auth import login_form, check_authentication, logout
from utils.database import init_database, get_week_data, get_all_playbook_rules
from datetime import datetime
import pandas as pd

st.set_page_config(
    page_title="Mind Balance",
    page_icon="🧠",
    layout="wide"
)

# CSS SIÊU ĐẸP - FOX MASCOT + GRADIENT TRENDY
st.markdown("""
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
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
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
    
    /* TITLE STYLING */
    .big-title {
        font-family: 'Poppins', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0;
        color: white;
    }
    
    .subtitle {
        font-size: 1.3rem;
        text-align: center;
        color: rgba(255, 255, 255, 0.95);
        margin-bottom: 2rem;
        font-weight: 500;
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
        text-transform: none;
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
        color: white !important;
    }
    
    /* TEXT COLORS */
    h1, h2, h3, p, span, div, li {
        color: white !important;
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
    
    /* MARKDOWN */
    .stMarkdown {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

if not check_authentication():
    # TRANG LOGIN VỚI FOX EMOJI
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem; animation: fadeInDown 0.8s ease;">
        <div style="font-size: 8rem; display: inline-block; animation: bounce 2s ease-in-out infinite; filter: drop-shadow(0 8px 16px rgba(0, 0, 0, 0.2));">🦊</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="big-title">🧠 Mind Balance</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Hệ thống tư duy có cấu trúc</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        login_form()
        
        st.markdown("---")
        
        with st.expander("ℹ️ Mind Balance là gì?"):
            st.markdown("""
            **Mind Balance KHÔNG phải:**
            - ❌ App tạo prompt
            - ❌ Chatbot therapy
            - ❌ Mood tracker thông thường
            
            **Mind Balance LÀ:**
            - ✅ Hệ thống thu thập data có cấu trúc
            - ✅ Phát hiện patterns tự động
            - ✅ **8 frameworks tư duy** dựa trên nghiên cứu tâm lý học
            - ✅ Xây dựng playbook cá nhân
            - ✅ Tạo AI prompt context-rich (optional)
            
            **Kết quả:** Bạn tự học cách xử lý stress thông minh hơn!
            
            👉 Mỗi ngày = 1 framework khác nhau từ GTD, Eisenhower, Ultradian Rhythm...
            """)
else:
    # DASHBOARD SAU KHI LOGIN
    init_database(st.session_state.username)
    
    # Sidebar
    with st.sidebar:
        st.success(f"👋 Xin chào **{st.session_state.name}**")
        
        if st.button("🚪 Đăng xuất", width="stretch"):
            logout()
        
        st.markdown("---")
        st.caption("📍 Điều hướng nhanh")
        st.page_link("pages/1_📝_Nhập_Liệu_Hàng_Ngày.py", label="📝 Check-in hôm nay")
        st.page_link("pages/2_📊_Tổng_Kết_Tuần.py", label="📊 Xem phân tích")
        st.page_link("pages/3_📚_Sổ_Tay_Cá_Nhân.py", label="📚 Playbook của tôi")
        
        st.markdown("---")
        
        # NÚT XEM FRAMEWORK SCIENCE
        if st.button("🧠 Tại sao app hiệu quả?", width="stretch"):
            st.session_state.show_science = True
    
    # Header với FOX EMOJI
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem; animation: fadeInDown 0.8s ease;">
        <div style="font-size: 6rem; display: inline-block; animation: bounce 2s ease-in-out infinite; filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.2));">🦊</div>
        <h1 style="margin: 0.5rem 0 0 0; font-family: 'Poppins', sans-serif; font-size: 2.5rem; font-weight: 700; color: white;">🧠 Mind Balance Dashboard</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9; color: white;">Hôm nay: {datetime.now().strftime('%A, %d/%m/%Y')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Lấy data
    df_week = get_week_data(st.session_state.username)
    df_playbook = get_all_playbook_rules(st.session_state.username)
    
    # HIỂN THỊ FRAMEWORK SCIENCE NẾU ĐƯỢC YÊU CẦU
    if st.session_state.get('show_science', False):
        try:
            from utils.framework_explainer import show_framework_science
            show_framework_science()
            
            if st.button("✖️ Đóng", key="close_science"):
                st.session_state.show_science = False
                st.rerun()
            
            st.markdown("---")
        except ImportError:
            st.error("Chưa cài file framework_explainer.py. Vui lòng thêm file utils/framework_explainer.py")
    
    st.markdown("---")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        days_tracked = len(df_week)
        st.metric("📅 Ngày đã theo dõi", f"{days_tracked}/7")
    
    with col2:
        if days_tracked > 0:
            avg_energy = df_week['energy_level'].mean()
            st.metric("⚡ Năng lượng TB", f"{avg_energy:.1f}/10")
        else:
            st.metric("⚡ Năng lượng TB", "—")
    
    with col3:
        playbook_count = len(df_playbook)
        verified_count = len(df_playbook[df_playbook['status'] == 'verified']) if playbook_count > 0 else 0
        st.metric("📚 Playbook Rules", f"{verified_count} verified")
    
    with col4:
        if days_tracked > 0:
            import json
            total_tasks = sum(df_week['tasks'].apply(lambda x: len(json.loads(x))))
            st.metric("📋 Tổng công việc", total_tasks)
        else:
            st.metric("📋 Tổng công việc", "—")
    
    st.markdown("---")
    
    # Quick actions
    st.subheader("🚀 Hành động nhanh")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Check-in hôm nay", width="stretch", type="primary"):
            st.switch_page("pages/1_📝_Nhập_Liệu_Hàng_Ngày.py")
    
    with col2:
        if st.button("📊 Xem phân tích tuần", width="stretch"):
            st.switch_page("pages/2_📊_Tổng_Kết_Tuần.py")
    
    with col3:
        if st.button("📚 Mở Playbook", width="stretch"):
            st.switch_page("pages/3_📚_Sổ_Tay_Cá_Nhân.py")
    
    st.markdown("---")
    
    # Nội dung chính
    if days_tracked == 0:
        st.info("👋 Chào mừng đến Mind Balance! Hãy bắt đầu với check-in đầu tiên.")
        
        st.markdown("### 🎯 Cách sử dụng:")
        st.markdown("""
        1. **📝 Check-in hàng ngày** (1-2 phút)
           - Ghi lại trạng thái tinh thần, năng lượng
           - Liệt kê công việc hôm nay
           - Xem framework tư duy theo ngày
        
        2. **📊 Xem phân tích sau 3+ ngày**
           - 3 biểu đồ tự động
           - Phát hiện patterns
           - Tạo AI prompt context-rich
        
        3. **📚 Xây dựng Playbook**
           - Ghi lại quy luật từ kinh nghiệm
           - Test và verify
           - Tạo "sách hướng dẫn" cho chính mình
        """)
        
        if st.button("🚀 Bắt đầu check-in đầu tiên", type="primary", width="stretch"):
            st.switch_page("pages/1_📝_Nhập_Liệu_Hàng_Ngày.py")
    
    else:
        # Hiển thị mini charts
        tab1, tab2 = st.tabs(["📈 Xu hướng tuần này", "📚 Playbook gần đây"])
        
        with tab1:
            if days_tracked >= 3:
                from utils.charts import create_energy_trend
                fig = create_energy_trend(df_week)
                st.plotly_chart(fig, width="stretch")
                
                st.info(f"Bạn đã check-in {days_tracked} ngày tuần này. {'✅ Tuyệt vời!' if days_tracked >= 6 else '💪 Hãy tiếp tục!'}")
            else:
                st.warning(f"Cần ít nhất 3 ngày để hiển thị biểu đồ. Bạn đang có {days_tracked}/3 ngày.")
        
        with tab2:
            if playbook_count == 0:
                st.info("Bạn chưa có rule nào trong playbook. Hãy thêm rule đầu tiên sau khi phân tích tuần!")
            else:
                recent_rules = df_playbook.head(3)
                
                for idx, row in recent_rules.iterrows():
                    status_emoji = {'verified': '✅', 'testing': '🧪', 'failed': '❌'}
                    st.markdown(f"**{status_emoji[row['status']]} {row['rule_title']}**")
                    st.caption(f"Action: {row['action'][:100]}...")
                    st.markdown("---")
                
                if st.button("Xem tất cả rules →"):
                    st.switch_page("pages/3_📚_Sổ_Tay_Cá_Nhân.py")
    
    # Footer
    st.markdown("---")
    st.caption("💡 Tip: Check-in đều đặn mỗi ngày để phát hiện patterns chính xác hơn!")