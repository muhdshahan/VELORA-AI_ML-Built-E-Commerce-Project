import streamlit as st
import requests

st.title("Your Cart")

if st.button("Go back to Catalog"):
        st.switch_page("pages/3_Catalog.py")

if "show_logout_form" not in st.session_state:
    st.session_state.show_logout_form = False

if not st.session_state.show_logout_form:
    if st.button("Logout"):
        st.session_state.show_logout_form = True
else:
    with st.form("logout_form"):
        fb = st.text_area("Feedback (required to logout):")
        submitted = st.form_submit_button("Submit Feedback & Logout")
        if submitted:
            if fb.strip():
                BACKEND_URL = "http://localhost:8000/feedback/"
                user_id = st.session_state.get("user_id")
                try:
                    resp = requests.post(BACKEND_URL, json={"user_id": user_id, "text": fb}, timeout=5)
                    if resp.status_code == 200:
                        st.session_state.clear()
                        st.switch_page("app.py")
                    else:
                        st.error(resp.json().get("error", "Feedback storing error."))
                except Exception as e:
                    st.error(f"Error connecting to backend: {e}")
            else:
                st.error("Please enter feedback before logout.")

# Backend URL and token
BACKEND_URL = "http://localhost:8000/cart/"
token = st.session_state.get("token", "")
headers = {"Authorization": f"Bearer {token}"} if token else {}

# Fetch cart items from backend
cart = []
try:
    resp = requests.get(BACKEND_URL, headers=headers, timeout=5)
    if resp.status_code == 200:
        cart = resp.json()
    else:
        st.error("Error fetching cart: " + resp.text)
except Exception as e:
    st.error(f"Error connecting to backend: {e}")

if not cart:
    st.info("Your cart is empty.")
else:
    total = 0
    for item in cart:
        print(item)
        # Adjust these keys according to your CartItemOut model fields
        st.write(f"{item['quantity']} × {item['product']['name']} - ₹{item['product']['price']} each")  
        total += item['quantity'] * item['product']['price']
        # Optional: Add remove button per item if you implement a remove endpoint
        # st.button("Remove", key=f"rm_{item['id']}")
    st.write(f"### Total: ₹{total}")

    if st.button("Checkout"):
        st.success("Order placed! Thank you.")

