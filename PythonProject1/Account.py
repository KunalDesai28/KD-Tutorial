import streamlit as st
import firebase_admin

from firebase_admin import credentials
from firebase_admin import auth
#from firebase_admin_user_mgt import UserRecord

cred = credentials.Certificate('kd-tutorial-3a09f5227e49.json')
firebase_admin.initialize_app(cred)


def app():
    st.title('Welcome to :violet[KD] App:sunglasses:')

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''

    def f():
        try:
            user= auth.get_user_by_email(email)
            #print(user.uid)

            st.write('Login Successful')

            st.session_state.username = user.uid
            st.session_state.useremail = user.email

            st.session_state.signedout = True
            st.session_state.signout = True


        except:
            st.warning('Login Failed')


    def t():
        st.session_state.signedout = False
        st.session_state.signout = False
        st.session_state.username = ''

    if "signedout" not in st.session_state:
        st.session_state.signedout = False
    if 'signout' not in st.session_state:
        st.session_state.signout = False

    if not st.session_state['signedout']:
        choice = st.selectbox('Login/Signup', ['Login', 'Signup'])

        if choice == 'Login':

            email = st.text_input('Email Address')
            password = st.text_input('Password', type='password')

            st.button('Login', on_click=f)

        else:
            email = st.text_input('Email Address')
            password = st.text_input('Password', type='password')

            username = st.text_input('Enter the Unique Username')

            if st.button('Create My Account'):
                user = auth.create_user(email=email, password=password, uid=username)

                st.success('Account Created Successfully!')
                st.markdown('Please Login using your Email & Password.')
                st.balloons()

    if st.session_state.signout:
        st.text('Name = ' + st.session_state.username)
        st.text('Email id = ' + st.session_state.useremail)
        st.button('Sign Out', on_click=t)
