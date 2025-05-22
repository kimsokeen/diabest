import streamlit as st

def page1():
    # Apply custom CSS for background, text, and button styling
    st.markdown("""
        <style>
            body, .stApp {
                background-color: white;
                color: black;
            }
            /* Style Streamlit buttons */
            div.stButton > button {
                background-color: white;
                color: black;
                border: 1px solid black;
                padding: 0.5em 1.5em;
                font-weight: bold;
                border-radius: 6px;
            }
            div.stButton > button:hover {
                background-color: #f0f0f0;
                color: black;
            }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Centered title
        st.markdown("<h1 style='text-align: center;'>Welcome</h1>", unsafe_allow_html=True)

        # Load and display the logo centered
        logo_path = "assets/logo3_square.png"
        try:
            st.image(logo_path, width=300)
        except FileNotFoundError:
            st.error(f"Logo file not found at {logo_path}. Please check the file path.")

        # Add vertical spacing
        st.markdown("<br><br><br>", unsafe_allow_html=True)

    # Button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Get Started"):
            st.session_state['current_page'] = "page2"
            st.stop()
