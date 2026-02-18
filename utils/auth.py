import streamlit as st
import hashlib

# Database user đơn giản
USERS = {
    "demo": {
        "name": "Demo User",
        "password": hashlib.sha256("secret123".encode()).hexdigest()
    },
    "test": {
        "name": "Test User",
        "password": hashlib.sha256("test123".encode()).hexdigest()
    }
}

def check_password(username, password):
    if username in USERS:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return USERS[username]["password"] == hashed_password
    return False

def login_form():
    st.markdown("### 🔐 Đăng nhập")
    
    with st.form("login_form"):
        username = st.text_input("Tên đăng nhập")
        password = st.text_input("Mật khẩu", type="password")
        submit = st.form_submit_button("Đăng nhập")
        
        if submit:
            if check_password(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.name = USERS[username]["name"]
                st.rerun()
            else:
                st.error("❌ Sai tên đăng nhập hoặc mật khẩu")
    
    st.info("""
    **Tài khoản demo:**
    - Username: `demo` / Password: `secret123`
    - Username: `test` / Password: `test123`
    """)

def check_authentication():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    return st.session_state.authenticated

def logout():
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.name = None
    st.rerun()