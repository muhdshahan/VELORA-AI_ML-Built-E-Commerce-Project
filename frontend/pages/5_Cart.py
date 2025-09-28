# pages/5_Cart.py
import streamlit as st

st.title("Your Cart")

if st.button("Logout"):
    fb = st.text_area("Feedback (required to logout):", key="user_feedback")
    if st.button("Submit Feedback & Logout") and fb.strip():
        # Save feedback & log out
        st.session_state.clear()
        st.switch_page("app.py")
    elif st.button("Submit Feedback & Logout"):
        st.error("Please enter feedback before logout.")

cart = st.session_state.setdefault("cart", [])
if not cart:
    st.info("Your cart is empty.")
else:
    total = 0
    for item in cart:
        st.write(f"{item['qty']} × {item['name']} - ₹{item['price']} each")
        total += item['qty'] * item['price']
        st.button("Remove", key=f"rm_{item['name']}")
    st.write(f"### Total: ₹{total}")
    if st.button("Checkout"):
        st.success("Order placed! Thank you.")
        st.session_state["orders"] = st.session_state.get("orders", []) + [{"items": cart, "total": total}]
        st.session_state["cart"] = []
