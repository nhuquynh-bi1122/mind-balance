import streamlit as st
from utils.database import get_week_data, init_database
from utils.charts import create_energy_trend, create_task_energy_comparison, create_mood_matrix
from utils.pattern_detector import detect_patterns
from utils.auth import check_authentication
from utils.ui_components import apply_gradient_theme, show_fox_header
import json

st.set_page_config(
    page_title="Tổng kết tuần",
    page_icon="📊",
    layout="wide"
)

# ===== THÊM GRADIENT THEME =====
apply_gradient_theme()
# ================================

if not check_authentication():
    st.warning("⚠️ Vui lòng đăng nhập trước!")
    st.stop()

username = st.session_state.username
init_database(username)

# ===== FOX HEADER =====
show_fox_header("📊 Tổng kết tuần")
# ======================

df = get_week_data(username)

if len(df) == 0:
    st.info("Bạn chưa có dữ liệu nào. Hãy bắt đầu check-in hàng ngày!")
    st.stop()

if len(df) < 6:
    st.warning(f"⚠️ Bạn mới check-in {len(df)}/7 ngày. Cần ít nhất 6 ngày để phân tích đầy đủ!")

st.success(f"✅ Bạn đã check-in {len(df)} ngày trong tuần này!")

st.markdown("---")

st.subheader("📈 Biểu đồ phân tích")

tab1, tab2, tab3 = st.tabs(["Xu hướng năng lượng", "Công việc vs Năng lượng", "Ma trận tâm trạng"])

with tab1:
    fig1 = create_energy_trend(df)
    st.plotly_chart(fig1, width="stretch")

with tab2:
    fig2 = create_task_energy_comparison(df)
    st.plotly_chart(fig2, width="stretch")

with tab3:
    fig3 = create_mood_matrix(df)
    st.plotly_chart(fig3, width="stretch")

st.markdown("---")

st.subheader("🔍 Patterns phát hiện được")

patterns = detect_patterns(df)

for pattern in patterns:
    if "⚠️" in pattern or "📋" in pattern or "😴" in pattern or "🔋" in pattern:
        st.warning(pattern)
    else:
        st.success(pattern)

st.markdown("---")

st.subheader("📊 Thống kê tổng quan")

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_energy = df['energy_level'].mean()
    st.metric("Năng lượng TB", f"{avg_energy:.1f}/10")

with col2:
    avg_sleep = df['sleep_quality'].mean()
    st.metric("Giấc ngủ TB", f"{'⭐' * int(avg_sleep)}")

with col3:
    total_tasks = sum(df['tasks'].apply(lambda x: len(json.loads(x))))
    st.metric("Tổng công việc", total_tasks)

with col4:
    heavy_days = len(df[df['mental_load'].isin(['Nặng', 'Cực nặng'])])
    st.metric("Ngày áp lực cao", f"{heavy_days}/{len(df)}")

# PHẦN AI PROMPT GENERATOR
if len(df) >= 3:
    st.markdown("---")
    st.subheader("🤖 AI Prompt Generator")
    
    st.info("💡 Prompt này chứa toàn bộ context tuần của bạn, giúp AI đưa ra giải pháp CỤ THỂ")
    
    from utils.prompt_builder import build_weekly_prompt
    
    prompt = build_weekly_prompt(df, patterns)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("**Cách dùng:** Copy prompt bên dưới → Paste vào ChatGPT/Claude/Gemini")
    
    with col2:
        if st.button("📋 Copy Prompt", width="stretch", type="primary"):
            st.toast("✅ Đã copy! Paste vào AI assistant của bạn", icon="✅")
    
    st.code(prompt, language="markdown", line_numbers=True)
    
    with st.expander("ℹ️ Giải thích prompt này"):
        st.markdown("""
        **Prompt này chứa:**
        1. 📊 Dữ liệu tổng quan (năng lượng TB, số công việc TB)
        2. 📅 Chi tiết từng ngày trong tuần
        3. 🔍 Patterns tự động phát hiện
        4. 💥 Phân tích sâu ngày năng lượng sụp đổ (nếu có)
        5. ❓ Câu hỏi cụ thể yêu cầu AI đưa ra 3 giải pháp vi mô
        
        **AI sẽ trả về:**
        - Nguyên nhân gốc rễ
        - 3 hành động cụ thể có thể làm ngay tuần sau
        - Không phải lời khuyên chung chung!
        """)

if len(df) >= 6:
    st.markdown("---")
    st.success("🎉 Bạn đã hoàn thành đủ dữ liệu tuần này!")