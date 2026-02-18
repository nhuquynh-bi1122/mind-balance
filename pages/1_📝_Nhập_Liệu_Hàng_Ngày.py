import streamlit as st
from datetime import datetime
from utils.database import (init_database, save_checkin, get_checkin_today, 
                           save_task_metadata, get_task_metadata, 
                           save_schedule, get_schedule)
from utils.auth import check_authentication
from utils.ui_components import apply_gradient_theme, show_fox_header
from utils.framework_explainer import show_framework_science
import json

st.set_page_config(
    page_title="Nhập liệu hàng ngày",
    page_icon="📝",
    layout="wide"
)

apply_gradient_theme()

if not check_authentication():
    st.warning("⚠️ Vui lòng đăng nhập trước!")
    st.stop()

username = st.session_state.username
init_database(username)

show_fox_header("📝 Nhập liệu hàng ngày")

weekday_emoji = {
    "Monday": "📅", "Tuesday": "📘", "Wednesday": "⚡", "Thursday": "🤝",
    "Friday": "🎯", "Saturday": "📋", "Sunday": "😴"
}
today_weekday = datetime.now().strftime("%A")
emoji = weekday_emoji.get(today_weekday, "📅")
st.markdown(f"**Hôm nay:** {emoji} {datetime.now().strftime('%A, %d/%m/%Y')}")

show_framework_science()

existing_checkin = get_checkin_today(username)

if existing_checkin:
    st.success("✅ Bạn đã check-in hôm nay rồi!")
    if st.button("🔄 Cập nhật lại"):
        st.rerun()
else:
    st.info("Hãy dành 2-3 phút để check-in hôm nay")

st.markdown("---")

# ============= FORM CHECK-IN NÂNG CẤP =============
if not existing_checkin:
    with st.form("daily_checkin_form"):
        st.subheader("🧠 Bạn cảm thấy thế nào hôm nay?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            mental_load = st.radio(
                "Mức độ áp lực tinh thần:",
                ["Nhẹ nhàng", "Bình thường", "Nặng", "Cực nặng"],
                horizontal=True
            )
            
            energy_level = st.slider(
                "Mức năng lượng:",
                min_value=1, max_value=10, value=5
            )
        
        with col2:
            pressure_source = st.radio(
                "Nguồn áp lực chính:",
                ["Deadline bên ngoài", "Tự đặt ra", "Cả hai"],
                horizontal=True
            )
            
            sleep_quality = st.select_slider(
                "Chất lượng giấc ngủ:",
                options=[1, 2, 3, 4, 5],
                value=3,
                format_func=lambda x: "⭐" * x
            )
        
        st.markdown("---")
        st.subheader("📋 Công việc hôm nay")
        
        # THÊM LỊCH CỐ ĐỊNH
        with st.expander("⚙️ Lịch cố định hôm nay (học, học kèm, hoạt động...)"):
            st.caption("Nhập các lịch CỐ ĐỊNH không thay đổi được (học trên lớp, học kèm, câu lạc bộ...)")
            
            num_fixed = st.number_input("Số lịch cố định:", min_value=0, max_value=10, value=0, key="num_fixed")
            
            fixed_schedule = []
            for i in range(num_fixed):
                col_a, col_b, col_c = st.columns([2, 1, 1])
                with col_a:
                    fixed_name = st.text_input(f"Tên lịch {i+1}:", key=f"fixed_name_{i}", 
                                              placeholder="VD: Học trên lớp, Học kèm Toán...")
                with col_b:
                    fixed_start = st.time_input(f"Từ:", datetime.strptime("07:00", "%H:%M").time(), key=f"fixed_start_{i}")
                with col_c:
                    fixed_end = st.time_input(f"Đến:", datetime.strptime("11:30", "%H:%M").time(), key=f"fixed_end_{i}")
                
                if fixed_name:
                    fixed_schedule.append({
                        'name': fixed_name,
                        'start': fixed_start.strftime("%H:%M"),
                        'end': fixed_end.strftime("%H:%M")
                    })
        
        st.markdown("---")
        
        # NHẬP TASKS VỚI METADATA
        st.caption("**Công việc cần làm trong khoảng thời gian rảnh:**")
        
        num_tasks = st.number_input("Số công việc:", min_value=1, max_value=15, value=3, key="num_tasks")
        
        tasks_with_meta = []
        
        for i in range(num_tasks):
            with st.container():
                st.markdown(f"**Công việc {i+1}:**")
                
                col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
                
                with col1:
                    task_name = st.text_input(
                        "Tên công việc:", 
                        key=f"task_{i}",
                        placeholder="VD: Làm bài tập Sinh học chương 3"
                    )
                
                with col2:
                    estimated_time = st.selectbox(
                        "Thời gian ước tính:",
                        [15, 30, 45, 60, 90, 120, 180, 240],
                        format_func=lambda x: f"{x//60}h{x%60}'" if x >= 60 else f"{x}'",
                        key=f"time_{i}"
                    )
                
                with col3:
                    priority = st.selectbox(
                        "Độ ưu tiên:",
                        ["High", "Medium", "Low"],
                        key=f"priority_{i}"
                    )
                
                with col4:
                    task_type = st.selectbox(
                        "Loại công việc:",
                        ["Deep Work", "Shallow Work", "Meeting"],
                        key=f"type_{i}",
                        help="Deep Work: Cần tập trung cao (học, làm bài). Shallow: Admin, reply. Meeting: Họp nhóm."
                    )
                
                if task_name:
                    tasks_with_meta.append({
                        'name': task_name,
                        'estimated_time': estimated_time,
                        'priority': priority,
                        'task_type': task_type
                    })
                
                st.markdown("---")
        
        task_feeling = st.radio(
            "Nhìn vào danh sách công việc, bạn cảm thấy:",
            ["Hoàn toàn làm được", "Hơi căng nhưng OK", "Nặng", "Không thể nào"],
            horizontal=True
        )
        
        col_a, col_b = st.columns([1, 1])
        with col_a:
            work_start = st.time_input("Giờ thức dậy:", datetime.strptime("06:00", "%H:%M").time())
        with col_b:
            work_end = st.time_input("Giờ đi ngủ:", datetime.strptime("22:00", "%H:%M").time())
        
        submitted = st.form_submit_button("💾 Lưu check-in hôm nay", type="primary", use_container_width=True)
        
        if submitted:
            if len(tasks_with_meta) == 0:
                st.error("❌ Vui lòng nhập ít nhất 1 công việc!")
            else:
                # Lưu check-in cơ bản
                tasks_list = [t['name'] for t in tasks_with_meta]
                data = {
                    'date': datetime.now().strftime("%Y-%m-%d"),
                    'mental_load': mental_load,
                    'energy_level': energy_level,
                    'pressure_source': pressure_source,
                    'sleep_quality': sleep_quality,
                    'tasks': tasks_list,
                    'task_feeling': task_feeling
                }
                
                if save_checkin(username, data):
                    # Lưu metadata
                    save_task_metadata(username, data['date'], tasks_with_meta)
                    
                    # Lưu fixed schedule vào session để dùng cho scheduler
                    st.session_state.fixed_schedule = fixed_schedule
                    st.session_state.work_hours = {
                        'start': work_start.strftime("%H:%M"),
                        'end': work_end.strftime("%H:%M")
                    }
                    
                    st.success("✅ Đã lưu thành công!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Có lỗi xảy ra!")

