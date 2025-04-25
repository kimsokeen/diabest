import streamlit as st
from pages.page1_home import page1
from pages.page2_login import page2
from pages.page3_register import page3
from pages.page4_datadate import page4
from pages.page5_dashboard import page5
from pages.page6_analyze import page6
from pages.page7_chat import page7
from pages.page8_account import page8
from pages.page9_instruction import page9
from utils.database import create_users_table, create_results_table

st.set_page_config(page_title="Personal Assistance App", layout="centered")
create_users_table()
create_results_table()

def main():
    

    # Set default page
    if "current_page" not in st.session_state:
        st.session_state.current_page = "page1"

    # Page navigation
    if st.session_state.current_page == "page1":
        page1()
    elif st.session_state.current_page == "page2":
        page2()
    elif st.session_state.current_page == "page3":
        page3()
    elif st.session_state.current_page == "page4":
        page4()
    elif st.session_state.current_page == "page5":
        page5()
    elif st.session_state.current_page == "page6":
        page6()
    elif st.session_state.current_page == "page7":
        page7()
    elif st.session_state.current_page == "page8":
        page8()
    elif st.session_state.current_page == "page9":
        page9()

if __name__ == "__main__":
    main()
