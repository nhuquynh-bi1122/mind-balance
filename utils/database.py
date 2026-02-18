import sqlite3
import pandas as pd
from datetime import datetime
import json

def get_db_path(username):
    return f"data/{username}.db"

def init_database(username):
    conn = sqlite3.connect(get_db_path(username))
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS daily_checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT UNIQUE,
            mental_load TEXT,
            energy_level INTEGER,
            pressure_source TEXT,
            sleep_quality INTEGER,
            tasks TEXT,
            task_feeling TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # BẢNG MỚI: Lưu metadata của tasks
    conn.execute("""
        CREATE TABLE IF NOT EXISTS task_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            checkin_date TEXT,
            task_name TEXT,
            estimated_time INTEGER,
            priority TEXT,
            task_type TEXT,
            FOREIGN KEY (checkin_date) REFERENCES daily_checkins(date)
        )
    """)
    
    # BẢNG MỚI: Lưu lịch đã tạo
    conn.execute("""
        CREATE TABLE IF NOT EXISTS daily_schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            checkin_date TEXT UNIQUE,
            work_start TEXT,
            work_end TEXT,
            schedule_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (checkin_date) REFERENCES daily_checkins(date)
        )
    """)
    
    conn.commit()
    conn.close()

def save_checkin(username, data):
    conn = sqlite3.connect(get_db_path(username))
    
    try:
        conn.execute("""
            INSERT OR REPLACE INTO daily_checkins 
            (date, mental_load, energy_level, pressure_source, 
             sleep_quality, tasks, task_feeling)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data['date'],
            data['mental_load'],
            data['energy_level'],
            data['pressure_source'],
            data['sleep_quality'],
            json.dumps(data['tasks'], ensure_ascii=False),
            data['task_feeling']
        ))
        conn.commit()
        return True
    except Exception as e:
        print(f"Lỗi: {e}")
        return False
    finally:
        conn.close()

def save_task_metadata(username, date, tasks_meta):
    """Lưu metadata của tasks (time, priority, type)"""
    conn = sqlite3.connect(get_db_path(username))
    
    try:
        # Xóa metadata cũ của ngày này
        conn.execute("DELETE FROM task_metadata WHERE checkin_date = ?", (date,))
        
        # Insert metadata mới
        for task in tasks_meta:
            conn.execute("""
                INSERT INTO task_metadata 
                (checkin_date, task_name, estimated_time, priority, task_type)
                VALUES (?, ?, ?, ?, ?)
            """, (
                date,
                task['name'],
                task['estimated_time'],
                task['priority'],
                task['task_type']
            ))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Lỗi save_task_metadata: {e}")
        return False
    finally:
        conn.close()

def get_task_metadata(username, date):
    """Lấy metadata của tasks cho 1 ngày"""
    conn = sqlite3.connect(get_db_path(username))
    
    query = """
        SELECT * FROM task_metadata 
        WHERE checkin_date = ?
        ORDER BY id
    """
    
    df = pd.read_sql_query(query, conn, params=(date,))
    conn.close()
    
    return df

def save_schedule(username, date, work_start, work_end, schedule_data):
    """Lưu lịch đã tạo"""
    conn = sqlite3.connect(get_db_path(username))
    
    try:
        conn.execute("""
            INSERT OR REPLACE INTO daily_schedules 
            (checkin_date, work_start, work_end, schedule_json)
            VALUES (?, ?, ?, ?)
        """, (
            date,
            work_start,
            work_end,
            json.dumps(schedule_data, ensure_ascii=False)
        ))
        conn.commit()
        return True
    except Exception as e:
        print(f"Lỗi save_schedule: {e}")
        return False
    finally:
        conn.close()

def get_schedule(username, date):
    """Lấy lịch của 1 ngày"""
    conn = sqlite3.connect(get_db_path(username))
    
    cursor = conn.execute(
        "SELECT * FROM daily_schedules WHERE checkin_date = ?", 
        (date,)
    )
    result = cursor.fetchone()
    conn.close()
    
    return result

def get_checkin_today(username):
    conn = sqlite3.connect(get_db_path(username))
    today = datetime.now().strftime("%Y-%m-%d")
    
    cursor = conn.execute(
        "SELECT * FROM daily_checkins WHERE date = ?", 
        (today,)
    )
    result = cursor.fetchone()
    conn.close()
    
    return result

def get_week_data(username):
    conn = sqlite3.connect(get_db_path(username))
    
    query = """
        SELECT * FROM daily_checkins 
        ORDER BY date DESC 
        LIMIT 7
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    return df

# PLAYBOOK FUNCTIONS
def init_playbook_table(username):
    """Tạo bảng playbook nếu chưa có"""
    conn = sqlite3.connect(get_db_path(username))
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS playbook (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_title TEXT,
            trigger TEXT,
            action TEXT,
            tested_week TEXT,
            result TEXT,
            status TEXT DEFAULT 'testing',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def save_playbook_rule(username, rule_data):
    """Lưu rule vào playbook"""
    conn = sqlite3.connect(get_db_path(username))
    
    try:
        conn.execute("""
            INSERT INTO playbook 
            (rule_title, trigger, action, tested_week, result, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            rule_data['rule_title'],
            rule_data['trigger'],
            rule_data['action'],
            rule_data['tested_week'],
            rule_data['result'],
            rule_data['status']
        ))
        conn.commit()
        return True
    except Exception as e:
        print(f"Lỗi: {e}")
        return False
    finally:
        conn.close()

def get_all_playbook_rules(username):
    """Lấy tất cả rules"""
    conn = sqlite3.connect(get_db_path(username))
    
    query = """
        SELECT * FROM playbook 
        ORDER BY created_at DESC
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    return df

def update_rule_status(username, rule_id, new_status, new_result=None):
    """Cập nhật status của rule"""
    conn = sqlite3.connect(get_db_path(username))
    
    try:
        if new_result:
            conn.execute("""
                UPDATE playbook 
                SET status = ?, result = ?
                WHERE id = ?
            """, (new_status, new_result, rule_id))
        else:
            conn.execute("""
                UPDATE playbook 
                SET status = ?
                WHERE id = ?
            """, (new_status, rule_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Lỗi: {e}")
        return False
    finally:
        conn.close()

def delete_playbook_rule(username, rule_id):
    """Xóa rule"""
    conn = sqlite3.connect(get_db_path(username))
    
    try:
        conn.execute("DELETE FROM playbook WHERE id = ?", (rule_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Lỗi: {e}")
        return False
    finally:
        conn.close()