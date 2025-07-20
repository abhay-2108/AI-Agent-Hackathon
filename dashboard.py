import streamlit as st
import subprocess
import sys

st.title("Competitor Feature Tracker - Email Dashboard")

st.write("Enter your email address to receive the latest competitor updates after scraping.")

email = st.text_input("Email Address", "")

if st.button("Send Updates"):
    if email:
        # Call main.py with the email as an argument
        try:
            result = subprocess.run([sys.executable, "main.py", "--email", email], capture_output=True, text=True)
            if result.returncode == 0:
                st.success(f"Updates sent to {email}!")
            else:
                st.error(f"Failed to send updates. Error: {result.stderr}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid email address.") 