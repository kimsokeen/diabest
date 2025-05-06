import streamlit as st
from helpers import back_button

def page9():
    back_button(5)
    #st.title("วิธีการใช้งาน")
    ins_path = "assets/วิธีใช้งาน.jpg"
    st.image(ins_path)
