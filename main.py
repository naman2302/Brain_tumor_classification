import streamlit as st
from utils import set_background
from PIL import Image
from tensorflow import keras
from classifier import classifier
from io import BytesIO
import base64

# Page Config
st.set_page_config(
    page_title='Brain Tumor Classification',
    layout='centered'
)

# Set Background Image
set_background('utils/bg.jpg')

# Enhanced CSS for better UI
st.markdown(
    """
    <style>
    /* Title Styling */
    .title {
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        color: #d5a6ff;
        text-shadow: 3px 3px 8px rgba(213, 166, 255, 0.8);
        margin-top: -30px;
        letter-spacing: 1px;
        white-space: nowrap;
    }

    /* Subheading Styling */
    .header {
        text-align: center;
        font-size: 22px;
        font-weight: 600;
        color: #ffffff;
        background: rgba(0, 0, 0, 0.6);
        padding: 10px 20px;
        border-radius: 10px;
        display: inline-block;
        margin-top: 20px; /* Added space from title */
        margin-bottom: 35px; /* More space before input box */
    }

    /* File Uploader Styling */
    .stFileUploader {
        border: 2px solid #d5a6ff !important;
        border-radius: 12px;
        background-color: rgba(50, 50, 50, 0.7);
        color: #fff !important;
        text-align: center !important;
    }
    .stFileUploader:hover {
        border-color: #ff7fff !important;
        box-shadow: 0px 0px 15px rgba(255, 127, 255, 0.7);
    }

    /* Image Preview */
    .result-image {
        width: 80%;
        border-radius: 15px;
        margin-top: 20px;
    }

    /* Prediction Result */
    .result-text {
        font-size: 28px;
        font-weight: bold;
        color: #fff;
        background: rgba(0, 0, 0, 0.5);
        padding: 12px;
        border-radius: 10px;
        display: inline-block;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title & Heading
st.markdown('<div class="title">🧠 Brain Tumor Classification</div>', unsafe_allow_html=True)
st.markdown('<div class="header">Upload an MRI scan to classify it as Brain Tumor or No Brain Tumor.</div>', unsafe_allow_html=True)

# File Uploader
file = st.file_uploader("", type=['jpg', 'jpeg', 'png', 'jfif'])

# Load Model
model = keras.models.load_model("Model/model.keras")
class_names = {0: 'No Brain Tumor', 1: 'Brain Tumor'}

if file is not None:
    image = Image.open(file).convert('RGB')
    prediction, score = classifier(image, model, class_names)

    # Convert image to Base64 for inline display
    bufferd = BytesIO()
    image.save(bufferd, format='PNG')
    img_base64 = base64.b64encode(bufferd.getvalue()).decode()

    # Display Classification Results
    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src="data:image/png;base64,{img_base64}" class="result-image"/>
            <div class="result-text">
                <p><strong>Result: {prediction}</strong></p>
                <p style="margin-top:-5px;"><strong>Confidence Score: {score}%</strong></p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
