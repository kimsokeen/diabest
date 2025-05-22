import streamlit as st

def page1():
    # Create three equal-width columns to center the content
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Centered title
        st.markdown("<h1 style='text-align: center;'>Welcome</h1>", unsafe_allow_html=True)

        st.write("")

        # Load and display the logo centered
        logo_path = "assets/logo3_square.png"
        try:
            st.image(logo_path, width=300)
        except FileNotFoundError:
            st.error(f"Logo file not found at {logo_path}. Please check the file path.")

        # Add vertical spacing
        st.markdown("<br><br><br>", unsafe_allow_html=True)

        # Centered button
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        if st.button("Get Started"):
            st.session_state['current_page'] = "page2"
            st.stop()
        st.markdown("</div>", unsafe_allow_html=True)
