import streamlit as st
from main import run_tracker

st.title("Competitor Feature Tracker - Email Dashboard")

st.write("Enter your email address to receive the latest competitor updates after scraping.")

email = st.text_input("Email Address", "")

if st.button("Send Updates"):
    if email:
        try:
            run_tracker(email=email)
            st.success(f"Updates sent to {email}!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid email address.") 