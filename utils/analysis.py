import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import get_custom_objects
from PIL import Image
import cv2
import traceback
import streamlit as st
import os
import sqlite3
import matplotlib.pyplot as plt

# Register IoU metric as a custom object for Keras
@tf.keras.utils.register_keras_serializable()
def iou_metric(y_true, y_pred):
    intersection = tf.reduce_sum(tf.minimum(y_true, y_pred))
    union = tf.reduce_sum(tf.maximum(y_true, y_pred))
    return intersection / union

# Dice loss function (for segmentation)
def dice_loss(y_true, y_pred):
    smooth = 1e-6  # Smoothing constant to avoid division by zero
    intersection = tf.reduce_sum(tf.multiply(y_true, y_pred))
    union = tf.reduce_sum(y_true) + tf.reduce_sum(y_pred)
    dice = (2. * intersection + smooth) / (union + smooth)
    return 1 - dice  # Return 1 - Dice coefficient for loss

# Load pre-trained models for classification and segmentation
try:
    model = load_model(
        r'models/mobilenet_model1.h5'
    )
    print("Classification model loaded successfully.")
    print(model.summary())  # Debug: Print model summary
except Exception as e:
    print("Error loading classification model.")
    traceback.print_exc()

try:
    segmentation_model = load_model(
        r'C:\keen\project\project\project\models\foot_ulcer_model_mobilenet.keras',
        custom_objects={'iou_metric': iou_metric, 'dice_loss': dice_loss}
    )

    print("Segmentation model loaded successfully.")
except Exception as e:
    print("Error loading segmentation model.")
    traceback.print_exc()

def analyze_colors(image, mask, color_thresholds):
    """
    Analyze the colors (red, yellow, black, white) in the wound region and the whole image.
    """
    # Create an empty dictionary to store the color areas
    color_areas = {color: {"wound": 0, "whole_image": 0} for color in color_thresholds}

    # Total image area
    total_area = image.shape[0] * image.shape[1]

    # Iterate over each color threshold to analyze
    for color, (lower, upper) in color_thresholds.items():
        # Create a mask for the color
        color_mask = cv2.inRange(image, lower, upper)
        
        # Apply the color mask to the wound region (using the provided mask)
        wound_masked = cv2.bitwise_and(color_mask, color_mask, mask=mask.astype(np.uint8))

        # Calculate the area of the color in the wound region
        color_areas[color]["wound"] = np.sum(wound_masked) / 255.0

        # Calculate the area of the color in the whole image
        color_areas[color]["whole_image"] = np.sum(color_mask) / 255.0

    return color_areas, total_area

def resize_and_pad(image, target_size=(512, 512)):
    """
    Resize the image to fit within the target size while preserving the aspect ratio,
    and pad the remaining area with black pixels.
    """
    original_size = image.size  # (width, height)
    target_width, target_height = target_size

    # Calculate the aspect ratio
    aspect_ratio = original_size[0] / original_size[1]

    # Determine the new dimensions to fit within the target size
    if aspect_ratio > 1:  # Width is greater than height
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
    else:  # Height is greater than or equal to width
        new_height = target_height
        new_width = int(target_height * aspect_ratio)

    # Resize the image while preserving the aspect ratio
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Create a new black image of the target size
    padded_image = Image.new("RGB", (target_width, target_height), (0, 0, 0))

    # Calculate padding offsets to center the resized image
    x_offset = (target_width - new_width) // 2
    y_offset = (target_height - new_height) // 2

    # Paste the resized image onto the padded image
    padded_image.paste(resized_image, (x_offset, y_offset))

    return padded_image

from PIL import Image
import numpy as np

def resize_and_split_image(image):
    # Resize and pad the image to 512x512 (preserving aspect ratio)
    padded_image = resize_and_pad(image, target_size=(512, 512))

    # Convert the padded image to a numpy array
    image_array = np.array(padded_image)

    # Get the new dimensions of the padded image
    width, height = padded_image.size

    # Calculate grid size (3x3 grid)
    grid_size = height // 3  # 512 / 3 = 170 (approximately)

    # Define the coordinates for the bottom-right grid
    x_start = 2 * grid_size
    y_start = 2 * grid_size

    # Color the bottom-right grid with black
    for y in range(y_start, height):
        for x in range(x_start, width):
            image_array[y, x] = [0, 0, 0]  # RGB black color

    # Extract the bottom-right grid (9th grid)
    bottom_right_grid = padded_image.crop((x_start, y_start, width, height))

    # Convert the modified numpy array back to an image
    padded_image = Image.fromarray(image_array)


    return padded_image, np.array(bottom_right_grid)

