
######
#Notes
######

#NOTE TO TEAM - TO OPEN THE FILE ONLINE: streamlit run app.py
#or now: https://minifignet.streamlit.app

#Lego colours: https://usercontent.flodesk.com/de8064d5-0183-4c90-a0f9-0da438a65bce/upload/37cfed05-9017-4e5b-b5b8-ae11a341f132.pdf

########
#Imports
########
import streamlit as st
import base64
import toml
from PIL import Image
import requests

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
# .topImage {
#     background-image: url(header.png);
#     background-size: contain;
#     height: 200px;  # adjust as needed
# }
"""
st.markdown(f'<style>{CSS}</style>', unsafe_allow_html=True)
st.markdown('<div class="topImage"></div>', unsafe_allow_html=True)
st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

#TODO fix the image link above




#####################
#Header
#####################

# st.title('MinifigNET')
st.markdown('<style>h1{font-size: 200px;}</style>', unsafe_allow_html=True)
st.markdown('# MinifigNET', unsafe_allow_html=True)
st.write('Can’t remember the names of your LEGO minifigs? Now there’s an app for that!')
st.text("")
st.text("")
st.text("")

#####################
#Resizing function
#####################

def resize_224(picture):
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
# Let the user take a photo from the app
# (more info on camera input here:
# https://docs.streamlit.io/library/api-reference/widgets/st.camera_input)
#####################

st.title('Take a photo of your minifig ...')
st.write('and we\'ll tell you what it\'s called!')
st.write(' Please try to take a clear photo, against a white background')
picture = st.camera_input('Your photo:')

if picture:
    resize_224(picture)


#############################################
#Let the user upload a photo of their minifig
#############################################

st.title(' ... or upload a photo if you prefer')
uploaded_file = st.file_uploader("Upload your file here...", type=['png', 'jpeg', 'jpg'])

if uploaded_file is not None:
    resize_224(uploaded_file)



#####################################################
#check the image against the model, return the answer
#####################################################

# params = dict()
# OUR_URL = 'https://taxifare.lewagon.ai/predict' #TODO - change this to our model
# response = requests.get(wagon_cab_api_url, params=params) #TODO - change this to our model
# prediction = response.json()
# pred = prediction['fare'] #TODO - change this to our model
# st.header(f'Your minifig is a: ${whatever it is)}')

st.markdown('<style>h1{font-size: 30px;}</style>', unsafe_allow_html=True)
st.markdown('# Thank you! This minifig is called XXX', unsafe_allow_html=True)
st.text("")
st.text("")


####################################
#ask for input to build our database
####################################

#TODO - remove this code, we can return later when we are allowing people to contribute?

st.title('Can you help us to learn more?')
st.write("Do you know the name of a minifig that we don't have on your system? If so, please let us know!")

# user_text = st.text_input('Name:')
# st.write(f'You entered: {user_text}')
st.text("")
st.text("")

#based on https://en.wikipedia.org/wiki/Lego_Minifigures_(theme)
option = st.selectbox(
    'What class does the minifig belong to?',
    ('No: 43 - Marvel Collectible Minifigure Series 1 (Set Number: 71039)',
     'No: 42 - Disney 100 Minifigure Series (Set Number: 71038)',
     'No: 41 - Series 24 (Set Number: 71037)',
     'No: 40 - Series 23 (Set Number: 71034)',
     'No: 39 - Muppets Series (Set Number: 71033)',
     'No: 38 - Series 22 (Set Number: 71032)',
     'No: 37 - Marvel Collectible Minifigure Series 2 (Set Number: 71031)',
     'No: 36 - Looney Tunes Series (Set Number: 71030)',
     'No: 35 - Series 21 (Set Number: 71029)',
     'No: 34 - Harry Potter Series 2 (Set Number: 71028)'







     ))

st.write('You selected Class:', option)

if option == 'No: 43 - Marvel Collectible Minifigure Series 1 (Set Number: 71039)':
    marvel1_option = st.selectbox('Select character name', ('Minifig 1', 'Minifig 2'))
    st.write('You selected Marvel Collectible Minifigure Series 1:', marvel1_option)

elif option == 'No: 42 - Disney 100 Minifigure Series (Set Number: 71038)':
    disney_option = st.selectbox('Select character name', ('Minifig 1', 'Minifig 2'))
    st.write('You selected Disney 100 Minifigure Series:', disney_option)

elif option == 'No: 41 - Series 24 (Set Number: 71037)':
    series24_option = st.selectbox('Select character name', ('Minifig 1', 'Minifig 2'))
    st.write('You selected Series 24:', series24_option)

elif option == 'No: 40 - Series 23 (Set Number: 71034)':
    series23_option = st.selectbox('Select character name', ('Minifig 1', 'Minifig 2'))
    st.write('You selected Series 23:', series23_option)

elif option == 'No: 39 - Muppets Series (Set Number: 71033)':
    muppets_option = st.selectbox('Select character name', ('Animal', 'Swedish Chef', 'Miss Piggy', 'Kermit'))
    st.write('You selected Muppets Series:', muppets_option)

elif option == 'No: 38 - Series 22 (Set Number: 71032)':
    series22_option = st.selectbox('Select character name', ('Minifig 1', 'Minifig 2'))
    st.write('You selected Series 22:', series22_option)

elif option == 'No: 37 - Marvel Collectible Minifigure Series 2 (Set Number: 71031)':
    marvel2_option = st.selectbox('Select character name', ('Minifig 3', 'Minifig 4'))
    st.write('You selected Marvel Collectible Minifigure Series 2:', marvel2_option)

elif option == 'No: 36 - Looney Tunes Series (Set Number: 71030)':
    looney_option = st.selectbox('Select character name', ('Minifig 1', 'Minifig 2'))
    st.write('You selected Looney Tunes Series:', looney_option)

elif option == 'No: 35 - Series 21 (Set Number: 71029)':
    series21_option = st.selectbox('Select character name', ('Minifig 1', 'Minifig 2'))
    st.write('You selected Disney 100 Minifigure Series:', series21_option)

elif option == 'No: 34 - Harry Potter Series 2 (Set Number: 71028)':
    harry_option = st.selectbox('Select character name', ('Harry', 'Hermione', 'Ron'))
    st.write('You selected Harry Potter Series 2:', harry_option)






#TODO add drop dwn with all classes and names - api response , hard code to start

#########################################
#code for adding any image copyright info
#########################################

st.text("")
st.text("")
st.text("")
# url = "https://www.streamlit.io"
# st.write("Background image courtesy of: [link](%s)" % url)
# st.markdown("check out this [link](%s)" % url)
