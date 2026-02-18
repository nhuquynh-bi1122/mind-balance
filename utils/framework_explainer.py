"""
Component hiển thị giải thích khoa học về 8 frameworks
Dùng trong app.py hoặc page nào cần
"""

import streamlit as st
from utils.prompt_builder import get_framework_science

def show_framework_science():
    """Hiển thị expander với giải thích khoa học đầy đủ"""
    
    science = get_framework_science()
    
    with st.expander("🧠 Tại sao Mind Balance hiệu quả? (Dựa trên 8 nghiên cứu tâm lý học)"):
        st.markdown(f"### {science['title']}")
        st.markdown(science['intro'])
        
        st.markdown("---")
        st.markdown("## 📚 Chi tiết 8 Frameworks")
        
        for fw in science['frameworks']:
            with st.container():
                # Header với icon
                day_icons = {
                    "Thứ 2": "📅",
                    "Thứ 3": "📘",
                    "Thứ 4": "⚡",
                    "Thứ 5": "🤝",
                    "Thứ 6": "🎯",
                    "Thứ 7": "📋",
                    "Chủ nhật": "😴"
                }
                icon = day_icons.get(fw['day'], "📌")
                
                st.markdown(f"### {icon} {fw['day']}: {fw['name']}")
                
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    st.markdown("**📖 Nghiên cứu:**")
                    st.markdown("**💡 Tại sao work:**")
                    st.markdown("**📊 Evidence:**")
                    st.markdown("**🎯 Cách làm:**")
                
                with col2:
                    st.markdown(fw['research'])
                    st.markdown(fw['why_works'])
                    st.info(fw['evidence'])
                    st.success(fw['how'])
                
                st.markdown("---")
        
        # Conclusion
        st.markdown("## 🎓 Kết luận")
        st.markdown(science['conclusion'])
        
        # Call to action
        st.success("💪 **Bắt đầu ngay:** Check-in hàng ngày để train não bộ theo 8 frameworks này!")


def show_framework_science_compact():
    """Version nhỏ gọn - chỉ list tên frameworks"""
    
    with st.expander("ℹ️ Tại sao có 8 frameworks khác nhau?"):
        st.markdown("""
        **Mind Balance sử dụng 8 frameworks dựa trên nghiên cứu tâm lý học:**
        
        - 📅 **Thứ 2 - Weekly Review** (GTD Method): Nhìn tổng quan tuần mới
        - 📘 **Thứ 3 - Eisenhower Matrix**: Phân loại Urgent vs Important  
        - ⚡ **Thứ 4 - Ultradian Rhythm**: Quản lý chu kỳ năng lượng 90 phút
        - 🤝 **Thứ 5 - Delegation**: Giảm cognitive load bằng cách nhờ người khác
        - 🎯 **Thứ 6 - Reflective Practice**: Học từ kinh nghiệm tuần vừa qua
        - 📋 **Thứ 7 - Strategic Planning**: If-then planning cho tuần sau
        - 😴 **Chủ nhật - Purposeful Recovery**: Nghỉ ngơi có chủ đích
        
        Mỗi ngày = 1 cách suy nghĩ khác nhau về cùng 1 danh sách công việc!
        
        👉 [Xem giải thích chi tiết về nghiên cứu](#) *(click để mở full version)*
        """)