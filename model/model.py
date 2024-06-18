# app.py

import streamlit as st
from PIL import Image
import torch
from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer
import os

# Load the pre-trained model, feature extractor, and tokenizer
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTFeatureExtractor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


def generate_caption(image):
    image = Image.open(image).convert("RGB")

    # Resize the image if it's too large
    max_size = (800, 800)
    image.thumbnail(max_size, Image.LANCZOS)

    pixel_values = feature_extractor(images=image, return_tensors="pt").pixel_values.to(device)

    # Generate captions
    output_ids = model.generate(pixel_values, max_length=16, num_beams=4)
    caption = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return caption


st.title("Image Captioning with Transformers")
st.write("Upload an image to generate a caption.")

uploaded_file = st.file_uploader("Choose an image...", type="jpg")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Generating caption...")
    caption = generate_caption(uploaded_file)
    st.write(f"Caption: {caption}")
