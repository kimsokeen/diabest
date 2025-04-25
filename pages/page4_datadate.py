import streamlit as st
from utils.database import get_results_by_date
from datetime import date
from helpers import back_button

def page4():
    # Ensure username is in session state
    if "username" not in st.session_state:
        st.session_state["username"] = "Guest"

    st.title(f"Results for {st.session_state.username}")

    # Use selected date from session state if available
    selected_date = st.session_state.get("selected_date", date.today())
    st.write(f"Selected Date: {selected_date}")

    # Fetch results for the selected date
    results = get_results_by_date(st.session_state.username, selected_date)

    if results:
        st.write(f"Results for {selected_date}:")
        for timestamp, result, wound_size, overlay_resized in results:
            st.write(f"- **Time:** {timestamp}, **Result:** {result}, **Wound Size:** {wound_size:.2f} cm²")
            # Display image if overlay_resized is not None
            if overlay_resized:
                st.image(overlay_resized, caption="Wound Overlay Image")
    else:
        st.write("No results found for the selected date.")

    back_button(5)
