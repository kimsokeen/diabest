# helpers.py
import streamlit as st

def back_button(target_page):
    """
    Function to navigate back to a specific page.
    """
    if st.button("ย้อนกลับ"):
        st.session_state.current_page = f"page{target_page}"  # Update the target page
        # No need for st.experimental_rerun()

# Function to navigate between pages
def navigate(page_name):
    st.session_state['current_page'] = page_name  # Set the current page in session state
    st.rerun()  # Use st.rerun() to refresh the page and show the correct page



