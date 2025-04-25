import streamlit as st
import datetime
from utils.database import get_latest_results
from helpers import back_button, navigate
from utils.visualization import display_wound_chart

def page5():
    st.markdown("""
        <style>
        body, h1, h2, h3, h4, h5 {
            font-family: 'Segoe UI', sans-serif;
        }

        /* Custom full-height panel inside left column */
        .left-panel-container {
            background-color: #f8f9fa;
            padding: 2rem;
            border-radius: 20px;
            min-height: 100%;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }

        /* Stylish buttons */
        .fancy-btn {
            background: linear-gradient(135deg, #00b4db, #0083b0);
            border: none;
            color: white;
            padding: 0.75rem 1rem;
            font-size: 1.05rem;
            border-radius: 12px;
            cursor: pointer;
            width: 100%;
            transition: all 0.3s ease-in-out;
            box-shadow: 0 4px 14px rgba(0,0,0,0.1);
            margin-top: 1rem;
        }

        .fancy-btn:hover {
            background: linear-gradient(135deg, #0083b0, #00b4db);
            transform: translateY(-2px);
        }

        .stButton > button {
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"<h2>สวัสดี คุณ {st.session_state.get('username', 'Guest')}!</h2>", unsafe_allow_html=True)
    st.markdown("<h4>ยินดีต้อนรับเข้าสู่แอปพลิเคชันตรวจแผลเบาหวาน</h4>", unsafe_allow_html=True)
    st.write(" ")

    # Columns for layout
    left_col, spacer, right_col = st.columns([2, 0.25, 1.75])

    with right_col:
        # This is the box that will cover everything in the left panel
        with st.container(border = True):

            results = get_latest_results(st.session_state.username)
            if results:
                st.write("ผลวิเคราะห์ล่าสุด")
                for r in results[:3]:
                    timestamp = r[0]
                    result = r[1]
                    woundsize = r[2]

                    st.write(f"- วันที่: {timestamp.split()[0]}")
                    st.write(f"ประเภท: {result} {float(woundsize):.2f} cm²")
                    st.write("---")
            else:
                st.info("ไม่พบผลลัพธ์ล่าสุด กรุณาอัปโหลดรูปภาพเพื่อเริ่มการวิเคราะห์")
            
            selected_date = st.date_input("📅 เลือกวันที่:", value=datetime.date.today())
            if selected_date:
                st.session_state["selected_date"] = selected_date.strftime('%Y-%m-%d')

            if st.button("ยืนยันวันที่ต้องการ"):
                st.session_state.current_page = "page4"
                st.rerun()

    with left_col:
        def styled_button(label, key, page):
            st.markdown("""
                <style>
                div.stButton > button {
                    padding: 1.2rem 1rem !important;
                    font-size: 1.1rem !important;
                    border-radius: 10px !important;
                    background-color: #0099cc !important;
                    color: white !important;
                    border: none;
                    box-shadow: 0 3px 10px rgba(0,0,0,0.1);
                    margin-bottom: 0.75rem;
                }
                div.stButton > button:hover {
                    background-color: #007799 !important;
                    transform: translateY(-2px);
                }
                </style>
            """, unsafe_allow_html=True)

            if st.button(label, key=key):
                st.session_state.current_page = page
                st.rerun()

        styled_button("อัพโหลดรูปภาพ", "upload_btn", "page6")
        col1, col2 = st.columns(2)

        with col1:
            styled_button("วิธีใช้งาน", "howto_btn", "page9")
            #styled_button("💬 คุยกับคุณหมอ", "chat_btn", "page7")

        with col2:
            styled_button("บัญชีของคุณ", "account_btn", "page8")

            

        

        