def find_coin_radius(image):
    try:
        # Convert image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Thresholding or edge detection if needed (add debug logs for threshold values)
        _, threshold_image = cv2.threshold(gray_image, 120, 255, cv2.THRESH_BINARY)

        # Detect circles (Hough Transform or other methods)
        circles = cv2.HoughCircles(threshold_image, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30, param1=50, param2=30, minRadius=10, maxRadius=50)

        # Debugging: Show circles detected (if any)
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            max_radius = 0  # Initialize the variable to track the max radius

            # Loop through detected circles and draw them
            for (x, y, r) in circles:
                cv2.circle(image, (x, y), r, (0, 255, 0), 4)  # Draw circle
                max_radius = max(max_radius, r)  # Update max_radius with the largest found radius
            
            # Show the image with circles drawn
            st.image(image, caption="Detected Circles", width = 150)

            return max_radius  # Return the largest radius
        else:
            st.write("No circles detected.")
            return None
    except Exception as e:
        st.write(f"Error in find_coin_radius: {e}")
        return None


def overlay_color_highlights(image, mask, color_thresholds):
    """
    Highlight the colors (red, white-yellow, black) in the wound region with the color mask overlays.
    """
    highlighted_image = image.copy()

    # Iterate over each color threshold
    for color, (lower, upper) in color_thresholds.items():
        # Create a mask for the color
        color_mask = cv2.inRange(image, lower, upper)

        # Highlight the color regions in the image with specific colors
        if color == "Red":
            highlighted_image[color_mask > 0] = [0, 255, 0]  # Green for Red
        elif color == "White_Yellow":
            highlighted_image[color_mask > 0] = [255, 255, 0]  # Yellow for White-Yellow
        elif color == "Black":
            highlighted_image[color_mask > 0] = [0, 255, 0]  # Green for Black (as per your request)

    return highlighted_image

def preprocess_segmentation_output(segmentation_output, target_size=(512, 512), threshold=0.5):
    """
    Preprocess the segmentation output:
    - Resize to target size
    - Threshold the output to make it binary (0 or 1)
    """
    # Resize segmentation output to match the input image size
    resized_output = cv2.resize(segmentation_output, target_size, interpolation=cv2.INTER_LINEAR)

    # Apply thresholding to make the segmentation mask binary
    _, binary_mask = cv2.threshold(resized_output, threshold, 1, cv2.THRESH_BINARY)

    return binary_mask


def analyze_colors_and_generate_masks(wound_only_array):
    """ 
    Analyze colors in the wound and generate masks for each color.
    """
    # Define color ranges in HSV
    color_ranges = {
        "Red": ([0, 30, 30], [5, 255, 255]),  # Expanding H to 50 and lowering S threshold
        "White_Yellow": ([0, 50, 100], [50, 255, 255]), # Combined White and Yellow color
        "Black": ([0, 0, 0], [160, 160, 160]),             # Black color
    }

    # Convert image to HSV
    hsv_image = cv2.cvtColor(wound_only_array, cv2.COLOR_RGB2HSV)
    color_analysis = {}
    color_masks = {}

    # Track pixels that have already been accounted for in previous masks
    accounted_pixels = np.zeros_like(hsv_image[:, :, 0], dtype=bool)

    # Analyze each color range
    for color_name, (lower, upper) in color_ranges.items():
        lower_bound = np.array(lower, dtype=np.uint8)
        upper_bound = np.array(upper, dtype=np.uint8)
        
        # Create a mask for the current color
        mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

        # Convert the mask to a boolean array
        mask = mask.astype(bool)

        # Only count pixels that haven't been accounted for in previous masks
        mask = mask & ~accounted_pixels

        # Mark these pixels as accounted for
        accounted_pixels |= mask

        # Calculate the area in the wound region (non-zero pixels in mask)
        area = np.sum(mask)  # Count non-zero pixels
        total_pixels = np.prod(wound_only_array.shape[:2])  # Total number of pixels in the image
        percentage = (area / total_pixels) * 100

        # Save color analysis and mask
        color_analysis[color_name] = round(percentage, 2)
        color_masks[color_name] = mask

    return color_analysis, color_masks