# ============= SAU KHI CHECK-IN =============
if existing_checkin:
    st.markdown("---")
    st.subheader("📸 Check-in hôm nay")
    
    tasks = json.loads(existing_checkin[6])
    date = existing_checkin[1]
    energy = existing_checkin[3]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Trạng thái tinh thần", existing_checkin[2])
        st.metric("Năng lượng", f"{energy}/10")
    
    with col2:
        st.metric("Nguồn áp lực", existing_checkin[4])
        st.metric("Giấc ngủ", "⭐" * existing_checkin[5])
    
    with col3:
        st.metric("Số công việc", len(tasks))
        st.metric("Cảm giác", existing_checkin[7])
    
    # ============= NÚT TẠO LỊCH THÔNG MINH =============
    st.markdown("---")
    
    existing_schedule = get_schedule(username, date)
    
    if not existing_schedule:
        st.subheader("🤖 Tạo lịch thông minh")
        st.info("💡 AI sẽ giúp bạn xếp lịch dựa trên năng lượng, framework hôm nay, và tránh burn out!")
        
        if st.button("✨ Tạo lịch thông minh ngay", type="primary", use_container_width=True):
            # Lấy metadata tasks
            tasks_meta_df = get_task_metadata(username, date)
            
            if len(tasks_meta_df) == 0:
                st.error("❌ Chưa có metadata tasks. Vui lòng cập nhật lại check-in với thông tin đầy đủ!")
            else:
                tasks_with_meta = tasks_meta_df.to_dict('records')
                
                # Lấy fixed schedule từ session hoặc default empty
                fixed_schedule = st.session_state.get('fixed_schedule', [])
                work_hours = st.session_state.get('work_hours', {'start': '06:00', 'end': '22:00'})
                
                # Get framework name
                weekday = datetime.strptime(date, "%Y-%m-%d").strftime("%A")
                framework_names = {
                    "Monday": "📅 Thứ 2 - Weekly Review (GTD Method)",
                    "Tuesday": "📘 Thứ 3 - Eisenhower Matrix",
                    "Wednesday": "⚡ Thứ 4 - Ultradian Rhythm Management",
                    "Thursday": "🤝 Thứ 5 - Delegation & Cognitive Offloading",
                    "Friday": "🎯 Thứ 6 - Reflective Practice (Kolb's Cycle)",
                    "Saturday": "📋 Thứ 7 - Strategic Planning (If-Then)",
                    "Sunday": "😴 Chủ nhật - Purposeful Recovery"
                }
                framework_name = framework_names.get(weekday, "")
                
                # Tạo lịch
                from utils.scheduler import create_daily_schedule
                
                result = create_daily_schedule(
                    tasks_with_meta=tasks_with_meta,
                    fixed_schedule=fixed_schedule,
                    work_start=work_hours['start'],
                    work_end=work_hours['end'],
                    energy_level=energy,
                    today_framework=framework_name
                )
                
                # Lưu lịch
                save_schedule(username, date, work_hours['start'], work_hours['end'], result)
                
                st.success("✅ Đã tạo lịch thành công!")
                st.rerun()
    
    # ============= HIỂN THỊ LỊCH ĐÃ TẠO =============
    if existing_schedule:
        st.subheader("📅 Lịch hôm nay")
        
        schedule_data = json.loads(existing_schedule[4])
        
        # Warnings
        if len(schedule_data['warnings']) > 0:
            st.warning("⚠️ **CẢNH BÁO BURN OUT:**")
            for warning in schedule_data['warnings']:
                st.markdown(f"- {warning}")
        
        # Suggestions
        if len(schedule_data['suggestions']) > 0:
            st.info("💡 **GỢI Ý TỐI ƯU:**")
            for suggestion in schedule_data['suggestions']:
                st.markdown(f"- {suggestion}")
        
        st.markdown("---")
        
        # Timeline
        st.markdown("### 🕐 Timeline hôm nay")
        
        for item in schedule_data['schedule']:
            item_type = item['type']
            color = item.get('color', '#6B7280')
            
            if item_type == 'Fixed':
                st.markdown(f"""
                <div style="background: {color}; padding: 0.75rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 4px solid #4B5563;">
                    <strong>{item['start']} - {item['end']}</strong> | 🏫 {item['task']}
                </div>
                """, unsafe_allow_html=True)
            
            elif item_type == 'Break':
                st.markdown(f"""
                <div style="background: {color}; padding: 0.5rem; border-radius: 8px; margin-bottom: 0.5rem; opacity: 0.8;">
                    <strong>{item['start']} - {item['end']}</strong> | {item['task']}
                </div>
                """, unsafe_allow_html=True)
            
            else:
                priority_emoji = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}.get(item['priority'], '')
                duration = (datetime.strptime(item['end'], "%H:%M") - datetime.strptime(item['start'], "%H:%M")).seconds // 60
                
                st.markdown(f"""
                <div style="background: {color}; padding: 0.75rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 4px solid {color};">
                    <strong>{item['start']} - {item['end']}</strong> ({duration}') | {priority_emoji} {item['task']}<br>
                    <small style="opacity: 0.8;">{item['type']}</small>
                </div>
                """, unsafe_allow_html=True)
        
        # Stats
        st.markdown("---")
        st.markdown("### 📊 Thống kê")
        
        col1, col2, col3, col4 = st.columns(4)
        stats = schedule_data['stats']
        
        with col1:
            st.metric("Tổng tasks", stats['total_tasks'])
        with col2:
            st.metric("Đã xếp", stats['scheduled_tasks'])
        with col3:
            st.metric("Thời gian làm", f"{stats['actual_work_time']//60}h{stats['actual_work_time']%60}'")
        with col4:
            st.metric("Breaks", stats['breaks_count'])
        
        # Xóa và tạo lại
        if st.button("🔄 Tạo lại lịch"):
            # Xóa lịch cũ bằng cách không làm gì, chỉ rerun để hiện nút tạo lại
            st.session_state.temp_delete_schedule = date
            st.rerun()
    
    # ============= FRAMEWORK TƯ DUY =============
    st.markdown("---")
    st.subheader("🧠 Framework tư duy hôm nay")
    
    from utils.prompt_builder import build_daily_framework_prompt
    
    data = {
        'mental_load': existing_checkin[2],
        'energy_level': existing_checkin[3],
        'tasks': tasks
    }
    
    weekday = datetime.strptime(date, "%Y-%m-%d").strftime("%A")
    framework_names = {
        "Monday": "📅 Thứ 2 - Weekly Review (GTD Method)",
        "Tuesday": "📘 Thứ 3 - Eisenhower Matrix",
        "Wednesday": "⚡ Thứ 4 - Ultradian Rhythm Management",
        "Thursday": "🤝 Thứ 5 - Delegation & Cognitive Offloading",
        "Friday": "🎯 Thứ 6 - Reflective Practice (Kolb's Cycle)",
        "Saturday": "📋 Thứ 7 - Strategic Planning (If-Then)",
        "Sunday": "😴 Chủ nhật - Purposeful Recovery"
    }
    framework_name = framework_names.get(weekday, "📅 Thứ 2 - Weekly Review")
    
    st.info(f"**Framework hôm nay:** {framework_name}")
    
    prompt = build_daily_framework_prompt(date, data, framework_name)
    
    tab1, tab2 = st.tabs(["📖 Tự suy nghĩ", "🤖 Hỏi AI"])
    
    with tab1:
        st.markdown(prompt)
        st.caption("💡 Framework giúp rèn TƯ DUY - Scheduler giúp CHỐNG BURN OUT!")
    
    with tab2:
        st.markdown("**Copy prompt và hỏi ChatGPT/Claude:**")
        st.code(prompt, language="markdown")