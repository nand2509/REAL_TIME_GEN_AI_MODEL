# import streamlit as st
# import google.generativeai as genai
# import os
# import pytesseract
# from PIL import Image
# import pandas as pd
# from PyPDF2 import PdfReader
# from werkzeug.utils import secure_filename
#
# # Configure the generative AI model
# genai.configure(api_key="AIzaSyBH9pjDICFfC4RqNF2luI86P1LVlLyCF78")  # Replace with your actual API key
# model = genai.GenerativeModel("gemini-1.5-flash")
#
# # Streamlit app configuration
# st.title("Generative AI Text Response Generator")
#
# # Allow users to enter a prompt
# user_prompt = st.text_area("Enter your prompt:")
#
# # File upload section
# uploaded_file = st.file_uploader("Choose a file (txt, pdf, csv, xlsx, png, jpg)",
#                                  type=["txt", "pdf", "csv", "xlsx", "png", "jpg", "jpeg"])
#
# # Create uploads directory if it doesn't exist
# if not os.path.exists("uploads"):
#     os.makedirs("uploads")
#
# extracted_text = ""
#
# if uploaded_file is not None:
#     filename = os.path.join("uploads", secure_filename(uploaded_file.name))
#
#     # Save uploaded file
#     with open(filename, "wb") as f:
#         f.write(uploaded_file.getbuffer())
#
#         # Extract text based on file type
#     if filename.lower().endswith(".txt"):
#         with open(filename, "r") as file:
#             extracted_text = file.read()
#
#     elif filename.lower().endswith(".pdf"):
#         with open(filename, "rb") as file:
#             reader = PdfReader(file)
#             for page in reader.pages:
#                 extracted_text += page.extract_text() + "\n"
#
#     elif filename.lower().endswi   th(".csv"):
#         df = pd.read_csv(filename)
#         extracted_text = df.to_string()  # Convert DataFrame to string
#
#     elif filename.lower().endswith(".xlsx"):
#         df = pd.read_excel(filename)
#         extracted_text = df.to_string()  # Convert DataFrame to string
#
#     elif filename.lower().endswith((".png", ".jpg", ".jpeg")):
#         image = Image.open(filename)
#         extracted_text = pytesseract.image_to_string(image)
#
#     else:
#         st.error("Invalid file type")
#
#     # Display extracted text if any
# if extracted_text:
#     st.subheader("Extracted Text:")
#     st.write(extracted_text)
#
# # Button to generate response for the user prompt
# if st.button("Generate Response for Prompt"):
#     if user_prompt:  # Check if user prompt is not empty
#         # Generate response for the user prompt
#         prompt_response = model.generate_content(user_prompt)
#         formatted_prompt_response = "\n".join(
#             [f"{i + 1}. {line.strip()}." for i, line in enumerate(prompt_response.text.split(". ")) if line.strip()]
#         )
#
#         st.subheader("AI Response to Your Prompt:")
#         st.write(formatted_prompt_response)
#     else:
#         st.warning("Please enter a prompt to generate a response.")
#
#     # Button to generate response for both user prompt and extracted text
# if st.button("Generate Combined Response"):
#     if extracted_text and user_prompt:  # Both inputs are required
#         combined_input = f"Prompt: {user_prompt}\nExtracted Text: {extracted_text}"
#         combined_response = model.generate_content(combined_input)
#         formatted_combined_response = "\n".join(
#             [f"{i + 1}. {line.strip()}." for i, line in enumerate(combined_response.text.split(". ")) if line.strip()]
#         )
#
#         st.subheader("AI Response to Combined Inputs:")
#         st.write(formatted_combined_response)
#     else:
#         st.warning("Please provide both a prompt and an uploaded file to generate a combined response.")
#
# if uploaded_file is None and not user_prompt:
#     st.warning("Please upload a file to extract text from, or enter a prompt.")

import streamlit as st
import google.generativeai as genai
import os
import pytesseract
from PIL import Image
import pandas as pd
from PyPDF2 import PdfReader
from werkzeug.utils import secure_filename

# Configure the generative AI model
genai.configure(api_key="AIzaSyBH9pjDICFfC4RqNF2luI86P1LVlLyCF78")  # Replace with your actual API key
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit app configuration
st.title("Generative AI Text Response Generator")

# Allow users to enter a prompt
user_prompt = st.text_area("Enter your prompt:")

# File upload section
uploaded_file = st.file_uploader("Choose a file (txt, pdf, csv, xlsx, png, jpg)",
                                 type=["txt", "pdf", "csv", "xlsx", "png", "jpg", "jpeg"])

# Create uploads directory if it doesn't exist
if not os.path.exists("uploads"):
    os.makedirs("uploads")

extracted_text = ""

if uploaded_file is not None:
    filename = os.path.join("uploads", secure_filename(uploaded_file.name))

    # Save uploaded file
    with open(filename, "wb") as f:
        f.write(uploaded_file.getbuffer())

        # Extract text based on file type
    if filename.lower().endswith(".txt"):
        with open(filename, "r") as file:
            extracted_text = file.read()

    elif filename.lower().endswith(".pdf"):
        with open(filename, "rb") as file:
            reader = PdfReader(file)
            for page in reader.pages:
                extracted_text += page.extract_text() + "\n"

    elif filename.lower().endswith(".csv"):
        df = pd.read_csv(filename)
        extracted_text = df.to_string()  # Convert DataFrame to string

    elif filename.lower().endswith(".xlsx"):
        df = pd.read_excel(filename)
        extracted_text = df.to_string()  # Convert DataFrame to string

    elif filename.lower().endswith((".png", ".jpg", ".jpeg")):
        image = Image.open(filename)
        extracted_text = pytesseract.image_to_string(image)

    else:
        st.error("Invalid file type")

    # Display extracted text if any
if extracted_text:
    st.subheader("Extracted Text:")
    st.write(extracted_text)

# Button to generate response for the user prompt
if st.button("Generate Response for Prompt"):
    if user_prompt:  # Check if user prompt is not empty
        # Generate response for the user prompt
        prompt_response = model.generate_content(user_prompt)
        formatted_prompt_response = "\n".join(
            [f"{i + 1}. {line.strip()}." for i, line in enumerate(prompt_response.text.split(". ")) if line.strip()]
        )

        st.subheader("AI Response to Your Prompt:")
        st.write(formatted_prompt_response)
    else:
        st.warning("Please enter a prompt to generate a response.")

    # Button to generate response for both user prompt and extracted text
if st.button("Generate Combined Response"):
    if extracted_text and user_prompt:  # Both inputs are required
        combined_input = f"Prompt: {user_prompt}\nExtracted Text: {extracted_text}"
        combined_response = model.generate_content(combined_input)
        formatted_combined_response = "\n".join(
            [f"{i + 1}. {line.strip()}." for i, line in enumerate(combined_response.text.split(". ")) if line.strip()]
        )

        st.subheader("AI Response to Combined Inputs:")
        st.write(formatted_combined_response)
    else:
        st.warning("Please provide both a prompt and an uploaded file to generate a combined response.")

if uploaded_file is None and not user_prompt:
    st.warning("Please upload a file to extract text from, or enter a prompt.")