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

    # Your existing layout code below
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("<h1 style='text-align: center;'>Welcome</h1>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        logo_path = "assets/logo3_square.png"
        try:
            st.image(logo_path, width=300)
        except FileNotFoundError:
            st.error(f"Logo file not found at {logo_path}. Please check the file path.")
        st.markdown("<br><br>", unsafe_allow_html=True)

    bcol1, bcol2, bcol3, bcol4, bcol5 = st.columns([1, 1, 1, 1, 1])
    with bcol3:
        if st.button("Get Started"):
            st.session_state['current_page'] = "page2"
            st.stop()
