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



#TODO add background image - I really don't know how to do this!



#TRIAL ONE:
# @st.cache_data(allow_output_mutation=True)
# @st.cache_data()
# def get_base64_of_bin_file(bin_file):
#     with open(bin_file, 'rb') as f:
#         data = f.read()
#     return base64.b64encode(data).decode()

# def set_png_as_page_bg(png_file):
#     bin_str = get_base64_of_bin_file(png_file)
#     page_bg_img = (
#     <style>
#     body {
    # background-image: url("website/blueblocks.png;base64,%s");
#         background-image: url("website/blueblocks/png;base64,%s");

#     background-size: cover;
#     }
#     </style>)
#     % bin_str

#     st.markdown(page_bg_img, unsafe_allow_html=True)
#     return

# set_png_as_page_bg('blueblocks.png')


#TRIAL TWO:
st.markdown(
    """
    <style>
    .reportview-container {
        background: url("website/blueblocks.png");
    }
   </style>
    """,
    unsafe_allow_html=True
)

#TRIAL THREE:


with open('minifig.toml', 'r') as f:
    config = toml.load(f)

theme = config.get('theme', {})
primaryColor = theme.get('primaryColor')
backgroundColor = theme.get('backgroundColor')
secondaryBackgroundColor = theme.get('secondaryBackgroundColor')
textColor = theme.get('textColor')
font = theme.get('font')

# Create a CSS string using your theme settings
css = f"""
<style>
.stMarkdown {{
    background-color: {secondaryBackgroundColor};
    color: {textColor};
    font-family: {font};
}}
</style>
"""

# Apply the CSS to your Streamlit app
st.markdown(css, unsafe_allow_html=True)

# Now when you use st.markdown, it will be styled with your theme settings
st.markdown("Experimenting with themes - bear with me...")

#TODO Link HERE to database and search function

st.title('MinifigNET')
st.write('Can’t remember the names of your LEGO minifigs? Now there’s an app for that!')
st.text("")
st.text("")
st.text("")

#Let the user take a photo from the app (more info on camera input here: https://docs.streamlit.io/library/api-reference/widgets/st.camera_input)
st.title('Take a photo of your minifig here...')
picture = st.camera_input("and we'll tell you what it's called!")

if picture:
    st.image(picture)

#Let the user upload a photo of their minifig
st.title(' ... or upload a photo of your minifig here')
uploaded_file = st.file_uploader("Upload your file here...", type=['png', 'jpeg', 'jpg'])

if uploaded_file is not None:
    st.image(uploaded_file)

st.write(f'Thank you! This minifig is called XXX')

#TODO - add this later, allowing people to contribute?
st.title('Minifig name')

user_text = st.text_input('Do you know the name of this minifig? If so, please let us know:')
st.write(f'You entered: {user_text}')

#TODO Query the database based on user input


#code for adding image copyright info
st.text("")
st.text("")
st.text("")
url = "https://www.streamlit.io"
st.write("Background image courtesy of: [link](%s)" % url)
# st.markdown("check out this [link](%s)" % url)
