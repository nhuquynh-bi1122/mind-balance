# 🧠 Mind Balance

Hệ thống tư duy có cấu trúc giúp bạn:
- Thu thập data về mental state theo cách khoa học
- Phát hiện patterns mà bạn không thấy
- Học 7 frameworks xử lý stress khác nhau
- Tự xây dựng playbook cá nhân qua thời gian

## 🚀 Cài đặt
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📖 Hướng dẫn sử dụng

### 1. Check-in hàng ngày (2 phút)
- Ghi lại trạng thái tinh thần, năng lượng
- Liệt kê công việc
- Xem framework tư duy theo ngày

### 2. Phân tích tuần (sau 3+ ngày)
- Xem 3 biểu đồ tự động
- Phát hiện patterns
- Tạo AI prompt để hỏi ChatGPT/Claude

### 3. Xây dựng Playbook
- Lưu quy luật từ kinh nghiệm
- Test và verify hiệu quả
- Tạo "sách hướng dẫn" riêng

## 🔐 Tài khoản demo

- Username: `demo`
- Password: `secret123`

## 🧠 7 Frameworks tư duy

- **Thứ 2:** Đánh giá tổng quan
- **Thứ 3:** Ưu tiên (Eisenhower Matrix)
- **Thứ 4:** Quản lý năng lượng
- **Thứ 5:** Giao việc & hợp tác
- **Thứ 6:** Suy ngẫm tuần
- **Thứ 7:** Lên kế hoạch tuần sau

## 📊 Tech Stack

- **Frontend:** Streamlit
- **Database:** SQLite
- **Charts:** Plotly
- **Auth:** Custom hash-based

## 📁 Cấu trúc project
```
mind-balance/
├── app.py                          # Trang chủ + Login
├── pages/
│   ├── 1_📝_Nhập_Liệu_Hàng_Ngày.py
│   ├── 2_📊_Tổng_Kết_Tuần.py
│   └── 3_📚_Sổ_Tay_Cá_Nhân.py
├── utils/
│   ├── auth.py                     # Authentication
│   ├── database.py                 # SQLite operations
│   ├── charts.py                   # Plotly charts
│   ├── pattern_detector.py         # Pattern analysis
│   └── prompt_builder.py           # AI prompt generator
└── data/                           # SQLite databases (per user)
```

## 🎯 Value Proposition

**Mind Balance KHÔNG phải:**
- ❌ App tạo prompt
- ❌ Chatbot therapy
- ❌ Mood tracker thông thường

**Mind Balance LÀ:**
- ✅ Structured data collection system
- ✅ Pattern detection engine (rule-based)
- ✅ Cognitive framework library (7 modes)
- ✅ Personal playbook builder
- ✅ Progressive autonomy trainer

AI chỉ là Layer 5/5, không phải core!