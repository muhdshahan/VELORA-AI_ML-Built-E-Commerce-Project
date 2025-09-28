import streamlit as st
import requests

st.title("Admin Dashboard")

if st.button("Add Product"):
    st.switch_page("pages/7_AddProduct.py")

if st.button("View All Products"):
    st.switch_page("pages/8_AllProducts.py")

# Fetch users from Backend
BACKEND_URL = "http://localhost:8000/admin/allusers"

try:
    resp = requests.get(
        BACKEND_URL,
        timeout=5
        )
    data = resp.json()
    print(data)
    print(resp.status_code)
    if resp.status_code == 200:
        st.subheader("Users")
        st.table(data)
    else:
        # Show error message from backend
        st.error(data.get("error", "Users retreival failed."))
except Exception as e:
    st.error(f"Error connecting to backend:{e}")


if st.button("Logout"):
    st.session_state.clear()
    st.switch_page("app.py")

