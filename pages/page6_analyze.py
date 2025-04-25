import streamlit as st
import numpy as np
from PIL import Image
from utils.analysis import analyze_image, save_result_to_db
from helpers import back_button, navigate
from utils.analysis import display_color_highlights
import datetime
import traceback


def page6():
    back_button(5)
    st.title("อัพโหลดรูปภาพ")


    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    # Step 1: File uploader
    uploaded_image = st.file_uploader("อัพโหลดรูปภาพ", type=["jpg", "jpeg", "png"])


    if uploaded_image is not None:
        try:
            # Step 2: Open and convert image to RGB
            image_data = Image.open(uploaded_image).convert("RGB")


            # Debugging: Output image properties
            st.write(f"ขนาดของภาพ: {image_data.size}, Image mode: {image_data.mode}")


            # Resize and display uploaded image
            max_width = 400
            aspect_ratio = image_data.height / image_data.width
            resized_image = image_data.resize((max_width, int(max_width * aspect_ratio)))
            st.image(resized_image, caption="อัพโหลดรูปภาพ", width = 300)  # Display the uploaded image
        except Exception as e:
            st.error("ไม่สามารถอัพโหลดรูปได้")
            st.write(f"Debugging logs: {e}")
            return


        # Step 3: Analyze button logic
        if st.button("ประมวลผล"):
            st.write("เริ่มทำการประมวลผล..")


            try:
                # Call the analyze_image function
                (
                    predicted_class,
                    probability,
                    wound_size,
                    overlay_resized,
                    wound_only_resized,
                    color_analysis,
                    color_highlights,
                ) = analyze_image(image_data)


                # Debugging: Print raw model output and probability
                #st.write(f"Debug: Predicted Class = {predicted_class}")
                #st.write(f"Debug: Probability = {probability}")
                #st.write(f"Debug: Wound Size (pixels) = {wound_size}")


            except ValueError as e:
                st.error(f"Analysis failed: {e}")
                st.write(f"Debugging logs: {e}")
                return
            except Exception as e:
                st.error("Error during analysis. Please try again.")
                st.write(f"Debugging logs: {e}")
                st.write(f"Traceback: {traceback.format_exc()}")
                return


            # Step 4: Display results or handle errors
            if probability is not None and wound_size is not None:
                wound_size_cm = wound_size # Convert pixels to cm²


                # Display classification result and wound size
                st.success(f"ผลการตรวจ: {predicted_class}")
                st.info(f"ขนาดของแผล: {wound_size_cm:.2f} cm²")

                col1, col2 = st.columns(2)

                # Ensure the overlay image is in the correct format
                if overlay_resized is not None:
                    if overlay_resized.dtype != np.uint8:
                        overlay_resized = np.clip(overlay_resized, 0, 255).astype(np.uint8)
                    with col1:
                        st.image(overlay_resized, caption="Overlayed Image", width = 300)
                else:
                    st.error("Error during segmentation. No overlay available.")


                # Display wound area
                if wound_only_resized is not None and wound_only_resized.size > 0:
                    with col2:
                        st.image(wound_only_resized, caption="Wound Area", width = 300)
                else:
                    st.error("ไม่พบแผลเบาหวาน")


                # Display color analysis
                if color_analysis:
                    st.write("### การวิเคราะห์สี")
                    for color, percentage in color_analysis.items():
                        st.write(f"- {color}: {percentage:.2f}%")


                    # Display color highlights
                    if color_highlights:
                        display_color_highlights(color_highlights)


                # Save the results
                    try:
                        save_result_to_db(st.session_state.username, predicted_class, wound_size_cm, timestamp , overlay_resized)
                        st.success("ข้อมูลถูกบันทึกลงในระบบเรียบร้อย")
                    except Exception as e:
                        st.warning(f"Error saving results lol: {e}")


                # Finish button
                if st.button("เสร็จสิ้น"):
                    st.session_state.current_page = 'page5'
            else:
                st.error("Failed to analyze the image. Please try again.")
                st.write("Debugging logs: Check the console for details.")



