import streamlit as st
import login
import appCBIR  



if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if 'user_info' not in st.session_state:
    st.session_state['user_info'] = {}

if not st.session_state['authenticated']:
    st.error("You have to login!")
    login.show_login_page()


else:

    st.sidebar.title("Navigation")
    st.sidebar.markdown("Logged in as")
    
    username = st.session_state['user_info'].get("username") or st.session_state['user_info'].get("name", "Unknown")
    email = st.session_state['user_info'].get("email", "No email")
    
    st.sidebar.success(f"Username : {username}")
    st.sidebar.write(f"Email : {email}")
    
    if st.sidebar.button(" Logout"):
        st.session_state['authenticated'] = False
        st.session_state['user_info'] = {}
        st.success("You have been logged out.")
        st.rerun()

    # Main page
    st.title(f"Welcome back, {username} !")
    st.write("CBIR System !")
    
    appCBIR.main()