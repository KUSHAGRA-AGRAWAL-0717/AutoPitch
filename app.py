import os
import streamlit as st
import pandas as pd
from job_scraper import extract_job_details
from email_generator import generate_email

# Fix USER_AGENT warning
os.environ["USER_AGENT"] = "streamlit-app"

# Streamlit Page Configuration
st.set_page_config(page_title="Cold Email Generator", layout="wide")
st.title("Cold Email Generator")

# Sidebar for User Inputs
st.sidebar.header("🔹 User Information")
user_name = st.sidebar.text_input("Enter Your Full Name", placeholder="e.g., Kushagra Agrawal")
user_role = st.sidebar.text_input("Enter Your Current Role", placeholder="e.g., MERN Stack Developer")

st.sidebar.header("📂 Upload Your Portfolio")
uploaded_file = st.sidebar.file_uploader("Upload CSV (Projects & Skills)", type=["csv"])

portfolio_df = None
if uploaded_file:
    try:
        portfolio_df = pd.read_csv(uploaded_file)
        st.sidebar.success("✅ Portfolio Loaded Successfully!")
    except Exception as e:
        st.sidebar.error(f"❌ Error loading file: {e}")

# Job URL Input
job_url = st.text_input("🔗 Enter Job Posting URL")

# Ensure job_info is stored in session state for updates
if "job_info" not in st.session_state:
    st.session_state.job_info = None

# Debug: Print values to check
st.write("🔍 **Debug Info:**")
st.write(f"- User Name: {user_name}")
st.write(f"- User Role: {user_role}")
st.write(f"- Uploaded File: {'Yes' if uploaded_file else 'No'}")
st.write(f"- Job URL: {job_url}")

# Extract Job Details Button
if job_url and portfolio_df is not None and user_name and user_role:
    if st.button("Extract Job Details"):
        st.write("✅ **Extract Job Details button clicked!**")  # Debug print
        with st.spinner("🔄 Extracting job details..."):
            try:
                st.session_state.job_info = extract_job_details(job_url)
                if st.session_state.job_info:
                    st.write(f"🔍 **Job Info Extracted:** {st.session_state.job_info}")  # Debug print
                else:
                    st.error("❌ No job details found.")
            except Exception as e:
                st.error(f"❌ Error extracting job details: {e}")
                st.write(f"❌ **Debug Error:** {e}")

# Display extracted job details
if st.session_state.job_info:
    st.subheader("📌 Extracted Job Details")
    st.json(st.session_state.job_info)

# Generate Cold Email Button
if st.session_state.job_info and portfolio_df is not None and user_name and user_role:
    if st.button("Generate Cold Email"):
        st.write("✅ **Generate Cold Email button clicked!**")  # Debug print
        with st.spinner("✉️ Generating email..."):
            try:
                email_content = generate_email(st.session_state.job_info, portfolio_df, user_name, user_role)
                if email_content:
                    st.write(f"🔍 **Email Generated:** {email_content}")  # Debug print
                else:
                    st.error("❌ Failed to generate email.")
            except Exception as e:
                st.error(f"❌ Error generating email: {e}")
                st.write(f"❌ **Debug Error:** {e}")
                email_content = None
        
        # Display generated email
        if email_content:
            st.subheader("✉️ Generated Cold Email")
            st.text_area("Email Content", email_content, height=300)
