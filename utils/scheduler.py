"""
AI Scheduler - Tạo lịch thông minh CHỐNG BURN OUT
Tích hợp 8 frameworks để tối ưu hiệu quả
"""

from datetime import datetime, timedelta

def create_daily_schedule(tasks_with_meta, fixed_schedule, work_start="07:00", work_end="22:00", 
                         energy_level=5, today_framework=""):
    """
    Tạo lịch thông minh với logic chống burn out
    
    Args:
        tasks_with_meta: List[dict] - Tasks với metadata
        fixed_schedule: List[dict] - Lịch cố định [{'start': '07:00', 'end': '11:30', 'name': 'Học trên lớp'}]
        work_start: str - Giờ thức dậy
        work_end: str - Giờ đi ngủ
        energy_level: int - Năng lượng hiện tại (1-10)
        today_framework: str - Framework hôm nay
    
    Returns:
        dict: Full schedule với warnings + suggestions
    """
    
    # Parse time
    day_start = datetime.strptime(work_start, "%H:%M")
    day_end = datetime.strptime(work_end, "%H:%M")
    
    # Parse fixed schedule
    fixed_blocks = []
    for block in fixed_schedule:
        fixed_blocks.append({
            'start': datetime.strptime(block['start'], "%H:%M"),
            'end': datetime.strptime(block['end'], "%H:%M"),
            'name': block['name'],
            'type': 'Fixed'
        })
    
    fixed_blocks.sort(key=lambda x: x['start'])
    
    # Tìm khoảng trống
    free_slots = []
    current_time = day_start
    
    for block in fixed_blocks:
        if current_time < block['start']:
            free_duration = int((block['start'] - current_time).total_seconds() / 60)
            if free_duration >= 30:
                free_slots.append({
                    'start': current_time,
                    'end': block['start'],
                    'duration': free_duration
                })
        current_time = max(current_time, block['end'])
    
    if current_time < day_end:
        free_duration = int((day_end - current_time).total_seconds() / 60)
        if free_duration >= 30:
            free_slots.append({
                'start': current_time,
                'end': day_end,
                'duration': free_duration
            })
    
    total_free_minutes = sum([slot['duration'] for slot in free_slots])
    total_task_time = sum([t['estimated_time'] for t in tasks_with_meta])
    
    # LOGIC CHỐNG BURN OUT
    warnings = []
    suggestions = []
    
    # Chỉ nên làm 70% thời gian rảnh
    effective_free_time = int(total_free_minutes * 0.7)
    
    # Điều chỉnh theo năng lượng
    if energy_level <= 3:
        max_work_time = int(effective_free_time * 0.6)
        warnings.append(f"⚠️ Năng lượng thấp ({energy_level}/10) - Chỉ nên làm {max_work_time//60}h{max_work_time%60}'")
    elif energy_level <= 6:
        max_work_time = int(effective_free_time * 0.8)
    else:
        max_work_time = effective_free_time
    
    # Phát hiện overload
    if total_task_time > max_work_time:
        overload = total_task_time - max_work_time
        warnings.append(f"🔥 BURN OUT ALERT: {total_task_time//60}h{total_task_time%60}' công việc vs {max_work_time//60}h{max_work_time%60}' khả dụng")
        warnings.append(f"⚠️ Cần giảm {overload//60}h{overload%60}' để tránh kiệt sức!")
    
    # Chuẩn hóa key names (database trả về 'task_name' nhưng code cần 'name')
    for task in tasks_with_meta:
        if 'task_name' in task and 'name' not in task:
            task['name'] = task['task_name']
    
    # Phân loại tasks
    deep_work = [t for t in tasks_with_meta if t['task_type'] == 'Deep Work']
    meetings = [t for t in tasks_with_meta if t['task_type'] == 'Meeting']
    shallow = [t for t in tasks_with_meta if t['task_type'] == 'Shallow Work']
    
    priority_map = {'High': 1, 'Medium': 2, 'Low': 3}
    deep_work.sort(key=lambda x: priority_map[x['priority']])
    shallow.sort(key=lambda x: priority_map[x['priority']])
    
    # FRAMEWORK INSIGHTS
    insights = get_framework_insights(today_framework, tasks_with_meta, energy_level)
    suggestions.extend(insights)
    
    # TẠO LỊCH
    schedule = []
    scheduled_tasks = []
    worked_minutes = 0
    
    # Thêm fixed schedule
    for block in fixed_blocks:
        schedule.append({
            'start': block['start'].strftime("%H:%M"),
            'end': block['end'].strftime("%H:%M"),
            'task': block['name'],
            'type': 'Fixed',
            'priority': 'System',
            'color': '#9CA3AF'
        })
    
    # Xếp tasks vào free slots
    for slot in free_slots:
        slot_start = slot['start']
        slot_remaining = slot['duration']
        current_time = slot_start
        hour = slot_start.hour
        
        # Xác định slot type
        if 6 <= hour < 12:
            slot_type = 'morning'
        elif 12 <= hour < 14:
            slot_type = 'lunch'
        elif 14 <= hour < 18:
            slot_type = 'afternoon'
        else:
            slot_type = 'evening'
        
        # Slot buổi trưa
        if slot_type == 'lunch':
            lunch_duration = min(45, slot_remaining)
            lunch_end = current_time + timedelta(minutes=lunch_duration)
            schedule.append({
                'start': current_time.strftime("%H:%M"),
                'end': lunch_end.strftime("%H:%M"),
                'task': '🍱 Ăn trưa + nghỉ',
                'type': 'Break',
                'priority': 'System',
                'color': '#10B981'
            })
            current_time = lunch_end
            slot_remaining -= lunch_duration
        
        # Slot buổi sáng - Deep work
        if slot_type == 'morning':
            for task in deep_work[:]:
                if worked_minutes >= max_work_time or slot_remaining < 20:
                    break
                
                task_duration = min(task['estimated_time'], slot_remaining, max_work_time - worked_minutes, 90)
                if task_duration < 20:
                    continue
                
                task_end = current_time + timedelta(minutes=task_duration)
                schedule.append({
                    'start': current_time.strftime("%H:%M"),
                    'end': task_end.strftime("%H:%M"),
                    'task': task['name'],
                    'type': task['task_type'],
                    'priority': task['priority'],
                    'color': '#EF4444' if task['priority'] == 'High' else '#F59E0B'
                })
                
                current_time = task_end
                worked_minutes += task_duration
                slot_remaining -= task_duration
                scheduled_tasks.append(task['name'])
                
                if task_duration >= task['estimated_time']:
                    deep_work.remove(task)
                else:
                    task['estimated_time'] -= task_duration
                
                # Auto break
                if task_duration >= 60 and slot_remaining >= 10:
                    break_end = current_time + timedelta(minutes=10)
                    schedule.append({
                        'start': current_time.strftime("%H:%M"),
                        'end': break_end.strftime("%H:%M"),
                        'task': '☕ Break',
                        'type': 'Break',
                        'priority': 'System',
                        'color': '#10B981'
                    })
                    current_time = break_end
                    slot_remaining -= 10
                break
        
        # Slot chiều/tối - Mix
        if slot_type in ['afternoon', 'evening']:
            # Meetings trước
            for task in meetings[:]:
                if worked_minutes >= max_work_time or slot_remaining < task['estimated_time']:
                    continue
                
                task_end = current_time + timedelta(minutes=task['estimated_time'])
                schedule.append({
                    'start': current_time.strftime("%H:%M"),
                    'end': task_end.strftime("%H:%M"),
                    'task': task['name'],
                    'type': 'Meeting',
                    'priority': task['priority'],
                    'color': '#8B5CF6'
                })
                
                current_time = task_end
                worked_minutes += task['estimated_time']
                slot_remaining -= task['estimated_time']
                scheduled_tasks.append(task['name'])
                meetings.remove(task)
            
            # Shallow work
            for task in shallow[:]:
                if worked_minutes >= max_work_time or slot_remaining < 15:
                    break
                
                task_duration = min(task['estimated_time'], slot_remaining, max_work_time - worked_minutes)
                if task_duration < 15:
                    continue
                
                task_end = current_time + timedelta(minutes=task_duration)
                schedule.append({
                    'start': current_time.strftime("%H:%M"),
                    'end': task_end.strftime("%H:%M"),
                    'task': task['name'],
                    'type': 'Shallow Work',
                    'priority': task['priority'],
                    'color': '#3B82F6' if task['priority'] == 'Low' else '#F59E0B'
                })
                
                current_time = task_end
                worked_minutes += task_duration
                slot_remaining -= task_duration
                scheduled_tasks.append(task['name'])
                
                if task_duration >= task['estimated_time']:
                    shallow.remove(task)
                else:
                    task['estimated_time'] -= task_duration
    
    # Tasks không xếp được
    unscheduled = []
    for task in deep_work + meetings + shallow:
        unscheduled.append(task['name'])
    
    if len(unscheduled) > 0:
        warnings.append(f"⚠️ Không xếp được {len(unscheduled)} tasks: {', '.join(unscheduled)}")
        
        low_priority = [t for t in tasks_with_meta if t['name'] in unscheduled and t['priority'] == 'Low']
        if len(low_priority) > 0:
            suggestions.append(f"💡 Delegate: {', '.join([t['name'] for t in low_priority])}")
    
    schedule.sort(key=lambda x: datetime.strptime(x['start'], "%H:%M"))
    
    stats = {
        'total_tasks': len(tasks_with_meta),
        'scheduled_tasks': len(scheduled_tasks),
        'unscheduled_tasks': len(unscheduled),
        'actual_work_time': worked_minutes,
        'breaks_count': len([s for s in schedule if s['type'] == 'Break'])
    }
    
    return {
        'schedule': schedule,
        'warnings': warnings,
        'suggestions': suggestions,
        'stats': stats
    }


def get_framework_insights(framework_name, tasks, energy_level):
    """Framework-specific insights"""
    insights = []
    
    if "Eisenhower" in framework_name:
        high = len([t for t in tasks if t['priority'] == 'High'])
        if high > 3:
            insights.append(f"📘 Eisenhower: {high} High priority - Có việc nào chỉ 'gấp' không 'quan trọng'?")
    
    elif "Delegation" in framework_name:
        shallow = len([t for t in tasks if t['task_type'] == 'Shallow Work'])
        if shallow > 2:
            insights.append(f"🤝 Delegation: {shallow} Shallow tasks - Ai giúp được không?")
    
    elif "Ultradian" in framework_name:
        deep_time = sum([t['estimated_time'] for t in tasks if t['task_type'] == 'Deep Work'])
        if energy_level <= 5 and deep_time > 120:
            insights.append(f"⚡ Ultradian: Năng lượng {energy_level}/10 với {deep_time//60}h Deep Work - Chia nhỏ!")
    
    elif "Recovery" in framework_name:
        if len(tasks) > 3:
            insights.append(f"😴 Recovery: Ngày nghỉ mà {len(tasks)} tasks - Thực sự CẦN?")
    
    return insights