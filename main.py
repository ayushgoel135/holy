# Import necessary libraries
import streamlit as st
import pymongo
import pandas as pd
from dotenv import load_dotenv, find_dotenv
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables from the .env file
load_dotenv(find_dotenv())

# Configure Streamlit page settings
st.set_page_config(page_title="BuildHub Nutrition Monitor", page_icon="🔮")

# Configure Google Generative AI library with an API key from environment variables
genai.configure(api_key="AIzaSyD1ReYAISW1MRMC8rxja4wU_w5z0NFEzU0")

# Apply custom CSS to enhance the Streamlit app's appearance
st.markdown("""
    <style>

    .stApp {
    background-img:D:\APTECH\Python\HACKFIT\nutrition_bg.jpg;
        background-color: #f5f5f5;        # Light grey background for the app
        font-family: Arial, sans-serif;   # Arial font for a clean look
    }
    .stButton>button {
        background-color: #4CAF50;       # Green background for buttons
        color: white;                    # White text for buttons
        font-size: 16px;                 # Larger text for better readability
    }
    .stHeader {
        font-size: 24px;                 # Large font size for headers
        font-weight: bold;               # Bold font weight for headers
    }

    </style>
    """, unsafe_allow_html=True)  # Enable HTML within markdown for custom styles


# Define a function to handle the response from Google Gemini API
def get_gemini_response(input, image):
    # Initialize the Gemini model
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    # Send input and image data to the model and get textual response
    response = model.generate_content([input, image[0]])
    return response.text


# Define a function to set up image uploading and handle the image data
def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file content
        bytes_data = uploaded_file.getvalue()
        # Create a dictionary to hold image data including MIME type and raw data
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data,
            }
        ]
        return image_parts
    else:
        # Raise an error if no image is uploaded
        raise FileNotFoundError("No image uploaded")


# Sidebar configuration for navigation and file upload
st.sidebar.title("Navigation")
st.sidebar.header("Upload Section")
uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Display the main header of the application
st.header("Nutrition Monitor")
# Check if an image is uploaded and display it
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Create a button for triggering the food analysis
submit = st.button("Analyse this Food")
# Set the prompt for the AI model
input_prompt = """
You are an expert nutritionist analyzing the food items in the image.
Start by determining if the image contains food items. 
If the image does not contain any food items, 
clearly state "No food items detected in the image." 
and do not provide any calorie information. 

Follow the format below:

If no food items are detected:
No food items detected in the image.

If food items are detected:
Meal Name: [Name of the meal]


Total estimated calories: X

show the protein,carbohydrates,fats in approximate percentage of nutrients and in grams in a table format with good color combination also estimate the portion size for more accurate nutrition data. 
cross-check the above data once before giving the result
don't show any note of approximation instead show positive message if the food item belongs to healthy category and show not healthy message if the food item belongs to not healthy food
"""

# Action to take when the 'Analyse this Food' button is clicked
if submit:
    with st.spinner("Processing..."):  # Show a processing spinner while processing
        # Prepare the image data
        image_data = input_image_setup(uploaded_file)
        # Get the response from the AI model
        response = get_gemini_response(input_prompt, image_data)
        ind = response.index("Total")
        dish_name = response[10:ind - 1]
        dic = {}

        dish_name.lstrip()
        dic[ind] = dish_name
        a = open("file.txt", "a")
        a.write(str(dic))
        a.close()
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        data = pd.read_csv("file.txt")
    # Indicate processing is complete
    st.success("Done!")
    # Display the subheader and the response from the AI model
    st.subheader("Food Analysis")
    st.write(response)