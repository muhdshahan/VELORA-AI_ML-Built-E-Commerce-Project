import streamlit as st
import requests

st.title("Product Catalog")

col1, col2 = st.columns([1, 1])   # Adjust ratios for sizing

with col1:
    if st.button("View Cart"):
        st.switch_page("pages/5_Cart.py")
with col2:
    if st.button("🔐 Logout"):
        st.switch_page("pages/2_Login.py")



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
                        st.error(resp.json().get("error", "Feedback storing."))
                except Exception as e:
                    st.error(f"Error connecting to backend: {e}")
            else:
                st.error("Please enter feedback before logout.")


# Sample products (backend: replace with GET /api/products)
sample_products = [
    {"id":"p01","name":"Stellar Sapphire Ring","category":"ring","price":299,"desc":"Sapphire in white gold.","stock":7},
    {"id":"p02","name":"Lunar Velvet Dress","category":"dress","price":189,"desc":"Navy velvet, gala style.","stock":8},
    {"id":"p03","name":"Astra Beaded Handbag","category":"bag","price":159,"desc":"Beaded constellation motifs.","stock":9},
    {"id":"p04","name":"Celestia Pendant","category":"necklace","price":210,"desc":"Star diamond pendant.","stock":5},
]
products = st.session_state.setdefault("products", sample_products)
search = st.text_input("Search products")

if search:
    results = [p for p in products if search.lower() in p["name"].lower() or search.lower() in p["category"].lower() or search.lower() in p["desc"].lower()]
else:
    results = products

st.write(f"{len(results)} products found:")

for p in results:
    st.write(f"**{p['name']}** ({p['category']}) ₹{p['price']} – {p['desc']}")
    cols = st.columns([1, 4, 2, 1])   # Adjust ratios for sizing
    with cols[1]:
        if st.button("View", key=p['id']+"_view"):
            st.session_state.clear()
            st.switch_page("pages/4_Product.py")
    with cols[2]:
        st.button("Add to Cart", key=p['id']+"_cart")