def analyze_image(image):
    try:
        
        # Resize and split image into 9 grids (Check)
        resized_padded_image, middle_grid = resize_and_split_image(image)
        if resized_padded_image is None or middle_grid is None:
            raise ValueError("Image processing failed, unable to resize and split the image correctly.")
        
        # Now process middle grid for coin detection (Check if radius is detected)
        radius = find_coin_radius(middle_grid)
        if radius is None:
            raise ValueError("Coin radius detection failed in the middle grid.")

        # Resize for classification model
        classification_input = resized_padded_image.resize((224, 224))

        # Convert to numpy array and normalize (if required by the model)
        classification_input = np.array(classification_input).astype(np.float32) / 255.0  # Normalize to [0, 1]

        # Add batch dimension
        classification_input = np.expand_dims(classification_input, axis=0)

        # Classification Prediction
        classification_prediction = model.predict(classification_input)
        probability = classification_prediction[0][0]  # Probability for class "normal"

        # Interpret the prediction
        predicted_class = "Diabetic Foot" if probability < 0.75 else "Non-Diabetic Foot"

        if predicted_class == "Diabetic Foot":
            # Detect coin radius from the middle grid (change from bottom-right to middle)
            pixels_per_cm = find_coin_radius(middle_grid)

            if pixels_per_cm:
                # Resize for segmentation model
                segmentation_input = resized_padded_image.resize((256, 256))

                # Convert to numpy array and normalize (if required by the model)
                segmentation_input = np.array(segmentation_input).astype(np.float32) / 255.0  # Normalize to [0, 1]

                # Add batch dimension
                segmentation_input = np.expand_dims(segmentation_input, axis=0)

                # Segmentation Prediction
                segmentation_output = segmentation_model.predict(segmentation_input)[0, :, :, 0]

                # Lower threshold if needed
                mask = preprocess_segmentation_output(segmentation_output)

                # Extract wound region
                original_image_array = np.array(resized_padded_image).astype(np.uint8)
                mask_expanded = np.expand_dims(mask, axis=-1)
                mask_expanded = np.repeat(mask_expanded, 3, axis=-1)
                wound_only_image = np.where(mask_expanded, original_image_array, [0, 0, 225])

                # Overlay mask
                overlay = np.where(mask_expanded, original_image_array, original_image_array * 0.7)

                # Perform color analysis
                color_analysis, color_masks = analyze_colors_and_generate_masks(np.array(wound_only_image).astype(np.uint8))

                # Total area of the image and the wound
                total_image_area = original_image_array.size  # Total number of pixels
                total_wound_area = np.sum(mask)  # Total pixels in the wound

                # Ensure wound_size is a valid numeric value (int or float)
                wound_size = float(total_wound_area) / (pixels_per_cm ** 2)  # Convert to cm²

                # Generate color highlights
                color_highlights = {}
                highlight_colors = {
                    "Red": [255, 0, 0],   # Red in RGB
                    "White_Yellow": [255, 255, 0], # Combined white-yellow (yellow)
                    "Black": [0, 255, 0],  # Green for Black
                }

                color_percentages = {}
                for color_name, highlight_color in highlight_colors.items():
                    if color_name in color_masks:
                        # Masked color area within the wound
                        color_in_wound = np.sum(color_masks[color_name] * mask)  # Only color pixels in the wound
                        color_in_wound_percentage = (color_in_wound / total_wound_area) * 100 if total_wound_area > 0 else 0

                        # Save wound color percentages
                        color_percentages[f"{color_name} (Wound)"] = color_in_wound_percentage

                        # Highlight image generation
                        highlight_image = np.zeros_like(original_image_array)
                        highlight_image[color_masks[color_name] > 0] = highlight_color
                        color_highlights[color_name] = Image.fromarray(highlight_image)

                # Adjust "Other" category to make percentages sum to 100% in the wound area
                total_colored_area = sum(color_percentages.values())
                if total_colored_area < 100.0:
                    color_percentages["Other (Wound)"] = 100.0 - total_colored_area
                else:
                    color_percentages["Other (Wound)"] = 0.0

                return predicted_class, probability, wound_size, overlay, wound_only_image, color_percentages, color_highlights
        
        else:
            return predicted_class, probability, 0, None, None, {}, {}

    except Exception as e:
        st.error(f"Error in analyze_image: {traceback.format_exc()}")
        return None, None, None, None, None, {}, {}

    
def display_color_highlights(color_highlights):
    """
    Display color highlights in a row, ensure all 3 colors are shown.
    """
    st.write("### Color Highlights")
    col1, col2, col3 = st.columns(3)  # Create 3 columns for 3 colors

    color_order = ["Red", "White_Yellow", "Black"]
    highlight_images = [color_highlights.get(color, None) for color in color_order]

    # Display all 3 images
    with col1:
        if highlight_images[0]:
            st.image(highlight_images[0], caption="Red Highlight", width = 180)
    with col2:
        if highlight_images[1]:
            st.image(highlight_images[1], caption="White-Yellow Highlight", width = 180)
    with col3:
        if highlight_images[2]:
            st.image(highlight_images[2], caption="Black Highlight (Green)", width = 180)


# Function to save the analysis result including the selected date
def save_result_to_db(username, result, wound_size, selected_date, overlay_resized):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Convert overlay image to binary (if available)
        overlay_bytes = None
        if overlay_resized is not None:
            _, buffer = cv2.imencode('.png', overlay_resized)
            overlay_bytes = buffer.tobytes()

        # Insert the data into the database
        cursor.execute(""" 
            INSERT INTO results (username, timestamp, result, wound_size, overlay_resized)
            VALUES (?, ?, ?, ?, ?) 
        """, (username, selected_date, result, wound_size, overlay_bytes))

        conn.commit()
        conn.close()
        print("Result saved successfully.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
