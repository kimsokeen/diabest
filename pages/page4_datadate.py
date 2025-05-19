import streamlit as st
from utils.database import get_results_by_date
from datetime import date
from helpers import back_button
from utils.database import get_user_info
from utils.email_utils import send_report_email

def page4():
    # Ensure username is in session state
    if "username" not in st.session_state:
        st.session_state["username"] = "Guest"

    st.title(f"ผลลัพธ์ของ คุณ{st.session_state.username}")

    # Use selected date from session state if available
    selected_date = st.session_state.get("selected_date", date.today())
    #st.write(f"ผลลัพธ์ในวันที่: {selected_date}")

    # Fetch results for the selected date
    results = get_results_by_date(st.session_state.username, selected_date)

    if results:
        st.write(f"ผลลัพธ์ในวันที่ {selected_date}:")
        for timestamp, result, wound_size, overlay_resized in results:
            st.write(f"- **Time:** {timestamp}, **Result:** {result}, **Wound Size:** {wound_size:.2f} cm²")
            # Display image if overlay_resized is not None
            if overlay_resized:
                st.image(overlay_resized, caption="Wound Overlay Image")
        if st.button("ส่งรายงานไปยังอีเมล"):
            user_info = get_user_info(st.session_state.username)
            if user_info and len(user_info) == 5:
                full_name, age, gender, tel, email = user_info

                summary_lines = []
                for timestamp, result, wound_size, _ in results:
                    summary_lines.append(f"Time: {timestamp}, Result: {result}, Wound Size: {wound_size:.2f} cm²")
                
                summary_text = "\n".join(summary_lines)

                print(f"[DEBUG] Sending email to {email} with result: {summary_text}")

                # Call email utility
                success = send_report_email(
                    to_email=email,
                    full_name=full_name,
                    selected_date=selected_date,
                    result_summary=summary_text,
                    wound_size=sum(r[2] for r in results)  # sum of all wound sizes
                )



                if success:
                    st.success(f"ส่งอีเมลสำเร็จไปยัง {email}")
                else:
                    st.error("เกิดข้อผิดพลาดในการส่งอีเมล")
            else:
                st.error("ไม่สามารถดึงข้อมูลผู้ใช้งานได้")
    else:
        st.write("ไม่มีผลลัพธ์ในวันที่เลือก")

    back_button(5)
