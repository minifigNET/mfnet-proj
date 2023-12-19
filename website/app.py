######
# Notes
######

# TO OPEN THE FILE ONLINE: streamlit run app.py
# or now: https://minifignet.streamlit.app

########
# Imports
########
import streamlit as st
from PIL import Image
import requests
import html

#####################
# Set up the page style
#####################

st.set_page_config(
    page_title="MinifigNET",
    page_icon="https://cdn-icons-png.flaticon.com/512/1674/1674274.png",
    layout="centered")


st.write("""
    <style>
        h1 {
            color: red;
            font-size: 96px !important;
        }
        h2 {
            color: red;
        }
    </style>""", unsafe_allow_html=True)


#####################
# Header
#####################

st.title('MinifigNET ![](https://lh3.googleusercontent.com/u/2/drive-viewer/AEYmBYR3Q5FtiJs9Eo-azS4c1phN_j0FsKqwYQbE7u259ys-0dkmPINtwIaJwfZN1YezGMfppva0383ja1ncwtaBC223GYDWqw=w2940-h1538 "Ho ho ho!")')

st.markdown(
    '##### Can’t remember the names of your LEGO minifigs? Now there’s an app for that!')

st.text("")
st.text("")
st.text("")

#####################
# Resizing + cropping function
#####################


def resize_224(picture):
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

    return img.resize((224, 224))


#####################
# Let the user take a photo from the app
# (more info on camera input here:
# https://docs.streamlit.io/library/api-reference/widgets/st.camera_input)
#####################
st.markdown('## Take a photo of your minifig ...')
st.write('and we\'ll tell you what it\'s called!')

if st.button("📸 Open camera"):
    if "upload" in st.session_state:
        del st.session_state.upload
    st.camera_input("ℹ️ Please try to take a clear photo, against a white background, and centre your subject 🎯", key="capture")


#############################################
# Let the user upload a photo of their minifig
#############################################
st.markdown('## ... or upload one if you prefer')

st.file_uploader("Select a photo (preferably with the subject in the centre):",
                 type=['png', 'jpeg', 'jpg'], key="upload")

#####################################################
# check the image against the model, return the answer
#####################################################

photo = st.session_state.capture if "capture" in st.session_state \
    else st.session_state.upload if "upload" in st.session_state and st.session_state.upload \
    else None

if photo:
    st.markdown("## Now let's analyze your photo")
    photo = resize_224(photo)
    st.image(photo)

    with st.spinner("Analyzing..."):
        # Get bytes from the file buffer
        img_bytes = photo.convert("RGB").tobytes()

        # Make request to API
        response = requests.post('http://127.0.0.1:8000/predict',
                                 files={'img': img_bytes,
                                        })

        if response.status_code == 200:
            print("✅ Image analyzed successfully.")
            # prediction = {
            #     'probability': 0.99,
            #     'minifigure_name': "SANTA",
            #     'set_id': "99999",
            #     'set_name': "CHRISTMAS SET",
            #     'class_id': 99
            # }
            prediction = response.json()
            st.markdown('### This minifig is called:')
            st.write(f'{prediction["minifigure_name"]} ({prediction["probability"]:2.0%} sure). Tada! 😊')

        else:
            st.markdown("**Oops**, something went wrong 😓 Please try again.")
            print(response.status_code, response.content)


st.text("")
st.text("")


####################################
# ask for input to build our database
####################################

# TODO - decide whether we should remove this code, we can return it later when we are allowing people to contribute?

st.markdown('## Can you help us to learn more?')
st.write("You know the name of your minifig, but we don't have it in our database?")
st.write("If so, please help us out!")

st.text("")
st.text("")

# based on https://en.wikipedia.org/wiki/Lego_Minifigures_(theme)
option = st.selectbox(
    'What class does your minifig belong to?',
    ('No: 43 - Marvel Collectible Minifigure Series 1 (Set Number: 71039)',
     'No: 42 - Disney 100 Minifigure Series (Set Number: 71038)',
     'No: 41 - Series 24 (Set Number: 71037)',
     'No: 40 - Series 23 (Set Number: 71034)',
     'No: 39 - Muppets Series (Set Number: 71033)',
     'No: 38 - Series 22 (Set Number: 71032)',
     'No: 37 - Marvel Collectible Minifigure Series 2 (Set Number: 71031)',
     'No: 36 - Looney Tunes Series (Set Number: 71030)',
     'No: 35 - Series 21 (Set Number: 71029)',
     'No: 34 - Harry Potter Series 2 (Set Number: 71028)',
     'No: 33 - Series 20 (Set Number: 71027)',
     'No: 32 - DC Super Heroes Series (Set Number: 71026)',
     'No: 31 - Series 19 (Set Number: 71025)',
     'No: 30 - Disney Series 2[ (Set Number: 71024)',
     ))

