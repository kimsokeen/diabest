import streamlit as st
from utils.auth import login  # Import login function

def page2():
    st.title("เข้าสู่ระบบ")

    # Input fields for login
    username = st.text_input("ชื่อบัญชี")
    password = st.text_input("รหัสผ่าน", type="password")

    # Login button
    if st.button("เข้าสู่ระบบ"):
        if username and password:  # Ensure inputs are provided
            if login(username, password):  # Check credentials
                st.success("Login successful! Redirecting...")
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state.current_page = "page5"  # Go to Dashboard
                st.rerun()  # Refresh page
            else:
                st.error("รหัสผ่านไม่ถูกต้อง")
        else:
            st.error("โปรดใส่ข้อมูลให้ครบถ้วน")

    # Create Account button
    if st.button("สร้างบัญชี"):
        st.session_state.current_page = "page3"
        st.rerun()

    # Back button to go to Home page
    if st.button("ย้อนกลับ"):
        st.session_state.current_page = "page1"
        st.rerun()
