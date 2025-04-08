import streamlit as st
import database
import bcrypt
import numpy as np
import face_recognition
import cv2
import re
import pickle
from google.oauth2 import id_token
from google.auth.transport import requests
from google_auth_oauthlib.flow import Flow
import google.auth

GOOGLE_CLIENT_ID = "279332564876-d0hoiali6mef65n91fd6i4hpmmk6hrjc.apps.googleusercontent.com"
REDIRECT_URI = 'http://localhost:8502/'

if st.session_state.get('authenticated', False):
    st.switch_page("pages/home.py")

def authenticate_google():
    """Authenticates user with Google OAuth."""
    flow = Flow.from_client_secrets_file(
        "client_secret.json",
        scopes=["https://www.googleapis.com/auth/userinfo.email", "openid"],
        redirect_uri=REDIRECT_URI
    )

    code = st.query_params.get("code", None)

    if not code:
        auth_url, _ = flow.authorization_url(prompt='consent')
        st.markdown(f"[Connectez-vous avec Google]({auth_url})")
        return None

    try:
        flow.fetch_token(code=code)
    except Exception as e:
        st.error(f"Error fetching token: {e}")
        return None

    credentials = flow.credentials
    request = google.auth.transport.requests.Request()

    try:
        id_info = id_token.verify_oauth2_token(credentials.id_token, request, GOOGLE_CLIENT_ID)
    except ValueError as e:
        st.error(f"Error verifying token: {e}")
        return None

    email = id_info.get("email")
    name = id_info.get("name")
    if email:
        st.session_state['authenticated'] = True
        st.session_state['user_info'] = {'email': email, 'name': name}
        st.switch_page("pages/home.py")
        return email
    else:
        st.error("Échec de l'authentification Google.")
    return None

def authenticate_email_password(email, password):
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user is None:
            st.error("Email non trouvé.")
            return None

        stored_password = user[3] 
        
        if isinstance(password, str): 
            password = password.encode() 

        if bcrypt.checkpw(password, stored_password):
            st.session_state['authenticated'] = True
            st.session_state['user_info'] = {'username': user[1], 'email': user[2]}
            st.switch_page("pages/home.py")
            return user[1]
        else:
            st.error("Mot de passe incorrect.")
            return None
    except Exception as e:
        st.error(f"Erreur de la base de données : {e}")
        return None

def authenticate_face(email):
    st.write("Reconnaissance faciale en cours...")

    camera_image = st.camera_input("Prends une photo")

    if camera_image is None:
        st.warning("Veuillez prendre une photo pour vous connecter.")
        return None

    img_array = np.frombuffer(camera_image.getbuffer(), dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    if img is None:
        st.error("Erreur lors de la lecture de l'image.")
        return None

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    new_encoding = face_recognition.face_encodings(img_rgb)

    if len(new_encoding) == 0:
        st.error("Aucun visage détecté. Réessaie avec une meilleure photo.")
        return None

    new_encoding = new_encoding[0]

    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username, face_encoding FROM users WHERE email=?", (email,))
        user = cursor.fetchone()

        conn.close()

        if user is None:
            st.error("Email non trouvé.")
            return None

        visage = pickle.loads(user[1])  
        username = user[0]
       
        match = face_recognition.compare_faces([visage], new_encoding, tolerance=0.5)

        if match[0]:
            st.session_state['authenticated'] = True
            st.session_state['user_info'] = {'username': username, 'email': email}
            st.switch_page("pages/home.py")
            return username
        else:
            st.error("Aucune correspondance trouvée avec votre visage.")
            return None
    except Exception as e:
        st.error(f"Erreur lors de la connexion à la base de données: {e}")
        return None

def is_valid_email(email):
    """Check if the email follows a valid format."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def show_login_page():
    st.title("Connexion - Reconnaissance Faciale, Email et Google")

    email = st.text_input("Email", key="email_input")

    if email:
        if not is_valid_email(email):
            st.error("Veuillez entrer une adresse email valide.")
        else:
            conn = database.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email=?", (email,))
            user_exists = cursor.fetchone()
            conn.close()

            if not user_exists:
                st.error("Cet email n'est pas enregistré. Veuillez créer un compte.")
                st.rerun()
            else:
                st.success("Email trouvé! Choisissez une méthode de connexion.")

                login_method = st.radio(
                    "Choisir une méthode de connexion",
                    ["Email et mot de passe", "Reconnaissance faciale", "Connexion Google"],
                    key=f"login_method_{email}"
                )

                if login_method == "Email et mot de passe":
                    password = st.text_input("Mot de passe", type="password", key=f"password_input_{email}")
                    if st.button("Se connecter avec Email et mot de passe", key=f"login_button_{email}"):
                        if email and password:
                            username = authenticate_email_password(email, password)
                            if username:
                                st.rerun()
                        else:
                            st.warning("Veuillez remplir tous les champs.")

                elif login_method == "Reconnaissance faciale":
                    username = authenticate_face(email)
                    if username:
                        st.rerun()  

                elif login_method == "Connexion Google":
                    google_user = authenticate_google()
                    if google_user:
                        st.rerun()  
    else:
        st.warning("Veuillez entrer votre email.")
