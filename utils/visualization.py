import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.database import get_latest_results

def display_wound_chart(username):
    results = get_latest_results(username, limit=100)  # ดึงข้อมูลล่าสุด 100 รายการเพื่อให้แน่ใจว่ามีข้อมูล 14 วัน

    if results:
        # แปลงข้อมูลเป็น DataFrame
        data = {"Date": [], "Wound Size (cm²)": []}
        for result in results:
            timestamp, _, wound_size = result
            date = timestamp.split(" ")[0]  # ดึงแค่วันที่ (YYYY-MM-DD)
            data["Date"].append(date)
            data["Wound Size (cm²)"].append(wound_size)

        df = pd.DataFrame(data)
        df["Date"] = pd.to_datetime(df["Date"])

        # เก็บเฉพาะค่าล่าสุดของแต่ละวัน
        df = df.sort_values(by="Date").drop_duplicates(subset="Date", keep="last")

        # เก็บเฉพาะ 14 วันล่าสุด
        df = df.tail(14)

        # วาดแผนภูมิแท่ง
        fig, ax = plt.subplots(figsize=(5, 4))  # ปรับขนาดให้เล็กลง
        ax.bar(df["Date"].dt.strftime("%Y-%m-%d"), df["Wound Size (cm²)"], color="skyblue")
        ax.set_xlabel("วันที่")
        ax.set_ylabel("ขนาดแผล (cm²)")
        ax.set_title("การเปลี่ยนแปลงขนาดแผลในช่วง 14 วันล่าสุด")
        ax.tick_params(axis='x', rotation=45)

        st.pyplot(fig)
    else:
        st.info("ยังไม่มีข้อมูลขนาดแผล กรุณาอัปโหลดรูปภาพเพื่อตรวจวัดขนาดแผล")