import streamlit as st

def page1():
    # Load your logo path
    logo_path = "assets/logo3_square.png"

    # Custom HTML and CSS for full centering
    st.markdown(f"""
        <style>
            .center-container {{
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                height: 90vh;
            }}
            .center-container img {{
                width: 300px;
                max-width: 80vw;
                margin-bottom: 30px;
            }}
            .center-container button {{
                padding: 0.7em 2em;
                font-size: 1.1em;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
            }}
            .center-container button:hover {{
                background-color: #45a049;
            }}
        </style>

        <div class="center-container">
            <h1>Welcome</h1>
            <img src="{logo_path}" alt="Logo">
            <form action="/" method="post">
                <button type="submit">Get Started</button>
            </form>
        </div>
    """, unsafe_allow_html=True)

    # Handle the button manually with session state (since HTML form doesn't set Streamlit state)
    if st.query_params.get("start") == "1" or st.button("Get Started"):
        st.session_state['current_page'] = "page2"
        st.stop()
