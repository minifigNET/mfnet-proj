#NOTE TO TEAM - TO OPEN THE FILE ONLINE: streamlit run app.py
#or now: https://minifigurenet.streamlit.app

#Lego colours: https://usercontent.flodesk.com/de8064d5-0183-4c90-a0f9-0da438a65bce/upload/37cfed05-9017-4e5b-b5b8-ae11a341f132.pdf

import streamlit as st
import base64
import toml

st.set_page_config(
            page_title="MinifigNET",
            page_icon="🐍",
            layout="centered", # wide
            initial_sidebar_state="auto") # collapsed



#TODO add background image and colours - I really don't know what I'm doing here!!


# with open('minifig.toml', 'r') as f:
#     config = toml.load(f)

# theme = config.get('theme', {})
# primaryColor = theme.get('primaryColor')
# backgroundColor = theme.get('backgroundColor')
# secondaryBackgroundColor = theme.get('secondaryBackgroundColor')
# textColor = theme.get('textColor')
# font = theme.get('font')

# css = f"""
# <style>
# .stMarkdown {{
#     primaryColor: {primaryColor};
#     background-color: {backgroundColor};
#     secondaryBackgroundColor: {secondaryBackgroundColor};
#     color: {textColor};
#     font-family: {font};
# }}
# </style>
# """

# st.markdown(css, unsafe_allow_html=True)

# st.markdown("Experimenting with themes - bear with me...")

#testing this from Le Wagon site

CSS = """
h1 {
    color: red;
}
.stApp {
    background-image: url(https://avatars.githubusercontent.com/u/153445611?v=4);
    background-size: cover;
}
"""


st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

#TODO Link HERE to database and search function

st.title('MinifigNET')
st.write('Can’t remember the names of your LEGO minifigs? Now there’s an app for that!')
st.text("")
st.text("")
st.text("")

#Let the user take a photo from the app (more info on camera input here: https://docs.streamlit.io/library/api-reference/widgets/st.camera_input)
st.title('Take a photo of your minifig ...')
st.write('and we\'ll tell you what it\'s called!')
picture = st.camera_input('Your photo:')

if picture:
    st.image(picture)

#Let the user upload a photo of their minifig
st.title(' ... or upload a photo if you prefer')
uploaded_file = st.file_uploader("Upload your file here...", type=['png', 'jpeg', 'jpg'])

if uploaded_file is not None:
    st.image(uploaded_file)

# st.write(f'Thank you! This minifig is called XXX')
st.markdown('<style>h1{font-size: 30px;}</style>', unsafe_allow_html=True)
st.markdown('# Thank you! This minifig is called XXX', unsafe_allow_html=True)
st.text("")
st.text("")
#TODO - add this later, allowing people to contribute?
st.title('Can you help us to learn more?')
st.write("Do you know the name of a minifig that we don't have on your system? If so, please let us know!")

user_text = st.text_input('Name:')
st.write(f'You entered: {user_text}')

#TODO Query the database based on user input


#code for adding image copyright info
st.text("")
st.text("")
st.text("")
url = "https://www.streamlit.io"
st.write("Background image courtesy of: [link](%s)" % url)
# st.markdown("check out this [link](%s)" % url)
