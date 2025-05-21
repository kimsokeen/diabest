import streamlit as st
from utils.database import get_user_info
from helpers import navigate
from helpers import back_button

def page8():
    back_button(5)
    st.title("User Account")

    user_info = get_user_info(st.session_state.username)
    if user_info:
        # Unpack values safely
        full_name, age, gender, tel, email = user_info

        st.write(f"**Full Name**: {full_name}")
        st.write(f"**Age**: {age}")
        st.write(f"**Gender**: {gender}")
        st.write(f"**Tel. Number**: {tel}")
        st.write(f"**Email**: {email}")

        if st.button("Edit"):
            st.write("Edit functionality not implemented yet.")
    else:
        st.write("No user info found")
