import streamlit as st
from utils.database import (
    init_database, init_playbook_table, 
    save_playbook_rule, get_all_playbook_rules,
    update_rule_status, delete_playbook_rule
)
from utils.auth import check_authentication
from utils.ui_components import apply_gradient_theme, show_fox_header
from datetime import datetime

st.set_page_config(
    page_title="Sổ tay cá nhân",
    page_icon="📚",
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
init_playbook_table(username)

# ===== FOX HEADER =====
show_fox_header("📚 Sổ Tay Cá Nhân")
# ======================

st.markdown("### Những quy luật bạn tự khám phá")

st.info("""
💡 **Playbook là gì?**

Đây là nơi lưu những quy luật bạn học được từ kinh nghiệm:
- ✅ **Verified:** Đã test và có hiệu quả
- 🧪 **Testing:** Đang thử nghiệm
- ❌ **Failed:** Thử rồi nhưng không hiệu quả
""")

# Lấy tất cả rules
df_rules = get_all_playbook_rules(username)

# Tabs
tab1, tab2 = st.tabs(["📖 Xem Playbook", "➕ Thêm Rule Mới"])

with tab1:
    if len(df_rules) == 0:
        st.warning("Bạn chưa có rule nào. Hãy thêm rule đầu tiên!")
    else:
        st.success(f"✅ Bạn có {len(df_rules)} rules trong playbook")
        
        # Filter theo status
        status_filter = st.radio(
            "Lọc theo trạng thái:",
            ["Tất cả", "✅ Verified", "🧪 Testing", "❌ Failed"],
            horizontal=True
        )
        
        status_map = {
            "✅ Verified": "verified",
            "🧪 Testing": "testing",
            "❌ Failed": "failed"
        }
        
        if status_filter != "Tất cả":
            filtered_df = df_rules[df_rules['status'] == status_map[status_filter]]
        else:
            filtered_df = df_rules
        
        if len(filtered_df) == 0:
            st.info(f"Không có rule nào với status: {status_filter}")
        else:
            # Hiển thị từng rule
            for idx, row in filtered_df.iterrows():
                status_emoji = {
                    'verified': '✅',
                    'testing': '🧪',
                    'failed': '❌'
                }
                
                with st.expander(f"{status_emoji[row['status']]} {row['rule_title']}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**Khi nào áp dụng:** {row['trigger']}")
                        st.markdown(f"**Hành động:** {row['action']}")
                        st.markdown(f"**Tuần test:** {row['tested_week']}")
                        st.markdown(f"**Kết quả:** {row['result']}")
                    
                    with col2:
                        st.markdown("**Thao tác:**")
                        
                        if row['status'] == 'testing':
                            if st.button("✅ Mark Verified", key=f"verify_{row['id']}"):
                                update_rule_status(username, row['id'], 'verified')
                                st.rerun()
                            
                            if st.button("❌ Mark Failed", key=f"fail_{row['id']}"):
                                update_rule_status(username, row['id'], 'failed')
                                st.rerun()
                        
                        if st.button("🗑️ Xóa", key=f"delete_{row['id']}", type="secondary"):
                            delete_playbook_rule(username, row['id'])
                            st.toast("Đã xóa rule!", icon="🗑️")
                            st.rerun()

with tab2:
    st.subheader("➕ Thêm Rule Mới")
    st.caption("Ghi lại những gì bạn học được từ tuần vừa qua")
    
    with st.form("add_rule_form"):
        rule_title = st.text_input(
            "Tên rule (ngắn gọn):",
            placeholder="Ví dụ: Pack lunch đêm trước khi có lịch dày"
        )
        
        trigger = st.text_area(
            "Khi nào cần áp dụng rule này?",
            placeholder="Ví dụ: Khi hôm sau có lịch học/họp liên tục từ sáng đến chiều",
            height=80
        )
        
        action = st.text_area(
            "Hành động cụ thể là gì?",
            placeholder="Ví dụ: Tối hôm trước chuẩn bị lunch box + 2 món ăn vặt. Set alarm 12h để nhắc ăn.",
            height=100
        )
        
        tested_week = st.text_input(
            "Tuần nào đã test?",
            value=f"Tuần {datetime.now().isocalendar()[1]}/2026"
        )
        
        result = st.text_area(
            "Kết quả khi áp dụng:",
            placeholder="Ví dụ: Năng lượng tăng từ 2/10 lên 6/10. Không bị crash sau meeting nữa.",
            height=80
        )
        
        status = st.radio(
            "Trạng thái:",
            ["🧪 Đang test", "✅ Đã verify hiệu quả", "❌ Không hiệu quả"],
            horizontal=True
        )
        
        status_value_map = {
            "🧪 Đang test": "testing",
            "✅ Đã verify hiệu quả": "verified",
            "❌ Không hiệu quả": "failed"
        }
        
        submitted = st.form_submit_button("💾 Lưu rule", width="stretch", type="primary")
        
        if submitted:
            if not rule_title or not trigger or not action:
                st.error("❌ Vui lòng điền đầy đủ: Tên rule, Trigger, Action")
            else:
                rule_data = {
                    'rule_title': rule_title,
                    'trigger': trigger,
                    'action': action,
                    'tested_week': tested_week,
                    'result': result,
                    'status': status_value_map[status]
                }
                
                if save_playbook_rule(username, rule_data):
                    st.success("✅ Đã lưu rule vào playbook!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Có lỗi xảy ra!")

st.markdown("---")

# Stats playbook
if len(df_rules) > 0:
    st.subheader("📊 Thống kê Playbook")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        verified_count = len(df_rules[df_rules['status'] == 'verified'])
        st.metric("✅ Rules đã verify", verified_count)
    
    with col2:
        testing_count = len(df_rules[df_rules['status'] == 'testing'])
        st.metric("🧪 Rules đang test", testing_count)
    
    with col3:
        failed_count = len(df_rules[df_rules['status'] == 'failed'])
        st.metric("❌ Rules thất bại", failed_count)