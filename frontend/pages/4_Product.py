# pages/4_Product.py
import streamlit as st

st.title("Product Detail")

if st.button("View Cart"):
        st.session_state.clear()
        st.switch_page("pages/5_Cart.py")

if st.button("Logout"):
    fb = st.text_area("Feedback (required to logout):", key="user_feedback")
    if st.button("Submit Feedback & Logout") and fb.strip():
        # Save feedback & log out
        st.session_state.clear()
        st.switch_page("app.py")
    elif st.button("Submit Feedback & Logout"):
        st.error("Please enter feedback before logout.")

# In real app, product ID comes from URL param or selection logic
products = st.session_state.get("products", [])
# For demo just pick first product
p = products[0] if products else None
if not p:
    st.info("No product data.")
else:
    st.write(f"#### {p['name']}")
    st.write(f"Category: {p['category']}")
    st.write(f"Price: ₹{p['price']}")
    st.write(f"Description: {p['desc']}")
    st.write(f"Stock: {p['stock']}")

    # Simulate activity log for recommendations
    st.session_state.setdefault("activity", []).append({"user": st.session_state.get("user", {}).get("username"), "product_id": p["id"], "action": "viewed"})
    # Fallback "Recommendations" (actual: compute via backend in full app)
    st.write("##### Recommended Products")
    for rp in products[1:4]:
        st.write(rp['name'])

    st.button("Add to Cart", key="add_to_cart")
