import streamlit as st

st.markdown("""
<style>
div.stButton > button {
  font-size: 1.17rem;
  font-weight: bold;
  padding: 0.7em 2.25em;
  box-shadow: 0 3px 18px #1c295644;
  margin: 18px 18px 12px 0 !important;
  transition: background 0.17s, color 0.17s, border 0.17s;
}
</style>
""", unsafe_allow_html=True)

st.title("💎 Velora – Premium Jewels & Clothing")
st.image("banner.jpeg")


st.write("""
✨ Welcome to Velora, your destination for premium jewels and clothing.<br>
Enjoy a night-sky themed shopping experience!  
""", unsafe_allow_html=True)

# Place buttons side by side
cols= st.columns([1, 4, 2, 1])   # Adjust ratios for sizing

with cols[1]:
    if st.button("📝 Register"):
        st.switch_page("pages/1_Register.py")
with cols[2]:
    if st.button("🔐 Login"):
        st.switch_page("pages/2_Login.py")


