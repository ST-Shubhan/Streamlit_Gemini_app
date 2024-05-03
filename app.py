
import google.generativeai as genai
from PIL import Image
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image[0], prompt])
    return response.text


def input_image_setup(uploaded_file):

    if uploaded_file is not None:

        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


st.set_page_config(page_title="Smart Plant Disease Analyzer using Gemini ")

st.header("🌿 Smart Plant Disease Analyzer using Gemini 👨🏻‍💻")
input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader(
    "Choose an image...", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit = st.button("Tell me about the image")


input_prompt = """
You are an agricultural expert system designed to analyze images of tomato plants and provide detailed information to help farmers identify and address plant diseases or issues.

Given:
- An image of a tomato plant showing potential disease symptoms or issues
- Additional context from the farmer about the plant's condition, growth stage, and environment

Your task is to generate a comprehensive guide for the farmer with the following sections:

Disease Identification:
Examine the image and identify the most likely disease or issue affecting the tomato plant based on the visual symptoms observed.

Symptom Breakdown:
Describe the key symptoms visible in the image (e.g., leaf discoloration, spots, wilting) and explain how they relate to the identified disease or issue.

Preventative Measures:
Provide actionable steps the farmer can take to prevent the spread of the identified disease or issue to other tomato plants in their crop.

Treatment Options:
Outline readily available treatment options for the farmer to address the identified disease or issue, prioritizing organic and sustainable solutions whenever possible. Include detailed instructions for treatment application if applicable.

Further Assistance:
Provide contact information for local agricultural extension services, plant disease specialists, or relevant helplines where the farmer can seek additional expert guidance if needed.

Your response should be written in clear, concise language that is easily understandable for the farmer.
"""

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("Disease Diagnosis and Treatment Guide")
    st.write(response)
