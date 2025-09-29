import streamlit as st
import requests

st.title("All Products")

col1, col2 = st.columns([1, 1])   # Adjust ratios for sizing

with col1:
    if st.button("Go back to Dashboard"):
        st.switch_page("pages/6_Admin.py")
with col2:
    if st.button("🔐 Logout"):
        st.switch_page("pages/2_Login.py")

if st.button("Logout"):
        st.switch_page("app.py")


BACKEND_URL = "http://localhost:8000/products/"
# Fetch products only once, cache in session
if "products" not in st.session_state:
    try:
        resp = requests.get(BACKEND_URL, timeout=5)
        print(f"Catalog2: {resp.status_code}")
        st.session_state.products = resp.json() if resp.status_code == 200 else []
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")
        st.session_state.products = []

products = st.session_state.products

search = st.text_input("Search products")

# Filter results based on search input
if search:
    results = [
        p for p in products
        if search.lower() in str(p.get("name", "")).lower()
        or search.lower() in str(p.get("category", "")).lower()
        or search.lower() in str(p.get("desc", "")).lower()
    ]
else:
    results = products

st.write(f"{len(results)} products found:")

for p in results:
    st.write(f"**{p['name']}** ({p['category']}) ₹{p['price']}")
    st.write(f"{p['description']}")
    # Display product image as a thumbnail (height=80 pixels, can adjust)
    if p.get('image_url'):
        st.image(p['image_url'], width=80)  # Use width OR height for thumbnail effect