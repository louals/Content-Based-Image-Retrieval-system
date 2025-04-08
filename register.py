import streamlit as st
import cv2
import numpy as np
import face_recognition
import database
import tempfile
import os
import login

def show_registration_page():
    st.title("Inscription - Reconnaissance Faciale")

   
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "email" not in st.session_state:
        st.session_state.email = ""
    if "password" not in st.session_state:
        st.session_state.password = ""

    
    username = st.text_input("Nom d'utilisateur", value=st.session_state.username)
    email = st.text_input("Email", value=st.session_state.email)
    password = st.text_input("Mot de passe", type="password", value=st.session_state.password)

   
    st.session_state.username = username
    st.session_state.email = email
    st.session_state.password = password

    
    st.write("Capture une image de ton visage")
    camera = st.camera_input("Prends une photo")

    if st.button("S'inscrire"):
        if not username or not email or not password or not camera:
            st.error("Tous les champs sont obligatoires !")
        elif database.user_exists(email):
            st.error("Cet email est déjà enregistré.")
        else:
       
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                temp_file.write(camera.getbuffer())
                image_path = temp_file.name
            
            try:
                img = face_recognition.load_image_file(image_path)
                face_encodings = face_recognition.face_encodings(img)

                if len(face_encodings) == 0:
                    st.error("Aucun visage détecté. Réessaie avec une meilleure photo.")
                else:
                    face_encoding = face_encodings[0]

                    success = False
                    if database.face_exists(face_encoding):
                        st.error("Un utilisateur avec ce visage existe déjà.")
                    else:
                        success = database.add_user(username, email, password, face_encoding)

                    if success:
                        st.success("Inscription réussie ! Tu peux maintenant te connecter.")
                        login.show_login_page()
                    else:
                        st.error("Erreur : Nom d'utilisateur ou email déjà utilisé.")
            except Exception as e:
                st.error(f"Erreur lors du traitement de l'image : {e}")
            finally:
                os.remove(image_path)