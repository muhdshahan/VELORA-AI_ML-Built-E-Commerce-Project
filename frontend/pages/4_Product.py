import streamlit as st
import requests

st.title("Product Detail")

if st.button("View Cart"):
        st.switch_page("pages/5_Cart.py")
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
                print(f"Catalog: user_id{user_id}, feedback{fb}")
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

p = st.session_state.get("selected_product")
if not p:
    st.info("No product data.")
else:
    st.write(f"#### {p['name']}")
    st.write(f"Category: {p['category']}")
    st.write(f"Price: ₹{p['price']}")
    st.write(f"Description: {p['description']}")
    st.write(f"Stock: {p['stock']}")

    # Simulate activity log for recommendations
    st.session_state.setdefault("activity", []).append({"user": st.session_state.get("user", {}).get("username"), "product_id": p["id"], "action": "viewed"})
    # Fallback "Recommendations" (actual: compute via backend in full app)
    st.write("##### Recommended Products")
    for rp in products[1:4]:
        st.write(rp['name'])

    st.button("Add to Cart")