st.write('You selected Class:', option)

if option == 'No: 43 - Marvel Collectible Minifigure Series 1 (Set Number: 71039)':
    marvel1_option = st.selectbox(
        'What is the character name?',
        ('Goliath', 'She-Hulk', 'Echo', 'Kate Bishop', 'Hawkeye', 'Moon Knight', 'Mr. Knight', 'Storm', 'Beast',
         'Wolverine', 'Agatha Harkness', 'The Werewolf'))
    st.write('You selected Marvel Collectible Minifigure Series 1:', marvel1_option)

elif option == 'No: 42 - Disney 100 Minifigure Series (Set Number: 71038)':
    disney_option = st.selectbox('What is the character name?',
                                 ('Pocahontas', 'Aurora', 'Mulan', 'Tiana', 'The Queen', 'Queen of Hearts',
                                  'Dr Facilier', 'Cruella de Vil & Dalmatian puppy', 'Sorcerers Apprentice Mickey',
                                  'Pinocchio', 'Jimmy Cricket', 'Michael', 'Dante', 'Ernesto de la Cruz', 'Stitch 626',
                                  'Oswald the Lucky Rabbit', 'Robin Hood', 'Prince John', 'Baymax'))
    st.write('You selected Disney 100 Minifigure Series:', disney_option)

elif option == 'No: 41 - Series 24 (Set Number: 71037)':
    series24_option = st.selectbox('What is the character name?',
                                   ('T-Rex Fan Costume', 'Rococo Aristocrat', 'Robot Warrior', 'Potter',
                                    'Newspaper Kid', 'Orc', 'Soccer Referee', 'Falconer', 'Conservationist',
                                    'Carrot Mascot', 'Brown Astronaut and Spacebaby', 'Rockin Horse Rider'))
    st.write('You selected Series 24:', series24_option)

elif option == 'No: 40 - Series 23 (Set Number: 71034)':
    series23_option = st.selectbox(
        'What is the character name?',
        ('Green Dragon Costume', 'Knight of the Yellow Castle'
         'Cardboard Robot', 'Popcorn Costume', 'Nutcracker', 'Sugar Fairy', 'Ferry Captain', 'Turkey Costume',
         'Wolf Costume', 'Snowman', 'Reindeer Costume', 'Holiday Elf'))
    st.write('You selected Series 23:', series23_option)

elif option == 'No: 39 - Muppets Series (Set Number: 71033)':
    muppets_option = st.selectbox(
        'What is the character name?',
        ('Statler', 'Waldorf', 'Dr. Bunsen Honeydew', 'Beaker', 'Animal', 'Miss Piggy', 'Kermit the Frog',
         'Rowlf the Dog', 'The Swedish Chef', 'Gonzo', 'Janice', 'Fozzie Bear'))
    st.write('You selected Muppets Series:', muppets_option)

elif option == 'No: 38 - Series 22 (Set Number: 71032)':
    series22_option = st.selectbox('What is the character name?',
                                   ('Figure Skating Champion', 'Snow Guardian', 'Chili Costume Fan',
                                    'Racoon Costume Fan', 'Forest Elf', 'Night Protector', 'Space Creature',
                                    'Robot Repair Tech', 'Troubadour'))
    st.write('You selected Series 22:', series22_option)

elif option == 'No: 37 - Marvel Collectible Minifigure Series 2 (Set Number: 71031)':
    marvel2_option = st.selectbox('What is the character name?',
                                  ('Captain America', 'Winter Soldier', 'The Scarlet Witch', 'The Vision',
                                   'Monica Rambeau', 'Gamora', 'Zombie Hunter Spidey', 'Zombie Captain America',
                                   'Captain Carter', 'TChalla Star Lord', 'Loki', 'Sylvie'))
    st.write('You selected Marvel Collectible Minifigure Series 2:', marvel2_option)

elif option == 'No: 36 - Looney Tunes Series (Set Number: 71030)':
    looney_option = st.selectbox(
        'What is the character name?',
        ('Bugs Bunny', 'Lola Bunny', 'Daffy Duck', 'Tweety Bird', 'Sylvester', 'Road Runner', 'Wile E. Coyote',
         'Porky Pig', 'Petunia Pig', 'Speedy Gonzales', 'Tasmanian Devil', 'Marvin the Martian'))
    st.write('You selected Looney Tunes Series:', looney_option)

elif option == 'No: 35 - Series 21 (Set Number: 71029)':
    series21_option = st.selectbox('What is the character name?',
                                   ('Centaur Warrior', 'Shipwreck Survivor', 'Pug Costume Guy', 'Beekeeper',
                                    'Ladybug Girl', 'Violin Kid', 'Alien', 'Space Police Guy', 'Ancient Warrior',
                                    'Airplane Girl', 'Cabaret Singer', 'Paddle Surfer'))
    st.write('You selected Disney 100 Minifigure Series:', series21_option)

