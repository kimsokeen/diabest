import streamlit as st

# Function to display the "Get Started" page
def page1():
    # Set the page title
    st.title("Welcome")

    # Load and display the logo
    logo_path = r"C:\keen\project\project\project\assets\logo3_square.png"
    try:
        st.image(
            logo_path,
            width=300,  # Set the desired width here (e.g., 300 pixels)
        )
    except FileNotFoundError:
        st.error(f"Logo file not found at {logo_path}. Please check the file path.")

    # Add vertical spacing
    st.markdown("<br><br><br>", unsafe_allow_html=True)

    # Center the button horizontally
    col1, col2, col3 = st.columns([1, 1, 1])  # Equal spacing for centering
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)  # Extra spacing before the button
        if st.button("Get Started"):
            # Update session state and simulate page reload
            st.session_state['current_page'] = "page2"  # Navigate to the Login page
            st.stop()  # Stop the execution of the current script
