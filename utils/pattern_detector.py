import pandas as pd
import json

def detect_patterns(df):
    """Phát hiện các pattern trong data"""
    patterns = []
    
    if len(df) < 3:
        return ["Chưa đủ dữ liệu để phân tích pattern (cần ít nhất 3 ngày)"]
    
    # Pattern 1: Energy crash
    energy_changes = df['energy_level'].diff()
    big_drops = energy_changes[energy_changes < -3]
    
    if len(big_drops) > 0:
        for idx in big_drops.index:
            date = df.loc[idx, 'date']
            drop = abs(big_drops[idx])
            patterns.append(
                f"⚠️ Năng lượng giảm mạnh {int(drop)} điểm vào ngày {date}"
            )
    
    # Pattern 2: Task overload
    df['task_count'] = df['tasks'].apply(lambda x: len(json.loads(x)))
    avg_tasks = df['task_count'].mean()
    
    overload_days = df[df['task_count'] > avg_tasks * 1.5]
    if len(overload_days) > 0:
        for _, row in overload_days.iterrows():
            patterns.append(
                f"📋 Quá tải công việc vào {row['date']}: {int(row['task_count'])} việc (trung bình: {avg_tasks:.1f})"
            )
    
    # Pattern 3: Poor sleep correlation
    low_sleep_days = df[df['sleep_quality'] <= 2]
    if len(low_sleep_days) > 0:
        avg_energy_low_sleep = low_sleep_days['energy_level'].mean()
        avg_energy_good_sleep = df[df['sleep_quality'] >= 4]['energy_level'].mean()
        
        if avg_energy_good_sleep - avg_energy_low_sleep > 2:
            patterns.append(
                f"😴 Giấc ngủ kém ảnh hưởng đến năng lượng: TB {avg_energy_low_sleep:.1f} vs {avg_energy_good_sleep:.1f}"
            )
    
    # Pattern 4: Consistent low energy days
    low_energy_days = df[df['energy_level'] <= 4]
    if len(low_energy_days) >= 2:
        days = ", ".join(low_energy_days['date'].tolist())
        patterns.append(f"🔋 Các ngày năng lượng thấp: {days}")
    
    if len(patterns) == 0:
        patterns.append("✅ Tuần này khá ổn định, không có pattern đáng lo ngại!")
    
    return patterns