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
    BACKEND_URL = "http://localhost:8000/search/smart"
    try:
        resp = requests.post(BACKEND_URL, json={"query": search}, timeout=10)
        if resp.status_code == 200:
            results = resp.json()
            st.write(f"{len(results)} products found:")
            for p in results:
                st.write(f"**{p['name']}** ({p['category']}) ₹{p['price']} – {p['description']}")
        else:
            st.warning("No results found.")
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")
else:
    results = products

st.write(f"{len(results)} products found:")

for p in results:
    st.write(f"**{p['name']}** ({p['category']}) ₹{p['price']} – {p['description']}")
    # Display product image as a thumbnail (height=80 pixels, can adjust)
    if p.get('image_url'):
        st.image(p['image_url'], width=80)  # Use width OR height for thumbnail effect
    
    cols = st.columns([1, 4, 2, 1])
    with cols[1]:
        if st.button("View", key=str(p['id'])+"_view"):
            st.session_state.selected_product = p  
            st.switch_page("pages/4_Product.py")
    with cols[2]:
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

