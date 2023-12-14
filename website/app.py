#NOTE TO TEAM - TO OPEN THE FILE ONLINE: streamlit run app.py
#or now: https://minifigurenet.streamlit.app

#Lego colours: https://usercontent.flodesk.com/de8064d5-0183-4c90-a0f9-0da438a65bce/upload/37cfed05-9017-4e5b-b5b8-ae11a341f132.pdf

import streamlit as st
import base64
import toml
from PIL import Image

#####################
#Set up the page style
#####################

st.set_page_config(
            page_title="MinifigNET",
            page_icon="🤖",

            layout="centered", # wide
            initial_sidebar_state="auto") # collapsed


CSS = """
h1 {
    color: red;
}
.stApp {
    background-image: url(https://avatars.githubusercontent.com/u/153445611?v=4);
    background-size: contain;
    background-position: top right;
    background-repeat: no-repeat;
}
.topImage {
    background-image: url(Header_image.jpg);
    background-size: cover;
    height: 200px;  # adjust as needed
}
"""
st.markdown(f'<style>{CSS}</style>', unsafe_allow_html=True)
st.markdown('<div class="topImage"></div>', unsafe_allow_html=True)
st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

#TODO fix the image link above



# st.title('MinifigNET')
st.markdown('<style>h1{font-size: 100px;}</style>', unsafe_allow_html=True)
st.markdown('# MinifigNET', unsafe_allow_html=True)
st.write('Can’t remember the names of your LEGO minifigs? Now there’s an app for that!')
st.text("")
st.text("")
st.text("")

#####################
# Let the user take a photo from the app (more info on camera input here: https://docs.streamlit.io/library/api-reference/widgets/st.camera_input)
#####################

st.title('Take a photo of your minifig ...')
st.write('and we\'ll tell you what it\'s called!')
picture = st.camera_input('Your photo:')

#####  I tried the code below but it squishes the image
# resize(picture)
# if picture:
#     st.image(picture)
#     img = Image.open(picture)
#     img = img.resize((224, 224))
#     st.image(img)


if picture:
    st.image(picture)
    img = Image.open(picture)
    width, height = img.size
    aspect = width / height

    if aspect > 1:
        new_width = height
        start_x = (width - height) / 2
        img = img.crop((start_x, 0, start_x + new_width, height))
    else:
        new_height = width
        start_y = (height - width) / 2
        img = img.crop((0, start_y, width, start_y + new_height))

    img = img.resize((224, 224))
    st.image(img)

#####################
#Let the user upload a photo of their minifig
#####################

st.title(' ... or upload a photo if you prefer')
uploaded_file = st.file_uploader("Upload your file here...", type=['png', 'jpeg', 'jpg'])

if uploaded_file is not None:
    st.image(uploaded_file)
    img = Image.open(picture)
    width, height = img.size
    aspect = width / height

    if aspect > 1:
        new_width = height
        start_x = (width - height) / 2
        img = img.crop((start_x, 0, start_x + new_width, height))
    else:
        new_height = width
        start_y = (height - width) / 2
        img = img.crop((0, start_y, width, start_y + new_height))

    img = img.resize((224, 224))
    st.image(img)


st.markdown('<style>h1{font-size: 30px;}</style>', unsafe_allow_html=True)
st.markdown('# Thank you! This minifig is called XXX', unsafe_allow_html=True)
st.text("")
st.text("")

#TODO Link HERE to database and search function
#TODO Query the database based on user input

#TODO - take this out, return later when we are allowing people to contribute?
st.title('Can you help us to learn more?')
st.write("Do you know the name of a minifig that we don't have on your system? If so, please let us know!")

user_text = st.text_input('Name:')
st.write(f'You entered: {user_text}')



#####################
#code for adding any image copyright info
#####################

st.text("")
st.text("")
st.text("")
# url = "https://www.streamlit.io"
# st.write("Background image courtesy of: [link](%s)" % url)
# st.markdown("check out this [link](%s)" % url)
