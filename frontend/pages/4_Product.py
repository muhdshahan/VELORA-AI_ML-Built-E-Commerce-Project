import streamlit as st
import requests

st.title("Product Detail")

if st.button("View Cart"):
        st.switch_page("pages/5_Cart.py")
if st.button("Go back to Catalog"):
        st.switch_page("pages/3_Catalog.py")

# Feedback/logout logic
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

# Product detail and backend-powered recommendations
p = st.session_state.get("selected_product")
token = st.session_state.get("token")
headers = {"Authorization": f"Bearer {token}"} if token else {}

if not p:
    st.info("No product data.")
else:
    st.write(f"#### {p['name']}")
    st.write(f"Category: {p['category']}")
    st.write(f"Price: ₹{p['price']}")
    st.write(f"Description: {p['description']}")
    st.write(f"Stock: {p['stock']}")

     # Fetch backend recommendations & log view
    st.write("##### Recommended Products")
    BACKEND_URL = f"http://localhost:8000/products/view{p['id']}"
    recommendations = []
    try:
        resp = requests.get(BACKEND_URL, headers=headers, timeout=5)
        if resp.status_code == 200:
            recommendations = resp.json()
        else:
            st.warning("Could not fetch recommendations.")
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")

    
    if recommendations:
        for rp in recommendations:
            st.write(rp.get('name'))
    else:
        st.info("No recommendations available.")

    # Add to Cart logic
    with st.form(key=f"cart_form_{p['id']}"):
            quantity = st.number_input("Qty", min_value=1, max_value=p['stock'], value=1)
            if st.form_submit_button("Add to Cart"):
                BACKEND_URL = "http://localhost:8000/cart/add"
                data = {
                    "product_id": p['id'],
                    "quantity": quantity
                }
                token = st.session_state.get("token", "")
                headers = {"Authorization": f"Bearer {token}"} if token else {}
                resp = requests.post(BACKEND_URL, json=data, headers=headers)
                if resp.status_code == 200:
                    st.success("Added to cart!")
                else:
                    st.error(f"Add to cart failed: {resp.text}")
