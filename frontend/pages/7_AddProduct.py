import streamlit as st

orders = st.session_state.get("orders", [])

st.subheader("Orders")
for o in orders:
    st.write(o)

st.subheader("Add Product")
with st.form("addProd"):
    name = st.text_input("Name")
    cat = st.text_input("Category")
    price = st.number_input("Price", min_value=1)
    stock = st.number_input("Stock", min_value=1)
    desc = st.text_input("Description")
    submit = st.form_submit_button("Add Product")
if submit:
    prods = st.session_state.setdefault("products", [])
    prods.append({"id":name.lower(),"name":name,"category":cat,"price":price,"desc":desc,"stock":stock})
    st.success(f"Product {name} added.")

if st.button("View All Products"):
    st.switch_page("pages/8_AllProducts.py")

if st.button("Go back to Dashboard"):
    st.switch_page("pages/6_Admin.py")