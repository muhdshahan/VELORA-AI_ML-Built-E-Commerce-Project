import streamlit as st
import requests

st.title("Login to Velora")

with st.form("loginForm"):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")

if submit:
    # Backend endpoint URL
    BACKEND_URL = "http://localhost:8000/auth/login"
    try:
        resp = requests.post(
            BACKEND_URL,
            json={"email": email, "password": password},
            timeout=5
        )
        data = resp.json()
        if resp.status_code == 200:
            # Save token to session 
            st.session_state.token = data.get("access_token") or data.get("token")
            st.session_state.role = data.get("role")
            if data["role"] == "admin":
                st.switch_page("pages/6_Admin.py")
            else:
                st.session_state.user_id = data["user_id"]
                st.switch_page("pages/3_Catalog.py")
        else:
            # Show error message from backend
            st.error(data.get("error", "Login failed."))
    except Exception as e:
        st.error(f"Error connecting to backend:{e}")


if st.button("Don't have an account? Register"):
    st.switch_page("pages/1_Register.py")



