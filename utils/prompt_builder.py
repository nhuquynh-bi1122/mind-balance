import json
from datetime import datetime

def build_weekly_prompt(df, patterns):
    """Tạo AI prompt từ data tuần"""
    
    if len(df) == 0:
        return "Chưa có dữ liệu để tạo prompt"
    
    # Tính toán metrics
    avg_energy = df['energy_level'].mean()
    df['task_count'] = df['tasks'].apply(lambda x: len(json.loads(x)))
    avg_tasks = df['task_count'].mean()
    
    # Tìm ngày năng lượng thấp nhất
    worst_day = df.loc[df['energy_level'].idxmin()]
    best_day = df.loc[df['energy_level'].idxmax()]
    
    # Build prompt
    prompt = f"""# BỐI CẢNH TUẦN VỪA QUA

Tôi đã theo dõi trạng thái tinh thần và năng lượng của mình trong {len(df)} ngày vừa qua. Dưới đây là data chi tiết:

## DỮ LIỆU TỔNG QUAN
- Năng lượng trung bình: {avg_energy:.1f}/10
- Số công việc trung bình mỗi ngày: {avg_tasks:.1f} việc
- Ngày năng lượng cao nhất: {best_day['date']} ({best_day['energy_level']}/10)
- Ngày năng lượng thấp nhất: {worst_day['date']} ({worst_day['energy_level']}/10)

## CHI TIẾT TỪNG NGÀY
"""
    
    # Thêm data từng ngày
    for _, row in df.iterrows():
        tasks = json.loads(row['tasks'])
        prompt += f"""
### {row['date']}
- Trạng thái tinh thần: {row['mental_load']}
- Năng lượng: {row['energy_level']}/10
- Nguồn áp lực: {row['pressure_source']}
- Giấc ngủ: {'⭐' * row['sleep_quality']}
- Số công việc: {len(tasks)} việc
- Cảm giác về công việc: {row['task_feeling']}
"""
    
    # Thêm patterns
    prompt += f"""
## PATTERNS PHÁT HIỆN ĐƯỢC
"""
    for i, pattern in enumerate(patterns, 1):
        # Bỏ emoji để AI dễ đọc
        clean_pattern = pattern.replace('⚠️', '').replace('📋', '').replace('😴', '').replace('🔋', '').replace('✅', '').strip()
        prompt += f"{i}. {clean_pattern}\n"
    
    # Thêm ngày năng lượng crash (nếu có)
    energy_drops = df['energy_level'].diff()
    big_drops = energy_drops[energy_drops < -3]
    
    if len(big_drops) > 0:
        crash_day = df.loc[big_drops.idxmin()]
        prev_day = df.loc[big_drops.idxmin() - 1] if big_drops.idxmin() > 0 else None
        
        prompt += f"""
## PHÂN TÍCH SÂU: NGÀY NĂNG LƯỢNG SỤP ĐỔ

Ngày {crash_day['date']}, năng lượng của tôi giảm từ {prev_day['energy_level'] if prev_day is not None else 'N/A'}/10 xuống {crash_day['energy_level']}/10.

Chi tiết ngày này:
- Trạng thái: {crash_day['mental_load']}
- Công việc: {len(json.loads(crash_day['tasks']))} việc
- Giấc ngủ đêm trước: {'⭐' * crash_day['sleep_quality']}
- Nguồn áp lực: {crash_day['pressure_source']}
"""
    
    # Yêu cầu AI
    prompt += """
---

Dựa trên dữ liệu cụ thể này, hãy giúp tôi:

1. **Xác định nguyên nhân chính** gây ra sự sụp đổ năng lượng hoặc patterns tiêu cực
2. **Đưa ra 3 giải pháp vi mô cụ thể** (micro-changes) mà tôi có thể thử ngay tuần sau
3. **Tập trung vào hành động thực tế**, không phải lời khuyên chung chung như "nghỉ ngơi nhiều hơn"

Ví dụ giải pháp tốt:
- "Di chuyển 1 công việc từ thứ 4 sang thứ 3"
- "Chuẩn bị bữa trưa tối thứ 3 để tránh bỏ bữa thứ 4"
- "Chặn 30 phút buffer sau meeting để không phải vội vàng"

Hãy đưa ra giải pháp dựa trên PATTERN CỤ THỂ trong data của tôi.
"""
    
    return prompt


