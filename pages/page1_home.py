import streamlit as st

def page1():
    # Add CSS to set background to white and text to black
    st.markdown("""
        <style>
            body {
                background-color: white;
                color: black;
            }
            .stApp {
                background-color: white;
                color: black;
            }
        </style>
    """, unsafe_allow_html=True)

    # Set the page title
    st.title("Welcome")

    # Load and display the logo
    logo_path = "assets/logo3_square.png"
    try:
        st.image(
            logo_path,
            width=300,  # Set the desired width here (e.g., 300 pixels)
        )
    except FileNotFoundError:
        st.error(f"Logo file not found at {logo_path}. Please check the file path.")

    # Add vertical spacing
    st.markdown("<br><br><br>", unsafe_allow_html=True)

    # Center the button horizontally using columns
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Get Started"):
            st.session_state['current_page'] = "page2"
            st.stop()
