import streamlit as st
from helpers import navigate
from helpers import back_button

# Function to handle chatting with the doctor
def page7():
    back_button(5)
    st.title("Talk to Doctor")
    st.write("Chat with our experts")
    
    chat_history = st.session_state.get("chat_history", [])
    
    for message in chat_history:
        st.write(f"{message['sender']}: {message['content']}")
    
    user_input = st.text_input("Your message")
    if st.button("Send"):
        chat_history.append({"sender": "User", "content": user_input})
        st.session_state.chat_history = chat_history
        st.write(f"You: {user_input}")