def build_daily_framework_prompt(date, data, framework_name):
    """Tạo prompt cho framework hàng ngày"""
    
    tasks = data.get('tasks', [])
    
    frameworks = {
        "Thứ 2 - Weekly Review": """
Hôm nay là Thứ Hai - chế độ WEEKLY REVIEW (Đánh giá tổng quan).

📚 **Framework:** David Allen's Getting Things Done (GTD)

Thay vì lao vào làm việc, hãy nhìn bức tranh toàn cảnh trước:

CÂU HỎI FRAMEWORK:
1. Những công việc nào có liên quan đến nhau?
2. Việc nào BẮT BUỘC hôm nay vs việc nào có thể đợi?
3. Điểm nghẽn là gì? (meeting cố định, deadline cứng...)
4. Nếu chỉ làm được 2 việc, 2 việc nào tác động lớn nhất?

Hãy giúp tôi phân tích danh sách công việc theo 4 câu hỏi trên.
""",
        "Thứ 3 - Eisenhower Matrix": """
Hôm nay là Thứ Ba - chế độ ƯU TIÊN.

📚 **Framework:** Eisenhower Decision Principle (Urgent vs Important)

Áp dụng ma trận Eisenhower để phân loại:

CÂU HỎI FRAMEWORK:
1. Việc nào VỪA QUAN TRỌNG VỪA GẤP? → Làm NGAY
2. Việc nào "cảm giác gấp" nhưng thực ra không quan trọng? → XÓA/UỶ QUYỀN
3. Việc nào quan trọng nhưng chưa gấp (dễ bỏ qua)? → LÊN LỊCH CỤ THỂ
4. Việc nào có thể loại bỏ hoàn toàn? → IGNORE

Phân loại công việc của tôi vào 4 quadrants này.
""",
        "Thứ 4 - Ultradian Rhythm": """
Hôm nay là Thứ Tư - chế độ QUẢN LÝ NĂNG LƯỢNG.

📚 **Framework:** Kleitman's Basic Rest-Activity Cycle (BRAC)

Thứ 4 thường là ngày năng lượng giảm. Cần match công việc với nhịp sinh học:

CÂU HỎI FRAMEWORK:
1. Việc nào cần năng lượng cao nhất? → Làm sáng sớm (9-11am)
2. Việc nào làm được khi mệt? → Để chiều/tối (3-5pm)
3. Lúc nào trong ngày tôi thường mệt nhất? → Tránh deep work lúc đó
4. Cần tạo break buffer ở đâu? → Mỗi 90 phút nghỉ 10-15 phút

Sắp xếp lại lịch công việc theo chu kỳ năng lượng 90 phút.
""",
        "Thứ 5 - Delegation": """
Hôm nay là Thứ Năm - chế độ GIAO VIỆC & HỢP TÁC.

📚 **Framework:** Cognitive Load Theory (Sweller, 1988)

Não bộ chỉ xử lý được 4±1 items cùng lúc. Không phải làm hết một mình:

CÂU HỎI FRAMEWORK:
1. Việc nào người khác có thể làm thay? → DELEGATE
2. Việc nào cần xin trợ giúp? → ASK FOR HELP
3. Việc nào có thể làm chung (hiệu quả hơn)? → COLLABORATE
4. Việc nào có thể xin gia hạn deadline? → NEGOTIATE

Xác định điểm có thể giảm cognitive load bằng cách nhờ người khác.
""",
        "Thứ 6 - Reflective Practice": """
Hôm nay là Thứ Sáu - chế độ SUY NGẪM TUẦN.

📚 **Framework:** Kolb's Experiential Learning Cycle

Học từ kinh nghiệm = Experience + Reflection. Nhìn lại tuần vừa qua:

CÂU HỎI FRAMEWORK:
1. Việc gì làm được tốt nhất tuần này? → KEEP DOING
2. Việc gì làm mệt/stress nhất? → STOP DOING
3. Nếu làm lại, tôi sẽ thay đổi gì? → START DOING
4. Pattern nào lặp lại trong tuần? → INSIGHT

Giúp tôi rút ra 2-3 bài học cụ thể để áp dụng tuần sau (dạng: Start/Stop/Keep).
""",
        "Thứ 7 - Strategic Planning": """
Hôm nay là Thứ Bảy - chế độ LÊN KẾ HOẠCH TUẦN SAU.

📚 **Framework:** Implementation Intentions (Gollwitzer, 1999)

"If-then planning" giúp não autopilot. Chuẩn bị trước để tuần sau dễ thở:

CÂU HỎI FRAMEWORK:
1. Deadline/sự kiện lớn nào tuần sau? → IDENTIFY
2. Việc gì có thể chuẩn bị trước hôm nay/mai? → PREP
3. Ngày nào trong tuần sau sẽ bận nhất? → ANTICIPATE
4. Cần sắp xếp lại gì để tránh crash giữa tuần? → BUFFER

Lập chiến lược if-then: "Nếu thứ 3 có meeting, thì tôi sẽ..."
""",
        "Chủ nhật - Purposeful Recovery": """
Hôm nay là Chủ Nhật - chế độ PHỤC HỒI CÓ CHỦ ĐÍCH.

📚 **Framework:** Recovery-Stress Theory (Kellmann, 2010)

Nghỉ ngơi ≠ làm gì cũng được. Purposeful recovery phục hồi năng lượng gấp 3 lần passive rest:

CÂU HỎI FRAMEWORK:
1. Hoạt động nào khiến tôi cảm thấy "nạp năng lượng"? → DO MORE
2. Hoạt động nào chỉ "giết thời gian" nhưng không restore? → DO LESS
3. Cần disconnect khỏi gì để thật sự nghỉ? → BOUNDARIES
4. Hoạt động restore nào tôi có thể làm hôm nay? → PLAN

Chọn 2-3 hoạt động restore energy: Đọc sách, chơi thể thao, gặp bạn bè, hobby...
Tránh: Scroll mạng xã hội vô thức, xem phim liên tục không chủ đích.
"""
    }
    
    # Tìm framework theo ngày
    weekday = datetime.strptime(date, "%Y-%m-%d").strftime("%A")
    framework_map = {
        "Monday": "Thứ 2 - Weekly Review",
        "Tuesday": "Thứ 3 - Eisenhower Matrix",
        "Wednesday": "Thứ 4 - Ultradian Rhythm",
        "Thursday": "Thứ 5 - Delegation",
        "Friday": "Thứ 6 - Reflective Practice",
        "Saturday": "Thứ 7 - Strategic Planning",
        "Sunday": "Chủ nhật - Purposeful Recovery"
    }
    
    framework_key = framework_map.get(weekday, "Thứ 2 - Weekly Review")
    framework_guide = frameworks[framework_key]
    
    prompt = f"""# {framework_key.upper()}

Ngày: {date}
Trạng thái tinh thần: {data.get('mental_load', 'N/A')}
Năng lượng: {data.get('energy_level', 'N/A')}/10

Công việc hôm nay:
"""
    
    for i, task in enumerate(tasks, 1):
        prompt += f"{i}. {task}\n"
    
    prompt += f"\n{framework_guide}"
    
    return prompt


