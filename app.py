import streamlit as st
import register  
import login



if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False


if st.session_state['authenticated']:
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choisir une page", ["Home", "Déconnexion"])

else:
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choisir une page", ["Connexion", "Inscription"])

    if page == "Inscription":
        register.show_registration_page()
    elif page == "Connexion":
        login.show_login_page()
