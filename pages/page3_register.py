import streamlit as st
from utils.auth import create_account  # Import account creation function

def page3():
    st.title("สร้างบัญชี")

    # Input fields for account creation
    username = st.text_input("ชื่อบัญชี")
    password = st.text_input("รหัสผ่าน", type="password")
    full_name = st.text_input("ชื่อ-นามสกุล")
    age = st.number_input("อายุ", min_value=0, step=1)
    gender = st.selectbox("เพศ", ["Male", "Female", "Other"])
    tel = st.text_input("เบอร์โทรศัพท์")

    # Create account button
    if st.button("สร้างบัญชี"):
        if username and password and full_name and gender and tel:  # Ensure all required fields are filled
            if create_account(username, password, full_name, age, gender, tel):
                st.success("Account successfully created!")
                st.session_state.current_page = "page2"  # Redirect to login page
                st.rerun()  # Refresh app
            else:
                st.error("ไม่สามารถสร้างบัญชีได้ ชื่อนีถูกใช้แล้ว")
        else:
            st.error("โปรดใส่ข้อมูลให้ครบถ้วน")

    # Back button
    if st.button("กลับ"):
        st.session_state.current_page = "page2"  # Go back to login page
        st.rerun()