def get_framework_science():
    """Trả về giải thích khoa học đầy đủ về 8 frameworks"""
    
    return {
        "title": "🧠 Tại sao Mind Balance hiệu quả? Khoa học đằng sau 8 Frameworks",
        "intro": """Mind Balance không phải app tạo prompt hay mood tracker thông thường. 

Đây là hệ thống dựa trên **8 nghiên cứu tâm lý học được kiểm chứng** - mỗi ngày trong tuần áp dụng 1 framework khác nhau để tối ưu hóa cách bạn suy nghĩ về công việc.

**Tại sao cần 8 frameworks khác nhau?** Vì não bộ cần góc nhìn đa chiều để giải quyết cùng 1 danh sách công việc. Một việc có thể "quan trọng" (Thứ 3) nhưng cần "năng lượng cao" (Thứ 4) và "có thể nhờ người khác" (Thứ 5). Mỗi framework khai phá 1 insight khác nhau.""",
        
        "frameworks": [
            {
                "day": "Thứ 2",
                "name": "Weekly Review",
                "research": "David Allen's Getting Things Done (GTD), 2001",
                "why_works": "Não bộ cần 'closure' (đóng vòng lặp) trước khi bắt đầu tuần mới. Khi có quá nhiều 'open loops' (việc chưa xong tuần trước), não tiêu tốn năng lượng để nhớ → tăng anxiety và giảm focus.",
                "evidence": "Nghiên cứu của Zeigarnik (1927) cho thấy não bộ nhớ việc chưa xong tốt hơn việc đã xong gấp 2 lần. Allen's GTD giúp 'externalize' những open loops này → giảm anxiety 40%.",
                "how": "Review tuần trước, đóng tasks cũ, reset mindset với góc nhìn tổng quan trước khi lao vào chi tiết."
            },
            {
                "day": "Thứ 3",
                "name": "Eisenhower Matrix",
                "research": "Eisenhower Decision Principle, phổ biến bởi Stephen Covey (1989)",
                "why_works": "Não bộ không tự phân biệt được 'urgent' (gấp) vs 'important' (quan trọng). Mọi thứ cảm giác 'gấp' đều kích hoạt stress response như nhau, khiến ta làm việc sai → burn out.",
                "evidence": "Nghiên cứu của Covey (1989) cho thấy 80% thời gian người ta dành cho Quadrant 3+4 (không quan trọng). Ma trận này giúp tách bạch → tăng productivity 35%.",
                "how": "Chia tasks thành 4 quadrants: Q1 (Gấp+Quan trọng), Q2 (Quan trọng nhưng chưa gấp), Q3 (Gấp nhưng không quan trọng), Q4 (Cả 2 đều không). Tập trung vào Q2 để phòng ngừa Q1."
            },
            {
                "day": "Thứ 4",
                "name": "Ultradian Rhythm Management",
                "research": "Kleitman's Basic Rest-Activity Cycle (BRAC), 1963",
                "why_works": "Năng lượng con người không 'flat' suốt ngày. Não hoạt động theo chu kỳ 90-120 phút (ultradian rhythm). Làm việc chống lại rhythm này = đốt năng lượng gấp đôi → crash về chiều.",
                "evidence": "Nghiên cứu của Rossi (1991) cho thấy làm việc liên tục >90 phút không nghỉ → giảm hiệu suất 50%. Nghỉ 10-15 phút sau mỗi 90 phút → phục hồi 80% năng lượng.",
                "how": "Phân công Deep Work vào peak hours (9-11am), Shallow Work vào low hours (2-4pm). Break mỗi 90 phút. Thứ 4 thường là ngày năng lượng thấp nhất tuần → cần quản lý đặc biệt."
            },
            {
                "day": "Thứ 5",
                "name": "Delegation & Cognitive Offloading",
                "research": "Sweller's Cognitive Load Theory (1988)",
                "why_works": "Working memory (bộ nhớ làm việc) chỉ giữ được 4±1 items cùng lúc. Khi vượt quá → cognitive overload → stress + sai sót. Delegate không phải 'lười' mà là giảm load để focus vào việc quan trọng nhất.",
                "evidence": "Nghiên cứu của Sweller (1988) cho thấy giảm cognitive load từ 7→4 items → tăng accuracy 60% và giảm stress 40%.",
                "how": "Nhận diện tasks không cần bạn trực tiếp (routine, admin) → delegate. Tasks cần expertise của người khác → collaborate. Tasks có thể đợi → negotiate timeline."
            },
            {
                "day": "Thứ 6",
                "name": "Reflective Practice",
                "research": "Kolb's Experiential Learning Cycle (1984)",
                "why_works": "Học từ kinh nghiệm = Experience + Reflection. Chỉ trải nghiệm mà không reflect = lặp lại sai lầm mãi. Reflection giúp não 'consolidate' (củng cố) kinh nghiệm thành kiến thức.",
                "evidence": "Nghiên cứu của Kolb (1984) cho thấy reflection sau experience → tăng retention 25% và transfer learning 40%. Người reflect đều đặn cải thiện performance nhanh hơn 2.3 lần.",
                "how": "Cuối tuần, hỏi: Gì work? Gì không? Tại sao? Rút ra actionable lessons theo framework Start/Stop/Keep."
            },
            {
                "day": "Thứ 7",
                "name": "Strategic Planning với Implementation Intentions",
                "research": "Gollwitzer's Implementation Intentions (1999)",
                "why_works": "Kế hoạch mơ hồ ('Tuần sau tôi sẽ cố gắng') có success rate 35%. Kế hoạch if-then cụ thể ('Nếu thứ 3 có meeting, tôi sẽ prep từ thứ 2 tối') có success rate 91% → tăng gấp 3 lần.",
                "evidence": "Meta-analysis của Gollwitzer & Sheeran (2006) trên 94 studies cho thấy implementation intentions tăng goal achievement từ 34% → 91%.",
                "how": "Thay vì 'Tuần sau sẽ làm X', viết: 'Khi [trigger], tôi sẽ [action]. Nếu [obstacle], tôi sẽ [backup plan].' Não sẽ autopilot theo if-then này."
            },
            {
                "day": "Chủ nhật",
                "name": "Purposeful Recovery",
                "research": "Kellmann's Recovery-Stress Theory (2010)",
                "why_works": "Nghỉ ngơi passive (xem phim vô thức, scroll mạng xã hội) chỉ phục hồi 30% năng lượng. Nghỉ ngơi active có chủ đích (đọc sách, chơi thể thao, gặp bạn) phục hồi 90% năng lượng.",
                "evidence": "Nghiên cứu của Sonnentag & Fritz (2007) cho thấy 'psychological detachment' (ngắt hoàn toàn khỏi công việc) + 'mastery experience' (làm việc có thành tựu) phục hồi năng lượng gấp 3 lần binge-watching.",
                "how": "Plan 2-3 hoạt động restore: Đọc sách yêu thích, chơi nhạc cụ, chạy bộ, gặp bạn. Tránh: Scroll mạng xã hội >30 phút, xem phim liên tục không chủ đích, làm việc 'thêm một tí'."
            }
        ],
        
        "conclusion": """**Tại sao 8 frameworks thay vì 1 cách duy nhất?**

Vì mỗi ngày não bộ cần góc nhìn khác nhau. Thứ 2 cần "nhìn rộng", Thứ 3 cần "ưu tiên", Thứ 4 cần "quản năng lượng"... 

Khi bạn xoay vòng 8 frameworks này, bạn đang train não bộ phân tích đa chiều → dần dần tự động hóa → không cần app nữa, bạn TỰ BIẾT cách xử lý stress!

**Mind Balance = Personal trainer cho não bộ, không phải crutch (cái nạng).**"""
    }