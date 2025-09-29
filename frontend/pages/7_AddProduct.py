import streamlit as st
import requests

st.subheader("Add Product")
with st.form("addProd"):
    name = st.text_input("Name")
    cat = st.text_input("Category")
    price = st.number_input("Price", min_value=1)
    stock = st.number_input("Stock", min_value=1)
    desc = st.text_input("Description")
    img_url = st.text_area("Image URL")
    submit = st.form_submit_button("Add Product")
if submit:
    BACKEND_URL = "http://localhost:8000/products/"
    try:
        resp = requests.post(BACKEND_URL, json={"name": name, "category": cat, "description": desc, "price": price, "stock": stock, "image_url": img_url}, timeout=5)
        print(f"AddProduct: status_code = {resp.status_code}")
        data = resp.json()
        print(resp.status_code)
        if resp.status_code == 200:
            st.success(f"Product {name} added.")
        else:
            st.error(data.get("error", "Product creation failed."))
    except Exception as e:
        st.error(f"Error connecting to backend:{e}")

if st.button("View All Products"):
    st.switch_page("pages/8_AllProducts.py")

if st.button("Go back to Dashboard"):
    st.switch_page("pages/6_Admin.py")