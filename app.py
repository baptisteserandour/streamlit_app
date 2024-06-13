import streamlit as st
import requests
from PIL import Image
import random

# Apply custom CSS to change the background color and text color
st.markdown(
    """
    <style>
    h1{
        color:black;
    }
    .stApp {
        background-color: white;
        color: black;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 1000vh;
        position: relative;
    }
    .stFileUpload label div {
        color: white;
    }
    .stFileUpload label div span {
        color: white;
    }

    .stImage{
        display: None;
    }

    .logo-container {
        width: 100px;
    }
    """,
    unsafe_allow_html=True
)

# Display logo
logo = Image.open("streamlit_app/img/pv_img.png")
st.image(logo, width=200)

# Title of the app
st.title("Picky Vampire")

# Description of the app
st.write("Welcome to Picky Vampire, a cell classification AI ! Please upload a blood cell picture")

# File uploader allows users to upload a picture
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], accept_multiple_files=False)

friendly_messages = [
    "Oh, delicious!",
    "I'll pass on this one.",
    "Not bad, not bad...",
    "Meh.",
    "Intriguing...",
    "More, please!",
    "I expected better.",
    "A strange taste...",
    "An explosion of flavors!",
    "Bland and boring."
]

#Call api when button is clicked via POST request
if uploaded_file is not None:
    st.write("Image uploaded successfully!")
    st.write("Click on the button below to make a prediction")

    if st.button("Validate"):
        # Send the image to the API
        #url = "http://localhost:8000/prediction"#local
        url = "https://picky-vampire2-ouxqpmwlaq-ew.a.run.app/prediction"
        files = {'file_cell': (uploaded_file.name, uploaded_file.getvalue(), 'image/jpeg')}
        request = requests.post(url, files=files)
        response = request.json()
        #st.write(response)
        #st.write(request)
        winning_class = request.json()['prediction']
        confidence = round(request.json()['confidence'] * 100, 2)

        #open all the files in the bboxes
        #image = Image.open('/Users/gillesziani/code/Biologeek89/picky_vampire/tmp_demo/bboxes_image/BA_47_withbboxes.jpg')

        if winning_class == 'ig':
            st.write(f"Mmmh.... I can tell at **{confidence}** % you are an **Immature granulocyte** cell.")

        else:
            st.write(f"Mmmh.... I can tell at **{confidence}** % you are a **{winning_class}** cell.")
        st.write(random.choice(friendly_messages))
else:
    st.write("Please upload an image")


# Check if a file has been uploaded
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    # Display the image
    st.image(image, caption='Uploaded Image', width=100)
    st.write("Image uploaded successfully!")
else:
    st.write(" ")