elif option == 'No: 34 - Harry Potter Series 2 (Set Number: 71028)':
    harry2_option = st.selectbox('What is the character name?',
                                 ('Harry Potter', 'Hermione Granger™', 'Ron Weasley™', 'Ginny Weasley', 'Fred Weasley',
                                  'George Weasley', 'Luna Lovegood™', 'Moaning Myrtle', 'Griphook',
                                  'Headmaster Albus Dumbledore™', 'Professor Sprout', 'Neville Longbottom™',
                                  'Kingsley Shacklebolt', 'Bellatrix Lestrange', 'Lily Potter', 'James Potter'))
    st.write('You selected Harry Potter Series 2:', harry2_option)

elif option == 'No: 33 = Series 20 (Set Number: 71027)':
    series20_option = st.selectbox(
        'What is the character name?',
        ('Piñata boy', 'Pajama girl', 'Drone boy', '80s musician', 'Peapod costume girl', 'Sea rescuer', 'Viking',
         'Pirate girl', 'Martial arts boy', 'Breakdancer', 'Llama costume girl', 'Brick costume guy', 'Athlete',
         'Space fan', 'Super warrior', 'Tournament knight'))
    st.write('You selected Series 20:', series20_option)

elif option == 'No: 32 - DC Super Heroes Series (Set Number: 71026)':
    dc_super_option = st.selectbox('What is the character name?',
                                   ('Batman', 'Superman', 'The Joker', 'Huntress', 'Metamorpho', 'Sinestro',
                                    'Green Lantern', 'Mr. Miracle', 'Bat-Mite', 'Star Girl', 'Cheetah', 'Aquaman',
                                    'Cyborg', 'BUMBLEBEE', 'The Flash', 'Wonder Woman'))
    st.write('You selected DC Super Heroes Series:', dc_super_option)

elif option == 'No: 31 - Series 19 (Set Number: 71025)':
    series19_option = st.selectbox('What is the character name?',
                                   ('Dog Sitter', 'Video Game Champ', 'Shower Guy', 'Rugby Player', 'Bear Costume Guy',
                                    'Pizza Costume Guy', 'Galactic Bounty Hunter', 'Monkey King', 'Programmer',
                                    'Gardener', 'Fire Fighter', 'Mountain Biker', 'Fright Knight', 'Mummy Queen',
                                    'Jungle Explorer', 'Fox Costume Girl'))
    st.write('You selected Series 19:', series19_option)

elif option == 'No: 30 - Disney Series 2[ (Set Number: 71024)':
    disney2_option = st.selectbox(
        'What is the character name?',
        ('Vintage Mickey', 'Vintage Minnie', 'Hercules', 'Jack Skellington', 'Scrooge McDuck', 'Huey, Dewey', 'Louie',
         'Chip', 'Dale', 'Jasmine', 'Jafar', 'Hades', 'Elsa', 'Anna', 'Sally', 'Edna', 'Frozone'))
    st.write('You selected Disney Series 2:', disney2_option)

st.text("")
st.text("")


def sanitize_input(input_str):
    sanitized_str = html.escape(input_str)
    return sanitized_str


st.write("Now please tell us all the details you have. Name, series, set number - any information is helpful!")

user_text = st.text_input("Name:")
minifig_name = sanitize_input(user_text)
user_text = st.text_input("Series:")
minifig_series = sanitize_input(user_text)
user_text = st.text_input("Set Number:")
minifig_set = sanitize_input(user_text)

st.file_uploader("Select a photo (preferably with the subject in the centre):", type=[
                                 'png', 'jpeg', 'jpg'],accept_multiple_files=True,key='class_upload')
photo_classes = st.session_state.class_upload if "class_upload" in st.session_state and st.session_state.class_upload \
    else None

if photo_classes and minifig_series and minifig_name and minifig_name:
    if len(photo_classes) > 7:
        photos = [resize_224(photo).convert("RGB").tobytes() for photo in photo_classes]
        data = {
            "lego_ids": minifig_set,
            "lego_names": minifig_series,
            "minifigure_name": minifig_name
        }
        files = [("imgs", (f"photo{i}", photo)) for i, photo in enumerate(photos)]
        # st.write(files)
        response = requests.post('http://127.0.0.1:8000/add_class',
                                        params = data,
                                        files = files
                                        )
        if response.status_code == 200:
            st.markdown('### Added to database:')
            st.write( 'Tada! 😊')
            photo_classes.clear()
        else:
            st.markdown("**Oops**, something went wrong 😓 Please try again.")
            print(response.status_code, response.content)

    else:
        st.write('Please add more photos')

st.write(
    f'Thank you! You entered: {user_text}. We will add this to our database.')


#########################################
# code for adding any image copyright info
#########################################

st.text("")
st.text("")
st.text("")
